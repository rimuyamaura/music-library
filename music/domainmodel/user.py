from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.playlist import PlayList


class User:

    def __init__(self, user_id: int, user_name: str, password: str):
        if type(user_id) is not int or user_id < 0:
            raise ValueError("User ID should be a non negative integer.")
        self.__user_id = user_id

        if type(user_name) is str:
            self.__user_name = user_name.lower().strip()
        else:
            self.__user_name = None

        if isinstance(password, str) and len(password) >= 7:
            self.__password = password
        else:
            self.__password = None

        self.__reviews: list[Review] = []
        #self.__liked_tracks: list[Track] = []

        #self.__playlist: PlayList = PlayList()
        self.__playlist: list[PlayList] = []
        user_playlist = PlayList()
        user_favorite = PlayList()
        self.__playlist.append(user_playlist)
        self.__playlist.append(user_favorite)

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def user_name(self) -> str:
        return self.__user_name

    @property
    def password(self) -> str:
        return self.__password

    @property
    def reviews(self) -> list:
        return self.__reviews
    
    @property
    def playlist(self) -> PlayList:
        return self.__playlist[0]

    def add_review(self, new_review: Review):
        if not isinstance(new_review, Review) or new_review in self.__reviews:
            return
        self.__reviews.append(new_review)

    def remove_review(self, review: Review):
        if not isinstance(review, Review) or review not in self.__reviews:
            return
        self.__reviews.remove(review)

    @property
    def liked_tracks(self) -> list:
        return self.__playlist[1].list_of_tracks

    @property
    def liked_playlist(self) -> PlayList:
        return self.__playlist[1]

    def add_liked_track(self, track: Track):
        if not isinstance(track, Track) or track in self.__playlist[1].list_of_tracks:
            return
        self.__playlist[1].add_track(track)

    def remove_liked_track(self, track: Track):
        if not isinstance(track, Track) or track not in self.__playlist[1].list_of_tracks:
            return
        self.__playlist[1].remove_track(track)


    # -- Playlist functions
    def add_to_playlist(self, track: Track):
        return self.__playlist[0].add_track(track)

    def remove_from_playlist(self, track: Track):
        return self.__playlist[0].remove_track(track)


    def __repr__(self):
        return f'<User {self.user_name}, user id = {self.user_id}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.user_id == other.user_id

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return True
        return self.user_id < other.user_id

    def __hash__(self):
        return hash(self.user_id)
