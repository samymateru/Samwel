from pydantic_core import Url
from pydantic import BaseModel, EmailStr, HttpUrl
from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic_core import Url


class UserType(str, Enum):
    ADMINISTRATOR = "administrator",
    USER = "user"

class ResourceTypes(str, Enum):
    RISK_RATING = "risk_rating",
    BUSINESS_PROCESS = "business_process"
    SUB_PROCESS = "sub_process",
    RISK_TYPE = "risk_type",
    ROOT_CAUSE_CATEGORY = "root_cause_category",
    CONTROL_TYPE = "control_type",
    IMPACT_CATEGORY_RATING = "impact_category_rating"
    CONTROL_EFFECTIVE_RATING = "control_effective_rating",
    CONTROL_WEAKNESS_RATING = "control_weakness_rating",
    AUDIT_OPINION_RATING = "audit_opinion_rating",
    RISK_MATURITY_RATING = "risk_maturity_rating",
    ISSUE_IMPLEMENTATION_STATUS = "issue_implementation_status",
    EXTENDED_TESTING = "extended_testing",
    ISSUE_SOURCE = "issue_source",


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
    password: str
    entity_type: str
    module_id: List[int]
    status: Optional[str] = "setup"
    type: UserType = UserType.ADMINISTRATOR

class UpdateCompany(BaseModel):
    company_id: int
    name: Optional[str] = None
    owner: Optional[str] = None
    description: Optional[str] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    website: Optional[str] = None

class Resource(BaseModel):
    resource: ResourceTypes
    name: str

