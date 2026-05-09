from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.storage.models import EmotionAnalysis


class ChatRequest(BaseModel):
    user_input: str = Field(description="用户输入文本")
    user_id: str = Field(default="default", description="用户标识")


class ChatResponse(BaseModel):
    emotion_analysis: Optional[EmotionAnalysis] = None
    diary_entry_id: Optional[str] = None
    response: str = Field(description="AI 回复")
    intent: str = Field(default="", description="识别的意图")


class DiaryEntryResponse(BaseModel):
    id: str
    user_id: str
    content: str
    emotion: str
    emotion_score: float
    keywords: list[str]
    summary: str
    created_at: datetime


class DiaryListResponse(BaseModel):
    entries: list[DiaryEntryResponse]
    total: int


class ReportRequest(BaseModel):
    period: str = Field(default="week", description="week 或 month")
    date: Optional[str] = Field(default=None, description="参考日期 YYYY-MM-DD")


class ReportResponse(BaseModel):
    report: str
    period: str
    date: str


class SearchResponse(BaseModel):
    results: list[dict]
    query: str
    total: int
