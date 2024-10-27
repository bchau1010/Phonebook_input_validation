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


valid_phones += [
    "(123) 456-7890",
    "202.555.0188",
    "123 456 7890",
    "+44 20 7946 0958",
    "1-800-555-5555",
    "1 (800) 555-5555",
    "+1-800-555-5555",
    "+86 (10) 1234 5678",
    "+81 3 1234 5678",
    "011 44 20 7946 0958",
    "001 (510) 555-5555",
    "+61 (2) 9876 5432",
    "011 44 7911 123456",
    "+91 80 1234 5678",
    "1-700-555-5555",
    "011 86 10 1234 5678",
    "011 81 3 1234 5678",
    "+1 415-555-2671",
    "+1 (949) 555-2671",
    "+27 21 555 5555",
    "011 61 2 9876 5432",
    "011 86 21 9876 5432",
    "+49 (30) 1234-5678",
    "+55 11 98765-4321",
    "12345-12345",
    "0044 20 7946 0958",
    "+1 (650) 555-3456",
    "011 972 2 1234567",
    "+971 4 123 4567",
    "011 852 1234 5678",
    "+7 495 123-4567",
    "011 55 21 1234 5678",
    "+1-650-555-1234",
    "011 81 50 1234 5678",
    "+1 212 555 1234",
    "+1 646 555 4567",
    "(555) 123-4567",
    "+31 (0) 20 555 1234",
    "011 32 2 555 1234",
    "+39 06 555 1234",
    "011 30 21 555 1234",
]

invalid_phones += [
    "12",                             # Too short
    "1234/567",                       # Wrong format with slash
    "555-555-55555",                  # Too many digits
    "(123)-456-789",                  # Area code incorrectly formatted
    "+(123) 456-7890",                # Invalid country code format
    "(123)-456/7890",                 # Wrong separator
    "555-555-555a",                   # Alphabetic character
    "+123 (456) 789 12345",           # Too long
    "01112345678901",                 # Missing spaces
    "+01 (800) 555-1234",             # Invalid country code (leading zero)
    "(000) 555-1234",                 # Invalid area code (all zeros)
    "(123) 555 12345",                # Too long after area code
    "555-555-555",                    # Too few digits
    "555.555.555a",                   # Contains letter
    "555*555*5555",                   # Invalid separator
    "+1 (123) 555_1234",              # Invalid separator (_)
    "(555)123-456",                   # Too short after area code
    "(12345) 123-1234",               # Invalid area code
    "123-1234-1234",                  # Too many parts
    "555-555-555-5555",               # Too many sections
    "555 555 555",                    # Too few digits
    "555 555 5555 555",               # Too many digits
    "555-555 555",                    # Missing a digit
    "555-5555555",                    # Missing separator
    "555.555555",                     # Missing separator
    "555..555.5555",                  # Double separator
    "555.5555.555",                   # Incorrect format
    "(555 555-5555 ext)",             # Missing extension number
    "555-555-555 ext",                # Incomplete extension
    "555-555-5555 ext123456",         # Extension too long
    "555-555-5555x",                  # Incomplete extension with "x"
    "+1 (555) 555 555a",              # Contains letter
    "5555 555 5555",                  # Invalid area code length
    "1-800 555 555",                  # Missing digit
    "+1 (555) 555 555a",              # Contains letter
    "(555) 555-5555 x99999",          # Extension too long
    "+1 (123) 555 12a4",              # Contains letter in subscriber number
    "123-123-12345",                  # Too many digits
    "+1 (123) 555-555555",            # Too many digits in subscriber number
    "(123) 555 12a4",                 # Contains letter in subscriber number
    "+1-555-5555-1234",                # Invalid separator placement
    " ",
]

valid_names += [
    "Ann Marie",
    "Anne O’Hara",
    "Patrick O'Connor",
    "John F. Kennedy",
    "A.J. Abrams",
    "Saoirse Ronan",
    "Michael O’Leary",
    "Sir Isaac Newton",
    "Alexander Graham Bell",
    "Barack Obama",
    "Elon Musk",
    "Tim Berners-Lee",
    "William R. Hearst",
    "Serena O'Connell",
    "O’Brian, Lisa",
    "Van Helsing",
    "O’Connell, John P.",
    "Patricia O'Malley",
    "James O'Shea",
    "John O'Kelly",
    "Lara Croft",
    "Elizabeth Bennet",
    "Sherlock Holmes",
    "Dwayne O'Neil",
    "Patrick O’Doyle",
    "O’Brien, Michael J.",
    "Hugh O'Malley",
    "O’Sullivan, Liam",
    "Samantha O’Neal",
    "Santiago O’Rourke",
    "Patricia O'Reilly",
    "Catherine O'Donoghue",
    "O’Toole, Bryan",
    "Gordon O’Reilly",
    "Jessica O’Connor",
    "Bridget O’Carroll",
    "Jean O’Rourke",
    "Claire O'Malley"
]

invalid_names += [
    " ",
    "12345",                            # Numbers in name
    "John123",                          # Numbers in first name
    "O’123Malley",                      # Numbers in last name
    "Jean-Luc Pic@rd",                  # Special characters in name
    "Marie$$$Claire",                   # Invalid special characters
    "Anne O’’Connor",                   # Double apostrophe
    "Patrick O'Connor-Smith-Jones",     # Too many hyphenated names
    "<script>alert('XSS')",             # XSS attack
    "Michael O’Leary123",               # Numbers in last name
    "FitzGer@ld",                       # Invalid character
    "John O''''Malley",                 # Multiple apostrophes
    "Marie-Ann-Pierre",                 # Too many hyphens
    "Jean-Luc Picard-Dupont-Baker",     # Too many hyphenated last names
    "O'Malley, John Paul Smith",        # More than one first/middle name
    "John O''''"
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