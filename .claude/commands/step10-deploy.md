# Step 10: Docker 容器化 + 部署

## 本步目标
将项目容器化并部署到云平台，实现线上可访问。

## 部署架构
```
Docker Compose
├── backend  (FastAPI + Agent + SQLite + ChromaDB)
│   └── port: 8000
└── frontend (Streamlit)
    └── port: 8501
```

## 实现任务
1. 编写 Dockerfile — 多阶段构建，优化镜像大小
2. 编写 docker-compose.yml — 编排 backend + frontend
3. 配置 .env.example — 所有环境变量说明
4. 配置 .dockerignore — 排除不需要的文件
5. 本地 `docker-compose up` 验证一键启动
6. 部署到 Railway 或 Render:
   - 配置环境变量（OPENAI_API_KEY 等）
   - 验证线上可访问

## 完成标准
- [ ] `docker-compose up --build` 一键启动成功
- [ ] 前端 localhost:8501 可访问，后端 localhost:8000/docs 可用
- [ ] 容器重启后数据不丢失（volume 持久化）
- [ ] 线上部署成功，外网可访问
- [ ] .env.example 包含所有需要的环境变量说明

## 提交
```bash
git add . && git commit -m "feat(step-10): Docker 容器化和云平台部署" && git push
```
