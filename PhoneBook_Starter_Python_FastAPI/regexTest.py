import pytest
from httpx import AsyncClient
from main import app, phone_regex, name_regex, validate_name, validate_phone
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
# ENDPOINT TEST

# Helper function for token retrieval
@pytest.mark.asyncio
async def get_token(username, password):
    async with AsyncClient(app=app, base_url="http://test") as client:
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
    async with AsyncClient(app=app, base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/PhoneBook/list", headers=headers)
    assert response.status_code == expected_status
    assert isinstance(response.json(), list), "Expected a list of phonebook entries"

#############################################################
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