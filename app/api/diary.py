from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.api.schemas import DiaryListResponse, DiaryEntryResponse
from app.storage import database

router = APIRouter()


@router.get("/", response_model=DiaryListResponse)
async def list_diaries(
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    emotion: Optional[str] = Query(None, description="情绪类别筛选"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user_id: str = Query("default"),
):
    try:
        await database.init_db()
        entries = await database.get_entries(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            emotion=emotion,
            limit=limit,
            offset=offset,
        )
        return DiaryListResponse(
            entries=[DiaryEntryResponse(**e.model_dump()) for e in entries],
            total=len(entries),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
