from typing import Optional
from fastapi import APIRouter, Depends, Query, Form, UploadFile, File, HTTPException

from models.issue_models import create_new_issue_model, fetch_single_issue_item_model, update_issue_details_model, \
    delete_issue_details_model, issue_accept_model, change_issue_status
from schemas.issue_schemas import NewIssue, SendIssueImplementor, IssueResponseActors, IssueLOD2Feedback, \
    NewDeclineResponse, UpdateIssueDetails, NewIssueResponse, IssueResponseTypes, IssueStatus
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response, return_checker

router = APIRouter(prefix="/issues")

@router.post("/{sub_program_id}")
async def create_new_issue(
        issue: NewIssue,
        sub_program_id: str,
        module_id: str = Query(...),
        engagement_id: str = Query(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await create_new_issue_model(
            connection=connection,
            module_id=module_id,
            engagement_id=engagement_id,
            sub_program_id=sub_program_id,
            issue=issue
        )

        return await return_checker(
            data=results,
            passed="Issue Successfully Created",
            failed="Failed Creating  Issue"
        )


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
        data = await fetch_single_issue_item_model(
            connection=connection,
            issue_id=issue_id
        )
        if data is None:
            raise HTTPException(status_code=404, detail="Issue Not Found")
        return data



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
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),

):
    with exception_response():
        status = None
        if accept_actor.value == "lod1_owner":
            status = IssueStatus.CLOSED_NOT_VERIFIED.value
        elif accept_actor.value == "lod3_audit_manager":
            status = IssueStatus.CLOSED_VERIFIED_BY_AUDIT.value
        else:
            status = lod2_feedback.value


        response = NewIssueResponse(
            notes=accept_notes,
            attachments=accept_attachment.filename,
            type=IssueResponseTypes.ACCEPT.value,
            issued_by=""
        )

        results = await issue_accept_model(
            connection=connection,
            response=response,
            issue_id=issue_id,
            status=status
        )

        return await return_checker(
            data=results,
            passed="Issue Successfully Accepted",
            failed="Failed Accepting  Issue"
        )


@router.put("/decline_response/{issue_id}")
async def issue_decline_response(
        issue_id: str,
        issue: NewDeclineResponse,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),

):
    with exception_response():
        status = None
        if issue.actor.value == "lod1_owner":
            status = IssueStatus.IN_PROGRESS_IMPLEMENTER.value
        elif issue.actor.value == "lod2_risk_manager" or issue.actor.value == "lod2_compliance_officer":
            status = IssueStatus.IN_PROGRESS_OWNER.value
        elif issue.actor.value == "lod3_audit_manager":
            status = IssueStatus.CLOSED_NOT_VERIFIED.value
        else:
            status = None

        response = NewIssueResponse(
            notes=issue.decline_notes,
            attachments=None,
            type=IssueResponseTypes.DECLINE.value,
            issued_by=""
        )

        results = await issue_accept_model(
            connection=connection,
            response=response,
            issue_id=issue_id,
            status=status
        )

        return await return_checker(
            data=results,
            passed="Issue Successfully Declined",
            failed="Failed Declining  Issue"
        )


@router.put("/{issue_id}")
async def update_issue_details(
        issue_id: str,
        issue: UpdateIssueDetails,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),

):
    with exception_response():
        results = await update_issue_details_model(
            connection=connection,
            issue=issue,
            issue_id=issue_id
        )

        return await return_checker(
            data=results,
            passed="Issue Successfully Updated",
            failed="Failed Updating  Issue"
        )


@router.delete("/{issue_id}")
async def delete_issue_details(
        issue_id: str,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await delete_issue_details_model(
            connection=connection,
            issue_id=issue_id
        )

        return await return_checker(
            data=results,
            passed="Issue Successfully Deleted",
            failed="Failed Deleting  Issue"
        )