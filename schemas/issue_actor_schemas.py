from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class IssueActorColumns(str, Enum):
    ISSUE_ACTOR_ID = "issue_actor_id"
    ISSUE_ID = "issue_id"
    USER_ID = "user_id"
    NAME = "name"
    EMAIL = "email"
    ROLE = "role"
    CREATED_AT = "created_at"


class IssueActors(str, Enum):
    IMPLEMENTER = "lod1_implementer"
    OWNER = "lod1_owner"
    RISK_MANAGER = "lod2_risk_manager"
    COMPLIANCE_OFFICER = "lod2_compliance_officer"
    AUDIT_MANAGER = "lod3_audit_manager"
    OBSERVERS = "observers"


class NewIssueActor(BaseModel):
    user_id: str
    name: str
    email: str
    role: IssueActors


class CreateIssueActor(NewIssueActor):
    issue_actor_id: str
    issue_id: str
    created_at: datetime


class ReadIssueActors(CreateIssueActor):
    pass