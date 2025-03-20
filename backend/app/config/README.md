# Backend config files

## .env
Create a file .env in the root backend folder

```
DATABASE_URL=postgresql://user:password@localhost:5432/db
ARBITR_URL = "https://kad.arbitr.ru"

SECRET_KEY=secret
ALGORITHM=algorithm

ACCESS_TOKEN_EXPIRE_MINUTES=5
REFRESH_TOKEN_EXPIRE_DAYS=30
```

## .ini
Create/configure the .ini files in the config folder
### [headers_config.ini](headers_config.ini)
Headers for parser requests

### [cookies_config.ini]()
Cookie for accessing ARBITR_URL

#### Must have cookies
```

```