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

class UserType(BaseModel):
    id: str
    type: str
    role: str
    title: str
    engagements: List[str]

class __User__(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    telephone: str
    role: Optional[str] = None
    type: Optional[str] = None
    title: Optional[str]= None
    created_at: datetime = datetime.now()

class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    telephone: str
    password: Optional[str] = Field(default="123456")
    role: Optional[str] = None
    title: str = None
    module: Optional[str] = None
    type: Optional[str] = None
    created_at: datetime = datetime.now()


