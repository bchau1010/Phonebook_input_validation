from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "readonlyuser": {
        "username": "readonlyuser",
        "hashed_password": pwd_context.hash("readonlypassword"),
        "role": "read",
        "token": ""
    },
    "adminuser": {
        "username": "adminuser",
        "hashed_password": pwd_context.hash("adminpassword"),
        "role": "read/write",
        "token": ""
    }
}
