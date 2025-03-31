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
    reference: str
    title: Section
    date_raised: datetime
    raised_by: User
    resolution_summary: Section
    resolution_details: Section
    resolved_by: User
    date_resolved: datetime
    decision: str

class SummaryReviewNotes(BaseModel):
    reference: str
    title: Optional[str]
    date_raised: datetime
    raised_by: User
    resolution_summary: Optional[str]
    resolution_details: Optional[str]
    resolved_by: User
    date_resolved: datetime
    decision: str

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

class Note(BaseModel):
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
    reference: str
    title: str
    prepared_by: User
    reviewed_by: User
    effectiveness: str
    issue_count: int