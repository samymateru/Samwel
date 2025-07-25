import shutil
import tempfile
from typing import Optional, Union
from contextlib import asynccontextmanager
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, BackgroundTasks, UploadFile
from psycopg_pool import AsyncConnectionPool
import uuid
from Management.roles.schemas import Roles, Permissions, RolesSections
from commons import get_role, get_engagement_role
from constants import administrator, head_of_audit, member, audit_lead, audit_reviewer, audit_member, business_manager, \
    risk_manager, compliance_manager
from s3 import upload_file
from schema import CurrentUser, RoleActions
import secrets
import string
from psycopg import sql, AsyncCursor
from psycopg.errors import UniqueViolation, UndefinedColumn, UndefinedFunction
from typing import List
import redis.asyncio as redis
from redis.asyncio import Redis
from psycopg import AsyncConnection
from psycopg.rows import dict_row
from psycopg.sql import SQL, Identifier, Placeholder, Composed


roles_map = {
    "Administrator": administrator,
    "Head of Audit": head_of_audit,
    "Member": member,
    "Audit Lead": audit_lead,
    "Audit Reviewer": audit_reviewer,
    "Audit Member": audit_member,
    "Business Manager": business_manager,
    "Risk Manager": risk_manager,
    "Compliance Manager": compliance_manager
}

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
        decoded_token = jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms=["HS256"])
        decoded_token["status_code"] = 200
        decoded_token["description"] = "success"
        return CurrentUser(**decoded_token)
    except jwt.ExpiredSignatureError:
        return CurrentUser(status_code=401, description="token expired")
    except jwt.InvalidTokenError:
        return CurrentUser(status_code=401, description="invalid token")

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

async def get_role_from_token(token: str = Depends(oauth2_scheme)):
    if not token:
        return CurrentUser(status_code=401, description="auth token not provided")
    try:
        user_dict = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        user = CurrentUser(**user_dict)
        async for connection in get_async_db_connection():
            if user.module_id is not None and user.role is not None:
                role_data = await get_role(connection=connection, name=user.role, module_id=user.module_id)
                roles: List[Roles] = [Roles(**role_dict) for role_dict in role_data]
                if roles.__len__() != 0:
                    return roles[0]
                else:
                    return roles_map.get(user.role)
            else:
                raise HTTPException(status_code=400, detail="Invalid token make sure to re-authorize")

    except jwt.ExpiredSignatureError:
        return CurrentUser(status_code=401, description="token expired")
    except jwt.InvalidTokenError:
        return CurrentUser(status_code=401, description="invalid token")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in authorization check {e}")

async def get_role_from_engagement(engagement_id: str, user: CurrentUser):
    try:
        async for connection in get_async_db_connection():
            if user.module_id is not None and user.role is not None:
                engagement_role = await get_engagement_role(connection=connection, engagement_id=engagement_id, user_email=user.user_email)
                if engagement_role.__len__() == 0:
                    raise HTTPException(status_code=400, detail="Oops sorry role unavailable on the engagement")
                role_data = await get_role(connection=connection, name=engagement_role[0], module_id=user.module_id)
                roles: List[Roles] = [Roles(**role_dict) for role_dict in role_data]
                if roles.__len__() != 0:
                    return roles[0]
                else:
                    return roles_map.get(user.role)
            else:
                raise HTTPException(status_code=400, detail="Invalid token make sure to re-authorize")

    except jwt.ExpiredSignatureError:
        return CurrentUser(status_code=401, description="token expired")
    except jwt.InvalidTokenError:
        return CurrentUser(status_code=401, description="invalid token")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in authorization check {e}")

def check_permission(section: RolesSections, action: Permissions):
    def inner(role: Roles = Depends(get_role_from_token)):
        if role == None:
            raise HTTPException(
                status_code=403,
                detail=f"System cant retrieve role information"
            )
        if not has_permission([role], section=section.value, action=action.value):
            raise HTTPException(
                status_code=403,
                detail=f"Access denied to {action.value.upper().title()} {section.value.upper().replace('_', ' ').title()}"
            )
        return True
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

async def check_row_exists(
    connection: AsyncConnection,
    table_name: str,
    filters: dict
) -> bool:
    """
    Check if a row exists in the given table using column-value filters.

    Args:
        conn (AsyncConnection): psycopg async connection
        table_name (str): table name (must be validated)
        filters (dict): column-value conditions

    Returns:
        bool: True if row exists, False otherwise
        :param filters:
        :param table_name:
        :param connection:
    """
    if not filters:
        raise ValueError("filters cannot be empty")

    # Build WHERE clause safely
    conditions: list[Composed] = []
    values = {}

    for i, (col, val) in enumerate(filters.items()):
        ph = f"val{i}"
        conditions.append(SQL("{} = {}").format(Identifier(col), Placeholder(ph)))
        values[ph] = val

    where_clause = SQL(" AND ").join(conditions)

    query = SQL("SELECT 1 FROM {} WHERE ").format(Identifier(table_name)) + where_clause + SQL(" LIMIT 1")

    async with connection.cursor(row_factory=dict_row) as cur:
        await cur.execute(query, values)
        row = await cur.fetchone()

    return row is not None

def upload_attachment(
        background_tasks: BackgroundTasks,
        user: CurrentUser,
        attachment: UploadFile
):
    try:
        key: str = f"{user.entity_name}/{uuid.uuid4()}-{attachment.filename}"
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            shutil.copyfileobj(attachment.file, tmp)
            temp_path = tmp.name

        background_tasks.add_task(upload_file, temp_path, key)
    except Exception as e:
        print(e)

def has_permission(roles: List[Roles], section: str, action: str) -> bool:

    """
    Checks if any of the given roles has the specified permission for a section.

    Args:
        roles (List[Roles]): List of role instances.
        section (str): Section name (e.g., "planning").
        action (str): Permission to check (e.g., "view").

    Returns:
        bool: True if any role grants the permission, else False.
    """
    for role in roles:
        try:
            section_permissions: Union[List[str], None] = getattr(role, section)
        except AttributeError:
            continue  # Skip if section doesn't exist in this role

        if isinstance(section_permissions, list) and action in section_permissions:
            return True
    return False

async def generate_user_token(connection: AsyncConnection, module_id: str, user_id: str):
    query_module_data = sql.SQL(
        """
        SELECT 
        usr.id,
        usr.name,
        usr.email,
        usr.entity,
        mod.organization,
        mod_usr.module_id,
        mod.name as module_name,
        mod_usr.title,
        mod_usr.role,
        mod_usr.type
        FROM modules_users mod_usr
        JOIN users usr ON usr.id = mod_usr.user_id
        JOIN modules mod ON mod.id = mod_usr.module_id
        WHERE mod_usr.module_id = %s  AND mod_usr.user_id = %s
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query_module_data, (module_id, user_id))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            current_user = CurrentUser(
                user_id=data[0].get("id"),
                user_name=data[0].get("name"),
                user_email=data[0].get("email"),
                entity_id=data[0].get("entity"),
                organization_id=data[0].get("organization"),
                module_id=data[0].get("module_id"),
                module_name=data[0].get("module_name"),
                role=data[0].get("role"),
                title=data[0].get("title"),
                type=data[0].get("type"),
            )
            return current_user
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error generating token {e}")

def validate_start_end_dates(start: Optional[datetime], end: Optional[datetime]) -> None:
    now = datetime.now(timezone.utc)

    if start is not None:
        if start < now:
            raise HTTPException(status_code=400, detail="Start date must be in the future.")

    if start is not None and end is not None:
        if end <= start:
            raise HTTPException(status_code=400, detail="End date must be after start time.")


async def check_row_count(cursor: AsyncCursor, detail: str):
    if cursor.rowcount == 0:
        raise HTTPException(status_code=400, detail=detail)

async  def check_if_organization_admin_owner(user_id: str, organization: str):
    query = sql.SQL(
        """
        SELECT id, administrator, owner FROM public.users WHERE id = %s;
        """)
    pass

async def check_if_entity_administrator(connection: AsyncConnection, user_id: id):
    query = sql.SQL(
        """
        SELECT id, administrator, owner FROM public.users WHERE id = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (user_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            user_data = [dict(zip(column_names, row_)) for row_ in rows]
            if user_data[0].get("administrator", False):
                return True
            else:
                raise HTTPException(status_code=403, detail="Access denied your not entity admin")
    except HTTPException as e:
        await connection.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)
