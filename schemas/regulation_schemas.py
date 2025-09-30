from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class RegulationColumns(str, Enum):
    ID = "id"
    ENGAGEMENT = "engagement"
    NAME = "name"
    ISSUE_DATE = "issue_date"
    KEY_AREAS = "key_areas"



class NewRegulation(BaseModel):
    name: str
    issue_date: datetime
    key_areas: str


class CreateRegulation(NewRegulation):
    id: str
    engagement: str


class UpdateRegulation(NewRegulation):
    pass


class BaseRegulation(CreateRegulation):
    pass


class ReadRegulation(BaseRegulation):
    pass
