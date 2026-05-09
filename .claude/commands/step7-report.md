# Step 7: 成长报告生成

## 本步目标
实现基于历史数据的情绪趋势分析和成长洞察报告（周报/月报）。

## 报告生成 Prompt
```
基于用户的历史情绪日记数据，生成一份成长洞察报告。

检索到的相关日记:
{retrieved_entries}

情绪统计数据:
{emotion_stats}

分析要求:
1. 情绪趋势: 这段时间整体情绪走向
2. 关键事件: 哪些事件明显影响了情绪
3. 模式识别: 是否有重复出现的情绪触发因素
4. 成长建议: 基于模式给出 1-2 条可执行建议

输出格式: 使用 markdown，包含标题和分点
```

## 实现任务
1. 实现 app/agents/report.py:
   - 聚合指定时间段的日记数据（SQLite 统计 + ChromaDB 检索）
   - 生成结构化的趋势报告（markdown 格式）
   - 支持周报和月报两种粒度
2. 更新 app/agents/graph.py — 接入报告生成分支
3. 编写 tests/test_report.py — 测试报告生成

## 完成标准
- [ ] "生成本周报告" 能输出包含趋势、事件、建议的 markdown 报告
- [ ] 报告数据基于真实日记，不编造
- [ ] 周报和月报粒度切换正常
- [ ] 无日记数据时给出友好提示
- [ ] pytest tests/test_report.py 全部通过

## 提交
```bash
git add . && git commit -m "feat(step-7): 实现情绪趋势分析和成长报告生成" && git push
```
