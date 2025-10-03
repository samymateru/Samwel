from fastapi import APIRouter, HTTPException
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os


load_dotenv()

PROMPT_ID = "pmpt_68dff1e1b0508190aad7968097707e580ca0b5c943f846d1"
PROMPT_VERSION = "1"  # Keep this aligned with your template version in dashboard
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter(prefix="/ai")


@router.get("/chat")
async def chat(
    user_input: str
):
    """
    Generate an audit report using a saved OpenAI Prompt template.
    """
    try:
        response = await client.responses.create(
            model="gpt-4.1-mini",  # Or another supported model
            prompt={
                "id": PROMPT_ID,
                "version": PROMPT_VERSION,
                "variables": {
                    "user_input": user_input  # Inject the real user input
                }
            }
        )

        # Extract model output
        result = getattr(response, "output_text", None)
        if not result:
            raise HTTPException(status_code=500, detail="No output generated from model")

        return {
            "success": True,
            "input": user_input,
            "output": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))