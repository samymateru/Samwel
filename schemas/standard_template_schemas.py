from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class TemplateType(str, Enum):
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


class TemplateStatus(str, Enum):
    PENDING = "pending"
    PREPARED = "prepared"
    REVIEWED = "reviewed"
    COMPLETED = "completed"


class ProcedureTypes(str, Enum):
    PLANNING = "Planning"
    REPORTING = "Reporting"
    FINALIZATION = "Finalization"


class PreparedReviewedBy(BaseModel):
    name: str
    email: str
    date_issued: datetime


class NewStandardTemplate(BaseModel):
    title: str


class Section(BaseModel):
    value: str



class CreateStandardTemplate(NewStandardTemplate):
    id: str
    engagement: str
    reference: str
    tests: Section
    objectives: Section
    results: Section
    observation: Section
    conclusion: Section
    type: TemplateType
    status: TemplateStatus
    prepared_by: PreparedReviewedBy
    reviewed_by: PreparedReviewedBy



class ReadStandardTemplate(CreateStandardTemplate):
    pass


