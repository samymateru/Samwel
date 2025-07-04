from pydantic import BaseModel
from typing import List, Optional
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
    id: Optional[str] = None
    name: ModuleName
    purchase_date: Optional[datetime] = datetime.now()
    status: Optional[ModuleStatus] = ModuleStatus.ACTIVE

