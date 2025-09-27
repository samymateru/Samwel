from typing import List, Optional
from datetime import datetime
from pydantic import  BaseModel
from enum import Enum


class FollowUpStatus(str, Enum):
    DRAFT = "Draft"
    PREPARED = "Prepared"
    COMPLETED = "Completed"

class FollowUpColumns(str, Enum):
    FOLLOW_UP_ID = "follow_up_id"
    MODULE_ID = "module_id"
    NAME = "name"
    ATTACHMENT = "attachment"
    STATUS = "status"
    CREATED_BY = "created_by"
    REVIEWED_BY = "reviewed_by"
    CREATED_AT = "created_at"


class FollowUpTestColumns(str, Enum):
    TEST_ID = "test_id"
    FOLLOW_UP_ID = "follow_up_id"
    NAME = "name"
    DESCRIPTION = "description"
    OUTCOME = "outcome"
    CREATED_AT = "created_at"


class FollowUpEngagements(str, Enum):
    FOLLOW_UP_ENGAGEMENT_ID = "follow_up_engagement_id"
    FOLLOW_UP_ID = "follow_up_id"
    ENGAGEMENT_ID = "engagement_id"
    CREATED_AT = "created_at"



class FollowUpIssues(str, Enum):
    FOLLOW_UP_ISSUE_ID = "follow_up_issue_id"
    FOLLOW_UP_ID = "follow_up_id"
    ISSUE_ID = "issue_id"
    CREATED_AT = "created_at"


class NewFollowUp(BaseModel):
    name: str
    issue_ids: Optional[List[str]] = None
    engagement_ids: Optional[List[str]] = None
    attachment: Optional[str] = None

class CreateFollowUp(BaseModel):
    follow_up_id: str
    module_id: str
    name: str
    status: FollowUpStatus
    attachment: Optional[str] = None
    created_by: str
    reviewed_by: Optional[str] = None
    created_at: datetime


class UpdateFollowUp(BaseModel):
    name: str
    attachment: Optional[str] = None



class NewFollowUpTest(BaseModel):
    name: str
    description: Optional[str] = None
    outcome: Optional[str] = None



class UpdateFollowUpTest(NewFollowUpTest):
    name: str
    description: Optional[str] = None
    outcome: Optional[str] = None


class CreateFollowUpTest(NewFollowUpTest):
    test_id: str
    follow_up_id: str
    created_at: datetime


class CreateFollowUpEngagement(BaseModel):
    follow_up_engagement_id: str
    follow_up_id: str
    engagement_id: str
    created_at: datetime



class CreateFollowUpIssue(BaseModel):
    follow_up_issue_id: str
    follow_up_id: str
    issue_id: str
    created_at: datetime



class ReviewFollowUp(BaseModel):
    status: FollowUpStatus
    reviewed_by: str



class DisApproveFollowUp(BaseModel):
    status: FollowUpStatus
    reviewed_by: str



class CompleteFollowUp(BaseModel):
    status: FollowUpStatus