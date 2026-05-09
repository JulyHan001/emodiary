import json
import os
from datetime import datetime

import aiosqlite

from app.config import get_settings
from app.storage.models import DiaryEntry

_DB_PATH: str | None = None


def _get_db_path() -> str:
    global _DB_PATH
    if _DB_PATH is None:
        settings = get_settings()
        path = settings.database_url.replace("sqlite:///", "")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        _DB_PATH = path
    return _DB_PATH


async def init_db():
    async with aiosqlite.connect(_get_db_path()) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS diary_entries (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                content TEXT NOT NULL,
                emotion TEXT NOT NULL,
                emotion_score REAL NOT NULL,
                keywords TEXT NOT NULL,
                summary TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        await db.commit()


async def create_entry(entry: DiaryEntry) -> DiaryEntry:
    async with aiosqlite.connect(_get_db_path()) as db:
        await db.execute(
            """INSERT INTO diary_entries (id, user_id, content, emotion, emotion_score, keywords, summary, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                entry.id,
                entry.user_id,
                entry.content,
                entry.emotion,
                entry.emotion_score,
                json.dumps(entry.keywords, ensure_ascii=False),
                entry.summary,
                entry.created_at.isoformat(),
            ),
        )
        await db.commit()
    return entry


def _row_to_entry(row: tuple) -> DiaryEntry:
    return DiaryEntry(
        id=row[0],
        user_id=row[1],
        content=row[2],
        emotion=row[3],
        emotion_score=row[4],
        keywords=json.loads(row[5]),
        summary=row[6],
        created_at=datetime.fromisoformat(row[7]),
    )


async def get_entry_by_id(entry_id: str) -> DiaryEntry | None:
    async with aiosqlite.connect(_get_db_path()) as db:
        cursor = await db.execute(
            "SELECT * FROM diary_entries WHERE id = ?", (entry_id,)
        )
        row = await cursor.fetchone()
        return _row_to_entry(row) if row else None


async def get_entries(
    user_id: str = "default",
    start_date: str | None = None,
    end_date: str | None = None,
    emotion: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[DiaryEntry]:
    query = "SELECT * FROM diary_entries WHERE user_id = ?"
    params: list = [user_id]

    if start_date:
        query += " AND created_at >= ?"
        params.append(start_date)
    if end_date:
        query += " AND created_at <= ?"
        params.append(end_date + "T23:59:59")
    if emotion:
        query += " AND emotion = ?"
        params.append(emotion)

    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    async with aiosqlite.connect(_get_db_path()) as db:
        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()
        return [_row_to_entry(row) for row in rows]
