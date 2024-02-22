from typing import List, Iterable

from music.adapters.repository import AbstractRepository, RepositoryException
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.playlist import PlayList
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User



class NonExistentArticleException(Exception):
    pass


class UnknownUserException(Exception):
    pass

def add_review(track: Track, review_text: str, user_name:str, rating: int, repo: AbstractRepository):
    # Check that the track exists.
    target_track = repo.get_track(track.track_id)
    if target_track is None:
        raise NonExistentArticleException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    # Create comment.
    review = new_review(user, target_track, review_text, rating)

    # Update the repository.
    repo.add_review(review, user)


def new_review(user:User, track: Track, review_text: str, rating: int):

    review = Review(track, review_text, rating)
    user.add_review(review)
    return review

def get_track(track_id:int, repo: AbstractRepository):
    return repo.get_track(track_id)

def get_user(user_name:str, repo: AbstractRepository):
    return repo.get_user(user_name)

def get_reviews(repo: AbstractRepository):
    return repo.get_reviews()