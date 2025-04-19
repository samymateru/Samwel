from pydantic import BaseModel
from typing import Optional, List

class CombinedRiskCategory(BaseModel):
    process_name: str
    sub_process_name: List[str]