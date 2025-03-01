from datetime import datetime
from pydantic import BaseModel
from typing import Any, Optional

class Section(BaseModel):
    value: str

class User(BaseModel):
    id: int
    name: str

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

class Task(BaseModel):
    id: Optional[int]
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
    id: Optional[int]
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

