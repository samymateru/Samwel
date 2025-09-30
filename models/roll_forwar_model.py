from datetime import datetime
from fastapi import HTTPException
from psycopg import AsyncConnection
from core.tables import Tables
from models.attachment_model import fetch_item_attachment
from models.engagement_models import get_single_engagement_details, register_new_engagement
from models.policy_models import get_engagement_policies_model, \
    create_new_policy_model
from models.regulation_models import get_engagement_regulations_model, create_new_regulation_model
from schemas.attachement_schemas import AttachmentCategory, CreateAttachment, AttachmentColumns
from schemas.engagement_schemas import EngagementStatus, EngagementStage, NewEngagement, Risk
from schemas.policy_schemas import CreatePolicy
from schemas.regulation_schemas import CreateRegulation
from services.connections.postgres.insert import InsertQueryBuilder
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









