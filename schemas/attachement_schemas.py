from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

class AttachmentCategory(str, Enum):
    PLANNING = "planning"
    FINALIZATION = "finalization"
    REPORTING = "reporting"
    PROCEDURE = "procedure"
    PROGRAM = "procedure"
    DRAFT_ENGAGEMENT = "draft_engagement"
    FINAL_ENGAGEMENT = "final_engagement"
    ANNUAL_PLAN = "annual_plan"
    ISSUE_IMPLEMENTATION = "issue_implementation"
    ENGAGEMENT_ADMINISTRATION = "engagement_administration"


class AttachmentColumns(str, Enum):
    ATTACHMENT_ID = "attachment_id"
    MODULE_ID = "module_id"
    FILENAME = "filename"
    ITEM_ID = "item_id"
    SIZE = "size"
    TYPE = "type"
    CATEGORY = "category"
    CREATOR = "creator"
    CREATED_AT = "created_at"


class CreateAttachment(BaseModel):
    attachment_id: Optional[str] = None
    module_id: Optional[str] = None
    item_id: Optional[str] = None
    filename: Optional[str] = None
    size: Optional[int] = None
    type: Optional[str] = None
    url: Optional[str] = None
    category: Optional[AttachmentCategory] = None
    creator: Optional[str] = None
    created_at: Optional[datetime] = None


class ReadAttachment(CreateAttachment):
    pass