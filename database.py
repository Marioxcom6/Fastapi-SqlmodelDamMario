from sqlmodel import SQLModel, create_engine, Session
from contextlib import asynccontextmanager

DATABASE_URL = "sqlite:///db/mydatabase.db"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    return Session(engine)

@asynccontextmanager
async def lifespan(app):
    print("Initializing the database...")
    SQLModel.metadata.create_all(engine)
    yield
    print("Closing database connection...")

