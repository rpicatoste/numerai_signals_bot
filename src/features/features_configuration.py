from pathlib import Path
from typing import Union
import yaml


class FeaturesConfiguration:
    def __init__(self, cfg_path: Union[Path, str]):
        self.cfg_path = cfg_path

        with open(self.cfg_path, 'r') as file:
            cfg_dict = yaml.safe_load(file)

        # Configs can be a file only for the features configuration or a common file for multiple
        # configurations. In the latter case, we need to select only the database configuration.
        if 'features' in cfg_dict:
            cfg_dict = cfg_dict['features']

        self.features_dir = Path(cfg_dict['features_dir'])
