# FE-ENT-ADV-FILTER-WIRE-L01 · 前端对接枚举契约（lumen-ui-topic）

> **移交**：2026-08-03 `human:孔东` → `human:曹丽影` 接着处理高筛页面适配  
> 上游：`ENT-JAVA-ENUM-CONTRACT-L02`（另开 FE-ENT-ADV-FILTER-WIRE）  
> 仓：`lumen-ui-topic` · `dev` → `origin/dev`

## 认领 / 移交

| 阶段 | 字段 | 值 |
|------|------|-----|
| 初领 | claimed_by / supervised_by | `agent:frontend-agent` / `human:孔东` |
| 初领时间 | claimed_at | `2026-08-03T10:53:41+08:00` |
| 移交后 | status | `in_progress`（曹丽影认领续作 2026-08-03T16:30） |
| 续作认领 | claimed_by / supervised_by | `human:曹丽影` / `human:曹丽影` |
| 续作时间 | claimed_at / in_progress_at | `2026-08-03T16:30:00+08:00` |
| 移交后 | supervised_by | `human:曹丽影` |
| 移交时间 | | `2026-08-03T11:52:32+08:00` |

## 孔东已交付（接口对接，本阶段止于此）

| 项 | 结果 |
|----|------|
| `#137` `POST .../meta/query-tree-schema` | ✅ paths + types + `entSearchMetaQueryTreeSchema` + mock |
| `#9` filters 三数组 | ✅ `stock_types` / `supply_chain_roles` / `core_tech_tags` |
| 出站 op 粗映射 | ✅ UI `containsAll/notContainsAll/has/none` → `all/not_in/exist` |
| 上市/规模纠错 | ✅ 热门预设「上市」；「规上」拆 `is_above_scale` |
| bootstrap 挂 schema | ✅ `applyQueryTreeSchemaToFieldLibrary`（基础版） |
| 顺带修 | 评估历史 list 不传 `subType`；重点分析区域标题码→名 |
| type-check | ✅ |

## 曹丽影续作交付（2026-08-03）

| 项 | 结果 |
|----|------|
| 字段别名双向映射 | ✅ `entQueryTreeWire.ts`：`tags_flat↔tag`、`region_id↔enterprise_region`、`industry_chain_names_flat↔industry_chain`、`registered_capital_value↔registered_capital` |
| 出站 query_tree | ✅ `filterDslToQueryTree.ts` 经 wire adapter 输出契约 `field` / `operator` |
| exist 字符串 | ✅ `has/none` → `exist` + `"1"`/`"0"` |
| is_above_scale 对象枚举 | ✅ 出站 `eq` + `{ code, name, field, combinable }`；入站 history 反解为 UI `eq` + boolean |
| neq / gt / lt | ✅ 类型 + ConditionBuilder 标签 + schema 动态暴露（如注册资本） |
| is_chain_leader | ✅ UI 仅 `eq`；出站 `eq`+boolean（非 exist）；mock schema 补字段 |
| mock #137 对齐 | ✅ wire 字段名 + `is_above_scale` 对象枚举 + `tags_flat` deprecated |
| build | ✅ `npm run build` |

### 变更文件（lumen-ui-topic，未 push）

- **新增** `src/utils/entQueryTreeWire.ts`
- `src/utils/filterDslToQueryTree.ts`
- `src/utils/applyQueryTreeSchemaToFieldLibrary.ts`
- `src/components/filter/FilterEngine.ts`（`fromQueryExpress` 入站 wire→UI）
- `src/components/filter/ConditionBuilder.vue`
- `src/types/filter.ts`
- `src/fixtures/enterprise/filterFieldSchema.ts`
- `src/mock/enterprise/topicApi.ts`

## 产物（孔东阶段，已合入）

- `src/api/enterprise/paths.ts` / `search.ts` / `types/search.ts` / `index.ts`
- `src/utils/filterDslToQueryTree.ts` / `applyQueryTreeSchemaToFieldLibrary.ts`（新增）
- `src/utils/applyEntMetaToFieldLibrary.ts` / `keyAnalysisParams.ts`
- `src/composables/useEntServerSearch.ts` / `useSearchBootstrap.ts` / `enterpriseEvalLoaders.ts` / `useKeyEnterpriseAnalysis.ts`
- `src/config/enterpriseSearchConfig.ts` / `views/enterprise/EnterpriseSearch.vue`
- `src/components/enterprise/keyAnalysis/TypeRegionPanel.vue`
- `src/fixtures` / `src/mock/**`

## cost（孔东阶段）

| 字段 | 值 |
|------|-----|
| `actual_tokens` | 90000 |
| `model_used` | cursor-grok-4.5 |
| `actual_cost` | 1.8 |
| `cost_warn` | green |

## cost（曹丽影续作）

| 字段 | 值 |
|------|-----|
| `actual_tokens` | 45000 |
| `model_used` | composer-2.5 |
| `actual_cost` | 0.9 |
| `cost_warn` | green |
