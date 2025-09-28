from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

from schemas.attachement_schemas import ReadAttachment


class AnnualPlanStatus(str, Enum):
    PENDING = "Pending"
    ON_GOING = "Ongoing"
    COMPLETED = "Completed"
    DELETED = "Deleted"
    ARCHIVED = "Archived"


class AnnualPlanColumns(str, Enum):
    ID = "id"
    MODULE = "module"
    REFERENCE = "reference"
    NAME = "name"
    YEAR = "year"
    START = "start"
    END = "end"
    STATUS = "status"
    CREATOR = "creator"
    CREATED_AT = "created_at"


class NewAnnualPlan(BaseModel):
    name: str
    year: str
    start: datetime
    end: datetime


class CreateAnnualPlan(NewAnnualPlan):
    id: str
    module: str
    reference: str
    status: AnnualPlanStatus
    creator: Optional[str] = None
    created_at: Optional[datetime] = None


class AnnualPlan(CreateAnnualPlan):
    pass


class ReadAnnualPlan(AnnualPlan):
    attachment: ReadAttachment


class UpdateAnnualPlan(BaseModel):
    name: str
    year: str
    start: datetime
    end: datetime

class RemoveAnnualPlanPartially(BaseModel):
    status: AnnualPlanStatus






