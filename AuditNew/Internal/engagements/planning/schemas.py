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

class ProcedureTypes(str, Enum):
    PLANNING = "Planning"
    REPORTING = "Reporting"
    FINALIZATION = "Finalization"

class Section(BaseModel):
    value: str

class User(BaseModel):
    id: str
    name: str

class PreparedReviewedBy(BaseModel):
    name: Optional[str]
    email: Optional[str]
    date_issued: Optional[datetime] = datetime.now()

class PRCM(BaseModel):
    id: Optional[str] = None
    reference: Optional[str] = None
    process: Optional[str]
    risk: Optional[str]
    risk_rating: Optional[str]
    control: Optional[str]
    control_objective: Optional[str]
    control_type: Optional[str]
    residue_risk: Optional[str] = None
    summary_audit_program: Optional[str] = None
    type: Optional[str] = None

class SummaryAuditProgram(BaseModel):
    id: Optional[str] = None
    process: Optional[str]
    risk: Optional[str]
    risk_rating: Optional[str]
    control: Optional[str]
    control_objective: Optional[str]
    control_type: Optional[str]
    procedure: Optional[str]
    program: Optional[str]

class EngagementLetter(BaseModel):
    id: Optional[str] = None
    name: Optional[str]
    value: Optional[str]
    size: Optional[int]
    type: Optional[str] = None
    extension: Optional[str]

class StandardTemplate(BaseModel):
    id: Optional[str] = None
    reference: Optional[str] = None
    objectives: Optional[Section] = None
    title: Optional[str]
    tests: Optional[Section]
    results: Optional[Section]
    observation: Optional[Section]
    attachments: Optional[List[str]]
    conclusion: Optional[Section]
    type: Optional[Type]  = Type.STANDARD
    prepared_by: Optional[PreparedReviewedBy] = None
    reviewed_by: Optional[PreparedReviewedBy] = None

class NewPlanningProcedure(BaseModel):
    title: str


class SummaryAuditProgramResponse(BaseModel):
    reference: Optional[str] = None
    process: Optional[str]
    risk: Optional[str]
    risk_rating: Optional[str]
    control: Optional[str]
    control_type: Optional[str] = None
    procedure: Optional[str]
    program: Optional[str]
    procedure_id: Optional[str] = None


class SaveProcedure(BaseModel):
    objectives: Optional[Section] = None
    tests: Optional[Section]
    results: Optional[Section]
    observation: Optional[Section]
    conclusion: Optional[Section]
    type: Optional[ProcedureTypes]

class PlanningWorkProgram(BaseModel):
    program_name: str
    procedure_name: str
    prcm_id: str
