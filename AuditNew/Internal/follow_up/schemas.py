from typing import List, Optional
from datetime import datetime
from pydantic import  BaseModel
from enum import Enum


class FollowUpStatus(str, Enum):
    DRAFT = "Draft"
    PREPARED = "Prepared"
    COMPLETED = "Completed"

class FollowUpColumns(str, Enum):
    FOLLOW_UP_ID = "follow_up_id"
    MODULE_ID = "module_id"
    NAME = "name"
    ATTACHMENT = "attachment"
    STATUS = "status"
    CREATED_BY = "created_by"
    REVIEWED_BY = "reviewed_by"
    CREATED_AT = "created_at"


class NewFollowUp(BaseModel):
    name: str
    issue_ids: Optional[List[str]] = None
    engagement_ids: Optional[List[str]] = None
    attachment: Optional[str] = None


class CreateFollowUp(BaseModel):
    follow_up_id: str
    module_id: str
    name: str
    status: FollowUpStatus
    attachment: Optional[str] = None
    created_by: str
    reviewed_by: Optional[str] = None
    created_at: datetime
