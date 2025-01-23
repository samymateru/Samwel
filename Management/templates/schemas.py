from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class NewTemplate(BaseModel):
    name: str
    category: str
    phases: List[str]
    actions: List[str]
    procedures: List[str]
    created_at: datetime = datetime.now()
