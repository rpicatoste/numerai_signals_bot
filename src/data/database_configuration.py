from pathlib import Path
import yaml


class DataBaseConfiguration:
    """
    Reads the database configuration and applies checks if needed.
    """

    def __init__(self, cfg_path: Path):
        self.cfg_path = cfg_path

        with open(self.cfg_path, "r") as file:
            cfg_dict = yaml.safe_load(file)

        # Configs can be a file only for the database configuration or a common file for multiple
        # configurations. In the latter case, we need to select only the database configuration.
        if "database" in cfg_dict:
            cfg_dict = cfg_dict["database"]

        self.db_dir = Path(cfg_dict["db_dir"])
