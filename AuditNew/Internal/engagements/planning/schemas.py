from pydantic import BaseModel
from typing import Any, Optional, List
from enum import Enum

class Type(str, Enum):
    STANDARD = "standard"
    RISKS = "risks"
    LETTERS = "letters"
    PROGRAM = "program"

class Section(BaseModel):
    value: str | None

class User(BaseModel):
    id: int | None
    name: str | None

class PRCM(BaseModel):
    id: Optional[int] = None
    process: Optional[Section] = None
    risk: Optional[Section] = None
    risk_rating: Optional[str] = None
    control: Optional[Section] = None
    control_objective: Optional[Section] = None
    control_type: Optional[str] = None
    residue_risk: Optional[str] = None

class SummaryAuditProgram(BaseModel):
    process: Optional[Section] = None
    risk: Optional[Section] = None
    risk_rating: Optional[str] = None
    control: Optional[Section] = None
    procedure: Optional[str] = None
    program: Optional[str] = None

class EngagementLetter(BaseModel):
    name: Optional[str] = None
    value: Optional[str] = None

class StandardTemplate(BaseModel):
    reference: Optional[str] = ""
    title: Optional[str] = ""
    tests: Optional[Section] | None
    results: Optional[Section] | None
    observation: Optional[Section] | None
    attachments: Optional[List[str]] | None
    conclusion: Optional[Section] | None
    type: Optional[Type] | None = Type.STANDARD
    prepared_by: Optional[User] | None
    reviewed_by: Optional[User] | None
