import os
import streamlit as st
import requests
from datetime import datetime

API_BASE = os.environ.get("API_BASE", "http://localhost:8000/api")

st.set_page_config(page_title="EmoDiary - 情感日记", page_icon="📔", layout="wide")
st.title("📔 EmoDiary — 情感日记助手")

tab_chat, tab_dashboard, tab_history, tab_report = st.tabs(
    ["💬 聊天", "📊 情绪仪表盘", "📖 历史日记", "📈 成长报告"]
)

# --- Chat Tab ---
with tab_chat:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg.get("emotion"):
                emotion_colors = {
                    "happy": "🟢", "sad": "🔵", "anxious": "🟡",
                    "angry": "🔴", "calm": "⚪", "excited": "🟠", "confused": "🟣",
                }
                icon = emotion_colors.get(msg["emotion"], "⚪")
                st.caption(f"{icon} {msg['emotion']} ({msg.get('score', '')})")
            st.markdown(msg["content"])

    if user_input := st.chat_input("告诉我你今天的心情..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("正在分析你的心情..."):
                try:
                    resp = requests.post(f"{API_BASE}/chat/", json={"user_input": user_input}, timeout=60)
                    data = resp.json()

                    if resp.status_code != 200:
                        st.error(f"后端错误: {data.get('detail', resp.text)}")
                    else:
                        emotion = None
                        score = None
                        if data.get("emotion_analysis"):
                            emotion = data["emotion_analysis"]["emotion"]
                            score = data["emotion_analysis"]["score"]
                            emotion_colors = {
                                "happy": "🟢", "sad": "🔵", "anxious": "🟡",
                                "angry": "🔴", "calm": "⚪", "excited": "🟠", "confused": "🟣",
                            }
                            icon = emotion_colors.get(emotion, "⚪")
                            st.caption(f"{icon} {emotion} ({score})")

                        st.markdown(data.get("response", ""))
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": data.get("response", ""),
                            "emotion": emotion,
                            "score": score,
                        })
                except Exception as e:
                    st.error(f"连接后端失败: {e}")

# --- Dashboard Tab ---
with tab_dashboard:
    st.subheader("情绪仪表盘")
    try:
        resp = requests.get(f"{API_BASE}/diary/?limit=100", timeout=10)
        data = resp.json()
        entries = data.get("entries", [])

        if not entries:
            st.info("还没有日记记录，去聊天页面记录你的第一篇日记吧！")
        else:
            import pandas as pd

            df = pd.DataFrame(entries)
            df["created_at"] = pd.to_datetime(df["created_at"])

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("总记录数", len(entries))
            with col2:
                most_common = df["emotion"].mode().iloc[0] if len(df) > 0 else "N/A"
                st.metric("最常见情绪", most_common)
            with col3:
                avg_score = df["emotion_score"].mean()
                st.metric("平均情绪分数", f"{avg_score:.2f}")

            col_pie, col_line = st.columns(2)
            with col_pie:
                st.subheader("情绪分布")
                emotion_counts = df["emotion"].value_counts()
                st.bar_chart(emotion_counts)

            with col_line:
                st.subheader("情绪分数趋势")
                chart_df = df[["created_at", "emotion_score"]].set_index("created_at").sort_index()
                st.line_chart(chart_df)
    except Exception as e:
        st.error(f"加载数据失败: {e}")

# --- History Tab ---
with tab_history:
    st.subheader("历史日记")

    col_filter1, col_filter2, col_filter3 = st.columns(3)
    with col_filter1:
        start_date = st.date_input("开始日期", value=None, key="hist_start")
    with col_filter2:
        end_date = st.date_input("结束日期", value=None, key="hist_end")
    with col_filter3:
        emotion_filter = st.selectbox(
            "情绪筛选", ["全部", "happy", "sad", "anxious", "angry", "calm", "excited", "confused"]
        )

    params = {"limit": 50}
    if start_date:
        params["start_date"] = start_date.isoformat()
    if end_date:
        params["end_date"] = end_date.isoformat()
    if emotion_filter != "全部":
        params["emotion"] = emotion_filter

    try:
        resp = requests.get(f"{API_BASE}/diary/", params=params, timeout=10)
        data = resp.json()
        entries = data.get("entries", [])

        if not entries:
            st.info("没有找到符合条件的日记记录。")
        else:
            for entry in entries:
                emotion_colors = {
                    "happy": "🟢", "sad": "🔵", "anxious": "🟡",
                    "angry": "🔴", "calm": "⚪", "excited": "🟠", "confused": "🟣",
                }
                icon = emotion_colors.get(entry["emotion"], "⚪")
                created = entry["created_at"][:10]
                with st.expander(f"{created} {icon} {entry['emotion']} — {entry['summary']}"):
                    st.markdown(f"**原文:** {entry['content']}")
                    st.markdown(f"**情绪强度:** {entry['emotion_score']}")
                    st.markdown(f"**关键词:** {', '.join(entry['keywords'])}")
    except Exception as e:
        st.error(f"加载日记失败: {e}")

# --- Report Tab ---
with tab_report:
    st.subheader("成长报告")

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        report_period = st.selectbox("报告周期", ["week", "month"], format_func=lambda x: "周报" if x == "week" else "月报")
    with col_r2:
        report_date = st.date_input("参考日期", value=datetime.now(), key="report_date")

    if st.button("生成报告", type="primary"):
        with st.spinner("正在生成报告..."):
            try:
                resp = requests.get(
                    f"{API_BASE}/report/",
                    params={"period": report_period, "date": report_date.isoformat()},
                    timeout=60,
                )
                data = resp.json()
                st.markdown(data.get("report", "生成失败"))
            except Exception as e:
                st.error(f"生成报告失败: {e}")
