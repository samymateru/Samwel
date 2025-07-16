from pydantic import BaseModel
from typing import Optional, List, Dict
from enum import Enum

from Management.organization.schemas import Organization
from Management.roles.schemas import Roles


class Endpoints(BaseModel):
    pass

class CurrentUser(BaseModel):
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    entity_id: Optional[str] = None
    module_id: Optional[str] = None
    role: Optional[str] = None
    title: Optional[str] = None
    type: Optional[str] = None
    status_code: Optional[int] = None
    description: Optional[str] = None

class UserData(BaseModel):
    id: Optional[str]
    name: Optional[str]
    email: Optional[str]
    telephone: Optional[str]
    type: Optional[str]
    status: Optional[str] = None
    role: Optional[Roles] = None
    title: Optional[str] = None

class TokenError(BaseModel):
    status_code: int
    description: str

class ErrorResponse(BaseModel):
       message: str
       status_code: int

class ResponseMessage(BaseModel):
    detail: str

class TokenResponse(BaseModel):
    token: Optional[str]

class EmailSchema(BaseModel):
    to: str
    subject: str
    body: str

class LoginResponse(BaseModel):
    token: str
    token_type: str = "Bearer"
    user_id: str
    entity_id: str
    name: str
    email: str
    telephone: str = None
    administrator: bool
    owner: bool
    organizations: List[Organization]

class RoleActions(str, Enum):
    VIEW = "view"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    APPROVE = "approve"
