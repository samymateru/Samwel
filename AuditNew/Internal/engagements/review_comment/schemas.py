from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ReviewCommentDecisionStatus(str, Enum):
    CLOSED_ACCEPTED = "Closed & Accepted"
    RE_OPEN = "Re-open"

class User(BaseModel):
    name: Optional[str]
    email: Optional[str]
    date_issued: Optional[datetime]

class ActionOwner(BaseModel):
    name: Optional[str]
    email: Optional[str]


class NewReviewComment(BaseModel):
    title: Optional[str]
    description: Optional[str]
    raised_by: Optional[User]
    href: Optional[str]
    action_owner: Optional[List[ActionOwner]]

class ResolveReviewComment(BaseModel):
    resolution_summary: Optional[str]
    resolution_details: Optional[str]
    resolved_by: Optional[User]

class ReviewCommentDecision(BaseModel):
    decision: Optional[ReviewCommentDecisionStatus]

