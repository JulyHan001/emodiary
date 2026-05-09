from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.api.schemas import ReportResponse
from app.agents.report import generate_report

router = APIRouter()


@router.get("/", response_model=ReportResponse)
async def get_report(
    period: str = Query("week", description="week 或 month"),
    date: Optional[str] = Query(None, description="参考日期 YYYY-MM-DD"),
    user_id: str = Query("default"),
):
    if period not in ("week", "month"):
        raise HTTPException(status_code=400, detail="period must be 'week' or 'month'")
    try:
        ref_date = date or datetime.now().strftime("%Y-%m-%d")
        report = await generate_report(period=period, date=ref_date, user_id=user_id)
        return ReportResponse(report=report, period=period, date=ref_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
