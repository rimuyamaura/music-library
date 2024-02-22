from datetime import date
from typing import List

from sqlalchemy import desc, asc, Column
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session


from music.adapters.repository import AbstractRepository

from music.adapters.repository import AbstractRepository, RepositoryException
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.playlist import PlayList
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User

from music.adapters.csvdatareader import TrackCSVReader


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_album(self, album: Album):
        with self._session_cm as scm:
            scm.session.merge(album)
            scm.commit()

    @property
    def users(self):
        return self._session_cm.session.query(User).all()

    @property
    def reviews(self):
        return self._session_cm.session.query(Review).all()


    def get_album(self, id: int) -> Album:
        album = None
        try:
            album = self._session_cm.session.query(Album).filter(Album._Album__album_id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return album

    def add_artist(self, artist: Artist):
        with self._session_cm as scm:
            scm.session.merge(artist)
            scm.commit()


    def get_artist(self, id: int) -> Artist:
        artist = None
        try:
            artist = self._session_cm.session.query(Artist).filter(Artist._Artist__artist_id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return artist



    def add_track(self, track: Track):
        with self._session_cm as scm:
            scm.session.merge(track)
            scm.commit()

    def get_track(self, id: int) -> Track:
        track = None
        try:
            track = self._session_cm.session.query(Track).filter(Track._Track__track_id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return track
    
    def get_all_tracks(self) -> List[Track]:
        tracks = self._session_cm.session.query(Track).all()
        return tracks
    def get_all_artists(self) -> List[Artist]:
        artists = self._session_cm.session.query(Artist).all()
        return artists
    def get_all_albums(self) -> List[Album]:
        albums = self._session_cm.session.query(Album).all()
        return albums


    def get_tracks_by_album(self, album_name: str):
        matching_tracks = []
        # get album_id first then use album_id to get matching track
        matching_album = self._session_cm.session.query(Album).filter(Album._Album__title == album_name).all()

        #return matching_album
        for album in matching_album:
            matching_album_id = album.album_id
            tracks = self._session_cm.session.query(Track).filter(Track._Track__album_id == matching_album_id).all()
            for track in tracks:
                matching_tracks.append(track)
        return matching_tracks


    def get_tracks_by_artist(self, artist_name: str):
        matching_tracks = []
        matching_artist = self._session_cm.session.query(Artist).filter(Artist._Artist__full_name == artist_name).all()

        for artist in matching_artist:
            matching_artist_id = artist.artist_id
            tracks = self._session_cm.session.query(Track).filter(Track._Track__artist_id == matching_artist_id).all()
            for track in tracks:
                matching_tracks.append(track)
        return matching_tracks






    def get_tracks_by_genre(self, genre_name: str):
        tracks_ids = []
        matching_genre = self._session_cm.session.query(Genre).filter(Genre._Genre__name == genre_name).all()
        for genre in matching_genre:
            genre_id = genre.genre_id
            tracks_ids = self._session_cm.session.execute(
                'SELECT track_id FROM track_genres WHERE genre_id = :genre_id ORDER BY track_id ASC',
                {'genre_id': genre_id}
            ).fetchall()
            tracks_ids = [id[0] for id in tracks_ids]

        matching_tracks = []
        for i in range(len(tracks_ids)):
            track = self.get_track(tracks_ids[i])
            matching_tracks.append(track)


        return matching_tracks


    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def get_genre(self, id: int) -> Genre:
        genre = None
        try:
            genre = self._session_cm.session.query(Genre).filter(Genre._Genre__genre_id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return genre


    def add_review(self, review: Review, user: User):
        super().add_review(review, user)
        matching_user = self._session_cm.session.query(User).filter(User._User__user_name == user.user_name).one()
        matching_user.add_review(review)

        with self._session_cm as scm:
            scm.session.merge(review)
            scm.commit()

    def get_reviews(self):
        comments = self._session_cm.session.query(Review).all()
        return comments


    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.merge(user)
            scm.commit()

    def get_user(self, user_name:str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            #user = "result not found"
            pass

        return user


    def get_users_playlist(self, user_name) -> PlayList:
        user = self.get_user(user_name)
        if user != None:
            return user.playlist

    def get_user_by_id(self, user_id: int) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_id == user_id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user


    def add_to_playlist(self, track: Track, current_user: User):
        user = None
        result = False
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_id == current_user.user_id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        if user != None:
            playlist = user.playlist
            result = playlist.add_track(track)
            with self._session_cm as scm:
                scm.session.merge(playlist)
                scm.commit()
        return result


    def remove_from_playlist(self, track: Track, current_user: User):
        user = None
        result = False
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_id == current_user.user_id).one()
        except NoResultFound:
            pass
        if user != None:
            playlist = user.playlist
            result = playlist.remove_track(track)
            with self._session_cm as scm:
                #scm.session.query(User).filter(User.name == "squidward").delete(synchronize_session="fetch")
                scm.session.merge(playlist)
                scm.commit()
        return result


    def add_to_favourite(self, track, current_user: User):
        user = None
        result = False
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_id == current_user.user_id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        if user != None:
            #playlist = user.liked_playlist
            result = user.add_liked_track(track)
            with self._session_cm as scm:
                scm.session.merge(user.liked_playlist)
                scm.commit()
        return result


    def remove_liked_track(self, track, current_user: User):
        user = None
        result = False
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_id == current_user.user_id).one()
        except NoResultFound:
            pass
        if user != None:
            #playlist = user.liked_playlist
            result = user.remove_liked_track(track)
            with self._session_cm as scm:
                # scm.session.query(User).filter(User.name == "squidward").delete(synchronize_session="fetch")
                scm.session.merge(user.liked_playlist)
                scm.commit()
        return result

    def like_playlist(self, friend: User, user_who_likes: User):

        playlist_owner = None
        user = None
        result = False
        try:
            playlist_owner = self._session_cm.session.query(User).filter(User._User__user_id == friend.user_id).one()
            user = self._session_cm.session.query(User).filter(User._User__user_id == user_who_likes.user_id).one()
        except NoResultFound:
            pass
        if (user != None):
            playlist = playlist_owner.playlist
            result = playlist.like(user)
            
            with self._session_cm as scm:
                scm.session.merge(playlist)
                scm.commit()
        return result

    def unlike_playlist(self, friend: User, user_who_likes: User):
        playlist_owner = None
        user = None
        result = False
        try:
            playlist_owner = self._session_cm.session.query(User).filter(User._User__user_id == friend.user_id).one()
            user = self._session_cm.session.query(User).filter(User._User__user_id == user_who_likes.user_id).one()
        except NoResultFound:
            pass
        if (user != None):
            playlist = playlist_owner.playlist
            result = playlist.unlike(user)

            with self._session_cm as scm:
                scm.session.merge(playlist)
                scm.commit()
        return result
