from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class Role(BaseModel):
    id: Optional[str] = None
    name: str

class Module(BaseModel):
    id: str
    name: str

class UserA(BaseModel):
    id: str
    name: str
    email: str

class Task(BaseModel):
    assigned_by: UserA
    date_assigned: datetime

class User(BaseModel):
    id: str
    name: str
    telephone: str
    type: str
    email: str
    status: bool
    role: List[Role]
    module: List[Module]
    task: Optional[Task] = None
    created_at: datetime

class NewUser(BaseModel):
    name: str
    email: str
    module: List[Module]
    role: List[Role]
    telephone: Optional[str] = Field(default="12345678")
    type: Optional[str] = Field(default="user")
    password: Optional[str] = Field(default="1234")
    status: Optional[bool] = False

class UpdateUser(BaseModel):
    name: Optional[str]
    telephone: Optional[str] = None
    type: Optional[str] = None
    email: Optional[ str] = None
    password: Optional[str] = None
    status: Optional[bool] = None


