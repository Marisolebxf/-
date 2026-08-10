# FE-DISPLAY-GI-TOPBAR-OVERLAY-L01 · 全球创新监测详情顶栏按钮遮挡领域筛选修复

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch`（2026-08-09 监管人截图报告，会话直接指示修复） |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最短修复路径：3 条 CSS 属性解决遮挡；顺手修的「框选断线」为验证期发现的同文件根因缺陷（共享函数缺 key），按"修共享函数一次"原则落在 detailMapToolbar 本地动作，未扩散改动面。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip`（MCP 已挂载；本单为定点 CSS/JS 修复，无大日志） |

## 问题清单

1. **本单主问题**：全球创新监测 → 创新成果展示页，`订阅区域 / 推送记录 / 对比分析` 三按钮遮挡「领域」筛选（监管人截图，1024px 视口）。
   - 根因：`.gi-detail-topbar` 定高 `flex: 0 0 83px` 不换行；`.gi-detail-filter`（flex 可缩、min-width:0）内四个定宽子项（220+190+300+340px）在窄视口溢出，与 flex 末尾的按钮组交叠。
2. **验证期发现的存量断线（顺带修复）**：`InnovationDetail.test.mjs` 基线失败——详情页地图工具栏缺「框选区域」。根因：详情页图标/激活态/处理器全接 `MAP_TOOLBAR_ACTIONS.selectArea`，但共享 `mapToolbar.js` 未定义该 key（`getMapToolbarItems({withAreaSelection:true})` 被静默忽略），框选功能整体不可达。
   - 约束冲突：`globalSituationMapSectionRuntime.test.mjs` 明文禁止 `selectArea/withAreaSelection/框选` 出现在全域地图链路（App.jsx/SharedRegionMap.jsx/mapToolbar.js）——P0 移除决策，不得回退。
   - 解法：框选动作**本地化**到 `detailMapToolbar.js`（`DETAIL_MAP_ACTION_SELECT_AREA`），详情页三处引用改本地常量；`mapToolbar.test.mjs` 移除与 P0 决策矛盾的过期 `withAreaSelection` 断言（加注释指向两处真源）。

## 修改内容（commit `0d44168`，push origin/dev + dev:main）

- `src/pages/global-innovation/style.css`：`.gi-detail-topbar` 改 `flex: 0 0 auto + flex-wrap: wrap`（保留 min-height 83px）；`.gi-detail-filter` 加 `flex-wrap: wrap + row-gap`；`.gi-detail-top-actions` 加 `margin-left: auto`（换行后仍右对齐）
- `src/pages/global-innovation/tabs/detailMapToolbar.js`：本地框选动作
- `src/pages/global-innovation/tabs/InnovationDetail.jsx`：三处 `MAP_TOOLBAR_ACTIONS.selectArea` → `DETAIL_MAP_ACTION_SELECT_AREA`
- `src/pages/global-innovation/tabs/InnovationDetail.test.mjs`：新增 3 条顶栏布局断言（换行/右对齐防回退）
- `src/mapToolbar.test.mjs`：移除过期断言

## 测试结果

- `InnovationDetail.test.mjs` ✅（基线失败已修）· `detailMonitorModel` ✅ · `globalInnovationLayout` / `GlobalInnovationTabs` ✅ · `globalSituationMapSectionRuntime` ✅（P0 移除约束保持）· `mapToolbar.test.mjs` ✅ · tech-index-new 自检 ✅（回归）
- `npm run build` ✅（2m07s）
- 基线核证（git stash 对照）：`globalSituationP0.test.mjs`（TOP5 聚类断言）与 `shenzhenInnovationLayout.test.mjs`（载体排行卡片结构）在干净 HEAD 即失败，与本单无关，未动；建议另立 bugfix 单处理

## 遗留风险

- 窄视口下按钮组换行到第二行右对齐；中等宽度（1200–1500px）下筛选组内部换行，均经 CSS 断言锁定；实际视觉效果请监管人在 30999 复查
- 框选按钮恢复显示后，框选交互链路（高德 MouseTool）建议 QA 抽查一次

## CI/CD

- 分支：dev commit `0d44168` → push `origin/dev` + `dev:main`（8a46d7d..0d44168，非 force）
- 部署：静态站 30999，push 后 2–3 min 生效

## 架构合规自检（§2）

| # | 铁律 | 结果 |
|---|---|---|
| 1-4 | 算法/调用链/图谱/可观测 | N/A（纯 CSS + 本地常量） |
| 5 | CI/CD | ✅ push main → 30999 |
| 6 | demo 只读 merge | ✅ 仅 demo-ui-science |
| 9-11 | D8/D9/D10 | ✅ 无 UI 体系/指标/交互语义变更；恢复既有设计内的框选按钮 |

## 成本回填

| 字段 | 值 |
| --- | --- |
| actual_tokens | 220000（估，含截图放大定位与基线对照） |
| model_used | kimi-k3 |
| actual_cost | 2.2 USD（估） |
| cost_warn | green |

## 建议下一状态

bugfix：handoff 已交 → `pending_test`；请监管人在 30999「全球创新监测 → 创新成果展示」复查窄屏遮挡消除 + 框选按钮出现。
