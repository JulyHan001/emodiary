# Step 3: LangGraph Agent 编排

## 本步目标
用 LangGraph 构建日记记录的完整 Agent 工作流：用户输入 → 情绪识别 → 结构化提取 → 存储 → 共情回复。

## 架构设计

### 系统架构层级
```
前端 (Streamlit) → API (FastAPI) → Agent 编排 (LangGraph) → 存储 (SQLite + ChromaDB)
```

### 日记记录流程 (状态机)
```
用户输入
    │
    ▼
[emotion_detect] ──── 识别情绪类别和强度
    │
    ▼
[structured_extract] ── 提取关键词、生成摘要
    │
    ▼
[store] ──────────── 写入 SQLite + ChromaDB
    │
    ▼
[respond] ─────────── 生成共情回复 + 可选建议
```

### 历史查询流程 (状态机)
```
用户提问 ("我这周心情怎么样？")
    │
    ▼
[intent_classify] ──── 判断: 查询历史 / 生成报告 / 闲聊
    │
    ├──▶ [rag_search] ──── 向量检索相关日记
    │        │
    │        ▼
    │    [synthesize] ──── 基于检索结果生成回答
    │
    └──▶ [report_gen] ──── 聚合数据生成趋势报告
```

## 实现任务
1. 定义 LangGraph State（包含 user_input, emotion, diary_entry, response 等字段）
2. 实现 app/agents/graph.py — 主流程编排，定义节点和边
3. 实现 app/agents/diary.py — 日记结构化节点（调用 Step 2 的情绪识别）
4. 串联 emotion_detect → structured_extract → store → respond 四个节点
5. 编写 tests/test_agent.py — 测试完整流程端到端

## 完成标准
- [ ] LangGraph 状态机能从 "用户输入" 走完整个流程到 "共情回复"
- [ ] 每个节点输入/输出类型明确
- [ ] 中间状态可打印（方便调试）
- [ ] pytest tests/test_agent.py 全部通过
- [ ] 终端运行 `python -m app.agents.graph "今天好开心"` 能输出完整结果

## 提交
```bash
git add . && git commit -m "feat(step-3): 实现 LangGraph Agent 日记记录工作流" && git push
```
