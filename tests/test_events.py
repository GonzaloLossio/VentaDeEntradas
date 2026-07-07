import pytest


@pytest.mark.asyncio
async def test_create_event(client, auth_headers_admin):
    response = await client.post("/api/events", json={
        "title" : "testEvent",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "12:00:00",
        "location" : "Test Location"
    }, headers=auth_headers_admin)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "testEvent"
    assert data["description"] == "This is a test event"
    assert data["date"] == "2028-07-07"
    assert data["time"] == "12:00:00"
    assert data["location"] == "Test Location"

@pytest.mark.asyncio
async def test_create_event_as_client(client,auth_headers_client):
    response = await client.post("/api/events", json={
        "title" : "testEvent",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "12:00:00",
        "location" : "Test Location"
    }, headers=auth_headers_client)

    assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_list_of_events(client, auth_headers_admin):
    await client.post("/api/events",json = {
        "title" : "testEvent",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "12:00:00",
        "location" : "Test Location"
    },headers = auth_headers_admin)
    await client.post("/api/events",json = {
        "title" : "testEvent2",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "17:00:00",
        "location" : "Test Location"
    },headers = auth_headers_admin)

    response = await client.get("/api/events")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["title"] == "testEvent"
    assert data[1]["title"] == "testEvent2"

@pytest.mark.asyncio
async def test_get_list_of_events_empty(client):
    response = await client.get("/api/events")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_event_by_id(client, auth_headers_admin):
    response = await client.post("/api/events",json = {
        "title" : "testEvent",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "12:00:00",
        "location" : "Test Location"
        }, headers = auth_headers_admin) 

    event_id = response.json()["id"]

    response = await client.get(f"/api/events/{event_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "testEvent"   

@pytest.mark.asyncio
async def test_get_event_by_id_not_found(client):
    response = await client.get("/api/events/999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_event(client, auth_headers_admin):
    create_response = await client.post("/api/events", json={
        "title" : "testEvent",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "12:00:00",
        "location" : "Test Location"
    }, headers=auth_headers_admin)

    event_id = create_response.json()["id"]

    response = await client.put(f"/api/events/{event_id}", json={
        "title" : "updatedEvent",
        "description" : "This is an updated test event",
        "date" : "2028-07-08",
        "time" : "14:00:00",
        "location" : "Updated Location"
        }, headers=auth_headers_admin)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "updatedEvent"    

@pytest.mark.asyncio
async def test_update_event_as_client(client, auth_headers_client,auth_headers_admin):
    create_response = await client.post("/api/events", json={
        "title" : "testEvent",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "12:00:00",
        "location" : "Test Location"
    }, headers=auth_headers_admin)

    event_id = create_response.json()["id"]

    response = await client.put(f"/api/events/{event_id}", json={
        "title" : "updatedEvent",
        "description" : "This is an updated test event",
        "date" : "2028-07-08",
        "time" : "14:00:00",
        "location" : "Updated Location"
        }, headers=auth_headers_client)

    assert response.status_code == 403    

@pytest.mark.asyncio
async def test_update_event_not_found(client, auth_headers_admin):
    response = await client.put("/api/events/999", json={
        "title" : "updatedEvent",
        "description" : "This is an updated test event",
        "date" : "2028-07-08",
        "time" : "14:00:00",
        "location" : "Updated Location"
    }, headers=auth_headers_admin)
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_event(client, auth_headers_admin):
    create_response = await client.post("/api/events", json={
        "title" : "testEvent",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "12:00:00",
        "location" : "Test Location"
    }, headers=auth_headers_admin)

    event_id = create_response.json()["id"]

    response = await client.delete(f"/api/events/{event_id}", headers=auth_headers_admin)
    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] == False

@pytest.mark.asyncio
async def test_delete_event_as_client(client, auth_headers_client,auth_headers_admin):
    create_response = await client.post("/api/events", json={
        "title" : "testEvent",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "12:00:00",
        "location" : "Test Location"
    }, headers=auth_headers_admin)

    event_id = create_response.json()["id"]

    response = await client.delete(f"/api/events/{event_id}", headers=auth_headers_client)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_delete_event_not_found(client, auth_headers_admin):
    response = await client.delete("/api/events/999", headers=auth_headers_admin)
    assert response.status_code == 404    