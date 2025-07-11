from pydantic import BaseModel
from typing import Optional, List, Dict
from enum import Enum

from Management.roles.schemas import Roles


class Endpoints(BaseModel):
    pass

class CurrentUser(BaseModel):
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    entity_id: Optional[str] = None
    organization_id: Optional[str] = None
    module_id: Optional[str] = None
    module_name: Optional[str] = None
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