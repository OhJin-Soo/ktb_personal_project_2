from sqlmodel import create_engine, SQLModel, Session
from contextlib import contextmanager

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

@contextmanager
def get_session():
    """
    Use as:
    with get_session() as session:
        ...
    """
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
