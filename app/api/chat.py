from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def chat_endpoint():
    return {"message": "chat endpoint placeholder"}
