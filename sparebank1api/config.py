import configparser
import os


class Config:
    def __init__(self, config_path="config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    def _get(self, section: str, key: str):
        if self.config.has_option(section, key):
            return self.config.get(section, key)
        return None

    @property
    def client_id(self):
        return os.getenv("CLIENT_ID", self._get("DEFAULT", "client_id"))

    @property
    def client_secret(self):
        return os.getenv("CLIENT_SECRET", self._get("DEFAULT", "client_secret"))

    @property
    def redirect_uri(self):
        return os.getenv("REDIRECT_URI", self._get("DEFAULT", "redirect_uri"))

    @property
    def fin_inst(self):
        return os.getenv("FIN_INST", self._get("DEFAULT", "fin_inst"))
