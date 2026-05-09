from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage.models import EmotionAnalysis, DiaryEntry

client = TestClient(app)


class TestHealthEndpoint:
    def test_health(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestChatEndpoint:
    def test_chat_casual(self):
        with patch("app.api.chat.run_agent", new_callable=AsyncMock) as mock_agent:
            mock_agent.return_value = {
                "intent": "casual_chat",
                "response": "你好！我是 EmoDiary。",
            }
            response = client.post("/api/chat/", json={"user_input": "你好"})
            assert response.status_code == 200
            data = response.json()
            assert data["intent"] == "casual_chat"
            assert "response" in data

    def test_chat_diary_recording(self):
        with patch("app.api.chat.run_agent", new_callable=AsyncMock) as mock_agent:
            entry = DiaryEntry(
                content="今天好累", emotion="sad", emotion_score=0.7,
                keywords=["累"], summary="疲惫",
            )
            mock_agent.return_value = {
                "intent": "record_diary",
                "emotion_analysis": EmotionAnalysis(
                    emotion="sad", score=0.7, keywords=["累"], summary="疲惫"
                ),
                "diary_entry": entry,
                "response": "我理解你的疲惫。",
            }
            response = client.post("/api/chat/", json={"user_input": "今天好累"})
            assert response.status_code == 200
            data = response.json()
            assert data["intent"] == "record_diary"
            assert data["emotion_analysis"]["emotion"] == "sad"
            assert data["diary_entry_id"] is not None

    def test_chat_missing_input(self):
        response = client.post("/api/chat/", json={})
        assert response.status_code == 422


class TestDiaryEndpoint:
    def test_list_diaries(self):
        with patch("app.api.diary.database") as mock_db:
            mock_db.init_db = AsyncMock()
            entry = DiaryEntry(
                content="test", emotion="happy", emotion_score=0.9,
                keywords=["test"], summary="test entry",
            )
            mock_db.get_entries = AsyncMock(return_value=[entry])
            response = client.get("/api/diary/")
            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 1
            assert data["entries"][0]["emotion"] == "happy"

    def test_list_diaries_with_filters(self):
        with patch("app.api.diary.database") as mock_db:
            mock_db.init_db = AsyncMock()
            mock_db.get_entries = AsyncMock(return_value=[])
            response = client.get("/api/diary/?emotion=happy&start_date=2026-05-01&end_date=2026-05-07")
            assert response.status_code == 200
            mock_db.get_entries.assert_called_once()


class TestReportEndpoint:
    def test_get_report(self):
        with patch("app.api.report.generate_report", new_callable=AsyncMock) as mock_report:
            mock_report.return_value = "## 情绪趋势\n整体平稳"
            response = client.get("/api/report/?period=week&date=2026-05-09")
            assert response.status_code == 200
            data = response.json()
            assert "情绪趋势" in data["report"]

    def test_invalid_period(self):
        response = client.get("/api/report/?period=year")
        assert response.status_code == 400


class TestSearchEndpoint:
    def test_search(self):
        with patch("app.api.search.vectorstore") as mock_vs:
            mock_vs.search.return_value = [
                {"id": "1", "document": "test", "metadata": {"emotion": "sad"}, "distance": 0.1}
            ]
            response = client.get("/api/search/?q=工作压力")
            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 1
            assert data["query"] == "工作压力"

    def test_search_missing_query(self):
        response = client.get("/api/search/")
        assert response.status_code == 422
