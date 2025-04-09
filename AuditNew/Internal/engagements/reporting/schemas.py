from pydantic import BaseModel
from typing import Optional

class NewReportingProcedure(BaseModel):
    title: str

class ProgramSummary(BaseModel):
    id: Optional[int]
    name: str
    status: Optional[str]
    process_rating: Optional[str]
    issue_count: int
    acceptable: int
    improvement_required: int
    significant_improvement_required: int
    unacceptable: int
    recurring_issues: int
