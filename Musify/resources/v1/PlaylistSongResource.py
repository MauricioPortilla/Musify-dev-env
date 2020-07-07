from flask_restful import Resource
from Model import database, Playlist, PlaylistSong, PlaylistSongSchema, Song, SongSchema
from flask import request, Response
from .AuthResource import auth_token
from .lang.lang import get_request_message

playlist_song_schema = PlaylistSongSchema()
song_schema = SongSchema()
songs_schema = SongSchema(many=True)

class PlaylistSongResource(Resource):
    @auth_token
    def get(self, account, playlist_id, song_id=None):
        playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()
        if not playlist:
            return { "status": "failed", "message": get_request_message(request, "NON_EXISTENT_PLAYLIST") }, 422
        if account.account_id != playlist.account_id:
            return { "status": "failed", "message": get_request_message(request, "UNAUTHORIZED") }, 401

        if (song_id is None):
            playlist_songs = PlaylistSong.query.filter_by(playlist_id=playlist_id)
            songs = []
            for playlist_song in playlist_songs:
                song = Song.query.filter_by(song_id=playlist_song.song_id, status="ready").first()
                songs.append(song)
            return { "status": "success", "data": songs_schema.dump(songs).data }
        else:
            playlist_song = PlaylistSong.query.filter_by(playlist_id=playlist_id, song_id=song_id).first()
            if not playlist_song:
                return { "status": "failed", "message": get_request_message(request, "SONG_NOT_IN_PLAYLIST") }, 422
            song = Song.query.filter_by(song_id=playlist_song.song_id, status="ready").first()
            return { "status": "success", "data": song_schema.dump(song).data }
            
    @auth_token
    def post(self, account, playlist_id):
        json_data = request.get_json()
        if (not json_data):
            return { "status": "failed", "message": get_request_message(request, "NO_INPUT_DATA_PROVIDED") }, 400
        playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()
        if not playlist:
            return { "status": "failed", "message": get_request_message(request, "NON_EXISTENT_PLAYLIST") }, 422
        if account.account_id != playlist.account_id:
            return { "status": "failed", "message": get_request_message(request, "UNAUTHORIZED") }, 401
        if (PlaylistSong.query.filter_by(playlist_id=playlist_id, song_id=json_data["song_id"]).first()):
            return { "status": "failed", "message": get_request_message(request, "SONG_ALREADY_IN_PLAYLIST") }, 409
        playlist_song = PlaylistSong(playlist_id=playlist_id, song_id=json_data["song_id"])
        database.session.add(playlist_song)
        database.session.commit()
        result = playlist_song_schema.dump(playlist_song).data
        return { "status": "success", "data": result }, 201

    @auth_token
    def delete(self, account, playlist_id, song_id):
        playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()
        if not playlist:
            return { "status": "failed", "message": get_request_message(request, "NON_EXISTENT_PLAYLIST") }, 422
        if account.account_id != playlist.account_id:
            return { "status": "failed", "message": get_request_message(request, "UNAUTHORIZED") }, 401
        song = PlaylistSong.query.filter_by(playlist_id=playlist_id, song_id=song_id).first()
        database.session.delete(song)
        database.session.commit()
        return { "status": "success", "message": get_request_message(request, "SONG_DELETED_FROM_PLAYLIST") }, 200
