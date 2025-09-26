from enum import Enum
from pydantic import BaseModel

class EngagementPRCMColumns(str, Enum):
    ID = "id"
    PROCESS = "process"
    RISK = "risk"
    RISK_RATING = "risk_rating"
    CONTROL = "control"
    CONTROL_OBJECTIVE = "control_objective"
    CONTROL_TYPE = "control_type"
    RESIDUAL_RISK = "residual_risk"
    SUMMARY_AUDIT_PROGRAM = "summary_audit_program"
    TYPE = "type"
    CREATED_AT = "created_at"


class NewRiskEngagementPRCM(BaseModel):
    process: str
    risk: str
    risk_rating: str
    control: str
    control_objective: str
    control_type: str
    residual_risk: str


class CreateEngagementPRCM(NewRiskEngagementPRCM):
    id: str
    engagement: str
