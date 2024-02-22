from typing import List, Iterable

from music.adapters.repository import AbstractRepository, RepositoryException
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.playlist import PlayList
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User

def get_user(user_name: str, repo: AbstractRepository):
    return repo.get_user(user_name)

def get_user_by_id(id : int, repo: AbstractRepository):
    return repo.get_user_by_id(id)

# def like_playlist(friend: User, user_name):
#     return friend.playlist.like(user_name)

# def unlike_playlist(friend: User, user_name):
#     return friend.playlist.unlike(user_name)
def like_playlist(friend: User, user_name, repo: AbstractRepository):
    user = repo.get_user(user_name)
    return repo.like_playlist(friend, user)

def unlike_playlist(friend: User, user_name, repo: AbstractRepository):
    user = repo.get_user(user_name)
    return repo.unlike_playlist(friend, user)