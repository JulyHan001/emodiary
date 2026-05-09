import json

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from app.config import get_settings
from app.prompts.emotion_detect import EMOTION_DETECT_PROMPT
from app.prompts.empathy_reply import EMPATHY_REPLY_PROMPT
from app.storage.models import EmotionAnalysis, DiaryEntry, EMOTION_CATEGORIES


def _get_llm() -> ChatOpenAI:
    settings = get_settings()
    return ChatOpenAI(
        model=settings.llm_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        temperature=0.3,
    )


async def analyze_emotion(user_input: str) -> EmotionAnalysis:
    llm = _get_llm()
    prompt = EMOTION_DETECT_PROMPT.format(user_input=user_input)
    response = await llm.ainvoke([HumanMessage(content=prompt)])

    raw = response.content.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    data = json.loads(raw)

    if data["emotion"] not in EMOTION_CATEGORIES:
        data["emotion"] = "confused"
    data["score"] = max(0.0, min(1.0, float(data["score"])))
    if not (2 <= len(data["keywords"]) <= 5):
        data["keywords"] = data["keywords"][:5] if len(data["keywords"]) > 5 else data["keywords"]

    return EmotionAnalysis(**data)


async def generate_empathy_reply(user_input: str, emotion_analysis: EmotionAnalysis) -> str:
    llm = _get_llm()
    prompt = EMPATHY_REPLY_PROMPT.format(
        user_input=user_input,
        emotion_analysis=emotion_analysis.model_dump_json(ensure_ascii=False),
    )
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return response.content.strip()


async def process_diary_input(user_input: str, user_id: str = "default") -> tuple[DiaryEntry, str]:
    analysis = await analyze_emotion(user_input)
    reply = await generate_empathy_reply(user_input, analysis)

    entry = DiaryEntry(
        user_id=user_id,
        content=user_input,
        emotion=analysis.emotion,
        emotion_score=analysis.score,
        keywords=analysis.keywords,
        summary=analysis.summary,
    )

    return entry, reply
