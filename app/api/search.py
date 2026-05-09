from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.api.schemas import SearchResponse
from app.storage import vectorstore

router = APIRouter()


@router.get("/", response_model=SearchResponse)
async def search_diaries(
    q: str = Query(..., description="搜索关键词"),
    top_k: int = Query(5, ge=1, le=20),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    user_id: str = Query("default"),
):
    try:
        results = vectorstore.search(
            query=q,
            top_k=top_k,
            start_date=start_date,
            end_date=end_date,
            user_id=user_id,
        )
        return SearchResponse(results=results, query=q, total=len(results))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
