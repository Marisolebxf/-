# FE-ENT-ADV-FILTER-WIRE-L01 · 前端对接枚举契约（lumen-ui-topic）

> **移交**：2026-08-03 `human:孔东` → `human:曹丽影` 接着处理高筛页面适配  
> 上游：`ENT-JAVA-ENUM-CONTRACT-L02`（另开 FE-ENT-ADV-FILTER-WIRE）  
> 仓：`lumen-ui-topic` · `dev` → `origin/dev`

## 认领 / 移交

| 阶段 | 字段 | 值 |
|------|------|-----|
| 初领 | claimed_by / supervised_by | `agent:frontend-agent` / `human:孔东` |
| 初领时间 | claimed_at | `2026-08-03T10:53:41+08:00` |
| 移交后 | status | `ready`（交曹丽影认领续作） |
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

## 交曹丽影续作（高筛页面 ↔ 真实 #137 适配）

对照现网 #137 实测响应，**暂未做**（孔东确认先不动）：

1. **字段别名**：本地 key（`tags_flat` / `region_id` / `industry_chain_names_flat` / `registered_capital_value` 等）↔ schema `field`（`tag` / `enterprise_region` / `industry_chain` / `registered_capital`…）；出站 `query_tree.field` 须用契约名  
2. **`is_above_scale` 对象枚举**、`exist` 值 `"1"`/`"0"` 字符串  
3. **`neq` / `gt` / `lt` UI 暴露**；`is_chain_leader` 按 `eq`+boolean 而非 exist  
4. mock / 字段库与真实 `fields`+`enums` 对齐  

## 产物（已合入，待 push）

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
