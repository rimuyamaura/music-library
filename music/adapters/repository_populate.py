# from pathlib import Path

# from music.adapters.repository import AbstractRepository
# from music.adapters.csv_data_importer import load_track

# def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
#     load_track(data_path, repo)


from pathlib import Path

from music.adapters.repository import AbstractRepository
from music.adapters.csvdatareader import load_data, load_user, load_review

def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):

    load_data(data_path, repo)
    if (database_mode == True):
        load_user(data_path, repo)
        load_review(data_path, repo)


    