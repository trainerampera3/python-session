from fastapi import APIRouter

from database.connection import get_connection

from pydantic import BaseModel

from passlib.context import CryptContext

import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/signup", tags=["Create User"])


class User(BaseModel):
    username: str
    password: str



def get_password_hash(password: str) -> str:

    password_bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)

    return hashed.decode('utf-8')




# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

@router.post("")
def create_user(user: User):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_registration WHERE username = %s", (user.username,))
    existing_user = cursor.fetchone()

    if existing_user:
        return {"message": "Username already exists."}


    cursor.execute(
        "INSERT INTO user_registration (username, password) VALUES (%s, %s)",
        (user.username, get_password_hash(user.password))
    )
    connection.commit()

    return {"message": "User created successfully."}


