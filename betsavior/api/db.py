import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from betsavior.models.base import Base
from betsavior.models import session as chat_session  # noqa: F401
from betsavior.models import upload as upload_model  # noqa: F401
from betsavior.models import user  # noqa: F401

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://betsavior:password@localhost:5432/betsavior",
)

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
