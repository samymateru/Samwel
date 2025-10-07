from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
from pydantic import BaseModel, model_validator, PrivateAttr


class ModuleDataReference(str, Enum):
    PROCEDURE_REFERENCE = "procedure_reference"
    INTERNAL_ISSUES = "internal_issues"
    EXTERNAL_ISSUES = "external_issues"
    PLAN_REFERENCE = "plan_reference"

class ModulesColumns(str, Enum):
    ID = "id"
    ORGANIZATION = "organization"
    NAME = "name"
    PURCHASE_DATE = "purchase_date"
    STATUS = "status"
    PROCEDURE_REFERENCE = "procedure_reference"
    INTERNAL_ISSUES = "internal_issues"
    EXTERNAL_ISSUES = "external_issues"
    PLAN_REFERENCE = "plan_reference"
    CREATED_AT = "created_at"


class ModuleName(str, Enum):
    E_AUDIT_NEXT = "eAuditNext"
    E_RISK = "eRisk"
    E_GOVERNANCE = "eGovernance"
    E_COMPLIANCE = "eCompliance"
    E_FRAUD = "eFraud"


class ModuleStatus(str, Enum):
    PENDING = "Pending"
    ACTIVE = "Active"
    CLOSED = "Closed"


class ActivationColumns(str, Enum):
    ACTIVATION_TOKEN = "activation_token"
    MODULE_ID = "module_id"
    CREATED_AT = "created_at"


class AuditLicenceColumns(str, Enum):
    LICENCE_ID = "licence_id"
    MODULE_ID = "module_id"
    PLAN_ID = "plan_id"
    NAME = "name"
    AUDIT_STAFF = "audit_staff"
    BUSINESS_STAFF = "business_staff"
    ENGAGEMENTS_COUNT = "engagements_count"
    ISSUES_COUNT = "issues_count"
    EMAILS_COUNT = "emails_count"
    PRICE = "price"
    FOLLOW_UP = "follow_up"


class NewModule(BaseModel):
    licence_id: str
    name: ModuleName


class CreateModule(BaseModel):
    id: str
    organization: str
    name: str
    status: ModuleStatus
    purchase_date: Optional[datetime] = None
    created_at: datetime


class CreateModuleActivation(BaseModel):
    activation_token: str
    module_id: str
    created_at: datetime


class CreateAuditLicence(BaseModel):
    licence_id: str
    plan_id: str
    module_id: str
    name: str
    audit_staff: int
    business_staff: int
    engagements_count: int
    issues_count: int
    emails_count: int
    price: int
    follow_up: bool


class EAuditLicence(BaseModel):
    licence_id: str
    name: str
    audit_staff: int
    business_staff: int
    engagements_count: int
    issues_count: int
    emails_count: int
    follow_up: bool
    price: int


class ActivateModule(BaseModel):
    status: ModuleStatus
    purchase_date: datetime

class BaseModule(CreateModule):
    pass



class ReadModule(BaseModel):
    id: str
    organization: str
    name: str
    status: str  # or ModuleStatus
    purchase_date: Optional[datetime] = None
    created_at: datetime
    expired_at: Optional[datetime] = None
    licence_name: Optional[str] = None
    licence_id: Optional[str] = None

    # private attribute (not a field)
    __licence_licence_id: Optional[str] = PrivateAttr(default=None)

    @model_validator(mode="before")
    def move_licence_id(cls, values: dict):
        # if licence_licence_id exists, move it to licence_id
        if "licence_licence_id" in values and not values.get("licence_id"):
            values["licence_id"] = values.pop("licence_licence_id")
        return values

    @model_validator(mode="after")
    def compute_expiration(self):
        if self.purchase_date and not self.expired_at:
            self.expired_at = self.purchase_date + timedelta(days=365)
        return self

    class Config:
        extra = "ignore"


class IncrementInternalIssues(BaseModel):
    internal_issues: int


class IncrementExternalIssues(BaseModel):
    external_issues: int


class IncrementPlanReferences(BaseModel):
    plan_reference: int


class IncrementProcedureReferences(BaseModel):
    procedure_reference: int


class DeleteModuleTemporarily(BaseModel):
    status: ModuleStatus


class ReadLicence(BaseModel):
    name: str
    licence_id: str