from datetime import date, datetime
from typing import List

import pytest
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.playlist import PlayList
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User

from music.adapters.repository import AbstractRepository, RepositoryException
from music.adapters.memory_repository import MemoryRepository
from music.adapters.csvdatareader import TrackCSVReader



def test_repository_can_add_a_user(in_memory_repo):
    user = User(1, 'dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = User(1, 'dave', '123456789')
    in_memory_repo.add_user(user)

    user = in_memory_repo.get_user('dave')
    assert user == User(1, 'dave', '123456789')


def test_repository_can_retrieve_a_user_by_id(in_memory_repo):
    user = User(1, 'dave', '123456789')
    in_memory_repo.add_user(user)

    user = in_memory_repo.get_user_by_id(1)
    assert user == User(1, 'dave', '123456789')

def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_add_an_album(in_memory_repo):
    album = Album(2, 'International')
    in_memory_repo.add_album(album)

    assert in_memory_repo.get_album(2) is album


def test_repository_can_retrieve_an_album(in_memory_repo):
    album = in_memory_repo.get_album(4)
    assert album == Album(4, 'dave')


def test_repository_does_not_retrieve_a_non_existent_album(in_memory_repo):
    album = in_memory_repo.get_album(2)
    assert album is None

def test_repository_can_add_an_artist(in_memory_repo):
    artist = Artist(2, 'Artist name')
    in_memory_repo.add_artist(artist)

    assert in_memory_repo.get_artist(2) is artist


def test_repository_can_retrieve_an_artist(in_memory_repo):

    artist = in_memory_repo.get_artist(1)
    assert artist == Artist(1, 'OWAl')


def test_repository_does_not_retrieve_a_non_existent_artist(in_memory_repo):
    artist = in_memory_repo.get_artist(2)
    assert artist is None


def test_repository_can_get_tracks_by_album(in_memory_repo):
    album = Album(4, 'Niris')
    album_name = album.title
    tracks = in_memory_repo.get_tracks_by_album(album_name)
    all_tracks = in_memory_repo.tracks
    tracks_in_album = []

    for track in all_tracks:
        if track.album == album:
            tracks_in_album.append(track)
    
    assert tracks == tracks_in_album


def test_repository_can_get_tracks_by_artist(in_memory_repo):
    artist = Artist(4, 'Nicky Cook')
    artist_name = artist.full_name
    tracks = in_memory_repo.get_tracks_by_artist(artist_name)
    all_tracks = in_memory_repo.tracks
    tracks_in_artist = []

    for track in all_tracks:
        if track.artist == artist:
            tracks_in_artist.append(track)

    assert tracks == tracks_in_artist

def test_repository_can_get_tracks_by_artist(in_memory_repo):
    artist = Artist(4, 'Nicky Cook')
    artist_name = artist.full_name
    tracks = in_memory_repo.get_tracks_by_artist(artist_name)
    all_tracks = in_memory_repo.tracks
    tracks_in_artist = []

    for track in all_tracks:
        if track.artist == artist:
            tracks_in_artist.append(track)

    assert tracks == tracks_in_artist


def test_repository_can_get_tracks_by_genre(in_memory_repo):
    genre = Genre(1, 'Avant-Garde')
    genre_name = genre.name
    tracks = in_memory_repo.get_tracks_by_genre(genre_name)
    
    all_tracks = in_memory_repo.tracks
    tracks_in_genre = []
    for track in all_tracks:
        for g in track.genres:
            if g.name == genre_name:
                tracks_in_genre.append(track)
    assert tracks == tracks_in_genre


def test_repository_can_get_all_tracks(in_memory_repo):
    all_tracks_function = in_memory_repo.get_all_tracks()

    all_tracks = in_memory_repo.tracks
    assert len(all_tracks) == len(all_tracks_function)



def test_repository_can_add_an_genre(in_memory_repo):
    genre = Genre(100, 'International')
    in_memory_repo.add_genre(genre)

    assert in_memory_repo.get_genre(100) is genre


def test_repository_can_retrieve_an_genre(in_memory_repo):
    genre = in_memory_repo.get_genre(1)
    assert genre == Genre(1, 'Genre name')


def test_repository_does_not_retrieve_a_non_existent_genre(in_memory_repo):
    genre = in_memory_repo.get_genre(100)
    assert genre is None


def test_repository_can_add_an_track(in_memory_repo):
    track = Track(1, 'Track name')
    in_memory_repo.add_track(track)

    assert in_memory_repo.get_track(1) is track


def test_repository_can_retrieve_an_track(in_memory_repo):
    track = in_memory_repo.get_track(2)
    assert track == Track(2, 'Track name')


def test_repository_does_not_retrieve_a_non_existent_track(in_memory_repo):
    track = in_memory_repo.get_track(100)
    assert track is None


def test_repository_can_add_review(in_memory_repo):
    user = User(1, 'dave', '123456789')
    in_memory_repo.add_user(user)

    track = Track(1, 'Track name')
    review = Review(track, 'review', 1)
    in_memory_repo.add_review(review, user)

    assert review in user.reviews


def test_repository_can_retrieve_review(in_memory_repo):
    user = User(1, 'dave', '123456789')
    in_memory_repo.add_user(user)

    track = Track(1, 'Track name')
    review = Review(track, 'review', 1)
    in_memory_repo.add_review(review, user)

    assert in_memory_repo.get_reviews() == user.reviews

def test_repository_can_get_users_playlist(in_memory_repo):
    user = User(1, 'dave', '123456789')
    track = Track(1, 'Track name')
    user.add_to_playlist(track)
    in_memory_repo.add_user(user)

    playlist = in_memory_repo.get_users_playlist(user.user_name)
    assert playlist.list_of_tracks == [track]

def test_repository_can_get_user_by_id(in_memory_repo):
    user = User(1, 'dave', '123456789')
    in_memory_repo.add_user(user)

    in_memory_repo.get_user_by_id(1)
    assert in_memory_repo.get_user_by_id(1) is user







