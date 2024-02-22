from ast import Str
import csv
from pathlib import Path
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from music.adapters.repository import AbstractRepository, RepositoryException
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.playlist import PlayList
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User

from music.adapters.csvdatareader import TrackCSVReader

class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__tracks = []
        # Set of unique artists
        self.__artists = set()
        # Set of unique albums
        self.__albums = set()
        # Set of unique genres
        self.__genres = set()

        self.__reviews = []
        self.__users = set()

    @property
    def tracks(self) -> list:
        return self.__tracks

    @property
    def artists(self) -> set:
        return self.__artists

    @property
    def albums(self) -> set:
        return self.__albums

    @property
    def genres(self) -> set:
        return self.__genres

    @property
    def reviews(self) -> list:
        return self.__reviews

    @property
    def users(self) -> set:
        return self.__users



    def add_album(self, album: Album):
        self.__albums.add(album)

    def get_album(self, id: int) -> Album:
        target_album = None
        for album in self.__albums:
            #print(album)
            if album.album_id == id:
                target_album = album

        return target_album



    def add_artist(self, artist: Artist):
        self.__artists.add(artist)

    def get_artist(self, id: int) -> Artist:
        target_artist = None
        for artist in self.__artists:
            if artist.artist_id == id:
                target_artist= artist

        return target_artist



    def get_tracks_by_album(self, album_name: Str) -> List[Track]:
        matching_tracks = []
        try:
            for track in self.__tracks:
                if track.album is not None:                  # -- check if tracks have album
                    if track.album.title == album_name:
                        matching_tracks.append(track)
        except ValueError:
            pass
        return matching_tracks

    def get_tracks_by_artist(self, artist_name: Str) -> List[Track]:
        matching_tracks = []
        try:
            for track in self.__tracks:
                if track.artist.full_name == artist_name:
                    matching_tracks.append(track)
        except ValueError:
            pass
        return matching_tracks

    def get_tracks_by_genre(self, genre: Genre) -> List[Track]:
        matching_tracks = []
        try:
            for track in self.__tracks:
                for g in track.genres:
                    if g.name == genre:
                        matching_tracks.append(track)
        except ValueError:
            pass
        return matching_tracks
    
    def add_track(self, track: Track):
        self.__tracks.append(track)

    def get_track(self, id: int) -> Track:
        target_track = None
        for track in self.__tracks:
            if track.track_id== id:
                target_track = track
        return target_track
    
    def get_all_tracks(self):
        return self.__tracks



    def add_genre(self, genre: Genre):
        self.__genres.add(genre)

    def get_genre(self, id: int) -> Genre:
        target_genre = None
        for genre in self.__genres:
            if genre.genre_id == id:
                target_genre = genre

        return target_genre



    def add_review(self, review: Review, user: User):
        for u in self.__users:
            if u == user:
                user.add_review(review)
        super().add_review(review, user)
        self.__reviews.append(review)

    def get_reviews(self):
        return self.__reviews



    def add_user(self, user: User):
        self.__users.add(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def get_users_playlist(self, user_name) -> PlayList:
        user = self.get_user(user_name)
        if user != None:
            return user.playlist

    def get_user_by_id(self, user_id: int) -> User:
        target_user = None
        for user in self.__users:
            if user.user_id == user_id:
                target_user = user
        return target_user

    def add_to_playlist(self, track: Track, user: User):
        if user != None:
            return user.add_to_playlist(track)

    def remove_from_playlist(self, track: Track, user: User):
        return user.remove_from_playlist(track)

    def add_to_favourite(self, track, user: User):
        if user != None and track not in user.liked_tracks:
            user.add_liked_track(track)
            return True
        return False

    def remove_liked_track(self, track, user: User):
        return user.remove_liked_track(track)


    def like_playlist(self, friend: User, user: User):
        return friend.playlist.like(user)
        
    def unlike_playlist(self, friend: User, user: User):
        return friend.playlist.unlike(user)



