import time
from typing import Any, Dict, List
import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from psycopg2 import pool
import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
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
        relation: str = "engagement"
    elif resource == "task":
        start = "TSK"
        relation: str = "engagement"
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
            print(result)

            if result is None:
                return f"{start}-0001"

            last_number = int(result[0].split("-")[1])
            new_ref = f"{start}-{last_number + 1:04d}"
            return new_ref

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching reference {e}")

def has_permission(roles: List[Dict], resource: str, action: str):
    for role in roles:
        permissions = role.get("permissions")
        if permissions is None:
            raise HTTPException(status_code=402, detail="Bad role format ")
        actions = permissions.get(resource)
        if actions is None:
            raise HTTPException(status_code=402, detail="Bad role format  permissions are not added")
        if action in actions:
            return True
        else:
            return False

def check_permission(resource: str, action: str):
    def dependency(user: CurrentUser = Depends(get_current_user), connection: Connection = Depends(get_db_connection)):
        query_user_roles: str = """
                                SELECT role from public.users WHERE id = %s
                                """
        query_roles = """
                         SELECT * FROM public.roles WHERE id = %s
                      """
        try:
            with connection.cursor() as cursor:
                cursor: Cursor
                cursor.execute(query_user_roles, (user.user_id,))
                rows = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                data = [dict(zip(column_names, row_)) for row_ in rows]
                for role in data[0].get("role"):
                    cursor.execute(query_roles, (81,))
                    rows = cursor.fetchall()
                    column_names = [desc[0] for desc in cursor.description]
                    data = [dict(zip(column_names, row_)) for row_ in rows]
                    print(data)
        except Exception as e:
            connection.rollback()
            raise HTTPException(status_code=400, detail=f"Error occur while fetching roles{e}")
        role = [{
            "name": "Owner",
            "permissions": {
                "user-roles": ["create", "view", "delete", "update", "assign", "approve"],
                "account-profile": ["create", "view", "delete", "update", "assign", "approve"],
                "subscription": ["create", "delete", "update", "assign", "approve"]
            }
        }
        ]
        if not has_permission(role, resource, action):
            raise HTTPException(status_code=403, detail="Permission Denied")
        return True
    return dependency




