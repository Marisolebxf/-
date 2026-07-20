# ENT-COMPARE Demo v1.8 增量验证报告

> 验证日期：2026-07-20
> delivery_stage：`v1_hifi_round1`
> 页面：`http://127.0.0.1:4177/enterprise-center/basket`

## 本轮验收结论

| acceptance_unit_id | source_relation | delivery_tier | 状态 |
| --- | --- | --- | --- |
| `ENT-COMPARE-SELECT-ALL-FILTERED` | `product_interpretation` | `DEMO` | verified |
| `ENT-COMPARE-SUPPLY-CHAIN-LIMIT` | `product_interpretation` / Decision 120 | `DEMO` | verified |

- “全选当前筛选结果”合并当前名称与企业类型筛选下的可见企业；取消全选只移除当前可见企业，筛选外选择保留。
- “取消选择”清除全部选择；恢复全部结果后，存在部分选择时全选框呈半选态。
- 已选超过 2 家时，“供应链关系分析”保留在任务选择浮层但禁用，并显示“最多选择 2 家企业”；不静默截断，其他任务不受此规则影响。
- 对比篮标题说明使用稳定评审挂点；业务模式隐藏该挂点，但保留全选和供应链上限业务规则。

## 自动与浏览器验证

- `node tests/enterprise-compare-basket-definition.test.mjs`：通过。
- `node tests/enterprise-select-all-pointer.test.mjs`：通过；Chromium 真实 pointer 点击并用 `document.elementFromPoint` 校验命中。
- `node tests/enterprise-profile-compare-basket.test.mjs`、评审挂点与自隔离回归测试：通过。
- 复合 label 检查、`npm run design:check`、`npm run build`、`git diff --check`：通过；构建仅保留既有大 chunk 警告。
- TRACE、source manifest、implementation coverage、page packages YAML：解析通过。

## 本轮证据

- `evidence/2026-07-20-basket-select-all.png`
- `evidence/2026-07-20-basket-supply-chain-limit.png`
- `evidence/2026-07-20-basket-select-all-pointer-evidence.json`

## 继承证据与剩余边界

- v1.5 的对象分发、返回恢复、权限、工作区布局和目标页自动带入证据继续保留，但因定义升级未在本轮重新宣告 verified。
- lumen 正式实现和服务端单用户持久化契约不在本次修改范围。
