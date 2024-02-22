from __future__ import annotations
from datetime import datetime
from music.adapters.repository import AbstractRepository, RepositoryException
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.playlist import PlayList
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User

class ModelException(Exception):
    pass


def make_review(track:Track, review_text: str, rating: int, user:User):
    review = Review(track, review_text, rating)
    user.add_review(review)

    return review


def make_genre_association(track: Track, genre: Genre):
    track.add_genre(genre)

'''
def make_playlist_track_association(track: Track, playlist: PlayList):
    playlist.add_track(track)'''


