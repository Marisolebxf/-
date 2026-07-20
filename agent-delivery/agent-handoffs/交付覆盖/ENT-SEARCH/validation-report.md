# ENT-SEARCH v1.2 Demo 验证报告

> 验证日期：2026-07-20
> delivery_stage：`v1_hifi_round1`
> 页面：`http://127.0.0.1:4177/development/search`

## 验收结论

| acceptance_unit_id | source_relation | delivery_tier | 状态 |
| --- | --- | --- | --- |
| `ENT-SEARCH-SELECT-ALL-PAGE` | `product_interpretation` | `DEMO` | verified |

- “全选本页”只选择当前分页 9 家企业；复选框支持未选、半选、全选三态。
- 重新查询、结果内再筛、排序或翻页会通过 `selectionResetKey` 清除旧选择，避免把不可见对象带入批量动作。
- 卡片逐项选择与全选共用同一批量操作栏；“取消选择”清除当前选择。
- 业务 / 评审模式共用同一业务控件；全选没有评审挂点。评审追溯使用稳定 `data-review-mount-id`。

## 自动与浏览器验证

- `node tests/enterprise-search-select-all.test.mjs`：通过。
- `node tests/enterprise-select-all-pointer.test.mjs`：通过；Chromium 真实 pointer 点击并用 `document.elementFromPoint` 校验命中。
- 相关企业对比篮 / 评审模式回归测试：通过。
- 复合 label 检查、`npm run design:check`、`npm run build`、`git diff --check`：通过；构建仅保留既有大 chunk 警告。

## 证据

- `evidence/2026-07-20-search-select-all.png`
- `evidence/2026-07-20-search-select-all-pointer-evidence.json`

## 剩余边界

- 不支持跨页全选或全命中集合选择。
- 本轮只验证 Demo；lumen 正式实现不在本次范围。
