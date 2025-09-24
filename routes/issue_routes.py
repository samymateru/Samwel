from typing import Optional

from fastapi import APIRouter, Depends, Query, Form, UploadFile, File
from schemas.issue_schemas import NewIssue, SendIssueImplementor, IssueResponseActors, IssueLOD2Feedback, \
    NewDeclineResponse
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response

router = APIRouter(prefix="/issues")

@router.post("/{sub_program_id}")
async def create_new_issue(
        issue: NewIssue,
        sub_program_id: str,
        engagement_id: str = Query(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        print(issue)


@router.get("/{module_id}")
async def fetch_all_module_issues_filtered(
        module_id: str,
        filters: str =  Query(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass



@router.get("/{issue_id}")
async def fetch_single_issue_item(
        issue_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass


@router.get("/user/{user_id}")
async def fetch_all_user_issues(
        user_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass


@router.put("/save_implementation/{issue_id}")
async def save_issue_implementation(
        issue_id: str,
        notes: str = Form(...),
        attachment: UploadFile = File(None),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass


@router.put("/send_implementor")
async def send_issue_to_implementor(
        issue: SendIssueImplementor,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass



@router.put("/send_owner/{issue_id}")
async def send_issue_to_owner(
        issue_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass


@router.put("/accept_response/{issue_id}")
async def issue_accept_response(
        issue_id: str,
        accept_actor: IssueResponseActors = Form(...),
        accept_notes: Optional[str] = Form(None),
        accept_attachment: Optional[UploadFile] = File(None),
        lod2_feedback: Optional[IssueLOD2Feedback] = Form(None),
):
    with exception_response():
        pass


@router.put("/decline_response/{issue_id}")
async def issue_accept_response(
        issue_id: str,
        issue: NewDeclineResponse
):
    with exception_response():
        pass