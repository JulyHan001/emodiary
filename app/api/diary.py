from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_diaries():
    return {"message": "diary endpoint placeholder"}
