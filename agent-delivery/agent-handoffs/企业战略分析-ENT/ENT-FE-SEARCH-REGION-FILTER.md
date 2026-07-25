# ENT-FE-SEARCH-REGION-FILTER · 高级筛选「企业所属地区」

> 状态：实现完成，**待人工检查后再 commit**（监管人：徐滕强）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| claimed_at | `2026-07-24T18:30:00+08:00` |
| lock_until | `2026-07-24T22:30:00+08:00` |

## 范围与实现

1. 字段库「注册区县」改为「企业所属地区」
2. 控件由深圳区县多选改为全国省市区 Cascader 多选（可搜）
3. 运算符默认「包含任意」；条件值存行政区划编码
4. 本地 Mock 评估支持省/市/区命中

## 产物

- `repos/demo-ui-topic/src/app/mock/enterprise/regionTree.ts`
- `repos/demo-ui-topic/src/app/mock/enterprise/filterFieldSchema.ts`
- `repos/demo-ui-topic/src/app/components/search/ConditionBuilder.tsx`
- `repos/demo-ui-topic/src/app/components/search/queryEngine.ts`
- `repos/demo-ui-topic/tests/enterprise-region-filter-contract.test.mjs`

## 说明

正式仓 `lumen-ui-topic` 当前无高级筛选组件落地（历史 COMPONENTS 未 commit），本轮改 `demo-ui-topic` 可见实现，并对齐 Java/Python meta/regions 契约。
