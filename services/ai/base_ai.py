from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from models.user_models import get_entity_user_details_by_mail, update_user_ai_session
from schema import CurrentUser
from services.connections.postgres.connections import AsyncDBPoolSingleton
from services.logging.logger import global_logger
from services.security.security import get_current_user
from utils import exception_response


load_dotenv()

PROMPT_ID = "pmpt_68dff1e1b0508190aad7968097707e580ca0b5c943f846d1"
AGENT_PROMPT_ID = "pmpt_68e06c797b648190a09dfd23c9b2280c0a1f4e65171cafb4"
NORMAL_PROMPT_ID = "pmpt_68e2067c51d8819495ae4bf53a91b2bd08e384013663abdd"
MAX_INPUT_WORDS = 1500
MAX_OUTPUT_TOKENS = 500
USER_MONTHLY_LIMIT = 100000
PROMPT_VERSION = "1"
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


router = APIRouter(prefix="/ai")


class Variables(BaseModel):
    prompt_version: str
    prompt_id: str
    context: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Flexible context object; may contain varying fields"
    )
    user_input: str



@router.post("/chat")
async def chat(
    chat_request: Variables,
    connection=Depends(AsyncDBPoolSingleton.get_db_connection),
    auth: CurrentUser = Depends(get_current_user)
):
    """
    Generate an audit report using a saved OpenAI Prompt template.
    """
    with exception_response():
        if len(chat_request.user_input) > MAX_INPUT_WORDS:
            raise HTTPException(status_code=405, detail="To Many Words You Pass The Maximum 1500")

        data = await get_entity_user_details_by_mail(
            connection=connection,
            email=auth.user_email
        )

        if data is None:
            raise HTTPException(status_code=404, detail="User Not Found")



        new_session_count = int(data.get("ai_session_count") or 0) + len(chat_request.user_input.split())


        if new_session_count > USER_MONTHLY_LIMIT:
            raise HTTPException(status_code=405, detail="Sorry Maximum Usage Reached")


        results = await update_user_ai_session(
            connection=connection,
            user_id=data.get("id"),
            count=int(new_session_count)
        )

        if results is  None:
            raise HTTPException(status_code=400, detail="Error Occur While Trying To Analyze AI Query")


        global_logger.info("Passed AI Check")

        response = await client.responses.create(
            model="gpt-4.1-mini",  # Or another supported model
            prompt={
                "id": chat_request.prompt_id,
                "version": chat_request.prompt_version,
                "variables": {
                    "user_input": chat_request.user_input,
                    "context": chat_request.context,
                }
            }
        )

        # Extract model output
        result = getattr(response, "output_text", None)
        if not result:
            raise HTTPException(status_code=500, detail="No output generated from model")

        return {
            "message": result,
            "prompt_id": chat_request.prompt_id,
            "prompt_version": chat_request.prompt_version
        }










