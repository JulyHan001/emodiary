# Step 2: OpenAI API 调用 + 情绪识别

## 本步目标
实现情绪识别核心功能：用户输入一段文字，AI 返回结构化的情绪分析结果。

## 数据模型
```python
class DiaryEntry:
    id: str              # UUID
    user_id: str         # 用户标识
    content: str         # 原始用户输入
    emotion: str         # 主要情绪: happy/sad/anxious/angry/calm/excited/confused
    emotion_score: float # 情绪强度 0.0-1.0
    keywords: list[str]  # 关键词: ["工作压力", "加班", "同事"]
    summary: str         # AI 生成的一句话总结
    created_at: datetime # 记录时间
```

## Prompt 设计

### 情绪识别 Prompt
```
你是一个情绪分析专家。分析用户的文字，识别其主要情绪。

规则:
1. 从以下类别中选择最匹配的情绪: happy, sad, anxious, angry, calm, excited, confused
2. 给出情绪强度 (0.0-1.0)
3. 提取 2-5 个关键词

输出格式 (JSON):
{
  "emotion": "anxious",
  "score": 0.7,
  "keywords": ["工作压力", "deadline", "睡不好"],
  "summary": "因为工作deadline临近感到焦虑，影响了睡眠"
}

用户输入: {user_input}
```

### 共情回复 Prompt
```
你是一个温暖、有同理心的情感助手。根据用户的情绪分析结果，生成一段回复。

规则:
1. 先共情（"我理解你的感受..."）
2. 再提供一个具体、可执行的小建议
3. 语气温和、不说教
4. 控制在 100 字以内

情绪分析: {emotion_analysis}
用户原文: {user_input}
```

## 实现任务
1. 实现 app/prompts/emotion_detect.py — 情绪识别 prompt 模板
2. 实现 app/prompts/empathy_reply.py — 共情回复 prompt 模板
3. 实现 app/agents/emotion.py — 调用 LLM API 进行情绪分析
4. 实现 app/storage/models.py — DiaryEntry 数据模型 (Pydantic)
5. 编写 tests/test_emotion.py — 测试情绪识别功能

## 完成标准
- [ ] 输入 "今天加班到很晚，好累" 能返回正确格式的情绪 JSON
- [ ] emotion 字段在 7 种类别内
- [ ] score 在 0.0-1.0 范围
- [ ] keywords 是 list 且 2-5 个元素
- [ ] 共情回复在 100 字以内且语气温和
- [ ] pytest tests/test_emotion.py 全部通过

## 提交
```bash
git add . && git commit -m "feat(step-2): 实现情绪识别和共情回复功能" && git push
```
