from pydantic import BaseModel
from typing import Optional

class PlanDetails(BaseModel):
    total: Optional[int] = 0
    completed: Optional[int] = 0
    pending: Optional[int] = 0
    ongoing: Optional[int] = 0