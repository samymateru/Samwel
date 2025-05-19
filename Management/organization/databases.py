from psycopg import AsyncConnection, sql
from utils import get_unique_key
from Management.organization.schemas import *
from fastapi import HTTPException

async def new_organization(connection: AsyncConnection, organization: Organization, company_id: str):
    pass

async def update_organization(connection: AsyncConnection, organization: Organization, organization_id: str):
    pass

async def fetch_organization(connection: AsyncConnection, company_id: str):
    pass