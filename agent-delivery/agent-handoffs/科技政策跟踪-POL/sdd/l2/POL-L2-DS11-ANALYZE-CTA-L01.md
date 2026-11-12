# POL-L2-DS11-ANALYZE-CTA-L01 · 政策分析评价页「先分析后出结果」CTA 对齐原型

[agent:frontend-agent]
- 仓：`lumen-ui-science-pc`（dev；基线 `d167788`，已含 e7da3b1 viz 七块接线）
- 监管：human:淮政玮
- ponytail: full
- 状态：**产物停本地工作区，未 commit/push**（fe-manual-confirm-push 闸门，主会话收口）
- 运行环境：Windows + PowerShell

---

## 1. 范围与实现（对照走查需求真源）

政策分析评价页 `src/views/policy/analysis/index.vue` 三项走查问题全部对齐 demo 原型
（只读参照 `demo-ui-science/src/pages/policy-tracking/PolicyAnalysis.jsx` L1500–1590 与 `analysis/DimensionBar.jsx`，Vue 重写、零代码复制）：

| # | 走查问题 | 实现 |
|---|---------|------|
| ① 布局 | 维度条在页签下方、结果区上方 | 维度条上移至 `PageTabFrame #header` 公共区：**页面标题 → 分析维度条 → 六张统计卡 → 页签 → 结果区**（原型同序），三 Tab 恒定可见 |
| ② 按钮 | 【应用】点击无 loading 即时生效 | 改名【开始分析】；点击后结果区 `a-spin` loading（750ms 最小演示时长） |
| ③ 语义 | 结果直出无分析动作 | 附录 E「先分析后出结果」：进页默认已分析一次（结果直出）；此后改任何维度**不自动刷新**，必须再点【开始分析】才按新维度重算 |

## 2. 布局前后对照

| 前（不对齐） | 后（对齐原型） |
|---|---|
| `#header`：标题 + 统计卡 → 页签 → **维度条** → 结果区 | `#header`：标题 → **维度条** + 统计卡 → 页签 → 结果区 |
| 维度条属 Tab1 内容区，切 Tab 不可见 | 维度条进公共区，三 Tab 恒定（与统计卡同列）；`margin-bottom: 16px`（`.pa-dimension-in-header`，组件自含样式，不裸引他页类名） |

## 3. 交互时序（附录 E 三分支）

| 分支 | 触发 | 行为 |
|------|------|------|
| A 进页 | 页面挂载 | `appliedRun=true` 初始 → loading 不亮；`appliedDimensions=DEFAULT_DIMENSIONS`，219/220 首屏取数一次，结果直出（对照原型与截图 1/2） |
| B 改维度 | 维度条任意筛选项变化 | 只写 `dimensions`（v-model），**`appliedDimensions` 不变** → 219/220 的 watch 不触发、不重取、不闪 loading（结果保持上次分析态） |
| C 点【开始分析】 | DimensionBar `@apply` | `startAnalysis()`：① `appliedDimensions = {...dimensions}` → 219 TrendMetricsChart / 220 RegionGroupCompare watch 即按新维度重取；② `appliedRun=false` → 结果区 a-spin 遮罩（含无维度联动的七 viz 块 metric/portrait/geo/region_impl/topic_heat/topic_sentiment/bubble，同遮罩时序）；③ 750ms 后 `appliedRun=true` 渲染新结果。种子轨（USE_MOCK=true）原有 Message「已按所选维度刷新分析图表（Mock）」保留在回调内，语义一致 |

实现要点：
- `a-spin :loading="!appliedRun"` 包住 `.policy-analysis-page` 滚动壳全部内容（Tab1–Tab3 + 导出弹窗），`display:block` 保证 flex 壳布局不变。
- `appliedRun` 门控而非逐块传 loading prop —— 一处遮罩覆盖全结果区，改动面最小（ponytail）。
- 既有失败防护语义未动（各块 catch 独立置空不清其它块）；D9 角标、PageTabFrame、统计卡结构零改动。

## 4. 安全性核查

- 【应用】→【开始分析】改名：`DimensionBar.vue` 仅被本页挂载；`RegionGroupCompare.vue` 只引 `RESOURCE_TARGET_OPTIONS` 常量（自检断言证实），改名无外溢。
- `appliedDimensions` 写点收敛为 `startAnalysis` 内唯一一处（自检断言「唯一写点」），杜绝旁路自动刷新。

## 5. 自检证据（实跑）

| 检查 | 命令 | 结果 |
|------|------|------|
| 类型门 | `pnpm type-check`（vue-tsc --build） | ✅ 0 error（exit 0） |
| 新自检 | `node --experimental-strip-types src/views/policy/analysis/POL-L2-DS11-ANALYZE-CTA.test.mjs` | ✅ 8 项全过（布局顺序/旧位清除/改名/常量引用 + 三分支 + spin 包裹范围） |
| 既有 FE-POL-02A | 同法 | ✅ 35 组断言全绿（#1 headerBlock：11 张 StatCard / 5 空态卡 / cols-6 全部不破） |
| 既有 VIZ-WIRING | 同法 | ✅ 29 项全过 |
| 既有 VIZ-GAPFILL-L02-FE | 同法 | ✅ 22 组断言全绿 |

新自检断言映射：分支A `appliedRun = ref(true)` + `:loading="!appliedRun"`；分支B `appliedDimensions.value =` 全文唯一且在 `startAnalysis` 体内 + 维度条 v-model 只落 `dimensions`；分支C 函数体内三步（同步 appliedDimensions → loading 置位 → setTimeout 复位）。

## 6. 架构合规自检

| 铁律 | 自检 |
|------|------|
| D8 Design | ✅ 维度条沿用既有 `pa-chart-card` 白卡 + Arco 控件；仅改按钮文案与位置，视觉 token 零新增；对照用户截图「分析维度 ⏲ 标题 + 重置/应用两钮」结构一致（MockBadge 保留） |
| D9 数据血缘 | ✅ 统计卡 / viz 块血缘角标全部未动；无新增统计数字，无需 8 件套 |
| D10 交互规范 | ✅ Arco `a-spin` 行内 loading、`a-button type=primary` 主 CTA、32px 语义不变；「改条件不自动跑、显式 CTA 触发」即附录 E 语义 |
| D12 demo→lumen | ✅ 只读对照 demo 原型后 Vue 重写，零代码复制、零 merge |
| 调用链 | ✅ 仍走前端 → Java REST → Python `/internal/*`，未新增直连 |

## 7. 产物清单（文件清单）

| 文件 | 改动 |
|------|------|
| `src/views/policy/analysis/DimensionBar.vue` | 按钮文案【应用】→【开始分析】（+注释） |
| `src/views/policy/analysis/index.vue` | ① 维度条挪入 `#header`（标题后、统计卡前）；② `applyDimensions` → `startAnalysis`（appliedRun 门控 + 750ms）；③ `a-spin` 包结果区；④ scoped 样式 `.pa-dimension-in-header` |
| `src/views/policy/analysis/POL-L2-DS11-ANALYZE-CTA.test.mjs` | 新增自检（8 断言） |
| `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-ANALYZE-CTA-L01.md` | 本 handoff |

未改动：`.gitignore` / `package.json` / `vite.config.*`（禁改清单）；无新依赖。

## 8. 偏离说明

- 750ms 最小演示时长取走查要求区间 600–900ms 中值：纯前端演示节奏，不涉真算（真轨 219/220 请求本身仍异步完成，遮罩保证不早于 750ms 消失）。
- loading 遮罩采用整结果区包裹而非逐块：七 viz 块无维度联动但同属「分析动作后的呈现区」，整体遮罩与原型观感一致且改动面最小。

## 9. 验收建议（主会话/监管人）

1. `USE_MOCK=true` 与 `false` 各进页一次：结果直出、无 loading。
2. 任意改维度（时间/地区/类别/投向/指标）：页签下结果**不**变化。
3. 点【开始分析】：结果区 750ms 遮罩 → 恢复；219 趋势/220 区域对比按新维度重取（Network 面板可见新请求）。
4. 布局顺序目检：标题 → 分析维度条 → 六张统计卡 → 页签 → 结果区；切 Tab 维度条不消失。
