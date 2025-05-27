from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class Role(BaseModel):
    name: str

class Assignee(BaseModel):
    name: str
    email: str

class Task(BaseModel):
    assigned_by: Assignee
    href: str
    date_assigned: datetime

class Type(BaseModel):
    name: str
    modules: List[str]

class __User__(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    telephone: str
    created_at: datetime = datetime.now()

class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    telephone: str
    password: Optional[str] = Field(default="123456")
    module_id: List[str]
    created_at: datetime = datetime.now()


