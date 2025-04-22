from pydantic import BaseModel
from typing import Optional, List

class CombinedRiskCategory(BaseModel):
    risk_category: str
    sub_risk_category: List[str]