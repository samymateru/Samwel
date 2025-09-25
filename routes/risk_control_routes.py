from fastapi import APIRouter, Depends
from schema import ResponseMessage
from schemas.risk_contol_schemas import NewRiskControl
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response

router = APIRouter(prefix="/risk_controls")

@router.post("/{sub_program_id}", status_code=201, response_model=ResponseMessage)
async def create_new_risk_control_on_sub_program(
        entity: NewRiskControl,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass


@router.get("/{sub_program_id}")
async def fetch_all_risk_control_on_sub_program(
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass


@router.get("/single/{sub_program_id}")
async def fetch_single_risk_control_on_sub_program(
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass


@router.put("/{risk_control_id}")
async def edit_risk_control_on_sub_program(
        risk_control_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass


@router.delete("/{risk_control_id}")
async def delete_risk_control_on_sub_program(
        risk_control_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass