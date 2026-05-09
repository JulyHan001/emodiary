# Step 4: SQLite 数据持久化

## 本步目标
实现日记的结构化存储，支持增删改查和按条件筛选。

## 数据模型 (SQLite 表结构)
```python
class DiaryEntry:
    id: str              # UUID 主键
    user_id: str         # 用户标识
    content: str         # 原始用户输入
    emotion: str         # 主要情绪: happy/sad/anxious/angry/calm/excited/confused
    emotion_score: float # 情绪强度 0.0-1.0
    keywords: str        # JSON 序列化的关键词列表
    summary: str         # AI 生成的一句话总结
    created_at: str      # ISO 格式时间戳
```

## 实现任务
1. 实现 app/storage/database.py:
   - 初始化数据库连接和建表
   - `save_entry(entry: DiaryEntry)` — 插入日记
   - `get_entry(entry_id: str)` — 按 ID 查询
   - `list_entries(user_id, start_date, end_date, emotion)` — 按条件筛选
   - `delete_entry(entry_id: str)` — 删除日记
   - `get_emotion_stats(user_id, days)` — 情绪统计（各情绪出现次数）
2. 更新 app/agents/graph.py 的 store 节点，接入 SQLite
3. 编写 tests/test_database.py — 覆盖 CRUD 和筛选场景

## 完成标准
- [ ] 日记能成功存入 SQLite，重启后数据不丢失
- [ ] 按日期范围查询返回正确结果
- [ ] 按情绪类别筛选正常工作
- [ ] 情绪统计能返回最近 N 天各情绪的次数
- [ ] Agent 流程中 store 节点写入数据库成功
- [ ] pytest tests/test_database.py 全部通过

## 提交
```bash
git add . && git commit -m "feat(step-4): 实现 SQLite 日记存储和查询功能" && git push
```
