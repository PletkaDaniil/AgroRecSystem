from fastapi import FastAPI
from app.routes.router import router
from app.routes.file_router import file_router
from app.database.database import init_db
from fastapi.middleware.cors import CORSMiddleware
from app.config.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.allow_origins,
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allow_methods,
    allow_headers=settings.cors.allow_headers,
)

init_db()

app.include_router(
    router=router, prefix='/api'
)
app.include_router(
    router=file_router, prefix='/api'
)
