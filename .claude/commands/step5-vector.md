# Step 5: ChromaDB 向量存储 + Embedding

## 本步目标
实现日记的向量化存储，为后续 RAG 检索做准备。

## 向量存储模型
```python
# 每条日记生成 embedding 存入 ChromaDB
{
    "id": "diary_uuid",
    "document": "用户原始内容 + AI总结",
    "metadata": {
        "emotion": "anxious",
        "emotion_score": 0.7,
        "date": "2026-05-09"
    },
    "embedding": [0.12, -0.34, ...]  # text-embedding-3-small
}
```

## RAG 技术决策
| 决策项 | 选择 | 理由 |
|--------|------|------|
| Embedding 模型 | OpenAI text-embedding-3-small | API 一行调用，先跑通 RAG 全链路 |
| 相似度计算 | 余弦相似度 | 日记长短不一，只比语义方向不比长度 |
| 向量索引 | Flat/HNSW | 数据量 < 10K，ChromaDB 默认 HNSW 即可 |
| 向量数据库 | ChromaDB | pip install 零配置，Python 原生 |

## 实现任务
1. 实现 app/storage/vectorstore.py:
   - 初始化 ChromaDB 客户端和 collection
   - `add_entry(entry_id, text, metadata)` — 向量化并存入
   - `search(query, top_k=5)` — 相似度检索
   - `delete_entry(entry_id)` — 删除向量
2. 更新 app/agents/graph.py 的 store 节点，同时写入 SQLite 和 ChromaDB
3. 编写 tests/test_vectorstore.py — 测试存储和检索

## 完成标准
- [ ] 日记能生成 embedding 并存入 ChromaDB
- [ ] 搜索 "工作压力" 能返回包含相关内容的日记
- [ ] metadata 筛选（按情绪、按日期）正常工作
- [ ] ChromaDB 数据持久化到本地目录，重启不丢失
- [ ] Agent store 节点同时写入 SQLite + ChromaDB
- [ ] pytest tests/test_vectorstore.py 全部通过

## 提交
```bash
git add . && git commit -m "feat(step-5): 实现 ChromaDB 向量存储和 Embedding" && git push
```
