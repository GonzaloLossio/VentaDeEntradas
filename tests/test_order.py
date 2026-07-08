import pytest

@pytest.mark.asyncio
async def test_create_order_success(client, auth_headers_admin, auth_headers_client):
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

    create_order_response = await client.post("/api/orders",json= {
        "tickets" :"2" ,
        "zone_id" : f"{zone_id}"
    },headers = auth_headers_client)

    assert create_order_response.status_code == 200
    data = create_order_response.json()
    assert data["order"]["tickets"] == 2
    assert data["order"]["zone_id"] == zone_id

@pytest.mark.asyncio
async def test_create_order_not_enough_tickets(client, auth_headers_admin, auth_headers_client):
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
        "capacity" : 1
    },headers = auth_headers_admin)

    zone_id = create_zone_response.json()["id"]

    create_order_response = await client.post("/api/orders",json= {
        "tickets" :"2" ,
        "zone_id" : f"{zone_id}"
    },headers = auth_headers_client)

    assert create_order_response.status_code == 400

@pytest.mark.asyncio
async def test_create_order_invalid_zone(client, auth_headers_client):
    create_order_response = await client.post("/api/orders",json= {
        "tickets" :"2" ,
        "zone_id" : 9999
    },headers = auth_headers_client)

    assert create_order_response.status_code == 404

@pytest.mark.asyncio
async def test_get_all_orders(client, auth_headers_admin, auth_headers_client):
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

    await client.post("/api/orders",json= {
        "tickets" :"2" ,
        "zone_id" : f"{zone_id}"
    },headers = auth_headers_client)

    get_orders_response = await client.get("/api/orders/me",headers = auth_headers_client)
    assert get_orders_response.status_code == 200
    data = get_orders_response.json()
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_get_order_empty(client, auth_headers_client):
    get_orders_response = await client.get("/api/orders/me",headers = auth_headers_client)
    assert get_orders_response.status_code == 404