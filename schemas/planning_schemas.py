from pydantic import BaseModel


class AttachDaftEngagement(BaseModel):
    engagement_name: str
    plan_name: str
    plan_year: str
    attachment: str
