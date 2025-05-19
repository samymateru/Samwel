from pydantic import BaseModel
from typing import Optional

class PlanDetails(BaseModel):
    total: Optional[int] = 0
    completed: Optional[int] = 0
    not_started: Optional[int] = 0
    closed: Optional[int] = 0