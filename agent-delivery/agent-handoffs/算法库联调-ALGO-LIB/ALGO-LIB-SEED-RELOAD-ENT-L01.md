# ALGO-LIB-SEED-RELOAD-ENT-L01 · 企业灌数据补「重灌」(mode=reload，对照政策)

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `coordinator_dispatch` |
| 说明 | coordinator 已 MCP 认领并 `in_progress`；本叶按厚包执行，未再向用户逐叶确认。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用现成 `apply_ods_to_dwd(replace=True)`，不另写 TRUNCATE 列表；不发明第四档。未用 YAGNI 跳过 live 写守卫、图谱剥离硬闸、handoff、可观测中间件。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未走 Headroom；对照政策 BasicPage + `reload_from_ods` 语义即可。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A（本叶不改存储流图拓扑） |
| 图 diff | 灌数仍只写 Demo ODS→DWD→ADS；图谱边仍只走 `/internal/entan/graph*`。重灌后图空或保持旧图都合法。 |
| 会签态 | 抄 `COORD-GRAPH-TRIPLE-UI-DISPATCH-20260831.md` §0.1 已拍板。 |

## 范围与实现

企业基础指标页「灌数据」补第二档 `mode=reload`：保留 ODS，只清 DWD，按现有 ODS 全量映入后重算 ADS。语义照抄政策，禁止第四档。

| 档 | mode | 语义 |
|---|---|---|
| 追加 | `append` | 对齐政策 `ingest_pending`：只映 ODS 有、DWD 无的 `org_id`；不清贴源、不内存造数 |
| 重灌 | `reload` | 跳过造数；`apply_ods_to_dwd(replace=True)` 清企业 DWD 后全量映入；ADS 全量重算 |
| 重建 | `replace` | 清 ODS+DWD，再内存造底数 |

改动：

1. `entan/llm_ods/seed.py`：三档原样；`reload` 不调用 `orgs_for_batch` / `build_seed_rows` / `write_rows`。
2. `scripts/run_all.py`：去掉「非 replace 一律折成 append」；`--mode` 含 `reload`；步骤标签「重灌」。
3. `api/main.py` `POST /internal/run-pipeline`：接受 `append\|reload\|replace`；live 仍拒写。
4. `demo-ui-system-test` 企业 `BasicPage.vue`：下拉中间加「重灌」+ 确认框 + SeedHelpBadge 一句；灌数流程去掉建图步骤。
5. `src/api/entan/index.ts`：`runPipeline` 类型补 `reload`（前端才能下传第三档）。
6. **2026-09-03 本叶补丁（监管人徐滕强）**：`append` 去掉 `orgs_for_batch` / `write_rows`；`gdf_sim` 按 `org_id` 差集拉取；`/internal/status` 回 `pending_count`；50100 无增量拦截。

## 偏离说明

- 厚包写「只改 BasicPage.vue 及相关企业灌数文案」。为让 TS 把 `reload` 传给网关，同步改了 `src/api/entan/index.ts` 的 `runPipeline` 联合类型。未改政策 / 产业链 / 产业服务页。
- **重灌未在共享 Demo 点全量执行**（监管人确认暂缓：5 万 ODS 会 TRUNCATE 企业 DWD 再全量映 + 全量 ADS）。入口与后端 `mode=reload` 已在，现网点验只做追加拦截。
- 未做三方「数据同步」，未改 lumen-*。本叶只收企业。

## 产物清单

| 产物 | 路径 |
|------|------|
| seed | `demo-algo-ent-analysis/entan/llm_ods/seed.py` |
| 流水线 | `demo-algo-ent-analysis/scripts/run_all.py` |
| API | `demo-algo-ent-analysis/api/main.py`（仅 `/internal/run-pipeline` 接受 reload） |
| 单测 | `demo-algo-ent-analysis/tests/test_entan_seed_reload.py`；`tests/test_entan_graph_ops.py` 扩三档 |
| 企业页 | `demo-ui-system-test/src/views/entan/pages/BasicPage.vue` |
| 前端 API 类型 | `demo-ui-system-test/src/api/entan/index.ts` |
| 本 handoff | `agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/ALGO-LIB-SEED-RELOAD-ENT-L01.md` |

## 三模式对照

| 层 | append | reload | replace |
|----|--------|--------|---------|
| UI | 追加（读 ODS 增量，不清空贴源）；`pending=0` 拦截 | 重灌（保留 ODS，只清 DWD 并重算基础指标） | 重建（先清空再灌，divided） |
| 确认框 | 把 N 条 ODS 增量映入 DWD，不造数 | 保留 ODS，只清企业 DWD，全量映入并重算；不写 Nebula、不建企业图谱 | 清 Demo ODS P0 + DWD 再灌 |
| seed.py | **不造数** + `apply_ods_to_dwd(replace=False)` | **不造数** + `apply_ods_to_dwd(replace=True)` | `write_rows(truncate=True)` + 清 DWD |
| run_all | 原样下传 | 原样下传（不再折成 append） | 原样下传 |
| 图 | 不建 | 不建 | 不建 |

## DoD 对照（本叶执行侧）

| # | DoD | 结果 |
|---|-----|------|
| 1 | 下拉第二档「重灌」，文案/确认框对照政策 | ✅ 50100 已部署；未改政策页 |
| 2 | `mode=reload` 贯穿 seed / run_all / run-pipeline，不折成 append | ✅ 单测 |
| 3 | 重灌不清 ODS、不造数、不写正式库、不建图 | ✅ 代码 + grep + 单测 |
| 4 | Demo 可点重灌 + 截图 | ⚠ **as-built**：监管人徐滕强确认共享 Demo **不点**全量重灌（5 万 ODS 同步清 DWD）。现网点验改为追加拦截 + `pending_count=0`（监管人确认提示出现）。无重灌截图。 |

## 测试结果

- 2026-09-03 复测：`python -m pytest tests/test_entan_seed_reload.py tests/test_entan_graph_ops.py test_llm_ods_gdf_sim.py::test_fetch_all_empty_ids_skips_query -q` → **12 passed**
  - `run("reload")` 原样下传；未知 mode 抛 `ValueError`，不折成 append
  - `run_seed("reload"|"append")` 只调 `apply_ods_to_dwd`，零次 `orgs_for_batch` / `build_seed_rows` / `write_rows`
  - `build_steps("reload")` 标签「重灌」；三档步骤名均无 实体识别 / Nebula / 图谱成员
  - `_fetch_all(..., org_ids=set())` 不发 SQL
- 图谱剥离 grep（灌数路径）：
  - `seed.py`：无 `graph` / `nebula` / entity NER-RE 调用
  - `run_all.py`：仅模块头注释「图谱 A/B/C 不在本路径」；`build_steps` 无 graph/nebula/entity
  - `POST /internal/run-pipeline`：只调 `scripts.run_all.run`，不调 graph 路由
  - `BasicPage.vue` 灌数流程已去掉「B 实体识别 + 关系图谱」；确认框按厚包写「不写 Nebula、不建企业图谱」（否定句，不是调用）

## 行数证据

### 2026-09-02 灌数前基线（只读，已过时）

| 库.表 | 行数 |
|--------|------|
| `demo_gkxlumenx_ods.dwd_org_base_info` | 50000 |
| `demo_gkxlumenx_dwd.enterprise_base` | 102 |
| `demo_gkxlumenx_ads.enterprise_score` | 100 |

### 2026-09-03 监管人点验（现网已追平）

本地 `mode=append` 空跑（pending=0，各 DWD 插入 0）。`GET http://111.198.38.90:50100/api/entan/internal/status`：

| 字段 | 值 |
|------|-----|
| `ods.dwd_org_base_info` | 50000 |
| `dwd.enterprise_base` | 50000 |
| `dwd.enterprise_executive` | 438307（与 ODS 高管对齐） |
| `tables.enterprise_score` / `biz_power` / `tech_power` | 50000 |
| `pending_count` | **0** |

50100 `/entan/basic` 前端分块已含「可追加 / 没有可追加的增量」。监管人徐滕强确认：点追加被拦截。未点重灌、未点重建。未写正式 `gkxlumenx_*`。

## 遗留风险

- **重灌仍是同步全量**：现网 5 万 ODS / 43 万高管，点下去会清企业 DWD 再全表映 + 全量 ADS。监管人确认本叶不点。入口在，现网验收用追加拦截代替「可点重灌」。
- 重灌若以后要在共享 Demo 跑，需另开异步/分批叶；**不是本叶范围**。

## CI/CD（必填）

- 分支：`dev`（两业务仓）
- 首批 reload 入口：`demo-algo-ent-analysis` `782d609`；`demo-ui-system-test` `9363446`
- 本叶补丁：algo `3bb1b14`；UI `b13631d`
- pipeline：algo [5965](https://gitlab.htmisoft.net/gkx-lumen/demo-algo-ent-analysis/-/pipelines/5965) 绿；UI [5964](https://gitlab.htmisoft.net/gkx-lumen/demo-ui-system-test/-/pipelines/5964) 绿
- K8s rollout：监管人确认已部署
- dev 测试 URL：`http://111.198.38.90:50100/#/entan/basic`（追加拦截已点验）

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用 `ent-analysis-demo`
- 灌数仍走现网 `TraceHeaderMiddleware`；前端 `request.ts` 已带 `X-Trace-Id`
- Tempo / Loki：本叶未抽样

## 涉及文件

- `demo-algo-ent-analysis/entan/llm_ods/seed.py`
- `demo-algo-ent-analysis/entan/llm_ods/gdf_sim.py`
- `demo-algo-ent-analysis/scripts/run_all.py`
- `demo-algo-ent-analysis/api/main.py`
- `demo-algo-ent-analysis/tests/test_entan_seed_reload.py`
- `demo-algo-ent-analysis/tests/test_entan_graph_ops.py`
- `demo-ui-system-test/src/views/entan/pages/BasicPage.vue`
- `demo-ui-system-test/src/api/entan/index.ts`

## 架构合规自检

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法只在 Python | ✅ seed / run_all / ADS 重算均在 Python |
| 2 | 调用链 前端→网关→Python | ✅ `POST /entan/internal/run-pipeline` |
| 3 | 图谱 NebulaGraph | ✅ 灌数零调用；图只走企业图谱 A/B/C |
| 4 | 可观测性 | ✅ 沿用 Trace 中间件 |
| 5 | CI/CD | ✅ push `origin/dev`；未 force |
| 6 | demo 不污染 lumen | ✅ 只改 demo 仓 + 编排 handoff |
| 7 | 方案 A | ✅ Java 不写算法、不直连 nGQL |
| 8 | 数据走 ADS | ✅ 重灌后按 DWD 重算 demo ADS |
| 9 | D8 | ✅ 50100 Element Plus，对照政策 BasicPage |
| 10 | D9/D10 | ✅ 联调台灌数页，无新指标口径 |
| 12 | D12 lumen 不调 demo | ✅ 未改 lumen-*；禁止 merge demo→lumen |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 135000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 2.40 |
| cost_warn | green |

口径：首批 overnight + 2026-09-03 追加对齐/现网点验；algorithm 默认 in/out 75/25。单任务 < $5。

## 联调确认

追加联调通过：2026-09-03 监管人徐滕强在 50100 `/entan/basic` 确认 `pending=0` 拦截提示。重灌入口与单测齐，共享 Demo 未点全量（监管人暂缓 as-built）。

## 明确未做（本叶范围外，不做）

- 未改政策 / 产业链 / 产业服务灌数页
- 未做三方「数据同步」
- 未对共享 Demo 执行全量 `mode=reload` / `replace`
- 未改 lumen-*、未写正式 `gkxlumenx_*`
- 未重写异步/分批重灌
