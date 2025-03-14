from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum

class UserType(str, Enum):
    ADMINISTRATOR = "administrator",
    USER = "user"

class ResourceTypes(str, Enum):
    RISK_RATING = "risk_rating"
    BUSINESS_PROCESS = "business_process"
    RISK_CATEGORY = "risk_category"
    ROOT_CAUSE_CATEGORY = "root_cause_category"
    CONTROL_TYPE = "control_type"
    IMPACT_CATEGORY_RATING = "impact_category_rating"
    CONTROL_EFFECTIVE_RATING = "control_effective_rating"
    CONTROL_WEAKNESS_RATING = "control_weakness_rating"
    AUDIT_OPINION_RATING = "audit_opinion_rating"
    RISK_MATURITY_RATING = "risk_maturity_rating"
    ISSUE_IMPLEMENTATION_STATUS = "issue_implementation_status"
    EXTENDED_TESTING = "extended_testing"
    ISSUE_SOURCE = "issue_source"

class SubResourceTypes(str, Enum):
    SUB_RISK_CATEGORY = "sub_risk_category"
    SUB_ROOT_CAUSE_CATEGORY = "sub_root_cause_category"
    SUB_IMPACT_CATEGORY_RATING = "sub_impact_category_rating"
    BUSINESS_SUB_PROCESS = "business_sub_process",

class Module(BaseModel):
    id: int
    name: str

class Company(BaseModel):
    id: Optional[int]
    name: str
    owner: str
    email: str
    telephone: str
    website: Optional[str] = None
    entity_type: str
    status: str
    created_at: datetime

class NewCompany(BaseModel):
    name: str
    owner: str
    email: EmailStr
    telephone: str
    website:  Optional[str]
    password: str
    entity_type: str
    status: Optional[str] = "setup"

class Resource(BaseModel):
    resource: ResourceTypes
    name: str

class SubResource(BaseModel):
    sub_resource: SubResourceTypes
    name: str

#########################################################3
class BusinessProcess(BaseModel):
    code: str
    name: str

class BusinessSubProcess(BaseModel):
    name: str