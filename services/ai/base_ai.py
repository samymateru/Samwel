from fastapi import APIRouter, HTTPException, Depends, Query
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

from starlette.responses import StreamingResponse

from models.user_models import get_entity_user_details_by_mail, update_user_ai_session
from services.connections.postgres.connections import AsyncDBPoolSingleton
from services.logging.logger import global_logger
from utils import exception_response
from enum import Enum


load_dotenv()

PROMPT_ID = "pmpt_68dff1e1b0508190aad7968097707e580ca0b5c943f846d1"
PROMPT_VERSION = "1"  # Keep this aligned with your template version in dashboard
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter(prefix="/ai")

class Mode(str, Enum):
    NORMAL = "normal"
    AUDIT = "audit"


MAX_INPUT_WORDS = 1500
MAX_OUTPUT_TOKENS = 500
USER_MONTHLY_LIMIT = 100000

@router.get("/chat")
async def chat(
    user_input: str,
    mode: Mode = Query(...),
    connection=Depends(AsyncDBPoolSingleton.get_db_connection)
):
    """
    Generate an audit report using a saved OpenAI Prompt template.
    """
    with exception_response():
        if len(user_input) > MAX_INPUT_WORDS:
            raise HTTPException(status_code=405, detail="To Many Words You Pass The Maximum 1500")

        data = await get_entity_user_details_by_mail(
            connection=connection,
            email="cornely@gmail.com"
        )

        if data is None:
            raise HTTPException(status_code=404, detail="User Not Found")


        new_session_count = int(data.get("ai_session_count")) + len(user_input.split())


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

        if mode == Mode.AUDIT:
            response = await client.responses.create(
                model="gpt-4.1-mini",  # Or another supported model
                prompt={
                    "id": PROMPT_ID,
                    "version": PROMPT_VERSION,
                    "variables": {
                        "user_input": user_input
                    }
                }
            )

            # Extract model output
            result = getattr(response, "output_text", None)
            if not result:
                raise HTTPException(status_code=500, detail="No output generated from model")

            return result

        else:
            async def event_stream():
                stream = await client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": user_input}],
                    stream=True,
                )
                async for event in stream:
                    if event.choices[0].delta.content:
                        yield event.choices[0].delta.content

            return StreamingResponse(event_stream(), media_type="text/plain")


