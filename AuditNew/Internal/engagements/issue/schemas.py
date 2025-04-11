from pydantic import BaseModel
from enum import Enum
from typing import Optional, List, Dict
from datetime import datetime

class User(BaseModel):
    name: Optional[str]
    email: Optional[str]
    date_issued: Optional[datetime]

class IssueActors(str, Enum):
    IMPLEMENTER = "implementer"
    OWNER = "owner"
    RISK_MANAGER = "risk_manager"
    COMPLIANCE_OFFICER = "compliance_officer"
    AUDIT_MANAGER = "audit_manager"

class IssueResponseType(str, Enum):
    ACCEPT = "accept"
    DECLINE = "decline"

class IssueStatus(str, Enum):
    NOT_STARTED = "Not started"
    OPEN = "Open"
    IN_PROGRESS_IMPLEMENTER = "In progress -> implementer"
    IN_PROGRESS_OWNER = "In progress -> owner"
    CLOSED_NOT_VERIFIED = "Close unverified"
    CLOSED_VERIFIED = "Closed verified"


class Issue(BaseModel):
    id: Optional[int] = None
    title: Optional[str]
    criteria: Optional[str]
    finding: Optional[str]
    risk_rating: Optional[str]
    process: Optional[str]
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
    LOD1_implementer: Optional[List[User]]
    LOD1_owner: Optional[List[User]]
    LOD2_risk_manager: Optional[List[User]] = None
    LOD2_compliance_officer: Optional[List[User]] = None
    LOD3_audit_manager: Optional[List[User]]

class IssueStatusDecline(BaseModel):
    notes: Optional[str]

class IssueStatusAccept(BaseModel):
    notes: Optional[str] = None
    attachment: Optional[List[str]] = None
    reply: Optional[str] = None


class NewIssue(BaseModel):
    title: str

class IssueSendImplementation(BaseModel):
    id: List[int]

class IssueResponse(BaseModel):
    actor: IssueActors
    type: IssueResponseType
    accept_notes: Optional[str] = None
    accept_attachment: Optional[List[str]] = None
    decline_notes: Optional[str]

class MailedIssue(BaseModel):
    title: Optional[str]
    criteria: Optional[str]
    finding: Optional[str]
    risk_rating: Optional[str]
    implementors: List[str]
