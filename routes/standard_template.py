from fastapi import Depends, APIRouter
from schema import ResponseMessage
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response



router = APIRouter(prefix="/engagements")
@router.post("/{sub_program_id}", status_code=201, response_model=ResponseMessage)
async def create_(
        risk_control: NewRiskControl,
        sub_program_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
