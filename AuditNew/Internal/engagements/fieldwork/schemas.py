from datetime import datetime
from pydantic import BaseModel
from typing import Any, Optional

class Section(BaseModel):
    value: str

class User(BaseModel):
    name: str
    email: str

class SummaryProcedures(BaseModel):
    id: Optional[int]
    reference: Optional[str]
    title: Optional[Section]
    date_raised: Optional[datetime]
    raised_by: Optional[User]
    resolution_summary: Optional[Section]
    resolution_details: Optional[Section]
    resolved_by: Optional[User]
    date_resolved: Optional[datetime]
    decision: Optional[str]

class SummaryReviewNotes(BaseModel):
    reference: Optional[str]
    title: Optional[str]
    description: Optional[str]
    date_raised: Optional[datetime]
    raised_by: Optional[User]
    resolution_summary: Optional[str]
    resolution_details: Optional[str]
    resolved_by: Optional[User]
    date_resolved: Optional[datetime]
    decision: Optional[str]

class SummaryTask(BaseModel):
    reference: Optional[str]
    title: Optional[str]
    description: Optional[str]
    date_raised: Optional[datetime]
    raised_by: Optional[User]
    resolution_summary: Optional[str]
    resolution_details: Optional[str]
    resolved_by: Optional[User]
    date_resolved: Optional[datetime]
    decision: Optional[str]

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Section
    date_raised: datetime
    raised_by: User
    action_owner: User
    resolution_summary: Section
    resolution_details: Section
    resolved_by: User
    date_resolved: datetime
    decision: str

class SummaryAuditProcedure(BaseModel):
    reference: Optional[str]
    program: Optional[str]
    title: Optional[str]
    prepared_by: Optional[User]
    reviewed_by: Optional[User]
    effectiveness: Optional[str]
    issue_count: Optional[int]