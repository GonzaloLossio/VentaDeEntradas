import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from app.main import app
from app.database import get_db
from app.models.user import User
from app.models.event import Event
from app.models.zone import Zone
from app.models.order import Order
from app.models.ticket import Ticket
import os
from dotenv import load_dotenv

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

@pytest_asyncio.fixture(scope="function")
async def db():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def client(db):
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()\
    

@pytest_asyncio.fixture(scope="function")
async def auth_headers_admin(client,db):
    from app.models.user import User
    from app.core.security import hash_password

    admin_user = User(
        username="admintest",
        email="admin@test.com",
        hashed_password = hash_password("testpassword"),
        role="admin"
    )
    db.add(admin_user)
    await db.commit()

    response = await client.post("/api/auth/login", data = {
        "username": "admintest",
        "password": "testpassword"
    })
    token = response.json()["access_token"]
    return {"Authorization" : f"Bearer {token}"}

@pytest_asyncio.fixture(scope="function")
async def auth_headers_client(client,db):
    from app.models.user import User
    from app.core.security import hash_password

    client_user = User(
        username="clienttest",
        email="client@test.com",
        hashed_password = hash_password("testpassword"),
        role="client"
    )

    db.add(client_user)
    await db.commit()

    response = await client.post("/api/auth/login", data = {
        "username": "clienttest",
        "password": "testpassword"
    })
    token = response.json()["access_token"]
    return {"Authorization" : f"Bearer {token}"}