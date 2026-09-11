# CROSS-VEC-EMBED-SWITCH-L01 · 切 embed_text 到 bge-base-zh-v1.5（DIM 768）+ 重建索引

> 总控 [`CROSS-VEC-长任务总控.md`](./CROSS-VEC-长任务总控.md) §0 #16 #17 #18 #19 / §6.4 步 2 / §6.5；前序 [`CROSS-VEC-PY-INDEX-L01.md`](./CROSS-VEC-PY-INDEX-L01.md) · [`CROSS-VEC-CHAIN-HOOK-L01.md`](./CROSS-VEC-CHAIN-HOOK-L01.md) · [`CROSS-VEC-EMBED-DEPLOY-L01.md`](./CROSS-VEC-EMBED-DEPLOY-L01.md)。
> **本叶最重要的一条**：`embed_text` 已从 stdlib blake2b 切到现网 TEI `bge-base-zh-v1.5`（dim **768**，`MODEL_VERSION=bge-base-zh-v1.5-tei-1.8.3`）。运维式重跑 **一次** rebuild（256→768 drop+create）。search 路径复测「集成电路产量增长23.1%」：**top1 = `chain:INB1303` 集成电路 0.50304**，矿产勘探 0.196573 且不进 top-50。§0 #17 语义缺陷在检索链上修好；**禁止采 top1 定码**仍保留。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控 §6.4 步 2；lock 24h；接单时已 claimed + in_progress |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只改接入点：`DIM` / `MODEL_VERSION` / `embed_text()`（加批量 `embed_texts` + query 前缀）。HTTP 复用仓内已装 `httpx`（connect 5s / read 60s），零新依赖。MemoryStore + `assert_owned_collection` 原样保留。未用 YAGNI 跳过 honesty / 前缀守卫 / dim 校验 / handoff。客户端不再 L2 归一。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 单仓单叶，本机未挂 Headroom |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `02-概要设计.md` §2 调用链（FE → GW → Java → Python `/internal` → Milvus 19530 ∥ TEI 8080） |
| 图 diff | **边已由 EMBED-DEPLOY 加上**：Python → `gkxlumen-embed-tei:8080`。本叶把这条边接到 `embed_text`；未新增 Java / 前端边；未碰 `amcpdp-*` / `aip_kb_*` / `spk_id_*` |
| 会签态 | `v0.3-draft`（抄源文件 frontmatter，未自填绿） |

## 范围与实现

**做**：把产业锚点向量化从字面哈希切到现网 TEI，重跑一次 rebuild，用同一查询证明 §0 #17 在 **search 路径**修好。

1. **接入点**（`lumen_common/algorithms/industry_embed.py`）
   - `DIM=768`；`MODEL_VERSION=bge-base-zh-v1.5-tei-1.8.3`（§6.5 建议值）。
   - `embed_text` / `embed_texts` 调 OpenAI 兼容 `POST {EMBED_BASE_URL}/v1/embeddings`，body `{"model": EMBED_MODEL, "input":[...]}`。
   - **query 侧**加前缀 `为这个句子生成表示以用于检索相关文章：`；**锚点 / doc 侧不加**。
   - TEI 向量**不再**客户端 L2 归一；hashgram 回退仍归一（仅 `EMBED_BASE_URL` 未设）。
   - 批量 32 条/请求、重试 2 次、connect 5s / read 60s；并发按串行批次（≤4）。
   - dim ≠ 768 → `EmbedUnavailable`，禁止截断/填充写入。
   - 端点不可用 / 空响应 → `code=1` + `degraded=true` + 空 items / `indexed=0`，HTTP **503**，禁止假 VID。

2. **保留**
   - `MemoryStore` 回退（`MILVUS_URI` 空 → 进程内，`degraded=true`）。
   - `assert_owned_collection` 仍是 create/drop/insert/search 的第一句（§0 #16 fail-closed）。
   - 不采 top1 写 `industry_link_code`（§0 #17）；search item 字段集不变，无定码字段。

3. **env 注入**（与 `MILVUS_URI` 同表，未新造一套）
   - `EMBED_BASE_URL=http://gkxlumen-embed-tei:8080`
   - `EMBED_MODEL=BAAI/bge-base-zh-v1.5`
   - 可选 `EMBED_API_KEY`（当前无 token；预留 Secret `lumen-algo-embed`）
   - 注入点：`lumen-algo-py/k8s/api.yaml` · `k8s/worker.yaml` · `.env.example` · helm `entanPy.env` / `entanPyWorker.env`

**不做**（按派单逐条确认未越界）：`jobs/enrich` / POLICY-SEARCH / 改 Java / 改前端；未装 torch / transformers / onnxruntime / pymilvus；未再调灌链（CHAIN-HOOK 已挂钩，本叶只运维式 `rebuild()` 一次）；未碰 `aip_kb_*` / `spk_id_*` / `amcpdp-*` / 正式 `gkxlumenx_*`。

## 偏离

| # | 偏离 | 理由 / as-built |
|---|------|-----------------|
| 1 | 本机无 kubectl；TEI 是 ClusterIP。rebuild 经 SSH `88.50` `kubectl port-forward --address 0.0.0.0 svc/gkxlumen-embed-tei 18080:8080`，本机 `EMBED_BASE_URL=http://192.168.88.50:18080` 调 `embed_text` 后写 88.43:19530 | MCP `user-ssh-executor` 本叶可用（台账 L 当时损坏，现已 `ready`）。port-forward 收工已 cancel。未把 TEI 改成 Ingress / NodePort。 |
| 2 | `EMBED_BASE_URL` 未设时仍走 hashgram（dim 768），不是 TEI | 单测「不联网回退路径绿」。生产 k8s 已注入 URL；URL 有值但连不上 → **不**回退哈希，诚实 503。 |
| 3 | 矿产勘探分数 0.196573，与 DEVOPS 裸向量 0.1571 不完全相等 | DEVOPS 比的是四个**短名**的裸 TEI 余弦；本叶 search 的锚点向量是 `name + aliases`。search 路径 top1 仍是集成电路 **0.50304**（与 DEVOPS 0.5030 对齐），矿产勘探不进 top-50。 |
| 4 | helm `values.yaml` 加了 `EMBED_*`，但 `entanPy.enabled=false`，本叶未点 `helm:deploy` | 与 DEVOPS-NET 同表补键；entan 未启用，不影响现网 algo-py。algo-py 的真注入点是 `k8s/api.yaml` / `worker.yaml`（随本仓 CI deploy）。 |

未违反硬闸：守卫 fail-closed；未采 top1 定码；rebuild 失败时不 drop（embed 在 drop 前）；未 force push；未写正式库。

## 产物清单

- `lumen-algo-py/lumen_common/algorithms/industry_embed.py`（`DIM` / `MODEL_VERSION` / TEI `embed_text`）
- `lumen-algo-py/tests/test_industry_embed.py`（+4 例：端点不可用 / dim 错配 / query 前缀 / 路由 503）
- `lumen-algo-py/k8s/api.yaml` · `k8s/worker.yaml` · `k8s/README.md` · `.env.example`
- `lumen-svc-platform/helm/gkxlumen-platform/values.yaml`（`entanPy.env` / `entanPyWorker.env` 同表加 `EMBED_*`）
- 现网 collection `gkxlumen_industry_anchor`：dim 256→768，一次 rebuild
- 本 handoff

## 验收证据

### 1. pytest（不联网）

```text
cd ${GKX_ROOT}/repos/lumen-algo-py
python -m pytest tests/test_industry_embed.py -q
  → 25 passed, 1 warning in 32.56s

python -m pytest -q
  → 399 passed, 1 skipped, 1 warning in 266.54s
```

新增用例：

| 用例 | 断言 |
|------|------|
| `test_embed_endpoint_down_is_degraded_not_fake` | `EMBED_BASE_URL=http://127.0.0.1:1` → rebuild/search `code≠0` + `degraded` + 空 items，**不**走 hashgram 假 VID |
| `test_embed_dim_mismatch_is_error_not_silent_write` | 返回 dim 256 → `EmbedUnavailable`，MemoryStore 不写入 |
| `test_query_prefix_only_on_query_side` | query 请求带指令前缀；doc 侧不加 |
| `test_route_embed_down_maps_to_503` | HTTP 503 + `code=1` + `degraded=true` + 空 items |
| 原 21 例守卫 / MemoryStore / honesty | 仍绿（autouse 清掉 `EMBED_BASE_URL`） |

### 2. 跑前 / 跑后索引

| | `index_version` | `indexed` | `dim` | `model_version` |
|---|---|---|---|---|
| 跑前 | `20260911004738`（CHAIN-HOOK） | 1516 | **256** | `hashgram-blake2b-c1c3-256-v0` |
| 跑后 | **`20260911113702`** | **1516**（102 chain + 1414 segment） | **768** | `bge-base-zh-v1.5-tei-1.8.3` |

```text
# 跑前 describe / stats / query 一行
vector.dim=256  rowCount=1516  index_version=20260911004738  model=hashgram-blake2b-c1c3-256-v0

# 本叶唯一一次 rebuild（经 embed_text 批量 32 + MilvusHttpStore.drop+create）
REBUILD_ELAPSED 168.3s
{"code":0,"data":{"collection":"gkxlumen_industry_anchor","store":"milvus",
 "model_version":"bge-base-zh-v1.5-tei-1.8.3","dim":768,"indexed":1516,
 "index_version":"20260911113702","kinds":{"chain":102,"segment":1414},"degraded":false}}

# 跑后 describe
vector.dim=768
```

### 3. 对比查询（search 路径，不是裸 curl）

`search({"query":"集成电路产量增长23.1%","top_k":8})`，query 经 `embed_text(..., is_query=True)`：

| rank | vid | name | score |
|------|-----|------|------:|
| 1 | `chain:INB1303` | 集成电路 | **0.50304** |
| 2 | `segment:INB17010107` | 第三代半导体 | 0.434562 |
| 3 | `segment:INB17010102` | 晶圆制造 | 0.428947 |
| 4 | `chain:INB170101` | 半导体与集成电路 | 0.425768 |
| 5 | `segment:INB1303050301` | 射频集成电路 | 0.422609 |
| 6 | `segment:INB17010101` | 集成电路设计 | 0.420591 |
| 7 | `segment:INB17010105` | 智能传感器 | 0.417065 |
| 8 | `segment:INB17010108` | MEMS中试 | 0.41621 |

同 query 向量 × 索引行（仍是 `embed_text` + 已写入量，不是另写模型）：

| name | vid | score |
|------|-----|------:|
| 集成电路 | `chain:INB1303` | 0.50304 |
| 矿产勘探 | `segment:INB18040102` | **0.196573**（**不在 top-50**） |
| 深海矿产 | `chain:INB180401` | 0.174545 |

对照 PY-INDEX 字面哈希：top1 矿产勘探 0.329 / 集成电路 0.327。现 top1 集成电路，分差约 **2.6×**。DEVOPS 裸短名：集成电路 0.5030 / 半导体制造 0.3768 / 矿产勘探 0.1571。词表无「半导体制造」整名（有「晶圆制造」「第三代半导体」等同族，均高于矿产）。

`index_version=20260911113702`，`degraded=false`。响应无 `industry_link_code`。

### 4. 他人库未动

```text
跑前 LIST: aip_kb_1, aip_kb_2, spk_id_speaker_embeddings, aip_portal_service_vec, gkxlumen_industry_anchor
跑后 LIST: 同上五张，无增删
```

`aip_portal_service_vec` 是本叶开工前已存在的第三方库，只看名字。

## 问题清单 / 开放项

| # | 事项 | 谁做 | 状态 |
|---|------|------|------|
| A | algo-py Pod 要吃到 `EMBED_*` 须等本仓 CI `deploy:api` / `deploy:worker` | CI / devops | 🟡 随 push |
| B | helm `entanPy` 仍 `enabled=false`，台账 D 的 `helm:deploy` 未点 | devops | 🟡 既有 |
| C | §0 #17 / #19 仍有效：POLICY-SEARCH / JOB-A 解 blocked 后仍须 top-k→`match_industry_anchors`，且不得与灌链并排 | coordinator | 本叶不改那两张单 |
| D | PY-INDEX 开放项 D（`GET .../status`）仍未闭 | 算法低优先 | 🟡 |

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 只改 `lumen-algo-py` 的 `/internal` 向量化；Java / 前端零改动（helm 只加 env 键） |
| 调用链不可越层 | ✅ 前端 / Java 仍只打 `/internal/industry/embed/*`；Python → TEI 8080 是算法侧边 |
| 图谱仅 Nebula | ✅ 未动 9669；VID 仍来自 `map_graph` |
| 可观测 | ✅ 沿用 `current_trace_id`；embed 日志不写全文 |
| CI/CD | ✅ push `origin/dev`，未 force；commit `[agent:algorithm-agent]` |
| D12 | ✅ 未改 demo-* 仓、未调 demo 服务 |
| 数据策略 | ✅ 只 drop+create 本前缀；未写正式 `gkxlumenx_*` |
| 密钥不入 git | ✅ `EMBED_API_KEY` 只从 env / 预留 Secret 读 |
| D8 / D9 / D10 | N/A（无 UI / 无指标卡） |

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 145000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.87 |
| cost_warn | green |

口径：coding 默认 75/25 读写比；B 档 `$3/$15` per 1M；`145000×0.75×3/1e6 + 145000×0.25×15/1e6 = 0.87`。

## CI/CD（必填）

- 分支：`lumen-algo-py` `origin/dev`（先 `git pull --ff-only` = `1646874..fdb91b4`，含 CHAIN-HOOK HEAD，未 force）
- commit：**`c41233e`**（`c41233e1564cf5a2d8b8976c1c72a689da19aa7c`）`feat(industry): switch embed_text to TEI bge-base-zh-v1.5 dim 768 [agent:algorithm-agent]`
- pipeline：push 触发 `deploy:api` / `deploy:worker`
- K8s rollout：本叶验收不依赖新镜像（rebuild 用本机新代码 + port-forward TEI + 直连 19530）
- helm：`lumen-svc-platform` 同批加 `EMBED_*`，未点 `helm:deploy`

## 对 POLICY-SEARCH / JOB-A

§6.4 两步：**① EMBED-DEPLOY = `ready_to_sign`（端点就绪）② 本叶交卷（切模型 + 重建）**。语义 hold 的技术条件已齐。`POLICY-SEARCH` / `JOB-A` 此刻仍是 `blocked`——**本叶不改它们的状态**，请 coordinator 按闸门解 blocked。§0 #17（禁止采 top1 定码）与 #19（JOB-A 不得与灌链并排）**仍然有效**。
