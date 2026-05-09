import os
import pytest
import pytest_asyncio

from app.storage.models import DiaryEntry
from app.storage import database


@pytest_asyncio.fixture(autouse=True)
async def setup_test_db(tmp_path, monkeypatch):
    db_path = str(tmp_path / "test.db")
    monkeypatch.setattr(database, "_DB_PATH", db_path)
    await database.init_db()
    yield


def _make_entry(**overrides) -> DiaryEntry:
    defaults = dict(
        content="今天好累",
        emotion="sad",
        emotion_score=0.7,
        keywords=["工作", "加班"],
        summary="加班感到疲惫",
    )
    defaults.update(overrides)
    return DiaryEntry(**defaults)


class TestInitDb:
    @pytest.mark.asyncio
    async def test_creates_table(self, tmp_path, monkeypatch):
        db_path = str(tmp_path / "fresh.db")
        monkeypatch.setattr(database, "_DB_PATH", db_path)
        await database.init_db()
        assert os.path.exists(db_path)


class TestCreateEntry:
    @pytest.mark.asyncio
    async def test_insert_and_retrieve(self):
        entry = _make_entry()
        result = await database.create_entry(entry)
        assert result.id == entry.id

        fetched = await database.get_entry_by_id(entry.id)
        assert fetched is not None
        assert fetched.content == "今天好累"
        assert fetched.emotion == "sad"
        assert fetched.keywords == ["工作", "加班"]


class TestGetEntries:
    @pytest.mark.asyncio
    async def test_list_entries(self):
        for i in range(3):
            await database.create_entry(_make_entry(content=f"entry {i}"))
        entries = await database.get_entries()
        assert len(entries) == 3

    @pytest.mark.asyncio
    async def test_filter_by_emotion(self):
        await database.create_entry(_make_entry(emotion="happy", emotion_score=0.9))
        await database.create_entry(_make_entry(emotion="sad", emotion_score=0.6))
        entries = await database.get_entries(emotion="happy")
        assert len(entries) == 1
        assert entries[0].emotion == "happy"

    @pytest.mark.asyncio
    async def test_filter_by_date_range(self):
        from datetime import datetime
        e1 = _make_entry(content="old")
        e1.created_at = datetime(2026, 5, 1, 10, 0)
        e2 = _make_entry(content="new")
        e2.created_at = datetime(2026, 5, 7, 10, 0)
        await database.create_entry(e1)
        await database.create_entry(e2)

        entries = await database.get_entries(start_date="2026-05-05", end_date="2026-05-08")
        assert len(entries) == 1
        assert entries[0].content == "new"

    @pytest.mark.asyncio
    async def test_pagination(self):
        for i in range(5):
            await database.create_entry(_make_entry(content=f"e{i}"))
        page = await database.get_entries(limit=2, offset=0)
        assert len(page) == 2

    @pytest.mark.asyncio
    async def test_empty_result(self):
        entries = await database.get_entries(emotion="happy")
        assert entries == []


class TestGetEntryById:
    @pytest.mark.asyncio
    async def test_not_found(self):
        result = await database.get_entry_by_id("nonexistent")
        assert result is None
