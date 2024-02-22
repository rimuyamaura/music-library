from music.adapters.repository import AbstractRepository
from random import randrange
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.playlist import PlayList
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User

# -- Functions used by only by tracks
def get_all_tracks(repo: AbstractRepository):
    tracks = repo.get_all_tracks()
    return tracks

def get_track(track_id, repo: AbstractRepository):
    track = repo.get_track(track_id)
    return track

def get_tracks_by_artist(artist, repo: AbstractRepository):
    tracks = repo.get_tracks_by_artist(artist)
    return tracks

def get_tracks_by_album(album, repo: AbstractRepository):
    tracks = repo.get_tracks_by_album(album)
    return tracks

def get_tracks_by_genre(genre, repo: AbstractRepository):
    tracks = repo.get_tracks_by_genre(genre)
    return tracks

def get_all_reviews(repo: AbstractRepository):
    return repo.reviews

def get_all_users(repo: AbstractRepository):
    return repo.users

def get_user(user_name, repo: AbstractRepository):
    return repo.get_user(user_name)


def get_user_interests(user, repo: AbstractRepository):
    favorite = user.liked_tracks
    #print(favorite)
    interests_track = []
    if len(favorite) > 0:
        random = randrange(0,len(favorite))
        select_track = favorite[random]    #get a random track from favorite playlist

        #return [select_track]


        for i in range(2):
            genres = select_track.genres
            if genres != None and len(genres) > 0:
                gen_name = select_track.genres[0].name
                genres_list = repo.get_tracks_by_genre(gen_name)    #get tracks with the same genre as selected favorite track

                if genres_list != None and len(genres_list) > 0:
                    random_gen = randrange(len(genres_list))
                    target_track = genres_list[random_gen]    # pick a random track in same genre

                    if (target_track not in favorite) and (target_track not in interests_track) and target_track != None:
                        interests_track.append(target_track)                  #add to interest track list


        artist = select_track.artist
        if artist != None:
            #print(artist)
            artist_name = artist.full_name
            artist_list = repo.get_tracks_by_artist(artist_name)
            if artist_list != None and len(artist_list) > 0:
                random_artist = randrange(len(artist_list))
                target_track = artist_list[random_artist]
                if (target_track not in favorite) and (target_track not in interests_track) and target_track != None:
                    interests_track.append(target_track)

    #print(interests_track)
    return interests_track





