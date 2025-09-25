from psycopg import AsyncConnection
from core.tables import Tables
from schemas.risk_contol_schemas import RiskControlColumns, NewRiskControl, UpdateRiskControl
from services.connections.postgres.read import ReadBuilder
from utils import exception_response



async def create_new_risk_control_on_sub_program_model(
        connection: AsyncConnection,
        risk_control: NewRiskControl,
        sub_program_id: str
):
    with exception_response():
        pass


async def fetch_all_risk_control_on_sub_program_model(
        connection: AsyncConnection,
        sub_program_id: str
):
    with exception_response():
        pass


async def fetch_single_risk_control_on_sub_program_model(connection: AsyncConnection, risk_control_id: str):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.RISK_CONTROL.value)
            .where(RiskControlColumns.ID, risk_control_id)
            .fetch_one()
        )
        return builder


async def edit_risk_control_on_sub_program_model(
        connection: AsyncConnection,
        risk_control: UpdateRiskControl,
        risk_control_id: str
):
    with exception_response():
        pass


async def delete_risk_control_on_sub_program_model(
        connection: AsyncConnection,
        risk_control_id: str
):
    with exception_response():
        pass

