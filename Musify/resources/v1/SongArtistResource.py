from flask_restful import Resource
from Model import database, Artist, ArtistSchema, SongArtist, SongArtistSchema
from flask import request
from .AuthResource import auth_token
import json

artists_schema = ArtistSchema(many=True)
artist_schema = ArtistSchema()

class SongArtistResource(Resource):
    @auth_token
    def get(self, account, song_id):
        song_artists = SongArtist.query.filter_by(song_id=song_id)
        artists = []
        for artist in song_artists:
            artists.append(Artist.query.filter_by(artist_id=artist.artist_id).first())
        return { "status": "success", "data": artists_schema.dump(artists).data }, 200
