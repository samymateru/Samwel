from pydantic import BaseModel
from typing import Any, Optional, List

class Section(BaseModel):
    value: str

class User(BaseModel):
    id: int
    name: str

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

class StandardTemplate(BaseModel):
    reference: Optional[str]
    title: str
    tests: Section
    results: Section
    observation: Section
    attachments: List[str]
    conclusion: Section
    prepared_by: User
    reviewed_by: User

