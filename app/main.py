from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import engine
from app.models.user import User
from app.models.event import Event
from app.models.order import Order
from app.models.ticket import Ticket
from app.models.zone import Zone

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@app.get("/")
async def root():
    return ({"Hello" : "World"})