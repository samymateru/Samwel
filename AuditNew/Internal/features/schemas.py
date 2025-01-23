from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class NewFeature(BaseModel):
    module_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True

class UpdateFeature(BaseModel):
    feature_id: int
    module_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    updated_at: datetime = datetime.now()

class DeleteFeature(BaseModel):
    feature_id: List[int]
