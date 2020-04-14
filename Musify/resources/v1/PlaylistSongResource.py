from flask_restful import Resource
from Model import database, PlaylistSong, PlaylistSongSchema, Song, SongSchema
from flask import request, Response

playlist_song_schema = PlaylistSongSchema()
song_schema = SongSchema()
songs_schema = SongSchema(many=True)

class PlaylistSongResource(Resource):
    def get(self, playlist_id, song_id=None):
        if (song_id is None):
            playlistSongs = PlaylistSong.query.filter_by(playlist_id=playlist_id)
            songs = []
            for playlistSong in playlistSongs:
                song = Song.query.filter_by(song_id=playlistSong.song_id).first()
                songs.append(song)
            return { "status": "success", "data": songs_schema.dump(songs).data }
        else:
            playlistSong = PlaylistSong.query.filter_by(playlist_id=playlist_id, song_id=song_id).first()
            if (not playlistSong):
                return { "status": "failed", 'message': 'Playlist does not have this song.' }, 401
            song = Song.query.filter_by(song_id=playlistSong.song_id).first()
            return { "status": "success", "data": song_schema.dump(song).data }
            
    def post(self, playlist_id):
        json_data = request.get_json()
        if (not json_data):
            return { "status": "failed", 'message': 'No input data provided' }, 400
        if (PlaylistSong.query.filter_by(playlist_id=playlist_id, song_id=json_data["song_id"]).first()):
            return { "status": "failed", 'message': 'Playlist already has this song.' }, 401
        playlistSong = PlaylistSong(playlist_id=playlist_id, song_id=json_data["song_id"])
        database.session.add(playlistSong)
        database.session.commit()
        result = playlist_song_schema.dump(playlistSong).data
        return { "status": "success", "data": result }, 201
