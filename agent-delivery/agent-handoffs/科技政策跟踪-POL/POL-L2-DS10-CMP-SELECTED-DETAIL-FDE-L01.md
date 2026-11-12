# POL-L2-DS10-CMP-SELECTED-DETAIL-FDE-L01 · handoff

- 监管人：human:淮政玮
- 执行：agent:fullstack-agent
- 日期：2026-11-12
- ponytail: full（复用 PolicyDetailDrawer / openLiveDetail；未新造详情页）

## 范围与实现

214-7：政策详情对比弹窗常显已选政策列表；点击打开全景既有详情（live=`openLiveDetail`，mock=`PolicyDetailDrawer`）。顺带修 `v-model:selected` ↔ prop `selected` 接线。

## 产物

| 仓 | 改动 |
|---|---|
| `lumen-ui-science-pc` | `ComparisonModal.vue` 已选列表 + `open-policy`；`index.vue` `onOpenPolicyFromCompare`；`FE-POL-01B.test.mjs` 锚点 |
| `gkx-orchestration` | FDE 计划 / A·B 简报 / 会签；合规用例 214 行补形态 |

## 验收证据

- `pnpm type-check` 绿
- `node src/views/policy/panorama/FE-POL-01B.test.mjs` 绿

## 架构合规

- 调用链：前端 → 既有 detail；无越层
- D12：未调 demo 服务
- 用户可见文案：已选列表为业务话；无 Job/gapfill 黑话进 DOM

## cost（估）

- actual_tokens: ~45000
- model_used: composer
- actual_cost: ~0.5
- cost_warn: green
