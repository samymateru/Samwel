from psycopg import AsyncConnection
from core.tables import Tables
from schemas.risk_contol_schemas import RiskControlColumns, NewRiskControl, UpdateRiskControl, CreateRiskControl
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response, get_unique_key
from datetime import datetime

async def create_new_risk_control_on_sub_program_model(
        connection: AsyncConnection,
        risk_control: NewRiskControl,
        sub_program_id: str
):
    with exception_response():
        __risk_control__ = CreateRiskControl(
            id=get_unique_key(),
            summary_audit_program=sub_program_id,
            risk=risk_control.risk,
            risk_rating=risk_control.risk_rating,
            control=risk_control.control,
            control_objective=risk_control.control_objective,
            control_type=risk_control.control_type,
            residual_risk=risk_control.residual_risk,
            created_at=datetime.now(),
            type="Program"
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.RISK_CONTROL.value)
            .values(__risk_control__)
            .check_exists({RiskControlColumns.RISK.value: risk_control.risk})
            .check_exists({RiskControlColumns.CONTROL.value: risk_control.control})
            .check_exists({RiskControlColumns.SUMMARY_AUDIT_PROGRAM.value: sub_program_id})
            .returning(RiskControlColumns.ID.value)
            .execute()
        )

        return builder


async def fetch_all_risk_control_on_sub_program_model(
        connection: AsyncConnection,
        sub_program_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.RISK_CONTROL.value)
            .where(RiskControlColumns.SUMMARY_AUDIT_PROGRAM.value, sub_program_id)
            .fetch_all()
        )
        return builder


async def fetch_single_risk_control_on_sub_program_model(connection: AsyncConnection, risk_control_id: str):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.RISK_CONTROL.value)
            .where(RiskControlColumns.ID.value, risk_control_id)
            .fetch_one()
        )
        return builder


async def edit_risk_control_on_sub_program_model(
        connection: AsyncConnection,
        risk_control: UpdateRiskControl,
        risk_control_id: str
):
    with exception_response():
        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.RISK_CONTROL.value)
            .values(risk_control)
            .check_exists({RiskControlColumns.ID.value: risk_control_id})
            .where({RiskControlColumns.ID.value: risk_control_id})
            .returning(RiskControlColumns.ID.value)
            .execute()
        )

        return builder


async def delete_risk_control_on_sub_program_model(
        connection: AsyncConnection,
        risk_control_id: str
):
    with exception_response():
        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(Tables.RISK_CONTROL.value)
            .check_exists({RiskControlColumns.ID.value: risk_control_id})
            .where({RiskControlColumns.ID.value: risk_control_id})
            .returning(RiskControlColumns.ID.value)
            .execute()
        )

        return builder

