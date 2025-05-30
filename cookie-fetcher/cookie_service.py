from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from kad_access_cookies import get_cookies_dict
import asyncio
import json
import os
import time
from contextlib import asynccontextmanager


COOKIE_CACHE_FILE = "data/cookies_cache.json"
MIN_REQUEST_INTERVAL = 60  # seconds
CORS_ORIGINS = [
    "http://backend:8080",
]

lock = asyncio.Lock()
last_request_time = 0
cached_cookies = None


async def load_cached_cookies_from_file():
    if os.path.exists(COOKIE_CACHE_FILE):
        with open(COOKIE_CACHE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return None
    return None

async def save_cached_cookies_to_file(cookies: dict):
    with open(COOKIE_CACHE_FILE, "w") as f:
        json.dump(cookies, f)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global cached_cookies
    cached_cookies = await load_cached_cookies_from_file()
    yield


app = FastAPI(lifespan=lifespan)
router = APIRouter()


@router.get("/cookies", tags=["Cookies"])
async def get_cookies(headless: bool = False, debug: bool = False):
    global last_request_time, cached_cookies

    async with lock:
        now = time.time()

        if cached_cookies is None:
            cached_cookies = await load_cached_cookies_from_file()

        if now - last_request_time < MIN_REQUEST_INTERVAL:
            if cached_cookies:
                return cached_cookies
            else:
                raise HTTPException(503, "Rate limited and no cached cookies available")

        try:
            cookies = await get_cookies_dict(headless=headless, debug=debug)
            if not cookies:
                raise HTTPException(500, "Empty result")

            cached_cookies = cookies
            last_request_time = now
            await save_cached_cookies_to_file(cookies)

            return cookies
        except Exception as e:
            if cached_cookies:
                return cached_cookies
            else:
                raise HTTPException(500, str(e))
            

@router.get("/cookies/file", tags=["Cookies"])
async def get_cookies_from_file():
    cookies = await load_cached_cookies_from_file()
    if cookies is None:
        cookies = await get_cookies(headless=False, debug=False)
    return cookies

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8041)
