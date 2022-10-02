"""
Class to manage the database.
It will connect to the sources and get the data. Then it will store it in a database.
"""
from pathlib import Path

from opensignals.data.yahoo import Yahoo
from opensignals.features import RSI, SMA
import pandas as pd


class DataBaseGenerator:
    def __init__(self):
        pass

    def create_initial_database(self):
            
        db_dir = Path('db')

        yahoo = Yahoo()
        yahoo.download_data(db_dir)

        features_generators = [
            RSI(num_days=5, interval=14, variable='adj_close'),
            RSI(num_days=5, interval=21, variable='adj_close'),
            SMA(num_days=5, interval=14, variable='adj_close'),
            SMA(num_days=5, interval=21, variable='adj_close'),
        ]

        print('Generating features')

        train, test, live, feature_names = yahoo.get_data(
            db_dir,
            features_generators=features_generators,
            feature_prefix='feature'
        )

        train['friday_date'] = pd.to_datetime(train['friday_date'], format='%Y%m%d')
        test['friday_date'] = pd.to_datetime(test['friday_date'], format='%Y%m%d')

        training_data_output_path = 'example_training_data_yahoo.csv'
        tournament_data_output_path = 'example_tournament_data_yahoo.csv'

        train.to_csv(training_data_output_path)
        tournament_data = pd.concat([test, live])
        tournament_data.to_csv(tournament_data_output_path)

        print('Done')


    def update_database(self):
        pass


if __name__ == "__main__":
    db_gen = DataBaseGenerator()
    db_gen.create_initial_database()
