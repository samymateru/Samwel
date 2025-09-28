from fastapi import APIRouter, Depends, UploadFile, File, Query, BackgroundTasks

from core.utils import upload_attachment
from models.attachment_model import add_new_attachment, fetch_item_attachment, remove_attachment
from schema import ResponseMessage, CurrentUser
from schemas.attachement_schemas import AttachmentCategory
from services.connections.postgres.connections import AsyncDBPoolSingleton
from services.connections.postgres.insert import InsertQueryBuilder
from services.security.security import get_current_user
from utils import exception_response, return_checker

router = APIRouter(prefix="/attachment")


@router.post("/{item_id}", response_model=ResponseMessage)
async def add_category_attachment(
        item_id: str,
        category: AttachmentCategory = Query(...),
        attachment: UploadFile = File(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        background_tasks: BackgroundTasks = BackgroundTasks(),
        auth: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        results = await add_new_attachment(
            connection=connection,
            attachment=attachment,
            item_id=item_id,
            module_id=auth.module_id,
            url=upload_attachment(
            category=category,
            background_tasks=background_tasks,
            file=attachment
            ),
            category=category
        )

        return await return_checker(
            data=results,
            passed=f"Attachment From {category}  Successfully Added",
            failed=f"Failed Adding  Attachment From {category}"
        )




@router.get("/{item_id}")
async def fetch_item_attachments(
        item_id: str,
        category: AttachmentCategory = Query(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await fetch_item_attachment(
            connection=connection,
            category=category,
            item_id=item_id
        )

        return data



@router.delete("/{attachment_id}", response_model=ResponseMessage)
async def delete_item_attachments(
        attachment_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await remove_attachment(
            connection=connection,
            attachment_id=attachment_id
        )


        return await return_checker(
            data=results,
            passed=f"Attachment Successfully Deleted",
            failed=f"Failed Deleting Attachment"
        )
