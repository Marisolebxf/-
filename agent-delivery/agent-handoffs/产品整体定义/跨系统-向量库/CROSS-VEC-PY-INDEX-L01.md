# CROSS-VEC-PY-INDEX-L01 · 产业锚点索引（embed/rebuild + embed/search）

> 派单包 `派单/CROSS-VEC-PY-INDEX-L01-派单包.md`；总控 §0 #4 #5 #11 #16 / §4 第 2 行；设计 `03-详细设计.md` §0–§2、`02-概要设计.md` §1.1。
> **本叶最重要的两条**：①「客户端前缀守卫」已落成硬闸（`assert_owned_collection`，`aip_kb_1` 类名字一律抛错，含单测）；②真连了现网 `10.50.69.111:19530`，**真建了** collection `gkxlumen_industry_anchor`（1516 条锚点），三个别的系统的 collection 一个没动。
> **本轮 embedding 是字面哈希向量，不是语义模型**（仓内无文本模型，见 §偏离 2）。`model_version` 写的是实际用的算法名，不是编的模型名。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控段 B；lock 24h；接单时已 claimed + in_progress |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 新增 3 个文件（1 算法模块 + 1 路由 + 1 单测），**零新依赖**：Milvus 走 2.4 HTTP v2 + stdlib `urllib`（不引 pymilvus），向量化用 stdlib `hashlib.blake2b`（不引 numpy / sentence-transformers）。VID 映射直接复用 `graph_project.map_graph`，别名拆词复用 `polan.graph.entity.split_anchor_tokens`（与 L1 对码同源），响应包用仓内 `response.ok/error`，DWD 只读用 `demo_guard.connect_chain_readonly`。未用 YAGNI 跳过：架构铁律、honesty、前缀守卫、handoff、可观测（沿用仓内 `current_trace_id`）。一处 `ponytail:` 注释标了已知天花板（前缀取自 env，账号级隔离仍待运维开鉴权）。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 单仓单叶，本机未挂 Headroom |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `02-概要设计.md` **§1.1**（建库_产业链灌数 vs 消费_政策企业等灌数）；另对照 §2 调用链 |
| 图 diff | **边不变**：`C 上图 VID 稳定 → D embed/rebuild 一次 → E Milvus` 这条实线由本叶实现（`load_anchors` → `rebuild`）；`E -.-> J/K`（跑批 / 按钮）本叶只交 `search` 供其调用，**`jobs/enrich` 不在本叶**（= `CROSS-VEC-JOB-A-L01`），本叶没有加任何「重灌 → rebuild」的边。节点名修正：`E` 实际 collection 名为 `gkxlumen_industry_anchor`（下划线，见 §偏离 1）。 |
| 会签态 | `v0.3-draft`（抄源文件 frontmatter，未自填绿） |

## 范围与实现

**做**：`lumen-algo-py` 内产业锚点索引的建库与检索两条 `/internal` 接口 + 内存回退 + honesty。

1. **路由**（`lumen_algo_service/views/industry.py`，prefix `/internal/industry/embed`）
   - `POST /internal/industry/embed/rebuild`：整库一次重建（drop + create + insert），产业链灌数末段 / 运维调。
   - `POST /internal/industry/embed/search`：单条 top-k，返回候选 `vid` + `name` + `kind` + `industry_code` + `score`。
   - `code≠0` 一律映射 **HTTP 503**（引擎不可用 / 词表为空），前缀守卫命中 → **422**。禁止 200 + 空 items 冒充成功。

2. **词表来源**（`lumen_common/algorithms/industry_embed.py`）
   - 读 demo DWD `industry_chain` + `industry_chain_node`（`connect_chain_readonly`，非 `demo_` 库直接拒），再喂 `graph_project.map_graph(chains, nodes, [], [])`。
   - **VID 不另写生成器**：直接取 map_graph 产出的 `chain:{chain_id}` / `segment:{node_id}`，与上图 Nebula 点同一套码（总控 §0 #8）。
   - 字段（03 §1）：`vid` / `kind` / `name` / `aliases` / `text` / `industry_code` / `model_version` / `index_version` / `graph_source=dwd_chain`。别名 = `split_anchor_tokens(name)`（「半导体与集成电路」→ 半导体 / 集成电路）+ segment 的父链名；`text` = name + 别名拼接。

3. **物理落库**：Milvus 2.4 **HTTP v2**（`/v2/vectordb/collections/{list,create,drop}`、`/entities/{insert,search}`），stdlib `urllib`。collection quick-setup：主键 `vid`（VarChar 128）、向量字段 `vector`、`dim=256`、`metricType=COSINE`，其余字段走 dynamic field。
   - `index_version` = 重建批次时间戳（`%Y%m%d%H%M%S`），随每行写入，`search` 回传命中行的版本。

4. **前缀守卫（总控 §0 #16 硬闸）** → 函数 **`assert_owned_collection(name)`**
   - 位置：`lumen_common/algorithms/industry_embed.py`。
   - `create` / `drop` / `insert` / `search` **每个方法进门第一件事**就是过它（`MilvusHttpStore.create/drop/insert/search`、`MemoryStore.rebuild/search`、以及 `rebuild()` / `search()` 入口对 body 里的 `collection` 参数），不是只在一处或只写注释。
   - 规则：名字必须以 `MILVUS_COLLECTION_PREFIX`（env 真源）开头**且**只含 `[A-Za-z0-9_]`、不以数字开头；否则抛 `CollectionGuardError`。
   - **fail closed**：`MILVUS_COLLECTION_PREFIX` 被清空 / 写成非法字符时，守卫不是放行而是拒绝一切读写（否则守卫等于没有）。
   - 单测：见 §测试结果（`aip_kb_1` / `aip_kb_2` / `spk_id_speaker_embeddings` / 连字符名 / 空名全部必须被拒）。

5. **内存回退 + honesty**
   - `MILVUS_URI` 为空 → `MemoryStore`（进程内），`degraded=true` + `store=memory`（不持久化，必须诚实标注）；本地 pytest 全程走这条，不碰网络。
   - `MILVUS_URI` 有值但连不上 / 协议报错 → `code=1` + `degraded=true` + `items=[]` + `indexed=0`，HTTP 503。**不返回任何 VID**。
   - 词表为空（图点未稳定）→ 直接返回非 0，**不 drop、不 create**，保留上一版 `index_version`（03 §5 / 总控金路径 #4 的语义）。
   - `score` 只是相似度，响应里**没有** `industry_link_code` 字段；定码仍走 `match_industry_anchors` + 图 FETCH（03 §3）。

**不做**（按派单，逐条确认未越界）：`jobs/enrich` 跑批（= `CROSS-VEC-JOB-A-L01`，本叶零代码）、灌链末段挂钩（`CROSS-VEC-CHAIN-HOOK-L01`）、政策重灌调 rebuild（政策侧代码本叶未改一行）、改 Java / 前端、NetworkPolicy / 开鉴权（运维项，DEVOPS-NET 升级项 B）。

## 偏离

| # | 偏离 | 理由 / as-built |
|---|------|-----------------|
| 1 | collection 名用 `gkxlumen_industry_anchor`（下划线），不是 03 §0 的 `gkxlumen-industry-*`；地址用 `10.50.69.111:19530` 不是 88.48 | 沿用 `CROSS-VEC-DEVOPS-NET-L01` 实测结论（连字符被 Milvus `code 1100` 拒；88.48 无监听）。代码里**不硬编码业务前缀**，一律读 env `MILVUS_COLLECTION_PREFIX`（默认值与 k8s 注入值一致）。SAD 文本修订仍是 DEVOPS-NET 升级项 A / C，🟡 未闭。 |
| 2 | **embedding 不是语义模型**：`model_version = hashgram-blake2b-c1c3-256-v0`，`dim=256` | 仓内**没有**已装文本 embedding 模型（`requirements.txt` 无 sentence-transformers / transformers，连 numpy 都不在），按总控 §0 #11「不要凭空装一个」，本轮用 stdlib blake2b 的字符 1/2/3-gram 有符号哈希向量 + L2 归一（配 COSINE）。它**只有字面相似度**，做不到「芯片 ≈ 集成电路」。名字如实写成算法名而不是假模型名。正式模型 / 维度 / 阈值 = **VEC-Q2**，会签后换 `embed_text` + 升 `MODEL_VERSION` + 重跑一次 rebuild 即可（collection 里每行都带 `model_version`，可对账）。 |
| 3 | 用内置 `hash()` 的诱惑没走，改用 `blake2b` | Python 内置 `hash()` 对 str 按进程加盐 → api 进程建的索引、worker 进程检索会落到不同桶，索引直接失效。这属于「lazy 不能省的正确性」。 |
| 4 | `kinds` 子集过滤在客户端做（多取 4 倍再筛），没用 Milvus dynamic field 的 `filter` 表达式 | 少一份对 2.4 动态字段 filter 语法的依赖，代码更短且两个 store 共用同一条路径；锚点千级、`limit ≤ 64`，代价可忽略。 |
| 5 | 没有把 `scripts/milvus_probe.py` 改成共享库供本模块 import | 该脚本要能 `kubectl cp` 到 Pod 里裸跑（README 已写这种用法），一旦 import `lumen_common` 就跑不动了。故探测脚本保持零依赖不动、**继续作为连通性真源**；本模块自带写路径客户端 + 守卫（守卫本来就必须长在业务代码里）。重复的只有 6 行名字规则。 |

未违反硬闸：全程未出现 `amcpdp-` 任何操作（单测里也无该字样）；未生成任何 `chain:` 新码（VID 全部来自 DWD/图）；未把分数写成 `industry_link_code`；未 force push。

## 产物清单

- `lumen-algo-py/lumen_common/algorithms/industry_embed.py`（新增：守卫 + 向量化 + 词表 + 两个 store + `rebuild` / `search`）
- `lumen-algo-py/lumen_algo_service/views/industry.py`（新增：`/internal/industry/embed/{rebuild,search}`）
- `lumen-algo-py/lumen_algo_service/main.py`（挂 router + root modules 列表加 `industry-embed`）
- `lumen-algo-py/tests/test_industry_embed.py`（新增 21 个用例）
- `lumen-algo-py/k8s/README.md`（Milvus 小节补 as-built：已建 collection、唯一写入方、守卫函数名）
- 现网 Milvus：新 collection `gkxlumen_industry_anchor`（见 §验收证据 3）
- 本 handoff

## 验收证据

### 1. pytest（内存回退，不连网）

```text
cd ${GKX_ROOT}/repos/lumen-algo-py
python -m pytest tests/test_industry_embed.py -q
  → 21 passed, 1 warning in 7.18s

python -m pytest -q            # 全仓回归
  → 388 passed, 1 skipped, 1 warning in 240.93s
```

用例覆盖（`tests/test_industry_embed.py`，单测内**无 `amcpdp-` 字样**）：

| 用例 | 断言什么 |
|------|----------|
| `test_guard_rejects_foreign_collection`（参数化 7 例） | `aip_kb_1` / `aip_kb_2` / `spk_id_speaker_embeddings` / `gkxlumen-industry-anchor` / `gkxlumenx_industry_anchor` / `""` / `None` **全部抛 `CollectionGuardError`** |
| `test_guard_accepts_own_collection` | `gkxlumen_industry_anchor` 通过；`default_collection()` 即该名 |
| `test_guard_blocks_write_into_foreign_collection` | 写路径（`store.rebuild("aip_kb_1", …)`）被拒，不只是入口被拒 |
| `test_guard_rejects_empty_prefix_env` | env 前缀被清空时 fail closed（仍拒 `aip_kb_1`） |
| `test_anchor_docs_reuse_graph_vids` | VID = `chain:INB13` / `segment:INB1301`…；别名拆词 + 父链名进别名；`industry_code` 正确 |
| `test_embed_is_deterministic_and_normalized` | 同文本两次向量相同（跨进程可用）、L2 范数 = 1 |
| `test_rebuild_then_search_returns_graph_vid` | rebuild 4 条 → search 命中 `chain:INB13*`；`index_version` 前后一致；内存回退 `degraded=true` |
| `test_search_never_invents_vid_or_link_code` | 返回 VID 必在词表内；item 字段集固定；响应 JSON 里**无** `industry_link_code`、**无**凭空 `chain:INB1303` |
| `test_search_kinds_filter` / `test_search_min_score_drops_weak_hits` | kinds 子集只回 segment；`min_score` 生效 |
| `test_rebuild_empty_vocabulary_keeps_previous_index` | 词表空 → `code≠0`、`indexed=0`、不建空索引 |
| `test_search_empty_query_is_not_a_silent_success` | 空 query 非 0 |
| `test_unreachable_engine_is_degraded_not_fake` | `MILVUS_URI=http://127.0.0.1:1` → rebuild / search 均 `code≠0` + `degraded=true` + 空 items |
| `test_routes_exist_and_degraded_maps_to_503` | 两条路径在 OpenAPI 里；不可用 → HTTP 503 |
| `test_route_rejects_foreign_collection_with_422` | body 传 `collection=aip_kb_1` → 422 且 msg 点名该库 |

### 2. 真连过 19530（本机可直达 `10.50.11.76`，未走跳板）

```text
MILVUS_URI=http://10.50.69.111:19530 python scripts/milvus_probe.py     # 建库前（复用 DEVOPS-NET 脚本）
  TCP 10.50.69.111:19530 ok
  collections=3 本前缀(gkxlumen_industry_)=尚未创建
  只读不动（禁止 drop/insert）：['aip_kb_1', 'aip_kb_2', 'spk_id_speaker_embeddings']
```

词表读取（只读 demo DWD `10.50.11.76:3306` / `demo_gkxlumenx_dwd`）：`load_anchors()` → **1516** 条。

### 3. 真建了 collection（如实记录）

```text
python -c "... rebuild({}) ..."
{"code":0,"data":{"collection":"gkxlumen_industry_anchor","store":"milvus",
 "model_version":"hashgram-blake2b-c1c3-256-v0","dim":256,"metric_type":"COSINE",
 "indexed":1516,"index_version":"20260911002447",
 "kinds":{"chain":102,"segment":1414},"degraded":false}}
```

第二次 rebuild 走 drop + create + insert 全路径，`index_version` 变为 `20260911002540`（证明整库重建幂等、旧批次被顶掉）。

建库后再探测：

```text
python scripts/milvus_probe.py
  TCP 10.50.69.111:19530 ok
  collections=4 本前缀(gkxlumen_industry_)=['gkxlumen_industry_anchor']
  只读不动（禁止 drop/insert）：['aip_kb_1', 'aip_kb_2', 'spk_id_speaker_embeddings']
```

→ **建了的 collection 只有 `gkxlumen_industry_anchor` 一个**；`aip_kb_1` / `aip_kb_2` / `spk_id_speaker_embeddings` 名单前后完全一致，未 drop、未 insert、未读其内容。

### 4. 真检索（对着现网 collection，不是内存）

```text
search({"query":"日均产量超15亿块！上半年我国规上工业企业集成电路产量增长23.1%","top_k":5})
 items: segment:INB18040102 矿产勘探 0.329 / chain:INB1303 集成电路 0.327 /
        chain:INB180401 深海矿产 0.296 / segment:INB1303050301 射频集成电路 0.287 /
        segment:INB17010101 集成电路设计 0.248
 index_version=20260911002447  degraded=false

search({"query":"集成电路","top_k":2})
 items: chain:INB1303 集成电路 1.0 / segment:INB1303050301 射频集成电路 0.804
```

`chain:INB1303 集成电路` 在现网词表里**真实存在**（与 03 §2 示例一致，非伪造）。
**同时暴露了偏离 2 的真实代价**：长文本查询下字面 n-gram 噪声明显（top1 竟是「矿产勘探」）。因此 Job A **必须**按 03 §3 拿 top-k 候选名再过 `match_industry_anchors` 二次对码，**不得直接采 top1 落库**；短查询（如「集成电路」「晶圆制造」）表现正常。

### 5. 未做的事的证明

- `rg "jobs/enrich|amcpdp" lumen_common/algorithms/industry_embed.py lumen_algo_service/views/industry.py tests/test_industry_embed.py` → 无命中（`jobs/enrich` 仅在模块 docstring 里写「不在本模块」这一句说明）。
- 政策 / 企业侧代码、Java、前端零改动（`git show --stat` 仅 5 个文件，见 §CI/CD）。

## 问题清单 / 开放项（升级给 `human:淮政玮`）

| # | 事项 | 谁做 | 状态 |
|---|------|------|------|
| A | **VEC-Q2 正式文本 embedding**：本轮是字面哈希向量，语义能力为 0。要真正解决「芯片≠集成电路」，需拍板模型（本地 bge-small / m3e 之类要装包 + 镜像体积，或走已有 LLM 服务的 embedding 接口）+ 维度 + 阈值 | 架构 + 淮政玮 | 🟡 |
| B | **词表口径**：现网 1516 条锚点里 chain 102 / segment 1414，含「Fabless设计」「其他晶圆制造材料」这类长尾名。是否全部进索引、是否要按 `chain_level` 或发布切面裁剪 | 数据 + 产品 | 🟡 |
| C | **鉴权仍未开**（承接 DEVOPS-NET 升级项 B）：本叶的客户端守卫是**唯一**防线。现在 `gkxlumen_industry_anchor` 已有真数据，别的系统的进程照样能 drop 它 | 运维 + 淮政玮 | 🟡 |
| D | **`index_version` 谁记账**：`search` 只能回传命中行的版本，没有「当前索引版本」查询接口。CHAIN-HOOK 若要报 `industry_index_version` 进度，需要我加一条 `GET .../status`（本叶按 YAGNI 未做） | coordinator 决定要不要建叶 | 🟡 |
| E | 索引未持久化到任何 DWD/ADS 表：collection 被 drop 后只能重跑 rebuild（幂等、代价约 4 秒 / 1516 条），本叶判断无需另建备份表 | — | 已按此实施 |

## 修改内容

| 文件 | 改了什么 |
|------|----------|
| `lumen_common/algorithms/industry_embed.py` | 新增。`assert_owned_collection` 前缀守卫 + `collection_prefix`（env 真源、fail closed）；`embed_text`（blake2b 字符 n-gram，L2 归一）；`anchor_docs` / `load_anchors`（复用 `map_graph` + `split_anchor_tokens`）；`MemoryStore` / `MilvusHttpStore`（HTTP v2，stdlib urllib）；`rebuild()` / `search()` 返回 `ok/error` 包 + `degraded` |
| `lumen_algo_service/views/industry.py` | 新增。两条 POST；`code≠0 → 503`，守卫命中 → 422 |
| `lumen_algo_service/main.py` | `include_router(industry.router)`；root 的 modules 加 `industry-embed` |
| `tests/test_industry_embed.py` | 新增 21 例（守卫 / 词表 / 向量 / rebuild / search / honesty / 路由） |
| `k8s/README.md` | Milvus 小节补 as-built：已建 `gkxlumen_industry_anchor`（dim/metric/主键/条数）、唯一写入方是 rebuild、守卫函数名 |

## 测试结果

- `python -m pytest tests/test_industry_embed.py -q` → **21 passed**（无 `MILVUS_URI`，纯内存回退，不连网）
- `python -m pytest -q` → **388 passed, 1 skipped**（全仓回归，未破坏既有叶；1 skipped 来自既有用例，本叶 21 例无 skip）
- 现网实测：rebuild ×2（1516 条，第二次走 drop 重建）+ search ×4，见 §验收证据 3 / 4
- `python scripts/milvus_probe.py` 建库前 3 个 collection / 建库后 4 个，外部库名单不变

## 遗留风险

- **语义能力为 0**（偏离 2）：谁把本叶的 `search` 当「语义检索」就会失望。Job A / 按钮必须走「top-k 候选名 → `match_industry_anchors` 对码」，禁止直接采 top1。VEC-Q2 定了模型后必须重跑 rebuild。
- **守卫是唯一防线**：现网未开鉴权。任何后续叶新写 Milvus 调用，**必须**经 `MilvusHttpStore` / `assert_owned_collection`，不要另起一个 urllib 调用绕过守卫。
- 内存回退 `MemoryStore._data` 是类级字典，多 worker 进程不共享 —— 只用于本地单测，生产一定注入 `MILVUS_URI`（k8s 已注入，DEVOPS-NET 已 rollout 生效）。
- 本叶未加 OTel 自定义 span（沿用仓内 `current_trace_id` 写进响应）；如需 Milvus 调用耗时 span，留给可观测统一叶，`MILVUS_URI` 作为属性时只记 host:port。
- `gkxlumen_industry_anchor` 里现在是 **demo DWD** 的链表数据（`demo_gkxlumenx_dwd`，符合总控 §0 #9），正式 `gkxlumenx_*` 切换时需重跑 rebuild。

## CI/CD（必填）

- 分支：`lumen-algo-py` `origin/dev`（先 `git pull --ff-only` = already up to date，未 force）
- commit：**`def03e6`**（`def03e64a702b182a9819542b7090ac89054cd72`）`feat(industry): anchor embed rebuild/search on Milvus new collection [agent:algorithm-agent]`
- pipeline URL / ID：push 触发 GitLab CI（`9019505..def03e6 dev -> dev`）；dev 自动 `deploy:api` / `deploy:worker`
- 部署 namespace / 镜像 tag：`dev`；`gkx-lumen-algo-py-api:def03e6*` / `-worker:def03e6*`（由 CI 打 tag）
- K8s rollout：**未在本叶点名验证**（提交时刻 CI 刚触发）。本叶的验收不依赖 Pod：接口逻辑由 pytest 覆盖，现网写入由本机直连 19530 实测（证据 3 / 4）。段 E 由 coordinator 点名 CI deploy 绿。
- dev 测试 URL / 命令与结果：

```text
# 本机（连通 10.50.11.76，命令可原样在 Pod 内跑，env 已注入）
python -c "from lumen_common.algorithms.industry_embed import rebuild; print(rebuild({}))"
  → code=0 indexed=1516 index_version=20260911002447 degraded=false
python -c "from lumen_common.algorithms.industry_embed import search; print(search({'query':'集成电路','top_k':2}))"
  → code=0 items[0]=chain:INB1303 集成电路 score=1.0 degraded=false

# Pod 内 HTTP（待 rollout 后由 coordinator / QA 点）
kubectl -n dev exec deploy/lumen-platform-algo-py -- \
  python -c "import urllib.request,json;print(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8000/internal/industry/embed/search',data=json.dumps({'query':'集成电路'}).encode(),headers={'Content-Type':'application/json'})).read())"
```

## 可观测性（建议）

- OTEL_SERVICE_NAME：未改（`lumen-platform-algo-py` / `-worker`）
- traceId（dev 抽样）：本机运行无 OTel SDK 上下文 → 响应 `trace_id=null`（诚实为 null，未编造）；Pod 内由现有 `TraceHeaderMiddleware` 注入
- Tempo / Loki：无新增埋点；响应体已带 `trace_id` / `collection` / `store` / `index_version` / `degraded`，足够定位「是内存还是真库、哪一批索引」

## 涉及文件

- `lumen-algo-py/lumen_common/algorithms/industry_embed.py`
- `lumen-algo-py/lumen_algo_service/views/industry.py`
- `lumen-algo-py/lumen_algo_service/main.py`
- `lumen-algo-py/tests/test_industry_embed.py`
- `lumen-algo-py/k8s/README.md`
- 本 handoff

## 下游契约（给 CHAIN-HOOK / API-FEIGN / JOB-A）

| 项 | 值 |
|----|-----|
| 路径 | `POST /internal/industry/embed/rebuild`、`POST /internal/industry/embed/search`（**无 `/v1`**，与 02 §4 一致；网关外部前缀仍 `/lumen-algo`） |
| rebuild 请求 | body 可空 `{}`；可选 `collection`（仅本前缀，否则 422）。**无** `dry_run`（整库重建本身幂等） |
| rebuild 响应 `data` | `collection` / `store` / `model_version` / `dim` / `metric_type` / `indexed` / `index_version` / `kinds{chain,segment}` / `degraded` / `trace_id` |
| search 请求 | `{query, top_k=8(≤50), kinds=["chain","segment"], min_score=0.0, collection?}` |
| search 响应 `data` | `items[{vid,name,kind,industry_code,score}]` / `source="industry_embed"` / `model_version` / `index_version` / `degraded` / `collection` / `store` / `trace_id` |
| 失败语义 | 引擎不可用 / 词表空 → **HTTP 503** + `code=1` + `data.degraded=true` + 空 items；collection 名越界 → **422**。Java 侧按金路径 #5 未就绪回 **501** + honesty，**禁止** 200 假 VID |
| 红线 | `score` **不是** `industry_link_code`；响应里没有 link code 字段。定码必须 `match_industry_anchors` + 图 FETCH（03 §3）。LLM 若吐 `chain:` 前缀一律丢弃 |
| CHAIN-HOOK 用法 | 灌链末段、上图 VID 稳定后调 rebuild **一次**；点未稳定 → 本接口自己会返非 0 且不动旧索引，hook 只需照 `code` 决定是否保留上一 `index_version` |
| JOB-A 用法 | 只调 `search`（循环单条），**不得**调 rebuild；`jobs/enrich` 路由本叶未建，属 `CROSS-VEC-JOB-A-L01` |

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python（D1） | ✅ 向量化 / 检索 / 建库全在 `lumen-algo-py`；Java 零改动 |
| 调用链不可越层 | ✅ 仅 `/internal/industry/embed/*`，由 Java Feign 调；前端无直连；Python → Milvus 是唯一到 19530 的边 |
| 图谱仅 Nebula | ✅ 未动 `9669` / `demo_gkx_chain`；VID 复用图上码，向量**不替代建图**、不签发 VID |
| 可观测 | ✅ 沿用 `current_trace_id`，响应带 `trace_id`；未新起 tracer；未把连接串 / 口令写进日志 |
| CI/CD | ✅ push `origin/dev`，未 force；commit 带 `[agent:algorithm-agent]` |
| demo2 只读 / D12 | ✅ 未改任何 `demo-*` 仓、未 merge；lumen 侧只连 Milvus 与 demo **数据库**（`demo_gkxlumenx_dwd`，总控 §0 #9 指定数据面，非 demo 服务调用） |
| 数据策略 | ✅ 只 create/insert 本前缀 collection；`aip_kb_*` / `spk_id_*` 只看名字；未碰 `amcpdp-*`；未写正式 `gkxlumenx_*` |
| D8 / D10 | N/A（无 UI） |
| D9 数据血缘 | N/A（本叶不产出界面统计指标；`model_version` / `index_version` 已随每行落库可追溯） |
| 密钥不入 git | ✅ `MILVUS_TOKEN` 只从 env 读，仓内无口令 |

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 158000 |
| model_used | claude-opus-5-thinking |
| actual_cost | 0.95 |
| cost_warn | green |

口径：coding 默认 75/25 读写比；B 档 `$3/$15` per 1M；`158000×0.75×3/1e6 + 158000×0.25×15/1e6 = 0.95`。
