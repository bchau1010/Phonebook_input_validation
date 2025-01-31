import pytest
import logging
from httpx import AsyncClient
from httpx import ASGITransport
from main import app, phone_regex, name_regex, validate_name, validate_phone
from main import validate_phone, validate_name
from testData import valid_phones, invalid_phones, valid_names, invalid_names
from testData import valid_phones2, invalid_phones2, valid_names2, invalid_names2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

########################################
#THIS TEST FILE IS FOR UNIT TESTING OF INDIVIDUAL COMPONENTS
#API TEST DOES NOT INCLUDED IN HERE, EXCEPT FOR AUTHORIZATION


#########################################
#########################################
#########################################
#########################################
#########################################
#VALIDATION TEST

#valid_phones = valid_phones2
#invalid_phones = invalid_phones2
#valid_names = valid_names2
#invalid_names = invalid_names2


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


@pytest.mark.parametrize("Iname", invalid_names)
@pytest.mark.parametrize("name", valid_names)
def test_validate_names(Iname, name):
    assert not validate_name(Iname), f"Expected {Iname} to be invalid"
    assert validate_name(name), f"Expected {name} to be valid"

@pytest.mark.parametrize("phone", valid_phones)
@pytest.mark.parametrize("Iphone", invalid_phones)
def test_validate_phone_numbers(phone, Iphone):
    assert validate_phone(phone), f"Expected {phone} to be valid"
    assert not validate_phone(Iphone), f"Expected {Iphone} to be invalid"


#########################################
#########################################
#########################################
#########################################
#########################################
# ENDPOINT TEST ONLY FOR AUTHORIZATION

# Helper function for token retrieval
@pytest.mark.asyncio
async def get_token(username, password):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/token", data={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.mark.asyncio
@pytest.mark.parametrize("username, password, expected_status", [
    ("readonlyuser", "readonlypassword", 200),
    ("adminuser", "adminpassword", 200),
])
async def test_list_phonebook(username, password, expected_status):
    token = await get_token(username, password)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/PhoneBook/list", headers=headers)
    assert response.status_code == expected_status
    assert isinstance(response.json(), list), "Expected a list of phonebook entries"

# Test adding person with either admin or read only user
@pytest.mark.asyncio
@pytest.mark.parametrize("username, password, expected_status", [
    ("readonlyuser", "readonlypassword", 403),
    ("adminuser", "adminpassword", 200),])
async def test_add_person(username, password, expected_status):
    token = await get_token(username, password)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.post("/PhoneBook/add?full_name=John Doe&phone_number=123-4567", headers=headers)
        if response.status_code != expected_status:
            logger.error(f"Failed to add person. Status code: {response.status_code}, Response: {response.json()}")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == {"message": "Person added successfully"}

# Test delete by name with either admin or read only user
@pytest.mark.asyncio
@pytest.mark.parametrize("username, password, expected_status", [
    ("readonlyuser", "readonlypassword", 403),  
    ("adminuser", "adminpassword", 200),])
async def test_delete_person_by_name(username, password, expected_status):
    token = await get_token(username, password)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {token}"}
        if expected_status == 200:
            await client.post("/PhoneBook/add?full_name=John Doe&phone_number=123-4567", headers=headers)
        response = await client.put("/PhoneBook/deleteByName?full_name=John Doe", headers=headers)
        if response.status_code != expected_status:
            logger.error(f"Failed to delete person by name. Status code: {response.status_code}, Response: {response.json()}")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == {"message": "Person deleted successfully"}
        
# Test delete by number with either admin or read only user
@pytest.mark.asyncio
@pytest.mark.parametrize("username, password, expected_status", [
    ("readonlyuser", "readonlypassword", 403),  
    ("adminuser", "adminpassword", 200),])
async def test_delete_person_by_phone_number(username, password, expected_status):
    token = await get_token(username, password)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {token}"}
        if expected_status == 200:
            await client.post("/PhoneBook/add?full_name=John Doe&phone_number=123-4567", headers=headers)
        response = await client.put("/PhoneBook/deleteByNumber?phone_number=123-4567", headers=headers)
        if response.status_code != expected_status:
            logger.error(f"Failed to delete person by phone number. Status code: {response.status_code}, Response: {response.json()}")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == {"message": "Person deleted successfully"}



