import bcrypt


from fastapi import APIRouter

from database.connection import get_connection
from pydantic import BaseModel

from cryptography.fernet import Fernet

import os

from dotenv import load_dotenv
load_dotenv()  

secret_key = os.getenv("SECRET_KEY")
f = Fernet(secret_key)

def encrypt_token(token: str) -> str:
    token_bytes = token.encode('utf-8')
    encrypted_token = f.encrypt(token_bytes)
    return encrypted_token.decode('utf-8')

def decrypt_token(encrypted_token: str) -> str:
    encrypted_token_bytes = encrypted_token.encode('utf-8')
    decrypted_token_bytes = f.decrypt(encrypted_token_bytes)
    return decrypted_token_bytes.decode('utf-8')

router = APIRouter(prefix="/login", tags=["Login User"])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


class LoginUser(BaseModel):
    username: str
    password: str
    role: str
    
@router.post("")
def login_user(user: LoginUser):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_registration WHERE username = %s", (user.username,))
    existing_user = cursor.fetchone()

    if not existing_user:
        return {"message": "Invalid username or password."}

    stored_hashed_password = existing_user[2]  
    
    user_details = f"{user.username}:{user.role}"
    encrypted_token = encrypt_token(user_details)
    

    if not verify_password(user.password, stored_hashed_password):
        return {"message": "Invalid username or password."}

    return {"message": "Login successful.", "role": user.role, "token": encrypted_token}
