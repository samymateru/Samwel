from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File, Query
from AuditNew.Internal.engagements.schemas import EngagementStatus
from models.engagement_models import get_module_engagement_model
from models.follow_up_models import add_new_follow_up, update_follow_up_details_model, remove_follow_up_data_model, \
    approve_follow_up_data_model, reset_follow_up_status_to_draft_model, complete_follow_up_model, \
    add_follow_up_test_model, update_follow_up_test_model, delete_follow_up_test_model
from models.issue_models import get_engagement_issues_model
from schemas.follow_up_schemas import NewFollowUp, UpdateFollowUpTest, CreateFollowUpTest, CreateFollowUp, \
    FollowUpStatus, UpdateFollowUp
from schema import ResponseMessage
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response, get_unique_key, return_checker
from typing import List, Optional


router = APIRouter(prefix="/follow_up")

@router.post("/{module_id}", response_model=ResponseMessage)
async def create_new_follow_up(
        module_id: str,
        name: str = Form(...),
        engagement_ids: Optional[List[str]] = Form(None),
        issue_ids: Optional[List[str]] = Form(None),
        attachment: Optional[UploadFile] = File(None),
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():

        data = await add_new_follow_up(
            connection=connection,
            follow_up=CreateFollowUp(
            follow_up_id=get_unique_key(),
            name=name,
            attachment= attachment.filename if attachment is not None else None,
            module_id=module_id,
            status=FollowUpStatus.DRAFT,
            created_at=datetime.now(),
            created_by="",
            )
        )

        return await return_checker(
            data=data,
            passed="Follow Up Successfully Created",
            failed="Failed Creating  Follow Up"
        )



@router.put("/{follow_up_id}", response_model=ResponseMessage)
async def update_follow_up_details(
        follow_up_id: str,
        name: str = Form(...),
        engagement_ids: Optional[List[str]] = Form(None),
        issue_ids: Optional[List[str]] = Form(None),
        attachment: Optional[UploadFile] = File(None),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await update_follow_up_details_model(
            connection=connection,
            follow_up=UpdateFollowUp(
                name=name,
                attachment=attachment.filename if attachment is not None else None,
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

