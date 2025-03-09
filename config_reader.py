import configparser
import os

class ConfigReader:
    _instance = None

    def __init__(self, config_file="./config/config.ini"):
        if hasattr(self, "config"):
            return
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()

    @staticmethod
    def get_instance(config_file="./config/config.ini"):
        if ConfigReader._instance is None:
            ConfigReader._instance = ConfigReader(config_file)
        return ConfigReader._instance

    def load_config(self):
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file {self.config_file} not found")
        self.config.read(self.config_file)

    def get(self, section: str, key: str, fallback=None):
        return self.config.get(section, key, fallback=fallback)

    def get_default(self, key: str, fallback=None):
        return self.config.get("DEFAULT", key, fallback=fallback)

    def get_connection(self,  key: str, fallback=None):
        return self.config.get("CONNECTION", key, fallback=fallback)