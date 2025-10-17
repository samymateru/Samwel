import os
import secrets
import string
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import bcrypt
from starlette import status

from models.engagement_staff_models import fetch_engagement_staff_data_model
from models.role_models import get_role_data_model
from schema import CurrentUser
from schemas.role_schemas import RolesSections, Permissions
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


password_hasher = PasswordHasher(
    time_cost=2,        # Number of iterations
    memory_cost=102400, # RAM usage in KiB (e.g., 100MB)
    parallelism=8,      # Threads
    hash_len=32,        # Length of the hash
    salt_len=16         # Salt length
)


def hash_password(password: str) -> str:
    """
    Hashes a plain-text password using Argon2.
    """
    return password_hasher.hash(password)


def generate_hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt).decode()
    return hashed


def generate_password(length: int = 6) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def verify_password(hashed_password: str, plain_password: str) -> bool:
    """
    Verifies a plain-text password against its hashed version.
    Returns True if matched, False otherwise.
    """
    try:
        return password_hasher.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency function to extract and validate the current user from a JWT token.

    This function is used in FastAPI routes to authorize users based on a JWT token
    provided in the Authorization header (using the OAuth2 Bearer token scheme).

    It decodes the token using the secret key and returns a CurrentUser object if
    the token is valid. If the token is missing, expired, invalid, or if the
    secret key is not configured, it raises appropriate HTTP exceptions.

    Args:
        token (str): The JWT token provided via FastAPI's OAuth2PasswordBearer dependency.

    Returns:
        CurrentUser: An instance containing the decoded token data.

    Raises:
        HTTPException: If the token is missing, expired, or invalid.
        RuntimeError: If the SECRET_KEY is not set in environment variables.
    """
    if not token:
        raise HTTPException(status_code=401, detail="auth token not provided")
    try:
        secret_key = os.getenv("SECRET_KEY")
        if not secret_key:
            raise RuntimeError("SECRET_KEY not set in environment")
        decoded_token = jwt.decode(token, key=secret_key, algorithms=["HS256"])
        return CurrentUser(**decoded_token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="auth token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="auth token is invalid")



def check_permission(section: RolesSections, permission: Permissions):
    """
    Dependency factory that checks if the current user's role has
    the required permission in the specified section.

    This function returns an async dependency used with FastAPI's `Depends()`.
    When included in a route, it verifies whether the logged-in user has
    the given permission within the given section.

    Args:
        section (RolesSections): The section to check (e.g., RolesSections.REPORTING).
        permission (Permissions): The required permission (e.g., Permissions.APPROVE).

    Raises:
        HTTPException (403): If the user does not have the specified permission.
    """
    async def dependency(auth: CurrentUser = Depends(get_current_user)):
        pool = await AsyncDBPoolSingleton.get_instance().get_pool()
        with exception_response():
            async with pool.connection() as connection:
                role_data = await get_role_data_model(
                    connection=connection,
                    role_id=auth.role_id,
                )

                section_permissions = role_data.get(section.value)

                has_access = permission.value in section_permissions

                if not has_access:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Missing {permission.value} permission in {section.value}.",
                    )
                return auth

    return dependency


def check_engagement_permission(section: RolesSections, permission: Permissions, engagement_id: str):
    """
        Dependency factory that checks if the current user's role has
        the required permission in the specified Engagement.

        This function returns an async dependency used with FastAPI's `Depends()`.
        When included in a route, it verifies whether the logged-in user has
        the given permission within the given section.

        Args:
            :param permission: (Permissions): The required permission (e.g., Permissions.APPROVE)
            :param section: (RolesSections) : The role section (e.g., RolesSections.PLANNING
            :param engagement_id:

        Raises:
            HTTPException (403): If the user does not have the specified permission.

        """
    async def dependency(auth: CurrentUser = Depends(get_current_user)):
        pool = await AsyncDBPoolSingleton.get_instance().get_pool()
        with exception_response():
            async with pool.connection() as connection:
                staff_data = await fetch_engagement_staff_data_model(
                    connection=connection,
                    engagement_id=engagement_id,
                    user_id=auth.user_id
                )

                if staff_data is None:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"During Staff Check We Cant Get Your Data Please Contact The Audit Leads",
                    )

                role_data = staff_data.get("role")

                if role_data is None:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Missing {permission.value} permission in {section.value}.",
                    )


                section_permissions = role_data.get(section.value)

                has_access = permission.value in section_permissions

                if not has_access:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Missing {permission.value} permission in {section.value}.",
                    )

                return auth

    return dependency



