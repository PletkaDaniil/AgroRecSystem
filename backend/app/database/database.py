from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.config import settings
from app.database.models.models import Base

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.db.PG_USER}:{settings.db.PG_PASSWORD}"
    f"@{settings.db.PG_HOST}:{settings.db.PG_PORT}/{settings.db.PG_DBNAME}"
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


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
