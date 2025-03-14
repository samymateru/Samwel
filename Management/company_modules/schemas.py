from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CompanyModule(BaseModel):
    id: Optional[int] = None
    name: str
    purchase_date: datetime | None
    status: str

