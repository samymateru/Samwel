from pydantic import BaseModel, Json
from typing import Optional, List

class NewEngagementProfile(BaseModel):
    engagement_id: int
    profile_name: str
    key_contacts: Json
    estimated_time: str
    business_context: str

class UpdateEngagementProfile(BaseModel):
    profile_id: int
    engagement_id: Optional[int] = None
    profile_name: Optional[str] = None
    key_contacts: Optional[Json] = None
    estimated_time: Optional[str] = None
    business_context: Optional[str] = None

class DeleteEngagementProfile(BaseModel):
    profile_id: List[int]


