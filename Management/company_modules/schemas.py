from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class User(BaseModel):
    email: str
    name: str

class ModuleStatus(str, Enum):
    ACTIVE = "Active"
    CLOSED = "Closed"

class ModuleName(str, Enum):
    E_AUDIT_NEXT = "eAuditNext"
    E_RISK = "eRisk"
    E_GOVERNANCE = "eGovernance"
    E_COMPLIANCE = "eCompliance"
    E_FRAUD = "eFraud"

class Role(BaseModel):
    name: str
    user: User

class Module(BaseModel):
    id: str
    name: ModuleName
    purchase_date: Optional[datetime] = Field(default=datetime.now())
    status: Optional[ModuleStatus] = Field(default=ModuleStatus.ACTIVE)
    role: Optional[str] = None
    title: Optional[str] = None
    type: Optional[str] = None


class ReadModule(BaseModel):
    id: str
    licence_id: Optional[str] = None
    licence_name: Optional[str] = None
    audit_staff: Optional[int] = None
    business_staff: Optional[int] = None
    engagements_count: Optional[int] = None
    issues_count: Optional[int] = None
    emails_count: Optional[int] = None
    follow_up: Optional[bool] = None
    name: ModuleName
    purchase_date: Optional[datetime] = Field(default=datetime.now())
    status: Optional[ModuleStatus] = Field(default=ModuleStatus.ACTIVE)
    role: Optional[str] = None
    title: Optional[str] = None
    type: Optional[str] = None

class OrganizationModule(BaseModel):
    id: str
    name: ModuleName
    purchase_date: Optional[datetime] = Field(default=datetime.now())
    status: Optional[ModuleStatus] = Field(default=ModuleStatus.ACTIVE)

class NewModule(BaseModel):
    name: ModuleName
    licence_id: str


#---------------------------------------------------------

#---------------------------------------------------------------------------------------




