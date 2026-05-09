from collections import Counter
from datetime import datetime, timedelta

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from app.config import get_settings
from app.storage import database
from app.prompts.report_gen import REPORT_GEN_PROMPT


async def generate_report(
    period: str = "week",
    date: str | None = None,
    user_id: str = "default",
) -> str:
    ref_date = datetime.fromisoformat(date) if date else datetime.now()

    if period == "week":
        start_date = (ref_date - timedelta(days=7)).strftime("%Y-%m-%d")
        period_label = "过去一周"
    else:
        start_date = (ref_date.replace(day=1)).strftime("%Y-%m-%d")
        period_label = f"{ref_date.year}年{ref_date.month}月"

    end_date = ref_date.strftime("%Y-%m-%d")

    await database.init_db()
    entries = await database.get_entries(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        limit=100,
    )

    if len(entries) < 2:
        return f"当前时间段（{period_label}）只有 {len(entries)} 条日记记录，至少需要 2 条才能生成有意义的分析报告。多记录一些心情吧！"

    emotion_counts = Counter(e.emotion for e in entries)
    emotion_dist = ", ".join(f"{k}: {v}次" for k, v in emotion_counts.most_common())

    entries_detail = ""
    for e in entries:
        entries_detail += f"- [{e.created_at.strftime('%Y-%m-%d')}] 情绪: {e.emotion}({e.emotion_score}) | {e.summary}\n"

    settings = get_settings()
    llm = ChatOpenAI(
        model=settings.llm_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        temperature=0.7,
    )

    prompt = REPORT_GEN_PROMPT.format(
        period_label=period_label,
        entry_count=len(entries),
        emotion_distribution=emotion_dist,
        entries_detail=entries_detail,
    )

    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return response.content.strip()
