from datetime import datetime
from psycopg import AsyncConnection

from models.attachment_model import fetch_item_attachment
from models.engagement_models import get_single_engagement_details, register_new_engagement
from models.policy_models import get_single_engagement_policy_model, get_engagement_policies_model
from schemas.attachement_schemas import AttachmentCategory
from schemas.engagement_schemas import EngagementStatus, EngagementStage, CreateEngagement, NewEngagement, Risk
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

        attachment_data = await fetch_item_attachment(
            connection=connection,
            category=AttachmentCategory.POLICY,
            item_id=get_policy_data.get("id")
        )

        data = engagement_data.copy()






