from pydantic import BaseModel, model_validator
from enum import Enum
from typing import Optional, List
from datetime import datetime

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

class Issue(BaseModel):
    id: Optional[str] = None
    title: Optional[str]
    criteria: Optional[str]
    finding: Optional[str]
    risk_rating: Optional[str]
    process: Optional[str]
    source: Optional[str]
    sdi_name: Optional[str]
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

class IssueSendImplementation(BaseModel):
    id: List[str]

class IssueDeclineResponse(BaseModel):
    actor: ResponseActors
    decline_notes: Optional[str]

class IssueAcceptResponse(BaseModel):
    actor: ResponseActors
    accept_notes: Optional[str] = None
    accept_attachment: Optional[List[str]] = None
    lod2_feedback: Optional[LOD2Feedback] = None

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


class MailedIssue(BaseModel):
    id: Optional[str]
    title: Optional[str]
    criteria: Optional[str]
    finding: Optional[str]
    risk_rating: Optional[str]
    status: Optional[str]
    regulatory: Optional[bool]
    engagement: Optional[str]
    lod1_implementer: Optional[List[User]]
    lod1_owner: Optional[List[User]]
    lod2_risk_manager: Optional[List[User]]
    lod2_compliance_officer: Optional[List[User]]
    lod3_audit_manager: Optional[List[User]]
    implementors: List[str]

class IssueImplementationDetails(BaseModel):
    id: Optional[str] = None
    notes: Optional[str] = None
    attachments: Optional[List[str]] = None
    issued_by: Optional[User] = None
    type: Optional[str]

class Revise(BaseModel):
    reason: Optional[str]
    revised_date: datetime

