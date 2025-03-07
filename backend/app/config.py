from configparser import RawConfigParser
from pathlib import Path


class Settings:
    config = RawConfigParser()
    private_dir = (Path(__file__).parent.parent / "../configs").resolve()

    config.read(private_dir / 'headers_config.ini')
    headers = dict(config.items('headers'))
    config.read(private_dir / 'cookies_config.ini')
    cookies = dict(config.items('cookies'))

settings = Settings()