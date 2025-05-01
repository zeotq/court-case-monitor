from os import getenv
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = getenv("DATABASE_URL")
DATABASE_DROP_ALL = getenv("DATABASE_DROP_ALL").lower() == "true"
DATABASE_ECHO = getenv("DATABASE_ECHO").lower() == "true"

ARBITR_URL=getenv("ARBITR_URL")
FRONTEND_ORIGIN_1 = getenv("FRONTEND_ORIGIN_1")
FRONTEND_ORIGIN_2 = getenv("FRONTEND_ORIGIN_2")

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(getenv("REFRESH_TOKEN_EXPIRE_DAYS", ))

COOKIE_URL = getenv("COOKIE_SERVICE_URL", "http://localhost:8041")