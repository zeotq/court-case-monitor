import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from api.endpoints import router as api_router

app = FastAPI()

public_dir = (Path(__file__).parent.parent / "../frontend").resolve()

if not public_dir.exists():
    raise RuntimeError(f"Static dir {public_dir} not found!")

app.mount("/pages", StaticFiles(directory=public_dir, html=True), name="static")

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)