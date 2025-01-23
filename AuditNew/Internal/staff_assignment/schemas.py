from pydantic import BaseModel
from typing import  List, Optional

class NewStaffAssignment(BaseModel):
    engagement_id: int
    user_id: int
    role: str

class UpdateStaffAssignment(BaseModel):
    assignment_id: int
    engagement_id: Optional[int] = None
    user_id: Optional[int] = None
    role: Optional[str] = None

class DeleteStaffAssignment(BaseModel):
    assignment_id: List[int]

