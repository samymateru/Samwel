from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

class AttachmentSections(str, Enum):
    PLANNING = "Planning"
    FINALIZATION = "Finalization"
    REPORTING = "Reporting"
    PROGRAM = "Program"

class Attachment(BaseModel):
    id: Optional[str] = None
    engagement: str
    procedure: str
    name: str
    url: str
    size: int
    type: str
    section: AttachmentSections
    creator_name: Optional[str] = None
    creator_email: Optional[str] = None
    created_at: datetime = datetime.now()