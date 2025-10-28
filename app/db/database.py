from sqlmodel import create_engine, Session, SQLModel
from contextlib import contextmanager
import os
import logging

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///appointment.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)


def get_engine():
    return engine


@contextmanager
def get_session():
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception as e:
        logging.exception(f"Error in database session: {e}")
        session.rollback()
        raise
    finally:
        session.close()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)