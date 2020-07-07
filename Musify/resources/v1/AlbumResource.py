from flask_restful import Resource
from Model import database, Album, AlbumSchema, AlbumArtist, AlbumArtistSchema, Song, SongSchema, SongArtist, SongArtistSchema
from flask import request
from .AuthResource import auth_token
from .lang.lang import get_request_message
import json

albums_schema = AlbumSchema(many=True)
album_schema = AlbumSchema()
song_schema = SongSchema()

class AlbumResource(Resource):
    @auth_token
    def get(self, account, album_id):
        album = Album.query.filter_by(album_id=album_id).first()
        if not album:
            return { "status": "failed", "message": get_request_message(request, "NON_EXISTENT_ALBUM") }, 422
        return { "status": "success", "data": album_schema.dump(album).data }, 200

    @auth_token
    def post(self, account):
        json_data = request.get_json()
        if not json_data:
            return { "status": "failed", "message": get_request_message(request, "NO_INPUT_DATA_PROVIDED") }, 400
        data, errors = album_schema.load(json_data)
        if errors:
            return errors, 422
        album = Album(
            type=data["type"], 
            name=data["name"], 
            launch_year=data["launch_year"], 
            discography=data["discography"], 
            image_location=data["image_location"]
        )
        database.session.add(album)
        database.session.commit()
        result_album = album_schema.dump(album).data
        for artist in json_data["artists_id"]:
            album_artist = AlbumArtist(result_album["album_id"], artist["artist_id"])
            database.session.add(album_artist)
        for new_song in json_data["new_songs"]:
            song = Song(
                album_id=result_album["album_id"], 
                genre_id=new_song["genre_id"], 
                title=new_song["title"], 
                duration=new_song["duration"], 
                song_location=new_song["song_location"], 
                status="pending"
            )
            database.session.add(song)
            database.session.commit()
            result_song = song_schema.dump(song).data
            for artist in new_song["artists_id"]:
                song_artist = SongArtist(result_song["song_id"], artist["artist_id"])
                database.session.add(song_artist)
            database.session.commit()
        return { "status": "success", "data": result_album }, 201
