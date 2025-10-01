from datetime import datetime
from fastapi import HTTPException
from psycopg import AsyncConnection
from core.tables import Tables
from models.attachment_model import fetch_item_attachment
from models.engagement_administration_profile_models import fetch_engagement_administration_profile_model
from models.engagement_models import get_single_engagement_details, register_new_engagement
from models.engagement_process_models import get_single_engagement_process_model, get_engagement_processes_model, \
    create_engagement_process_model
from models.main_program_models import export_main_audit_program_to_library_model, fetch_main_programs_models, \
    import_main_audit_program_to_library_model
from models.policy_models import get_engagement_policies_model, \
    create_new_policy_model
from models.regulation_models import get_engagement_regulations_model, create_new_regulation_model
from schemas.attachement_schemas import AttachmentCategory, CreateAttachment, AttachmentColumns
from schemas.engagement_administration_profile_schemas import EngagementProfileColumns, \
    CreateEngagementAdministrationProfile
from schemas.engagement_process_schemas import CreateEngagementProcess
from schemas.engagement_schemas import EngagementStatus, EngagementStage, NewEngagement, Risk
from schemas.policy_schemas import CreatePolicy
from schemas.regulation_schemas import CreateRegulation
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from services.logging.logger import global_logger
from utils import exception_response, get_unique_key


async def export_engagement_content_model(
        connection: AsyncConnection,
        engagement_id: str,
        annual_plan_id: str

):
    with exception_response():
        engagement_data = await get_single_engagement_details(
            connection=connection,
            engagement_id=engagement_id
        )

        data = engagement_data.copy()

        data.update({
            "id": get_unique_key(),
            "start_date": datetime.now(),
            "end_date": datetime.now(),
            "created_at": datetime.now(),
            "status": EngagementStatus.PENDING.value,
           "stage": EngagementStage.PENDING,
            "risk": Risk(
                name=engagement_data.get("risk"),
                magnitude=0
            ),
            "leads": [],
            "archived": False
        })


        engagement = NewEngagement(**data)

        results = await register_new_engagement(
            connection=connection,
            engagement=engagement,
            annual_plan_id=annual_plan_id,
            module_id=engagement_data.get("module_id")
        )

        return results




async def roll_policy(
        connection: AsyncConnection,
        previous_engagement_id: str,
        new_engagement_id: str
):
    with exception_response():

        get_policy_data = await get_engagement_policies_model(
            connection=connection,
            engagement_id=previous_engagement_id
        )

        for policy in get_policy_data:

            __policy__ = CreatePolicy(**policy)

            policy_results = await create_new_policy_model(
                connection=connection,
                policy=__policy__,
                engagement_id=new_engagement_id,
                throw=False
            )

            if policy_results is None:
                raise HTTPException(status_code=400, detail="Error While Rolling Policy Cant Create Policy")

            attachment_data = await fetch_item_attachment(
                connection=connection,
                category=AttachmentCategory.POLICY,
                item_id=policy.get("id")
            )


            if attachment_data.__len__() == 0:
                 continue

            data = attachment_data[0].copy()


            data.update({
                "item_id": policy_results.get("id")
            })


            __attachment__ = CreateAttachment(**data)

            await (
                InsertQueryBuilder(connection=connection)
                .into_table(Tables.ATTACHMENTS.value)
                .values(__attachment__)
                .returning(AttachmentColumns.ATTACHMENT_ID.value)
                .execute()
            )

        return True




async def roll_regulation(
        connection: AsyncConnection,
        previous_engagement_id: str,
        new_engagement_id: str
):
    with exception_response():

        get_regulation_data = await get_engagement_regulations_model(
            connection=connection,
            engagement_id=previous_engagement_id
        )

        for regulation in get_regulation_data:

            __regulation__ = CreateRegulation(**regulation)

            regulation_results = await create_new_regulation_model(
                connection=connection,
                regulation=__regulation__,
                engagement_id=new_engagement_id,
                throw=False
            )

            if regulation_results is None:
                raise HTTPException(status_code=400, detail="Error While Rolling Engagement Cant Create Regulation")

            attachment_data = await fetch_item_attachment(
                connection=connection,
                category=AttachmentCategory.POLICY,
                item_id=regulation.get("id")
            )

            if attachment_data.__len__() == 0:
                continue

            data = attachment_data[0].copy()

            data.update({
                "item_id": regulation_results.get("id")
            })

            __attachment__ = CreateAttachment(**data)

            await (
                InsertQueryBuilder(connection=connection)
                .into_table(Tables.ATTACHMENTS.value)
                .values(__attachment__)
                .returning(AttachmentColumns.ATTACHMENT_ID.value)
                .execute()
            )

        return True




async def roll_forward_main_program(
        connection: AsyncConnection,
        previous_engagement_id: str,
        new_engagement_id: str,
        module_id: str
):
    with exception_response():

        main_program_data = await fetch_main_programs_models(
            connection=connection,
            engagement_id=previous_engagement_id
        )

        for program in main_program_data:
            data = await export_main_audit_program_to_library_model(
                connection=connection,
                program_id=program.get("id"),
            )

            await import_main_audit_program_to_library_model(
                connection=connection,
                engagement_id=new_engagement_id,
                module_id=module_id,
                main_program=data
            )




async def engagement_roll_forward_model(
    connection: AsyncConnection,
    engagement_id: str,
    annual_plan: str,
    module_id: str
):
    with exception_response():
        data = await export_engagement_content_model(
            connection=connection,
            engagement_id=engagement_id,
            annual_plan_id=annual_plan
        )

        await engagement_profile_roll(
            connection=connection,
            previous_engagement_id=engagement_id,
            new_engagement_id=data.get("id")
        )


        await roll_policy(
            connection=connection,
            previous_engagement_id=engagement_id,
            new_engagement_id=data.get("id")
        )


        await roll_regulation(
            connection=connection,
            previous_engagement_id=engagement_id,
            new_engagement_id=data.get("id")
        )


        await engagement_process_roll(
            connection=connection,
            previous_engagement_id=engagement_id,
            new_engagement_id=data.get("id")
        )


        await roll_forward_main_program(
            connection=connection,
            previous_engagement_id=engagement_id,
            new_engagement_id=data.get("id"),
            module_id=module_id
        )


        return data




async def engagement_profile_roll(
        connection: AsyncConnection,
        previous_engagement_id: str,
        new_engagement_id: str,
):
    with exception_response():
        profile_data = await fetch_engagement_administration_profile_model(
            connection=connection,
            engagement_id=previous_engagement_id
        )

        data = profile_data.copy()

        data.update({
            "id": get_unique_key(),
            "engagement": new_engagement_id
        })

        profile = CreateEngagementAdministrationProfile(**data)

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.ENGAGEMENT_PROFILE.value)
            .values(profile)
            .check_exists({EngagementProfileColumns.ENGAGEMENT.value: new_engagement_id})
            .returning(EngagementProfileColumns.ID.value)
            .execute()
        )
        return builder



async def engagement_process_roll(
        connection: AsyncConnection,
        previous_engagement_id: str,
        new_engagement_id: str,
):
    with exception_response():
        engagement_process_data = await get_engagement_processes_model(
            connection=connection,
            engagement_id=previous_engagement_id
        )

        for  _engagement_process_ in engagement_process_data:

            data = _engagement_process_.copy()

            data.update({
                "id": get_unique_key(),
                "engagement": new_engagement_id
            })

            engagement_process = CreateEngagementProcess(**data)

            await create_engagement_process_model(
                connection=connection,
                engagement_process=engagement_process,
                engagement_id=new_engagement_id,
                throw=False
            )

        global_logger.info(f"Engagement Process Roll Forwarded to {new_engagement_id}")

        return True











