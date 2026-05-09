from unittest.mock import AsyncMock, patch, MagicMock

import pytest

from app.agents.rag import search_history, synthesize_answer


class TestSearchHistory:
    def test_delegates_to_vectorstore(self):
        with patch("app.agents.rag.vectorstore") as mock_vs:
            mock_vs.search.return_value = [{"id": "1", "document": "test", "metadata": {}, "distance": 0.1}]
            results = search_history("工作压力", user_id="default", top_k=3)
            mock_vs.search.assert_called_once_with(
                query="工作压力", top_k=3, start_date=None, end_date=None, user_id="default"
            )
            assert len(results) == 1


class TestSynthesizeAnswer:
    @pytest.mark.asyncio
    async def test_empty_entries_returns_fallback(self):
        result = await synthesize_answer("我这周心情怎么样", [])
        assert "没有找到" in result or "还没有" in result

    @pytest.mark.asyncio
    async def test_synthesizes_from_entries(self):
        with patch("app.agents.rag.ChatOpenAI") as mock_cls:
            llm = AsyncMock()
            llm.ainvoke = AsyncMock(return_value=AsyncMock(content="根据你的日记记录，这周你的心情整体偏低落。"))
            mock_cls.return_value = llm

            entries = [
                {"id": "1", "document": "今天好累 加班疲惫", "metadata": {"date": 20260505, "emotion": "sad"}, "distance": 0.1},
                {"id": "2", "document": "工作压力大 deadline", "metadata": {"date": 20260506, "emotion": "anxious"}, "distance": 0.2},
            ]
            result = await synthesize_answer("我这周心情怎么样", entries)
            assert len(result) > 0
            llm.ainvoke.assert_called_once()
