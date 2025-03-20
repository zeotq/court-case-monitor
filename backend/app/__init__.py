from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import auth_router, external_router
from app.config import FRONTEND_ORIGIN_1, FRONTEND_ORIGIN_2


app = FastAPI()

origins = [
    FRONTEND_ORIGIN_1,
    FRONTEND_ORIGIN_2
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(auth_router)
app.include_router(external_router)
