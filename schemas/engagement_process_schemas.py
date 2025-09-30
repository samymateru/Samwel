from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class EngagementProcessColumns(str, Enum):
    ID = "id"
    ENGAGEMENT = "engagement"
    PROCESS = "process"
    SUB_PROCESS = "sub_process"
    DESCRIPTION = "description"
    BUSINESS_UNIT = "business_unit"


class NewEngagementProcess(BaseModel):
    process: str
    sub_process: List[str]
    description: str
    business_unit: Optional[str] = None


class CreateEngagementProcess(NewEngagementProcess):
    id: str
    engagement: str


class UpdateEngagementProcess(NewEngagementProcess):
    pass


class BaseEngagementProcess(CreateEngagementProcess):
    pass


class ReadEngagementProcess(BaseEngagementProcess):
    pass



