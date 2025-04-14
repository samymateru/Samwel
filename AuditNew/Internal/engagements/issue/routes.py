from fastapi import APIRouter, Depends, Query, Form, UploadFile, File
from pydantic_core import ValidationError

from utils import  get_db_connection
from utils import get_current_user
from schema import CurrentUser
from schema import ResponseMessage
from AuditNew.Internal.engagements.issue.databases import *
from datetime import datetime

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

@router.put("/send_implementor/", response_model=ResponseMessage)
def send_issue_for_implementation(
        issue_ids: IssueSendImplementation,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        send_issues_to_implementor(connection=db, issue_ids=issue_ids, user_email=user.user_email)
        return ResponseMessage(detail="Successfully send the issue for implementation")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/save_implementation/{issue_id}", response_model=ResponseMessage)
def save_issue_implementation(
        issue_id: int,
        implementer_name: str = Form(...),
        notes: str = Form(...),
        attachment: Optional[UploadFile] = File(None),
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if attachment is None:
        issue_details = IssueImplementationDetails(
            notes=notes,
            issued_by=User(
                name=implementer_name,
                email=user.user_email,
                date_issued=datetime.now()
            ),
            type="save"
        )
    else:
        issue_details = IssueImplementationDetails(
            notes=notes,
            attachment=attachment.filename,
            issued_by=User(
                name=implementer_name,
                email=user.user_email,
                date_issued=datetime.now()
            ),
            type="save"
        )

    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        save_issue_implementation_(connection=db, issue_details=issue_details, issue_id=issue_id, user_email=user.user_email)
        return ResponseMessage(detail="Successfully save the issue")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/send_owner/{issue_id}", response_model=ResponseMessage)
def submit_issue_to_owner(
        issue_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        send_issues_to_owner(connection=db, issue_id=issue_id, user_email=user.user_email)
        return ResponseMessage(detail="Successfully send the issue to owner")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/accept_response/{issue_id}", response_model=ResponseMessage)
def issue_accept_response(
        issue_id: int,
        accept_actor: ResponseActors = Form(...),
        accept_notes: Optional[str] = Form(None),
        accept_attachment: Optional[UploadFile] = File(None),
        lod2_feedback: Optional[LOD2Feedback] = Form(None),
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        if accept_attachment is None:
            issue = IssueAcceptResponse(
                actor=accept_actor,
                accept_notes=accept_notes,
                lod2_feedback=lod2_feedback
            )
        else:
            issue = IssueAcceptResponse(
                actor=accept_actor,
                accept_notes=accept_notes,
                accept_attachment=[accept_attachment.filename],
                lod2_feedback=lod2_feedback
            )
        send_accept_response(connection=db, issue=issue, issue_id=issue_id, user_email=user.user_email)
        return ResponseMessage(detail=f"Successfully send accept response ")
    except ValidationError as v:
        raise HTTPException(status_code=422, detail=v.errors()[0].get("msg"))

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/decline_response/{issue_id}", response_model=ResponseMessage)
def issue_decline_response(
        issue_id: int,
        issue: IssueDeclineResponse,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        send_decline_response(connection=db, issue=issue, issue_id=issue_id, user_email=user.user_email)
        return ResponseMessage(detail=f"Successfully send decline response to {issue.actor}")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/", response_model=List[Issue])
def fetch_issue_based_on_actor(
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_issue_from_actor(connection=db, user_email=user.user_email)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)



