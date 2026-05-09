from unittest.mock import patch, MagicMock
from datetime import datetime

import pytest

from app.storage.models import DiaryEntry
from app.storage import vectorstore


@pytest.fixture(autouse=True)
def setup_vectorstore(tmp_path, monkeypatch):
    vectorstore.reset_client()
    monkeypatch.setattr(vectorstore, "_client", None)
    monkeypatch.setattr(vectorstore, "_collection", None)

    settings_mock = MagicMock()
    settings_mock.chroma_persist_dir = str(tmp_path / "chroma")
    settings_mock.openai_api_key = "test-key"
    settings_mock.openai_base_url = "https://api.openai.com/v1"
    monkeypatch.setattr("app.storage.vectorstore.get_settings", lambda: settings_mock)
    yield
    vectorstore.reset_client()


FAKE_EMBEDDING = [0.1] * 1536


@pytest.fixture
def mock_embedding(monkeypatch):
    monkeypatch.setattr(vectorstore, "_get_embedding", lambda text: FAKE_EMBEDDING)


def _make_entry(**overrides) -> DiaryEntry:
    defaults = dict(
        content="今天工作很累",
        emotion="sad",
        emotion_score=0.7,
        keywords=["工作", "疲惫"],
        summary="加班导致疲惫",
    )
    defaults.update(overrides)
    entry = DiaryEntry(**defaults)
    if "created_at" in overrides:
        entry.created_at = overrides["created_at"]
    return entry


class TestAddEntry:
    def test_add_entry_stores_document(self, mock_embedding):
        entry = _make_entry()
        vectorstore.add_entry(entry)
        collection = vectorstore._get_collection()
        result = collection.get(ids=[entry.id])
        assert result["ids"] == [entry.id]
        assert "今天工作很累" in result["documents"][0]

    def test_add_entry_stores_metadata(self, mock_embedding):
        entry = _make_entry(emotion="happy", emotion_score=0.9)
        vectorstore.add_entry(entry)
        collection = vectorstore._get_collection()
        result = collection.get(ids=[entry.id], include=["metadatas"])
        meta = result["metadatas"][0]
        assert meta["emotion"] == "happy"
        assert meta["emotion_score"] == 0.9
        assert "date" in meta


class TestSearch:
    def test_search_returns_results(self, mock_embedding):
        for i in range(3):
            vectorstore.add_entry(_make_entry(content=f"entry {i}"))
        results = vectorstore.search("工作累", top_k=2)
        assert len(results) == 2
        assert "id" in results[0]
        assert "document" in results[0]
        assert "metadata" in results[0]

    def test_search_empty_collection(self, mock_embedding):
        results = vectorstore.search("anything", top_k=5)
        assert results == []

    def test_search_with_date_filter(self, mock_embedding):
        e1 = _make_entry(content="old entry")
        e1.created_at = datetime(2026, 5, 1)
        e2 = _make_entry(content="new entry")
        e2.created_at = datetime(2026, 5, 8)
        vectorstore.add_entry(e1)
        vectorstore.add_entry(e2)

        results = vectorstore.search("entry", start_date="2026-05-05", end_date="2026-05-10")
        assert len(results) == 1
        assert results[0]["metadata"]["date"] == 20260508


class TestPersistence:
    def test_collection_created_on_first_use(self, mock_embedding):
        collection = vectorstore._get_collection()
        assert collection is not None
        assert collection.name == "diary_entries"
