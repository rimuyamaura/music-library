from datetime import date

import pytest

from music.authentication.services import AuthenticationException
from music.reviews import services as reviews_services
from music.tracks import services as tracks_services
from music.authentication import services as auth_services
from music.friends import services as user_services
from music.playlists import services as playlists_services



from music.adapters.repository import AbstractRepository, RepositoryException
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.playlist import PlayList
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User

def test_can_add_user(in_memory_repo):
    new_user_name = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    user_name = 'thorke'
    password = 'abcd1A23'
    auth_services.add_user(user_name, password, in_memory_repo)

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)


def test_can_add_comment(in_memory_repo):
    track = Track(2, 'Track name')
    review_text = 'nice'
    user_name = 'fmercury'
    password = 'abcd1A23'
    rating = 5

    auth_services.add_user(user_name, password, in_memory_repo)
    reviews_services.add_review(track, review_text, user_name, rating, in_memory_repo)

    all_reviews = reviews_services.get_reviews(in_memory_repo)
    assert len(all_reviews) != 0

def test_get_invalid_track(in_memory_repo):
    track = tracks_services.get_track(99999999, in_memory_repo)
    assert track == None

def test_invalid_get_tracks_by_artist(in_memory_repo):
    tracks = tracks_services.get_tracks_by_artist("ZZZZZZZZZZZZZZz", in_memory_repo)
    assert tracks == []

def test_invalid_get_tracks_by_album(in_memory_repo):
    tracks = tracks_services.get_tracks_by_album("ZZZZZZZZZZZZZZz", in_memory_repo)
    assert tracks == []

def test_invalid_get_tracks_by_genre(in_memory_repo):
    tracks = tracks_services.get_tracks_by_genre("ZZZZZZZZZZZZZZz", in_memory_repo)
    assert tracks == []


def test_get_user_interest_return_related_track(in_memory_repo):
    user = User(1, 'dave', '123456789')
    in_memory_repo.add_user(user)

    track = in_memory_repo.get_track(2)
    playlists_services.add_to_playlist(track, user, in_memory_repo)
    playlists_services.add_to_favourite(track, user, in_memory_repo)

    interests = tracks_services.get_user_interests(user, in_memory_repo)
    assert len(interests) != 0

    for i in interests:
        assert (i.genres == track.genres) or (i.artist == track.artist)


def test_can_retrieve_a_user_by_id(in_memory_repo):
    user = User(1, 'dave', '123456789')
    in_memory_repo.add_user(user)

    user = user_services.get_user_by_id(int('1'), in_memory_repo)
    assert user == User(1, 'dave', '123456789')

def test_can_retrieve_a_user(in_memory_repo):
    user = User(1, 'dave', '123456789')
    in_memory_repo.add_user(user)

    user = user_services.get_user('dave', in_memory_repo)
    assert user == User(1, 'dave', '123456789')


def test_can_add_to_and_get_users_playlist(in_memory_repo):
    user = User(1, 'dave', '123456789')
    in_memory_repo.add_user(user)

    track = Track(2, 'Track name')
    playlists_services.add_to_playlist(track, user, in_memory_repo)

    playlist = playlists_services.get_users_playlist(user.user_name, in_memory_repo)
    assert playlist == [track]

def test_can_remove_from_playlist(in_memory_repo):
    user = User(1, 'dave', '123456789')
    in_memory_repo.add_user(user)

    track = Track(2, 'Track name')
    playlists_services.add_to_playlist(track, user, in_memory_repo)

    playlists_services.remove_from_playlist(track, user, in_memory_repo)

    playlist = playlists_services.get_users_playlist(user.user_name, in_memory_repo)
    assert playlist == []


def test_can_add_to_favourite(in_memory_repo):
    user = User(1, 'dave', '123456789')
    in_memory_repo.add_user(user)

    track = Track(2, 'Track name')
    playlists_services.add_to_playlist(track, user, in_memory_repo)
    playlists_services.add_to_favourite(track, user, in_memory_repo)

    playlist = playlists_services.get_users_playlist(user.user_name, in_memory_repo)
    assert playlist == [track]

    assert track in playlists_services.get_users_favourite(user.user_name, in_memory_repo)


def test_can_remove_from_favourite(in_memory_repo):
    user = User(1, 'dave', '123456789')
    in_memory_repo.add_user(user)

    track = Track(2, 'Track name')
    playlists_services.add_to_playlist(track, user, in_memory_repo)
    playlists_services.add_to_favourite(track, user, in_memory_repo)
    playlists_services.remove_from_favourite(track, user, in_memory_repo)

    assert track not in playlists_services.get_users_favourite(user.user_name, in_memory_repo)

def test_like_playlist(in_memory_repo):
    user1 = User(1, 'dave', '123456789')
    in_memory_repo.add_user(user1)
    user2 = User(2,'bob', '123456789')
    in_memory_repo.add_user(user2)
    user_services.like_playlist(user1, 'bob', in_memory_repo)

    assert user1.playlist.liked_by == [user2]

def test_unlike_playlist(in_memory_repo):
    user1 = User(1, 'dave', '123456789')
    in_memory_repo.add_user(user1)
    user2 = User(2,'bob', '123456789')
    in_memory_repo.add_user(user2)
    user_services.like_playlist(user1, 'bob', in_memory_repo)
    user_services.unlike_playlist(user1, 'bob', in_memory_repo)
    print(user1.playlist.liked_by)
    assert user1.playlist.liked_by == []




