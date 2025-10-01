from fastapi import Depends, APIRouter
from models.standard_template_models import create_new_standard_template_model, delete_standard_template_model, \
    read_standard_template_model, update_standard_template_model
from schema import ResponseMessage
from schemas.standard_template_schemas import NewStandardTemplate, ProcedureTypes, UpdateStandardProcedure
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response, return_checker

router = APIRouter(prefix="/engagements")

@router.post("/{engagement_id}", status_code=201, response_model=ResponseMessage)
async def create_standard_procedure(
        procedure: NewStandardTemplate,
        engagement_id: str,
        type_: ProcedureTypes,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await create_new_standard_template_model(
            connection=connection,
            procedure=procedure,
            type_=type_,
            engagement_id=engagement_id
        )

        return await return_checker(
            data=results,
            passed=f"Procedure in {type_.value} Successfully Added",
            failed=f"Failed Adding  Procedure {type_.value}"
        )



@router.get("/{engagement_id}")
async def get_standard_standard_procedure(
        engagement_id: str,
        type_: ProcedureTypes,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await read_standard_template_model(
            connection=connection,
            type_=type_,
            engagement_id=engagement_id
        )

        return data





@router.put("/{procedure_id}")
async def update_standard_standard_procedure(
        procedure_id: str,
        procedure: UpdateStandardProcedure,
        type_: ProcedureTypes,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await update_standard_template_model(
            connection=connection,
            type_=type_,
            procedure=procedure,
            procedure_id=procedure_id
        )

        return await return_checker(
            data=results,
            passed=f"Procedure in {type_.value} Successfully Updated",
            failed=f"Failed Updating  Procedure {type_.value}"
        )




@router.delete("/{procedure_id}")
async def delete_standard_standard_procedure(
        procedure_id: str,
        type_: ProcedureTypes,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await delete_standard_template_model(
            connection=connection,
            procedure_id=procedure_id,
            type_=type_,
        )

        return await return_checker(
            data=results,
            passed=f"Procedure in {type_.value} Successfully Deleted",
            failed=f"Failed Deleting  Procedure {type_.value}"
        )
