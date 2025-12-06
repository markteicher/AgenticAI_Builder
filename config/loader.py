import yaml
import logging
from pathlib import Path


class ConfigLoader:
    @staticmethod
    def load(config_path: str) -> dict:
        path = Path(config_path)
        if not path.exists():
            logging.error(f"❌ Config file not found: {config_path}")
            raise FileNotFoundError(f"Config file not found: {config_path}")

        try:
            with open(path, "r") as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            logging.error(f"❌ Failed to parse YAML config: {e}")
            raise

        ConfigLoader._validate(config)
        logging.info(f"✅ Loaded config from: {config_path}")
        return config

    @staticmethod
    def _validate(config: dict):
        required_keys = ["tasks", "template_dir", "output_dir"]
        missing = [key for key in required_keys if key not in config]
        if missing:
            logging.error(f"❌ Config missing required keys: {missing}")
            raise ValueError(f"Config is missing required keys: {missing}")
