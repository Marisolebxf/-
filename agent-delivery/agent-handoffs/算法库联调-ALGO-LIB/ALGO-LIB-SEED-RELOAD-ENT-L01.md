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
| 追加 | `append` | 读 ODS 增量差集入 DWD，不清贴源；仍走 `orgs_for_batch` / `write_rows` |
| 重灌 | `reload` | 跳过造数；`apply_ods_to_dwd(replace=True)` 清企业 DWD 后全量映入；ADS 全量重算 |
| 重建 | `replace` | 清 ODS+DWD，再内存造底数 |

改动：

1. `entan/llm_ods/seed.py`：三档原样；`reload` 不调用 `orgs_for_batch` / `build_seed_rows` / `write_rows`。
2. `scripts/run_all.py`：去掉「非 replace 一律折成 append」；`--mode` 含 `reload`；步骤标签「重灌」。
3. `api/main.py` `POST /internal/run-pipeline`：接受 `append\|reload\|replace`；live 仍拒写。
4. `demo-ui-system-test` 企业 `BasicPage.vue`：下拉中间加「重灌」+ 确认框 + SeedHelpBadge 一句；灌数流程去掉建图步骤。
5. `src/api/entan/index.ts`：`runPipeline` 类型补 `reload`（前端才能下传第三档）。

## 偏离说明

- 厚包写「只改 BasicPage.vue 及相关企业灌数文案」。为让 TS 把 `reload` 传给网关，同步改了 `src/api/entan/index.ts` 的 `runPipeline` 联合类型。未改 policy / chain 页。
- 现网 Demo ODS `dwd_org_base_info=50000`、DWD `enterprise_base=102`。本会话**未**对共享 Demo 点全量重灌（会按 5 万 ODS 重映 DWD，耗时长、会改现网 102 行演示集）。行数基线见下；部署后 Demo 点「重灌」验收。
- 未做三方「数据同步」，未改 lumen-*。

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
| UI | 追加（默认，不清空贴源） | 重灌（保留 ODS，只清 DWD 并重算基础指标） | 重建（先清空再灌，divided） |
| 确认框 | 追加一批到 ODS，不清贴源 | 保留 ODS，只清企业 DWD，全量映入并重算；不写 Nebula、不建企业图谱 | 清 Demo ODS P0 + DWD 再灌 |
| seed.py | 造数 + `apply_ods_to_dwd(replace=False)` | **不造数** + `apply_ods_to_dwd(replace=True)` | `write_rows(truncate=True)` + 清 DWD |
| run_all | 原样下传 | 原样下传（不再折成 append） | 原样下传 |
| 图 | 不建 | 不建 | 不建 |

## 测试结果

- `python -m pytest tests/test_entan_seed_reload.py tests/test_entan_graph_ops.py -q` → **8 passed**
  - `run("reload")` 原样下传；未知 mode 抛 `ValueError`，不折成 append
  - `run_seed("reload")` 只调 `apply_ods_to_dwd(..., replace=True)`，零次 `orgs_for_batch` / `build_seed_rows` / `write_rows`
  - `build_steps("reload")` 标签「重灌」；三档步骤名均无 实体识别 / Nebula / 图谱成员
- 图谱剥离 grep（灌数路径）：
  - `seed.py`：无 `graph` / `nebula` / entity NER-RE 调用
  - `run_all.py`：仅模块头注释「图谱 A/B/C 不在本路径」；`build_steps` 无 graph/nebula/entity
  - `POST /internal/run-pipeline`：只调 `scripts.run_all.run`，不调 graph 路由
  - `BasicPage.vue` 灌数流程已去掉「B 实体识别 + 关系图谱」；确认框按厚包写「不写 Nebula、不建企业图谱」（否定句，不是调用）

## 行数证据（2026-09-02 灌数前基线，只读）

| 库.表 | 行数 |
|--------|------|
| `demo_gkxlumenx_ods.dwd_org_base_info` | 50000 |
| `demo_gkxlumenx_ods.dwd_org_executive_info` | 438307 |
| `demo_gkxlumenx_ods.dwd_org_important_news_info` | 0 |
| `demo_gkxlumenx_dwd.enterprise_base` | 102 |
| `demo_gkxlumenx_ads.tech_power` | 100 |
| `demo_gkxlumenx_ads.enterprise_score` | 100 |

验收预期（部署后点重灌）：上表三张 ODS 行数不变；`enterprise_base` 按现有 ODS 重映（现网差集大，DWD 会从 102 扩到接近 ODS）；ADS 基础指标可刷新。未写正式 `gkxlumenx_*`。

## 遗留风险

- 现网 ODS 5 万、高管 43 万：Demo 点重灌会比追加长，确认框已提示语义；未在确认框写「约数万条」（政策页有，企业厚包指定文案未含耗时句）。
- 重灌后 DWD 从 102 → 按 ODS 全量，演示集从「百级」变成「万级」，技商力/深度 ADS 重算更重。属产品预期，不是本叶缺陷。
- 本会话无浏览器点验 50100；K8s 滚完后由 QA / 监管人点「重灌」对照上表 ODS 行数。

## CI/CD（必填）

- 分支：`dev`（两业务仓 + 编排仓）
- commit：`demo-algo-ent-analysis` `782d609`；`demo-ui-system-test` `9363446`；编排仓本文件同批
- pipeline URL / ID：push 后由 GitLab 触发
- 部署 namespace / 镜像 tag：K8s 待滚
- K8s rollout：待滚
- dev 测试 URL：50100 `/entan/basic`（滚完后点验三档）

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用 `ent-analysis-demo`
- 灌数仍走现网 `TraceHeaderMiddleware`；前端 `request.ts` 已带 `X-Trace-Id`
- Tempo / Loki：本叶未抽样

## 涉及文件

- `demo-algo-ent-analysis/entan/llm_ods/seed.py`
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
| actual_tokens | 98000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.72 |
| cost_warn | green |

口径：algorithm 默认 in/out 75/25；对照同仓近叶 `ALGO-LIB-ODS-MOCK-ENT-L01`（88000 → $1.55）按 token 比例折算。单任务 < $5。

## 明确未做

- 未改政策 / 产业链 / 产业服务灌数页
- 未做三方「数据同步」
- 未对共享 Demo 执行全量 `mode=reload`（避免本会话把 102 行 DWD 扩成 5 万）
- 未改 lumen-*、未写正式 `gkxlumenx_*`
