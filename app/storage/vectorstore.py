import os

import chromadb

from app.config import get_settings
from app.storage.models import DiaryEntry

_client: chromadb.ClientAPI | None = None
_collection: chromadb.Collection | None = None


def _get_collection() -> chromadb.Collection:
    global _client, _collection
    if _collection is None:
        settings = get_settings()
        persist_dir = settings.chroma_persist_dir
        os.makedirs(persist_dir, exist_ok=True)
        _client = chromadb.PersistentClient(path=persist_dir)
        _collection = _client.get_or_create_collection(
            name="diary_entries",
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def add_entry(entry: DiaryEntry) -> None:
    collection = _get_collection()
    document = f"{entry.content} {entry.summary}"
    collection.add(
        ids=[entry.id],
        documents=[document],
        metadatas=[{
            "emotion": entry.emotion,
            "emotion_score": entry.emotion_score,
            "date": int(entry.created_at.strftime("%Y%m%d")),
            "user_id": entry.user_id,
        }],
    )


def _date_to_int(date_str: str) -> int:
    return int(date_str.replace("-", ""))


def search(
    query: str,
    top_k: int = 5,
    start_date: str | None = None,
    end_date: str | None = None,
    user_id: str = "default",
) -> list[dict]:
    collection = _get_collection()

    where_filter: dict = {"user_id": user_id}
    if start_date and end_date:
        where_filter = {
            "$and": [
                {"user_id": user_id},
                {"date": {"$gte": _date_to_int(start_date)}},
                {"date": {"$lte": _date_to_int(end_date)}},
            ]
        }
    elif start_date:
        where_filter = {
            "$and": [
                {"user_id": user_id},
                {"date": {"$gte": _date_to_int(start_date)}},
            ]
        }
    elif end_date:
        where_filter = {
            "$and": [
                {"user_id": user_id},
                {"date": {"$lte": _date_to_int(end_date)}},
            ]
        }

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where=where_filter,
    )

    entries = []
    if results["ids"] and results["ids"][0]:
        for i, doc_id in enumerate(results["ids"][0]):
            entries.append({
                "id": doc_id,
                "document": results["documents"][0][i] if results["documents"] else "",
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                "distance": results["distances"][0][i] if results["distances"] else None,
            })
    return entries


def reset_client():
    global _client, _collection
    _client = None
    _collection = None
