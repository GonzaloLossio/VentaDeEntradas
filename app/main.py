from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import engine
from app.models.user import User
from app.models.event import Event
from app.models.order import Order
from app.models.ticket import Ticket
from app.models.zone import Zone
from app.routers.auth import router as auth_router
from app.routers.events import router as events_router
from app.routers.zones import router as zones_router
from app.routers.orders import router as orders_router
from app.routers.webhook import router as webhook_router
from app.routers.tickets import router as tickets_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(events_router, prefix="/api", tags=["events"])
app.include_router(zones_router, prefix="/api", tags=["zones"])
app.include_router(orders_router, prefix="/api", tags=["orders"])
app.include_router(webhook_router, prefix="/api", tags=["webhook"])
app.include_router(webhook_router, prefix="/api", tags=["tickets"])

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@app.get("/")
async def root():
    return ({"Hello" : "World"})