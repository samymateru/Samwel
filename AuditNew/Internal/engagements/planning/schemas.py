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
    email: Optional[str] = None
    date_issued: Optional[datetime] = datetime.now()



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


class SaveProcedure(BaseModel):
    objectives: Optional[Section] = None
    tests: Section
    results: Section
    observation: Section
    conclusion: Section
    type: ProcedureTypes

