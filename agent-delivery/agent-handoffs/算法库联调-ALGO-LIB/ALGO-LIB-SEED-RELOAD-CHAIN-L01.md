# ALGO-LIB-SEED-RELOAD-CHAIN-L01 · 产业链灌数据补「重灌」(mode=reload，对照政策)

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:李伟` |
| claim_type | `coordinator_dispatch` |
| 说明 | coordinator 已 MCP 认领并 `in_progress`；本叶按厚包执行，未再向用户逐叶确认。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | `reload` 复用 `apply_ods_to_dwd(replace=True)`，不另写 TRUNCATE 列表、不造底树、不发明第四档。未用 YAGNI 跳过 live 写守卫、图谱剥离硬闸、handoff、可观测中间件。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未走 Headroom；对照政策 BasicPage + 厚包三档语义即可。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A（本叶不改存储流图拓扑） |
| 图 diff | 灌数仍只写 Demo ODS→映射 DWD→ADS；图谱边仍只走 `/internal/chain/graph/{ner\|intra\|hang}`。重灌后图空或保持旧图都合法。 |
| 会签态 | 抄 `COORD-GRAPH-TRIPLE-UI-DISPATCH-20260831.md` §0.1 已拍板。 |

## 范围与实现

产业链基础指标页「灌数据」补第二档 `mode=reload`：保留 ODS 四表，只清映射 DWD，按现有产业树全量映入后重算 ADS。语义照抄政策，禁止第四档。

| 档 | mode | 语义 |
|---|---|---|
| 追加 | `append` | 读 ODS 增量，不清贴源；补缺失节点 + 延伸链 |
| 重灌 | `reload` | 保留 ODS，只清映射 DWD，再全量 ODS→DWD 并重算 ADS |
| 重建 | `replace` | 清 ODS+DWD，再造 3.0 底树 |

改动：

1. `chainan/llm_ods/seed.py`：三档原样；`reload` 不调用 `build_offline_rows` / `write_rows`，不清 ODS；只 `apply_ods_to_dwd(replace=True)` + `apply_gaps(replace=True)` + `recalc_ads`。重灌前后核对 ODS 四表行数，不一致即失败。
2. `scripts/run_all.py`：去掉「非 replace 一律折成 append」；CLI `--mode` 含 `reload`；步骤标签「重灌」。
3. `api/main.py` `POST /internal/run-chain-pipeline`：接受 `append|reload|replace`；live 仍拒写。
4. `demo-ui-system-test` 产业链 `BasicPage.vue`：下拉中间加「重灌」+ 第三张对照卡 + 厚包确认框。
5. `src/api/chain/index.ts`：`runChainPipeline` 类型补 `reload`。
6. `gdf_sim.py`：全量重映现网 ODS 时补三处硬闸（见偏离）。未改 policy / entan 页。

## 偏离说明

- 厚包写「只改 BasicPage.vue 及相关产业链灌数文案」。为让 TS 把 `reload` 传给网关，同步改了 `src/api/chain/index.ts`。
- 现网 Demo ODS 已含三方脏字段：`dwd_org_industry_tags.industry_link_code` 全是 list 字面量（最长 3049）、资讯 `industry_code` 同样打包（最长 255）、追加长出的 `CHAINMOCK*` 拼接 `node-rel:` 超过 VARCHAR(64)。不修映射则重灌在清 DWD 后中途失败。本叶在共享 `gdf_sim` 做了：**超长业务键哈希**、**拆开 list 节点码并去重**、资讯取首个合法 `chain_id`。append / replace 共用该映射，语义未改档。
- **企业上链 as-built**：`apply_ods_to_dwd(replace=True)` **会 TRUNCATE 映射 DWD**（含 `industry_chain_entity_rel`）。重灌后挂接作废，需重跑上链。禁止写成「挂接仍在」。本次实测 `entity_rel` 从 254 变成按 ODS 拆码重映的 73722，不是旧挂接残留。
- 未做三方「数据同步」，未改 lumen-*，未写正式 `gkxlumenx_*`。

## 产物清单

| 产物 | 路径 |
|------|------|
| seed | `demo-algo-science/chainan/llm_ods/seed.py` |
| 映射 | `demo-algo-science/chainan/llm_ods/gdf_sim.py` |
| 自检 | `demo-algo-science/chainan/llm_ods/self_check.py` |
| 流水线 | `demo-algo-science/scripts/run_all.py` |
| API | `demo-algo-science/api/main.py`（仅 `/internal/run-chain-pipeline` 接受 reload） |
| 产业链页 | `demo-ui-system-test/src/views/chain/pages/BasicPage.vue` |
| 前端 API 类型 | `demo-ui-system-test/src/api/chain/index.ts` |
| 本 handoff | `agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/ALGO-LIB-SEED-RELOAD-CHAIN-L01.md` |

## 三模式对照

| 层 | append | reload | replace |
|----|--------|--------|---------|
| UI | 【追加】保留已有产业树，只补新节点/延伸链（默认） | 【重灌】保留 ODS，只清 DWD 并按现有产业树重算指标 | 【重建】清空贴源与明细后再灌完整 3.0 底树（divided） |
| 确认框 | 不清 ODS；挂接保留 | 保留 ODS 四表，只清映射 DWD，全量映入并重算；不写 Nebula、不建图；上链需重跑 | 清四表 ODS+映射 DWD 再灌 10+5 |
| seed.py | `build_offline_rows` + `write_rows` + `apply_ods_to_dwd(replace=False)` | **不造树、不清 ODS** + `apply_ods_to_dwd(replace=True)` | TRUNCATE 四表 ODS + 造树 + 清 DWD |
| run_chain | 原样下传 | 原样下传（不再折成 append） | 原样下传 |
| 图 | 不建 | 不建 | 不建 |

## 测试结果

- 离线：`_check_reload_skips_tree_build()` → **OK**。`run_seed("reload")` 零次 `build_offline_rows` / `write_rows`；`apply_ods_to_dwd(..., replace=True)`。
- 离线：`CHAINMOCK*` 拼接 `relation_id` 哈希后 ≤64；`_iter_link_codes("['INB130901','INB13090102']")` 拆成两码。
- 现网 `python chainan/llm_ods/seed.py` 路径 `run_seed("reload")`（2026-09-02）→ **成功**，见下行数。
- `scripts/run_all.py` 导入本机缺 `networkx`（创新监测图步骤，**不在** `run_chain` 路径）。`_normalize_chain_mode` 源码三档原样下传。
- 图谱剥离：
  - `seed.py` / `run_chain()` / `POST /internal/run-chain-pipeline`：**不调用** nebula / hang-to-graph / graph_ops。仅返回 `projection.status=not_run`（剥离标记）。
  - `run_all.py` 模块顶仍 import `innov.graph`（创新监测 STEPS，不是产业链灌数）。
  - `api/main.py` 另有 `/internal/chain/graph/*`（全景菜单），灌数入口不走。
  - 本页确认框按厚包写「不写 Nebula、不建图」（否定句，不是调用）。
  - ADS 表名 `industry_chain_graph_snapshot` 是切面快照，不是 Nebula 建图。

## 行数证据（2026-09-02 本会话实测重灌）

| 面 | 重灌前 | 重灌后 |
|----|--------|--------|
| ODS `dwd_industry_chain_info` | 1275 | **1275**（不变） |
| ODS `dwd_industry_chain_news_info` | 12291 | **12291**（不变） |
| ODS `dwd_org_industry_product_tags` | 9290 | **9290**（不变） |
| ODS `dwd_org_industry_tags` | 19029 | **19029**（不变） |
| DWD `industry_chain` | 49 | 53（按现有 ODS 重映） |
| DWD `industry_chain_node` | 194 | 1220 |
| DWD `industry_chain_entity_rel` | 254 | 73722（旧挂接已清，按 ODS 拆码重映） |
| DWD `industry_chain_news_event` | 130 | 12291 |
| ADS `industry_chain_metric_fact` | 245 | **265**（已刷新） |

目标库：`demo_gkxlumenx_ods` / `_dwd` / `_ads`。未写正式 `gkxlumenx_*`。`ods_unchanged=True`。`hang_note=mapped DWD truncated; industry_chain_entity_rel hang is void; re-run hang`。

## 遗留风险

- 三方 tags 拆码后 `entity_rel` 从百级扩到 7 万级，ADS 重算更重（本次约 33s）。属现网 ODS as-built，不是第四档。
- 自检 `_try_live_counts` 仍会报「live tags must join tree」：tags 的 list 字面量无法直接 JOIN 树表。本叶只在映射层拆码，未改 ODS 贴源。
- 本会话无浏览器点 50100；K8s 滚完后由 QA / 监管人点「重灌」对照上表 ODS 行数。
- 企业上链若只认旧 254 行挂接，重灌后必须重跑上链。

## CI/CD（必填）

- 分支：`dev`（两业务仓 + 编排仓）
- commit：`demo-algo-science` `634cae5`；`demo-ui-system-test` `9182fd0`；编排仓本文件同批
- pipeline URL / ID：push 后由 GitLab 触发
- 部署 namespace / 镜像 tag：K8s 待滚
- K8s rollout：待滚
- dev 测试 URL：产业链基础指标页（滚完后点验三档）；本会话已用 Python `run_seed("reload")` 对 Demo 库实测。

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用 innov-algo-science / chainan
- 灌数仍走现网 `TraceHeaderMiddleware`；前端 `request.ts` 已带 `X-Trace-Id`
- Tempo / Loki：本叶未抽样

## 涉及文件

- `demo-algo-science/chainan/llm_ods/seed.py`
- `demo-algo-science/chainan/llm_ods/gdf_sim.py`
- `demo-algo-science/chainan/llm_ods/self_check.py`
- `demo-algo-science/scripts/run_all.py`
- `demo-algo-science/api/main.py`
- `demo-ui-system-test/src/views/chain/pages/BasicPage.vue`
- `demo-ui-system-test/src/api/chain/index.ts`

## 架构合规自检

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法只在 Python | ✅ seed / run_chain / ADS 重算均在 Python |
| 2 | 调用链 前端→网关→Python | ✅ `POST /innov/v1/industry/internal/run-chain-pipeline` |
| 3 | 图谱 NebulaGraph | ✅ 灌数零调用；图只走全景 / 深圳产业链 |
| 4 | 可观测性 | ✅ 沿用 Trace 中间件 |
| 5 | CI/CD | ✅ push `origin/dev`；未 force |
| 6 | demo 不污染 lumen | ✅ 只改 demo 仓 + 编排 handoff |
| 7 | 方案 A | ✅ Java 不写算法、不直连 nGQL |
| 8 | 数据走 ADS | ✅ 重灌后按 DWD 重算 demo ADS |
| 9 | D8 | ✅ 50100 Element Plus，对照政策句式 |
| 10 | D9/D10 | ✅ 联调台灌数页，无新指标口径 |
| 12 | D12 lumen 不调 demo | ✅ 未改 lumen-*；禁止 merge demo→lumen |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 145000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 2.55 |
| cost_warn | green |

口径：algorithm 默认 in/out 75/25；对照同目录近叶 `ALGO-LIB-SEED-RELOAD-ENT-L01`（98000 → $1.72）按 token 比例折算。本叶含现网重灌实测与映射脏数据修复，单任务 < $5。

## 明确未做

- 未改政策 / 企业 / 产业服务灌数页
- 未做三方「数据同步」
- 未改 lumen-*、未写正式 `gkxlumenx_*`、未碰 lumen-algo-py vendor
- 未在浏览器点 50100（Python 已对 Demo 库跑通 reload）
