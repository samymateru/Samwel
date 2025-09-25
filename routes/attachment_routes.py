from fastapi import APIRouter, Depends, UploadFile, File

from schema import ResponseMessage
from schemas.attachement_schemas import AttachmentCategory
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response

router = APIRouter(prefix="/attachments")


@router.post("/{section_id}", response_model=ResponseMessage)
async def add_category_attachment(
        section_id: str,
        category: AttachmentCategory,
        attachment: UploadFile = File(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass
    