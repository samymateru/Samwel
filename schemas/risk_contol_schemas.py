from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class RiskControlColumns(str, Enum):
    ID = "id"
    SUB_PROGRAM = "sub_program"
    RISK = "risk"
    RISK_RATING = "risk_rating"
    CONTROL = "control"
    CONTROL_OBJECTIVE = "control_objective"
    CONTROL_TYPE = "control_type"
    RESIDUAL_RISK = "residual_risk"

class NewRiskControl(BaseModel):
    risk: str
    risk_rating: str
    control: str
    control_objective: str
    control_type: str
    residual_risk: str

class CreateRiskControl(NewRiskControl):
    id: str
    sub_program: str
    created_at: datetime

class UpdateRiskControl(NewRiskControl):
    pass
