from typing import Any, Dict, List, Optional
from contextlib import asynccontextmanager
import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from psycopg2 import pool
import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from psycopg_pool import AsyncConnectionPool

from schema import UserData, CurrentUser
import secrets
import string
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

connection_pool = pool.SimpleConnectionPool(
            minconn=1,  # Minimum number of connections
            maxconn=100,  # Maximum number of connections
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
        )

connection_pool_async = AsyncConnectionPool(
    conninfo=f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
    min_size=1,
    max_size=10,
    open=False  # prevent auto-opening (this removes the warning)
)

connection_pool_async_: Optional[AsyncConnectionPool] = None

@asynccontextmanager
async def get_db_connection_async():
    global connection_pool_async_
    if not connection_pool_async_:
        connection_pool_async_ = AsyncConnectionPool(
            conninfo=f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
            min_size=1,
            max_size=10,
            open=False,  # IMPORTANT: prevent auto-opening
        )
        await connection_pool_async.open()  # Manually open it

    async with connection_pool_async.connection() as conn:
        yield conn

async def get_async_db_connection():
    async with get_db_connection_async() as conn:
        yield conn

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

def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        return CurrentUser(status_code=401, description="auth token not provided")
    try:
        decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        decoded_token["status_code"] = 200
        decoded_token["description"] = "success"
        return CurrentUser(**decoded_token)
    except jwt.ExpiredSignatureError:
        return CurrentUser(status_code=401, description="token expired")
    except jwt.InvalidTokenError:
        return CurrentUser(status_code=401, description="invalid token")

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
            if result is None:
                return f"{start}-0001"

            last_number = int(result[0].split("-")[1])
            new_ref = f"{start}-{last_number + 1:04d}"
            return new_ref

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching reference {e}")

def get_user_data(token: str = Depends(oauth2_scheme)):
    if not token:
        return CurrentUser(status_code=401, description="auth token not provided")
    query: str = """
                  SELECT * FROM public.users WHERE id = %s;
                 """
    query_roles: str = """
                  SELECT * FROM public.roles WHERE company = %s;
                 """
    try:
        decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        connection: Connection = next(get_db_connection())
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (decoded_token.get("user_id"),))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            user_data = [dict(zip(column_names, row_)) for row_ in rows][0]

            cursor.execute(query_roles, (decoded_token.get("company_id"),))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            roles_data = [dict(zip(column_names, row_)) for row_ in rows]

            user = UserData(
                id=user_data.get("id"),
                name=user_data.get("name"),
                email=user_data.get("email"),
                telephone=user_data.get("telephone"),
                status=user_data.get("status"),
                company_roles=roles_data[0].get("roles"),
                user_role=user_data.get("role"),
                module=user_data.get("module"),
                type=user_data.get("type")
            )

            return user
    except jwt.ExpiredSignatureError:
        return CurrentUser(status_code=401, description="token expired")
    except jwt.InvalidTokenError:
        return CurrentUser(status_code=401, description="invalid token")


def authorize(user_roles: list, module: str, required_permission: str) -> bool:
    for role in user_roles:
        permissions = role.get("permissions", {})
        if module in permissions:
            if required_permission in permissions[module]:
                return True
    return False

def check_permission(module: str, action: str):
    def inner(user: UserData = Depends(get_user_data)):
        roles = []
        for company_role in user.company_roles:
            for role in user.user_role:
                if role.get("name") == company_role.get("name"):
                    roles.append(company_role)

        if not authorize(roles, module, action):
            raise HTTPException(status_code=403, detail="Unauthorized")
    return inner


from psycopg import  AsyncConnection
async def test_async(conn: AsyncConnection):
    async with conn.cursor() as cur:
        await cur.execute("select * from companies")
        data = await  cur.fetchone()
        print(data)



