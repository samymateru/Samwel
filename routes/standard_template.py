from fastapi import Depends, APIRouter
from schema import ResponseMessage
from schemas.standard_template_schemas import NewStandardTemplate, ProcedureTypes, UpdateStandardProcedure
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response



router = APIRouter(prefix="/engagements")

@router.post("/{engagement_id}", status_code=201, response_model=ResponseMessage)
async def create_standard_procedure(
        procedure: NewStandardTemplate,
        engagement_id: str,
        type_: ProcedureTypes,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass


@router.get("/{engagement_id}")
async def get_standard_standard_procedure(
        engagement_id: str,
        type_: ProcedureTypes,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass



@router.put("/{procedure_id}")
async def update_standard_standard_procedure(
        procedure_id: str,
        procedure: UpdateStandardProcedure,
        type_: ProcedureTypes,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass



@router.delete("/{procedure_id}")
async def delete_standard_standard_procedure(
        procedure_id: str,
        type_: ProcedureTypes,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass