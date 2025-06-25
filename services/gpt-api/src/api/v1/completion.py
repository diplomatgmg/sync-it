from common.logger import get_logger
from fastapi import APIRouter, HTTPException
from schemas import PromptRequest, PromptResponse
from service import get_gpt_response


logger = get_logger(__name__)


router = APIRouter()


@router.post("/completion")
async def completion(request: PromptRequest) -> PromptResponse:
    try:
        response_text = await get_gpt_response(request.prompt)
        return PromptResponse(message=response_text)
    except Exception as e:
        logger.exception("Failed to get GPT response", exc_info=e)
        raise HTTPException(status_code=500, detail=str(e)) from e
