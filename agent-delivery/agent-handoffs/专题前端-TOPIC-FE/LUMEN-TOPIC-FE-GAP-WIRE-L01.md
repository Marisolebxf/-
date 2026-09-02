# LUMEN-TOPIC-FE-GAP-WIRE-L01 · 专题前端对接 Java 缺口 P0/P2

> 格式参考 `templates/handoff-template.md`。契约真源 `API-TOPIC-FE-GAP-CATALOG.md`。P1 / 维护 CMS / 风险图谱 enrich **不在本单**。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 用户确认「认领开工」后转 `in_progress`；本叶接线已落地，待联调。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用现有 `request` / Pinia / 分析任务中心；只加缺口路径与解析别名。未用 YAGNI 跳过 D8/D9/D10、可观测、调用链。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂 Headroom。 |

## 范围与实现

仓：`lumen-ui-topic`。`USE_MOCK=false` 时禁止 fixture 填数；空字典 / 空列表不回落写死。

### DoD 1 · #G1–G6

| ID | 行为 | 路径 |
|----|------|------|
| #G1–G4 | 招引/培育候选移除、批量清空走 Java；localStorage 只缓存 | `DELETE /enterprise/topic/v1/compare-basket/{recruit\|cultivate}-candidates[/{code}\| /batch]` |
| #G5 | 培育政策导向下拉；失败置空，不回落写死四项 | `GET /enterprise/topic/v1/search/meta/policy-orientations` |
| #G6 | 评估 / 引育 / 风险历史表「删除」；确认后软删，≠ cancel | `DELETE /topicAsync/topic/v1/analysis/tasks/{taskId}` |

### DoD 2 · #C1 + #S1

| ID | 行为 |
|----|------|
| #C1 | `GET /chain/topic/v1/industry/meta` 一次加载。年窗有值用 meta，否则仅保留契约默认近 3/5 年（不再 2021–2029）。区域评价城市空则下拉空，不回落写死城。Q016 `benchmark.items` 空 → 深圳标杆级联空，不冒充沪/京/苏州。高筛 `layoutStatus` / `coveredStage` 不再伪造「重点布局」「全链条」。全景 `as_of`/`asOf` 认响应根。 |
| #S1 | `POST /svc/topic/v1/service/meta`。服务类型/机构类型失败或空数组不回落「金融服务」。检索字段库由 meta 覆盖。 |

### DoD 3 · #S2–S5

服务机构对比篮走 `/svc/topic/v1/service/compare-basket`（GET / POST items / DELETE item / DELETE batch）。`source` 含 `external` 拒绝入篮。全清同时清企业篮 + 服务篮。依赖 MySQL `svc_compare_basket_item`；表未上则联调 5xx，见遗留。

### DoD 4 · #G7 #G8 #G10 #G11

| ID | 行为 |
|----|------|
| #G7 | 评估指标树吃 `label`/`metricId`/`weight`；`available=false` 或 `data_status=pending\|gap` 不改绿 |
| #G8 | 结果 `ranking`←`scores`；雷达认 `radar`；`dimension_diff` 吃 `name/label` 与 `score_a\|b`（企业码先看 result 再看 root） |
| #G9 附带 | 引育结果认 `policyDirections` / `riskCredit` 别名 |
| #G10 #G11 | 重点分析 / 深圳现状页头去掉写死日期；`dataTime`/`data_updated_at` 空显「暂无时点」 |

### DoD 5 · 其余 P2 / 仍空槽

已接路径按目录改解析，缺字段空展示：

- 门户概况 `filtered===false` → 文案「当前产业仅作上下文，KPI 未按产业切片」
- 检索 `tech_score` 空已是「暂无」
- 图谱仍只认 `nodes`/`edges`；rec-list 不在前端重算 score；结果缺 heat/matrix/paths 为 `[]`

**不在本单（仍空）**：P1（联想 / 深圳对标城选项 / 导出任务 / 跨端已读）；维护 CMS；第二套 SVC 产业目录；第二套 create 任务 URL；风险图谱 `owner`/`centrality` enrich。

**标杆有值后的缺口**：`benchmark.items` 一旦非空，级联仍先挂旧树 `SHENZHEN_BENCHMARK_CASCADER`（Q016 现恒空，本叶只堵冒充）。有值后须把选项/校验切到 meta items。

## 偏离说明

- 诊断年窗：meta 空时回落契约默认 3/5 年，不是 2021–2029。
- #S2–S5 已接线，联调成败取决于 DDL / Java 是否已上 `origin/dev`。
- 未给新 API 加 mock；`USE_MOCK=true` 会打真接口。
- 本机未 commit / 未 push（待监管人确认后再推 `origin/dev`）。

## 产物清单

- API：`src/api/enterprise/{paths,compare,search,analysisTask,index,types}` · `src/api/industry/*` · `src/api/service/*`
- 企业：`useCandidateLists` · `analysisTaskDelete` · 评估/引育/风险历史删除 · `evalResultMap` · `recruitResultMap` · `enterpriseEvalHelpers` · 重点分析/深圳页头
- 产业：`industryWorkspaceMeta` · 诊断/区域/深圳页 · `industryWorkspace` · `industrySearchModel` · `industryWorkspaceRuntime.js`
- 服务：`svcWorkspaceMeta` · `compareBasket` · `serviceOrgSearchModel` · 门户概况
- 规则：`src/utils/topicFeGapWire.ts` + `topicFeGapWire.selfcheck.mjs`
- 本 handoff

## 验收证据

- `node src/utils/topicFeGapWire.selfcheck.mjs` → `topicFeGapWire.selfcheck ok`
- `npx vue-tsc --build` → 绿
- 浏览器联调：本机无浏览器自动化，未点页面；待 K8s / 本机 Vite 对人测

## 遗留风险

- **#S2–S5 DDL**：`svc_compare_basket_item` 未上则服务篮同步 5xx；页面会保留本地缓存并打 error log，不回落假名单。
- **#G5 / #C1 / #S1 Feign 空**：下拉为空，评审态政策导向有 PendingBadge。
- **深圳标杆非空后的级联映射**未做（见上）。
- 未 commit，CI / K8s 尚未接续。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 未改算法 |
| 2 调用链 前端→Java | ✅ 只加 `/enterprise` `/chain` `/svc` `/topicAsync`，无直连 Python |
| 3 Nebula | ✅ 未改图谱存储 |
| 4 可观测 | ✅ 新接口走现有 `request`（traceId 已注入） |
| 5 CI | ⏳ 未 push |
| 6 demo2 不 merge lumen | ✅ |
| 7 共享聚合 / 只调 Java | ✅ |
| 8 数据策略 | ✅ 空字段空展示，不补假数 |
| 9 D8 Design | N/A 本叶接线，无新视觉组件 |
| 10 D9 指标 | ✅ 评估 available 不改绿；ⓘ 既有评审层未拆 |
| 11 D10 交互 | ✅ 删除走确认框；空下拉可清 |
| 12 D12 禁 demo-* | ✅ 未指向任何 `demo-*` |

## CI/CD（必填）

- 分支：`lumen-ui-topic` 工作区 `dev`（未 commit）
- commit：—
- pipeline URL / ID：—
- 部署 namespace / 镜像 tag：—
- K8s rollout：未做
- dev 测试 URL / 命令与结果：`node src/utils/topicFeGapWire.selfcheck.mjs` ok；`npx vue-tsc --build` 绿

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用现有前端 request
- traceId（dev 抽样）：未采
- Tempo / Loki：无

## 涉及文件

见上文产物清单；约 48 个文件（含 4 个新增：`analysisTaskDelete.ts`、`industryWorkspaceMeta.ts`、`svcWorkspaceMeta.ts`、`topicFeGapWire.ts` + selfcheck）。
