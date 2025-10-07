from datetime import datetime
from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException, BackgroundTasks

from core.utils import upload_attachment
from models.attachment_model import add_new_attachment
from models.regulation_models import create_new_regulation_model, update_engagement_regulation_model, \
    get_engagement_regulations_model, get_single_engagement_regulation_model, delete_engagement_regulation_model
from schema import ResponseMessage, CurrentUser
from schemas.attachement_schemas import AttachmentCategory
from schemas.regulation_schemas import NewRegulation, UpdateRegulation
from services.connections.postgres.connections import AsyncDBPoolSingleton
from services.security.security import get_current_user
from utils import exception_response, return_checker

router = APIRouter(prefix="/engagements")

@router.post("/context/regulations/{engagement_id}", status_code=201, response_model=ResponseMessage)
async def create_new_regulation(
        engagement_id: str,
        name: str = Form(...),
        issue_date: datetime = Form(...),
        key_areas: str = Form(...),
        attachment: UploadFile = File(...),
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
        background_tasks: BackgroundTasks = BackgroundTasks(),
        auth: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        regulation = NewRegulation(
            name=name,
            issue_date=issue_date,
            key_areas=key_areas,
        )

        regulation_results = await create_new_regulation_model(
            connection=connection,
            regulation=regulation,
            engagement_id=engagement_id
        )


        await add_new_attachment(
            connection=connection,
            attachment=attachment,
            item_id=regulation_results.get("id"),
            module_id=auth.module_id,
            url=upload_attachment(
            category=AttachmentCategory.REGULATION,
            background_tasks=background_tasks,
            file=attachment
            ),
            category=AttachmentCategory.REGULATION
        )



        return await return_checker(
            data=regulation_results,
            passed="Regulation Successfully Created",
            failed="Failed Creating  Regulation"
        )



@router.put("/context/regulations/{regulation_id}", response_model=ResponseMessage)
async def update_engagement_regulation(
        regulation_id: str,
        name: str = Form(...),
        issue_date: datetime = Form(...),
        key_areas: str = Form(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        regulation = UpdateRegulation(
            name=name,
            issue_date=issue_date,
            key_areas=key_areas,
        )

        results = await update_engagement_regulation_model(
            connection=connection,
            regulation=regulation,
            regulation_id=regulation_id

        )

        return await return_checker(
            data=results,
            passed="Regulation Successfully Updated",
            failed="Failed Updating  Regulation"
        )



@router.get("/context/regulations/{engagement_id}")
async def get_engagement_regulations(
        engagement_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_engagement_regulations_model(
            connection=connection,
            engagement_id=engagement_id
        )

        return data



@router.get("/context/regulations/single/{regulation_id}")
async def get_single_engagement_regulation(
        regulation_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_single_engagement_regulation_model(
            connection=connection,
            regulation_id=regulation_id
        )

        if data is None:
            raise HTTPException(status_code=404, detail="Regulation Not Found")

        return data




@router.delete("/context/regulations/{regulation_id}")
async def delete_single_engagement_regulation(
        regulation_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await delete_engagement_regulation_model(
            connection=connection,
            regulation_id=regulation_id
        )

        return await return_checker(
            data=results,
            passed="Regulation Successfully Deleted",
            failed="Failed Deleting  Regulation"
        )


