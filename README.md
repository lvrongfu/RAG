# 掌柜智库 (RAG)

基于 **检索增强生成（Retrieval-Augmented Generation）** 技术的企业级智能问答系统。通过外挂知识库实时检索相关信息，引导大语言模型基于事实回答，有效消除模型幻觉，显著提升回答的准确率与可信度。

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135+-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.1+-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![Milvus](https://img.shields.io/badge/Milvus-2.6+-00BEB0.svg)](https://milvus.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 项目简介

掌柜智库是一套集"私有知识库精准问答、实时联网信息补充、多维度结果优化"于一体的全流程智能客服解决方案。系统以 RAG 技术为核心，支持 PDF/Markdown 等多种格式文档的结构化导入，通过多路召回与混合检索策略，结合 BGE 重排序模型裁决，最终由大语言模型生成高质量答案，并借助 SSE（Server-Sent Events）实现实时流式输出。

### 核心场景

- 企业知识库问答
- 智能客服
- 专业领域咨询（法律 / 金融 / 政务）
- 文档助手
- 教育答疑
- 搜索增强

---

## 系统架构

```
┌──────────────────────────────────────────────────────┐
│                    用户入口层                          │
│     import.html (文件导入)    chat.html (智能问答)      │
└────────────┬──────────────────────┬──────────────────┘
             │                      │
┌────────────▼──────────┐  ┌────────▼─────────────────┐
│  知识导入流水线         │  │  知识检索流水线             │
│  (Import Pipeline)    │  │  (Query Pipeline)        │
├───────────────────────┤  ├──────────────────────────┤
│ 1. PDF结构化解析       │  │ 1. 意图识别与商品名确认     │
│ 2. 多模态图片理解       │  │ 2. 多路召回 ────────────┐ │
│ 3. 智能文档切片         │  │   ├─ 混合向量检索        │ │
│ 4. 商品名识别           │  │   ├─ HyDE假设检索        │ │
│ 5. BGE-M3混合向量化    │  │   ├─ MCP联网搜索        │ │
│ 6. Milvus幂等入库      │  │   └─ 知识图谱查询        │ │
│                       │  │ 3. RRF融合 + Rerank重排   │ │
│                       │  │ 4. LLM生成 + SSE流式输出   │ │
└───────────┬───────────┘  └───────────┬──────────────┘
            │                          │
┌───────────▼──────────────────────────▼──────────────┐
│                    基础设施层                          │
│  Milvus (向量库)  MongoDB (历史)  MinIO (文件)        │
│  Neo4j (图谱)    BGE-M3 (Embedding)  BGE-Reranker    │
└──────────────────────────────────────────────────────┘
```

---

## 技术栈

| 类别 | 技术选型 |
|------|---------|
| **Web 框架** | FastAPI + Uvicorn（异步 ASGI） |
| **工作流编排** | LangGraph（有状态图工作流） |
| **向量数据库** | Milvus（稠密 + 稀疏混合检索） |
| **图数据库** | Neo4j（知识图谱，预留） |
| **文档数据库** | MongoDB（对话历史持久化） |
| **对象存储** | MinIO（文件持久化） |
| **大语言模型** | 阿里云百炼 Qwen-Flash / Qwen3-VL-Flash（兼容 OpenAI API） |
| **Embedding 模型** | BAAI/bge-m3（稠密 1024 维 + 稀疏双向量） |
| **Reranker 模型** | BAAI/bge-reranker-large |
| **PDF 解析** | MinerU API（版面语义重建） |
| **联网搜索** | 阿里云百炼 MCP WebSearch |
| **前端** | 原生 HTML/CSS/JavaScript（零框架依赖） |
| **包管理** | UV（Python 包管理） |

---

## 项目结构

```
RAG/
├── app/                          # 主应用程序
│   ├── clients/                  # 数据库客户端 (Milvus/MinIO/MongoDB/Neo4j)
│   ├── conf/                     # 配置类 (LLM/Embedding/Milvus/Reranker/MCP)
│   ├── core/                     # 核心工具 (日志/Prompt加载)
│   ├── lm/                       # 语言模型工具 (Embedding/LLM/Reranker)
│   ├── utils/                    # 工具函数 (SSE/任务管理/路径处理)
│   ├── import_process/           # 知识库导入流水线
│   │   ├── agent/nodes/          # 7个LangGraph处理节点
│   │   ├── agent/main_graph.py   # 导入工作流编排
│   │   ├── agent/state.py        # 状态定义
│   │   ├── api/                  # 导入服务 API
│   │   └── page/import.html      # 导入前端页面
│   ├── query_process/            # 知识库检索流水线
│   │   ├── agent/nodes/          # 10个LangGraph处理节点
│   │   ├── agent/main_graph.py   # 检索工作流编排
│   │   ├── agent/state.py        # 状态定义
│   │   ├── api/                  # 查询服务 API
│   │   └── page/chat.html        # 聊天前端页面
│   └── tool/                     # 模型下载工具
├── prompts/                      # LLM 提示词模板
├── RAG/                          # 项目详细文档（22篇）
├── doc/                          # 测试用文档
├── test/                         # 测试脚本
├── output/                       # 运行输出（按日期组织）
├── logs/                         # 日志文件
├── .env                          # 环境变量配置
├── pyproject.toml                # 项目依赖配置
└── uv.lock                       # 依赖锁文件
```

---

## 快速开始

### 前置依赖

在启动项目之前，请确保以下服务已正确安装并运行：

- **Milvus** 向量数据库（必需）
- **MongoDB**（必需，用于存储对话历史）
- **MinIO** 对象存储（可选，用于文件持久化）
- **Neo4j** 图数据库（可选，用于知识图谱查询）
- **阿里云百炼 API 密钥**（必需，用于 LLM 调用和 MCP 联网搜索）

### 1. 克隆项目

```bash
git clone https://github.com/lvrongfu/RAG.git
cd RAG
```

### 2. 安装依赖

```bash
uv sync
```

### 3. 配置环境变量

编辑 `.env` 文件，填入正确的服务地址和 API 密钥：

```bash
# LLM 配置
DASHSCOPE_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
DASHSCOPE_API_KEY=your_api_key_here

# Milvus 连接
MILVUS_URL=http://localhost:19530
CHUNKS_COLLECTION=rag_chunks

# MongoDB 连接
MONGODB_URL=mongodb://localhost:27017

# MinIO 连接（可选）
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=your_minio_key
MINIO_SECRET_KEY=your_minio_secret

# BGE-M3 模型路径
BGE_M3_MODEL_PATH=/path/to/bge-m3

# BGE-Reranker 模型路径
BGE_RERANKER_MODEL_PATH=/path/to/bge-reranker

# 其他配置见 .env 文件
```

### 4. 启动服务

**导入服务**（文件上传与知识库构建，默认端口 8007）：

```bash
uvicorn app.import_process.api.file_import_service:app --host 127.0.0.1 --port 8007
```

访问导入页面：http://localhost:8007/import.html

**查询服务**（智能问答，默认端口 8001）：

```bash
uvicorn app.query_process.api.query_service:app --host 127.0.0.1 --port 8001
```

访问聊天页面：http://localhost:8001/chat.html

---

## 核心能力

### 知识库导入（Indexing）

| 节点 | 功能 | 说明 |
|------|------|------|
| node_entry | 入口分发 | 文件校验、格式识别、PDF/MD路由分支 |
| node_pdf_to_md | PDF 结构化解析 | 基于 MinerU API，实现版面语义重建 |
| node_md_img | 图片处理 | 提取 MD 图片、上传 MinIO、路径修复 |
| node_document_split | 智能文档切片 | 按语义边界切分，带 overlap 保证上下文连贯 |
| node_item_name_recognition | 商品名识别 | LLM 提取商品名称/型号 |
| node_bge_embedding | 混合向量化 | BGE-M3 生成稠密(1024维)+稀疏向量 |
| node_import_milvus | 向量入库 | 幂等写入 Milvus，自动建表 |

### 知识库检索（Retrieval & Generation）

| 节点 | 功能 | 说明 |
|------|------|------|
| node_item_name_confirm | 意图识别 | LLM 提取商品名，向量确认，支持反问 |
| node_search_embedding | 混合向量检索 | 稠密+稀疏混合搜索，item_name 过滤 |
| node_search_embedding_hyde | HyDE 检索 | 假设性文档增强，提升召回覆盖 |
| node_web_search_mcp | 联网搜索 | MCP WebSearch 实时网络信息补充 |
| node_query_kg | 知识图谱查询 | Neo4j 结构化知识（预留） |
| node_rrf | 倒数排名融合 | 多路召回结果加权融合、去重 |
| node_rerank | 重排序裁决 | BGE-Reranker 精细评分、断崖截断 |
| node_answer_output | 答案生成 | LLM 流式生成 + SSE 实时推送 |

---

## API 接口

### 导入服务 (port 8007)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/import.html` | 导入前端页面 |
| POST | `/upload` | 上传文件（多文件支持），返回 task_ids |
| GET | `/status/{task_id}` | 查询任务处理进度 |

### 查询服务 (port 8001)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/chat.html` | 聊天前端页面 |
| GET | `/health` | 服务健康检查 |
| POST | `/query` | 提交查询（支持流式/同步） |
| GET | `/stream/{session_id}` | SSE 流式接收结果 |
| GET | `/history/{session_id}` | 获取对话历史 |
| DELETE | `/history/{session_id}` | 清空对话历史 |

---

## 关键技术设计

### 混合向量检索

- **稠密向量（Dense）**：BGE-M3 生成 1024 维语义向量，COSINE 相似度，负责语义理解与同义泛化
- **稀疏向量（Sparse）**：BGE-M3 生成词权重向量，IP 内积相似度，负责关键词精确匹配
- **加权融合**：默认稠密 : 稀疏 = 0.8 : 0.2，兼顾语义广覆盖与关键词高精度

### 多路召回 + RRF 融合

并行执行四路检索（向量搜索 / HyDE / 网络搜索 / 知识图谱），通过倒数排名融合（RRF）算法统一排序，取各路的交集与并集，保证召回覆盖率。

### 断崖式 Top-K 截断

Reranker 重排序后，动态检测相邻文档得分断崖（分数落差超过阈值），自动截断低相关文档，避免噪声干扰 LLM 推理。

### 幂等性写入

Milvus 入库前基于 `item_name` 删除旧数据，确保同一商品多次导入只保留最新版本，避免数据重复。

### HyDE（Hypothetical Document Embeddings）

先由 LLM 生成假设性答案文档，再对该文档进行向量检索。当用户问题与知识库表述存在语义鸿沟时，HyDE 可显著提升召回效果。

---

## 项目文档

详细设计文档见 [RAG/](./RAG/) 目录：

- [01【掌柜智库】项目简介](./RAG/01【掌柜智库】项目简介.md)
- [02【掌柜智库】模块流程设计](./RAG/02【掌柜智库】模块流程设计.md)
- [03【掌柜智库】环境准备](./RAG/03【掌柜智库】环境准备.md)
- 04-06 导入流程详设
- 07-09 检索流程详设

---

## License

MIT License

---

## 致谢

本项目基于以下开源技术构建：

- [LangGraph](https://github.com/langchain-ai/langgraph) — 有状态工作流编排
- [Milvus](https://milvus.io/) — 高性能向量数据库
- [BGE-M3](https://huggingface.co/BAAI/bge-m3) — 多语言混合 Embedding 模型
- [BGE-Reranker](https://huggingface.co/BAAI/bge-reranker-large) — 高精度重排序模型
- [MinerU](https://github.com/opendatalab/MinerU) — PDF 结构化解析引擎
- [FastAPI](https://fastapi.tiangolo.com/) — 现代 Python Web 框架
