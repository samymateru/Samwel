from fastapi import APIRouter, Depends, Query
from models.libray_models import get_module_library_entry_model, update_main_program_library_model, \
    update_sub_program_library_model, update_risk_control_library_model, create_new_libray_entry_model, \
    delete_libray_entry_model
from schemas.library_schemas import LibraryCategory, MainProgramLibraryItem, SubProgramLibraryItem, \
    RiskControlLibraryItem, WorkingPapers
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
        risk_control: RiskControlLibraryItem,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await update_risk_control_library_model(
            connection=connection,
            risk_control=risk_control,
            library_id=library_id,
        )

        return await return_checker(
            data=results,
            passed="Risk Control Successfully Updated",
            failed="Failed Updating Risk Control"
        )



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



@router.post("/working_papers/{module_id}")
async def add_new_working_paper(
        module_id: str,
        working_paper: WorkingPapers,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await create_new_libray_entry_model(
            connection=connection,
            module_id=module_id,
            user_id="",
            library=working_paper.model_dump(),
            category=LibraryCategory.WORKING_PAPER
        )

        return await return_checker(
            data=results,
            passed="Working Paper Successfully Created",
            failed="Failed Creating Working Paper"
        )




@router.delete("/{library_id}")
async def deleting_library_item(
        library_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await delete_libray_entry_model(
            connection=connection,
            library_id=library_id
        )


        return await return_checker(
            data=results,
            passed="Working Paper Successfully Deleted",
            failed="Failed Deleting Working Paper"
        )








@router.get("/reports/{module_id}")
async def fetch_reports(
        module_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass



@router.get("/reports/{report_id}")
async def deleting_library_item(
        report_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass