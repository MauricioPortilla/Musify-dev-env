from flask_restful import Resource
from Model import database, Artist, ArtistSchema, SongArtist, SongArtistSchema
from flask import request
from resources.v1.AuthResource import auth_token
import json

artists_schema = ArtistSchema(many=True)
artist_schema = ArtistSchema()

class SongArtistResource(Resource):
    @auth_token
    def get(self, account, song_id):
        songArtists = SongArtist.query.filter_by(song_id=song_id)
        artists = []
        for artist in songArtists:
            artists.append(Artist.query.filter_by(artist_id=artist.artist_id).first())
        return { "status": "success", "data": artists_schema.dump(artists).data }, 200