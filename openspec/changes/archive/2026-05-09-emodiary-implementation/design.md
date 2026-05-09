## Context

EmoDiary 是一个情感日记 AI 智能体应用，用户用自然语言记录每日情绪，AI 识别情绪、存储日记、检索历史并生成个性化成长洞察报告。

当前状态：Step 1-2 已完成（项目初始化、配置管理、情绪识别、共情回复、Pydantic 模型、Prompt 模板、基础测试）。剩余 Step 3-11 待实现，涵盖 Agent 编排、数据持久化、向量检索、RAG、报告生成、API 层、前端和部署。

技术约束：
- Python 全栈，依赖已在 requirements.txt 中锁定
- 已有 Pydantic 模型（EmotionAnalysis, DiaryEntry）作为数据契约
- 已有 async 情绪识别和共情回复函数，后续节点需兼容 async 模式
- OpenAI API 作为 LLM 和 Embedding 提供商

## Goals / Non-Goals

**Goals:**
- 完成端到端的日记记录工作流：用户输入 → 情绪识别 → 结构化提取 → 存储 → 共情回复
- 完成历史查询工作流：用户提问 → 意图分类 → 向量检索 → 基于检索结果生成回答
- 完成成长报告生成：聚合历史数据 → 情绪趋势 → 模式识别 → 建议
- 提供完整的 REST API 接口层和 Streamlit 前端
- Docker 容器化，支持一键本地启动和云平台部署
- 代码结构清晰，每个组件可独立测试，面试时能逐层讲解

**Non-Goals:**
- 多用户认证系统（本版本单用户）
- 心理学专业知识库（不导入外部心理学资料）
- 语音输入
- 移动端（微信小程序/App）
- 多模型切换（本版本仅 OpenAI）
- 生产级高可用部署（本版本为作品展示级）

## Decisions

### D1: Agent 编排选择 LangGraph 状态机模式

**决策**: 使用 LangGraph StateGraph 实现两大工作流（日记记录、历史查询），每个节点是一个独立的 async 函数。

**替代方案**:
- LangChain AgentExecutor: 更简单但黑盒，无法可视化状态流转
- 纯代码编排（if/else）: 最简单但不可扩展，失去 Agent 框架学习价值

**理由**: LangGraph 提供显式状态管理和可视化工作流图，面试中可清晰讲解每个节点的职责和状态流转。状态机模式比 ReAct 循环更可控、更适合日记这种确定性流程。

### D2: 双存储架构（SQLite + ChromaDB）

**决策**: SQLite 存储结构化日记元数据（精确查询：按日期、情绪类型筛选），ChromaDB 存储向量嵌入（语义检索：模糊问题如"我上周心情怎么样"）。

**替代方案**:
- 纯 ChromaDB: 无法高效执行精确的日期/情绪筛选查询
- PostgreSQL + pgvector: 功能强大但部署复杂，对学习项目过重

**理由**: 两种存储各解决一类问题。SQLite 零配置、Python 内置；ChromaDB 零配置、pip install 即用。双存储架构本身是一个很好的面试话题。

### D3: Embedding 使用 OpenAI text-embedding-3-small

**决策**: 第一版使用 OpenAI text-embedding-3-small，预留切换接口。

**替代方案**:
- BGE-M3: 中文效果更好、免费，但需要本地加载 ~2GB 模型
- text-embedding-3-large: 效果更好但成本更高

**理由**: 优先跑通全链路，API 调用一行代码。config.py 已预留 embedding model 配置项，后续切换只需改配置。

### D4: LangGraph State 统一状态定义

**决策**: 定义一个 TypedDict 作为 LangGraph 全局状态，包含 user_input、emotion_analysis、diary_entry、response、retrieved_entries、report 等字段，所有节点读写同一状态。

**理由**: 统一状态避免节点间参数传递混乱，新增节点只需扩展状态字段。TypedDict 提供类型提示，IDE 友好。

### D5: API 设计遵循 RESTful + 异步

**决策**: FastAPI async 路由，四个核心端点：POST /chat（聊天入口）、GET/POST /diary（日记 CRUD）、GET /report（报告生成）、GET /search（历史检索）。

**理由**: FastAPI 的 async 支持与 LangGraph async 节点天然匹配，自动生成 OpenAPI 文档方便调试。

### D6: 前端 Streamlit 单页应用

**决策**: Streamlit 实现四个 Tab：聊天界面、情绪仪表盘、历史日记列表、成长报告。通过 HTTP 调用后端 API。

**替代方案**:
- Gradio: 更适合 ML demo 但定制性差
- React: 功能强大但开发周期长，超出 2 周范围

**理由**: Python 原生 UI，几行代码出页面，适合快速原型。前后端分离架构便于面试讲解。

## Risks / Trade-offs

- **OpenAI API 依赖** → 网络不稳定时全链路受影响。缓解：本地开发时可用 mock 模式跳过 API 调用运行测试。
- **SQLite 并发限制** → 单写锁，高并发写入会阻塞。缓解：本版本单用户，不构成问题；扩展时可切 PostgreSQL。
- **ChromaDB 不适合生产** → 无分布式、无认证。缓解：本版本为展示项目，生产可切 Qdrant。
- **LangGraph 版本变化快** → API 可能在版本升级中变化。缓解：锁定 requirements.txt 中的版本号。
- **情绪识别准确性依赖 Prompt** → LLM 输出不总是完美 JSON。缓解：已在 emotion.py 中实现 JSON 解析容错和字段验证。
