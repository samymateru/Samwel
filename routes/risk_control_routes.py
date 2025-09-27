from fastapi import APIRouter, Depends, HTTPException, Query

from models.libray_models import create_new_libray_entry_model, get_module_library_entry_items
from models.risk_control_models import create_new_risk_control_on_sub_program_model, \
    fetch_all_risk_control_on_sub_program_model, fetch_single_risk_control_on_sub_program_model, \
    edit_risk_control_on_sub_program_model, delete_risk_control_on_sub_program_model, \
    export_risk_control_to_library_model, import_risk_control_from_library_model
from schema import ResponseMessage
from schemas.library_schemas import LibraryCategory, ImportLibraryItems
from schemas.risk_contol_schemas import NewRiskControl, UpdateRiskControl
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response, return_checker

router = APIRouter(prefix="/risk_controls")

@router.post("/{sub_program_id}", status_code=201, response_model=ResponseMessage)
async def create_new_risk_control_on_sub_program(
        risk_control: NewRiskControl,
        sub_program_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await create_new_risk_control_on_sub_program_model(
            connection=connection,
            risk_control=risk_control,
            sub_program_id=sub_program_id
        )

        return await return_checker(
            data=results,
            passed="Risk Control Successfully Created",
            failed="Failed Creating  Risk Control"
        )


@router.get("/{sub_program_id}")
async def fetch_all_risk_control_on_sub_program(
        sub_program_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await fetch_all_risk_control_on_sub_program_model(
            connection=connection,
            sub_program_id=sub_program_id
        )
        return data


@router.get("/single/{risk_control_id}")
async def fetch_single_risk_control_on_sub_program(
        risk_control_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await fetch_single_risk_control_on_sub_program_model(
            connection=connection,
            risk_control_id=risk_control_id
        )

        if data is None:
            raise HTTPException(status_code=404, detail="Risk Control Not Found")
        return data


@router.put("/{risk_control_id}")
async def edit_risk_control_on_sub_program(
        risk_control_id: str,
        risk_control: UpdateRiskControl,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await edit_risk_control_on_sub_program_model(
            connection=connection,
            risk_control=risk_control,
            risk_control_id=risk_control_id
        )

        return await return_checker(
            data=results,
            passed="Risk Control Successfully Updated",
            failed="Failed Updating  Risk Control"
        )


@router.delete("/{risk_control_id}")
async def delete_risk_control_on_sub_program(
        risk_control_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await delete_risk_control_on_sub_program_model(
            connection=connection,
            risk_control_id=risk_control_id
        )

        return await return_checker(
            data=results,
            passed="Risk Control Successfully Deleted",
            failed="Failed Deleting  Risk Control"
        )



@router.post("/export/{risk_control_id}")
async def export_risk_control_to_library(
        risk_control_id: str,
        module_id: str = Query(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        library = await export_risk_control_to_library_model(
            connection=connection,
            risk_control_id=risk_control_id
        )

        results = await create_new_libray_entry_model(
            connection=connection,
            library=library,
            category=LibraryCategory.RISK_CONTROL,
            module_id=module_id,
            user_id=""
        )

        return await return_checker(
            data=results,
            passed="Risk Control Successfully Exported",
            failed="Failed Exporting Risk Control"
        )





@router.post("/import/{sub_program_id}")
async def import_risk_control_to_sub_program(
        sub_program_id: str,
        library_ids: ImportLibraryItems,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        risk_controls = await get_module_library_entry_items(
            connection=connection,
            library_ids=library_ids.library_ids,
            category=LibraryCategory.RISK_CONTROL
        )

        if risk_controls.__len__() == 0:
            raise HTTPException(status_code=404, detail="Risk Control Item Not Found In Library")


        results = await import_risk_control_from_library_model(
            connection=connection,
            risk_controls=risk_controls,
            sub_program_id=sub_program_id
        )

        return await return_checker(
            data=results,
            passed="Risk Control Successfully Imported",
            failed="Failed Importing Risk Control"
        )




