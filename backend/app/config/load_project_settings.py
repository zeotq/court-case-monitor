from configparser import RawConfigParser
from pathlib import Path


class Settings:
    config = RawConfigParser()
    private_dir = (Path(__file__) / '..').resolve()

    config.read(private_dir / 'headers_config.ini')
    headers = dict(config.items('headers'))
    cookies = dict()

settings = Settings()