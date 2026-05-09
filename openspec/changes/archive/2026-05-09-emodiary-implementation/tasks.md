## 1. SQLite 数据持久化层

- [x] 1.1 实现 database.py: 创建 async 数据库连接管理（aiosqlite），自动建表 diary_entries
- [x] 1.2 实现 diary CRUD 操作: create_entry, get_entries(filters), get_entry_by_id
- [x] 1.3 实现日期范围查询和情绪类别筛选功能
- [x] 1.4 编写 database 单元测试，验证建表、插入、查询、筛选功能

## 2. ChromaDB 向量存储层

- [x] 2.1 实现 vectorstore.py: ChromaDB 客户端初始化，持久化目录配置，collection 创建
- [x] 2.2 实现 add_entry 方法: 调用 OpenAI embedding API 生成向量，存入 ChromaDB（含 metadata）
- [x] 2.3 实现 search 方法: 接收查询文本，生成 embedding，执行 top-k 相似度检索
- [x] 2.4 实现 metadata 过滤（日期范围）功能
- [x] 2.5 编写 vectorstore 单元测试，验证存储和检索功能

## 3. LangGraph Agent 编排 - 日记记录流程

- [x] 3.1 定义 AgentState TypedDict（user_input, intent, emotion_analysis, diary_entry, response, retrieved_entries, report）
- [x] 3.2 实现意图分类节点 intent_classify: 使用 LLM 判断 record_diary / query_history / casual_chat
- [x] 3.3 实现 diary 节点: 调用已有 emotion.py 的 analyze_emotion，将结果写入 state
- [x] 3.4 实现 store 节点: 从 state 读取分析结果，调用 database + vectorstore 持久化
- [x] 3.5 实现 respond 节点: 调用已有 generate_empathy_reply，将回复写入 state
- [x] 3.6 组装 diary_recording_graph: StateGraph 连接上述节点，添加条件边
- [x] 3.7 编写 agent graph 集成测试，验证日记记录端到端流程

## 4. RAG 历史检索流程

- [x] 4.1 实现 rag.py 中的 rag_search 节点: 从 state 读取 user_input，调用 vectorstore.search 获取相关条目
- [x] 4.2 实现 synthesize 节点: 基于检索到的日记条目 + 用户问题，调用 LLM 生成回答
- [x] 4.3 编写 RAG 检索 prompt 模板（app/prompts/ 下）
- [x] 4.4 将 RAG 流程集成到主 graph 的 query_history 分支
- [x] 4.5 编写 RAG 检索集成测试

## 5. 成长报告生成

- [x] 5.1 实现 report.py: report_gen 节点，从 SQLite 聚合指定时间段数据（情绪统计、关键事件）
- [x] 5.2 实现 report_gen prompt（app/prompts/report_gen.py）: 基于聚合数据生成 Markdown 报告
- [x] 5.3 将 report 流程集成到主 graph 的 report 分支
- [x] 5.4 处理数据不足（< 2 条）的友好提示逻辑
- [x] 5.5 编写 report 生成测试

## 6. FastAPI 接口层

- [x] 6.1 实现 POST /chat 端点: 接收 user_input，调用 agent graph，返回完整结果
- [x] 6.2 实现 GET /diary 端点: 支持 start_date, end_date, emotion, limit, offset 参数
- [x] 6.3 实现 GET /report 端点: 支持 period (week/month) 和 date 参数
- [x] 6.4 实现 GET /search 端点: 支持 q 和 top_k 参数，调用向量检索
- [x] 6.5 统一错误处理: 添加全局异常处理器，返回一致的 JSON 错误格式
- [x] 6.6 定义 Pydantic request/response 模型（ChatRequest, ChatResponse, DiaryListResponse 等）
- [x] 6.7 编写 API 端点测试（使用 TestClient）

## 7. Streamlit 前端

- [x] 7.1 实现聊天界面 Tab: 消息输入、对话历史展示、情绪标签显示
- [x] 7.2 实现情绪仪表盘 Tab: 饼图（情绪分布）、折线图（情绪分数趋势）、统计摘要
- [x] 7.3 实现历史日记 Tab: 日记列表、日期筛选、情绪筛选、展开详情
- [x] 7.4 实现成长报告 Tab: 报告生成按钮、Markdown 渲染
- [x] 7.5 配置 Streamlit 页面布局和样式

## 8. Docker 容器化与部署

- [x] 8.1 编写 Dockerfile: 基于 python:3.11-slim，安装依赖，启动 uvicorn
- [x] 8.2 编写 docker-compose.yml: backend + frontend 双服务，共享 volume 持久化数据
- [x] 8.3 创建 .env.example 文件，文档化所有环境变量
- [ ] 8.4 本地测试 docker-compose up 一键启动
- [ ] 8.5 编写部署文档（Railway/Render 配置说明）

## 9. 集成测试与收尾

- [x] 9.1 端到端集成测试: 从 API 层发起请求，验证完整工作流（日记记录 → 查询 → 报告）
- [x] 9.2 验证数据一致性: 写入 SQLite 的数据与 ChromaDB 中的数据对应一致
- [ ] 9.3 补充 README.md: 项目介绍、架构图、本地运行说明、部署指南
- [x] 9.4 代码规范检查: 确保所有文件有适当的类型注解和模块导入
