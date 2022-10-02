"""
This module contains the ModelTrainer class, which is used to train a model.
"""
from pathlib import Path
import pandas as pd
from xgboost import XGBRegressor


TARGET_NAME = 'target_20d'
PREDICTION_NAME = 'signal'

class ModelTrainer:

    def __init__(self):
        pass

    def load_data(self, data_folder):
        """Creates example_signal_yahoo.csv to upload for validation and live data submission"""

        print('Reading data')
        data_folder = Path(data_folder)
        self.train = pd.read_csv('example_training_data_yahoo.csv')
        self.tournament = pd.read_csv('example_tournament_data_yahoo.csv')

        self.feature_names = self.train.filter(like='feature_').columns.to_list()

        assert len(self.train) > 0, 'Training data is empty'
        assert len(self.tournament) > 0, 'Tournament data is empty'

    def train_model(self):
        print('Training model')
        self.model = XGBRegressor(tree_method='gpu_hist')
        self.model.fit(self.train[self.feature_names], 
                       self.train[TARGET_NAME])

    def predict(self, output_dir=None):
        # predict test and live data
        print('Predicting test and live data')

        # drop rows where target or features are null
        self.tournament = self.tournament.dropna(subset=self.feature_names)
        self.tournament[PREDICTION_NAME] = self.model.predict(self.tournament[self.feature_names])

        # prepare and writeout example file
        print('Writing signal upload file')
        diagnostic_df = self.tournament.copy()
        diagnostic_df['data_type'] = diagnostic_df.data_type.fillna('live')

        example_signal_output_path = 'example_signal_upload.csv'
        if output_dir is not None:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            example_signal_output_path = output_dir/example_signal_output_path

        diagnostic_df = diagnostic_df.drop_duplicates(subset=["bloomberg_ticker", "friday_date"], keep="first")
        diagnostic_df[['bloomberg_ticker', 'friday_date', 'data_type', 'signal']].reset_index(drop=True).to_csv(example_signal_output_path, index=False)

        print('Finished')


if __name__ == '__main__':
    trainer = ModelTrainer()
    trainer.load_data(data_folder='db')
    trainer.train_model()
    trainer.predict(output_dir='output')
