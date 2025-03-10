from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api.routers import auth_router, external_router


app = FastAPI()

public_dir = (Path(__file__).resolve().parent.parent.parent / "frontend").resolve()

if not public_dir.exists():
    raise RuntimeError(f"Static dir {public_dir} not found!")

app.mount("/p", StaticFiles(directory=public_dir, html=True), name="static")

app.include_router(auth_router)
app.include_router(external_router)
