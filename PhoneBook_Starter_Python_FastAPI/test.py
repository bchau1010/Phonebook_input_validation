import pytest
from httpx import AsyncClient
from main import app, phone_regex, name_regex  # Ensure your FastAPI app is imported correctly from app.py
from main import validate_phone, validate_name


valid_phones = [
    "12345",
    "(703)111-2121",
    "123-1234",
    "+1(703)111-2121",
    "+32 (21) 212-2324",
    "1(703)123-1234",
    "011 701 111 1234",
    "12345.12345",
    "011 1 703 111 1234",
    "22.22.22.22",
    "2222.2222",
    "111 111 1111",
]


invalid_phones = [
    "123",                        # Too short
    "1/703/123/1234",             # Wrong separator
    "Nr 102-123-1234",            # Non-numeric characters
    '<script>alert("XSS")</script>', # XSS attempt
    "7031111234",                 # Missing separators
    "+1234 (201) 123-1234",       # Invalid country code
    "(001) 123-1234",             # Invalid area code
    "+01 (703) 123-1234",         # Invalid country code
    "(703) 123-1234 ext 204",      # Extension should be allowed but this particular format may be flagged
    "select * from users;" 
]


valid_names = [
    "Bruce Schneier",
    "Schneier, Bruce",
    "Schneier, Bruce Wayne",
    "O’Malley, John F.",
    "John O’Malley-Smith",
    "Cher"
]


invalid_names = [
    "Ron O’’Henry",                  # Double apostrophes
    "Ron O’Henry-Smith-Barnes",       # Too many hyphenated names
    "L33t Hacker",                    # Numbers in name
    '<script>alert("XSS")</script>',  # XSS/HTML tags
    "Brad Everett Samuel Smith",      # Too many name parts (over 3)
    "select * from users;",            # SQL injection
    '<script>alert("XSS")</script>'
]




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