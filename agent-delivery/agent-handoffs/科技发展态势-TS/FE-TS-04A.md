# FE-TS-04A · 全球创新监测（M4）整页复刻 — 前端交付（待联调）

> 仓库：`repos/lumen-ui-science-pc`；路由 `/situation/global-innovation-monitor`（menu.ts 既有路由）。
> 状态：mock 数据环境人工点测通过，**进入联调**（BE-TS-CONTRACT 契约冻结后切 `USE_MOCK=false`）。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 五 Tab 数据一次取全（demo index.jsx 同语义），本地派生全走 models 纯函数；复用 M1 底座（TiandituMap/ChartCard/StatCard/InsightDetailDrawer/defineApi）；年份范围选择统一 Arco RangePicker(mode="year") 并沉淀为后续同类标准；未用 YAGNI 跳过 D9/可观测。 |

## 范围与实现（对照 DoD）

| DoD 项 | 实现 |
|---|---|
| 综合展示：成果类型芯片 + 底座地图落点 + 成果列表联动 | `tabs/InnovationDetail.vue`（类型芯片/地图框选/飞线/突出显示/订阅/推送/成果抽屉对比）+ `MapDetailModal.vue` + `IndustrySelect.vue` + `SearchableCascadeFilter.vue` + `SectionPanel.vue` |
| 实时数据：4 KPI + 趋势 + 领域分布，30s 轮询（可配、页面不可见暂停、卸载清理） | `tabs/InnovationRealtime.vue` + `models/realtimeModel.ts`（轮询状态机）+ `RealtimeKnowledgeGraph.vue`（图谱落图）+ `tech-trend-components.ts`（折线/柱状/热力三态趋势 + 饼/柱领域分布） |
| 载体排行：多维筛选 + 五年分详情下钻 | `tabs/InnovationRanking.vue` + `models/carrierRankingModel.ts`（多维分组 + 口径/权重）+ `RankingCard.vue` |
| 监测分析：预警 + 推送记录（已读/未读） | `tabs/InnovationMonitor.vue` + `models/detailMonitorModel.ts` + `MonitorRuleDrawer.vue`（模型/订阅/关注配置）+ `PushRecordDrawer.vue` + `RuleStatusBadge.vue` |
| 能力分析：10 城五维雷达 + 政策建议 | `tabs/CityInnovationAnalysis.vue` + `models/cityModel.ts`（四视图切换 + 雷达 + 报告导出） |
| Mock 种子冻结自 demo；D9 ⓘ/🧪；pnpm build 绿 | ✅ 全量见验收证据 |

### 类型契约（联调对接清单）

- `types/situation.ts`：`GlobalInnovationDataset`（五 Tab 共享全量数据集）+ InnovationItem/Carrier/City/Alert/PushRecord
- `api/situation/globalInnovation.ts`：`GET /situation/v1/innovation/dataset` → `GlobalInnovationDataset`（demo index.jsx 一次取全语义；真实接口若拆分多端点，仅改本层，页面/models 零改动）
- 契约冻结后切 `USE_MOCK=false` 即联调，无前端结构改动

## 验收证据

- `pnpm type-check`（vue-tsc --build，含 noUncheckedIndexedAccess）：0 error
- `pnpm build`：绿（32.8s）
- 人工点测（监管人 human:孔东，2026-10-14~15）：五 Tab 全交互通过，含本轮 8 项 UI 修正（见下）

## 本轮人工点测修正（用户反馈驱动）

1. 详情 Tab 排序无视觉变化：根因 = demo 种子 value 与 date 严格同序，`value-desc`/`date-desc` 输出全等。修 = mock `globalInnovation.ts` date 列错开（lumen 端唯一偏离项，注释标明；value/city/type/domain 与 demo 冻结一致）
2. 成果抽屉操作列按钮压缩变形：`flex-wrap: wrap` + 按钮 `flex-shrink: 0; white-space: nowrap`（宽度变小时换行但单按钮宽度保证）+ 列宽再分配（c1 25% / c6 25%）
3. 成果抽屉 body 去内边距（`padding: 0`）+ 隐藏滚动条保留滚动
4. 载体排行 Tab：移除「排名筛选功能」辅助标题占行；年份双 select 换 **Arco RangePicker(mode="year")**（230px/34px/13px，防 `[Date, undefined]` 半选 NaN 守卫）——**沉淀为后续年份范围选择统一标准**；排行列表容器可滚但隐藏滚动条；弹窗统一 20px 24px 内边距 + 内滚 + 固定关闭位
5. 监测分析 Tab：外层 `gi-content-inner--monitor` 双层内边距清零 + 去 `scrollbar-gutter: stable` 空白 + `.gi-btn--sm` 统一 32px 高对齐设计规范
6. 城市能力 Tab：移除「创新能力排名计算」辅助标题占行
7. mock 层类型修复：jitter 数组索引/location 元组/字典 fallback 的 noUncheckedIndexedAccess 50 处机械修（本轮类型门修复一部分，详见 FE-TS-02A handoff「类型门修复」节——两任务共仓共门）

## 偏离说明

- mock date 列为 lumen 端唯一偏离（使排序可视觉验证）；接入真实数据后自然消失
- 实时 Tab 轮询为演示扰动（giRealtimeStatus 标注「演示刷新非真源流」），真源流接口待契约
- `compare-components.ts`/`tech-trend-components.ts` 为 Tab 内聚组件工厂（demo 函数式组件语义复刻），非过度抽象

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 FE→Java→Python | ✅ api 层只写真实调用路径 |
| D12 不调 demo-* | ✅ USE_MOCK=false 零 mock 代码 |
| D8 Design token | ✅ demo 样式整块抽取（demo-global-innovation.css/demo-tech-trend.css）+ token 主题 + 本轮对齐规范（32px 控件高） |
| D9 血缘 | ✅ StatCard ⓘ 挂位 + 🧪 MockBadge；giRealtimeStatus 口径标注 |
| D10 交互规范 | ✅ 年份范围选 Arco RangePicker（本次沉淀标准）；弹窗/抽屉交互对齐 |
| 可观测 | ✅ X-Trace-Id/traceparent 全请求注入（M1 拦截器）+ 轮询生命周期埋点位 |
| 无新依赖 | ✅ 本任务零新增（@antv/g6/xlsx 为 FE-TS-02A 所加，本页未用） |

## CI/CD（必填）

- 分支：`dev`（工作区未提交，零 git 操作——等联调回归后随批提交）
- dev 测试：`pnpm dev` → `/situation/global-innovation-monitor`（USE_MOCK=true）

## 涉及文件

**新增**：`src/views/situation/global-innovation/`（index.vue + 12 组件 + 5 models + 2 styles）、`src/api/situation/globalInnovation.ts`、`src/mock/modules/globalInnovation.ts`
**修改**：`src/mock/register.ts`、`src/types/situation.ts`（M4 类型块 + 索引签名透传）、`src/router/menu.ts`、`src/config/echarts.ts`、`src/components/map/TiandituMap.vue`（M2/M4 共享改动）

## 遗留风险

- `vue-tsc --noEmit` 空跑问题（见 FE-TS-02A handoff），后续验证一律 `pnpm type-check`
- metric_id（TS-M4-*）为前端占位，D9 正式接入后替换
- 实时轮询 30s 为演示口径；真实推送/订阅接口（MonitorRuleDrawer/PushRecordDrawer 的写操作）待契约，当前会话级状态
