from pydantic import BaseModel
from typing import Optional, List, Dict
from enum import Enum

class Endpoints(BaseModel):
    pass

class CurrentUser(BaseModel):
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    user_name: Optional[str] = None
    entity_id: Optional[str] = None
    entity_name: Optional[str] = None
    status_code: Optional[int] = None

class UserData(BaseModel):
    id: Optional[str]
    name: Optional[str]
    email: Optional[str]
    telephone: Optional[str]
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