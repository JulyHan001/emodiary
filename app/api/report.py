from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_report():
    return {"message": "report endpoint placeholder"}
