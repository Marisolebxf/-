# Frontend handoff：ENT-MOD-SEARCH-V2-S4

- 时间：2026-07-18（完善续作；首版 2026-07-15）
- 仓库：`repos/lumen-ui-topic`
- 分支：`dev`（监管确认直改）
- 监管人：`human:孔东`
- 执行：`agent:frontend-agent`
- CI：本地改动文件 type-check 无新增报错；仓内既有 `mock/enterprise` duplicate key / `AdvancedFilterView` 类型问题未纳入本轮
- 复刻自：demo `SearchPage.tsx` + `FilterPanel` / `FilterTemplateManager`
- 覆盖：规划 4.1 / 4.3 / 4.4 + **高筛 FilterPanel 接入**（完善）

## 本轮完善（2026-07-18）

| # | 产物 | 说明 |
|---|---|---|
| 高筛接入 | `EnterpriseSearch.vue` `#advanced-filter` | 注入 `FilterPanel`（page）+ `FilterTemplateManager`（页脚保存/使用） |
| 我的方案 | `SearchHub.vue` + `SearchScaffold.vue` | `mode=advanced` 隐藏「最近检索」，显示「我的方案」标签；点击 = 使用查询方案（载入 DSL 并应用） |
| 方案同源 | `composables/useFilterTemplates.ts` | Hub / TemplateManager 共享同一 storage ref |
| 菜单 | `router/menu.ts` | 侧栏「高级筛选」`showInMenu: false`（路由保留） |

## 范围与实现（含首版）

| # | 产物 | 说明 |
|---|---|---|
| 4.1 | `EnterpriseSearch.vue` + `config/enterpriseSearch.ts` | 正式查询页；URL 初始化；数据经 `api/enterprise.ts` |
| 4.3 | `EnterpriseCompare.vue` | 对比篮薄封装 |
| 4.4 | `router/menu.ts` | 企业查询 / 对比篮挂真页；高级筛选侧栏暂隐 |
| 详情 | PROFILE owner | 不双写 |

## 偏离说明

1. **高筛**：已从 Empty 占位改为 FilterPanel 接入（监管 2026-07-18 确认，不再等 COMPONENTS done）。
2. **我的方案位置**：Hub 仅标签列表；保存仍在 Panel 页脚（方案 A）。
3. **侧栏高级筛选**：暂隐；独立页 `AdvancedFilterView` 路由仍可直达。
4. **详情**：仍归 PROFILE，本任务不双写。

## demo vs lumen 对照

| 对照项 | demo | lumen S4 | 状态 |
|---|---|---|---|
| 查询页 SearchScaffold | ✅ | ✅ | ✅ |
| FilterPanel 接入 | ✅ | ✅ page 变体 | ✅ |
| advanced 下方案入口 | queryPlans | 我的方案标签 + 页脚 TemplateManager | ✅ |
| 对比篮 | ✅ | ✅ | ✅ |
| 详情整页 | Profile | PROFILE owner | ⚠️ intentional |

## 验收建议

1. 打开 `/enterprise/enterprise-search` → 切「高级筛选」→ 见 FilterPanel，**不见**最近检索，见「我的方案」
2. 添加条件 →「保存为查询方案」→ Hub「我的方案」出现标签 → 点击标签应载入并应用查询
3. 侧栏无「高级筛选」菜单项；直达 `/enterprise/enterprise-advanced-filter` 仍可开独立页

## 架构合规自检

1–11：与首版一致；本轮仅前端装配，接口仍经 `api/enterprise.ts` ✅

## Cost 回填（续作增量估）

| 字段 | 值 |
|---|---|
| `actual_tokens` | ~120_000（含首版累加估） |
| `model_used` | cursor-grok-4.5 |
| `actual_cost` | ~0.60 |
| `cost_warn` | green |

## 开放项

1. 监管确认后 commit / push `dev`（本会话未自动 commit）
2. PROFILE 交付后替换详情 stub
3. 飞书多维表 `recvpmwLY2Z2b6` 状态同步（coordinator）
4. 仓内既有 type-check 杂音（mock duplicate key）另单清理
