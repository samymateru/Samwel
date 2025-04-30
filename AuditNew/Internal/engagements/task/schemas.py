from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TaskDecisionStatus(str, Enum):
    CLOSED_ACCEPTED = "Closed & Accepted"
    RE_OPEN = "Re-open"

class User(BaseModel):
    name: Optional[str]
    email: Optional[str]
    date_issued: Optional[datetime]


class ActionOwner(BaseModel):
    name: Optional[str]
    email: Optional[str]


class NewTask(BaseModel):
    title: Optional[str]
    description: Optional[str]
    raised_by: Optional[User]
    action_owner: Optional[List[ActionOwner]]

class ResolveTask(BaseModel):
    resolution_summary: Optional[str]
    resolution_details: Optional[str]
    resolved_by: Optional[User]

class TaskDecision(BaseModel):
    decision: Optional[TaskDecisionStatus]
