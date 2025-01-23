from pydantic import BaseModel, Json
from datetime import datetime
from typing import List, Optional

class NewFeatureRecord(BaseModel):
    feature_id: int
    title: str
    record_type: str
    data: Json

class UpdateFeatureRecord(BaseModel):
    record_id: int
    feature_id: Optional[int] = None
    title: Optional[str] = None
    record_type: Optional[str] = None
    data: Optional[Json] = None

class DeleteFeatureRecord(BaseModel):
    record_id: List[int]
