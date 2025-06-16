from seedings import *
from utils import get_async_db_connection
from AuditNew.Internal.engagements.administration.databases import add_new_business_contact

async def set_company_profile(company_id: str):
    async for connection in get_async_db_connection():
        await risk_rating(connection=connection, company=company_id)
        await engagement_types(company=company_id, connection=connection)
        await issue_finding_source(connection=connection, company=company_id)
        await control_effectiveness_rating(connection=connection, company=company_id)
        await control_weakness_rating(connection=connection, company=company_id)
        await audit_opinion_rating(connection=connection, company=company_id)
        await risk_maturity_rating(connection=connection, company=company_id)
        await control_type(connection=connection, company=company_id)
        await roles(connection=connection, company=company_id)
        await business_process(connection=connection, company=company_id)
        await impact_category(connection=connection, company=company_id)
        await root_cause_category(connection=connection, company=company_id)
        await risk_category(connection=connection, company=company_id)

async def set_engagement_templates(engagement_id: str):
    async for connection in get_async_db_connection():
        await planning_procedures(connection=connection, engagement_id=engagement_id)
        await finalization_procedures(connection=connection, engagement_id=engagement_id)
        await reporting_procedures(connection=connection, engagement_id=engagement_id)
        await add_engagement_profile(connection=connection, engagement_id=engagement_id)
        await add_new_business_contact(connection=connection, engagement_id=engagement_id)
        await engagement_letter(connection=connection, engagement_id=engagement_id)

