from fastapi import APIRouter, HTTPException
from Management.subscriptions.schemas import EAuditLicence, ReadLicences
from core.constants import eaudit, plans

router = APIRouter(prefix="/subscriptions")

@router.get("/")
async def fetch_subscriptions():
    try:
        return {
            "eAuditNext": eaudit
        }
    except Exception:
        raise HTTPException(status_code=400, detail="System Error")


@router.get("/single/{subscription_id}", response_model=EAuditLicence)
async def fetch_subscriptions(
    subscription_id: str
):
    try:
        licence = plans.get(subscription_id)
        if licence is None:
            raise HTTPException(status_code=400, detail="Unknown Licence")
        return licence
    except Exception:
        raise HTTPException(status_code=400, detail="System Error")