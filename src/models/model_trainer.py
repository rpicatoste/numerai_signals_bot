"""
This module contains the ModelTrainer class, which is used to train a model.
"""
from pathlib import Path
from typing import Union
import pandas as pd
from xgboost import XGBRegressor

from features.feature_generator import FeatureGenerator


TARGET_NAME = 'target_20d'
PREDICTION_NAME = 'signal'

class ModelTrainer:

    def __init__(self, features_cfg_path: Union[Path, str]):
        self.feat_gen = FeatureGenerator(features_cfg_path)

    def load_data(self):
        print('Reading data')
        self.feat_gen.load_features()
        train = self.feat_gen.train
        tournament = self.feat_gen.tournament

        self.feature_names = train.filter(like='feature_').columns.to_list()

        assert len(train) > 0, 'Training data is empty'
        assert len(tournament) > 0, 'Tournament data is empty'

    def train_model(self):
        print('Training model')
        self.model = XGBRegressor(tree_method='gpu_hist')
        self.model.fit(self.feat_gen.train[self.feature_names], 
                       self.feat_gen.train[TARGET_NAME])

    def predict(self, output_dir=None):
        # predict test and live data
        print('Predicting test and live data')

        # drop rows where target or features are null
        self.feat_gen.tournament = self.feat_gen.tournament.dropna(subset=self.feature_names)
        self.feat_gen.tournament[PREDICTION_NAME] = self.model.predict(self.feat_gen.tournament[self.feature_names])

        # prepare and writeout example file
        print('Writing signal upload file')
        diagnostic_df = self.feat_gen.tournament.copy()
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
