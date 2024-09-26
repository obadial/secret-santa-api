from fastapi import FastAPI
from app.db import create_db_and_tables, engine
from contextlib import asynccontextmanager
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.exists("./data/database.db"):
        create_db_and_tables()

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/ping")
def ping():
    return {"message": "pong"}
