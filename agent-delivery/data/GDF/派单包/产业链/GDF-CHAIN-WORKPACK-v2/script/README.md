# script — 入向量库脚本由 GDF 配置

入图和入向量库分开。

| 做什么 | 谁做 | 用哪份 |
|---|---|---|
| 上图 | GDF 只触发燕大知识图谱引擎的调度任务并轮询终态 | 不配 `graph_project.py`、`chain_routes.py` |
| 入向量库 | GDF 在平台上配置本目录的 `industry_embed.py`，直接写 Milvus | `rebuild` |

入图与入向量库**互不依赖**。Wave B `CHAIN-B1-TREE` 当日 `success` 后即可跑入向量库作业，**不等**入图调度任务终态。每日批至多一次。不要逐行 embed，不要调用 `POST /internal/industry/embed/rebuild`。

## 入向量库作业

脚本：`industry_embed.py` 的 `rebuild`。请求体可空。成功时 `code=0`，`data.index_version` 为 `yyyyMMddHHmmss`，`data.indexed` 为写入条数。`code≠0` 当日回执写 `skip`，保留上一版索引。

**2026-11-03 路线 A**：本脚本已全环境变量化，**不再依赖 `lumen_common`**，配作业只设环境变量即可，**不必改代码**。

默认写入：Milvus 库 `gkxlumen`、集合 `gkxlumen_industry_anchor`（前缀 `gkxlumen_industry_`，768 维，COSINE）。词表读 `gkxlumenx_dwd.industry_chain` / `industry_chain_node`。

### 必配环境变量

| 变量 | 含义 | 示例 | 必填 |
|---|---|---|---|
| `MILVUS_URI` | Milvus HTTP 入口 | `http://…:19530` | 正式作业必填；空则内存回退（degraded） |
| `MILVUS_DB_NAME`（或 `DB_NAME`） | Milvus 库名 | `gkxlumen` | **必填**；未配或 `default` 会拒绝写入（防误伤 demo） |
| `MILVUS_COLLECTION_PREFIX` | 集合前缀守卫 | `gkxlumen_industry_` | 建议填；默认同上 |
| `EMBED_BASE_URL` | TEI 基址（脚本补 `/v1/embeddings`） | `http://10.50.69.111:30903` | 正式必填；空则 hashgram 仅自检 |
| `MYSQL_HOST`（或 `CHAIN_MYSQL_HOST`） | 词表 MySQL | 正式库主机 | 读锚点必填 |
| `MYSQL_USER` / `MYSQL_PASSWORD` | 词表账号 | — | 读锚点必填；口令不进本包 |

### 可选环境变量

| 变量 | 默认 | 含义 |
|---|---|---|
| `MILVUS_COLLECTION_SUFFIX` | `anchor` | 集合后缀；完整名=前缀+后缀 |
| `MILVUS_METRIC_TYPE` | `COSINE` | 度量 |
| `MILVUS_TOKEN` | 空 | Milvus Bearer（若开鉴权） |
| `ALLOW_MILVUS_DB_DEFAULT` | 关 | 仅调试允许 `dbName=default` |
| `CHAIN_DWD_SCHEMA` | `gkxlumenx_dwd` | 词表库；`demo_` 前缀默认拒绝 |
| `ALLOW_DEMO_DWD_SCHEMA` | 关 | 仅调试允许 demo 词表库 |
| `CHAIN_TABLE` | `industry_chain` | 链表名 |
| `CHAIN_NODE_TABLE` | `industry_chain_node` | 节点表名 |
| `MYSQL_PORT` | `3306` | 端口 |
| `MYSQL_CHARSET` | `utf8mb4` | 字符集 |
| `EMBED_MODEL` | `BAAI/bge-base-zh-v1.5` | TEI model 名 |
| `EMBED_MODEL_VERSION` | `bge-base-zh-v1.5-tei-1.8.3` | 写入元数据 |
| `EMBED_DIM` | `768` | 维数 |
| `EMBED_BATCH` | `32` | 批大小 |
| `EMBED_API_KEY` | 空 | TEI Bearer（若需要） |
| `TRACE_ID` / `OTEL_TRACE_ID` | 空 | 回执 trace |

运行时依赖：`httpx`、`pymysql`（标准库其余）。自检：`python industry_embed.py`。

| 文件 | 看哪里 | GDF 是否配置 |
|---|---|---|
| `industry_embed.py` | `rebuild`；`index_version` = `yyyyMMddHHmmss`；参数全走环境变量 | **配置**，直接入向量库 |
| `industry_embed_routes.py` | `POST /internal/industry/embed/rebuild` | 不配置。这是我方 HTTP，GDF 跑脚本 |
| `graph_project.py` | 入图实现 | 不配置（不进 GDF DAG） |
| `chain_routes.py` | `POST /internal/v1/chain/graph/project` | 不配置 |
