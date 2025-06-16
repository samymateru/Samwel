from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from datetime import datetime


class NewReportingProcedure(BaseModel):
    title: str

class ProgramSummary(BaseModel):
    id: Optional[str] = None
    name: str
    status: Optional[str]
    process_rating: Optional[str]
    issue_count: int
    acceptable: int
    improvement_required: int
    significant_improvement_required: int
    unacceptable: int
    recurring_issues: int


class User(BaseModel):
    name: Optional[str]
    email: Optional[str]
    date_issued: Optional[datetime]

class IssueActors(str, Enum):
    IMPLEMENTER = "lod1_implementer"
    OWNER = "lod1_owner"
    RISK_MANAGER = "lod2_risk_manager"
    COMPLIANCE_OFFICER = "lod2_compliance_officer"
    AUDIT_MANAGER = "lod3_audit_manager"

class IssueStatus(str, Enum):
    NOT_STARTED = "Not started"
    OPEN = "Open"
    IN_PROGRESS_IMPLEMENTER = "In progress -> implementer"
    IN_PROGRESS_OWNER = "In progress -> owner"
    CLOSED_NOT_VERIFIED = "Closed -> not verified"
    CLOSED_VERIFIED_BY_RISK = "Closed -> verified by risk"
    CLOSED_RISK_NA = "Closed -> risk N/A"
    CLOSED_RISK_ACCEPTED = "Closed -> risk accepted"
    CLOSED_VERIFIED_BY_AUDIT = "Closed -> verified by audit"

class ResponseActors(str, Enum):
    OWNER = "lod1_owner"
    RISK_MANAGER = "lod2_risk_manager"
    COMPLIANCE_OFFICER = "lod2_compliance_officer"
    AUDIT_MANAGER = "lod3_audit_manager"

class LOD2Feedback(str, Enum):
    CLOSED_VERIFIED_BY_RISK = "Closed -> verified by risk"
    CLOSED_RISK_NA = "Closed -> risk N/A"
    CLOSED_RISK_ACCEPTED = "Closed -> risk accepted"


class SummaryFinding(BaseModel):
    id: Optional[str] = None
    title: Optional[str]
    ref: Optional[str] = None
    criteria: Optional[str]
    finding: Optional[str]
    risk_rating: Optional[str]
    process: Optional[str]
    source: Optional[str]
    sdi_name: Optional[str] = None
    sub_process: Optional[str]
    root_cause_description: Optional[str]
    root_cause: Optional[str]
    sub_root_cause: Optional[str]
    risk_category: Optional[str]
    sub_risk_category: Optional[str]
    impact_description: Optional[str]
    impact_category: Optional[str]
    impact_sub_category: Optional[str]
    recurring_status: Optional[bool]
    recommendation: Optional[str]
    management_action_plan: Optional[str]
    regulatory: Optional[bool]
    estimated_implementation_date: Optional[datetime]
    prepared_by: Optional[User] = None
    reviewed_by: Optional[User] = None
    status: Optional[IssueStatus] | None = IssueStatus.NOT_STARTED
    reportable: Optional[bool] = None
    lod1_implementer: List[User]
    lod1_owner: List[User]
    observers: Optional[List[User]] = None
    lod2_risk_manager: Optional[List[User]]
    lod2_compliance_officer: Optional[List[User]] = None
    lod3_audit_manager: List[User]
    date_opened: Optional[datetime] = None
    date_closed: Optional[datetime] = None
    date_revised: Optional[datetime] = None
    revised_status: Optional[bool] = False
    revised_count: Optional[int] = 0