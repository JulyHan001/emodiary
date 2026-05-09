# Step 8: FastAPI 接口层

## 本步目标
用 FastAPI 包装所有 Agent 功能为 RESTful API，供前端调用。

## API 端点设计
```
┌─────────────────────────────────────────────┐
│               API 层 (FastAPI)               │
│  /chat  │  /diary  │  /report  │  /search   │
└─────────────────────────────────────────────┘
```

| 端点 | 方法 | 功能 | 请求体 | 响应 |
|------|------|------|--------|------|
| POST /api/chat | POST | 对话（记录日记或查询） | `{message, user_id}` | `{reply, emotion?, diary_id?}` |
| GET /api/diary | GET | 日记列表 | query: user_id, date_range, emotion | `{entries: [...]}` |
| GET /api/diary/{id} | GET | 日记详情 | - | `{entry}` |
| DELETE /api/diary/{id} | DELETE | 删除日记 | - | `{success}` |
| POST /api/report | POST | 生成报告 | `{user_id, period: "week"/"month"}` | `{report_markdown}` |
| GET /api/search | GET | 语义搜索 | query: q, user_id | `{results: [...]}` |

## 实现任务
1. 实现 app/main.py — FastAPI 入口，配置 CORS 和中间件
2. 实现 app/api/chat.py — 聊天接口（核心：调用 Agent graph）
3. 实现 app/api/diary.py — 日记 CRUD 接口
4. 实现 app/api/report.py — 报告生成接口
5. 编写 tests/test_api.py — API 端点集成测试

## 完成标准
- [ ] `uvicorn app.main:app` 能启动服务
- [ ] `/docs` 自动生成的 Swagger 文档可用
- [ ] POST /api/chat 能完成对话并返回情绪分析
- [ ] GET /api/diary 能按条件筛选日记
- [ ] POST /api/report 能生成报告
- [ ] CORS 配置允许前端跨域访问
- [ ] pytest tests/test_api.py 全部通过

## 提交
```bash
git add . && git commit -m "feat(step-8): 实现 FastAPI RESTful API 接口层" && git push
```
