from typing import Any
import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from psycopg2 import pool
import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from schema import TokenError, CurrentUser
import secrets
import string

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

connection_pool = pool.SimpleConnectionPool(
            minconn=1,  # Minimum number of connections
            maxconn=10,  # Maximum number of connections
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
        )


def generate_hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt).decode()
    return hashed

def verify_password(stored_hash: bytes, password: str) -> bool:
    return stored_hash == bcrypt.hashpw(password.encode(), stored_hash)


def create_jwt_token(data: dict, expiration_minutes: int = 30) -> str:
    payload = data.copy()
    expiration = datetime.now() + timedelta(minutes=expiration_minutes)
    payload.update({"exp": expiration})
    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
    return token

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenError | Any:
    if not token:
        return CurrentUser(status_code=404, description="auth token not provided")
    try:
        decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        decoded_token["status_code"] = 200
        decoded_token["description"] = "success"
        return CurrentUser(**decoded_token)
    except jwt.ExpiredSignatureError:
        return CurrentUser(status_code=404, description="token expired")
    except jwt.InvalidTokenError:
        return CurrentUser(status_code=404, description="invalid token")

def get_db_connection():
    connection = connection_pool.getconn()
    try:
        yield connection
    finally:
        connection_pool.putconn(connection)

def generated_password() -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(16))
    return password
