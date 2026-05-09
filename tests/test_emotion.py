import json
from unittest.mock import AsyncMock, patch

import pytest

from app.storage.models import EmotionAnalysis, DiaryEntry, EMOTION_CATEGORIES
from app.agents.emotion import analyze_emotion, generate_empathy_reply, process_diary_input


MOCK_EMOTION_RESPONSE = json.dumps({
    "emotion": "sad",
    "score": 0.8,
    "keywords": ["加班", "累", "工作"],
    "summary": "因为加班到很晚感到疲惫和沮丧"
}, ensure_ascii=False)

MOCK_EMPATHY_RESPONSE = "我理解你的疲惫感，加班确实让人身心俱疲。试着今晚早点休息，给自己泡杯热茶放松一下吧。"


@pytest.fixture
def mock_llm():
    with patch("app.agents.emotion._get_llm") as mock:
        llm_instance = AsyncMock()
        mock.return_value = llm_instance
        yield llm_instance


class TestEmotionAnalysis:
    @pytest.mark.asyncio
    async def test_analyze_emotion_returns_valid_format(self, mock_llm):
        mock_llm.ainvoke = AsyncMock(
            return_value=AsyncMock(content=MOCK_EMOTION_RESPONSE)
        )

        result = await analyze_emotion("今天加班到很晚，好累")

        assert isinstance(result, EmotionAnalysis)
        assert result.emotion in EMOTION_CATEGORIES
        assert 0.0 <= result.score <= 1.0
        assert isinstance(result.keywords, list)
        assert 2 <= len(result.keywords) <= 5
        assert len(result.summary) > 0

    @pytest.mark.asyncio
    async def test_analyze_emotion_handles_code_block(self, mock_llm):
        wrapped = f"```json\n{MOCK_EMOTION_RESPONSE}\n```"
        mock_llm.ainvoke = AsyncMock(
            return_value=AsyncMock(content=wrapped)
        )

        result = await analyze_emotion("今天加班到很晚，好累")
        assert result.emotion == "sad"
        assert result.score == 0.8

    @pytest.mark.asyncio
    async def test_analyze_emotion_clamps_score(self, mock_llm):
        bad_response = json.dumps({
            "emotion": "happy",
            "score": 1.5,
            "keywords": ["开心", "朋友"],
            "summary": "和朋友出去玩很开心"
        })
        mock_llm.ainvoke = AsyncMock(
            return_value=AsyncMock(content=bad_response)
        )

        result = await analyze_emotion("和朋友出去玩")
        assert result.score == 1.0

    @pytest.mark.asyncio
    async def test_analyze_emotion_fallback_invalid_category(self, mock_llm):
        bad_response = json.dumps({
            "emotion": "nostalgic",
            "score": 0.5,
            "keywords": ["回忆", "过去"],
            "summary": "回忆过去的时光"
        })
        mock_llm.ainvoke = AsyncMock(
            return_value=AsyncMock(content=bad_response)
        )

        result = await analyze_emotion("想起了小时候的事情")
        assert result.emotion == "confused"


class TestEmpathyReply:
    @pytest.mark.asyncio
    async def test_generate_empathy_reply(self, mock_llm):
        mock_llm.ainvoke = AsyncMock(
            return_value=AsyncMock(content=MOCK_EMPATHY_RESPONSE)
        )

        analysis = EmotionAnalysis(
            emotion="sad", score=0.8,
            keywords=["加班", "累", "工作"],
            summary="因为加班到很晚感到疲惫和沮丧"
        )

        reply = await generate_empathy_reply("今天加班到很晚，好累", analysis)

        assert isinstance(reply, str)
        assert len(reply) > 0
        assert len(reply) <= 150  # 允许一点余量

    @pytest.mark.asyncio
    async def test_empathy_reply_tone(self, mock_llm):
        mock_llm.ainvoke = AsyncMock(
            return_value=AsyncMock(content=MOCK_EMPATHY_RESPONSE)
        )

        analysis = EmotionAnalysis(
            emotion="sad", score=0.8,
            keywords=["加班", "累"],
            summary="加班疲惫"
        )

        reply = await generate_empathy_reply("好累", analysis)
        assert "理解" in reply or "感" in reply


class TestProcessDiaryInput:
    @pytest.mark.asyncio
    async def test_process_diary_input_full_flow(self, mock_llm):
        mock_llm.ainvoke = AsyncMock(
            side_effect=[
                AsyncMock(content=MOCK_EMOTION_RESPONSE),
                AsyncMock(content=MOCK_EMPATHY_RESPONSE),
            ]
        )

        entry, reply = await process_diary_input("今天加班到很晚，好累")

        assert isinstance(entry, DiaryEntry)
        assert entry.emotion == "sad"
        assert entry.emotion_score == 0.8
        assert entry.content == "今天加班到很晚，好累"
        assert entry.user_id == "default"
        assert len(entry.id) > 0
        assert entry.created_at is not None

        assert isinstance(reply, str)
        assert len(reply) > 0


class TestModels:
    def test_emotion_analysis_valid(self):
        analysis = EmotionAnalysis(
            emotion="happy", score=0.9,
            keywords=["朋友", "聚会"],
            summary="和朋友聚会很开心"
        )
        assert analysis.emotion == "happy"
        assert analysis.score == 0.9

    def test_diary_entry_defaults(self):
        entry = DiaryEntry(
            content="测试内容",
            emotion="calm",
            emotion_score=0.5,
        )
        assert entry.user_id == "default"
        assert len(entry.id) > 0
        assert entry.keywords == []
        assert entry.summary == ""
        assert entry.created_at is not None

    def test_emotion_categories(self):
        expected = ["happy", "sad", "anxious", "angry", "calm", "excited", "confused"]
        assert EMOTION_CATEGORIES == expected
