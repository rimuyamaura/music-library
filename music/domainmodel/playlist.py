from music.domainmodel.track import Track


class PlayList:

    def __init__(self):
        self.__list_of_tracks = []
        self.__liked_by = []            # -- List of users who like the playlist

    @property
    def list_of_tracks(self) -> list():
        return self.__list_of_tracks
    
    @property
    def liked_by(self) -> list():
        return self.__liked_by

    def size(self):
        size_playlist = len(self.__list_of_tracks)
        if size_playlist > 0:
            return size_playlist

    def add_track(self, track: Track):
        if track not in self.__list_of_tracks and isinstance(track, Track):
            self.__list_of_tracks.append(track)
            return True
        else:
            return False

    def first_track_in_list(self):
        if len(self.__list_of_tracks) > 0:
            return self.__list_of_tracks[0]
        else:
            return None

    def remove_track(self, track):
        if track in self.__list_of_tracks and isinstance(track, Track):
            self.__list_of_tracks.remove(track)
            return True
        else:
            return False

    def select_track_to_listen(self, index):
        if 0 <= index < len(self.__list_of_tracks):
            return self.__list_of_tracks[index]
        else:
            return None
    
    def like(self, user_name):
        if user_name not in self.__liked_by:
            self.__liked_by.append(user_name)
            return True
        else:
            return False
    
    def unlike(self, user_name):
        if user_name in self.__liked_by:
            self.__liked_by.remove(user_name)
            return True
        else:
            return False

    def __iter__(self):
        self.__current = 0
        return self

    def __next__(self):
        if self.__current >= len(self.__list_of_tracks):
            raise StopIteration
        else:
            self.__current += 1
            return self.__list_of_tracks[self.__current - 1]
