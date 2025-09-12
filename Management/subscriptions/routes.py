from typing import List
from fastapi import APIRouter, Depends, HTTPException
from Management.subscriptions.schemas import EAuditLicence
from core.constants import licences

router = APIRouter(prefix="/subscriptions")

@router.get("/", response_model=List[EAuditLicence])
async def fetch_subscription():
    try:
        return licences
    except Exception as e:
        raise HTTPException(status_code=400, detail="System Error")