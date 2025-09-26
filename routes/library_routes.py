from fastapi import APIRouter, Depends, Query, HTTPException

from models.libray_models import get_module_library_entry_model
from schemas.library_schemas import LibraryCategory
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


@router.get("/{module_id}")
async def fetch_all_library_items(
        module_id: str,
        category: LibraryCategory = Query(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_module_library_entry_model(
            connection=connection,
            module_id=module_id,
            category=category
        )

        if data.__len__() == 0:
            raise HTTPException(status_code=404, detail="Library Is Empty")

        return data[0]


@router.get("/{libray_item_id}")
async def fetch_single_library_item(
        libray_item_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass


