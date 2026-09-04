import bcrypt


from fastapi import APIRouter

from database.connection import get_connection
from pydantic import BaseModel

router = APIRouter(prefix="/login", tags=["Login User"])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


class LoginUser(BaseModel):
    username: str
    password: str
    
@router.post("")
def login_user(user: LoginUser):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_registration WHERE username = %s", (user.username,))
    existing_user = cursor.fetchone()

    if not existing_user:
        return {"message": "Invalid username or password."}

    stored_hashed_password = existing_user[2]  

    if not verify_password(user.password, stored_hashed_password):
        return {"message": "Invalid username or password."}

    return {"message": "Login successful."}