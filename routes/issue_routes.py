from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, Form, UploadFile, File, HTTPException, BackgroundTasks
from core.utils import upload_attachment
from models.attachment_model import add_new_attachment
from models.issue_actor_models import initialize_issue_actors
from models.issue_models import create_new_issue_model, fetch_single_issue_item_model, update_issue_details_model, \
    delete_issue_details_model, issue_accept_model, mark_issue_reportable_model, save_issue_responses, \
    revise_issue_model, generate_issue_reference, fetch_issue_responses_model, \
    save_issue_implementation_model, send_issue_to_owner_model, send_issue_for_implementation_model
from schema import ResponseMessage, CurrentUser
from schemas.attachement_schemas import AttachmentCategory
from schemas.issue_schemas import NewIssue, SendIssueImplementor, IssueResponseActors, IssueLOD2Feedback, \
    NewDeclineResponse, UpdateIssueDetails, NewIssueResponse, IssueResponseTypes, IssueStatus, ReadIssues, \
    ReadIssueResponse, IssueActors
from services.connections.postgres.connections import AsyncDBPoolSingleton
from services.security.security import get_current_user
from utils import exception_response, return_checker

router = APIRouter(prefix="/issue")



@router.post("/{sub_program_id}", response_model=ResponseMessage)
async def create_new_issue(
        issue: NewIssue,
        sub_program_id: str,
        module_id: str = Query(...),
        engagement_id: str = Query(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        reference = await generate_issue_reference(
            connection=connection,
            module_id=module_id,
            source=issue.source
        )

        data = await create_new_issue_model(
            connection=connection,
            module_id=module_id,
            engagement_id=engagement_id,
            sub_program_id=sub_program_id,
            issue=issue,
            reference=reference
        )

        if data is None:
            raise HTTPException(status_code=400, detail="Error While Creating New Issue")

        results = await initialize_issue_actors(
            connection=connection,
            issue_id=data.get("id"),
            issue=issue
        )

        return await return_checker(
            data=results,
            passed="Issue Successfully Created",
            failed="Failed Creating  Issue"
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




@router.get("/single/{issue_id}", response_model=ReadIssues)
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



@router.put("/reportable/{issue_id}", response_model=ResponseMessage)
async def mark_issue_reportable(
        issue_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await mark_issue_reportable_model(
            connection=connection,
            issue_id=issue_id
        )

        return await return_checker(
            data=results,
            passed="Issue Marked Reportable Successfully",
            failed="Failed Mark Issue Reportable"
        )





@router.put("/send_implementor/")
async def send_issue_for_implementation(
        issue_ids: SendIssueImplementor,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        auth: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        results = await send_issue_for_implementation_model(
            connection=connection,
            issue_ids=issue_ids,
            user_id=auth.user_id
        )

        return await return_checker(
            data=results,
            passed="Successfully Send Issue",
            failed="Fail Sending Issue"
        )



@router.put("/save_implementation/{issue_id}")
async def save_issue_implementation(
        issue_id: str,
        notes: str = Form(...),
        attachment: UploadFile = File(None),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        auth: CurrentUser = Depends(get_current_user),
        background_tasks: BackgroundTasks = BackgroundTasks()
):
    with exception_response():
        response =  NewIssueResponse(
            notes=notes,
            type=IssueResponseTypes.SAVE,
            issued_by=auth.user_id
        )

        results = await save_issue_implementation_model(
            connection=connection,
            user_id=auth.user_id,
            issue_id=issue_id,
            response=response
        )


        if attachment is not None:
            await add_new_attachment(
                connection=connection,
                attachment=attachment,
                item_id=results.get("id"),
                module_id=auth.module_id,
                url=upload_attachment(
                category=AttachmentCategory.ISSUE_RESPONSES,
                background_tasks=background_tasks,
                file=attachment
                ),
                category=AttachmentCategory.ISSUE_RESPONSES
            )

        return await return_checker(
            data=results,
            passed="Successfully Save Issue Implementation",
            failed="Fail Save Issue Implementation"
        )



@router.put("/send_owner/{issue_id}")
async def send_issue_to_owner(
        issue_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        auth: CurrentUser = Depends(get_current_user),
):
    with exception_response():
        results = await send_issue_to_owner_model(
            connection=connection,
            issue_id=issue_id,
            user_id=auth.user_id
        )

        return await return_checker(
            data=results,
            passed="Successfully Send Issue To Owner",
            failed="Fail Send Issue To Owner"
        )




@router.get("/issue_updates/{issue_id}", response_model=List[ReadIssueResponse])
async def fetch_issue_updates(
        issue_id: str,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await fetch_issue_responses_model(
            connection=connection,
            issue_id=issue_id
        )
        return data




@router.put("/accept_response/{issue_id}")
async def issue_accept_response(
        issue_id: str,
        accept_actor: IssueResponseActors = Form(...),
        accept_notes: Optional[str] = Form(None),
        accept_attachment: Optional[UploadFile] = File(None),
        lod2_feedback: Optional[IssueLOD2Feedback] = Form(None),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        auth: CurrentUser = Depends(get_current_user),
        background_tasks: BackgroundTasks = BackgroundTasks()
):
    with exception_response():
        status = None

        if accept_actor == IssueActors.OWNER:
            status = IssueStatus.CLOSED_NOT_VERIFIED
        elif accept_actor == IssueActors.AUDIT_MANAGER:
            status = IssueStatus.CLOSED_VERIFIED_BY_AUDIT
        else:
            status = lod2_feedback

        results = await issue_accept_model(
            connection=connection,
            response=NewIssueResponse(
            notes=accept_notes,
            type=IssueResponseTypes.ACCEPT,
            issued_by=auth.user_id
            ),
            issue_id=issue_id,
            status=status
        )

        if accept_attachment is not None:
            await add_new_attachment(
                connection=connection,
                attachment=accept_attachment,
                item_id=results.get("id"),
                module_id=auth.module_id,
                url=upload_attachment(
                category=AttachmentCategory.ISSUE_RESPONSES,
                background_tasks=background_tasks,
                file=accept_attachment
                ),
                category=AttachmentCategory.ISSUE_RESPONSES
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
        auth: CurrentUser = Depends(get_current_user),
):
    with exception_response():
        status = None
        if issue.actor == IssueActors.OWNER:
            status = IssueStatus.IN_PROGRESS_IMPLEMENTER
        elif issue.actor == IssueActors.RISK_MANAGER or issue.actor == IssueActors.COMPLIANCE_OFFICER:
            status = IssueStatus.IN_PROGRESS_OWNER
        elif issue.actor == IssueActors.AUDIT_MANAGER:
            status = IssueStatus.CLOSED_NOT_VERIFIED
        else:
            status = None

        response = NewIssueResponse(
            notes=issue.decline_notes,
            type=IssueResponseTypes.DECLINE,
            issued_by=auth.user_id
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





@router.put("/revise/{issue_id}",)
async def request_issue_revise(
        issue_id: str,
        revised_date: Optional[datetime] = Form(None),
        reason: str = Form(None),
        attachment: UploadFile = File(None),
        user_id: str = Query(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        auth: CurrentUser = Depends(get_current_user),
        background_tasks: BackgroundTasks = BackgroundTasks()
):
    with exception_response():
        results = await revise_issue_model(
            connection=connection,
            revised_date=revised_date,
            issue_id=issue_id,
            user_id=user_id
        )

        if results is None:
            raise HTTPException(status_code=400, detail="Failed To Save Revise Issue")

        response_result = await save_issue_responses(
            connection=connection,
            response=NewIssueResponse(
            notes=reason,
            type=IssueResponseTypes.REVISE,
            issued_by=auth.user_id
            ),
            issue_id=issue_id
        )


        if attachment is not None:
            await add_new_attachment(
                connection=connection,
                attachment=attachment,
                item_id=response_result.get("id"),
                module_id=auth.module_id,
                url=upload_attachment(
                category=AttachmentCategory.ISSUE_RESPONSES,
                background_tasks=background_tasks,
                file=attachment
                ),
                category=AttachmentCategory.ISSUE_RESPONSES
            )


        return await return_checker(
            data=results,
            passed="Successfully Revise Issue",
            failed="Fail Revising Issue"
        )