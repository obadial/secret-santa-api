from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import create_db_and_tables
from app.routers import blacklist, lists, draw, participants


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(participants.router, prefix="/v1")
app.include_router(blacklist.router, prefix="/v1")
app.include_router(lists.router, prefix="/v1")
app.include_router(draw.router, prefix="/v1")
