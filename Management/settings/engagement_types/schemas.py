from pydantic import BaseModel

class EngagementTypes(BaseModel):
    id: int
    name: str