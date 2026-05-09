from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field


EMOTION_CATEGORIES = ["happy", "sad", "anxious", "angry", "calm", "excited", "confused"]


class EmotionAnalysis(BaseModel):
    emotion: str = Field(description="主要情绪类别")
    score: float = Field(ge=0.0, le=1.0, description="情绪强度 0.0-1.0")
    keywords: list[str] = Field(description="关键词 2-5 个")
    summary: str = Field(description="一句话总结")


class DiaryEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str = Field(default="default")
    content: str = Field(description="原始用户输入")
    emotion: str = Field(description="主要情绪")
    emotion_score: float = Field(ge=0.0, le=1.0, description="情绪强度")
    keywords: list[str] = Field(default_factory=list, description="关键词")
    summary: str = Field(default="", description="AI 生成的一句话总结")
    created_at: datetime = Field(default_factory=datetime.now)
