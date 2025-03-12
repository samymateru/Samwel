from typing import Any
import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from psycopg2 import pool
import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from starlette import status

from schema import TokenError, CurrentUser
import secrets
import string
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor

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


def create_jwt_token(data: dict, expiration_days: int = 3) -> str:
    payload = data.copy()
    expiration = datetime.now() + timedelta(days=expiration_days)
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


def get_next_reference(connection: Connection, resource: str, engagement: int):
    query = f"""
        SELECT reference FROM public.{resource}
        WHERE engagement = %s
        ORDER BY reference DESC
        LIMIT 1
    """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (engagement,))
            result = cursor.fetchone()

            if result is None:
                return "REF-0001"

            print(result[0])

            #Extract number, increment, and format
            last_number = int(result[0].split("-")[1])
            print(last_number)
            new_ref = f"REF-{last_number + 1:04d}"
            return new_ref

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching reference {e}")


def get_reference(connection: Connection, resource: str, id: int):
    if resource == "review_comment":
        start: str = "RC"
        relation: str = "sub_program"
    elif resource == "task":
        start = "TSK"
        relation: str = "sub_program"
    else:
        start = "PROC"
        relation: str = "program"
    query = f"""
        SELECT reference FROM public.{resource}
        WHERE {relation} = %s
        ORDER BY reference DESC
        LIMIT 1
    """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (id,))
            result = cursor.fetchone()

            if result is None:
                return f"{start}-0001"

            last_number = int(result[0].split("-")[1])
            print(last_number)
            new_ref = f"{start}-{last_number + 1:04d}"
            return new_ref

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching reference {e}")

# def check_permission(
#     category_name: str,
#     permission: str,
#     user: CurrentUser = Depends(get_current_user),
#     db=Depends(get_db_connection),
# ):
#     # Fetch the role of the current user (we are assuming "Owner" role here for demonstration)
#     user_role = user.user_id
#     query: str = """
#                     SELECT role-->'id' from public.users WHERE id = %s
#                  """
#
#     if user_role == "Owner":
#         # In a real scenario, you would pull the role from the database or other data source
#         # Here we just use the example `owner_role` object.
#         role = ""  # Simulated role object
#
#         # Check if the category exists in the role
#         for category in role.categories:
#             if category.name == category_name:
#                 # Check if the user has the required permission in that category
#                 if permission in category.permissions.dict().get(permission, []):
#                     return True
#                 else:
#                     raise HTTPException(
#                         status_code=status.HTTP_403_FORBIDDEN,
#                         detail=f"You do not have {permission} permission for category {category_name}"
#                     )
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Category {category_name} not found for role {user_role}"
#         )
#
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Unauthorized"
#     )