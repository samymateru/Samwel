from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class User(BaseModel):
    id: int
    name: str
    email: str
    date_issue: str

class MainProgram(BaseModel):
    id: Optional[int] = None
    name: Optional[str]

class SubProgram(BaseModel):
    id: Optional[int] = None
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
    conclusion: Optional[str]

class SubProgramEvidence(BaseModel):
    id: Optional[int] = None
    attachment: Optional[str]

class NewSubProgram(BaseModel):
    title: str





