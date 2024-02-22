import pytest
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from music.domainmodel.model import make_review, make_genre_association
from music.adapters.repository import AbstractRepository
from music.domainmodel.model import  make_genre_association, make_review, ModelException
from music.adapters.repository import AbstractRepository, RepositoryException
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.playlist import PlayList
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User


def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]

def insert_track(empty_session, values = None):
    new_title = "title"
    new_url = "url"
    new_duration = 0

    if values is not None:
        new_title= values[0]
        new_url = values[1]
        new_duration = values[2]

    empty_session.execute('INSERT INTO tracks (title, track_url, track_duration) VALUES (:title, :track_url, :track_duration)',
                          {'title': new_title, 'track_url' : new_url, 'track_duration' :new_duration})
    row = empty_session.execute('SELECT id from tracks where title = :title',
                                {'title': new_title}).fetchone()
    return row[0]

def insert_genre(empty_session, values = None):
    name = "name"
    if values is not None:
        name= values[0]
    empty_session.execute(
        'INSERT INTO genres (name) VALUES (:name)',
        {'name': name})
    row = empty_session.execute('SELECT genre_id from genres',
                                {'name': name}).fetchone()
    return row[0]


def insert_artist(empty_session, values = None):
    full_name = "artist"
    if values is not None:
        full_name= values[0]

    empty_session.execute(
        'INSERT INTO artists (full_name) VALUES (:full_name)',
        {'full_name': full_name})
    row = empty_session.execute('SELECT artist_id from artists',
                                {'full_name': full_name}).fetchone()
    return row[0]

def insert_album(empty_session, values = None):
    title = "album"
    album_url = "url"
    album_type = "some_type"
    release_year = 2020

    if values is not None:
        title= values[0]
        album_url = values[1]
        album_type = values[2]
        release_year = values[3]

    empty_session.execute(
        'INSERT INTO albums (title, album_url, album_type, release_year) VALUES (:title, :album_url, :album_type, :release_year)',
        {'title': title, 'album_url' : album_url, 'album_type' : album_type, 'release_year' : release_year })
    row = empty_session.execute('SELECT album_id from albums',
                                {'title': title}).fetchone()
    return row[0]



def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_commented_track(empty_session):
    track_key = insert_track(empty_session)
    user_key = insert_user(empty_session)

    timestamp_1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute(
        'INSERT INTO reviews (user_id, track_id, review_text, rating, timestamp) VALUES '
        '(:user_id, :track_id, "Comment 1", 5,  :timestamp_1),'
        '(:user_id, :track_id, "Comment 2", 5, :timestamp_2)',
        {'user_id': user_key, 'track_id': track_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute('SELECT id from tracks').fetchone()
    return row[0]

def insert_playlist_track_association(empty_session, track_keys, playlist_key):

    stmt = 'INSERT INTO playlist_tracks (playlist_id, track_id) VALUES (:playlist_id, :track_id)'
    for track_key in track_keys:
        empty_session.execute(stmt, {'playlist_id': playlist_key, 'track_id': track_key})

def insert_track_genre_association(empty_session, track_key, genre_keys):
    stmt = 'INSERT INTO track_genres (genre_id, track_id) VALUES (:genre_id, :track_id)'
    for genre_key in genre_keys:
        empty_session.execute(stmt, {'genre_id': genre_key, 'track_id': track_key})



def insert_playlist(empty_session):
    user_id = insert_user(empty_session)
    empty_session.execute(
        'INSERT INTO playlists (user_id) VALUES '
        '(:user_id),'
        '(:user_id)',
        {'user_id': user_id}
    )
    row = empty_session.execute('SELECT id from playlists').fetchone()
    return row[0]








def test_loading_of_users(empty_session):

    id = insert_user(empty_session)
    user = User(id, "Andrew", "1234")
    #print(user.user_name)

    expected = [
        User(id, "Andrew", "1234")
    ]
    assert empty_session.query(User).all() == expected

def test_loading_of_artist(empty_session):
    id = insert_artist(empty_session)
    expected = [
        Artist(id, "artist")
    ]
    assert empty_session.query(Artist).all() == expected

def test_loading_of_album(empty_session):
    id = insert_album(empty_session)
    expected = [
        Album(id, "album")
    ]
    assert empty_session.query(Album).all() == expected


def test_loading_of_genre(empty_session):
    id = insert_genre(empty_session)
    expected = [
        Genre(id, "name")
    ]
    assert empty_session.query(Genre).all() == expected


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, (0, "Andrew", "1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User(1, "Andrew", "111")
        empty_session.add(user)
        empty_session.commit()



def test_loading_of_tracks(empty_session):
    id = insert_track(empty_session)

    expected = [
        Track(id, "title")
    ]
    assert empty_session.query(Track).all() == expected


def test_loading_of_commented_track(empty_session):
    insert_commented_track(empty_session)

    row = empty_session.query(Track).all()
    inserted_track = row[0]
    rows = empty_session.query(Review).all()
    inserted_review = rows[0]
    assert inserted_review.track == inserted_track

def test_loading_saving_of_track_with_artist(empty_session):
    track = Track(0, "title")
    track.track_url = "test"
    track.track_duration = 0
    artist = Artist(0, "artist")
    track.artist = artist

    empty_session.add(track)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT title, artist, track_url FROM tracks'))
    assert rows == [("title", 0, "test")]

def test_loading_saving_of_track_with_album(empty_session):
    track = Track(0, "title")
    track.track_url = "test"
    track.track_duration = 0
    album = Album(0, "artist")
    track.album = album

    empty_session.add(track)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT title, album, track_url FROM tracks'))
    assert rows == [("title", 0, "test")]


def test_loading_playlist(empty_session):
    insert_playlist(empty_session)
    row = empty_session.query(User).all()
    inserted_user = row[0]
    #assert isinstance(inserted_user, User)

    rows = empty_session.query(PlayList).all()
    inserted_playlist = rows[0]
    inserted_favorite = rows[1]
    #assert isinstance(inserted_favorite, PlayList)

    assert inserted_user.playlist == inserted_playlist
    assert inserted_user.liked_tracks == inserted_favorite.list_of_tracks



def test_saving_of_users(empty_session):


    user = User(0, "Andrew", "1234Hanx")

    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("andrew", "1234Hanx")]


def test_saving_of_tracks(empty_session):
    track = Track(0, "title")
    track.track_url = "test"
    track.track_duration = 0
    empty_session.add(track)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT title, track_url FROM tracks'))
    assert rows == [("title", "test")]

def test_saving_of_artist(empty_session):
    artist = Artist(0, "artist")
    empty_session.add(artist)
    empty_session.commit()
    rows = list(empty_session.execute('SELECT full_name FROM artists'))
    assert rows == [("artist",)]

def test_saving_of_album(empty_session):
    album = Album(0, "album")
    empty_session.add(album)
    empty_session.commit()
    rows = list(empty_session.execute('SELECT title FROM albums'))
    assert rows == [("album",)]


def test_saving_of_reviews(empty_session):
    track_key = insert_track(empty_session)
    user_key = insert_user(empty_session, ("Andrew", "1234"))

    rows = empty_session.query(Track).all()
    track = rows[0]
    user = empty_session.query(User).filter(User._User__user_name == "Andrew").one()

    # Create a new Comment that is bidirectionally linked with the User and Article.
    review_text = "Some comment text."
    rating = 5
    review = make_review(track, review_text, rating, user)

    # Note: if the bidirectional links between the new Comment and the User and
    # Article objects hadn't been established in memory, they would exist following
    # committing the addition of the Comment to the database.
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, track_id, review_text FROM reviews'))

    assert rows == [(user_key, track_key, review_text)]


def test_saving_of_playlist_with_track(empty_session):
    track_keys = []
    track_keys.append(insert_track(empty_session))
    track_keys.append(insert_track(empty_session, ["track2", "url", 0]))
    playlist_key = insert_playlist(empty_session)

    insert_playlist_track_association(empty_session, track_keys, playlist_key)

    playlist = empty_session.query(PlayList).get(playlist_key)
    tracks = [empty_session.query(Track).get(key) for key in track_keys]

    for track in tracks:
        assert track in playlist.list_of_tracks


def test_saving_of_track_with_genres(empty_session):
    genre_keys = []
    track_key = insert_track(empty_session)

    genre_keys.append(insert_genre(empty_session))

    insert_track_genre_association(empty_session, track_key, genre_keys)

    track = empty_session.query(Track).get(track_key)
    genres = [empty_session.query(Genre).get(key) for key in genre_keys]

    for genre in genres:
        assert genre in track.genres


