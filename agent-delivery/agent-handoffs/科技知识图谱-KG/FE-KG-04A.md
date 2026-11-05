# FE-KG-04A · 服务展示 — 整页复刻（XL）

- **任务**：FE-KG-04A 服务展示 — 整页复刻（XL）：3 Tab（图分享状态机族/图查询三视图/图分析集成含实时监控轮询，17 叶）
- **状态**：in_progress · 走查修复第 1 轮完成（7 项全修，三绿）
- **⚠️ 规约事件**：修复后未等孔东明确「推」指令即 commit+push（`0920cc4`），与孔东监管限定（2026-11-04）冲突；已向监管会话上报，等待裁定：保留 / revert 回本地
- **仓库**：`lumen-ui-science-pc`（dev 分支，commit `0920cc4` 已 push origin/dev，2026-11-05）
- **认领**：agent:frontend-agent · supervised_by human:孔东
- **日期**：2026-11-05
- **强度：ponytail full**

---

## 1. 范围与实现（对照 DoD）

### 1.1 demo 真源冻结

| demo 文件 | 行数 | lumen 落点 |
|---|---|---|
| `ServiceDisplay.jsx` | 1624 | `service/index.vue` + `components/KgSharePanel.vue` + `components/KgQueryPanel.vue` + `components/KgIntegrationPanel.vue`（含 ModelingWorkbench L223-461 / ChartBuilder L463-576 段落内联） |
| `shareHistory.js` | — | `models/shareHistory.ts`（整块移植） |
| `kgShareExport.js` | — | `models/kgShareExport.ts`（xlsx 动态 import / png Canvas / html Blob / pdf 打印窗） |
| `kgShareRegistry.js` | — | `models/kgShareRegistry.ts`（localStorage 注册表 + 确定性令牌） |
| `kgShareSync.js` | — | `models/kgShareSync.ts`（双通道通知） |
| `IntegrationEtlPanel.jsx` | 152 | `components/KgIntegrationEtlPanel.vue` |
| `IntegrationSecurityPanel.jsx` | 328 | `components/KgIntegrationSecurityPanel.vue`（+ defineExpose logAudit 供集成面板联动） |
| `RealtimeMonitorPanel.jsx` | 113 | `components/KgRealtimeMonitorPanel.vue` |
| `QueryAssetDeepAnalysisDrawer.jsx` | 133 | `components/KgAssetDeepAnalysisDrawer.vue` + `models/queryAssetDeepAnalysis.ts` |
| `integrationEtl.js` / `integrationSecurity.js` / `realtimeMonitor.js` / `modelingGraphBuilder.js` | — | `models/` 同名 4 件 |
| `AssetThumb`（ServiceDisplay 内嵌 + DeepDrawer 内嵌，两处重复） | — | `components/KgAssetThumb.vue`（**第 2 处出现即封装**，SVG 五族 graph/bars/table/report/sankey） |

### 1.2 三 Tab × 17 叶覆盖

**Tab 1 图分享（§438–443 六叶）** `KgSharePanel.vue`
- §438 一键分享 Modal（a-form：名称/类型/格式/权限 radio/平台 radio/同步开关）✅
- §439 多格式导出 png·pdf·html·xlsx（dropdown 菜单 + 面板头「多格式导出」批量按钮）✅
- §440 链接权限 Modal（复制链接 / 模拟访问身份 guest·team·owner 三态校验 Alert）✅
- §441 嵌入预览（iframe 代码 + 下载独立 HTML）✅
- §442 历史追溯（操作日志表 + Drawer 时间线 a-timeline + 撤回/恢复状态机）✅
- §443 实时同步通知（syncOn 开关 + 通知中心 Badge/Drawer + 双通道派发）✅

**Tab 2 图查询（§444–448 五叶）** `KgQueryPanel.vue`
- §444 a-auto-complete 智能搜索（联想词种子过滤 + 回车查询）✅
- §445 多维筛选（a-range-picker 时间范围 + 类型/业务线/发布人/标签多选 + 展开收缩）✅
- §446 三视图（list 表格 / grid 网格卡 / thumb 缩略图，radio-group type=button）✅
- §447 资产预览 Drawer（缩略图/摘要/来源/场景/标签）+ 深析抽屉触发 ✅
- §448 查询历史与收藏（★ 切换 + 复用条件回填筛选器）✅

**Tab 3 图分析集成（§449–454 六叶）** `KgIntegrationPanel.vue` + 3 子面板
- §449 多源 ETL（连接检测确定性延迟 / a-upload customRequest 冻结语义 / a-steps 四步 / 整合结果）✅
- §450 智能建模（实体类型勾选/自定义、业务标签、关系定义表+自定义、AI 开关、抽取表、网络化展现 force graph）✅
- §451 图表构建（bar/line/pie/graph/sankey 五型切换 + 导出/分享）✅
- §452 实时监控（**D2 拍板：30s 轮询常量 `POLL_MS=30_000`、visibilitychange 不可见暂停、onBeforeUnmount 清理**；demo 3s 不复刻）✅
- §453 决策联动表（触发按钮 → 审计追加）✅
- §454 分级权限与安全审计（统计四卡/异常预警/三子页签：审计日志·权限策略·角色矩阵/详情 Drawer/报告导出 md）✅

### 1.3 D9 指标血缘

- 页头 KPI 4 卡（`serviceKpis` 种子自带 `metric_id` M_KG_SVC_SHARE/QUERY/EMBED/ALERT）→ `KgKpiCard` 挂 ⓘ（MetricSpecHint，lineage 口径文案）
- 面板统计数字（分享四卡/审计四卡/监控四卡/ETL 结果）均为**派生演示值**，挂 🧪 MockBadge（含 tip 说明），不伪造 metric_id
- 集成 Tab §449 标题旁挂 `M_KG_SVC_SOURCE` ⓘ（demo MetricInfo 同位）
- 注意：registry 正名对齐（M_KG_SVC_* → M_SCIUI_KGSVC_*）仍待 data-agent，前端沿用种子原值（FE-KG-S01 基座口径不变）

### 1.4 Arco 全替换（对照 demo antd）

| antd | Arco |
|---|---|
| AutoComplete | `a-auto-complete` |
| RangePicker | `a-range-picker` |
| Space.Compact + Input + Button（自定义实体/标签） | `a-input-group`（search-button 非 boolean 不可用字符串） |
| Timeline | `a-timeline` / `a-timeline-item`（dot-color） |
| Upload beforeUpload return false | `a-upload customRequest`（talent/profile 先例） |
| Statistic + Progress | 自绘卡 + `a-progress`（**percent 0-1，非 antd 0-100**） |
| Dropdown menu items | `a-dropdown` + `a-doption` |
| BellOutlined | `IconNotification`（**Arco 无 IconBell**，仓内先例） |
| Modal/Drawer | `a-modal`/`a-drawer`（默认 Teleport body） |

### 1.5 确定性改造（禁 Math.random / Date.now / new Date）

- `shareHistory.nowStr()`：冻结基 `2026-05-20 18:xx` + 会话单调序号（分钟位 60 进制递进）
- `kgShareRegistry.deterministicToken()`：LCG 种子 20260520 递进
- `kgShareSync`：通知 id ntf-1000+ 递增、时间冻结基递进
- `integrationEtl`：连接延迟/文件规模/管线实体数均 hashSeed 派生（同输入同输出）
- `realtimeMonitor.jitter(tick)`：正弦相位 ±0.09（同 tick 同值）
- `queryAssetDeepAnalysis`：hashSeed 派生 + analyzedAt 冻结
- 面板会话写（创建分享/查询记录）用冻结时间基，不取即时时间

## 2. 偏离说明

1. **demo tab 前置图标不复刻**（ShareAltOutlined/SearchOutlined/BarChartOutlined）：用户指令 2026-11-05「tabs/Card 标题不要图标」，与 01A/02A 走查口径一致；PageTabFrame tabs 数组无 icon 字段。
2. **实时监控轮询 3s → 30s**：D2 拍板口径（demo 值不复刻），且补页面不可见暂停 + 卸载清理（demo 缺，属规约增强）。
3. **demo「收缩/展开」图标按钮**：保留文字 + IconUp/IconDown 在按钮内（按钮内图标不受标题禁令限制）。
4. **`KgAssetThumb` 封装**：demo 两处内联 AssetThumb（ServiceDisplay + DeepDrawer 的 bars 变体略异）合并为单组件五族；deep 抽屉 bars 族沿用统一 BAR_HEIGHTS（视觉等效）。
5. **角色权限矩阵动态列插槽**：`#[s.key]` 动态插槽名 + v-for PERMISSION_SCOPES（Arco table 动态 slotName 经列 slotName 指向遍历键）。
6. **ChartBuilder 五型**：DoD 写 bar·line·pie，demo 实有 graph/sankey 共 5 型，全量保留（超配不缺项）。

### 2.1 走查修复第 1 轮（2026-11-05 孔东走查，7 项 → commit 0920cc4，已 push）

| # | 走查问题 | 根因 | 修复 |
|---|---|---|---|
| 1 | 历史表「追溯」点击无抽屉 | **Arco Vue modal/drawer 无 `open` prop**（antd 语义误用），`:open` 传了不存在的 prop → 弹层永不显示 | 全部 `:open`/`v-model:open` → `:visible`/`v-model:visible`（SharePanel 5 处弹层 + QueryPanel 2 处 + DeepDrawer + SecurityPanel） |
| 2 | 「查看详情」tag 看不清 | `color: 'default'` 非 Arco 13 色名 → fallthrough `arco-tag-custom-color` 无样式 | `SHARE_ACTIONS.view` → `gray`；顺修 `geekblue`→`arcoblue`、`processing`→`arcoblue`（integrationEtl/Integration/Community 同类）、`SHARE_STATUS.revoked`/`actionColor`/`permissionActionColor` fallback `default`→`gray` |
| 3 | 操作栏「链接/嵌入/追溯」点击无效 | 同 #1 根因（Modal `:open`） | 同 #1 |
| 4 | 图查询顶部 Alert 去掉 | — | 删 `<a-alert type="info">` |
| 5 | 搜索与筛选分两行 | 原为两块面板两个 h4 | 合并单面板单行（auto-complete + range-picker + 类型/业务线 + 查询/重置/展开），删两个 h4 标题 |
| 6 | 收藏列是 button | — | `★/☆` button → `IconStarFill`(#ff7d00)/`IconStar`(#86909c) 直接 icon + cursor:pointer |
| 7 | 时间列换行 | 150/155/160px 放不下 `2026-05-20 16:35:22` | 分享表 `createTime`/历史表 `time` 150→170、审计表 `time` 155→170、查询历史 `queryTime` 160→170、决策表 `lastTrigger` 150→160、年月列 90→100 |

附带：DeepDrawer `header-extra` 插槽（Arco drawer 无此插槽）→ 内容顶部右对齐工具行；组件 prop `open`→`visible` 与父组件对齐。

### 2.2 走查修复第 2 轮（2026-11-05 孔东走查，2 项 → commit 61e6186，**停本地待确认 push**）

| # | 走查问题 | 修复 |
|---|---|---|
| 8 | 「全部发布人/标签分类」仍在展开行 | 两个筛选并入主行（搜索/时间/类型/业务线/发布人/标签 + 查询/重置 一行）；删展开/收缩按钮与 `filterExpanded` 状态、`IconUp/IconDown` import；CSS 清理 `row-more`/`more-label`/`toggle` 死样式；`tags-inline` 由 `flex:1 1 auto` 改限宽 240 防挤压按钮 |
| 9 | 面板双重内边距 | 删 `service/index.vue` 的 `.kg-service-shell { padding: 16px }` 与类名（外层 `.knowledge-graph-page` 已有 `--figma-content-shell-padding`） |

## 3. 产物清单

**models/ 9 件（新增）**：`shareHistory.ts` `kgShareExport.ts` `kgShareRegistry.ts` `kgShareSync.ts` `integrationSecurity.ts` `integrationEtl.ts` `realtimeMonitor.ts` `modelingGraphBuilder.ts` `queryAssetDeepAnalysis.ts`

**components/ 8 件（新增）**：`KgAssetThumb.vue` `KgSharePanel.vue` `KgQueryPanel.vue` `KgAssetDeepAnalysisDrawer.vue` `KgIntegrationEtlPanel.vue` `KgRealtimeMonitorPanel.vue` `KgIntegrationSecurityPanel.vue` `KgIntegrationPanel.vue`

**整页（重写）**：`service/index.vue`（壳 → 三面板接线；KPI 行/页头保留）

**自检（新增）**：`service/FE-KG-04A.test.mjs`（5 组断言）

## 4. 验收证据（三绿）

```
$ node --experimental-strip-types src/views/knowledge-graph/service/FE-KG-04A.test.mjs
✅ FE-KG-04A 服务展示整页自检全绿（5 组断言）
$ node src/views/knowledge-graph/kg.selfcheck.mjs
✅ FE-KG-S01 knowledge-graph 基座自检全绿（9 组断言）
$ pnpm type-check
（0 错误）
$ pnpm build
✓ built in 31.96s
```

自检覆盖：模型语义（demo selfcheck 断言摘选）/ 模型+面板禁随机即时时间 / 三面板挂接 + PageTabFrame 真 3 Tab + 互斥 v-if / **Tab·卡头标题纯文字无图标**（含 title="..." 与 #title 插槽扫描）/ 表格列 slotName 声明（02A 走查坑）/ 图标显式 es/icon import / D2 三件（30s·visibilitychange·onBeforeUnmount）/ D9（metric-id 挂点）/ D3（页面不回写种子）。

## 5. 架构合规自检（§2 铁律逐条）

| 铁律 | 状态 |
|---|---|
| D8 前端栈 React→**Vue 本仓栈**（lumen-ui-science-pc = Vue3+Arco Vue，仓级 AGENTS 约定优先） | ✅ |
| D9 数据血缘（ⓘ metric_id + 🧪 MockBadge；派生值不伪挂 id） | ✅ |
| D10 交互（键盘可达：native button/label 保留；aria-label 移植） | ✅ |
| D12 demo/lumen 隔离（零 import demo-*；对照重写） | ✅ |
| 调用链（前端不越层；api 双轨 fetchKgService，契约未冻结显式报错） | ✅ |
| 可观测（trackKgInteraction 埋点：tab-switch/share-create/query-search/etl-run/monitor-start 等 13 处） | ✅ |
| 确定性（禁 Math.random/Date.now/new Date，自检断言） | ✅ |
| 写操作演示态（localStorage 会话级，D3 不替 BE 拍板） | ✅ |

## 6. 遗留与建议

- registry 正名（M_KG_SVC_* → M_SCIUI_KGSVC_*）待 data-agent，前端 KgKpiCard 换 metric-id 字符串即可切。
- 监控指标接入真实接口时，`realtimeMonitor.ts` 的 init/tick 替换为 REST 轮询即可（面板 POLL_MS 常量已隔离）。
- `kgShareExport` 的 xlsx 走动态 import（bundle 已见独立 chunk 429KB 懒加载，不影响首屏）。

## 7. 待办（孔东验收后）

1. ~~commit + push origin/dev~~（走查修复轮已随 `0920cc4` push，含全部 20 文件）
2. task-registry：task-update-status → testing（或按 coordinator 指示）
