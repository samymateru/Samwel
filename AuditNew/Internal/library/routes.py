from fastapi import APIRouter, Depends
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response

router = APIRouter(prefix="/library")

@router.post("/{item_id}")
async def created_new_library_item(
        item_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass