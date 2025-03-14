from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import auth_router, external_router


app = FastAPI()

# Разрешённые источники (origins)
origins = [
    "http://localhost:3000",
    "http://localhost:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Разрешённые домены
    allow_credentials=True,  # Разрешение кук и авторизации
    allow_methods=["POST"],  # Разрешённые методы (безопасно ограничить)
    allow_headers=["Content-Type", "Authorization"],  # Разрешённые заголовки
)

app.include_router(auth_router)
app.include_router(external_router)
