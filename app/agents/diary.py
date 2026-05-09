from app.storage.models import DiaryEntry, EmotionAnalysis
from app.storage import database, vectorstore


async def store_diary_entry(
    user_input: str,
    analysis: EmotionAnalysis,
    user_id: str = "default",
) -> DiaryEntry:
    entry = DiaryEntry(
        user_id=user_id,
        content=user_input,
        emotion=analysis.emotion,
        emotion_score=analysis.score,
        keywords=analysis.keywords,
        summary=analysis.summary,
    )

    await database.init_db()
    await database.create_entry(entry)

    vectorstore.add_entry(entry)

    return entry
