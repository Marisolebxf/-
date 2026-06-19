# UI-DS-25-trial · ui-agent Handoff
> ⚠️ **后续编辑注解（2026-06-18，v2 重组）**：本文产出时引用的 UI 规范为 `AI可复用UI框架与设计规范.md`，**2026-06-18 已全量重组为 `agent-delivery/Design.md`**（Figma 风格稿落地版，14 节）。本文档**保留原引用以示事实历史**；下游 agent 接力时请按下表换算：
>
> | 本文中的旧引用 | 现行 `Design.md` 引用 |
> |---|---|
> | `AI可复用UI框架与设计规范.md` | `Design.md` |
> | §3 产品定位 / §4 信息架构 | §1 设计定位 + §3 页面骨架（六骨架 + 三段工作区） |
> | §5 技术框架 / §10 Arco 接入 | §0 给 AI 的执行指令（强制 Arco React + 主色 `#165DFF`）+ §13 推荐实现映射 |
> | §7 设计 Token | §4 色彩 + §5 字体 + §6 圆角描边阴影 + §13 主题 token |
> | §7.3 `.content-shell-glass` | §3.1 `.content-shell`（**取消毛玻璃强效果**） |
> | §7.3 / §7.4 图表分类色 chart-01~20 | §4.3 图表序列优先顺序（直接色值） |
> | §7.3.3 / §7.4.3 11 类业务对象 | §4.3 科技要素与图表色（**10 类，"资讯" 已取消**） |
> | §9 17 个通用组件（PageShell / GlobalWorkbenchTabs 等） | §7 通用组件 8 + §8 工作区 3（Figma 风格 class：`app-shell` / `content-shell` / `workspace-grid` / `layer-panel` / `map-stage` / `analysis-panel`） |
> | §9.3 / §9.4 Tab 分级 | §7.3 Tabs（**分级取消**） |
> | §18 验收 18 条 | §14 检查 8 + 验收 6 = 14 条（含截图取样定量验收） |
>
> 详见 `agent-delivery/architecture-baseline.md §8` v2.0 变更记录。

## 执行信息

| 项 | 值 |
|---|---|
| 任务 | DS-25 软科学成果展示沙箱页（ui-agent Step 2） |
| 执行时间 | 2026-06-17 23:37 – 2026-06-18 00:30（约 53 min） |
| 仓 | demo2（main 直推） |
| commit | `185ca15` |
| 改动文件数 | 38 |
| 新增行数 | 3,619 |
| push 状态 | ✅ `up to date with 'origin/main'` |

## 完成清单对照 DoD（37 项）

### 工程自检 10 条

| # | 项目 | 状态 |
|---|------|------|
| 1 | 路由 `/sandbox/soft-science-2026-06-17/*` 8 个页面均可访问 | ✅ |
| 2 | 覆盖 wireframe 全部 8 页（P0 完整 + P1 完整） | ✅ |
| 3 | 主菜单未变化（`src/data.js` 零改动） | ✅ |
| 4 | `package.json` / `vite.config.js` / `.gitignore` 零改动 | ✅ |
| 5 | Mock 数据字段名沿用 ODS + 含 `_mock_meta` | ✅ |
| 6 | 响应式 1280/1440/1920 三档不破版 | ✅（基本适配） |
| 7 | 关键交互节点埋点 `console.log('ss.xxx.event')` | ✅ |
| 8 | `npm run dev` 启动无错误 | ✅ |
| 9 | `npm run build` 构建通过 | ✅ |
| 10 | D9 三件套：MetricSpecCard + DataLineageDrawer + MockBadge 均实现 | ✅ |

### 设计规范合规自检 18+1 条

| # | 规范条目 | 状态 | 备注 |
|---|---------|------|------|
| 1 | 产品定位：分析工作台 + 汇报级驾驶舱 | ✅ | 浅色蓝灰风格，非深色霓虹 |
| 2 | 信息架构 7 段骨架 | ✅ | ContextBar→ModuleHeader→MetricCard→FilterBar→主可视化→右侧→表格 |
| 3 | §4.2 5 段优先级 | ✅ | 每页回答 5 段 |
| 4 | 技术栈 React+Vite+ECharts+Leaflet+dayjs | ✅ | |
| 5 | **Arco Design 优先** | ⚠️ | **阻塞：Arco 未安装 demo2，本沙箱用 AntD 5；等 PM 决策** |
| 6 | token 不硬编码 | ✅ | 用 `TOKENS` 常量 |
| 7 | 上升红下降绿持平灰 | ✅ | `TOKENS.rise/fall/neutral` |
| 8 | 11 类业务对象固定配色 | ✅ | 课题=chart-09 |
| 9 | 图表分类色 chart-01~20 序列 | ✅ | |
| 10 | Tag 浅底深字 | ✅ | |
| 11 | 卡片 8px 圆角 | ✅ | |
| 12 | 浅色蓝灰风格 | ✅ | |
| 13 | §9 通用组件命名 | ✅ | MetricCard/SectionPanel/DetailDrawer/EvidenceList 等 |
| 14 | 复杂筛选 4 项 | ✅ | 搜索/重置/确认/已选摘要 |
| 15 | 文案克制 | ✅ | 无空泛词 |
| 16 | 响应式 1440 优先 | ✅ | |
| 17 | 可访问性 WCAG AA | ✅ | 语义化标签+键盘可达 |
| 18 | commit 前 §18 逐条勾选 | ✅ | |
| 19 | D9 每个统计数字可追溯 | ✅ | ⓘ + 🧪 |

### ⚠️ 角标 5 处

| # | 位置 | 决策项 | 实现状态 |
|---|------|--------|---------|
| 1 | P-02/P-03/P-04 学科字段 | Q001 | ✅ WarningOutlined + Tooltip |
| 2 | P-02 市/区级按钮 | Q003 | ✅ disabled + ⚠️ icon |
| 3 | P-04 时间轴 + P-08 阶段名 | Q004 | ✅ ⚠️ icon + Tag |
| 4 | P-06 整页 | Q005 | ✅ 顶部固定 StatusTag（不可关闭） |
| 5 | P-08 超期阈值 | K-O7 | ✅ ⚠️ icon + 阈值说明 |

### git 纪律

| # | 项目 | 状态 |
|---|------|------|
| 1 | git push 到 origin/main | ✅ `185ca15` |
| 2 | `up to date with 'origin/main'` | ✅ |
| 3 | commit message 含 `[agent:ui-agent]` | ✅ |
| 4 | 远端可访问（push 后 2-3 min） | ✅ |

## 产物绝对路径

### 页面组件（8 页 + 3 共用 + 1 数据 + 1 README）

- `src/pages/sandbox/soft-science-2026-06-17/index.jsx` (P-01)
- `src/pages/sandbox/soft-science-2026-06-17/map.jsx` (P-02)
- `src/pages/sandbox/soft-science-2026-06-17/list.jsx` (P-03)
- `src/pages/sandbox/soft-science-2026-06-17/detail.jsx` (P-04)
- `src/pages/sandbox/soft-science-2026-06-17/stats.jsx` (P-05)
- `src/pages/sandbox/soft-science-2026-06-17/feedback.jsx` (P-06)
- `src/pages/sandbox/soft-science-2026-06-17/export.jsx` (P-07)
- `src/pages/sandbox/soft-science-2026-06-17/progress.jsx` (P-08)
- `src/pages/sandbox/soft-science-2026-06-17/_layout.jsx`
- `src/pages/sandbox/soft-science-2026-06-17/_router.jsx`
- `src/pages/sandbox/soft-science-2026-06-17/data.js`
- `src/pages/sandbox/soft-science-2026-06-17/README.md`

### D9 三件套

- `src/pages/sandbox/soft-science-2026-06-17/components/MetricSpecCard.jsx`
- `src/pages/sandbox/soft-science-2026-06-17/components/MockBadge.jsx`
- `src/pages/sandbox/soft-science-2026-06-17/components/DataLineageDrawer.jsx`

### Mock 数据

- `src/mocks/sandbox/soft-science-2026-06-17/metrics-catalog.json` (26+ metric_id 8 件套)
- `src/mocks/sandbox/soft-science-2026-06-17/overview.json`
- `src/mocks/sandbox/soft-science-2026-06-17/projects/list.json` (40 条课题)
- `src/mocks/sandbox/soft-science-2026-06-17/projects/ZH-2024-SS-0001.json`
- `src/mocks/sandbox/soft-science-2026-06-17/projects/ZH-2024-SS-0001/output.json`
- `src/mocks/sandbox/soft-science-2026-06-17/projects/ZH-2024-SS-0001/timeline.json`
- `src/mocks/sandbox/soft-science-2026-06-17/projects/ZH-2024-SS-0001/feedback.json`
- `src/mocks/sandbox/soft-science-2026-06-17/map/density_by_prov.json`
- `src/mocks/sandbox/soft-science-2026-06-17/map/topn_institutions.json`
- `src/mocks/sandbox/soft-science-2026-06-17/map/trend.json`
- `src/mocks/sandbox/soft-science-2026-06-17/stats/yearly.json`
- `src/mocks/sandbox/soft-science-2026-06-17/stats/category.json`
- `src/mocks/sandbox/soft-science-2026-06-17/stats/unit_contribution.json`
- `src/mocks/sandbox/soft-science-2026-06-17/stats/hot_keywords.json`
- `src/mocks/sandbox/soft-science-2026-06-17/stats/domain_distribution.json`
- `src/mocks/sandbox/soft-science-2026-06-17/progress/kpi.json`
- `src/mocks/sandbox/soft-science-2026-06-17/progress/overdue.json`
- `src/mocks/sandbox/soft-science-2026-06-17/progress/lineage.json`
- `src/mocks/sandbox/soft-science-2026-06-17/export/history.json`

### 桥接修改

- `src/pages/sandbox/SandboxRouter.jsx`（+2 行 import + else if 分支）
- `src/pages/sandbox/index.jsx`（+1 条 TRIAL 卡片）
- `src/pages/sandbox/sandbox.css`（+260 行 DS-25 专用样式）

## 体量统计

| 项 | 值 |
|---|---|
| jsx 文件行数 | ~2,300 行 |
| mock JSON 体量 | ~900 行 |
| CSS 新增 | ~260 行 |
| 总新增字符 | ~90,000 |

## 范围与实现

| 项 | 值 |
|---|---|
| scope_ref | bid §1.1.1.1.4.6.1 软科学成果展示 7 个三级子功能 |
| implementation_as_built | 8 页完整实现，P-06 为 Wave 0 占位 UI |
| data_gaps | P-06 互动传播全部 ❌ 用户态；P-05 词云/树图/案例推荐 🔧 待 algorithm |
| variance_note | **Arco Design 未安装**，用 AntD 5 替代；等 PM 决策 |

## ⚠️ 阻塞项

**Arco Design 未安装在 demo2 的 `package.json` 中**。按 D8 决策新页面必须用 Arco，但硬约束禁装新依赖。本沙箱暂时用 AntD 5 实现，与 DS-15 同组件库。PM 需决策：

1. 安装 Arco Design 到 demo2（打破"禁装新依赖"约束）
2. 保持 AntD（demo2 作为历史兼容仓，Arco 仅在 lumen 正式仓使用）

## 已知限制

1. P-02 地图：未沿用 `SharedRegionMap.jsx`（基于 AntD 不可直接用），重新用 react-leaflet 实现
2. P-03 搜索：NLP 智能搜索降级为 SQL LIKE，无自动建议
3. P-05 词云：用 Tag 代替 ECharts wordCloud（未安装 wordCloud 扩展）
4. P-05 树图：用 CSS grid 代替 ECharts treemap
5. P-04 典型案例：文本相似度算法待 algorithm-agent
6. P-06 全页为 Wave 0 占位，所有操作按钮 toast 提示"Wave 2 后开放"
7. 数据血缘 DataLineageDrawer 用静态 Steps 占位，未接 G6/mermaid

## 给 PM + UI/UE 评审的"重点看 3 项"

1. **D9 三件套实战效果**：在 P-01 / P-02 / P-05 点击 ⓘ 和 🧪，评估 MetricSpecCard + MockBadge 在汇报场景下的数据可信度提升
2. **P-04 时间轴 ⚠️ Q004**：4 阶段语义（立项/执行/结题/转化）是否合理，需甲方确认
3. **P-06 Wave 0 占位 + P-08 预警阈值 ⚠️ K-O7**：占位 UI 是否满足甲方评审需求；14d 黄 / 30d 红阈值

## 给 frontend-agent 后续 lumen 复刻的提示

1. **3 个 D9 组件可提级到 `src/components/`**：MetricSpecCard / MockBadge / DataLineageDrawer 是跨 DS 通用组件，lumen 应放在共享组件目录
2. **Mock JSON 字段名对齐 ODS**：切真实数据时前端代码零改动（仅改 API URL）
3. **Arco 替换**：lumen 正式仓应按 D8 用 Arco Design，AntD 组件需逐个替换
4. **路由改造**：lumen 用 React Router（非 hash 路由），`_router.jsx` 需改写
5. **API 接入**：mock JSON → Java REST (`gkxlumen-metrics` / `gkxlumen-topic`)

## 成本回填

| 项 | 值 |
|---|---|
| estimated_tokens | 200k |
| actual_tokens | ~180k |
| model_used | glm-5.1 |
| actual_cost | ~$3 |
| cost_warn | green |

## 试点反馈

### 1. 耗时实测

| 步骤 | 计划 | 实际 | 超时原因 |
|------|------|------|---------|
| 必读文件 | 6 min | 8 min | 文件量大，wireframe 920 行 |
| P0 4 页面 | 25 min | 30 min | map.jsx Leaflet 集成较复杂 |
| P1 4 页面 | 15 min | 12 min | feedback 为占位页，较快 |
| 路由+构建+push | 5 min | 15 min | 路径计算反复修正 3 轮 |
| handoff | 5 min | 8 min | |
| **合计** | **45 min** | **53 min** | |

### 2. 必读文件评价

| 用处大 | 用处小/冗余 |
|--------|------------|
| DS-25-wireframe.md（核心） | 客户决策清单跟踪表（5 项已在 wireframe 标注） |
| DS-25-IA.md（路由+组件映射） | repo-registry.yaml（demo2 规则已知） |
| data-lineage-policy.md（D9 三组件规范） | budget-estimate.md（与 UI 无关） |
| data/DS-25-data-availability-matrix.md（ODS 字段） | |
| AI可复用UI框架与设计规范.md（D8 §7 token） | |

### 3. 派单话术评价

**清晰可直接执行**：
- 8 页面清单 + 路由 + 优先级 + 降级策略
- D9 三组件规范 + 5 处 ⚠️ 角标位置
- Mock 数据要求（字段名 / 空值率 / 批次标识）
- git 纪律 + commit 模板

**有歧义需澄清**：
- "用 Arco Design"与"禁装新依赖"矛盾——未给出 fallback 策略
- "沿用 SharedRegionMap.jsx"但该组件基于 AntD，用 Arco 须重写——未说明
- "40 条课题"与"list.json 30-50 条"范围不一致

### 4. UX 产物可用性

**最有用的 3 项**：
1. wireframe 每页 metric_id 清单 → 直接映射到 MetricSpecCard
2. IA 路由建议 + §9 组件映射 → 零设计决策直接实现
3. data availability matrix ODS 字段映射 → mock 数据字段名对齐

**不够用的 1-2 项**：
1. 地图页缺少具体 GeoJSON 坐标数据，只有省名，需自行补省会坐标
2. P-06 占位页 wireframe 过于详细（3 个 Section），实际只需 1 个 StatusTag + 4 DataCard

### 5. D8/D9 规范实战落地

**最容易落地的 3 条**：
1. 8px 圆角 + 浅色蓝灰风格 → AntD Card + CSS 直接实现
2. 上升红下降绿持平灰 → 3 个 token 常量搞定
3. D9 MetricSpecCard → AntD Popover + Descriptions 一次写完

**最难落地的 3 条**：
1. Arco Design 强制 → 仓中未安装，与"禁装新依赖"硬冲突
2. 11 类业务对象固定配色 → 需跨页面统一维护 token 映射表，容易遗漏
3. §9 通用组件 15 个全部覆盖 → 工作量巨大，部分组件（GraphCanvas / MapPanel）需要深层封装

**Arco Design 覆盖率**：0%（因未安装，全部用 AntD 5 替代）

**D9 三组件工作量**：单个组件约 15-20 min；扩到 7 要素全页面约 2-3 小时/页面

### 6. 与 DS-15 沙箱页（pre-D8）对比

| 维度 | DS-15 (AntD+Tailwind) | DS-25 (AntD+D8 Token) |
|------|----------------------|----------------------|
| 视觉气质 | 深色渐变 hero card + 鲜艳 Tag | 浅色蓝灰 + chart-09 绿主色调 |
| 数据可信度 | 无 metric_id / 无 ⓘ / 无 🧪 | 26+ metric_id + ⓘ + 🧪 + DataLineageDrawer |
| 代码可读性 | 组件口语化（TrialHome/TrialLayout） | §9 命名（MetricCard/SectionPanel/EvidenceList） |
| 汇报场景 | 数字"裸奔"，甲方问来源无据可查 | ⓘ 一键展开 8 件套元数据 |

### 7. 给 PM 的 3 条改进建议

1. **派单前先检查依赖**：在派单话术中加入"依赖检查清单"步骤，如 Arco 未安装则自动降级方案
2. **wireframe 给出坐标数据**：地图页应附带省会 GeoJSON 坐标或至少一个 reference 数据源
3. **D9 三组件模板化**：将 MetricSpecCard / MockBadge / DataLineageDrawer 作为项目级脚手架，派单时直接"复制到沙箱 components/"，而非每次重写