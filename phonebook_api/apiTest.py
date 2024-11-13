import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from main import app
from testData import valid_phones, invalid_phones, valid_names, invalid_names

# Helper function for token retrieval
@pytest.mark.asyncio
async def get_token(username, password):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/token", data={"username": username, "password": password})
    assert response.status_code == 200, f"Failed to get token. Response: {response.text}"
    return response.json()["access_token"]

@pytest.mark.asyncio
@pytest.mark.parametrize("phone", valid_phones)
@pytest.mark.parametrize("name", valid_names)
async def test_add_person_valid_inputs(phone, name):
    token = await get_token("adminuser", "adminpassword")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Step 1: Add the person
        add_response = await client.post(
            f"/PhoneBook/add?full_name={name}&phone_number={phone}", 
            headers=headers
        )
        assert add_response.status_code == 200, f"Failed to add valid person. Response: {add_response.text}"
        assert add_response.json() == {"message": "Person added successfully"}

        # Step 2: Delete the person by phone number
        delete_response = await client.put(
            f"/PhoneBook/deleteByNumber?phone_number={phone}", 
            headers=headers
        )
        assert delete_response.status_code == 200, f"Failed to delete person. Response: {delete_response.text}"
        assert delete_response.json() == {"message": "Person deleted successfully"}

@pytest.mark.asyncio
@pytest.mark.parametrize("phone", invalid_phones)
@pytest.mark.parametrize("name", invalid_names)
async def test_add_person_invalid_inputs(phone, name):
    token = await get_token("adminuser", "adminpassword")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.post(f"/PhoneBook/add?full_name={name}&phone_number={phone}", headers=headers)
    assert response.status_code in (400, 500), f"Unexpected status for invalid input. Response: {response.text}"

# Test delete_by_name endpoint
@pytest.mark.asyncio
@pytest.mark.parametrize("name", valid_names)
async def test_delete_by_name_valid(name):
    token = await get_token("adminuser", "adminpassword")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {token}"}
        # Add a person first
        await client.post(f"/PhoneBook/add?full_name={name}&phone_number=123-4567", headers=headers)
        # Delete the person
        response = await client.put(f"/PhoneBook/deleteByName?full_name={name}", headers=headers)
    assert response.status_code == 200, f"Failed to delete person by name. Response: {response.text}"
    assert response.json() == {"message": "Person deleted successfully"}

@pytest.mark.asyncio
@pytest.mark.parametrize("name", invalid_names)
async def test_delete_by_name_invalid(name):
    token = await get_token("adminuser", "adminpassword")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.put(f"/PhoneBook/deleteByName?full_name={name}", headers=headers)
    assert response.status_code in (400, 404), f"Unexpected status for invalid name. Response: {response.text}"

# Test delete_by_number endpoint
@pytest.mark.asyncio
@pytest.mark.parametrize("phone", valid_phones)
async def test_delete_by_number_valid(phone):
    token = await get_token("adminuser", "adminpassword")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {token}"}
        # Add a person first
        await client.post(f"/PhoneBook/add?full_name=John Doe&phone_number={phone}", headers=headers)
        # Delete the person
        response = await client.put(f"/PhoneBook/deleteByNumber?phone_number={phone}", headers=headers)
    assert response.status_code == 200, f"Failed to delete person by number. Response: {response.text}"
    assert response.json() == {"message": "Person deleted successfully"}

@pytest.mark.asyncio
@pytest.mark.parametrize("phone", invalid_phones)
async def test_delete_by_number_invalid(phone):
    token = await get_token("adminuser", "adminpassword")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.put(f"/PhoneBook/deleteByNumber?phone_number={phone}", headers=headers)
    assert response.status_code in (400, 404), f"Unexpected status for invalid phone number. Response: {response.text}"
