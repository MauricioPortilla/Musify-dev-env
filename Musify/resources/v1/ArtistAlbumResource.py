from flask_restful import Resource
from Model import database, Album, AlbumSchema, AlbumArtist, AlbumArtistSchema
from flask import request
import json

albums_schema = AlbumSchema(many=True)
albumArtists_schema = AlbumArtistSchema(many=True)
albumArtist_schema = AlbumArtistSchema()

class ArtistAlbumResource(Resource):
    def get(self, artist_id):
        albumArtists = AlbumArtist.query.filter_by(artist_id=artist_id)
        albums = []
        for album in albumArtists:
            albums.append(Album.query.filter_by(album_id=album.album_id).first())
        return { "status": "success", "data": albums_schema.dump(albums).data }, 200
