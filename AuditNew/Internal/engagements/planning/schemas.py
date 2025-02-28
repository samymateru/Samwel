from pydantic import BaseModel
from typing import Any, Optional

class Section(BaseModel):
    value: str

class PRCM(BaseModel):
    id: Optional[int]
    process: Section
    risk: Section
    risk_rating: str
    control: Section
    control_objective: Section
    control_type: str
    residue_risk: str

class SummaryAuditProgram(BaseModel):
    process: Section
    risk: Section
    risk_rating: str
    control: Section
    procedure: str
    program: str

class EngagementLetter(BaseModel):
    name: str
    value: str

class Planning(BaseModel):
    pass
