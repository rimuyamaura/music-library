import pytest
from datetime import datetime

import music.adapters.repository as repo
from music.adapters.database_repository import SqlAlchemyRepository
from music.adapters.repository import RepositoryException


from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.playlist import PlayList
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User
from music.domainmodel.model import make_review, make_genre_association

def test_repository_can_add_or_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'dave', '123456789')
    repo.add_user(user)

    repo.add_user(User(2, 'Martin', '123456789'))
    user2 = repo.get_user('dave')
    assert user2 == user

def test_repository_can_add_an_album(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    album = Album(0, 'album')
    repo.add_album(album)


    album2 = repo.get_album(0)

    assert album2 == album

def test_repository_can_retrieve_an_album(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    album2 = repo.get_album(1)
    album = Album(1, "album")

    assert album2 == album

def test_repository_does_not_retrieve_a_non_existent_album(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    album = repo.get_album(0)
    assert album is None



def test_repository_can_add_an_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    artist = Artist(0, 'Dave')
    repo.add_artist(artist)
    artist2 = repo.get_artist(0)

    assert artist2 == artist

def test_repository_can_retrieve_an_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    artist2 = repo.get_artist(1)
    artist = Artist(1, "album")

    assert artist2 == artist



def test_repository_does_not_retrieve_a_non_existent_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    artist = repo.get_artist(0)
    assert artist is None


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None


def test_repository_can_add_a_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = Track(0, 'title')
    repo.add_track(track)
    track2 = repo.get_track(0)

    assert track2 == track


def test_repository_can_retrieve_a_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track2 = repo.get_track(2)
    track = Track(2, "title")

    assert track2 == track

def test_repository_does_not_retrieve_a_non_existent_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_track(1)
    assert track is None

def test_repository_can_retrieve_track_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_tracks = len(repo.get_all_tracks())

    # Check that the query returned 177 Articles.
    assert number_of_tracks == 2000

def test_repository_can_retrieve_album_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_albums = len(repo.get_all_albums())

    # Check that the query returned 177 Articles.
    assert number_of_albums == 427


def test_repository_can_retrieve_artist_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_artists = len(repo.get_all_artists())

    # Check that the query returned 177 Articles.
    assert number_of_artists == 263


def test_repository_can_retrieve_track_by_album(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    matching_tracks = repo.get_tracks_by_album("Niris")
    #assert matching_tracks == []


    all_tracks = repo.get_all_tracks()
    tracks_in_album = []

    for track in all_tracks:
        if track.album != None:
            if track.album.title == "Niris":
                tracks_in_album.append(track)

    assert matching_tracks == tracks_in_album


def test_repository_can_retrieve_track_by_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    matching_tracks = repo.get_tracks_by_artist("OWAL")


    all_tracks = repo.get_all_tracks()
    tracks_in_artist = []

    for track in all_tracks:
        if track.artist != None:
            if track.artist.full_name == "OWAL":
                tracks_in_artist.append(track)

    assert matching_tracks == tracks_in_artist


def test_repository_can_retrieve_track_by_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    matching_tracks = repo.get_tracks_by_genre("Hip-Hop")
    #assert matching_tracks == []

    all_tracks = repo.get_all_tracks()
    tracks_in_genre = []
    for track in all_tracks:
        for g in track.genres:
            if g.name == "Hip-Hop":
                tracks_in_genre.append(track)
    assert matching_tracks == tracks_in_genre


def test_repository_can_add_a_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genre = Genre(0, 'name')
    repo.add_track(genre)
    genre2 = repo.get_genre(0)

    assert genre2 == genre


def test_repository_can_retrieve_a_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genre2 = repo.get_genre(2)
    genre = Genre(2, "title")

    assert genre2 == genre


def test_repository_does_not_retrieve_a_non_existent_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_genre(0)
    assert track is None


def test_repository_can_add_or_get_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = Track(0, 'name')
    user = User(0, "name", "password")

    review = make_review(track, "text", 5,  user)

    repo.add_user(user)
    repo.add_review(review, user)
    review2 = repo.get_reviews()

    assert review in review2
    assert len(review2) != 0


def test_repository_does_not_add_a_review_without_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = Track(0, "title")
    review = Review(track, "text", 5)
    not_inserted_user = User(0, "name", "12345")

    with pytest.raises(RepositoryException):
        repo.add_review(review, not_inserted_user)


def test_repository_can_add_or_get_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(0, "user_name", "1234567")
    repo.add_user(user)
    # A playList is created within a user object

    assert isinstance(repo.get_users_playlist(user.user_name), PlayList)


def test_repository_can_retrieve_a_user_with_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(0, "user_name", "1234567")
    repo.add_user(user)

    targeted_user = repo.get_user_by_id(0)
    assert user == targeted_user


def test_can_add_to_and_get_users_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'dave', '123456789')
    repo.add_user(user)

    track = Track(0, 'Track name')
    repo.add_to_playlist(track, user)

    playlist = repo.get_users_playlist(user.user_name)
    assert playlist.list_of_tracks == [track]


def test_can_remove_from_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'dave', '123456789')
    repo.add_user(user)

    track = repo.get_track(2)
    repo.add_to_playlist(track, user)

    repo.remove_from_playlist(track, user)

    playlist = repo.get_users_playlist(user.user_name)
    assert playlist.list_of_tracks == []


def test_can_add_to_favourite(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'dave', '123456789')
    repo.add_user(user)

    track = repo.get_track(2)
    repo.add_to_playlist(track, user)
    repo.add_to_favourite(track, user)

    playlist = repo.get_users_playlist(user.user_name).list_of_tracks
    assert playlist == [track]

    user_after = repo.get_user_by_id(1)
    assert track in user_after.liked_tracks


def test_can_remove_from_favourite(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'dave', '123456789')
    repo.add_user(user)

    track = repo.get_track(2)
    repo.add_to_playlist(track, user)
    repo.add_to_favourite(track, user)
    repo.remove_liked_track(track, user)

    user_after = repo.get_user_by_id(1)
    assert track not in user_after.liked_tracks

def test_can_like_users_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    repo.add_user(User(1, 'dave', '123456789'))
    repo.add_user(User(2, 'joe', '123456789'))
    user1 = repo.get_user('dave')
    user2 = repo.get_user('joe')

    repo.like_playlist(user1, user2)
    #print(user1.playlist.liked_by)
    assert user1.playlist.liked_by == [user2]

def test_can_unlike_users_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    repo.add_user(User(1, 'dave', '123456789'))
    repo.add_user(User(2, 'joe', '123456789'))
    user1 = repo.get_user('dave')
    user2 = repo.get_user('joe')

    repo.like_playlist(user1, user2)
    repo.unlike_playlist(user1, user2)
    assert user1.playlist.liked_by == []
