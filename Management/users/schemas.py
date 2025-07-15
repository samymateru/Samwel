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
    engagements: Optional[List[str]] = None
    created_at: datetime = datetime.now()

class User(BaseModel):
    id: str
    entity_id: str
    name: str
    email: str
    telephone: str
    password: str
    administrator: bool = Field(default=False)
    owner: bool = Field(default=False)
    role: Optional[str] = None
    title: str = None
    module: Optional[str] = None
    type: Optional[str] = None
    created_at: datetime = datetime.now()

class EntityUser(BaseModel):
    id: str
    entity: str
    name: str
    email: str
    telephone: str
    administrator: bool = Field(default=False)
    owner: bool = Field(default=False)
    created_at: datetime = datetime.now()


class ModuleSection(BaseModel):
    id: str
    role: str
    title: str
    type: Optional[str] = None

class OrganizationUser(BaseModel):
    id: str
    entity: str
    organization: str
    name: str
    email: str
    telephone: str
    administrator: bool = Field(default=False)
    owner: bool = Field(default=False)
    modules: List[ModuleSection]
    created_at: datetime = datetime.now()

class ModuleUser(BaseModel):
    id: str
    entity: str
    module: str
    name: str
    email: str
    telephone: str
    title: str
    role: str
    type: Optional[str] = None
    created_at: datetime = datetime.now()


class NewUser(BaseModel):
    name: str = Field(default="")
    telephone: str =  Field(default="")
    email: str
    title: str
    role: str
    type: str
    module_id: str

class OrganizationsUsers(BaseModel):
    organization_id: str
    user_id: str
    administrator: bool
    owner: bool
    created_at: datetime = Field(default=datetime.now())

class ModulesUsers(BaseModel):
    module_id: str
    user_id: str
    title: str
    role: str
    type: str
    created_at: datetime = Field(default=datetime.now())


