from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class User(BaseModel):
    name: Optional[str]
    email: Optional[str]
    date_issued: Optional[datetime]

class MainProgram(BaseModel):
    id: Optional[str] = None
    name: Optional[str]

class SubProgram(BaseModel):
    id: Optional[str] = None
    reference: Optional[str] = None
    title: Optional[str]
    brief_description: Optional[str]
    audit_objective: Optional[str]
    test_description: Optional[str]
    test_type: Optional[str]
    sampling_approach: Optional[str]
    results_of_test: Optional[str]
    observation: Optional[str]
    extended_testing: Optional[bool]
    extended_procedure: Optional[str]
    extended_results: Optional[str]
    effectiveness: Optional[str]
    reviewed_by: Optional[User] = None
    prepared_by: Optional[User] = None
    conclusion: Optional[str]

class SubProgramEvidence(BaseModel):
    id: Optional[str] = None
    attachment: Optional[str]

class NewSubProgram(BaseModel):
    title: str







