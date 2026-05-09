# Step 1: 项目初始化 + 环境搭建

## 本步目标
搭建 EmoDiary 项目骨架，配置 Python 虚拟环境和依赖，创建目录结构。

## 技术栈
| 层 | 技术选型 |
|----|---------|
| LLM | OpenAI GPT-4o-mini / Claude Haiku |
| Agent 框架 | LangGraph |
| 向量数据库 | ChromaDB |
| 结构化存储 | SQLite |
| API | FastAPI |
| 前端 | Streamlit |
| 部署 | Docker + Railway/Render |

## 目录结构
```
emodiary/
├── README.md
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置管理
│   ├── agents/              # Agent 编排层
│   │   ├── __init__.py
│   │   ├── graph.py
│   │   ├── emotion.py
│   │   ├── diary.py
│   │   ├── rag.py
│   │   └── report.py
│   ├── prompts/             # Prompt 模板
│   │   ├── emotion_detect.py
│   │   ├── empathy_reply.py
│   │   └── report_gen.py
│   ├── storage/             # 数据层
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── vectorstore.py
│   │   └── models.py
│   └── api/                 # API 路由
│       ├── __init__.py
│       ├── chat.py
│       ├── diary.py
│       └── report.py
├── frontend/
│   └── streamlit_app.py
└── tests/
    ├── test_emotion.py
    ├── test_rag.py
    └── test_api.py
```

## 实现任务
1. 创建项目目录结构（所有文件夹和 __init__.py）
2. 创建 requirements.txt（列出所有依赖及版本）
3. 创建 .env.example（环境变量模板）
4. 创建 app/config.py（统一配置管理，从 .env 读取）
5. 搭建 Python 虚拟环境并安装依赖
6. 验证所有依赖能正常 import

## 完成标准
- [ ] 虚拟环境创建成功，所有依赖安装无报错
- [ ] `python -c "import langchain, langgraph, fastapi, chromadb, streamlit"` 正常
- [ ] 项目目录结构完整
- [ ] config.py 能正确读取 .env 配置

## 提交
```bash
git add . && git commit -m "feat(step-1): 项目初始化，搭建目录结构和依赖环境" && git push
```
