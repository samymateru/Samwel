from pydantic import BaseModel


class RiskRating(BaseModel):
    id: int
    name: str
    magnitude: int