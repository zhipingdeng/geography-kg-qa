# 地理旅游知识图谱问答系统 (Geography KG-QA)

基于 OwnThink 知识图谱中地理领域标签数据的 RAG 问答系统，专注地理、旅游、景点等领域的知识问答。

采用混合检索（向量 + BM25 + 图 + HyDE）+ RRF 融合排序。

## 技术栈

| 层级 | 技术 | 用途 |
|------|------|------|
| 前端 | Vue 3 + TypeScript + Vite + Tailwind CSS | SPA 界面 |
| 可视化 | D3.js | 知识图谱力导向图 |
| 后端 | FastAPI + uvicorn (4 workers) | API 服务 + 并发 |
| 图数据库 | Neo4j 5 | 知识图谱存储 |
| 向量数据库 | Milvus 2.4 | 语义向量检索 |
| 关系数据库 | MySQL 8 | 用户认证 |
| Embedding | Ollama bge-m3 (1024维) | 文本向量化 |
| LLM | mimo-v2.5-pro (小米 MiMo) | 回答生成 + HyDE + 查询重写 |
| 认证 | bcrypt + JWT | 注册/登录/鉴权 |
| 部署 | Docker Compose | 一键启动 7 个服务 |

## 数据领域

从 OwnThink 通用百科知识图谱中按以下标签过滤，专注地理领域：

- **地理** — 自然地理、人文地理、地理现象等
- **旅游** — 旅游景点、旅游路线、旅游文化等
- **景点** — 自然景观、人文景观、世界遗产等
- **山脉** — 高山、丘陵、高原等
- **河流** — 大江大河、湖泊、瀑布等
- **湖泊** — 淡水湖、咸水湖、人工湖等
- **国家** — 世界各国、政治、经济等
- **城市** — 大都市、古城、新兴城市等

## 系统架构

```
用户问题
  │
  ▼
┌─────────────┐
│ 查询重写     │ ← LLM 生成多个查询变体
└──────┬──────┘
       │
  ┌────┼────────────┐
  ▼    ▼            ▼
┌────┐┌────┐┌──────┐┌──────┐
│向量││HyDE││ BM25 ││ 图   │
│检索││检索││关键字 ││检索  │
└──┬─┘└──┬─┘└──┬───┘└──┬───┘
   │     │     │       │
   └──┬──┘     └───┬───┘
      ▼            ▼
   ┌──────────────────┐
   │  RRF 融合排序     │
   └────────┬─────────┘
            ▼
   ┌──────────────────┐
   │ LLM 生成回答      │ ← 基于检索文档 + 知识图谱
   └────────┬─────────┘
            ▼
        回答 + 引用
```

## 项目结构

```
geography-kg-qa/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # API 端点 (auth, qa, knowledge, health)
│   │   ├── data/            # OwnThink 解析器 + Neo4j 导入器
│   │   ├── database/        # Neo4j + MySQL + Milvus 客户端
│   │   ├── eval/            # 评估框架
│   │   ├── models/          # SQLAlchemy 模型 (User)
│   │   ├── rag/             # RAG 模块
│   │   ├── qa/              # QA 模块
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Auth 服务
│   │   ├── config.py        # 配置管理
│   │   └── main.py          # FastAPI 入口
│   ├── scripts/
│   │   ├── import_ownthink.py      # 导入地理标签实体到 Neo4j
│   │   ├── create_relationships.py # 创建实体间关系
│   │   ├── build_index.py          # 构建 Milvus + BM25 索引
│   │   ├── evaluate.py             # RAG 评估脚本
│   │   └── load_test.py            # 并发压测脚本
│   ├── tests/               # 测试用例
│   ├── Dockerfile
│   └── docker-entrypoint.sh
├── frontend/
│   ├── src/
│   │   ├── api/             # Axios HTTP 客户端
│   │   ├── views/           # Login, Home(问答), Knowledge(图谱)
│   │   ├── components/      # Header 导航
│   │   ├── stores/          # Pinia 认证状态
│   │   └── router/          # 路由守卫
│   ├── Dockerfile
│   └── nginx.conf           # Nginx 反向代理
├── docker-compose.yml       # 一键部署 7 个服务
├── .env                     # 环境变量
└── pyproject.toml           # Python 依赖
```

## 快速开始

### 方式一：Docker Compose 一键部署（推荐）

```bash
git clone <repo-url>
cd geography-kg-qa

# 配置 LLM API Key
# 编辑 .env 设置 LLM_API_KEY

# 一键启动（自动构建镜像 + 导入数据 + 构建索引）
docker-compose up -d
```

启动后访问：
- 前端: http://localhost:83
- 后端 API: http://localhost:8003
- API 文档: http://localhost:8003/docs
- Neo4j: http://localhost:7475 (neo4j/your_password)

### 方式二：本地开发

```bash
# 1. 启动数据库
docker-compose up -d neo4j mysql etcd minio milvus-standalone

# 2. 后端
conda create -n geography-kg-qa python=3.11 -y
conda activate geography-kg-qa
pip install -e ".[dev]"

# 导入地理领域数据（首次）
python backend/scripts/import_ownthink.py --tags "地理,旅游,景点,山脉,河流,湖泊,国家,城市"
python backend/scripts/create_relationships.py
python backend/scripts/build_index.py

# 启动
cd backend && python run.py

# 3. 前端
cd frontend
npm install --registry https://registry.npmjs.org
npm run dev
```

## API 端点

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | /api/v1/auth/register | 注册 | ✗ |
| POST | /api/v1/auth/login | 登录 | ✗ |
| GET | /api/v1/auth/me | 当前用户 | ✓ |
| POST | /api/v1/qa | 知识问答（混合检索） | ✓ |
| GET | /api/v1/knowledge/graph | 知识图谱数据 | ✓ |
| GET | /api/v1/health | 健康检查 | ✗ |

## Docker 服务

| 服务 | 端口 | 用途 |
|------|------|------|
| frontend-geography-kg-qa | 83 | Nginx + Vue 3 |
| backend-geography-kg-qa | 8003 | FastAPI (4 workers) |
| neo4j-geography-kg-qa | 7688/7475 | 知识图谱 |
| mysql-geography-kg-qa | 3308 | 用户认证 |
| milvus-geography-kg-qa | 19531 | 向量检索 |
| etcd-geography-kg-qa | 内部 | Milvus 元数据 |
| minio-geography-kg-qa | 内部 | Milvus 对象存储 |

## 测试

```bash
cd backend && pytest tests/ -v
```

## License

MIT