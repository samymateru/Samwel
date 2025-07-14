from pydantic import BaseModel, Field
from typing import List, Optional, Dict
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

class NewModule(BaseModel):
    name: ModuleName



