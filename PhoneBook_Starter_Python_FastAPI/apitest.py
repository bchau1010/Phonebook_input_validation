# test_endpoints.py
import pytest
from httpx import AsyncClient
from main import app
from testData import valid_phones, valid_names

# Helper function for token retrieval
@pytest.mark.asyncio
async def get_token(username, password):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/token", data={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]

# Test list phonebook with both roles
@pytest.mark.asyncio
@pytest.mark.parametrize("username, password, expected_status", [
    ("readonlyuser", "readonlypassword", 200),
    ("adminuser", "adminpassword", 200),
])
async def test_list_phonebook(username, password, expected_status):
    token = await get_token(username, password)
    async with AsyncClient(app=app, base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/PhoneBook/list", headers=headers)
    assert response.status_code == expected_status
    assert isinstance(response.json(), list), "Expected a list of phonebook entries"

# Test adding a person with both roles
@pytest.mark.asyncio
@pytest.mark.parametrize("username, password, expected_status", [
    ("readonlyuser", "readonlypassword", 403),  
    ("adminuser", "adminpassword", 200),
])
async def test_add_person(username, password, expected_status):
    token = await get_token(username, password)
    async with AsyncClient(app=app, base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {token}"}
        data = {"full_name": "John Doe", "phone_number": "22.22.22.22"}
        response = await client.post("/PhoneBook/add", headers=headers, json=data)
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == {"message": "Person added successfully"}

# Test delete person by name with both roles
@pytest.mark.asyncio
@pytest.mark.parametrize("username, password, expected_status", [
    ("readonlyuser", "readonlypassword", 403),  
    ("adminuser", "adminpassword", 200),
])
async def test_delete_person_by_name(username, password, expected_status):
    token = await get_token(username, password)
    async with AsyncClient(app=app, base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {token}"}
        # Ensure the person is added first if the user has admin access
        if expected_status == 200:
            await client.post("/PhoneBook/add", headers=headers, json={"full_name": valid_names[0], "phone_number": valid_phones[0]})
        response = await client.put("/PhoneBook/deleteByName", headers=headers, json={"full_name": valid_names[0]})
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == {"message": "Person deleted successfully"}

# Test delete person by phone number with both roles
@pytest.mark.asyncio
@pytest.mark.parametrize("username, password, expected_status", [
    ("readonlyuser", "readonlypassword", 403),  
    ("adminuser", "adminpassword", 200),
])
async def test_delete_person_by_phone_number(username, password, expected_status):
    token = await get_token(username, password)
    async with AsyncClient(app=app, base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {token}"}
        # Ensure the person is added first if the user has admin access
        if expected_status == 200:
            await client.post("/PhoneBook/add", headers=headers, json={"full_name": valid_names[0], "phone_number": valid_phones[0]})
        response = await client.put("/PhoneBook/deleteByNumber", headers=headers, json={"phone_number": valid_phones[0]})
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == {"message": "Person deleted successfully"}
