from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File, Query, BackgroundTasks
from AuditNew.Internal.engagements.schemas import EngagementStatus
from core.utils import upload_attachment
from models.attachment_model import add_new_attachment
from models.engagement_models import get_module_engagement_model
from models.follow_up_models import add_new_follow_up, update_follow_up_details_model, remove_follow_up_data_model, \
    approve_follow_up_data_model, reset_follow_up_status_to_draft_model, complete_follow_up_model, \
    add_follow_up_test_model, update_follow_up_test_model, delete_follow_up_test_model, attach_engagements_to_follow_up, \
    attach_issues_to_follow_up, get_all_module_follow_up, get_follow_up_test_model
from models.issue_models import get_engagement_issues_model
from schemas.attachement_schemas import AttachmentCategory
from schemas.follow_up_schemas import UpdateFollowUpTest, CreateFollowUpTest, CreateFollowUp, \
    FollowUpStatus, UpdateFollowUp, ReadFollowUpData
from schema import ResponseMessage
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response, get_unique_key, return_checker
from typing import List, Optional


router = APIRouter(prefix="/follow_up")


@router.post("/{module_id}")
async def create_new_follow_up(
        module_id: str,
        name: str = Form(...),
        engagement_ids: Optional[List[str]] = Form(None),
        issue_ids: Optional[List[str]] = Form(None),
        attachment: Optional[UploadFile] = File(None),
        reviewed_by: str = Form(...),
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
        background_tasks: BackgroundTasks = BackgroundTasks()
):
    with exception_response():

        follow_up_data = await add_new_follow_up(
            connection=connection,
            follow_up=CreateFollowUp(
            follow_up_id=get_unique_key(),
            name=name,
            attachment= attachment.filename if attachment is not None else None,
            module_id=module_id,
            status=FollowUpStatus.DRAFT,
            created_at=datetime.now(),
            reviewed_by=reviewed_by,
            created_by=""
            )
        )


        if follow_up_data is None:
            raise HTTPException(status_code=400, detail="Failed To Create Follow Up")


        for engagement_id in engagement_ids:
            await attach_engagements_to_follow_up(
                connection=connection,
                follow_up_id=follow_up_data.get("follow_up_id"),
                engagement_id=engagement_id
            )


        for issue_id in issue_ids:
            await attach_issues_to_follow_up(
                connection=connection,
                follow_up_id=follow_up_data.get("follow_up_id"),
                issue_id=issue_id
            )

        if attachment is not None:
            await add_new_attachment(
                connection=connection,
                attachment=attachment,
                item_id=follow_up_data.get("follow_up_id"),
                module_id=module_id,
                url=upload_attachment(
                category=AttachmentCategory.FOlLOW_UP,
                background_tasks=background_tasks,
                file=attachment
                ),
                category=AttachmentCategory.FOlLOW_UP
            )


        return follow_up_data



@router.put("/{follow_up_id}", response_model=ResponseMessage)
async def update_follow_up_details(
        follow_up_id: str,
        name: str = Form(...),
        reviewed_by: str = Form(...),
        attachment: Optional[UploadFile] = File(None),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await update_follow_up_details_model(
            connection=connection,
            follow_up=UpdateFollowUp(
                name=name,
                attachment=attachment.filename if attachment is not None else None,
                reviewed_by=reviewed_by
            ),
            follow_up_id=follow_up_id
        )


        return await return_checker(
            data=data,
            passed="Follow Up Successfully Updated",
            failed="Failed Updating  Follow Up"
        )



@router.delete("/{follow_up_id}", response_model=ResponseMessage)
async def remove_follow_up_data(
        follow_up_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await remove_follow_up_data_model(
            connection=connection,
            follow_up_id=follow_up_id
        )

        return await return_checker(
            data=results,
            passed="Follow Up Successfully Deleted",
            failed="Failed Deleting  Follow Up"
        )



@router.get("/engagements/{module_id}")
async def fetch_all_completed_engagements(
        module_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_module_engagement_model(
            connection=connection,
            module_id=module_id,
            status=EngagementStatus.COMPLETED
        )

        return data



@router.get("/issues/{module_id}")
async def fetch_all_issues_on_engagement(
        module_id: str,
        engagement_ids: List[str] = Query(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_engagement_issues_model(
            connection=connection,
            engagement_ids=engagement_ids,
            module_id=module_id
        )

        return data




@router.get("/{module_id}", response_model=List[ReadFollowUpData])
async def fetch_all_follow_up_on_module(
        module_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_all_module_follow_up(
            connection=connection,
            module_id=module_id
        )

        return data




@router.put("/review/{follow_up_id}", response_model=ResponseMessage)
async def review_follow_up_data(
        follow_up_id: str,
        reviewed_by: str = Query(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await approve_follow_up_data_model(
            connection=connection,
            reviewed_by=reviewed_by,
            follow_up_id=follow_up_id
        )

        return await return_checker(
            data=results,
            passed="Follow Up Successfully Reviewed",
            failed="Failed Reviewing  Follow Up"
        )



@router.put("/disprove/{follow_up_id}", response_model=ResponseMessage, description="This Endpoint Reverser status to draft")
async def reset_follow_up_status_to_draft(
        follow_up_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await reset_follow_up_status_to_draft_model(
            connection=connection,
            follow_up_id=follow_up_id
        )

        return await return_checker(
            data=results,
            passed="Follow Up Successfully Reset",
            failed="Failed Resetting  Follow Up"
        )



@router.put("/complete/{follow_up_id}", response_model=ResponseMessage)
async def complete_follow_up_data(
        follow_up_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await complete_follow_up_model(
            connection=connection,
            follow_up_id=follow_up_id
        )

        return await return_checker(
            data=results,
            passed="Follow Up Successfully Completed",
            failed="Failed Completing  Follow Up"
        )



@router.post("/test/{follow_up_id}", response_model=ResponseMessage)
async def create_new_follow_up_test(
        follow_up_id: str,
        test: CreateFollowUpTest,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await add_follow_up_test_model(
            connection=connection,
            follow_up_id=follow_up_id,
            test=test
        )


        return await return_checker(
            data=results,
            passed="Follow Up Test Successfully Created",
            failed="Failed Creating Follow Up Test"
        )



@router.put("/test/{test_id}", response_model=ResponseMessage)
async def update_follow_up_test(
        test_id: str,
        test: UpdateFollowUpTest,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await update_follow_up_test_model(
            connection=connection,
            test_id=test_id,
            test=test
        )

        return await return_checker(
            data=results,
            passed="Follow Up Test Successfully Updated",
            failed="Failed Updated Follow Up Test"
        )





@router.get("/test/{follow_up_id}", response_model=ResponseMessage)
async def fetch_follow_up_test_model(
        follow_up_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_follow_up_test_model(
            connection=connection,
            follow_up_id=follow_up_id
        )
        return data



@router.delete("/test/{test_id}", response_model=ResponseMessage)
async def delete_follow_up_test(
        test_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await delete_follow_up_test_model(
            connection=connection,
            test_id=test_id
        )

        return await return_checker(
            data=results,
            passed="Follow Up Test Successfully Deleted",
            failed="Failed Deleting Follow Up Test"
        )

