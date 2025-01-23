from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class NewPlanningDetails(BaseModel):
    engagement_id: int
    task: str
    notes: str
    status: str

class UpdatePlanningDetails(BaseModel):
    planning_id: int
    engagement_id: Optional[int] = None
    task: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None

class DeletePlanningDetails(BaseModel):
    planning_id: List[int]