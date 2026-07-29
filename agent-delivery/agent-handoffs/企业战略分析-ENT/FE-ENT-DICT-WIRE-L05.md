# Handoff：FE-ENT-DICT-WIRE-L05

- **task-id**：`FE-ENT-DICT-WIRE-L05`
- **执行**：`agent:frontend-agent`
- **监管**：`human:淮政玮`
- **认领**：`coordinator_dispatch` · `claimed_at=2026-07-29T21:05:00+08:00` → `in_progress` → `review` → **`done`**
- **性质**：实现类（`cicd: required` · `lumen-ui-topic`）
- **日期**：2026-07-29
- **上游**：`API-ENT-DICT-JAVA-L04`（done · lumen commit `6316e54`）

> **Coordinator 验收纪要（2026-07-29T21:50）**：Q056–Q059 DoD 对照 handoff 通过；`lumen-ui-topic@5478aee` 已 push `origin/dev`。企业字典闭环 L03–L06 全部 done。  
> **补记（2026-07-29 · human:淮政玮）**：CI + 现网冒烟已通过 → 原「待 CI type-check」残差关闭。

---

## 1. 范围与实现（对照 Q056–Q059 / DoD）

| DoD | 状态 | 证据 |
|-----|------|------|
| RegionSelect / 结果区级联默认走 Java `region-scopes`；`regionOptions.ts` 仅 fallback | ✅ | `entSearchMetaRegionScopes` + `loadMeta`；`regionScopesToCascaderOptions` → `SearchScaffold` → `ResultToolbar` → `RegionSelect.cascaderOptions`；本地写死降级为 fallback |
| 高筛：工商类型 + 资质标签双字段（Q057） | ✅ | `company_type` 标签「工商类型」；`tags_flat` 标签「资质标签」；废弃混选项 mock |
| 规模：大中小微 + 规上可叠加（Q058） | ✅ | `enterprise_scale` 四档；独立 `is_above_scale` boolean；meta `is_above_scale` 写入字段库 |
| 上市：上市/未上市/退市（不加「已」）（Q059） | ✅ | `listing_status` multiSelect；替换原 `isListed` 布尔筛选项；mock filters 对齐 |
| 只调 Java，不直连 Python `/internal/*` | ✅ | 全部经 `EnterpriseTopicPaths` → `/enterprise/topic/v1/search/meta/*` |
| observability 新请求路径按仓规 | ✅ | 新 API 走既有 `request.ts` 拦截器（`extractTraceId` / Grafana 深链）；未新增越层调用 |
| handoff + cost 四字段 | ✅ | 本文件 + registry |
| 明确不做：改 Java/Python 契约、全量国标灌数 | ✅ | 未改后端仓 |

---

## 2. 关键文件（`lumen-ui-topic`）

| 区域 | 文件 | 变更 |
|------|------|------|
| API | `src/api/enterprise/paths.ts` | `searchMetaRegionScopes` |
| API | `src/api/enterprise/types.ts` | `EntRegionScope*` / `EntAboveScaleOption`；filters/scales 补 `is_above_scale` |
| API | `src/api/enterprise/search.ts` + `index.ts` | `entSearchMetaRegionScopes` |
| Meta 加载 | `src/composables/useEntServerSearch.ts` | `loadMeta` 并行拉 region-scopes |
| 装配 | `src/components/search/SearchScaffold.vue` | 注入 `regionCascaderOptions` |
| Region | `RegionSelect.vue` / `ResultToolbar.vue` / `regionOptions.ts` | 权威树优先；写死仅 fallback |
| 字段库 | `filterFieldSchema.ts` / `applyEntMetaToFieldLibrary.ts` | Q057–Q059 对齐 |
| Mock | `topicApi.ts` / `smartParser.ts` | listing/scales/region-scopes mock |
| 展示兼容 | `enterpriseTypeContext.ts` | 微型纳入小微标签 |

编排仓：本 handoff + `task-registry.yaml` → `review` + cost。

---

## 3. 验收要点

1. **结果区 RegionSelect**：`serverSearch=true` 时请求 `POST /enterprise/topic/v1/search/meta/region-scopes`（`mode=tree`）；失败时回退 `regionOptions.ts`。
2. **高级筛选字段库**：可见「工商类型」「资质标签」分栏；规模为大型/中型/小型/微型 +「规上」独立开关；上市状态为上市/未上市/退市。
3. **meta 覆盖**：`filters` / `company-types` / `enterprise-scales` / `tags` 成功时覆盖本地 options；`is_above_scale` 从 scales 或 filters 写入。
4. **调用链**：Network 无 Python `/internal/*` 直连。
5. **Design / 交互**：沿用 Arco Cascader/Select；控件高小尺寸与既有 ResultToolbar 一致（Design.md §7 / 交互规范状态覆盖）。

---

## 4. 偏离与开放项

| 项 | 说明 |
|----|------|
| 本机未跑 `npm run type-check` / `build` | 环境无 `node`/`npm` PATH；依赖 CI Pipeline 绿 |
| `isListed` 仍存于列表 Mock / 画像展示 | 高筛已改 `listing_status`；卡片布尔字段展示兼容保留，待列表 DTO 全量带 `listing_status` 后再清 |
| listing/规上 ES 派生 | 归 `DATA-ENT-LISTING-SCALE-ETL-L06`；本单仅 meta/UI 接线 |
| portalAggregates 等统计 mock 仍含「小微/规上」互斥口径 | 非本单检索主路径；可 follow-up |

---

## 5. Design.md / 交互规范检查要点

| 检查 | 结果 |
|------|------|
| Design.md §14：主色/Arco Cascader/Select、无新增 AntD | ✅ |
| UX-UE §3.4：Cascader `change-on-select`、键盘/aria-label「选择区域」保留 | ✅ |
| D9：本单为字典枚举接线，无新增裸统计数字 | ✅ N/A（未新增指标卡） |

---

## 6. 架构合规自检（§2）

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法只在 Python | ✅ |
| 2 | FE→Java→Python | ✅ 仅 Java REST |
| 3 | NebulaGraph | ✅ 不涉及 |
| 4 | 可观测性 | ✅ 既有 request + observability |
| 5 | CI/CD required | ⏳ push 后 Pipeline |
| 6 | demo 不 merge lumen | ✅ 只改 lumen-ui-topic |
| 7 | 共享聚合 / 不直连 nGQL | ✅ |
| 8 | ADS/码表 | ✅ 读 Java meta |
| 9 | Design.md | ✅ |
| 10 | D9 | ✅ N/A 字典 |
| 11 | D10 交互规范 | ✅ |

---

## 7. Cost 四字段（回填 registry）

| 字段 | 值 |
|------|-----|
| `actual_tokens` | ~140000（估） |
| `model_used` | cursor-grok-4.5 |
| `actual_cost` | ~2.5（估 USD） |
| `cost_warn` | green |

---

## 8. Git

- 仓：`lumen-ui-topic` → `origin/dev` · SHA **`5478aeec9f2f6edd9786479512a61dea8be87d04`**
- 编排：`gkx-orchestration` → `origin/dev`
- message 含 `[agent:frontend-agent]`
- 禁止 force；已 `pull --rebase` 解决与上游 refactor（types/ 拆分、fixtures 迁移、SearchScaffold composable 化）冲突后推送

