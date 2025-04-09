from fastapi import APIRouter, Depends, HTTPException, Query
from utils import  get_db_connection
from utils import get_current_user
from schema import CurrentUser
from schema import ResponseMessage
from AuditNew.Internal.engagements.issue.databases import *

router = APIRouter(prefix="/issue")


@router.post("/{sub_program_id}", response_model=ResponseMessage)
def create_new_issue_(
        sub_program_id: int,
        issue: Issue,
        engagement_id: int = Query(),
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        add_new_issue(db, issue=issue, sub_program_id=sub_program_id, engagement_id=engagement_id)
        return {"detail": "Issue created successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{issue_id}", response_model=ResponseMessage)
def update_issue(
        issue_id: int,
        issue: Issue,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_issue(db, issue=issue, issue_id=issue_id)
        return {"detail": "Issue successfully updated"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{issue_id}", response_model=ResponseMessage)
def delete_issue(
        issue_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        remove_issue(connection=db, issue_id=issue_id)
        return {"detail": "Issue deleted successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/send/{issue_id}", response_model=ResponseMessage)
def send_issue_for_survey(
        issue_id: int,
        contacts: IssueContacts,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        send_issue(connection=db, contacts=contacts, issue_id=issue_id)
        return ResponseMessage(detail="Issue sent successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
