from pydantic import BaseModel, model_validator
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class IssueResponseTypes(str, Enum):
    SAVE = "Save"
    ACCEPT = "Accept"
    DECLINE = "Decline"
    SEND = "Send"
    REVISE = "Revise"

class User(BaseModel):
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    date_issued: Optional[datetime] = None

class IssueColumns(str, Enum):
    ID = "id"
    MODULE_ID = "module_id"
    TITLE = "title"
    STATUS = "status"
    ENGAGEMENT = "engagement"
    SUB_PROGRAM = "sub_program"
    REF = "ref"

class IssueResponseColumns(str, Enum):
    ID = "id"
    ISSUE = "issue"
    NOTES = "notes"
    ATTACHMENTS = "attachments"
    ISSUED_BY = "issued_by"
    TYPE  = "type"
    CREATED_AT = "created_at"


class IssueActors(str, Enum):
    IMPLEMENTER = "lod1_implementer"
    OWNER = "lod1_owner"
    RISK_MANAGER = "lod2_risk_manager"
    OBSERVERS = "observers"
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


class IssueResponseActors(str, Enum):
    OWNER = "lod1_owner"
    RISK_MANAGER = "lod2_risk_manager"
    COMPLIANCE_OFFICER = "lod2_compliance_officer"
    AUDIT_MANAGER = "lod3_audit_manager"


class IssueLOD2Feedback(str, Enum):
    CLOSED_VERIFIED_BY_RISK = "Closed -> verified by risk"
    CLOSED_RISK_NA = "Closed -> risk N/A"
    CLOSED_RISK_ACCEPTED = "Closed -> risk accepted"


class NewIssue(BaseModel):
    title: str
    criteria: Dict | str
    finding: Dict | str
    risk_rating: str
    source: str
    process: str
    sub_process: str
    root_cause: str
    sub_root_cause: str
    risk_category: str
    sub_risk_category: str
    impact_category: str
    impact_sub_category: str
    root_cause_description: Dict | str
    impact_description: Dict | str
    recommendation: Dict | str
    regulatory: bool
    estimated_implementation_date: datetime
    sdi_name: Optional[str] = None
    recurring_status: Optional[bool] = False
    management_action_plan: Optional[Dict] | Optional[str] = None
    lod1_implementer: List[User] = None
    lod1_owner: List[User] = None
    observers: Optional[List[User]] = None
    lod2_risk_manager: Optional[List[User]] = None
    lod2_compliance_officer: Optional[List[User]] = None
    lod3_audit_manager: List[User] = None


class CreateIssue(NewIssue):
    id: str
    module_id: str
    sub_program: str
    ref: str
    engagement: str
    created_at: datetime
    status: IssueStatus
    reportable: Optional[bool] = False


class SendIssueImplementor(BaseModel):
    issue_ids: List[str]


class NewDeclineResponse(BaseModel):
    actor: IssueResponseActors
    decline_notes: str


class IssueAcceptResponse(BaseModel):
    actor: IssueResponseActors
    accept_notes: Optional[str] = None
    accept_attachment: Optional[List[str]] = None
    lod2_feedback: Optional[IssueLOD2Feedback] = None

    @model_validator(mode="after")
    def validate_fields(self):
        valid_statuses = {
            IssueStatus.CLOSED_RISK_NA,
            IssueStatus.CLOSED_RISK_ACCEPTED,
            IssueStatus.CLOSED_VERIFIED_BY_RISK
        }
        if (self.actor == IssueActors.RISK_MANAGER or self.actor == IssueActors.COMPLIANCE_OFFICER) and self.lod2_feedback is None:
            raise ValueError("provide lod2 feedback please")
        if self.actor == IssueActors.RISK_MANAGER or self.actor == IssueActors.COMPLIANCE_OFFICER:
            if self.lod2_feedback not in valid_statuses:
                raise ValueError("Provide valid lod2 status")
        return self


class NewIssueResponse(BaseModel):
    notes: Optional[str] = None
    attachments: Optional[str] = None
    type: IssueResponseTypes
    issued_by: str

class CreateIssueResponses(NewIssueResponse):
    id: str
    issue: str
    created_at: datetime

class UpdateIssueStatus(BaseModel):
    status: IssueStatus

class UpdateIssueDetails(BaseModel):
    pass

class ReadIssues(BaseModel):
    id: str
    module_id: str
    sub_program: str
    ref: str
    engagement: str
    created_at: datetime
    status: IssueStatus
    reportable: Optional[bool] = False
    title: str
    criteria: Dict | str
    finding: Dict | str
    risk_rating: str
    source: str
    process: str
    sub_process: str
    root_cause: str
    sub_root_cause: str
    risk_category: str
    sub_risk_category: str
    impact_category: str
    impact_sub_category: str
    root_cause_description: Dict | str
    impact_description: Dict | str
    recommendation: Dict | str
    regulatory: bool
    estimated_implementation_date: datetime
    sdi_name: Optional[str] = None
    recurring_status: Optional[bool] = False
    management_action_plan: Optional[Dict] | Optional[str] = None


class MarkIssueReportable(BaseModel):
    reportable: bool


class ReviseIssue(BaseModel):
    date_revised: datetime
    revised_status: bool
    revised_count: int


class SetOpenDate(BaseModel):
    date_opened: bool


class SetClosedDate(BaseModel):
    date_opened: bool