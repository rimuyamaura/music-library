import abc
from typing import List
from datetime import date

from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.playlist import PlayList
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User

repo_instance = None

class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_album(self, album: Album):
        raise NotImplementedError

    @abc.abstractmethod
    def get_album(self, id: int) -> Album:
        raise NotImplementedError

    @abc.abstractmethod
    def add_artist(self, artist: Artist):
        raise NotImplementedError

    @abc.abstractmethod
    def get_artist(self, id: int) -> Artist:
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_album(self, album: Album) -> List[Track]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_artist(self, artist: Artist) -> List[Track]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_tracks_by_genre(self, genre: Genre) -> List[Track]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def get_genre(self, id: int) -> Genre:
        raise NotImplementedError

    @abc.abstractmethod
    def add_track(self, track: Track):
        raise NotImplementedError

    @abc.abstractmethod
    def get_track(self, id: int) -> Track:
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review, user : User):

        if review.track is None or review not in user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        #raise NotImplementedError

    @abc.abstractmethod
    def get_reviews(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User named user_name from the repository.
        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError
    
    def get_users_playlist(self, user_name) -> List[Track]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_by_id(self, user_id: int):
        raise NotImplementedError
    
    # -- used to get list of all tracks in music/tracks/services.py
    @abc.abstractmethod
    def get_all_tracks(self):
         raise NotImplementedError

    @abc.abstractmethod
    def add_to_playlist(self, track: Track, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_from_playlist(self, track: Track, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def add_to_favourite(self, track, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_liked_track(self, track, user: User):
        raise NotImplementedError
    
    
    @abc.abstractmethod
    def like_playlist(friend: User, user_name):
        raise NotImplementedError

    @abc.abstractmethod
    def unlike_playlist(friend: User, user_name):
        raise NotImplementedError



