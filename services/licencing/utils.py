from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import asyncio
_lock = asyncio.Lock()

class LicenceCache(BaseModel):
    checked_at: Optional[datetime]
    valid: bool
    reason: str


licence_cache = LicenceCache(
    checked_at=None,
    valid=False,
    reason="Not validated"
)


async def check_license_validity_cached(ttl_seconds=300):
    now = datetime.now()
    async with _lock:
        if licence_cache.checked_at and (now - licence_cache.checked_at).total_seconds() < ttl_seconds:
            return licence_cache.valid, licence_cache.reason

        valid, reason = verify_licence()
        licence_cache.model_update({
            "checked_at": now,
            "valid": valid,
            "reason": reason
        })
        return valid, reason



async def verify_licence() -> tuple[bool, str]:
    # Replace with your own logic:
    #   - read license file from disk
    #   - validate signature or hash
    #   - check expiry date
    #   - optionally verify with remote server (cached)
    valid = True
    reason = "OK"

    # Example of an expired license:
    # valid = False
    # reason = "License expired"

    return valid, reason