from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from app.config import get_settings
from app.storage import vectorstore
from app.prompts.rag_search import RAG_SYNTHESIZE_PROMPT


def search_history(
    query: str,
    user_id: str = "default",
    top_k: int = 5,
    start_date: str | None = None,
    end_date: str | None = None,
) -> list[dict]:
    return vectorstore.search(
        query=query,
        top_k=top_k,
        start_date=start_date,
        end_date=end_date,
        user_id=user_id,
    )


async def synthesize_answer(query: str, retrieved_entries: list[dict]) -> str:
    if not retrieved_entries:
        return "目前还没有找到相关的日记记录。多记录一些心情，我就能更好地帮你回顾了！"

    entries_text = ""
    for i, entry in enumerate(retrieved_entries, 1):
        meta = entry.get("metadata", {})
        entries_text += f"\n{i}. [{meta.get('date', '未知日期')}] 情绪: {meta.get('emotion', '未知')}\n   {entry.get('document', '')}\n"

    settings = get_settings()
    llm = ChatOpenAI(
        model=settings.llm_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        temperature=0.5,
    )

    prompt = RAG_SYNTHESIZE_PROMPT.format(
        user_input=query,
        retrieved_entries=entries_text,
    )

    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return response.content.strip()
