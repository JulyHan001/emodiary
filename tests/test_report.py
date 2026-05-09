from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock

import pytest
import pytest_asyncio

from app.agents.report import generate_report
from app.storage.models import DiaryEntry
from app.storage import database


@pytest_asyncio.fixture(autouse=True)
async def setup_test_db(tmp_path, monkeypatch):
    db_path = str(tmp_path / "test.db")
    monkeypatch.setattr(database, "_DB_PATH", db_path)
    await database.init_db()
    yield


def _make_entry(emotion="sad", score=0.7, day=5):
    entry = DiaryEntry(
        content=f"entry on day {day}",
        emotion=emotion,
        emotion_score=score,
        keywords=["test"],
        summary=f"summary for day {day}",
    )
    entry.created_at = datetime(2026, 5, day, 10, 0)
    return entry


class TestGenerateReport:
    @pytest.mark.asyncio
    async def test_insufficient_data(self):
        result = await generate_report(period="week", date="2026-05-09")
        assert "至少需要" in result or "只有" in result

    @pytest.mark.asyncio
    async def test_generates_report_with_enough_data(self):
        for day in range(3, 9):
            await database.create_entry(_make_entry(day=day))

        with patch("app.agents.report.ChatOpenAI") as mock_cls:
            llm = AsyncMock()
            llm.ainvoke = AsyncMock(return_value=AsyncMock(
                content="## 情绪趋势\n整体偏低落\n## 关键事件\n工作压力\n## 模式识别\n重复疲惫\n## 成长建议\n多休息"
            ))
            mock_cls.return_value = llm

            result = await generate_report(period="week", date="2026-05-09")
            assert "情绪趋势" in result
            assert "关键事件" in result
            assert "模式识别" in result
            assert "成长建议" in result

    @pytest.mark.asyncio
    async def test_monthly_report(self):
        for day in range(1, 6):
            await database.create_entry(_make_entry(day=day))

        with patch("app.agents.report.ChatOpenAI") as mock_cls:
            llm = AsyncMock()
            llm.ainvoke = AsyncMock(return_value=AsyncMock(content="## 情绪趋势\nok"))
            mock_cls.return_value = llm

            result = await generate_report(period="month", date="2026-05-09")
            assert len(result) > 0
