from fastapi import APIRouter, Depends, HTTPException, Query

from models.libray_models import create_new_libray_entry_model
from models.sub_program_models import create_new_sub_program_model, fetch_all_sub_program_model, \
    fetch_single_sub_program_model, update_sub_program_model, delete_sub_program_model, export_sub_program_to_lib_model
from schema import ResponseMessage, CurrentUser
from schemas.library_schemas import LibraryCategory
from schemas.sub_program_schemas import UpdateSubProgram, NewSubProgram
from services.connections.postgres.connections import AsyncDBPoolSingleton
from services.security.security import get_current_user
from utils import exception_response, return_checker

router = APIRouter(prefix="/engagements")


@router.post("/sub_program/{program_id}", status_code=201, response_model=ResponseMessage)
async def create_new_sub_program(
        program_id: str,
        sub_program: NewSubProgram,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        auth: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        results = await create_new_sub_program_model(
            connection=connection,
            sub_program=sub_program,
            program_id=program_id,
            module_id=auth.module_id
        )

        return await return_checker(
            data=results,
            passed="Sub Program Successfully Created",
            failed="Failed Creating  Sub Program"
        )


@router.get("/sub_program/{program_id}")
async def fetch_all_sub_program(
        program_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await fetch_all_sub_program_model(
            connection=connection,
            program_id=program_id
        )
        return data


@router.get("/sub_program/single/{sub_program_id}")
async def fetch_single_sub_program(
        sub_program_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await fetch_single_sub_program_model(
            connection=connection,
            sub_program_id=sub_program_id
        )

        if data is None:
            raise HTTPException(status_code=404, detail="Sub Program Not Found")
        return data


@router.put("/sub_program/{sub_program_id}", response_model=ResponseMessage)
async def update_sub_program(
        sub_program_id: str,
        sub_program: UpdateSubProgram,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await update_sub_program_model(
            connection=connection,
            sub_program=sub_program,
            sub_program_id=sub_program_id
        )

        return await return_checker(
            data=results,
            passed="Sub Program Successfully Updated",
            failed="Failed Updating  Sub Program"
        )



@router.delete("/sub_program/{sub_program_id}", response_model=ResponseMessage)
async def delete_sub_program(
        sub_program_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await delete_sub_program_model(
            connection=connection,
            sub_program_id=sub_program_id
        )

        return await return_checker(
            data=results,
            passed="Sub Program Successfully Deleted",
            failed="Failed Deleting  Sub Program"
        )


@router.post("/sub_program/export/{sub_program_id}", response_model=ResponseMessage)
async def export_sub_program_to_lib(
        sub_program_id: str,
        module_id: str = Query(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        library = await export_sub_program_to_lib_model(
            connection=connection,
            sub_program_id=sub_program_id
        )

        results = await create_new_libray_entry_model(
            connection=connection,
            library=library,
            category=LibraryCategory.SUB_PROGRAM,
            module_id=module_id,
            user_id=""
        )


        return await return_checker(
            data=results,
            passed="Sub Program Successfully Exported",
            failed="Failed Exporting  Sub Program"
        )
