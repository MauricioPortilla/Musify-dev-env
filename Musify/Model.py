from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

marshmallow = Marshmallow()
database = SQLAlchemy()

class Account(database.Model):
    __tablename__ = "account"
    account_id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(255), unique=True, nullable=False)
    password = database.Column(database.String(255), nullable=False)
    name = database.Column(database.String(50), nullable=False)
    last_name = database.Column(database.String(50), nullable=False)
    second_last_name = database.Column(database.String(50), nullable=True)
    creation_date = database.Column(database.Date, nullable=False)

    def __init__(self, email, password, name, last_name, second_last_name):
        self.email = email
        self.password = password
        self.name = name
        self.last_name = last_name
        self.second_last_name = second_last_name

class AccountSchema(marshmallow.Schema):
    account_id = fields.Integer(dump_only=True)
    email = fields.String(required=True, validate=validate.Length(255))
    password = fields.String(required=True)
    name = fields.String(required=True, validate=validate.Length(50))
    last_name = fields.String(required=True, validate=validate.Length(50))
    second_last_name = fields.String(required=False, validate=validate.Length(50))
    creation_date = fields.Date()

class Subscription(database.Model):
    __tablename__ = "subscription"
    subscription_id = database.Column(database.Integer, primary_key=True)
    account_id = database.Column(database.Integer, database.ForeignKey("account.account_id"), nullable=False)
    account = database.relationship("Account", backref=database.backref("account_subscription", lazy="dynamic"))
    cost = database.Column(database.Float, nullable=False)
    startDate = database.Column(database.Date, nullable=False)
    endDate = database.Column(database.Date, nullable=False)

class SubscriptionSchema(marshmallow.Schema):
    subscription_id = fields.Integer(dump_only=True)
    account_id = fields.Integer(required=True)
    cost = fields.Float(required=True)
    startDate = fields.Date()
    endDate = fields.Date()

class AccountSong(database.Model):
    __tablename__ = "account_song"
    account_song_id = database.Column(database.Integer, primary_key=True)
    account_id = database.Column(database.Integer, database.ForeignKey("account.account_id"), nullable=False)
    account = database.relationship("Account", backref=database.backref("account_accountsong", lazy="dynamic"))
    title = database.Column(database.String(50), nullable=False)
    song_location = database.Column(database.String(255), nullable=False)
    upload_date = database.Column(database.Date, nullable=False)

    def __init__(self, account_id, title, song_location, upload_date):
        self.account_id = account_id
        self.title = title
        self.song_location = song_location
        self.upload_date = upload_date

class AccountSongSchema(marshmallow.Schema):
    account_song_id = fields.Integer(dump_only=True)
    account_id = fields.Integer(required=True)
    title = fields.String(required=True, validate=validate.Length(50))
    song_location = fields.String(required=True, validate=validate.Length(255))
    upload_date = fields.Date()

class Playlist(database.Model):
    __tablename__ = "playlist"
    playlist_id = database.Column(database.Integer, primary_key=True)
    account_id = database.Column(database.Integer, database.ForeignKey("account.account_id"), nullable=False)
    account = database.relationship("Account", backref=database.backref("account_playlist", lazy="dynamic"))
    name = database.Column(database.String(20), nullable=False)

    def __init__(self, account_id, name):
        self.account_id = account_id
        self.name = name

class PlaylistSchema(marshmallow.Schema):
    playlist_id = fields.Integer(dump_only=True)
    account_id = fields.Integer(required=True)
    name = fields.String(required=True, validate=validate.Length(20))

class Album(database.Model):
    __tablename__ = "album"
    album_id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(25), nullable=False)
    launch_year = database.Column(database.Integer, nullable=False)
    discography = database.Column(database.String(50), nullable=False)
    image_location = database.Column(database.String(255), nullable=False)

    def __init__(self, name, launch_year, discography, image_location):
        self.name = name
        self.launch_year = launch_year
        self.discography = discography
        self.image_location = image_location

class AlbumSchema(marshmallow.Schema):
    album_id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(25))
    launch_year = fields.Integer(required=True)
    discography = fields.String(required=True, validate=validate.Length(50))
    image_location = fields.String(required=True, validate=validate.Length(255))

class Genre(database.Model):
    genre_id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(15), nullable=False)

    def __init__(self, name):
        self.name = name

class GenreSchema(marshmallow.Schema):
    genre_id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(15))

class Song(database.Model):
    song_id = database.Column(database.Integer, primary_key=True)
    album_id = database.Column(database.Integer, database.ForeignKey("album.album_id"), nullable=False)
    album = database.relationship("Album", backref=database.backref("album_song", lazy="dynamic"))
    genre_id = database.Column(database.Integer, database.ForeignKey("genre.genre_id"), nullable=False)
    genre = database.relationship("Genre", backref=database.backref("genre_song", lazy="dynamic"))
    title = database.Column(database.String(30), nullable=False)

    def __init__(self, album_id, genre_id, title):
        self.album_id = album_id
        self.genre_id = genre_id
        self.title = title

class SongSchema(marshmallow.Schema):
    song_id = fields.Integer(dump_only=True)
    album_id = fields.Integer(required=True)
    genre_id = fields.Integer(required=True)
    title = fields.String(required=True, validate=validate.Length(30))

class SongRate(database.Model):
    song_rate_id = database.Column(database.Integer, primary_key=True)
    account_id = database.Column(database.Integer, database.ForeignKey("account.account_id"), nullable=False)
    account = database.relationship("Account", backref=database.backref("account_songrate", lazy="dynamic"))
    song_id = database.Column(database.Integer, database.ForeignKey("song.song_id"), nullable=False)
    song = database.relationship("Song", backref=database.backref("song_songrate", lazy="dynamic"))
    rate = database.Column(database.Integer, nullable=False)

    def __init__(self, account_id, song_id, rate):
        self.account_id = account_id
        self.song_id = song_id
        self.rate = rate

class SongRateSchema(marshmallow.Schema):
    song_rate_id = fields.Integer(dump_only=True)
    account_id = fields.Integer(required=True)
    song_id = fields.Integer(required=True)
    rate = fields.Integer(required=True)

class Artist(database.Model):
    artist_id = database.Column(database.Integer, primary_key=True)
    account_id = database.Column(database.Integer, database.ForeignKey("account.account_id"), nullable=False)
    account = database.relationship("Account", backref=database.backref("account_artist", lazy="dynamic"))
    name = database.Column(database.String(50), nullable=False)
    last_name = database.Column(database.String(50), nullable=False)
    second_last_name = database.Column(database.String(50), nullable=True)

    def __init__(self, account_id, name, last_name, second_last_name):
        self.account_id = account_id
        self.name = name
        self.last_name = last_name
        self.second_last_name = second_last_name

class ArtistSchema(marshmallow.Schema):
    artist_id = fields.Integer(dump_only=True)
    account_id = fields.Integer(required=True)
    name = fields.String(required=True, validate=validate.Length(50))
    last_name = fields.String(required=True, validate=validate.Length(50))
    second_last_name = fields.String(required=False, validate=validate.Length(50))

class PlaylistSong(database.Model):
    playlist_id = database.Column(database.Integer, database.ForeignKey("playlist.playlist_id"), primary_key=True)
    playlist = database.relationship("Playlist", backref=database.backref("playlist_playlistsong", lazy="dynamic"))
    song_id = database.Column(database.Integer, database.ForeignKey("song.song_id"), primary_key=True)
    song = database.relationship("Song", backref=database.backref("song_playlistsong", lazy="dynamic"))

    def __init__(self):
        self.playlist_id = playlist_id
        self.song_id = song_id

class PlaylistSongSchema(marshmallow.Schema):
    playlist_id = fields.Integer(required=True)
    song_id = fields.Integer(required=True)

class AlbumArtist(database.Model):
    album_id = database.Column(database.Integer, database.ForeignKey("album.album_id"), primary_key=True)
    album = database.relationship("Album", backref=database.backref("album_albumartist", lazy="dynamic"))
    artist_id = database.Column(database.Integer, database.ForeignKey("artist.artist_id"), primary_key=True)
    artist = database.relationship("Artist", backref=database.backref("artist_albumartist", lazy="dynamic"))

    def __init__(self, album_id, artist_id):
        self.album_id = album_id
        self.artist_id = artist_id

class AlbumArtistSchema(marshmallow.Schema):
    album_id = fields.Integer(required=True)
    artist_id = fields.Integer(required=True)

class SongArtist(database.Model):
    song_id = database.Column(database.Integer, database.ForeignKey("song.song_id"), primary_key=True)
    song = database.relationship("Song", backref=database.backref("song_songartist", lazy="dynamic"))
    artist_id = database.Column(database.Integer, database.ForeignKey("artist.artist_id"), primary_key=True)
    artist = database.relationship("Artist", backref=database.backref("artist_songartist", lazy="dynamic"))
    
    def __init__(self, song_id, artist_id):
        self.song_id = song_id
        self.artist_id = artist_id

class AlbumArtistSchema(marshmallow.Schema):
    song_id = fields.Integer(required=True)
    artist_id = fields.Integer(required=True)

class ArtistGenre(database.Model):
    genre_id = database.Column(database.Integer, database.ForeignKey("genre.genre_id"), primary_key=True)
    genre = database.relationship("Genre", backref=database.backref("genre_artistgenre", lazy="dynamic"))
    artist_id = database.Column(database.Integer, database.ForeignKey("artist.artist_id"), primary_key=True)
    artist = database.relationship("Artist", backref=database.backref("artist_artistgenre", lazy="dynamic"))

    def __init__(self, genre_id, artist_id):
        self.genre_id = genre_id
        self.artist_id = artist_id

class ArtistGenreSchema(marshmallow.Schema):
    genre_id = fields.Integer(required=True)
    artist_id = fields.Integer(required=True)
