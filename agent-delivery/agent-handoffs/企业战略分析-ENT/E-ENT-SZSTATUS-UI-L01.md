# E-ENT-SZSTATUS-UI-L01 · 深圳企业现状分析前端（lumen-ui-topic）

> 监管：`human:孔东` · 执行：`agent:frontend-agent` · 2026-08-01  
> status：`review` · review_at：`2026-08-01T20:57:54+08:00`

## 认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull`（API 对接续作） |
| in_progress_at | `2026-08-01T19:37:51+08:00` |
| review_at | `2026-08-01T20:57:54+08:00` |
| branch | `dev` → `origin/dev` |

## 范围与实现

- 路由：`/enterprise/shenzhen-enterprise-status-analysis`
- **API 对接**：`API-ENT-full-catalog` **#132–#136** `/topic/v1/sz-status/**`
- 封装：`src/api/enterprise/szStatus.ts` + `types/szStatus.ts` + paths + mock
- composable：`useSzStatusAnalysis` 调 chain-kpi / chain-stage-stats / enterprise-list / city-benchmark / city-insight
- 字段真源：`included_enterprise_count`、`stage_distribution`、`chain_node_text`、`average_tech_power`、`advantages`/`shortboards` 等
- 产业链 / 对标城市改为 `chain_code` / 城市编码（`SZ_STATUS_CHAIN_OPTIONS` / `SZ_STATUS_BENCHMARK_CITY_OPTIONS`）
- 区域固定深圳 `region_id=440300`（页面展示「深圳市」）

## DoD

| 项 | 状态 |
|----|------|
| 页面可访问 + 双 Tab | ✅ |
| 雷达 / 对标表 / 企业清单 | ✅ |
| #132–136 defineApi 封装 + mock | ✅ |
| 生产接口对接 | ✅ |
| type-check | ✅ |
| 推 origin/dev | ✅（本 handoff 同期 push） |
| handoff | ✅ 本文 |

## 产物

- `src/api/enterprise/szStatus.ts` / `types/szStatus.ts`
- `src/composables/useSzStatusAnalysis.ts`
- `src/views/enterprise/EnterpriseSzStatus.vue`
- `src/components/enterprise/szStatus/*`
- 与 KEYENT 共用 `keyAnalysisSzStatusApi.ts` mock、`keyAnalysisParams.ts`

## 架构合规

- 前端只调 Java ✅
- 区域固定深圳 `region_id=440300` ✅
- 未改 package.json / vite.config ✅

## 开放项

- Java 门面 `E-ENT-KEYENT-JAVA-L01` 验收后全链路联调
- 商业力维度 `available=false` 时 UI 展示「暂不可用」
