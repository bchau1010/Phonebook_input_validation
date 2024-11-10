import pytest
from httpx import AsyncClient
from main import app, phone_regex, name_regex  # Ensure your FastAPI app is imported correctly from app.py
from main import validate_phone, validate_name
from testData import valid_phones, invalid_phones, valid_names, invalid_names




#########################################
#########################################
#########################################
#########################################
#########################################
#VALIDATION TEST

@pytest.mark.parametrize("phone", valid_phones)
def test_valid_phone_numbers(phone):
    assert phone_regex.match(phone), f"Expected {phone} to be valid"


@pytest.mark.parametrize("phone", invalid_phones)
def test_invalid_phone_numbers(phone):
    assert not phone_regex.match(phone), f"Expected {phone} to be invalid"


@pytest.mark.parametrize("name", valid_names)
def test_valid_names(name):
    assert name_regex.match(name), f"Expected {name} to be valid"

@pytest.mark.parametrize("name", invalid_names)
def test_invalid_names(name):
    assert not name_regex.match(name), f"Expected {name} to be invalid"


#########################################
#########################################
#########################################
#########################################
#########################################
# ENDPOINT TEST

'''
@pytest.mark.asyncio
async def test_list_phonebook():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/PhoneBook/list")
    assert response.status_code == 200
    assert isinstance(response.json(), list), "Expected a list of phonebook entries"


@pytest.mark.asyncio
@pytest.mark.parametrize("full_name, phone_number", zip(valid_names, valid_phones))
async def test_add_person_valid(full_name, phone_number):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/PhoneBook/add", json={"full_name": full_name, "phone_number": phone_number})
    assert response.status_code == 200
    assert response.json() == {"message": "Person added successfully"}


@pytest.mark.asyncio
@pytest.mark.parametrize("full_name", invalid_names)
async def test_add_person_invalid_name(full_name):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/PhoneBook/add", json={"full_name": full_name, "phone_number": valid_phones[0]})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid input for name"}


@pytest.mark.asyncio
@pytest.mark.parametrize("phone_number", invalid_phones)
async def test_add_person_invalid_phone(phone_number):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/PhoneBook/add", json={"full_name": valid_names[0], "phone_number": phone_number})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid input for phone number"}


@pytest.mark.asyncio
@pytest.mark.parametrize("full_name", valid_names)
async def test_delete_person_by_name(full_name):
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Add a person to ensure there is an entry to delete
        await client.post("/PhoneBook/add", json={"full_name": full_name, "phone_number": valid_phones[0]})
        
        # Delete by name
        response = await client.put("/PhoneBook/deleteByName", json={"full_name": full_name})
    assert response.status_code == 200
    assert response.json() == {"message": "Person deleted successfully"}


@pytest.mark.asyncio
@pytest.mark.parametrize("phone_number", valid_phones)
async def test_delete_person_by_phone_number(phone_number):
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Add a person to ensure there is an entry to delete
        await client.post("/PhoneBook/add", json={"full_name": valid_names[0], "phone_number": phone_number})
        
        # Delete by phone number
        response = await client.put("/PhoneBook/deleteByNumber", json={"phone_number": phone_number})
    assert response.status_code == 200
    assert response.json() == {"message": "Person deleted successfully"}
'''