from fastapi import APIRouter, HTTPException

from app.api.schemas import ChatRequest, ChatResponse
from app.agents.graph import run_agent

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        result = await run_agent(request.user_input, request.user_id)
        return ChatResponse(
            emotion_analysis=result.get("emotion_analysis"),
            diary_entry_id=result["diary_entry"].id if result.get("diary_entry") else None,
            response=result.get("response", ""),
            intent=result.get("intent", ""),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
