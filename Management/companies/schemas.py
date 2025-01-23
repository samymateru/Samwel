from pydantic_core import Url
from pydantic import BaseModel, EmailStr, HttpUrl
from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic_core import Url


class UserType(str, Enum):
    ADMINISTRATOR = "administrator",
    USER = "user"


class Company(BaseModel):
    name: str
    owner: str
    email: str
    telephone: str
    website: str
    description: str
    status: bool
    created_at: datetime


class NewCompany(BaseModel):
    name: str
    owner: str
    email: EmailStr
    telephone: str
    website:  str
    description: Optional[str] = None
    status: Optional[bool] = True
    type: UserType = UserType.ADMINISTRATOR
    password: str

class UpdateCompany(BaseModel):
    company_id: int
    name: Optional[str] = None
    owner: Optional[str] = None
    description: Optional[str] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    website: Optional[str] = None


