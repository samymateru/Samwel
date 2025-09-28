from fastapi import APIRouter, Depends, Query, HTTPException

from models.libray_models import get_module_library_entry_model
from schemas.library_schemas import LibraryCategory, MainProgramLibraryItem, SubProgramLibraryItem, \
    RiskControlLibraryItem
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response

router = APIRouter(prefix="/library")


@router.put("/main_program/{library_id}")
async def update_main_program_library_item(
        library_id: str,
        item: MainProgramLibraryItem,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass


@router.put("/sub_program/{library_id}")
async def update_sub_program_library_item(
        library_id: str,
        item: SubProgramLibraryItem,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass




@router.put("/risk_control/{library_id}")
async def update_risk_control_library_item(
        library_id: str,
        item: RiskControlLibraryItem,
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

        return data



@router.get("/{libray_item_id}")
async def fetch_single_library_item(
        libray_item_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass


