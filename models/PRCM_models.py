from psycopg import AsyncConnection
from core.tables import Tables
from schemas.PRCM_schemas import NewPRCM, CreatePRCM, PRCMColumns, UpdatePRCM, AddToAuditProgram
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response, get_unique_key
from datetime import datetime

async def create_new_prcm_model(
        connection: AsyncConnection,
        prcm: NewPRCM,
        engagement_id: str
):
    with exception_response():
        __prcm__ = CreatePRCM(
            id=get_unique_key(),
            engagement=engagement_id,
            process=prcm.process,
            risk=prcm.risk,
            risk_rating=prcm.risk_rating,
            control=prcm.control,
            control_type=prcm.control_type,
            control_objective=prcm.control_objective,
            residue_risk=prcm.residue_risk,
            created_at=datetime.now(),
            type="Planning"
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.RISK_CONTROL.value)
            .values(__prcm__)
            .check_exists({PRCMColumns.RISK.value: prcm.risk})
            .check_exists({PRCMColumns.CONTROL.value: prcm.control})
            .check_exists({PRCMColumns.ENGAGEMENT.value: engagement_id})
            .returning(PRCMColumns.ID.value)
            .execute()
        )

        return builder



async def get_prcm_model(
        connection: AsyncConnection,
        engagement_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.RISK_CONTROL.value)
            .where(PRCMColumns.ENGAGEMENT.value, engagement_id)
            .fetch_all()
        )

        return builder



async def get_summary_audit_program_model(
        connection: AsyncConnection,
        engagement_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.RISK_CONTROL.value)
            .where_raw(
                "summary_audit_program IS NOT NULL AND engagement = %(engagement_id)s",
                {
                "engagement_id": engagement_id
                }
            )
            .fetch_all()
        )

        return builder



async def update_prcm_model(
        connection: AsyncConnection,
        prcm: UpdatePRCM,
        prcm_id: str
):
    with exception_response():
        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.RISK_CONTROL.value)
            .values(prcm)
            .check_exists({PRCMColumns.ID.value: prcm_id})
            .where({PRCMColumns.ID.value: prcm_id})
            .returning(PRCMColumns.ID.value)
            .execute()
        )

        return builder



async def delete_prcm_model(
        connection: AsyncConnection,
        prcm_id: str
):
    with exception_response():
        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(Tables.RISK_CONTROL.value)
            .check_exists({PRCMColumns.ID.value: prcm_id})
            .where({PRCMColumns.ID.value: prcm_id})
            .returning(PRCMColumns.ID.value)
            .execute()
        )

        return builder




async def add_prcm_to_program_model(
    connection: AsyncConnection,
    sub_program_id: str,
    prcm_id: str
):
    with exception_response():
        __prcm__ = AddToAuditProgram(
            summary_audit_program=sub_program_id
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.RISK_CONTROL.value)
            .values(__prcm__)
            .check_exists({PRCMColumns.ID.value: prcm_id})
            .where({PRCMColumns.ID.value: prcm_id})
            .returning(PRCMColumns.ID.value)
            .execute()
        )

        return builder



async def remove_prcm_to_program_model(
    connection: AsyncConnection,
    prcm_id: str
):
    with exception_response():
        __prcm__ = AddToAuditProgram(
            summary_audit_program=None
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.RISK_CONTROL.value)
            .values(__prcm__)
            .check_exists({PRCMColumns.ID.value: prcm_id})
            .where({PRCMColumns.ID.value: prcm_id})
            .returning(PRCMColumns.ID.value)
            .execute()
        )

        return builder