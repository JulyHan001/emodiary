from unittest.mock import AsyncMock, patch, MagicMock

import pytest

from app.agents.graph import (
    AgentState,
    intent_classify,
    route_by_intent,
    emotion_detect,
    diary_store,
    empathy_respond,
    casual_respond,
)
from app.storage.models import EmotionAnalysis


@pytest.fixture
def mock_intent_llm():
    with patch("app.agents.graph.ChatOpenAI") as mock_cls:
        llm_instance = AsyncMock()
        mock_cls.return_value = llm_instance
        yield llm_instance


@pytest.fixture
def mock_store():
    with patch("app.agents.diary.database") as mock_db, \
         patch("app.agents.diary.vectorstore") as mock_vs:
        mock_db.init_db = AsyncMock()
        mock_db.create_entry = AsyncMock(side_effect=lambda e: e)
        mock_vs.add_entry = MagicMock()
        yield mock_db, mock_vs


class TestIntentClassify:
    @pytest.mark.asyncio
    async def test_record_diary_intent(self, mock_intent_llm):
        mock_intent_llm.ainvoke = AsyncMock(return_value=AsyncMock(content="record_diary"))
        state: AgentState = {"user_input": "今天好累啊", "user_id": "default"}
        result = await intent_classify(state)
        assert result["intent"] == "record_diary"

    @pytest.mark.asyncio
    async def test_query_history_intent(self, mock_intent_llm):
        mock_intent_llm.ainvoke = AsyncMock(return_value=AsyncMock(content="query_history"))
        state: AgentState = {"user_input": "我这周心情怎么样", "user_id": "default"}
        result = await intent_classify(state)
        assert result["intent"] == "query_history"

    @pytest.mark.asyncio
    async def test_casual_chat_intent(self, mock_intent_llm):
        mock_intent_llm.ainvoke = AsyncMock(return_value=AsyncMock(content="casual_chat"))
        state: AgentState = {"user_input": "你好", "user_id": "default"}
        result = await intent_classify(state)
        assert result["intent"] == "casual_chat"

    @pytest.mark.asyncio
    async def test_invalid_intent_defaults_to_casual(self, mock_intent_llm):
        mock_intent_llm.ainvoke = AsyncMock(return_value=AsyncMock(content="something_else"))
        state: AgentState = {"user_input": "???", "user_id": "default"}
        result = await intent_classify(state)
        assert result["intent"] == "casual_chat"


class TestRouteByIntent:
    def test_record_diary_routes_to_emotion(self):
        assert route_by_intent({"intent": "record_diary"}) == "emotion_detect"

    def test_query_history_routes_to_rag(self):
        assert route_by_intent({"intent": "query_history"}) == "rag_search"

    def test_casual_routes_to_casual(self):
        assert route_by_intent({"intent": "casual_chat"}) == "casual_respond"

    def test_missing_intent_defaults_casual(self):
        assert route_by_intent({}) == "casual_respond"


class TestCasualRespond:
    @pytest.mark.asyncio
    async def test_returns_greeting(self):
        result = await casual_respond({"user_input": "你好"})
        assert "response" in result
        assert len(result["response"]) > 0


class TestEmotionDetect:
    @pytest.mark.asyncio
    async def test_calls_analyze_emotion(self):
        mock_analysis = EmotionAnalysis(
            emotion="sad", score=0.7, keywords=["难过", "心情"], summary="心情不好"
        )
        with patch("app.agents.graph.analyze_emotion", new_callable=AsyncMock, return_value=mock_analysis):
            state: AgentState = {"user_input": "今天好难过"}
            result = await emotion_detect(state)
            assert result["emotion_analysis"].emotion == "sad"


class TestDiaryStore:
    @pytest.mark.asyncio
    async def test_stores_entry(self, mock_store):
        mock_db, mock_vs = mock_store
        analysis = EmotionAnalysis(emotion="sad", score=0.7, keywords=["累"], summary="疲惫")
        state: AgentState = {
            "user_input": "好累",
            "user_id": "default",
            "emotion_analysis": analysis,
        }
        result = await diary_store(state)
        assert result["diary_entry"] is not None
        assert result["diary_entry"].emotion == "sad"
        mock_db.create_entry.assert_called_once()
        mock_vs.add_entry.assert_called_once()


class TestEmpathyRespond:
    @pytest.mark.asyncio
    async def test_generates_reply(self):
        with patch(
            "app.agents.graph.generate_empathy_reply",
            new_callable=AsyncMock,
            return_value="我理解你的疲惫感。试着放松一下吧。"
        ):
            analysis = EmotionAnalysis(emotion="sad", score=0.7, keywords=["累"], summary="疲惫")
            state: AgentState = {"user_input": "好累", "emotion_analysis": analysis}
            result = await empathy_respond(state)
            assert "response" in result
            assert "理解" in result["response"]
