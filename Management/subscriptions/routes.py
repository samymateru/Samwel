from typing import List
from fastapi import APIRouter, Depends, HTTPException
from Management.subscriptions.schemas import EAuditLicence
from core.constants import licences, plans

router = APIRouter(prefix="/subscriptions")

@router.get("/", response_model=List[EAuditLicence])
async def fetch_subscriptions():
    try:
        return licences
    except Exception as e:
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
    except Exception as e:
        raise HTTPException(status_code=400, detail="System Error")