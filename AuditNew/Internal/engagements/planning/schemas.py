from pydantic import BaseModel
from typing import Any, Optional, List
from enum import Enum
from datetime import datetime

class Type(str, Enum):
    STANDARD = "standard"
    RISKS = "risk"
    LETTERS = "letter"
    PROGRAM = "program"
    FINDING = "finding"
    PROCEDURE = "procedure"
    AUDIT_PROCEDURE = "audit_process"
    SHEET = "sheet"
    SURVEY = "survey"
    ARCHIVE = "archive"

class Section(BaseModel):
    value: str

class User(BaseModel):
    id: int
    name: str

class PRCM(BaseModel):
    id: Optional[int] = None
    process: Optional[str]
    risk: Optional[str]
    risk_rating: Optional[str]
    control: Optional[str]
    control_objective: Optional[str]
    control_type: Optional[str]
    residue_risk: Optional[str]
    summary_audit_program: Optional[int] = None

class SummaryAuditProgram(BaseModel):
    id: Optional[int] = None
    process: Optional[str]
    risk: Optional[str]
    risk_rating: Optional[str]
    control: Optional[str]
    control_objective: Optional[str]
    control_type: Optional[str]
    procedure: Optional[str]
    program: Optional[str]

class EngagementLetter(BaseModel):
    id: Optional[int] = None
    name: Optional[str]
    date_attached: Optional[datetime]
    attachment: Optional[str]

class StandardTemplate(BaseModel):
    id: Optional[int] = None
    reference: Optional[str] = None
    title: Optional[str]
    tests: Optional[Section]
    results: Optional[Section]
    observation: Optional[Section]
    attachments: Optional[List[str]]
    conclusion: Optional[Section]
    type: Optional[Type]  = Type.STANDARD
    prepared_by: Optional[User]
    reviewed_by: Optional[User]

class NewPlanningProcedure(BaseModel):
    title: str


class SummaryAuditProgramResponse(BaseModel):
    id: Optional[int] = None
    process: Optional[str]
    risk: Optional[str]
    risk_rating: Optional[str]
    control: Optional[str]
    procedure: Optional[str]
    program: Optional[str]