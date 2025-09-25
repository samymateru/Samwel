from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from datetime import datetime


class UserColumns(str, Enum):
    ID = "id"
    ENTITY = "entity"
    NAME = "name"
    EMAIL = "email"
    TELEPHONE = "telephone"
    ADMINISTRATOR = "administrator"
    OWNER = "owner"
    IMAGE = "image"
    CREATE_AT = "created_at"


class OrganizationUserColumns(str, Enum):
    ORGANIZATION_USER_ID = "organization_user_id"
    ORGANIZATION_ID = "organization_id"
    USER_ID = "user_id"
    ADMINISTRATOR = "email"
    OWNER = "owner"
    CREATE_AT = "created_at"

class ModuleUserColumns(str, Enum):
    MODULE_USER_ID = "module_user_id"
    MODULE_ID = "module_id"
    USER_ID = "user_id"
    ROLE = "role"
    TITLE = "title"
    TYPE ="type"
    CREATE_AT = "created_at"

class UserStatus(str, Enum):
    NEW = "New"
    ACTIVE = "Active"
    IN_ACTIVE = "In Active"

class UserTypes(str, Enum):
    MANAGEMENT = "Management"
    AUDIT = "Audit"
    BUSINESS = "Business"

class NewUser(BaseModel):
    name: Optional[str]
    email: str
    type: UserTypes
    category: Optional[str] = None
    telephone: Optional[str] = None
    role: Optional[str] = None
    title: Optional[str] = None

class CreateUser(BaseModel):
    id: str
    entity: str
    name: Optional[str] = None
    email: str
    telephone: Optional[str] = None
    status: UserStatus
    password_hash: str
    administrator: bool
    owner: bool
    image: str
    created_at: datetime

class CreateOrganizationUser(BaseModel):
    organization_user_id: str
    organization_id: str
    user_id: str
    category: str
    administrator: bool
    owner: bool
    created_at: datetime

class CreateModuleUser(BaseModel):
    module_user_id: str
    module_id: str
    user_id: str
    title: str
    role: str
    type: str
    created_at: datetime

class BaseUser(BaseModel):
    id: str
    entity: str
    name: Optional[str] = None
    email: str
    telephone: Optional[str] = None
    status: UserStatus
    administrator: bool
    owner: bool
    image: str
    created_at: datetime

class ReadModuleUsers(BaseUser):
    type: str
    role: str
    title: Optional[str] = None

class UserModuleSection(BaseModel):
    id: str
    title: str
    role: str
    type: str
    name: str


class ReadOrganizationUser(BaseUser):
    modules: List[UserModuleSection]

class UpdateModuleUser(BaseModel):
    title: str
    role: str
    type: str


class UpdateEntityUser(BaseModel):
    name: str
    telephone: Optional[str]


