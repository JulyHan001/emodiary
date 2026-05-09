from __future__ import annotations

from typing import TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END

from app.agents.emotion import analyze_emotion, generate_empathy_reply
from app.config import get_settings
from app.storage.models import EmotionAnalysis, DiaryEntry


class AgentState(TypedDict, total=False):
    user_input: str
    user_id: str
    intent: str
    emotion_analysis: EmotionAnalysis | None
    diary_entry: DiaryEntry | None
    response: str
    retrieved_entries: list[dict]
    report: str | None
    report_period: str
    report_date: str


async def intent_classify(state: AgentState) -> AgentState:
    settings = get_settings()
    llm = ChatOpenAI(
        model=settings.llm_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        temperature=0,
    )

    prompt = f"""判断用户输入的意图，只返回以下三个类别之一，不要返回其他内容：
- record_diary: 用户在表达情感、记录心情、描述经历
- query_history: 用户在询问历史记录、过去的心情、要求生成报告
- casual_chat: 日常闲聊、打招呼、与情绪日记无关的对话

用户输入: {state["user_input"]}

意图:"""

    response = await llm.ainvoke([HumanMessage(content=prompt)])
    intent = response.content.strip().lower()

    if intent not in ("record_diary", "query_history", "casual_chat"):
        intent = "casual_chat"

    return {"intent": intent}


def route_by_intent(state: AgentState) -> str:
    intent = state.get("intent", "casual_chat")
    if intent == "record_diary":
        return "emotion_detect"
    elif intent == "query_history":
        return "rag_search"
    return "casual_respond"


async def casual_respond(state: AgentState) -> AgentState:
    return {"response": "你好！我是你的情感日记助手 EmoDiary。你可以告诉我今天的心情，或者问我你之前的情绪记录。"}


async def emotion_detect(state: AgentState) -> AgentState:
    analysis = await analyze_emotion(state["user_input"])
    return {"emotion_analysis": analysis}


async def diary_store(state: AgentState) -> AgentState:
    from app.agents.diary import store_diary_entry
    analysis = state["emotion_analysis"]
    entry = await store_diary_entry(
        user_input=state["user_input"],
        analysis=analysis,
        user_id=state.get("user_id", "default"),
    )
    return {"diary_entry": entry}


async def empathy_respond(state: AgentState) -> AgentState:
    reply = await generate_empathy_reply(state["user_input"], state["emotion_analysis"])
    return {"response": reply}


async def rag_search(state: AgentState) -> AgentState:
    from app.agents.rag import search_history
    entries = search_history(state["user_input"], user_id=state.get("user_id", "default"))
    return {"retrieved_entries": entries}


async def synthesize(state: AgentState) -> AgentState:
    from app.agents.rag import synthesize_answer
    answer = await synthesize_answer(state["user_input"], state["retrieved_entries"])
    return {"response": answer}


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("intent_classify", intent_classify)
    graph.add_node("emotion_detect", emotion_detect)
    graph.add_node("diary_store", diary_store)
    graph.add_node("empathy_respond", empathy_respond)
    graph.add_node("casual_respond", casual_respond)
    graph.add_node("rag_search", rag_search)
    graph.add_node("synthesize", synthesize)

    graph.add_edge(START, "intent_classify")
    graph.add_conditional_edges("intent_classify", route_by_intent)

    graph.add_edge("emotion_detect", "diary_store")
    graph.add_edge("diary_store", "empathy_respond")
    graph.add_edge("empathy_respond", END)

    graph.add_edge("rag_search", "synthesize")
    graph.add_edge("synthesize", END)

    graph.add_edge("casual_respond", END)

    return graph.compile()


async def run_agent(user_input: str, user_id: str = "default") -> AgentState:
    app = build_graph()
    result = await app.ainvoke({
        "user_input": user_input,
        "user_id": user_id,
    })
    return result
