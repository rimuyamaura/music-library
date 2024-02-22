from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym
from music.domainmodel import model

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table('users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), nullable=False),
    Column('password', String(225), nullable=False),

)

playlists_table = Table('playlists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id'))
)
playlist_tracks_table = Table('playlist_tracks', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('playlist_id', ForeignKey('playlists.id')),
    Column('track_id', ForeignKey('tracks.id'))
)
playlist_liked_by_table = Table('playlist_liked_by', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('playlist_id', ForeignKey('playlists.id'), unique=False),
    Column('user_name', ForeignKey('users.user_name'), unique=False)
)

tracks_table = Table('tracks', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('artist', ForeignKey('artists.artist_id')),
    Column('album', ForeignKey('albums.album_id')),
    Column('track_url', String(255), nullable=True),
    Column('track_duration', Integer, nullable=True)
)

artists_table = Table('artists', metadata,
    Column('artist_id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(255), nullable=False)
)

albums_table = Table('albums', metadata,
    Column('album_id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('album_url', String(255), nullable=True),
    Column('album_type', String(255), nullable=True),
    Column('release_year', Integer, nullable=True)
)

genres_table = Table('genres', metadata,
    Column('genre_id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False)
)

track_genres_table = Table('track_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.id')),
    Column('genre_id', ForeignKey('genres.genre_id'))
)

reviews_table = Table('reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('track_id', ForeignKey('tracks.id')),
    Column('review_text', String(1024), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

def map_model_to_tables():
    mapper(model.User, users_table, properties={
        '_User__user_id': users_table.c.id,
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(model.Review, backref='_Review__user'),
        '_User__playlist': relationship(model.PlayList, backref='_Playlist__user'),
        '_User__liked_playlists': relationship(model.PlayList, secondary=playlist_liked_by_table, back_populates='_PlayList__liked_by')
    })

    mapper(model.PlayList, playlists_table, properties={
        '_Track__track_id': playlists_table.c.id,
        '_PlayList__list_of_tracks': relationship(model.Track, secondary=playlist_tracks_table, back_populates='_Track__playlist'),
        '_PlayList__liked_by': relationship(model.User, secondary=playlist_liked_by_table, back_populates='_User__liked_playlists')
    })

    mapper(model.Track, tracks_table, properties={
        '_Track__track_id': tracks_table.c.id,
        '_Track__title': tracks_table.c.title,
        '_Track__artist_id': tracks_table.c.artist,
        '_Track__album_id': tracks_table.c.album,
        '_Track__track_url': tracks_table.c.track_url,
        '_Track__track_duration': tracks_table.c.track_duration,
        
        '_Track__genres': relationship(model.Genre, secondary=track_genres_table, back_populates='_Genre__tracks'),

        '_Track__playlist': relationship(model.PlayList, secondary=playlist_tracks_table,
                                         back_populates='_PlayList__list_of_tracks'),
        '_Track__reviews': relationship(model.Review, backref='_Review__track'),
    })

    mapper(model.Album, albums_table, properties={
        '_Album__album_id': albums_table.c.album_id,
        '_Album__title': albums_table.c.title,
        '_Album__album_url': albums_table.c.album_url,
        '_Album__album_type': albums_table.c.album_type,
        '_Album__release_year': albums_table.c.release_year,
        '_Album__track' : relationship(model.Track, backref='_Track__album')
    })
    mapper(model.Artist, artists_table, properties={
        '_Artist__artist_id': artists_table.c.artist_id,
        '_Artist__full_name': artists_table.c.full_name,
        '_Artist__track': relationship(model.Track, backref='_Track__artist')
    })
    mapper(model.Genre, genres_table, properties={
        '_Genre__genre_id': genres_table.c.genre_id,
        '_Genre__name' : genres_table.c.name,
        '_Genre__tracks' : relationship(model.Track, secondary=track_genres_table, back_populates='_Track__genres'),
    })

    mapper(model.Review, reviews_table, properties={
        '_Review__user_id' : reviews_table.c.user_id,
        '_Review__review_text': reviews_table.c.review_text,
        '_Review__rating': reviews_table.c.rating,
        '_Review__timestamp': reviews_table.c.timestamp,
    })