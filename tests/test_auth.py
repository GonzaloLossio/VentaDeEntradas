import pytest

@pytest.mark.asyncio 
async def test_register_user(client):
    response = await client.post("/api/auth/register", json = {
        "username" : "testuser",
        "email" : "testuser@example.com",
        "password" : "testpassword"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"

@pytest.mark.asyncio
async def test_register_duplicate_user(client):    
    await client.post("/api/auth/register", json = {
        "username" : " testuser",
        "email" : "testuser@example.com",
        "password" : "testpassword"
    })
    response = await client.post("/api/auth/register", json = {
        "username" : " testuser",
        "email" : "another@example.com",
        "password" : "testpassword"
    })
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_login_success(client):
    await client.post("/api/auth/register", json = {
        "username" : " testuser",
        "email" : "testuser@example.com",
        "password" : "testpassword"
    })

    response = await client.post("/api/auth/login", data = {
        "username" : " testuser",
        "password" : "testpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_failure_wrong_password(client):
    await client.post("/api/auth/register", json = {
        "username" : " testuser",
        "email" : "testuser@example.com",
        "password" : "testpassword"
    })

    response = await client.post("/api/auth/login", data = {
        "username" : " testuser",
        "password" : "wrongpassword"
    })
    assert response.status_code == 401
