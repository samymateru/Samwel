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
    id: Optional[int] | None
    process: Any | None
    risk: Section | None
    risk_rating: str | None
    control: Section | None
    control_objective: Section | None
    control_type: str | None
    residue_risk: str | None

class SummaryAuditProgram(BaseModel):
    process: Section | None
    risk: Section | None
    risk_rating: str | None
    control: Section | None
    procedure: str | None
    program: str | None

class EngagementLetter(BaseModel):
    name: str | None
    value: str | None

class StandardTemplate(BaseModel):
    reference: Optional[str] | None
    title: str | None
    tests: Section | None
    results: Section | None
    observation: Section | None
    attachments: List[str] | None
    conclusion: Section | None
    type: Type | None = Type.STANDARD
    prepared_by: User | None
    reviewed_by: User | None

