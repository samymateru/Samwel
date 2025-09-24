from psycopg import AsyncConnection
from core.tables import Tables
from schemas.risk_contol_schemas import RiskControlColumns
from services.connections.postgres.read import ReadBuilder
from utils import exception_response


async def get_all_risk_controls(connection: AsyncConnection, sub_program_id: str):
    with exception_response():
        pass


async def get_single_risk_control(connection: AsyncConnection, risk_control_id: str):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.RISK_CONTROL.value)
            .where(RiskControlColumns.ID, risk_control_id)
            .fetch_one()
        )
        print(builder)

async def add_new_risk_control(connection: AsyncConnection, sub_program_id: str):
    with exception_response():
        pass

