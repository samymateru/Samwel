from fastapi import HTTPException
from psycopg import AsyncConnection
from AuditNew.Internal.engagements.administration.databases import get_business_contacts
from core.tables import Tables
from models.engagement_administration_profile_models import fetch_engagement_administration_profile_model
from models.engagement_models import get_single_engagement_details
from models.engagement_staff_models import fetch_engagement_staff_model
from models.organization_models import get_module_organization
from reports.schemas.engagement_report_schemas import EngagementReportSchema, ReportLead, BusinessContacts
from schemas.engagement_administration_profile_schemas import \
    NewEngagementAdministrationProfile
from schemas.user_schemas import UserColumns
from services.connections.postgres.read import ReadBuilder
from services.logging.logger import global_logger
from utils import exception_response


async def get_engagement_report_details(
        connection: AsyncConnection,
        engagement_id: str
):
    with exception_response():
        engagement_data = await get_single_engagement_details(
            connection=connection,
            engagement_id=engagement_id
        )


        if engagement_data is None:
            global_logger.exception("Engagement Not Found")
            raise HTTPException(status_code=404, detail="Engagement Not Found")




        organization_data = await get_module_organization(
            connection=connection,
            module_id=engagement_data.get("module_id")
        )

        if organization_data is None:
            global_logger.exception("Organization Not Found")
            raise HTTPException(status_code=404, detail="Organization Not Found")




        engagement_profile_data = await fetch_engagement_administration_profile_model(
            connection=connection,
            engagement_id=engagement_id
        )


        if engagement_profile_data is None:
            global_logger.exception("Engagement Profile Not Found")
            raise HTTPException(status_code=404, detail="Engagement Profile Not Found")


        profile = NewEngagementAdministrationProfile(**engagement_profile_data)




        engagement_leads_data = await fetch_engagement_staff_model(
            connection=connection,
            engagement_id=engagement_id,
        )

        leads = [ReportLead(**item) for item in engagement_leads_data]




        business_contact_data = await get_business_contacts(
            connection=connection,
            engagement_id=engagement_id
        )


        if business_contact_data.__len__() < 2:
            raise HTTPException(status_code=404, detail="Business Contacts Not Found")

        business_contacts = []


        for user in business_contact_data[0]["user"] + business_contact_data[1]["user"]:
            data = await (
                ReadBuilder(connection=connection)
                .from_table(Tables.USERS.value, alias="usr")
                .join(
                    "LEFT",
                    Tables.MODULES_USERS.value,
                    "mod_usr.user_id = usr.id",
                    "mod_usr",
                    use_prefix=False
                )
                .where("usr."+UserColumns.EMAIL.value, user.get("email"))
                .fetch_one()
            )

            business_contacts.append(BusinessContacts(**data))


        data = EngagementReportSchema(
            engagement_id=engagement_data.get("id"),
            module_id=engagement_data.get("name"),
            organization_name=organization_data.get("name"),
            engagement_name=engagement_data.get("name"),
            engagement_code=engagement_data.get("code"),
            engagement_type=engagement_data.get("type"),
            engagement_opinion_rating=engagement_data.get("opinion_rating"),
            engagement_opinion_conclusion=engagement_data.get("opinion_conclusion"),
            engagement_risk_maturity_rating=engagement_data.get("risk_maturity_rating"),
            engagement_profile=profile,
            engagement_leads=leads,
            engagement_business_contacts=business_contacts
        )

        return  data





