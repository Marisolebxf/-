# ENT-SEARCH v1.2 Demo 交接

- 任务：`ENT-MOD-SEARCH-V1-SELECT-ALL-L01`
- 阶段：`v1_hifi_round1`
- 状态：`ENT-SEARCH-SELECT-ALL-PAGE` 已实现并验证。
- 产品口径：仅“全选本页”；查询、结果内再筛、排序、翻页均清除选择；不扩展为跨页或全部命中结果。
- 关键实现：`ResultList.tsx`、`SearchScaffold.tsx`。
- 测试入口：`node tests/enterprise-search-select-all.test.mjs`；真实指针入口：`node tests/enterprise-select-all-pointer.test.mjs`。
- 证据：`evidence/2026-07-20-search-select-all.png`、`evidence/2026-07-20-search-select-all-pointer-evidence.json`。
- 后续：lumen 正式实现按同一 `selectionResetKey` 与当前页范围契约迁移，不复用 Demo mock 数据。
