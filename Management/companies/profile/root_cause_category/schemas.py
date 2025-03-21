from pydantic import BaseModel
from typing import List, Optional


class RootCauseCategory(BaseModel):
    id: Optional[int] = None
    name: str
    company: str