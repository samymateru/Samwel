from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class PRCMColumns(str, Enum):
    ID = "id"
    ENGAGEMENT = "engagement"
    RISK = "risk"
    RISK_RATING = "risk_rating"
    CONTROL = "control"
    CONTROL_OBJECTIVE = "control_objective"
    CONTROL_TYPE = "control_type"
    RESIDUAL_RISK = "residual_risk"
    TYPE = "type"
    SUMMARY_AUDIT_PROGRAM = "summary_audit_program"
    CREATED_AT = "created_at"


class NewPRCM(BaseModel):
    process: str
    risk: str
    risk_rating: str
    control: str
    control_objective: str
    control_type: str
    residue_risk: Optional[str] = None


class CreatePRCM(NewPRCM):
    id: str
    type: str
    engagement_id: str
    created_at: datetime


class UpdatePRCM(NewPRCM):
    pass


class AddToAuditProgram(BaseModel):
    summary_audit_program: Optional[str] = None
