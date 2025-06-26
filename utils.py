from typing import Optional
from contextlib import asynccontextmanager
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from psycopg2 import pool
import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from psycopg_pool import AsyncConnectionPool
import uuid
from schema import UserData, CurrentUser
import secrets
import string
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from psycopg import AsyncConnection, sql
from psycopg.errors import UniqueViolation, UndefinedColumn, UndefinedFunction
from typing import List
import redis.asyncio as redis
from redis.asyncio import Redis



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
redis_client: Optional[Redis] = None


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


def create_jwt_token(data: dict, expiration_time: int = 2) -> str:
    payload = data.copy()
    expiration = datetime.now(timezone.utc) + timedelta(days=expiration_time)
    payload.update({"exp": int(expiration.timestamp())})
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


async def get_next_reference(connection: AsyncConnection, resource: str, engagement_id: str):
    query = sql.SQL(
        """
        SELECT reference FROM {resource}
        WHERE engagement = %s
        ORDER BY reference DESC
        LIMIT 1
    """).format(resource=sql.Identifier('public', resource))
    prefix_map = {
        "finalization_procedure": "FNL",
        "std_template": "PLN",
        "reporting_procedure": "RPT",
    }
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            result = await cursor.fetchone()

            if result is None:
                return f"{prefix_map.get(resource)}-0001"

            #Extract number, increment, and format
            last_number = int(result[0].split("-")[1])
            new_ref = f"{prefix_map.get(resource)}-{last_number + 1:04d}"
            return new_ref

    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching reference {e}")


async def get_reference(connection: AsyncConnection, resource: str, id: str):
    if resource == "review_comment":
        start: str = "RC"
        relation: str = "engagement"
    elif resource == "task":
        start = "TSK"
        relation: str = "engagement"
    else:
        start = "PROC"
        relation: str = "program"

    query = sql.SQL("""
        SELECT reference FROM {table}
        WHERE {column} = %s
        ORDER BY reference DESC
        LIMIT 1
    """).format(
        table=sql.Identifier('public', resource),
        column=sql.Identifier(relation)
    )
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (id,))
            result = await cursor.fetchone()
            if result is None:
                return f"{start}-0001"

            last_number = int(result[0].split("-")[1])
            new_ref = f"{start}-{last_number + 1:04d}"
            return new_ref
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching reference {e}")

async def get_next_issue_id():
    pass

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

def get_unique_key():
    uuid_str = str(uuid.uuid4()).split("-")
    key = uuid_str[0] + uuid_str[1]
    return key

async def is_data_exist(connection: AsyncConnection, table: str, column: str, id: str):
    query = sql.SQL("SELECT {column} FROM {table} WHERE id = %s").format(
        column=sql.Identifier(column),
        table=sql.Identifier('public', table)
    )
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (id,))
            rows = await cursor.fetchone()
            if rows is not None:
                raise UniqueViolation()
    except UniqueViolation:
        raise UniqueViolation()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching data {e}")

async def query_any_data(
        connection: AsyncConnection,
        table: str,
        columns: List[str],
        where_clause: str,
        value: str
):
    query = sql.SQL(
        """
        SELECT {columns} FROM {table} WHERE {where_clause} = %s;
        """
    ).format(
        table=sql.Identifier('public', table),
        columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
        where_clause=sql.Identifier(where_clause)
    )
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (value,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except UndefinedColumn:
        await connection.rollback()
        print("Column doesnt exists")
    except UndefinedFunction:
        await connection.rollback()
        print("There is data type mismatch")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching data from table {table} {e}")

def generate_attachment():
    pass

async def update_user_password(connection: AsyncConnection, user_id: str, old_password: str, new_password: str):
    query = sql.SQL(
        """
           UPDATE public.users
           SET 
           password_hash = %s
           WHERE id = %s;
        """)
    query_ = sql.SQL(
        """
        SELECT password_hash FROM public.users WHERE id = %s
        """
    )
    try:

        async with connection.cursor() as cursor:
            await cursor.execute(query_, (user_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            if data.__len__() == 0:
                raise HTTPException(status_code=400, detail="User doesnt exist")
            if verify_password(stored_hash=data[0].get("password_hash"), password=old_password):
                await cursor.execute(query, (
                    generate_hash_password(new_password),
                    user_id
                ))
                await connection.commit()
            else:
                raise HTTPException(status_code=400, detail="Invalid password")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error resolving review comment decision {e}")

def create_redis_client() -> Redis:
    """
    Create and return a Redis client.
    This is called once during the app startup.
    """
    return redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True,
        max_connections=10
    )

async def get_redis_connect():
    """
    Returns the global Redis client instance if initialized.
    """
    if not redis_client:
        raise RuntimeError("Redis client is not initialized!")
    return redis_client

def get_latest_reference_number(references_data):
    numbers = []

    for ref in references_data:
        ref_str = ref.get("reference", "")
        if "-" in ref_str:
            try:
                num = int(ref_str.split("-")[1])
                numbers.append(num)
            except ValueError:
                continue  # Skip invalid formats

    return max(numbers, default=0)