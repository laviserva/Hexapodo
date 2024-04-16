import configparser
from pathlib import Path

class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.config = configparser.ConfigParser()

            path = Path(__file__).parent.absolute() / 'configuration.config'

            cls._instance.config.read(path)
        return cls._instance

    @staticmethod
    def get_config():
        return ConfigManager()._instance.config