from pydantic import BaseModel
from typing import Any, Optional, List
from enum import Enum

class Type(str, Enum):
    STANDARD = "standard"
    RISKS = "risk"
    LETTERS = "letter"
    PROGRAM = "program"
    FINDING = "finding"
    PROCEDURE = "procedure"
    SHEET = "sheet"
    SURVEY = "survey"
    ARCHIVE = "archive"

class Section(BaseModel):
    value: str

class User(BaseModel):
    id: int
    name: str

class PRCM(BaseModel):
    id: Optional[int]
    process: Optional[Section]
    risk: Optional[Section]
    risk_rating: Optional[str]
    control: Optional[Section]
    control_objective: Optional[Section]
    control_type: Optional[str]
    residue_risk: Optional[str]

class SummaryAuditProgram(BaseModel):
    process: Optional[Section]
    risk: Optional[Section]
    risk_rating: Optional[str]
    control: Optional[Section]
    procedure: Optional[str]
    program: Optional[str]

class EngagementLetter(BaseModel):
    name: Optional[str]
    value: Optional[str]

class StandardTemplate(BaseModel):
    id: Optional[int] = None
    reference: Optional[str] = None
    title: Optional[str] | Any
    tests: Optional[Section] | Any
    results: Optional[Section] | Any
    observation: Optional[Section] | Any
    attachments: Optional[List[str]] | Any
    conclusion: Optional[Section] | Any
    type: Optional[Type] | Any  = Type.STANDARD
    prepared_by: Optional[User] | Any
    reviewed_by: Optional[User] | Any
