from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import create_engine, Column, Integer, String
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import re
import datetime
from jose import JWTError, jwt
#import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from loginInfo import fake_users_db

'''
run: `uvicorn main:app --reload`
GO TO THIS ADDRESS FOR UI: http://127.0.0.1:8000/docs
'''


#########################################
#########################################
#########################################
#########################################
#########################################
'''
SETUP FOR USERBASE
SETUP FOR LOGIN SECURITY ALGO
SETUP FOR REGEX
'''

# JWT Configuration for login only 
SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") 

app = FastAPI() 




phone_regex = re.compile(r"""
    ^                                          # Start of string
    ((\d{5}|                                   # 12345 
        
    \d{5}[-.\s]\d{5})|                         # 12345.12345
        
    (\d{3}[-.\s]\d{4})|                        # 123-4567
        
    (\+?[1-9]\d{0,2})?                      
        (\s?\(?[1-9]\d{1,2}\)?[-.\s]?)     
            (\d{3}[-.\s]\d{4})|                 
        
    ((\+?\d{1,3})[-.\s]\d{1,3}[-.\s]\d{3}[-.\s]\d{3}[-.\s]\d{4}$)|      # +1 234 567 8901
    
    (\d{4}[-.\s]\d{4})|                                                 # 1234 5678   
                 
    (\d{2}[-.\s]\d{2}[-.\s]\d{2}[-.\s]\d{2})|                           # 22 22 22 22
    
    ((\+?\d{1,3})[-.\s]\d{3}[-.\s]\d{3}[-.\s]\d{4})                     # +1 123 456 7890
    )$""", re.VERBOSE)


name_regex = re.compile(r"""
    ^                                  
    [a-zA-Z]([-'’\.])?[a-zA-Z]+?    
                        
    (([-'’\.])?,?\s[A-Z]([-'’\.])?[a-zA-Z]+(([\s -])?[A-Z][a-zA-Z]+)?)? 
                 
    (([-'’\.])?,?\s[A-Z]\.(\s[A-Z]([-'’\.])?[a-zA-Z]+(-[A-Z][a-zA-Z]+)?)?)?           
    $                                  
""", re.VERBOSE | re.UNICODE)



#########################################
#########################################
#########################################
#########################################
#########################################
'''
DATABASE SETUP
PHONEBOOK MODEL
'''

# SQLite database setup
engine = create_engine("sqlite:///phonebook.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# PhoneBook model
class PhoneBook(Base):
    __tablename__ = "phonebook"
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    phone_number = Column(String)
Base.metadata.create_all(engine)


#########################################
#########################################
#########################################
#########################################
#########################################
'''
LOGGING FUNCTION
LOGIN PROCCESSING AND TOKENS
'''

# Logging actions
def log_action(action, details):
    timestamp = datetime.datetime.now().isoformat()
    with open("audit.log", "a") as log_file:
        log_file.write(f"{timestamp} - {action}: {details}\n")

# JWT token creation
def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# Password verification
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Get user from database
def get_user(db, username: str):
    user = db.get(username)
    return user if user else None

# Get current user 
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


# Get current active user
def get_current_active_user(current_user: str = Depends(get_current_user)):
    user = get_user(fake_users_db, current_user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
    return user



#########################################
#########################################
#########################################
#########################################
#########################################
'''
READ/WRITE VALIDATION
REGEX INPUT VALIDATION
'''

# Authorization for read access
def authorize_read(user: dict = Depends(get_current_active_user)):
    if user["role"] not in ["read", "read/write"]:
        log_action("Try to list without privileges","Attempt to access data without priviledges")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges")
    return user

# Authorization for write access
def authorize_write(user: dict = Depends(get_current_active_user)):
    if user["role"] != "read/write":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges")
    return user

# Validate name, need to verify only, leave the exception for endpoint
def validate_name(name) -> bool:
    if not name_regex.match(name):
        return False
    if len(name) > 50:
        return False
    return True

# Validate phone, need to verify only, leave the exception for endpoint
def validate_phone(phone) -> bool:
    # Remove all non-digit characters
    cleaned_phone = re.sub(r'[^0-9]', '', phone)  
    if not phone_regex.match(phone):
        return False
    # Limit length to 15 digits
    if len(cleaned_phone) > 15:                   
        return False
    return True


#########################################
#########################################
#########################################
#########################################
#########################################
'''
ENDPOINTS
'''

# Login endpoint
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(fake_users_db, form_data.username)
    if not user or not verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user['username']})
    return {"access_token": access_token, "token_type": "bearer"}

# List phonebook entries
@app.get("/PhoneBook/list", status_code=status.HTTP_200_OK)
def list_phonebook(current_user: str = Depends(authorize_read)):
    try:
        session = Session()
        phonebook = session.query(PhoneBook).all()
        session.close()
        log_action("LIST", "Listed phonebook entries")
        return phonebook
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")

# Add person to phonebook 
@app.post("/PhoneBook/add", status_code=status.HTTP_200_OK)
def add_person(full_name: str, phone_number: str, current_user: str = Depends(authorize_write)):
    try:
        session = Session()
        # Validate name and phone number
        if not validate_name(full_name):
            log_action("Adding denied due to invalidname", f"Denied these input: {full_name}, {phone_number}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input for name")
        if not validate_phone(phone_number):
            log_action("Adding denied due to invalidnumber", f"Denied these input: {full_name}, {phone_number}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input for phone number")
        
        # Check if both full_name and phone_number match an existing record
        existing_person = (
            session.query(PhoneBook)
            .filter_by(full_name=full_name, phone_number=phone_number)
            .first()
        )
        if existing_person:
            session.close()
            log_action("Adding denied due to person already exists", f"Denied these input: {full_name},{phone_number}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Person already exists")

        new_person = PhoneBook(full_name=full_name, phone_number=phone_number)
        session.add(new_person)
        session.commit()
        session.close()

        log_action("ADD", f"Added: {full_name}, {phone_number}")
        return {"message": "Person added successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")

# Delete person by name 
@app.put("/PhoneBook/deleteByName", status_code=status.HTTP_200_OK)
def delete_by_name(full_name: str, current_user: str = Depends(authorize_write)):
    try:
        if(not validate_name(full_name)):
            log_action("DeleteByName denied due to invalidname", f"Denied these input: {full_name}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input for name")
        session = Session()
        
        # get the first match of the person, if there are more than 1 name
        person = session.query(PhoneBook).filter_by(full_name=full_name).first()
        
        if not person:
            session.close()
            log_action("DeleteByName denied due to person not found", f"Denied these input: {full_name}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
        phonenumber = person.phone_number
        session.delete(person)
        session.commit()
        session.close()
        log_action("DELETE", f"Deleted by name, details: {full_name},{phonenumber}")
        return {"message": "Person deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")

# Delete person by phone number 
@app.put("/PhoneBook/deleteByNumber", status_code=status.HTTP_200_OK)
def delete_by_number(phone_number: str, current_user: str = Depends(authorize_write)):
    try:
        session = Session()
        if(not validate_phone(phone_number)):
            log_action("DeleteByNumber denied due to invalidnumber", f"Denied these input: {phone_number}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input for phone number")
        #fetch the first intstance of user that match the phone number
        person = session.query(PhoneBook).filter_by(phone_number=phone_number).first()
        
        if not person:
            session.close()
            log_action("DeleteByNumber denied due to number not found", f"Denied these input: {phone_number}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Number not found")
        session.delete(person)
        session.commit()
        session.close()
        log_action("DELETE", f"Deleted by phone number, details: {phone_number},{person.full_name}")
        return {"message": "Person deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")

'''
@app.delete("/PhoneBook/clear", status_code=status.HTTP_200_OK)
def clear_phonebook(current_user: str = Depends(authorize_write)):
    """
    Clear all entries from the phonebook. Restricted to write-access users.
    """
    try:
        session = Session()
        # Delete all entries from the phonebook table
        session.query(PhoneBook).delete()
        session.commit()
        session.close()
        log_action("CLEAR", f"Cleared all phonebook entries by {current_user}")
        return {"message": "All phonebook entries have been cleared"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while clearing the phonebook: {str(e)}",
        )
'''

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
