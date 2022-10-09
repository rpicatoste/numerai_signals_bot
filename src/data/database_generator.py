from opensignals.data.yahoo import Yahoo
from pathlib import Path
from typing import Union

from .database_configuration import DataBaseConfiguration


class DataBaseGenerator:
    """
    Class to manage the database.
    It will connect to the sources and get the data. Then it will store it in a database.
    """
    def __init__(self, db_cfg_path: Union[Path, str]):
        self.cfg = DataBaseConfiguration(db_cfg_path)

    def create_initial_database(self):
        yahoo = Yahoo()
        yahoo.download_data(self.cfg.db_dir)
        print('Done')

    def update_database(self):
        pass


if __name__ == "__main__":
    db_gen = DataBaseGenerator()
    db_gen.create_initial_database()
