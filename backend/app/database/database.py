import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models.models import Base

PATH = "app/database/settings.json"
with open(PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{config['PG_USER']}:{config['PG_PASSWORD']}"
    f"@{config['PG_HOST']}:{config['PG_PORT']}/{config['PG_DBNAME']}"
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

Session = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    return Session()
