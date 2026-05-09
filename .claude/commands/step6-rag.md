# Step 6: RAG 历史检索

## 本步目标
实现基于 RAG 的历史日记检索：用户提问 → 向量检索相关日记 → LLM 基于真实数据生成回答。

## Agent 查询流程
```
用户提问 ("我上周心情怎么样？")
    │
    ▼
[intent_classify] ──── 判断: 查询历史 / 生成报告 / 记录日记 / 闲聊
    │
    ├──▶ [rag_search] ──── 向量检索相关日记 (ChromaDB)
    │        │
    │        ▼
    │    [synthesize] ──── 基于检索结果生成回答
    │
    └──▶ [report_gen] ──── (Step 7 实现)
```

## RAG 检索 + 回答 Prompt
```
基于用户的历史情绪日记，回答用户的问题。

检索到的相关日记:
{retrieved_entries}

规则:
1. 只基于检索到的日记内容回答，不编造信息
2. 如果检索结果不足以回答，诚实说明
3. 引用具体日期和内容增强可信度
4. 语气温暖、关心

用户问题: {user_query}
```

## 实现任务
1. 实现 app/agents/rag.py:
   - 意图分类（区分日记记录 / 历史查询 / 报告生成 / 闲聊）
   - 向量检索 + 结果格式化
   - 基于检索结果的 LLM 回答生成
2. 实现 app/prompts/report_gen.py — RAG 回答的 prompt 模板
3. 更新 app/agents/graph.py — 加入查询流程分支
4. 编写 tests/test_rag.py — 测试检索和回答质量

## 完成标准
- [ ] 意图分类能正确区分 "记录日记" 和 "查询历史"
- [ ] "我上周心情怎么样" 能检索到相关日记并生成合理回答
- [ ] 回答中包含具体日期和日记内容引用
- [ ] 没有相关日记时能诚实回复 "暂无相关记录"
- [ ] pytest tests/test_rag.py 全部通过

## 提交
```bash
git add . && git commit -m "feat(step-6): 实现 RAG 历史日记检索和问答" && git push
```
