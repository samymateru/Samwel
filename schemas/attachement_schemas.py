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



class NewAttachment(BaseModel):
    name: str
    url: str
    size: int
    type: str


class Attachment(BaseModel):

    attachment_id: str
    category: AttachmentCategory
    creator: str
    created_at: datetime