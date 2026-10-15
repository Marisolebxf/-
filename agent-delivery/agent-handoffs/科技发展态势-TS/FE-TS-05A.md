# FE-TS-05A · 湾区创新监测（M5）整页复刻 — 前端交付（待联调）

> 仓库：`repos/lumen-ui-science-pc`；路由 `/trend/bay-area-innovation-monitor`（menu.ts 注册，fullBleed 布局）。
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
| 说明 | 全量数据集一次取全（demo useState 语义），本地派生全走 models 纯函数；复用底座（TiandituMap/SearchableCascadeFilter/SectionPanel/InsightDetailDrawer/defineApi/M1 拦截器）；四 Tab 组件与 demo 文件一一对应；未用 YAGNI 跳过 D9/可观测。 |

## 范围与实现（对照 DoD）

| DoD 项 | 实现 |
|---|---|
| 成果地图：11 城 67 点落点 + 城市/类型/领域/时间筛选联动 | `tabs/OverviewTab.vue`（城市多选/成果分类/产业级联/时间范围四行筛选 + 底座地图落点 + 热点城市卡 + 价值分成果列表联动 + 地理落点弹层） |
| 创新能力：四维指数 + 计算方法说明 + 2020–2025 趋势 + 城市雷达 | `tabs/CapacityTab.vue`（SVG 四维能量环 + 11 城排名条形图 + Top4 趋势线 + 11 城明细表内联雷达）+ `components/CalcMethodModal.vue`（capacity-ranking / indicator 双视图维度拆解 + 公式） |
| SWOT：四象限全文 + 因素，默认展开短板维 + 诊断 | `tabs/SwotAnalysisTab.vue`（雷达 + 因素泳道矩阵 + S/W/O/T 象限卡 + 焦点因子视图 + CSV 导出）+ `components/DiagnosisReportModal.vue`（PDF 打印 / Word .doc / CSV 三导出） |
| 指标数据：6 指标 + 11 城构成 + 口径说明对比 | `tabs/IndicatorsTab.vue`（GIS 比例圆地图 + 指标卡（常用星标/展示开关/口径ⓘ）+ 对比趋势/柱状图 + 右侧证据面板 + 全城市明细抽屉 + CSV 导出） |
| 预警中心（demo 配套） | `components/AlertCenterDrawer.vue`（规则配置滑杆 + 通知记录双 Tab，定位地图/标为已读/全部已读） |
| Mock 种子冻结自 demo；D9 ⓘ/🧪；pnpm build 绿 | ✅ 全量见验收证据 |

### 类型契约（联调对接清单）

- `types/bayArea.ts`：`BayAreaInnovationDataset`（四 Tab + 预警中心共享全量数据集）+ City/Indicator/SwotFactor/AlertRecord
- `api/situation/bayAreaInnovation.ts`：`GET /situation/v1/bay-area/innovation/dataset` → `BayAreaInnovationDataset`（一次取全；真实接口若拆分多端点，仅改本层，页面/models 零改动）
- 契约冻结后切 `USE_MOCK=false` 即联调，无前端结构改动

## 验收证据

- `pnpm type-check`（vue-tsc --build，含 noUncheckedIndexedAccess）：**0 error**
- `pnpm build`：**绿（33.6s，2026-10-15）**
- 人工点测（监管人 human:孔东，2026-10-15，dev server :3000 `/trend/bay-area-innovation-monitor`）：
  - 四 Tab 全交互通过：成果地图（筛选联动/地图落点/热点卡/成果列表）、创新能力（能量环/排名/趋势/明细）、SWOT（象限/因素/诊断报告导出）、指标数据（指标卡/GIS 圆/对比图/明细抽屉/导出）
  - 预警中心抽屉：规则配置 + 通知记录（2 条）+ 定位/已读操作
  - 本轮 UI 修正：筛选栏成果分类多选标签溢出两行（58px）→ **单行 36px + `+2...` 折叠**（`:max-tag-count="4"` + CSS 单行 clamp），城市范围同理 `+9...`

## 偏离说明

- 无结构性偏离。demo 的 React 版 Hook 派生逻辑在 `models/bayAreaModel.ts` 以纯函数复刻（维度定义/能量环/排名/雷达/ SWOT 分组/指标筛选派生）
- mock 种子冻结自 demo `bayAreaInnovation` 模块；`emptyProvenance` fallback 为类型合规新增，不影响数据

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 FE→Java→Python | ✅ api 层只写真实调用路径（/situation/v1/bay-area/innovation/dataset） |
| D12 不调 demo-* | ✅ USE_MOCK=false 零 mock 代码 |
| D8 Design token | ✅ demo 样式整块抽取（demo-bay-innovation.css）+ token 主题 + 32px 控件高 |
| D9 血缘 | ✅ 指标卡口径 ⓘ 挂位 + 🧪 MockBadge（Mock 态）+ 证据面板数据来源说明 |
| D10 交互规范 | ✅ 筛选/弹窗/抽屉/导出交互对齐；多选筛选标签超限折叠为 +n（Arco 标准行为） |
| 可观测 | ✅ X-Trace-Id/traceparent 全请求注入（M1 拦截器复用） |
| 无新依赖 | ✅ 本任务零新增 npm 包 |

## CI/CD（必填）

- 分支：`dev`（已与 FE-TS-03A 同批提交 `origin/dev`）
- dev 测试：`pnpm dev` → `/trend/bay-area-innovation-monitor`（USE_MOCK=true）

## 涉及文件

**新增**：`src/views/situation/bay-innovation/`（index.vue + 3 components + 1 model + 1 style + 4 tabs）、`src/api/situation/bayAreaInnovation.ts`、`src/mock/modules/bayAreaInnovation.ts`、`src/types/bayArea.ts`
**修改**：`src/mock/register.ts`、`src/router/menu.ts`、`src/config/echarts.ts`、`src/components/drawer/InsightDetailDrawer.vue`、`src/components/drawer/detailModel.ts`

## 遗留风险

- metric_id（TS-M5-*）为前端占位，D9 正式接入后替换
- 预警中心规则/已读写操作为会话级状态，真实接口待契约
- 同仓并行任务（tracking 模块）曾短暂拉低 type-check，17:25 前已由并行会话修复；本任务构建验证在其后完成（build 绿）
