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
    title: str
    type: Type
    status: bool
    task: Optional[List[Task]] = None
    created_at: datetime = datetime.now()

class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    telephone: str
    password: Optional[str] = Field(default="1234")
    module_id: List[str]
    created_at: datetime = datetime.now()


