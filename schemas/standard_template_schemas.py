from typing import Optional

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


class StandardTemplateColumns(str, Enum):
    ID = "id"
    ENGAGEMENT = "engagement"
    TITLE = "title"
    REFERENCE = "reference"
    CREATED_AT = "created_at"



class TemplateStatus(str, Enum):
    PENDING = "Pending"
    PREPARED = "Prepared"
    REVIEWED = "Reviewed"
    COMPLETED = "Completed"


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
    prepared_by: Optional[PreparedReviewedBy] = None
    reviewed_by: Optional[PreparedReviewedBy] = None



class UpdateStandardProcedure(BaseModel):
    tests: Section
    objectives: Section
    results: Section
    observation: Section
    conclusion: Section
    prepared_by: Optional[PreparedReviewedBy] = None
    reviewed_by: Optional[PreparedReviewedBy] = None




class ReadStandardTemplate(CreateStandardTemplate):
    pass


