
from pathlib import Path
from typing import Union
from opensignals.features import RSI, SMA
import pandas as pd
from opensignals.data.yahoo import Yahoo

from data.database_configuration import DataBaseConfiguration
from features.features_configuration import FeaturesConfiguration


class FeatureGenerator:

    def __init__(self, 
                 db_cfg_path: Union[Path, str],
                 features_cfg_path: Union[Path, str]=None):

        if features_cfg_path is None:
            features_cfg_path = db_cfg_path

        self.db_cfg = DataBaseConfiguration(db_cfg_path)
        self.feat_cfg = FeaturesConfiguration(features_cfg_path)
        
        self.training_path = self.feat_cfg.features_dir/'training_data_yahoo.csv'
        self.tournament_path = self.feat_cfg.features_dir/'tournament_data_yahoo.csv'

    def generate_features(self):
        
        features_generators = [
            RSI(num_days=5, interval=14, variable='adj_close'),
            RSI(num_days=5, interval=21, variable='adj_close'),
            SMA(num_days=5, interval=14, variable='adj_close'),
            SMA(num_days=5, interval=21, variable='adj_close'),
        ]

        print('Generating features')
        yahoo = Yahoo()
        
        train, test, live, feature_names = yahoo.get_data(
            self.db_cfg.db_dir,
            features_generators=features_generators,
            feature_prefix='feature'
        )

        train['friday_date'] = pd.to_datetime(train['friday_date'], format='%Y%m%d')
        test['friday_date'] = pd.to_datetime(test['friday_date'], format='%Y%m%d')

        self.training_path.parent.mkdir(parents=True, exist_ok=True)
        train.to_csv(self.training_path)
        self.train = train
        self.tournament = pd.concat([test, live])
        self.tournament.to_csv(self.tournament_path)

    def load_features(self):
        self.train = pd.read_csv(self.training_path)
        self.tournament = pd.read_csv(self.tournament_path)
