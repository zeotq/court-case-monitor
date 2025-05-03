from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import account_router, auth_router, external_router, case_router
from app.config import FRONTEND_ORIGIN_1, FRONTEND_ORIGIN_2
from app.database import init_db

from app.models.case import CourtCaseDB
from app.models.organisation import OrganisationDB
from app.models.user import UserDB
from app.models.task import TaskDB
from app.models.blacklist import BannedUsersDB
from app.models.association_tables import user_organisation

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

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

app.include_router(account_router)
app.include_router(auth_router)
app.include_router(external_router)
app.include_router(case_router)
