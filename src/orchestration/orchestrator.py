from pathlib import Path
from typing import Union

from data.database_generator import DataBaseGenerator
from features.feature_generator import FeatureGenerator
from models.model_trainer import ModelTrainer


class Orchestrator:
    def __init__(self,
                 db_cfg_path: Union[Path, str],
                 features_cfg_path: Union[Path, str]=None):
        
        if features_cfg_path is None:
            features_cfg_path = db_cfg_path

        self.db_cfg_path = db_cfg_path
        self.features_cfg_path = features_cfg_path
    
    def run_all(self):
        print('Running all')
        print('Generate database')
        dbg = DataBaseGenerator(self.db_cfg_path)
        dbg.create_initial_database()

        print('Generate features')
        fg = FeatureGenerator(self.db_cfg_path, self.features_cfg_path)
        fg.generate_features()

        print('Train model')
        mt = ModelTrainer(self.features_cfg_path)
        mt.load_data()
        mt.train_model()
        mt.predict()
