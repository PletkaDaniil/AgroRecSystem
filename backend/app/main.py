from fastapi import FastAPI
from app.routes.router import router
from app.database.database import init_db

app = FastAPI()
init_db()

app.include_router(
    router=router, prefix='/api'
)
