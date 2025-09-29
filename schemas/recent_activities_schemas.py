from typing import Optional

from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class RecentActivityColumns(str, Enum):
    ACTIVITY_ID = "activity_id"
    MODULE_ID = "module_id"
    NAME = "name"
    DESCRIPTION = "description"
    CATEGORY = "category"
    CREATED_BY = "created_by"
    CREATED_AT = "created_at"



class RecentActivityCategory(str, Enum):
    ANNUAL_PLAN_CREATED = "annual_plan_created"
    ENGAGEMENT_CREATED = "engagement_created"
    ENGAGEMENT_COMPLETED = "engagement_completed"
    ENGAGEMENT_UPDATED = "engagement_updated"
    ENGAGEMENT_ARCHIVED = "engagement_archived"
    ENGAGEMENT_DELETED = "engagement_deleted"


class RecentActivities(BaseModel):
    activity_id: str
    module_id: str
    name: Optional[str] = None
    description: str
    category: str
    created_by: str
    created_at: datetime