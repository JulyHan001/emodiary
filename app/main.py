from fastapi import FastAPI
from app.api import chat, diary, report

app = FastAPI(title="EmoDiary", version="0.1.0")

app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(diary.router, prefix="/api/diary", tags=["diary"])
app.include_router(report.router, prefix="/api/report", tags=["report"])


@app.get("/health")
async def health():
    return {"status": "ok"}
