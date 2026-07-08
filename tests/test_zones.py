import pytest

@pytest.mark.asyncio
async def test_create_zone(client,auth_headers_admin):
    create_event_response = await client.post("/api/events",json = {
        "title" : "testEvent",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "12:00:00",
        "location" : "Test Location"
    },headers = auth_headers_admin)

    event_id = create_event_response.json()["id"]

    create_zone_response = await client.post(f"/api/events/{event_id}/zones",json = {
        "name" : "testZone",
        "price" : 50.0,
        "capacity" : 100
    },headers = auth_headers_admin)

    assert create_zone_response.status_code == 201
    data = create_zone_response.json()
    assert data["name"] == "testZone"
    assert data["price"] == 50.0
    assert data["capacity"] == 100

@pytest.mark.asyncio
async def test_create_zone_as_client(client,auth_headers_client,auth_headers_admin):
    create_event_response = await client.post("/api/events",json = {
        "title" : "testEvent",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "12:00:00",
        "location" : "Test Location"
    },headers = auth_headers_admin)

    event_id = create_event_response.json()["id"]

    create_zone_response = await client.post(f"/api/events/{event_id}/zones",json = {
        "name" : "testZone",
        "price" : 50.0,
        "capacity" : 100
    },headers = auth_headers_client)

    assert create_zone_response.status_code == 403

@pytest.mark.asyncio
async def test_get_all_zones_from_an_specific_event(client,auth_headers_admin):
    create_event_response = await client.post("/api/events",json = {
        "title" : "testEvent",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "12:00:00",
        "location" : "Test Location"
    },headers = auth_headers_admin)

    event_id = create_event_response.json()["id"]

    await client.post(f"/api/events/{event_id}/zones",json = {
        "name" : "testZone",
        "price" : 50.0,
        "capacity" : 100
    },headers = auth_headers_admin)

    await client.post(f"/api/events/{event_id}/zones",json = {
        "name" : "testZone2",
        "price" : 75.0,
        "capacity" : 150
    },headers = auth_headers_admin)


    get_zones_response = await client.get(f"/api/events/{event_id}/zones")
    assert get_zones_response.status_code == 200
    data = get_zones_response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "testZone"
    assert data[1]["name"] == "testZone2"

@pytest.mark.asyncio
async def test_get_all_zones_from_an_specific_event_no_zones(client,auth_headers_admin):
    create_event_response = await client.post("/api/events",json = {
        "title" : "testEvent",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "12:00:00",
        "location" : "Test Location"
    },headers = auth_headers_admin)

    event_id = create_event_response.json()["id"]

    get_zones_response = await client.get(f"/api/events/{event_id}/zones")
    assert get_zones_response.status_code == 404

@pytest.mark.asyncio
async def test_get_specific_zone_from_an_specific_event(client,auth_headers_admin):
    create_event_response = await client.post("/api/events",json = {
        "title" : "testEvent",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "12:00:00",
        "location" : "Test Location"
    },headers = auth_headers_admin)   

    event_id = create_event_response.json()["id"]

    create_zone_response = await client.post(f"/api/events/{event_id}/zones",json = {
        "name" : "testZone",
        "price" : 50.0,
        "capacity" : 100
    },headers = auth_headers_admin)

    zone_id = create_zone_response.json()["id"]

    get_zone_response = await client.get(f"/api/events/{event_id}/zones/{zone_id}")

    assert get_zone_response.status_code == 200
    data = get_zone_response.json()
    assert data["name"] == "testZone"
    assert data["price"] == 50.0
    assert data["capacity"] == 100

@pytest.mark.asyncio
async def test_get_specific_zone_from_an_specific_event_not_found(client,auth_headers_admin):
    create_event_response = await client.post("/api/events",json = {
        "title" : "testEvent",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "12:00:00",
        "location" : "Test Location"
    },headers = auth_headers_admin)   

    event_id = create_event_response.json()["id"]

    get_zone_response = await client.get(f"/api/events/{event_id}/zones/999")

    assert get_zone_response.status_code == 404


@pytest.mark.asyncio
async def test_update_zone(client,auth_headers_admin):    
    create_event_response = await client.post("/api/events",json = {
        "title" : "testEvent",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "12:00:00",
        "location" : "Test Location"
    },headers = auth_headers_admin)   

    event_id = create_event_response.json()["id"]

    create_zone_response = await client.post(f"/api/events/{event_id}/zones",json = {
        "name" : "testZone",
        "price" : 50.0,
        "capacity" : 100
    },headers = auth_headers_admin)

    zone_id = create_zone_response.json()["id"]

    get_zone_response = await client.put(f"/api/events/{event_id}/zones/{zone_id}",json = {
        "name" : "testZoneUpdated",
        "price" : 75.0,
        "capacity" : 150
    },headers = auth_headers_admin)

    assert get_zone_response.status_code == 200
    data = get_zone_response.json()
    assert data["name"] == "testZoneUpdated"
    assert data["price"] == 75.0
    assert data["capacity"] == 150

@pytest.mark.asyncio   
async def test_update_zone_as_client(client,auth_headers_client,auth_headers_admin):    
    create_event_response = await client.post("/api/events",json = {
        "title" : "testEvent",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "12:00:00",
        "location" : "Test Location"
    },headers = auth_headers_admin)   

    event_id = create_event_response.json()["id"]

    create_zone_response = await client.post(f"/api/events/{event_id}/zones",json = {
        "name" : "testZone",
        "price" : 50.0,
        "capacity" : 100
    },headers = auth_headers_admin)

    zone_id = create_zone_response.json()["id"]

    get_zone_response = await client.put(f"/api/events/{event_id}/zones/{zone_id}",json = {
        "name" : "testZoneUpdated",
        "price" : 75.0,
        "capacity" : 150
    },headers = auth_headers_client)

    assert get_zone_response.status_code == 403

@pytest.mark.asyncio
async def test_update_zone_not_found(client,auth_headers_admin):    
    create_event_response = await client.post("/api/events",json = {
        "title" : "testEvent",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "12:00:00",
        "location" : "Test Location"
    },headers = auth_headers_admin)   

    event_id = create_event_response.json()["id"]

    get_zone_response = await client.put(f"/api/events/{event_id}/zones/999",json = {
        "name" : "testZoneUpdated",
        "price" : 75.0,
        "capacity" : 150
    },headers = auth_headers_admin)

    assert get_zone_response.status_code == 404


@pytest.mark.asyncio
async def test_deactivate_zone(client,auth_headers_admin):
    create_event_response = await client.post("/api/events",json = {
        "title" : "testEvent",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "12:00:00",
        "location" : "Test Location"
    },headers = auth_headers_admin)   

    event_id = create_event_response.json()["id"]

    create_zone_response = await client.post(f"/api/events/{event_id}/zones",json = {
        "name" : "testZone",
        "price" : 50.0,
        "capacity" : 100
    },headers = auth_headers_admin)

    zone_id = create_zone_response.json()["id"]

    deactivate_zone_response = await client.delete(f"/api/events/{event_id}/zones/{zone_id}",headers = auth_headers_admin)

    assert deactivate_zone_response.status_code == 200
    data = deactivate_zone_response.json()
    assert data["is_active"] == False

@pytest.mark.asyncio
async def test_deactivate_zone_as_client(client,auth_headers_client,auth_headers_admin):
    create_event_response = await client.post("/api/events",json = {
        "title" : "testEvent",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "12:00:00",
        "location" : "Test Location"
    },headers = auth_headers_admin)   

    event_id = create_event_response.json()["id"]

    create_zone_response = await client.post(f"/api/events/{event_id}/zones",json = {
        "name" : "testZone",
        "price" : 50.0,
        "capacity" : 100
    },headers = auth_headers_admin)

    zone_id = create_zone_response.json()["id"]

    deactivate_zone_response = await client.delete(f"/api/events/{event_id}/zones/{zone_id}",headers = auth_headers_client)

    assert deactivate_zone_response.status_code == 403         


@pytest.mark.asyncio
async def test_deactivate_zone_not_found(client,auth_headers_admin):
    create_event_response = await client.post("/api/events",json = {
        "title" : "testEvent",
        "description" : "This is a test event",
        "date" : "2028-07-07",
        "time" : "12:00:00",
        "location" : "Test Location"
    },headers = auth_headers_admin)   

    event_id = create_event_response.json()["id"]

    deactivate_zone_response = await client.delete(f"/api/events/{event_id}/zones/999",headers = auth_headers_admin)

    assert deactivate_zone_response.status_code == 404    