# script — 入向量库脚本由 GDF 配置

入图和入向量库分开。

| 做什么 | 谁做 | 用哪份 |
|---|---|---|
| 上图 | GDF 只触发燕大知识图谱引擎的调度任务并轮询终态 | 不配 `graph_project.py`、`chain_routes.py` |
| 入向量库 | GDF 在平台上配置本目录的 `industry_embed.py`，直接写 Milvus | `rebuild` |

入图调度任务轮询到成功之后，再跑入向量库作业。每日批一次。不要逐行 embed，不要调用 `POST /internal/industry/embed/rebuild`。

## 入向量库作业

脚本：`industry_embed.py` 的 `rebuild`。请求体可空。成功时 `code=0`，`data.index_version` 为 `yyyyMMddHHmmss`，`data.indexed` 为写入条数。`code≠0` 当日回执写 `skip`，保留上一版索引。

写入目标只有 Milvus 库 `gkxlumen`、集合 `gkxlumen_industry_anchor`（前缀 `gkxlumen_industry_`，768 维，COSINE）。词表读正式库 `gkxlumenx_dwd` 的 `industry_chain`、`industry_chain_node`。

副本里有两处还是 demo，配到 GDF 平台时先改掉，再执行：

1. `DB_NAME` 现在是 `default`。改成 `gkxlumen`。不改就会 drop 库 `default` 里 demo 正在用的同名集合。
2. `load_anchors` 现在走 `connect_chain_readonly`，只读 demo 链树。改成读 `gkxlumenx_dwd`。GDF 不读 demo 库。

环境：`MILVUS_URI`、`MILVUS_COLLECTION_PREFIX=gkxlumen_industry_`、`EMBED_BASE_URL`（代理机 `http://10.50.69.111:30903`，脚本自行补 `/v1/embeddings`）。口令不进本包。

副本依赖 `lumen_common`，在本目录不能单独运行。配作业时带上它实际 import 的模块。

| 文件 | 看哪里 | GDF 是否配置 |
|---|---|---|
| `industry_embed.py` | `rebuild`；`index_version` = `yyyyMMddHHmmss`；`anchor_docs` | 配置，直接入向量库 |
| `industry_embed_routes.py` | `POST /internal/industry/embed/rebuild` | 不配置。这是我方 HTTP，GDF 跑脚本 |
| `graph_project.py` | 入图实现。其中 `_index_skip_reason` 比较的是图上顶点数，入向量库不用 | 不配置 |
| `chain_routes.py` | `POST /internal/v1/chain/graph/project` | 不配置 |
