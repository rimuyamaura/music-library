from music.adapters.repository import AbstractRepository
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.playlist import PlayList
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User

# -- Functions used by only by playlists
def get_users_playlist(user_name, repo: AbstractRepository):
    playlist = repo.get_users_playlist(user_name)
    if playlist != None:
        return playlist.list_of_tracks
    else:
        return

def get_users_favourite(user_name, repo: AbstractRepository):
    user = repo.get_user(user_name)
    playlist = user.liked_tracks
    if playlist != None:
        return playlist
    else:
        return

def get_user(user_name, repo: AbstractRepository):
    user = repo.get_user(user_name)
    return user

def get_track(track_id, repo: AbstractRepository):
    track = repo.get_track(track_id)
    return track

def add_to_playlist(track, user: User, repo: AbstractRepository):
    if user != None:
        return repo.add_to_playlist(track, user)

def remove_from_playlist(track, user: User, repo: AbstractRepository):
    return repo.remove_from_playlist(track, user)


def add_to_favourite(track, user: User, repo: AbstractRepository):
    return repo.add_to_favourite(track, user)


def remove_from_favourite(track, user: User, repo: AbstractRepository):
    return repo.remove_liked_track(track, user)

