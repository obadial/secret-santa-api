from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import create_db_and_tables
from app.routers import participants, blacklists, lists, draw


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


api_v1 = FastAPI()

api_v1.include_router(participants.router, prefix="/v1")
api_v1.include_router(blacklists.router, prefix="/v1")
api_v1.include_router(lists.router, prefix="/v1")
api_v1.include_router(draw.router, prefix="/v1")


app.mount("/v1", api_v1)
