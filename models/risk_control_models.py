from typing import List

from fastapi import HTTPException
from psycopg import AsyncConnection
from core.tables import Tables
from models.libray_models import get_module_library_entry_items
from schemas.library_schemas import LibraryCategory, ImportLibraryItems
from schemas.risk_contol_schemas import RiskControlColumns, NewRiskControl, UpdateRiskControl, CreateRiskControl
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response, get_unique_key
from datetime import datetime
from core.queries import risk_control_fetch

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
            residue_risk=risk_control.residue_risk,
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


async def export_risk_control_to_library_model(
        connection: AsyncConnection,
        risk_control_id: str
):
    with exception_response():
        async with connection.cursor() as cursor:
            await cursor.execute(risk_control_fetch, (risk_control_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            result = [dict(zip(column_names, row)) for row in rows]
            return result[0]



async def import_risk_control_from_library_model(
        connection: AsyncConnection,
        risk_controls: List,
        sub_program_id: str
):
    with exception_response():

        for risk_control in risk_controls:
            __risk_control__ = NewRiskControl(
                risk=risk_control.get("data").get("risk") or "",
                risk_rating=risk_control.get("data").get("risk_rating") or "",
                control=risk_control.get("data").get("control") or "",
                control_type=risk_control.get("data").get("control_type") or "",
                control_objective=risk_control.get("data").get("risk_rating") or "",
                residue_risk=risk_control.get("data").get("residue_risk") or ""
            )


            results = await create_new_risk_control_on_sub_program_model(
                connection=connection,
                risk_control=__risk_control__,
                sub_program_id=sub_program_id
            )

            if results is None:
                raise HTTPException(status_code=400, detail="Error Occurred While Importing Risk Control")

        return True