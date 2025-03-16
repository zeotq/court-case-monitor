import os
from configparser import RawConfigParser
from dotenv import load_dotenv
from pathlib import Path


class Settings:
    config = RawConfigParser()
    private_dir = (Path(__file__).parent.parent / ".." / ".." / "configs").resolve()

    config.read(private_dir / 'headers_config.ini')
    headers = dict(config.items('headers'))

    config.read(private_dir / 'cookies_config.ini')
    cookies = dict(config.items('cookies'))


settings = Settings()


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 1))