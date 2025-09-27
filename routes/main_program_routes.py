from fastapi import APIRouter, Depends, Query, HTTPException

from models.libray_models import create_new_libray_entry_model, get_module_library_entry_items
from models.main_program_models import create_new_main_audit_program_model, export_main_audit_program_to_library_model, \
    fetch_main_programs_models, update_main_audit_program_models, \
    update_main_audit_program_process_rating_model, delete_main_audit_program_model, \
    import_main_audit_program_to_library_model
from schema import ResponseMessage, CurrentUser
from schemas.library_schemas import LibraryCategory, ImportLibraryItems
from schemas.main_program_schemas import NewMainProgram, UpdateMainProgram, UpdateMainProgramProcessRating
from services.connections.postgres.connections import AsyncDBPoolSingleton
from services.security.security import get_current_user
from utils import exception_response, return_checker

router = APIRouter(prefix="/engagements")

@router.post("/main_program/{engagement_id}", status_code=201, response_model=ResponseMessage)
async def create_new_main_audit_program(
        engagement_id: str,
        main_program: NewMainProgram,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await create_new_main_audit_program_model(
            connection=connection,
            main_program=main_program,
            engagement_id=engagement_id
        )

        return await return_checker(
            data=results,
            passed="Main Program Successfully Created",
            failed="Failed Creating  Main Program"
        )


@router.post("/main_program/export/{program_id}", response_model=ResponseMessage)
async def export_main_audit_program_to_library(
        program_id: str,
        module_id: str = Query(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        library = await export_main_audit_program_to_library_model(
            connection=connection,
            program_id=program_id
        )

        results = await create_new_libray_entry_model(
            connection=connection,
            library=library,
            category=LibraryCategory.MAIN_PROGRAM,
            module_id=module_id,
            user_id=""
        )

        return await return_checker(
            data=results,
            passed="Main Program Successfully Exported",
            failed="Failed Exporting  Main Program"
        )




@router.post("/main_program/import/{engagement_id}", response_model=ResponseMessage)
async def import_main_audit_program_to_engagement(
        engagement_id: str,
        library_ids: ImportLibraryItems,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        auth: CurrentUser = Depends(get_current_user)
):
    with exception_response():

        main_programs = await get_module_library_entry_items(
            connection=connection,
            library_ids=library_ids.library_ids,
            category=LibraryCategory.MAIN_PROGRAM
        )


        for main_program in main_programs:
            results = await import_main_audit_program_to_library_model(
                connection=connection,
                engagement_id=engagement_id,
                main_program=main_program.get("data"),
                module_id=auth.module_id
            )

            if results is None:
                raise HTTPException(status_code=400, detail="Error Occurred While Import Main Program, Attach Sub Program Failed")


        return await return_checker(
            data=True,
            passed="Main Program Successfully Imported",
            failed="Failed Importing  Main Program"
        )





@router.get("/main_program/{engagement_id}")
async def fetch_all_main_programs(
        engagement_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await fetch_main_programs_models(
            connection=connection,
            engagement_id=engagement_id
        )
        return data


@router.put("/main_program/{program_id}", response_model=ResponseMessage)
async def update_main_audit_program(
        program_id: str,
        main_program: UpdateMainProgram,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await update_main_audit_program_models(
            connection=connection,
            main_program=main_program,
            program_id=program_id
        )

        return await return_checker(
            data=results,
            passed="Main Program Successfully Updated",
            failed="Failed Updating  Main Program"
        )


@router.put("/main_program/process_rating/{program_id}", response_model=ResponseMessage)
async def update_main_audit_program_process_rating(
        program_id: str,
        main_program: UpdateMainProgramProcessRating,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await update_main_audit_program_process_rating_model(
            connection=connection,
            main_program=main_program,
            program_id=program_id
        )

        return await return_checker(
            data=results,
            passed="Main Program Process Rating Successfully Updated",
            failed="Failed Updating  Main Program Process Rating"
        )



@router.delete("/main_program/{program_id}", response_model=ResponseMessage)
async def delete_main_audit_program(
        program_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await delete_main_audit_program_model(
            connection=connection,
            program_id=program_id
        )

        return await return_checker(
            data=results,
            passed="Main Program Successfully Deleted",
            failed="Failed Deleting  Main Program"
        )
