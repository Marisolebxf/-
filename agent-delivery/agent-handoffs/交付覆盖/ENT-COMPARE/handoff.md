# ENT-COMPARE Demo v1.8 增量交接

- 任务：`ENT-MOD-COMPARE-V1-SELECT-ALL-L01`
- 阶段：`v1_hifi_round1`
- 本轮状态：筛选结果全选与供应链 2 家上限均已实现并验证。
- 全选口径：只作用于当前名称 / 企业类型筛选可见集合；取消全选不影响筛选外选择；“取消选择”清除全部选择。
- 供应链口径：继承 Decision 120 与 ENT-RISK 的 1～2 家契约；超过 2 家时任务选项保留、禁用并说明上限，不静默截断。
- 关键实现：`repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseCompareBasketPage.tsx`。
- 测试入口：`node tests/enterprise-compare-basket-definition.test.mjs`；真实指针入口：`node tests/enterprise-select-all-pointer.test.mjs`。
- 证据：`evidence/2026-07-20-basket-select-all.png`、`evidence/2026-07-20-basket-supply-chain-limit.png`、`evidence/2026-07-20-basket-select-all-pointer-evidence.json`。
- 后续：lumen 正式实现继续保留目标页同规则防御校验；不得仅依赖对比篮前置禁用。
