from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import create_engine, Column, Integer, String
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

import re
import datetime
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from loginInfo import fake_users_db

'''
GO TO THIS ADDRESS FOR UI: http://127.0.0.1:8000/docs
run: `uvicorn main:app --reload`
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
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Password hashing context
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # OAuth2 scheme

app = FastAPI() # Initialize FastAPI app



# phone number with 7 number can be clean , no need for regex
    # replace all allowable extension with empty space (- + . ,)
    # the basic format for phone number is 1 670 123 4567
    #cleaned_phone = phone.replace('+', '').replace('-', '').replace('.', '').replace(' ', '')
phone_regex = re.compile(r"""
    ^                                          # Start of string
    ((\d{5}|                                   # 12345 
        
    \d{5}[-.\s]\d{5})|                      # 12345.12345
        
    (\d{3}[-.\s]\d{4})|                    # 123-4567
        
    (\+?[1-9]\d{0,2})?                      
        (\s?\(?[1-9]\d{1,2}\)?[-.\s]?)     
            (\d{3}[-.\s]\d{4})|                 
        
    ((\+?\d{1,3})[-.\s]\d{1,3}[-.\s]\d{3}[-.\s]\d{3}[-.\s]\d{4}$)|      # +1 234 567 8901
    
    (\d{4}[-.\s]\d{4})|                                  # 1234 5678   
                 
    (\d{2}[-.\s]\d{2}[-.\s]\d{2}[-.\s]\d{2})|              # 22 22 22 22
    
    ((\+?\d{1,3})[-.\s]\d{3}[-.\s]\d{3}[-.\s]\d{4})                 # +1 123 456 7890
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
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")


# Get current active user
def get_current_active_user(current_user: str = Depends(get_current_user)):
    user = get_user(fake_users_db, current_user)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid user")
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
        raise HTTPException(status_code=403, detail="Insufficient privileges")
    return user

# Authorization for write access
def authorize_write(user: dict = Depends(get_current_active_user)):
    if user["role"] != "read/write":
        raise HTTPException(status_code=403, detail="Insufficient privileges")
    return user

'''
# Validate name, need to verify only, leave the exception for endpoint
def validate_name(name):
    if not name_regex.match(name):
        raise HTTPException(status_code=400, detail="Invalid name format")
    if len(name) > 50:
        raise HTTPException(status_code=400, detail="Name exceeds maximum length of 50 characters")

# Validate phone number
def validate_phone(phone):
    cleaned_phone = phone.replace('+', '').replace('-', '').replace('.', '').replace(' ', '')
    if not phone_regex.match(phone):
        raise HTTPException(status_code=400, detail="Invalid phone number format")
    if len(cleaned_phone) > 15:
        raise HTTPException(status_code=400, detail="Phone number exceeds maximum length of 15 digits")
    if not cleaned_phone.isdigit():
        raise HTTPException(status_code=400, detail="Phone number contains invalid characters")
'''
# Validate name, need to verify only, leave the exception for endpoint
def validate_name(name) -> bool:
    if not name_regex.match(name):
        return False
    if len(name) > 50:
        return False
    return True
'''
# Validate phone number
def validate_phone(phone) -> bool:
    cleaned_phone = phone.replace('+', '').replace('-', '').replace('.', '').replace(' ', '').replace('(','').replace(')','')
    if not phone_regex.match(phone):
        print("does not match regex")
        return False
    if len(cleaned_phone) > 15:
        print("longer than 15")
        return False
    if not cleaned_phone.isdigit():
        print("is not digit")
        return False
    return True
'''

def validate_phone(phone) -> bool:
    cleaned_phone = re.sub(r'[^0-9]', '', phone)  # Remove all non-digit characters
    if not phone_regex.match(phone):
        return False
    if len(cleaned_phone) > 15:                   # Limit length to 15 digits
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
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user['username']})
    return {"access_token": access_token, "token_type": "bearer"}

# List phonebook entries (read role)
@app.get("/PhoneBook/list", status_code=status.HTTP_200_OK)
def list_phonebook(current_user: str = Depends(authorize_read)):
    #
    try:
        session = Session()
        phonebook = session.query(PhoneBook).all()
        session.close()
        log_action("LIST", "Listed phonebook entries")
        return phonebook
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Add person to phonebook (write role)
@app.post("/PhoneBook/add", status_code=status.HTTP_200_OK)
def add_person(full_name: str, phone_number: str, current_user: str = Depends(authorize_write)):
    #
    try:
        session = Session()
        # return the bool value of validation, should be true to continue
        if(not validate_name(full_name)):
            raise HTTPException(status_code=400, detail="Invalid input for name")
        if(not validate_phone(phone_number)):
            raise HTTPException(status_code=400, detail="Invalid input for phone number")
        
        existing_person = session.query(PhoneBook).filter_by(phone_number=phone_number).first()
        if existing_person:
            session.close()
            raise HTTPException(status_code=400, detail="Person already exists")
        new_person = PhoneBook(full_name=full_name, phone_number=phone_number)
        session.add(new_person)
        session.commit()
        session.close()
        log_action("ADD", f"Added: {full_name}, {phone_number}")
        return {"message": "Person added successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Delete person by name (write role)
@app.put("/PhoneBook/deleteByName", status_code=status.HTTP_200_OK)
def delete_by_name(full_name: str, current_user: str = Depends(authorize_write)):
    #
    try:
        session = Session()
        # get the first match of the person, if there are more than 1 name
        person = session.query(PhoneBook).filter_by(full_name=full_name).first()
        if not person:
            session.close()
            raise HTTPException(status_code=404, detail="Person not found")
        session.delete(person)
        session.commit()
        session.close()
        #REMEMBER TO ALSO INCLUDE THE NUMBER 
        log_action("DELETE", f"Deleted by name: {full_name},")
        return {"message": "Person deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Delete person by phone number (write role)
@app.put("/PhoneBook/deleteByNumber", status_code=status.HTTP_200_OK)
def delete_by_number(phone_number: str, current_user: str = Depends(authorize_write)):
    try:
        session = Session()
        person = session.query(PhoneBook).filter_by(phone_number=phone_number).first()
        if not person:
            session.close()
            raise HTTPException(status_code=404, detail="Person not found")
        session.delete(person)
        session.commit()
        session.close()
        log_action("DELETE", f"Deleted by phone number and person: {phone_number},{person}")
        return {"message": "Person deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# Run the application with Uvicorn if this script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
