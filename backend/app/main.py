from fastapi import FastAPI
from app.routes.router import router
from app.routes.users_router import users_router
from app.routes.file_router import file_router
from app.routes.calc_router import calculator_router
from app.database.database import init_db
from fastapi.middleware.cors import CORSMiddleware
from app.config.config import settings
from app.utils.exceptions import AppError, app_error_handler, unhandled_exception_handler
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

handler = RotatingFileHandler(
    LOG_DIR / "app.log",
    maxBytes=10 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8",
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[handler],
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.allow_origins,
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allow_methods,
    allow_headers=settings.cors.allow_headers,
)

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

init_db()

app.include_router(router=router, prefix='/api')
app.include_router(router=file_router, prefix='/api')
app.include_router(router=calculator_router, prefix='/api')
app.include_router(router=users_router, prefix='/api')