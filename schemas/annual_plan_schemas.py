from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


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
    start: str
    end: str


class CreateAnnualPlan(NewAnnualPlan):
    id: str
    module: str
    reference: str
    status: AnnualPlanStatus
    creator: str
    created_at: datetime


class AnnualPlan(CreateAnnualPlan):
    pass


class ReadAnnualPlan(AnnualPlan):
    pass


class UpdateAnnualPlan(BaseModel):
    name: str
    year: str
    start: str
    end: str

class RemoveAnnualPlanPartially(BaseModel):
    status: AnnualPlanStatus






