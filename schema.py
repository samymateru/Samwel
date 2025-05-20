from pydantic import BaseModel
from typing import Optional, List, Dict
from enum import Enum

class Endpoints(BaseModel):
    pass

class CurrentUser(BaseModel):
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    user_name: Optional[str] = None
    company_id: Optional[str] = None
    company_name: Optional[str] = None
    modules: Optional[List[Dict]] = None
    role_id: Optional[str] = None
    type: Optional[str] = None
    status_code: Optional[int] = None
    description: Optional[str] = None

class UserData(BaseModel):
    id: Optional[str]
    name: Optional[str]
    email: Optional[str]
    telephone: Optional[str]
    user_role: List[Dict]
    company_roles: List[Dict]
    type: Optional[str]
    module: List[Dict]
    status: Optional[bool]

class TokenError(BaseModel):
    status_code: int
    description: str

class ErrorResponse(BaseModel):
       message: str
       status_code: int

class ResponseMessage(BaseModel):
    detail: str