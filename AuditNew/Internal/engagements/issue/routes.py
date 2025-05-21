from fastapi import APIRouter, Depends, Query, Form, UploadFile, File, BackgroundTasks
from pydantic_core import ValidationError
from s3 import upload_file
from utils import  get_async_db_connection
from utils import get_current_user
from schema import CurrentUser
from schema import ResponseMessage
from AuditNew.Internal.engagements.issue.databases import *
from datetime import datetime
import tempfile
import shutil
import uuid
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(prefix="/issue")


@router.post("/{sub_program_id}", response_model=ResponseMessage)
async def create_new_issue_(
        sub_program_id: str,
        issue: Issue,
        engagement_id: str = Query(),
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await add_new_issue(db, issue=issue, sub_program_id=sub_program_id, engagement_id=engagement_id)
        return ResponseMessage(detail="Issue created successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{issue_id}", response_model=ResponseMessage)
async def update_issue(
        issue_id: str,
        issue: Issue,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_issue(db, issue=issue, issue_id=issue_id)
        return ResponseMessage(detail="Issue successfully updated")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{issue_id}", response_model=ResponseMessage)
async def delete_issue(
        issue_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await remove_issue(connection=db, issue_id=issue_id)
        return ResponseMessage(detail="Issue deleted successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/send_implementor/", response_model=ResponseMessage)
async def send_issue_for_implementation(
        issue_ids: IssueSendImplementation,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await send_issues_to_implementor(connection=db, issue_ids=issue_ids, user_email=user.user_email)
        return ResponseMessage(detail="Successfully send the issue for implementation")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/save_implementation/{issue_id}", response_model=ResponseMessage)
async def save_issue_implementation(
        issue_id: str,
        implementer_name: str = Form(...),
        notes: str = Form(...),
        attachment: Optional[UploadFile] = File(None),
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user),
        background_tasks: BackgroundTasks = BackgroundTasks()
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        key: Optional[str] = None
        temp_path = ""
        if attachment is None:
            issue_details = IssueImplementationDetails(
                notes=notes,
                issued_by=User(
                    name=user.user_name,
                    email=user.user_email,
                    date_issued=datetime.now()
                ),
                type="save"
            )
        else:
            key: str = f"issue/{user.company_name}/{uuid.uuid4()}-{attachment.filename}"
            public_url: str = f"https://{os.getenv("S3_BUCKET_NAME")}.s3.{os.getenv("AWS_DEFAULT_REGION")}.amazonaws.com/{key}"
            issue_details = IssueImplementationDetails(
                notes=notes,
                attachments=[public_url],
                issued_by=User(
                    name=user.user_name,
                    email=user.user_email,
                    date_issued=datetime.now()
                ),
                type="save"
            )

        is_success = await save_issue_implementation_(connection=db, issue_details=issue_details, issue_id=issue_id, user_email=user.user_email)
        if is_success:
            if attachment is not None:
                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    shutil.copyfileobj(attachment.file, tmp)
                    temp_path = tmp.name
                background_tasks.add_task(upload_file, temp_path, key)
        return ResponseMessage(detail="Successfully save the issue")
    except HTTPException as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/send_owner/{issue_id}", response_model=ResponseMessage)
async def submit_issue_to_owner(
        issue_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await send_issues_to_owner(
            connection=db,
            issue_id=issue_id,
            user_email=user.user_email,
            user_name=user.user_name)
        return ResponseMessage(detail="Successfully send the issue to owner")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/accept_response/{issue_id}", response_model=ResponseMessage)
async def issue_accept_response(
        issue_id: str,
        accept_actor: ResponseActors = Form(...),
        accept_notes: Optional[str] = Form(None),
        accept_attachment: Optional[UploadFile] = File(None),
        lod2_feedback: Optional[LOD2Feedback] = Form(None),
        db=Depends(get_async_db_connection),
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
        is_success = await send_accept_response(
            connection=db,
            issue=issue,
            issue_id=issue_id,
            user_email=user.user_email,
            user_name=user.user_name)
        if is_success:
            if accept_attachment is not None:
                pass
        return ResponseMessage(detail=f"Successfully send accept response ")
    except ValidationError as v:
        raise HTTPException(status_code=422, detail=v.errors()[0].get("msg"))

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/decline_response/{issue_id}", response_model=ResponseMessage)
async def issue_decline_response(
        issue_id: str,
        issue: IssueDeclineResponse,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await send_decline_response(
            connection=db,
            issue=issue,
            issue_id=issue_id,
            user_email=user.user_email,
            user_name=user.user_name)
        return ResponseMessage(detail=f"Successfully decline issue")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/revise/{issue_id}", response_model=ResponseMessage)
async def request_revise(
        issue_id: str,
        revise: Revise,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await request_extension_time(connection=db, revise=revise, issue_id=issue_id, user_email=user.user_email)
        return ResponseMessage(detail=f"Successfully requesting time extension")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/", response_model=List[Issue])
async def fetch_issue_based_on_actor(
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_issue_from_actor(connection=db, user_email=user.user_email)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/{issue_id}", response_model=Issue)
async def fetch_single_issue(
        issue_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_single_issue(connection=db, issue_id=issue_id)
        if data.__len__() == 0:
            raise HTTPException(status_code=400, detail="Issue not found")
        return data[0]
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/updates/{issue_id}", response_model=List[IssueImplementationDetails])
async def fetch_issue_updates(
        issue_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_issue_updates(connection=db, issue_id=issue_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/prepared/{issue_id}", response_model=ResponseMessage)
async def prepare_issue(
        issue_id: str,
        prepare: User,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await mark_issue_prepared(connection=db, prepare=prepare, issue_id=issue_id)
        return ResponseMessage(detail="Issue marked prepared successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/reviewed/{issue_id}", response_model=ResponseMessage)
async def review_issue(
        issue_id: str,
        review: User,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await mark_issue_reviewed(connection=db, review=review, issue_id=issue_id)
        return ResponseMessage(detail="Issue marked reviewed successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/reportable/{issue_id}", response_model=ResponseMessage)
async def report_issue(
        issue_id: str,
        reportable: bool = Query(),
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await mark_issue_reportable(connection=db, reportable=reportable, issue_id=issue_id)
        return ResponseMessage(detail="Issue marked reportable successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


