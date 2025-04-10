from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

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
    date_raised: Optional[datetime]
    raised_by: Optional[User]
    action_owner: Optional[List[ActionOwner]]

class ResolveReviewComment(BaseModel):
    resolution_summary: Optional[str]
    resolution_details: Optional[str]
    resolved_by: Optional[User]
    date_resolved: Optional[datetime]
    decision: Optional[str]


class ReviewComment(BaseModel):
    id: Optional[int] = None
    title: Optional[str]
    reference: Optional[str] = None
    description: Optional[str]
    date_raised: Optional[datetime]
    raised_by: Optional[User]
    action_owner: Optional[User]
    resolution_summary: Optional[str]
    resolution_details: Optional[str]
    resolved_by: Optional[User]
    date_resolved: Optional[datetime]
    decision: Optional[str]