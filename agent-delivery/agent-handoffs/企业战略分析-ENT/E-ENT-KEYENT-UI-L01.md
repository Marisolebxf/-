# E-ENT-KEYENT-UI-L01 · 重点企业分析前端（lumen-ui-topic）

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

- 路由：`/enterprise/key-enterprise-analysis`（`?view=domain`）
- **API 对接**：`API-ENT-full-catalog` **#122–#131** `/topic/v1/key-analysis/**`
- 封装：`src/api/enterprise/keyAnalysis.ts` + `types/keyAnalysis.ts` + `paths` + `defineApi` mock
- 页面 composable：`useKeyEnterpriseAnalysis` 并行调用 overview-kpi / map-distribution / region-insight；领域 Tab 调 domain-*；清单/轻量卡/依据按需
- 筛选复用：
  - **区域**：`RegionSelect` + `entSearchMetaRegionScopes`（`useEntRegionScopesStore`：Pinia + sessionStorage 30min）；输入框 `format-label`/`fallback` 显示中文路径，不露 key
  - **企业类型**：`entSearchMetaTags` + `buildCompareBasketTypeOptions`（`tag_codes`）
  - **产业**：`chain_codes`（`KEY_ANALYSIS_CHAIN_OPTIONS`）
- 字段真源：响应一律 snake_case（如 `matched_enterprise_count`、`type_structure`、`evidence_type=tech_patent`）

## DoD

| 项 | 状态 |
|----|------|
| 页面可访问 + 双 Tab | ✅ |
| 地图下钻 / 清单 Drawer / 领域矩阵与依据弹框 | ✅ |
| #122–131 defineApi 封装 + mock 注册 | ✅ |
| 生产接口对接（USE_MOCK=false 走 Java） | ✅ |
| 区域级联走接口 + 缓存 + 中文展示 | ✅ |
| type-check | ✅ |
| 推 origin/dev | ✅（本 handoff 同期 push） |
| handoff | ✅ 本文 |

## 产物

- `src/api/enterprise/keyAnalysis.ts` / `types/keyAnalysis.ts` / `paths.ts` / `index.ts`
- `src/mock/enterprise/keyAnalysisSzStatusApi.ts` + `register.ts`
- `src/composables/useKeyEnterpriseAnalysis.ts`
- `src/utils/keyAnalysisParams.ts`
- `src/stores/entRegionScopes.ts`（与企业查询共用）
- `src/components/search/RegionSelect.vue`（format-label / fallback）
- `src/views/enterprise/EnterpriseKeyAnalysis.vue`
- `src/components/enterprise/keyAnalysis/*`

## 架构合规

- 前端只调 Java `/enterprise/topic/v1/**` ✅
- 不直连 Python ✅
- Mock 经 `defineApi` 切换 ✅
- 未改 package.json / vite.config ✅

## 开放项

- `E-ENT-KEYENT-JAVA-L01` 仍 review；联调需网关已挂载 key-analysis
- 侧栏 `showInMenu` 仍为 false（可按产品要求打开）
- 地图坐标仍本地 `DISTRICT_COORDINATES` 补全（API 不返回经纬度）
