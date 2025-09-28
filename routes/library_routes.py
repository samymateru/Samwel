from fastapi import APIRouter, Depends, Query, HTTPException

from models.libray_models import get_module_library_entry_model, update_main_program_library_model, \
    update_sub_program_library_model
from schemas.library_schemas import LibraryCategory, MainProgramLibraryItem, SubProgramLibraryItem, \
    RiskControlLibraryItem
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response, return_checker

router = APIRouter(prefix="/library")


@router.put("/main_program/{library_id}")
async def update_main_program_library_item(
        library_id: str,
        main_program: MainProgramLibraryItem,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await update_main_program_library_model(
            connection=connection,
            main_program=main_program,
            library_id=library_id
        )

        return await return_checker(
            data=results,
            passed="Main Program  Successfully Updated",
            failed="Failed Updating  Main Program"
        )


@router.put("/sub_program/{library_id}")
async def update_sub_program_library_item(
        library_id: str,
        sub_program: SubProgramLibraryItem,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await update_sub_program_library_model(
            connection=connection,
            sub_program=sub_program,
            library_id=library_id
        )

        return await return_checker(
            data=results,
            passed="Sub Program  Successfully Updated",
            failed="Failed Updating Sub Program"
        )


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


