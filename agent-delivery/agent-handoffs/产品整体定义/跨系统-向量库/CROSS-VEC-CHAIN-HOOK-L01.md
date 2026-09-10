# CROSS-VEC-CHAIN-HOOK-L01 · 灌链末段挂钩（上图 VID 稳定 → 一次 embed/rebuild）

> 派单包 `派单/CROSS-VEC-CHAIN-HOOK-L01-派单包.md`；总控 §0 #2 #3 #4 #5 #16 #17 / §4 第 4 行；设计 `02-概要设计.md` §1.1（建库切面 vs 消费切面）；前序契约 `CROSS-VEC-PY-INDEX-L01.md` §下游契约。
> **本叶最重要的三条**：①挂钩点就一个 —— `project_graph()` 末尾，上图 `INSERT VERTEX/EDGE` 成功之后，**整条灌链再无第二处 rebuild**（grep + 单测双证）；②锚点直接复用本次上图读到的**同一批 DWD 行**，索引与图点同源、也省掉第二次读库；③真跑过完整灌链（20545 点 / 132937 边上图 → rebuild 1516 条），`index_version` 从 `20260911002540` 前进到 `20260911004738`。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控段 C；lock 24h；接单时已 claimed + in_progress |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | **零新文件、零新依赖**：改 2 个已有文件（`graph_project.py` +77 行 / `test_chain_graph.py` +101 行）。爬梯到第 2 级就停 —— 建库能力 PY-INDEX 已交（`rebuild(payload, anchors=...)`），本叶只是在既有 `project_graph` 末尾接一根线，没有新建 hook 框架 / 事件总线 / 配置开关。锚点复用本次上图的 `chains` / `nodes` 行 + `anchor_docs()`，不重读库、不重写 VID 生成。未用 YAGNI 跳过：honesty（失败三态 ok/skipped/failed）、前缀守卫（走 PY-INDEX 的 `assert_owned_collection`，本叶零新 Milvus 调用）、handoff、可观测（沿用响应内 `trace_id`）。无 `ponytail:` 新注释（本叶没有留已知天花板；PY-INDEX 那条守卫天花板注释仍在原处）。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 单仓单叶，本机未挂 Headroom |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `02-概要设计.md` **§1.1**（`chainIngest` 建库_产业链灌数 vs `bizIngest` 消费_政策企业等灌数） |
| 图 diff | **边不变，本叶把图里那条实线真接上**：`C 上图 chain/segment VID 稳定 --> D embed/rebuild 一次` —— PY-INDEX 交了 `D`（接口），本叶交的是 `C → D` 这条边（`project_graph()` 末尾唯一调用点）。`bizIngest` 子图**一条边没碰**：政策 / 企业重灌路径本叶零改动，`E -.-> J/K`（跑批 / 按钮）仍是虚线且属 `JOB-A`。`B → C` 的失败语义按图第 5 行落成 skip：点未稳定 → 跳过 rebuild、旧索引原样保留。节点名沿用 as-built 修正：`E` 实际为 `gkxlumen_industry_anchor`（下划线，总控 §0 #5）。 |
| 会签态 | `v0.3-draft`（抄源文件 frontmatter，未自填绿） |

## 范围与实现

**做**：产业链灌数管线（`lumen-algo-py`）末段，在 DWD 链表读完 **且** 上图 `chain`/`segment` 点写稳之后，调 **一次** `embed/rebuild`。

### 1. 灌链管线入口与挂钩位置

| 项 | as-built |
|----|----------|
| 灌链入口（HTTP） | `POST /internal/v1/chain/graph/project` → `lumen_algo_service/views/chain.py::chain_graph_project` |
| 灌链入口（CLI） | `python -m lumen_common.algorithms.chain.graph_project`（`main()`，运维/过夜可用） |
| 管线函数 | `lumen_common/algorithms/chain/graph_project.py::project_graph()` —— 只读 demo DWD 五张链表 → `map_graph()` → `NebulaSink.upsert()` 写 `demo_gkx_chain` |
| **挂钩点** | `project_graph()` 函数体**最后一句 return 之前**，紧跟在 `result["status"]="ok" / wrote=True / vertices_written=vc` 之后：`_hook_industry_index(result, chains, nodes)` |
| 挂钩的「哪一步之后」 | `NebulaSink.upsert()` 返回真实写入点/边数之后。upsert 抛异常 → 前面的 `except` 已 `return`，根本走不到挂钩；即「上图没写成功就没有 rebuild」是**控制流保证**，不是靠 if 判断兜的 |

> 本仓 **没有** 第二条「写 DWD 链表」的代码路径：`rg "INSERT INTO" lumen_common | rg -i chain` 只命中 `demo_guard.py:178` 的通用只读/受控写工具，链表本身由 GDF/ODS 侧灌入，`project_graph` 是本仓能看到的灌链末段。因此「DWD 链表写完」在本仓的可观测等价物 = `project_graph` 成功读到链表五表且 `table_errors` 为空。

### 2. 点未稳定的判定（`_index_skip_reason`）

按顺序判，命中任一条即 **跳过 rebuild**，不 drop / 不 create，上一版 `index_version` 原样留在 Milvus：

| # | 条件 | 语义 |
|---|------|------|
| 0 | `status != "ok"` 或 `wrote != True` | 上图失败 / `dry_run` / `nebula.enabled=false` —— **由控制流保证**（这些分支在挂钩之前就 return 了），返回体里 `industry_index` 保持初始化的 `skipped` |
| 1 | `table_errors` 非空 | DWD 链表读取有错 → 锚点不可信 |
| 2 | `vertex_counts.chain == 0` 或 `vertex_counts.segment == 0` | 链/环节点位数量异常（空链表、映射全跳） |
| 3 | `vertices_written < chain + segment` | 上图写入点数少于锚点点数 → VID 没写稳 |
| 4 | `anchor_docs()` 产出为空 | 词表为空（链表无可索引的名字） |

稳定则调 `industry_embed.rebuild({}, anchors=anchors)` **一次**。

### 3. 返回 / 日志字段（DoD：灌链带 `industry_index_version`）

`project_graph()` 返回体新增两个字段（HTTP 与 CLI 同一份，CLI `main()` 直接 `print(json.dumps(...))`，本仓 chain 模块无 logger，**返回体即日志**）：

```json
"industry_index": {"status": "ok|skipped|failed", "index_version": "20260911004738", "indexed": 1516, "detail": "…"},
"industry_index_version": "20260911004738"
```

并把结果并进 `detail` 尾巴，便于 grep 一行看全（真实样例见 §验收证据 2）：

```text
projected space=demo_gkx_chain vertices=20545 edges=132937 skipped=100177 | industry_index=ok: version=20260911004738 indexed=1516
```

skip / fail 时 `industry_index_version` 为 `null`（**诚实**：PY-INDEX 没有 `GET .../status` 接口，本叶查不到「保留下来的那一版是哪版」，就不编一个；旧版本仍完好留在 collection 里，见 §偏离 2）。

### 4. 硬闸落实

| 硬闸 | 落实方式 |
|------|----------|
| **一次性** | 全仓（非 vendor、非 tests）引用 `industry_embed` 的只有 2 个文件：`views/industry.py`（运维 / Java Feign 入口）与 `graph_project.py`（本挂钩）。`graph_project` 源码内 `rebuild(` 只出现 1 次。单测 `test_only_one_rebuild_call_site_in_ingest_pipeline` 把这条钉死（新增文件一旦 import 就红） |
| **不回滚** | `_hook_industry_index()` 就地改写 `result`，整段包在 `try/except Exception` 里，任何索引侧异常都**不外抛**、不改 `status` / `wrote` / `vertices_written` |
| **不假成功** | rebuild 非 0 → `industry_index.status="failed"` + 原因进 `detail`；返回体里**没有任何字段**在索引失败时说索引成功。`status` 字段语义仍只描述上图（它已成功且按硬闸不得回滚），调用方不能只看 `status` 就宣称灌链全绿 —— 判据是 `industry_index.status` |
| 不逐行 embed | 走 `rebuild(anchors=…)` 整库一次；本叶零处循环调 `search`/`embed_text` |
| 不碰别人的库 | 本叶**零新 Milvus 调用**，全部经 PY-INDEX 的 `MilvusHttpStore` + `assert_owned_collection`。实测前后 `aip_kb_1` / `aip_kb_2` / `spk_id_speaker_embeddings` 名单不变 |
| 无假 VID / 假 `chain:` 码 | 锚点 VID 全部来自本次 `map_graph()` 的产出，与刚写进 Nebula 的点**同一批对象**；本叶未生成任何新码 |
| 不写正式库 | MySQL 只读 `demo_gkxlumenx_dwd`；Nebula 只写 `demo_gkx_chain`（`assert_demo_nebula_space` 仍在）；Milvus 只写 `gkxlumen_industry_anchor` |

**不做**（按派单逐条确认未越界）：映射逐行 embed（零处）；政策 / 企业重灌调 rebuild（政策 / 企业侧代码本叶**一行未改**，grep 见 §验收证据 4）；`jobs/enrich`（= `CROSS-VEC-JOB-A-L01`，本叶零代码）；改 Java / 前端（零改动）；引 pymilvus / 装 embedding 模型（`requirements.txt` 未动）。

## 偏离

| # | 偏离 | 理由 / as-built |
|---|------|-----------------|
| 1 | 挂钩写在 `project_graph()` 内部，而不是 view 层或一个新的「灌链编排器」 | 写在 view 层则 CLI / 过夜脚本路径漏钩，且既有单测 `test_route_and_no_silent_write_from_search_sync_jobs` 断言 view 里 `project_graph(` 只能出现 1 次；新起编排器等于给一根线造一个框架（ponytail 违规）。写在管线函数末尾 = 唯一调用点覆盖全部入口，且「upsert 失败就走不到挂钩」由控制流保证。代价：`industry_embed` 依赖 `graph_project.map_graph`，故用**函数内延迟 import** 破循环（已在 docstring 注明）。 |
| 2 | skip / fail 时 `industry_index_version` 返回 `null`，而不是回填「保留下来的旧版本号」 | PY-INDEX 开放项 D 明确：没有「当前索引版本」查询接口，`search` 只能回传命中行的版本。为了填一个字段而额外打一次 Milvus 检索属于伪装的确定性；旧版本**物理上**完好（跳过 = 一次 Milvus 调用都没发），需要时运维/QA 用 `search` 一条即可读出（§验收证据 3 就是这么读的）。若 coordinator 认为 hook 必须回报旧版本号，那是 PY-INDEX 加 `GET .../status` 的活（开放项 D），不在本叶。 |
| 3 | `status` 字段在「上图 ok + rebuild failed」时仍为 `ok` | 硬闸要求二选一时的取舍：把 `status` 翻成 `failed` 会让调用方（Java / 过夜脚本）以为上图没成，从而重跑整条上图 —— 这等价于「因 rebuild 失败回滚上图」，正是硬闸禁止的。故 `status` 保持描述上图事实，索引结果单列 `industry_index.status=failed` 并合并进 `detail`。见 §范围与实现 4「不假成功」。 |
| 4 | 未给挂钩加 `skip_index` / `enable_index` 开关 | 派单没要；`project_graph` 的语义就是「显式灌链」，灌完就该建索引。真要不建索引的场合已有 `dry_run=true`（同样跳过，实测见 §验收证据 1）。 |

## 产物清单

- `lumen-algo-py/lumen_common/algorithms/chain/graph_project.py`（改：模块 docstring 说明建库切面；新增 `_index_block` / `_index_skip_reason` / `_hook_industry_index`；`_empty_result` 与 `result` 初始化各加 2 个字段；`project_graph` 末尾 1 行挂钩）
- `lumen-algo-py/tests/test_chain_graph.py`（改：新增 5 个用例 + 2 个测试夹具）
- 现网：`demo_gkx_chain` 一次全量上图 + `gkxlumen_industry_anchor` 一次 rebuild（见 §验收证据 2 / 3）
- 本 handoff

## 验收证据

### 1. pytest（不连网，内存回退）

```text
cd ${GKX_ROOT}/repos/lumen-algo-py
python -m pytest tests/test_chain_graph.py -q
  → 16 passed, 1 warning in 1.18s          （原 11 例 + 本叶 5 例）

python -m pytest tests/test_chain_graph.py tests/test_industry_embed.py tests/test_chain_shared.py -q
  → 48 passed, 1 warning in 7.30s

python -m pytest -q                          # 全仓回归
  → 393 passed, 1 skipped, 1 warning in 240.92s     （PY-INDEX 交付时为 388 passed，+5 = 本叶新增）
```

本叶新增用例（`tests/test_chain_graph.py`）：

| 用例 | 断言什么 |
|------|----------|
| `test_index_hook_rebuilds_once_when_vids_stable` | 上图成功 → `rebuild` **被调用且仅 1 次**；传入锚点 VID 恰为 `["chain:INB13","segment:INB1301","segment:INB1302"]`（图上码，非新造）；`industry_index.status="ok"`、`industry_index_version="20260911013000"`、`detail` 含 `industry_index=ok` |
| `test_index_hook_skipped_keeps_previous_version[graph_failed]` | 上图失败（nebula3 ImportError）→ `rebuild` **零调用**；`industry_index.status="skipped"`、`index_version is None`、detail 含「上一版」 |
| `test_index_hook_skipped_keeps_previous_version[no_segment]` | 上图成功但 `segment=0`（点数异常）→ `rebuild` **零调用**；`status` 仍为 `ok`（上图不回滚），`industry_index.detail` 含「数量异常」 |
| `test_index_failure_is_honest_and_does_not_roll_back_graph` | rebuild 返 `code=1` → `wrote is True`、`vertices_written==4` 不变（不回滚）；`industry_index.status="failed"`、`industry_index_version is None`、`detail` 含 `industry_index=failed` |
| `test_only_one_rebuild_call_site_in_ingest_pipeline` | 全仓（`lumen_common` + `lumen_algo_service`，排除 `industry_embed.py` 自身）引用 `industry_embed` 的文件集合 **恰等于** `{views/industry.py, chain/graph_project.py}`；`graph_project` 源码内 `rebuild(` 出现 **1 次**；`search` / `sync` / `job_runtime` / chain view 源码内无 `industry_embed` |

> DoD 要求的两条（「VID 稳定 → 调一次 rebuild」「点未稳定 → 不调 rebuild 且保留旧版本」）由前 3 例覆盖。

### 2. 真跑了一次完整灌链（本机可直达 `192.168.88.43`，未走跳板）

```text
env: MILVUS_URI=http://192.168.88.43:19530  LUMEN_ALGO_MYSQL_HOST=192.168.88.43 (demo_gkxlumenx_dwd)
python -c "from lumen_common.algorithms.chain.graph_project import project_graph; project_graph({})"

{"status":"ok","wrote":true,
 "vertex_counts":{"chain":102,"segment":1414,"enterprise":19029,"institution":0},
 "vertices_written":20545,"edges_written":132937,"table_errors":[],
 "industry_index":{"status":"ok","index_version":"20260911004738","indexed":1516,"detail":"灌链末段一次 rebuild"},
 "industry_index_version":"20260911004738",
 "detail":"projected space=demo_gkx_chain vertices=20545 edges=132937 skipped=100177 | industry_index=ok: version=20260911004738 indexed=1516"}
elapsed 26.6s
```

→ **这就是 DoD 要的「灌链日志里 `industry_index_version` 的样例」**。`102 chain + 1414 segment = 1516`，与 PY-INDEX 实测词表条数一致；`indexed=1516` 说明整库一次建成，不是逐行。

跑前 / 跑后 `index_version` 与 `indexed`：

| | `index_version` | `indexed` | 读法 |
|---|---|---|---|
| 跑前 | `20260911002540` | 1516（PY-INDEX 第二次 rebuild 留下的） | `search({"query":"集成电路"})` 回传命中行版本 |
| 跑后 | **`20260911004738`** | **1516** | 同上 |

### 3. 跑后复验（索引真的换了版本，别人的库一根汗毛没动）

```text
python -c "search({'query':'集成电路','top_k':2})"
  → code=0 index_version=20260911004738
    items: chain:INB1303 集成电路 1.0 / segment:INB1303050301 射频集成电路 0.8044

python scripts/milvus_probe.py
  TCP 192.168.88.43:19530 ok
  collections=4 本前缀(gkxlumen_industry_)=['gkxlumen_industry_anchor']
  只读不动（禁止 drop/insert）：['aip_kb_1', 'aip_kb_2', 'spk_id_speaker_embeddings']
```

### 4. 「只有一处调用」与「政策/企业重灌路径无 rebuild」的 grep 证据

```text
$ rg -n "industry_embed" --glob '*.py' --glob '!tests/**'
lumen_algo_service/views/industry.py:10:  from lumen_common.algorithms.industry_embed import (      ← 运维 / Java Feign 入口（PY-INDEX 交付）
lumen_algo_service/views/industry.py:25:  def industry_embed_rebuild(...)
lumen_algo_service/views/industry.py:34:  def industry_embed_search(...)
lumen_common/algorithms/chain/graph_project.py:8:   ``industry_embed.rebuild``。这是整条灌链**唯一**的 rebuild 调用点…   ← docstring
lumen_common/algorithms/chain/graph_project.py:598: ``industry_embed`` 反过来依赖本模块的 ``map_graph``…                ← docstring
lumen_common/algorithms/chain/graph_project.py:602: from lumen_common.algorithms.industry_embed import anchor_docs, rebuild   ← 本叶唯一挂钩
lumen_common/algorithms/industry_embed.py:331:      "source": "industry_embed"                                       ← 自身

$ rg -n "embed/rebuild" --glob '*.py'
（仅 docstring / 单测里的路径字符串，无第二个调用点）

$ rg -n "rebuild" vendor/entan-py/polan vendor/entan-py/entan lumen_common/algorithms/policy lumen_common/algorithms/entan --glob '*.py'
vendor/entan-py/entan/graph/nebula_loader.py:46,54,112,123,132   ← 全部是 Nebula 的 `ensure_schema(rebuild=)` DROP SPACE 开关，与 Milvus 无关
（政策 polan/* 与企业 entan/metrics 零命中）
```

→ **政策 / 企业重灌路径 grep 无 `embed/rebuild` 调用**；本叶 `git show --stat` 只有 2 个文件，政策 / 企业 / Java / 前端零改动。

### 5. skip 路径的现网实证（不是只有单测）

```text
python -c "project_graph({'dry_run': True})"   # 真读 DWD（1516 锚点），不写 Nebula
{"status":"dry_run","wrote":false,
 "dwd_rows":{"industry_chain":102,"industry_chain_node":1414,"industry_chain_node_rel":1073,
             "industry_chain_entity_rel":230425,"industry_chain_event_entity_rel":202},
 "industry_index":{"status":"skipped","index_version":null,"indexed":0,
                   "detail":"上图未完成，未调 rebuild；上一版索引保持不变"},
 "industry_index_version":null}
```

→ 点未稳定（这里是根本没上图）时 **一次 Milvus 调用都没发**，`20260911002540` 那版索引原封不动。

## 问题清单 / 开放项（升级给 `human:淮政玮`）

| # | 事项 | 谁做 | 状态 |
|---|------|------|------|
| A | **谁来定期触发灌链**：本叶只保证「灌链跑 → 索引跟着重建」。目前 `/internal/v1/chain/graph/project` 靠人 / 运维 / 过夜脚本点，没有调度器。夜管线（02 §3.2）真跑起来时，`灌链 → 政策重灌 → Job A` 的编排归谁 | coordinator + 运维 | 🟡 |
| B | **PY-INDEX 开放项 D 仍未闭**（`GET .../status`）：本叶 skip 时报不出「保留的是哪一版」（见 §偏离 2）。若 Java 侧进度页要显示「当前索引版本」，需 PY-INDEX 补一条只读接口 | coordinator 决定要不要建叶 | 🟡 |
| C | 承接 PY-INDEX 开放项 A / C：向量仍是字面哈希（无语义）、Milvus 仍未开鉴权。本叶未改变这两项风险面 | 架构 + 运维 | 🟡 |
| D | 现网 `industry_chain_entity_rel` 有 230425 行，本次上图 `skipped_total=100177`（多为 `entity_rel_missing_dst` / 未映射类型）。这不影响锚点（chain/segment 满额 1516），但企业侧挂链覆盖率是另一个话题 | 数据 + `human:李伟`（`graph_project` 既有升级项） | 🟡（既有，非本叶引入） |

## 修改内容

| 文件 | 改了什么 |
|------|----------|
| `lumen_common/algorithms/chain/graph_project.py` | 模块 docstring 增「灌链末段挂钩」段（建库切面 / 唯一调用点 / 不回滚）；新增 `_index_block()`（索引结果三态包）、`_index_skip_reason()`（点未稳定判据 4 条）、`_hook_industry_index()`（延迟 import + 唯一 rebuild 调用 + 全程 try/except）；`_empty_result()` 与 `project_graph` 的 `result` 初始化各加 `industry_index` / `industry_index_version` 默认 skipped 值；`project_graph` 成功路径末尾加 1 行挂钩 |
| `tests/test_chain_graph.py` | 新增夹具 `_fake_db` / `_spy_rebuild` 与 5 个用例（见 §验收证据 1）；文件 docstring 补本叶来源 |

## 测试结果

- `python -m pytest tests/test_chain_graph.py -q` → **16 passed**（本叶 5 例全绿，无 skip）
- `python -m pytest -q` → **393 passed, 1 skipped**（全仓回归；PY-INDEX 时 388 passed，未破坏既有叶）
- 现网实测：完整灌链 ×1（上图 20545 点 / 132937 边 + rebuild 1516 条，26.6s）、`dry_run` ×1（skip 路径）、`search` 复验 ×2、`milvus_probe` ×1

## 遗留风险

- **灌链变慢了**：末段多了一次 rebuild（本次 1516 条约 4 秒，占 26.6s 的一小部分）。链表规模涨到十万级锚点时，rebuild 会成为灌链尾部的显著耗时，届时应考虑「异步下发一个 job」而不是同步等 —— 现在锚点千级，同步是最短的正确解。
- **每次灌链都会 drop + create collection**：期间（秒级）`search` 会查不到 / 查到空。Job A、政策按钮若刚好撞上这个窗口，会拿到 `code≠0 + degraded`（PY-INDEX 契约保证不会返回假 VID），但**会白跑一批**。夜管线顺序（02 §3.2：灌链 → 重灌 → Job A）本身就避开了这个窗口，别把 Job A 和灌链并排跑。
- **`anchor_docs()` 用默认 `vid_length=80`，`project_graph` 用 `conf.vid_length`**：现网两边都是 80，一致；若运维把 `chain.vid_length` 改小，超长 VID 会在图上被跳过而在锚点里保留（反之亦然）。属配置面偏差，不改代码只记账（PY-INDEX 的 `load_anchors()` 有同样约定）。
- 索引失败时 `status` 仍为 `ok`（§偏离 3）：**下游必须看 `industry_index.status`**，只看 `status` 会误判「灌链全绿」。已在返回 `detail` 里追加，Java / 运维读一行日志就能看见。

## CI/CD（必填）

- 分支：`lumen-algo-py` `origin/dev`（先 `git pull --ff-only` = already up to date，未 force）
- commit：**`95f31bf`** `feat(chain): rebuild industry anchor index once at chain ingest tail [agent:algorithm-agent]`；**`1646874`** `test(chain): scope rebuild call-site guard to rebuild callers only [agent:algorithm-agent]`（守卫只盯 rebuild 调用方，避免误伤 JOB-A 的 `search` 消费）
- pipeline URL / ID：push 触发 GitLab CI（`def03e6..95f31bf`、`95f31bf..1646874  dev -> dev`）；dev 自动 `deploy:api` / `deploy:worker`
- 部署 namespace / 镜像 tag：`dev`；`gkx-lumen-algo-py-api:1646874*` / `-worker:1646874*`（由 CI 打 tag）
- K8s rollout：**未在本叶点名验证**（提交时刻 CI 刚触发）。本叶验收不依赖 Pod：逻辑由 pytest 覆盖，现网效果由本机直连 88.43 实测（证据 2 / 3）。段 E 由 coordinator 点名 CI deploy 绿。
- dev 测试 URL / 命令与结果：

```text
# 本机（env 与 k8s api.yaml / worker.yaml 注入值一致）
python -c "from lumen_common.algorithms.chain.graph_project import project_graph; print(project_graph({}))"
  → status=ok vertices_written=20545 edges_written=132937
    industry_index_version=20260911004738 industry_index.status=ok indexed=1516

# Pod 内 HTTP（待 rollout 后由 coordinator / QA 点）
kubectl -n dev exec deploy/lumen-platform-algo-py -- \
  python -c "import urllib.request,json;print(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8000/internal/v1/chain/graph/project',data=b'{}',headers={'Content-Type':'application/json'}),timeout=300).read())"
```

## 可观测性（建议）

- OTEL_SERVICE_NAME：未改（`lumen-platform-algo-py` / `-worker`）
- traceId（dev 抽样）：本机运行无 OTel SDK 上下文 → 响应 `trace_id=null`（诚实为 null，未编造）；Pod 内由现有 `TraceHeaderMiddleware` 注入
- Tempo / Loki：无新增埋点。本仓 chain 模块无 logger，**返回体即日志**：`detail` 尾部固定带 `| industry_index=<status>: …`，`industry_index_version` 为独立字段，一行 grep 即可判断某次灌链有没有建索引、建的是哪版

## 涉及文件

- `lumen-algo-py/lumen_common/algorithms/chain/graph_project.py`
- `lumen-algo-py/tests/test_chain_graph.py`
- 本 handoff

## 下游契约（给 JOB-A / API-FEIGN）

| 项 | 值 |
|----|-----|
| `JOB-A` 依赖满足 | ✅ 索引已由灌链自动维护，`JOB-A` **只调 `search`**，绝不调 rebuild。单测 `test_only_one_rebuild_call_site_in_ingest_pipeline` 只盯「同时出现 `industry_embed` + `rebuild`」的文件，**只 import `search` 的 `jobs/enrich` 不会被误伤**；反之 JOB-A 若把 rebuild 也拉进去，这条用例立刻红 |
| `JOB-A` 拿版本号 | 从 `search` 响应的 `index_version` 读（当前 `20260911004738`）；或看最近一次灌链返回的 `industry_index_version` |
| 总控 §0 #17 仍有效 | `search` 是字面哈希向量，**禁止直接采 top1 定码**，必须 top-k → `match_industry_anchors` 二次对码 |
| `API-FEIGN` | 若要把灌链结果透出给 Java，新增字段为 `industry_index`（对象）与 `industry_index_version`（字符串或 null）。Java **不得**因 `industry_index.status=failed` 就重发上图请求（会重复灌链） |

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python（D1） | ✅ 挂钩与索引全在 `lumen-algo-py`；Java / 前端零改动 |
| 调用链不可越层 | ✅ 挂钩是 Python 进程内调用（`project_graph` → `industry_embed.rebuild`），未新增任何对外边；前端 / Java 仍只经 `/internal/*` |
| 图谱仅 Nebula | ✅ 只写 `demo_gkx_chain`（`assert_demo_nebula_space` 未动）；向量不替代建图、不签发 VID，锚点 VID 全部来自本次 `map_graph` |
| 可观测 | ✅ 沿用响应内 `trace_id`；新增字段进 `detail`，未打印连接串 / 口令 |
| CI/CD | ✅ push `origin/dev`，未 force；commit 带 `[agent:algorithm-agent]` |
| demo2 只读 / D12 | ✅ 未改任何 `demo-*` 仓、未 merge；只连 demo **数据库 / 图空间**（总控 §0 #9 #10 指定数据面），非 demo 服务调用 |
| 数据策略 | ✅ MySQL 只读 `demo_gkxlumenx_dwd`；Milvus 只经前缀守卫写 `gkxlumen_industry_anchor`；未碰 `amcpdp-*` / `aip_kb_*` / `spk_id_*`（跑后 probe 名单不变）；未写正式 `gkxlumenx_*` |
| 建库 / 消费切面（总控 §0 #2 #3） | ✅ 建库只在灌链末段一次；政策 / 企业重灌路径零改动、grep 无 rebuild |
| D8 / D10 | N/A（无 UI） |
| D9 数据血缘 | N/A（本叶不产出界面统计指标；`index_version` 随灌链返回，索引每行仍带 `model_version` / `index_version` 可追溯） |
| 密钥不入 git | ✅ 本叶未新增任何配置 / 口令；MySQL / Nebula / Milvus 连接参数全部沿用既有 env 与 `conf/settings.yaml` |

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 96000 |
| model_used | claude-opus-5-thinking |
| actual_cost | 0.58 |
| cost_warn | green |

口径：coding 默认 75/25 读写比；B 档 `$3/$15` per 1M；`96000×0.75×3/1e6 + 96000×0.25×15/1e6 = 0.58`。
