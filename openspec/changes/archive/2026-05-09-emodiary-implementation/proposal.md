## Why

构建一个完整的情感日记 AI 智能体应用（EmoDiary），作为 Agent 开发学习项目，覆盖 Prompt Engineering、Agent 编排、RAG 三大核心技术。项目需在 2 周内完成可部署版本，作为求职作品集展示 AI 应用全栈开发能力。

## What Changes

- 新增 FastAPI 后端服务，提供聊天、日记 CRUD、报告生成、历史检索 API
- 新增 LangGraph Agent 编排层，实现情绪识别→结构化提取→存储→共情回复工作流
- 新增 SQLite 数据持久化层，存储结构化日记元数据
- 新增 ChromaDB 向量存储层，支持日记语义检索
- 新增 RAG 历史检索功能，基于向量相似度回答历史问题
- 新增成长报告生成功能，聚合情绪数据生成趋势分析
- 新增 Streamlit 前端，包含聊天界面、情绪仪表盘、历史日记、成长报告
- 新增 Docker 容器化配置，支持一键部署

## Capabilities

### New Capabilities

- `emotion-detection`: 情绪识别能力——接收用户自然语言输入，输出情绪类别、强度、关键词和摘要的结构化 JSON
- `diary-storage`: 日记存储能力——结构化日记条目的 CRUD 操作，支持按日期/情绪筛选查询
- `vector-search`: 向量检索能力——日记 embedding 存储与语义相似度检索
- `agent-orchestration`: Agent 编排能力——LangGraph 状态机实现日记记录和历史查询两大工作流
- `empathy-response`: 共情回复能力——基于情绪分析结果生成温暖、有建设性的回复
- `growth-report`: 成长报告能力——聚合历史数据生成情绪趋势分析和个性化建议
- `api-layer`: API 接口层——FastAPI RESTful 接口，统一请求/响应格式
- `frontend-ui`: 前端界面——Streamlit 聊天界面与数据可视化仪表盘
- `deployment`: 部署能力——Docker 容器化与云平台部署配置

### Modified Capabilities

## Impact

- 新增 Python 依赖: langchain, langgraph, openai, chromadb, fastapi, streamlit, uvicorn, pydantic
- 新增外部 API 依赖: OpenAI API (GPT-4o-mini + text-embedding-3-small)
- 新增本地数据存储: SQLite 数据库文件 + ChromaDB 持久化目录
- 新增环境变量: OPENAI_API_KEY
- 端口占用: FastAPI (8000), Streamlit (8501)
