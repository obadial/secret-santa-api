from sqlmodel import SQLModel, create_engine
from app.config import DATABASE_URL
import os

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    if not os.path.exists("./data"):
        os.makedirs("./data")

    SQLModel.metadata.create_all(engine)
