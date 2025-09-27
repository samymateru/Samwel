from typing import Optional

from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class RiskControlColumns(str, Enum):
    ID = "id"
    RISK = "risk"
    RISK_RATING = "risk_rating"
    CONTROL = "control"
    CONTROL_OBJECTIVE = "control_objective"
    CONTROL_TYPE = "control_type"
    RESIDUAL_RISK = "residue_risk"
    TYPE = "type"
    SUMMARY_AUDIT_PROGRAM = "summary_audit_program"
    CREATED_AT = "created_at"


class NewRiskControl(BaseModel):
    risk: str
    risk_rating: str
    control: str
    control_objective: str
    control_type: str
    residue_risk: Optional[str] = None

class CreateRiskControl(NewRiskControl):
    id: str
    type: str
    summary_audit_program: str
    created_at: datetime

class UpdateRiskControl(NewRiskControl):
    pass
