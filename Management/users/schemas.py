from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class Role(BaseModel):
    name: str

class Module(BaseModel):
    name: str

class Assignee(BaseModel):
    name: str
    email: str

class Task(BaseModel):
    assigned_by: Assignee
    href: str
    date_assigned: datetime

class __User__(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    telephone: str
    title: str
    status: bool
    role: List[Role]
    module: List[Module]
    task: Optional[List[Task]] = None
    created_at: datetime = datetime.now()

class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    telephone: str
    password: Optional[str] = Field(default="1234")
    title: str
    status: bool
    role: List[Role]
    module: List[Module]
    task: Optional[List[Task]] = None
    created_at: datetime = datetime.now()


