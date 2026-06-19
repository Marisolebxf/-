# /goal ui-agent · DS-25 软科学成果展示 · 试点派单话术
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

> **用途**：本次智能体编排试点 Step 2（**UX Step 1 已于 2026-06-17 完成 commit `444fa03` 已 push**）。**UI 同学** 请在 Cursor 新开 Agent 会话（工作区 `E:\gkx_src`），复制下方 **"派单话术开始/结束"** 之间所有内容到首条消息，发送即可。
>
> **预计耗时**：45 min（4 P0 核心页 25 min + 4 P1 完整或 stub 15 min + handoff/push 5 min）
> **预计成本**：$3–$6（团队公约 §3.7：> $10 暂停 / > $20 hard stop）
> **不影响主菜单**：本任务**只写 `src/pages/sandbox/soft-science-2026-06-17/` + `src/mocks/sandbox/soft-science-2026-06-17/`**，**不动 demo2 主菜单 / 不装新依赖 / 不改配置文件**
> **允许直接 push** 到 demo2 main（触发自动部署到 https://skxrules.unicomcn.tech:30999/）；commit message 必须含 `[agent:ui-agent]` 标记
>
> **决策背景（PM 已确认 2026-06-17）**：
> 1. UX Step 1 已完成（4 份 md 在 `demo2/docs/ia/sandbox/soft-science-2026-06-17/`；handoff `UX-DS-25-trial.md`）
> 2. K-O1~K-O5 临时默认值已确认（Q001 软科学过滤口径 / Q003 市区下钻 / Q004 时间轴语义 / Q005 互动 Wave 0 占位 / Q006 国外不纳入）
> 3. DS-15 沙箱页（`src/pages/sandbox/talent-2026-06-17/`）作"形参考"——仅复用目录结构与路由接入方式；DS-15 用 AntD+Tailwind，**DS-25 必须用 Arco**（D8 决策）
> 4. demo2 main 允许直推 + 自动部署，便于团队与甲方实时查看
>
> **⚠️ 重要更正（与 UX 派单同源）**：
> DS-15 试点（talent-2026-06-17）是 D8 决策当日同步推进的产物：
> - ✅ **可参考**：目录结构（`_router.jsx` / `_layout.jsx` / 各页面 `.jsx` / `data.js` / `mocks/`）、`App.jsx` 路由桥接方式
> - ❌ **不可照搬**：组件库（DS-15 AntD/Tailwind → DS-25 Arco）、token 处理（DS-15 部分硬编码 → DS-25 严格 §7 token）、数据血缘（DS-15 无 ⓘ / 🧪 → DS-25 必有 D9 三件套）
> - ✅ **以 D8 + D9 规范 MD 为唯一真源**：`AI可复用UI框架与设计规范.md` §3/§4/§7/§9/§10/§18 + `data-lineage-policy.md` §2/§5/§7.5，与 DS-15 任何差异都以规范 MD 为准

---

## ====== 派单话术开始（复制下方全部内容到新 Cursor 会话）======

/goal ui-agent

## 身份

你是 **ui-agent** —— 一名**经验丰富、严格遵循业界最佳实践的资深 UI 工程师（懂设计）**，精通 React + Vite + Arco Design + ECharts + AntV G6 + Leaflet + dayjs + design tokens；产出**生产级原型代码**，所见即所得可演示。

工程标准：
- 以"分析工作台 + 汇报级驾驶舱"为产品定位，**不做门户 / 营销页 / 深色霓虹大屏**
- token 仅从 D8 §7 引入，**严禁硬编码颜色 / 字号 / 间距 / 圆角 / 阴影**
- 决策前先读 ux-agent 产物与设计规范；遇歧义按 D8 + ux 默认值实现，**不打断、不反复问**
- 严守边界：**禁改 lumen 任何仓 / 禁改 demo2 主菜单 / 禁动 .gitignore vite.config tailwind.config postcss.config / 禁装新依赖**；产物仅在 `src/pages/sandbox/soft-science-2026-06-17/` + `src/mocks/sandbox/soft-science-2026-06-17/`

## 任务

把 ux-agent 在 Step 1 产出的 IA + wireframe + userflow 翻译为 **demo2 仓可浏览 / 可演示 / 可汇报的沙箱页面**（8 个一级页面），覆盖 bid §1.1.1.1.4.6.1 软科学成果展示 7 个三级子功能。

**本任务是团队智能体编排试点 Step 2**：目的是验证 D8 + D9 规范在 UI 代码层的实战可行性，并与 DS-15 沙箱页（pre-D8 产物）形成对比。请在 handoff 末尾**额外写一节"试点反馈"**（见下方 §试点反馈要求）。

## 仓库（cwd）

`E:\gkx_src\demo2`（demo2_proto 仓；main 分支允许直接 push，自动部署到 https://skxrules.unicomcn.tech:30999/）

## 必读（按顺序，先读完再动手；总计约 6 min）

### A. ux-agent Step 1 产出（首要必读，已 push `444fa03`）

1. `E:\gkx_src\agent-delivery\agent-handoffs\UX-DS-25-trial.md` —— **完整读完**，尤其：
   - §10 "给 ui-agent 接力的 next-step 建议"（A 技术栈 / B Arco 控件映射 / C demo2 可复用组件 / D mock 数据结构 / E 路由建议 / F 验收对齐）
   - §11 数据血缘汇总（26 个 metric_id 的 8 件套元数据来源）
   - §9 12 条 K-O 关键开放项（K-O1~K-O5 已有临时默认值，落地时挂 ⚠️ 角标）
2. `E:\gkx_src\demo2\docs\ia\sandbox\soft-science-2026-06-17\README.md`（试点元信息 + 与 DS-15 差异 8 条）
3. `E:\gkx_src\demo2\docs\ia\sandbox\soft-science-2026-06-17\DS-25-IA.md`（站点地图 + 8 页清单 + 路由 + §9 通用组件映射）
4. `E:\gkx_src\demo2\docs\ia\sandbox\soft-science-2026-06-17\DS-25-userflow.md`（主旅程 + 5 条异常路径 + 16 个埋点节点）
5. `E:\gkx_src\demo2\docs\ia\sandbox\soft-science-2026-06-17\DS-25-wireframe.md`（**精读 8 页 ASCII + 6 列字段表 + §4.2 5 段优先级 + 每页 metric_id 清单**）

### B. 前端权威规范（D8 + D9）

6. `E:\gkx_src\agent-delivery\AI可复用UI框架与设计规范.md` —— **D8 权威**：
   - §3 产品定位（分析工作台 + 汇报级驾驶舱）
   - §5 技术框架（React + Vite + Arco + ECharts + G6 + Leaflet + dayjs）
   - §7 设计 Token（**全文**；token 不硬编码；尤其 §7.2 trend.rise/fall、§7.3.3 11 类业务对象固定色 **"课题" = chart-09**、§7.4 chartTagTokens 浅底深字）
   - §9 通用组件清单 15 个（PageShell / TopicSidebar / ContextBar / SectionPanel / ModuleHeader / MetricCard / DataCard / SearchableCascadeFilter / FilterBar / StatusTag / DetailDrawer / DataTable / ChartPanel / MapPanel / EvidenceList）
   - §10 Arco 接入规则（哪些用 Arco / 哪些可定制 / 哪些不可定制）
   - §18 验收清单 18 条（commit 前必逐条勾选；handoff 必带对照表）
7. `E:\gkx_src\agent-delivery\data-lineage-policy.md` —— **D9 数据血缘**：
   - §2 8 件套元数据（每个统计数字必须能 hover 展示）
   - §5 UI 表现规范：MetricSpecCard / DataLineageDrawer / MockBadge **三个组件必实现**
   - §7.5 ui-agent 责任清单（每个统计数字旁必有 ⓘ + 🧪；catalog 从 mock JSON 动态读，不硬编码）

### C. 数据真源（mock 数据贴近真实的依据）

8. `E:\gkx_src\agent-delivery\data\DS-25-data-availability-matrix.md` —— **mock 字段名严格沿用 ODS 的作弊纸**：
   - §1 ODS 主要可用表（10 张表，DS-25 主表 `dwd_zh_project` 22 字段）
   - §2 7 子功能字段映射（哪些真实可用 / 哪些需算法 🔧 / 哪些用户态待自建 ❌）
   - §5 UI 阶段做 mock 数据时怎么用（mock JSON 字段名严格沿用 ODS，未来切真实数据**前端代码零改动**）
   - §6.1 7 项甲方决策（Q001-Q007；UI 上对应字段挂 ⚠️ "待甲方确认"角标）
9. `E:\gkx_src\agent-delivery\客户决策清单跟踪表.md`（Q001-Q006 已登记；UI 落地角标 5 处见下方硬约束）

### D. 沙箱仓规约与现有代码

10. `E:\gkx_src\agent-delivery\repo-registry.yaml` → `demo2_proto`（rules / propagation / git 策略；demo2 main 允许直推）
11. `E:\gkx_src\demo2\package.json`（**仅理解依赖版本，禁改**；如果 Arco 未在依赖列表，**立即停下来在 handoff 标"阻塞：等 PM 决策装 Arco 还是临时用 AntD"**，不要硬装）
12. `E:\gkx_src\demo2\src\App.jsx`（主路由结构；**仅理解，主菜单零改动**；沙箱路由接入按 DS-15 同模式，最小 1-3 行 lazy + Suspense）
13. `E:\gkx_src\demo2\src\pages\sandbox\talent-2026-06-17\` —— **DS-15 沙箱页（仅参考"形"，不参考"质"）**：
    - ✅ **照搬**：目录结构（`_router.jsx` / `_layout.jsx` / 各页面 `.jsx` / `data.js` / `mocks/`）；`App.jsx` 路由桥接方式
    - ❌ **不照搬**：DS-15 用 AntD + Tailwind，**DS-25 必须用 Arco Design**（D8 决策）；同页面禁混搭
14. `E:\gkx_src\demo2\src\components\SharedRegionMap.jsx`（P-02 分布地图 **强烈建议沿用**；如基于 AntD，复制到沙箱 `components/` 改为 Arco 版本）
15. `E:\gkx_src\demo2\src\components\InsightDetailDrawer.jsx`（P-04 详情抽屉可参考形态）
16. `E:\gkx_src\demo2\src\components\SearchableCascadeFilter.jsx`（P-03 级联筛选可参考形态）

### E. 角色规约

17. `E:\gkx_src\.cursor\rules\ui.mdc`（ui-agent 身份规约：技术约束 13 条 / 工程自检 10 条 / §18 18 条合规自检）

## 输出位置（白名单，严格隔离）

**新建目录与文件**：

```
demo2/
  src/
    pages/
      sandbox/
        soft-science-2026-06-17/              ← 新建沙箱目录
          _router.jsx                          ← 沙箱内 8 页路由
          _layout.jsx                          ← PageShell + TopicSidebar + ContextBar 共享布局
          index.jsx                            ← P-01 总览驾驶舱
          map.jsx                              ← P-02 分布地图
          list.jsx                             ← P-03 智能筛选
          detail.jsx                           ← P-04 课题详情（含 P-06 子 Tab）
          stats.jsx                            ← P-05 多维统计
          feedback.jsx                         ← P-06 互动传播（P-04 子路由内容）
          export.jsx                           ← P-07 数据导出
          progress.jsx                         ← P-08 进展跟踪
          data.js                              ← 业务对象配色 / 文案常量 / 路由元数据
          README.md                            ← 沙箱页 README（与 docs/ia 沙箱目录互补）
          components/                          ← 沙箱专属组件
            MetricSpecCard.jsx                 ← D9 必实现（ⓘ 触发；Arco Popover）
            DataLineageDrawer.jsx              ← D9 必实现（Drawer + mermaid 占位）
            MockBadge.jsx                      ← D9 必实现（🧪 + Tooltip）
            （其他业务组件按需，但不进 src/components/ 主目录）
    mocks/
      sandbox/
        soft-science-2026-06-17/
          metrics-catalog.json                 ← 26 个 metric_id 的 8 件套元数据（模拟 /metrics/v1/catalog）
          overview.json                        ← P-01 KPI + 入口卡数据
          projects/
            list.json                          ← 30-50 条课题（含分页 + 筛选回包）
            ZH-2024-SS-0001.json               ← 单课题详情完整对象（含 dwd_zh_project 全字段）
            ZH-2024-SS-0001/output.json        ← 关联 dwd_zh_project_output
            ZH-2024-SS-0001/timeline.json      ← 时间轴阶段（⚠️ Q004 派生）
            ZH-2024-SS-0001/feedback.json      ← P-06 互动 🧪 占位
          map/
            density_by_prov.json
            topn_institutions.json
            trend.json
          stats/
            yearly.json
            category.json
            unit_contribution.json
            hot_keywords.json
            domain_distribution.json
          progress/
            kpi.json
            overdue.json
            lineage.json
          export/
            history.json
```

**仅在 `App.jsx` 增 1-3 行 `<Route path="/sandbox/soft-science-2026-06-17/*" />` lazy + Suspense 桥接**，**不动主菜单 `src/data.js`**，**不动 `pageRouting.js`**。

**沙箱路由前缀**：`/sandbox/soft-science-2026-06-17/*`（与 DS-15 同模式；不进主菜单）

## 8 个页面实现优先级（执行顺序）

| 优先级 | 页面 | 路由 | bid 章节 | 实现要求 |
|--------|------|------|---------|---------|
| **P0** | P-01 总览驾驶舱 | `/overview`（默认） | §1.1.1.1.4.6.1 | 完整：4 KPI MetricCard + 结论摘要条 + 4 入口卡（含 mini-chart） |
| **P0** | P-02 分布地图 | `/map` | §...1 | 完整：**沿用 SharedRegionMap.jsx**（如基于 AntD 需新写 Arco 版本到沙箱 components/）+ Leaflet 热力 + 节点弹窗 DetailDrawer + 底部趋势 ChartPanel |
| **P0** | P-03 智能筛选 | `/list` | §...2 | 完整：SearchableCascadeFilter + FilterBar + DataTable（Arco Table 虚拟滚动）+ 右侧预览面板 |
| **P0** | P-05 多维统计 | `/stats` | §...4 | 完整：4 主图（年度折线+柱 / 类型饼 / 单位横向条形 / 词云+树图）+ 时间范围控件 |
| P1 | P-04 课题详情 | `/detail/:projectId` | §...3 | 完整：信息卡 + 时间轴 SectionPanel（⚠️ Q004）+ 影响力 MetricCard + EvidenceList 典型案例 |
| P1 | P-06 互动传播 | `/detail/:projectId/feedback` | §...5 | **占位 UI + ⚠️ "Wave 0 占位" 顶部固定 StatusTag**（不可关闭）；DataCard 4 项统计含 🧪 占位 |
| P1 | P-07 数据导出 | `/export` | §...6 | 完整：三步向导 Form + 导出历史 DataTable（mock）+ 角色权限 SectionPanel |
| P1 | P-08 进展跟踪 | `/progress` | §...7 | 完整：4 KPI MetricCard + 4 阶段看板 + 超期预警 EvidenceList + 全周期溯源 DataTable |

> **执行策略**：先完成 4 个 P0 页面（约 25 min），再补 4 个 P1（约 15 min），最后 5 min 补 README + handoff + push。
> **降级策略**：如 agent 超 40 min 未完成 P1，P-04 / P-06 / P-07 / P-08 可作 stub 占位（最小骨架 + "实现中"提示）；评审重点看 4 个 P0 页面。

## 硬约束（违反即任务失败）

### 范围与隔离（D8 + ui.mdc 铁律）

- **禁改 lumen 任何仓**（gkx_lumen_*）
- **禁改 demo2 主菜单 / 主路由**：`src/data.js` / `src/pageRouting.js` 零改动；`src/App.jsx` 仅追加 1-3 行 lazy 路由桥接
- **禁改配置文件**：`.gitignore` / `package.json` / `vite.config.js` / `tailwind.config.js` / `postcss.config.js` 零改动
- **禁装新依赖**：用 demo2 已有的；如果 Arco 未安装，**立即停在 handoff 标"阻塞：等 PM 决策"**，不要硬装
- **禁改 `src/components/` 现有组件**：复用 OK，但**复制到沙箱 components/ 修改**，避免污染主组件
- **不接 lumen 真实 API**：只用 mocks/

### D8 设计规范（违反即 §18 不过）

- **新页面用 Arco Design**；demo2 历史 AntD 兼容保留，**同页面禁混搭**（一个页面只能一套组件库）
- **token 不硬编码**：颜色 / 圆角 / 字号 / 间距 / 阴影全部从 D8 §7 token 导入（CSS 变量或 JS 常量）
- **方向性指标硬铁律**：上升红 `#ff4d4f`、下降绿 `#00b42a`、持平灰；连续量比较只用蓝系梯度
- **11 类业务对象固定配色**：**"课题" = chart-09**（深绿）；其他类目按 §7.3.3 全局映射
- **图表分类色按 chart-01~chart-20 序列**；Tag 浅底深字（不直接用高饱和图表色作 Tag 底色）
- **卡片 / 图表容器 8px 圆角**；浅色蓝灰风格；**禁深色霓虹大屏 / 强营销渐变 / 装饰纹理**
- **§9 通用组件命名落地**：jsx 组件命名沿用 wireframe 区块名（`<MetricCard>` `<SectionPanel>` `<DetailDrawer>` `<EvidenceList>` `<ChartPanel>` `<MapPanel>` `<FilterBar>` `<SearchableCascadeFilter>` `<DataTable>` `<StatusTag>` 等）
- **复杂筛选 4 项必有**：搜索 / 重置 / 确认 / 已选摘要（D8 §11）
- **文案克制**：不写"智能赋能 / 一站式 / 全方位"等空泛词；不写解释 UI 如何使用的说明文案
- **响应式**：默认 1440 中屏；适配 1920 / 1366；窄屏（< 1366）侧边栏折叠
- **可访问性（WCAG AA）**：语义化标签、键盘可达、对比度达标

### D9 数据血缘三组件（违反即 DoD 不过）

- **`MetricSpecCard.jsx`**（ⓘ 触发；Arco `Popover` + 自封装内容）
  - 触发：每个统计数字旁 ⓘ 图标 hover/点击
  - 内容：8 件套元数据（metric_id / metric_name_zh / definition / formula / source_tables / source_systems / update_freq / version）
  - 数据源：从 `mocks/sandbox/soft-science-2026-06-17/metrics-catalog.json` 动态读，**不硬编码到组件代码中**
  - 降级：catalog 未命中时显示"数据说明加载中"，不阻塞主界面
  - 底部按钮："查看完整加工链路 →" 触发 DataLineageDrawer
- **`MockBadge.jsx`**（🧪；emoji + Arco `Tooltip`）
  - Wave 0 阶段**所有统计数字旁强制显示**
  - tooltip 文本：`Mock 数据，预计 {mock_until} 切换为真实数据源 {source_systems}`
- **`DataLineageDrawer.jsx`**（"完整加工链路" Arco `Drawer`）
  - 触发：MetricSpecCard 底部按钮
  - 内容：ODS → DWD → DWS → ADS 4 段血缘可视化 + 算法节点（Wave 0 用 mermaid 占位或静态 SVG 即可）

### Mock 数据（违反即 DoD 第 5 条不过）

- **至少 30-50 条软科学课题**（覆盖 P-03 列表分页测试 + 空值率 ≥15% 触发 empty 状态）
- **字段名严格沿用 ODS**（与 `dwd_zh_project` 22 字段对齐）：
  - `id` / `title` / `project_number` / `project_source` / `funded_institution` / `funded_province`
  - `approval_year` / `approval_time` / `project_level` / `funded_amount`
  - `discipline` / `discipline_code` / `keywords[]` / `abstract`
  - `research_period` / `project_host` / `project_page_url` / `final_report_abstract`
  - `updated_time`
- **数据贴近真实**（对齐 DS-25-data-availability-matrix §5）：
  - 课题名称风格：政策研究 / 治理创新 / 战略评估 / 产业分析 类
  - 单位真实存在：深圳大学 / 南方科技大学 / 中山大学（深圳）/ 深圳社科院 / 深圳综合开发研究院
  - 资助金额：5–50 万合理范围
  - 学科范畴：管理学 / 公共管理 / 应用经济学 / 社会学 / 政治学 / 软科学
  - 立项时间：2018–2026 合理分布
- **固定种子可重复**（seed=42）；mock 文件 `_mock_meta` 顶部含 `batch_id: mock_20260617_seed42`
- **metrics-catalog.json 含全部 26 个 metric_id**（UX handoff §11.1 列出）

### 待甲方决策项的 UI 角标（D9 + 客户决策清单跟踪表）

| 位置 | 决策项 | UI 表达 |
|------|--------|---------|
| P-02 / P-03 / P-04 学科筛选 + 课题学科字段 | **Q001** 软科学过滤口径 | 学科 Tag 右上角 ⚠️ icon + Tooltip "口径待甲方确认 Q001" |
| P-02 地图层级切换（市/区级下钻按钮） | **Q003** 市区下钻精度 | 市/区级按钮 disabled 或带 ⚠️ icon |
| P-04 时间轴 4 阶段 + P-08 阶段名 | **Q004** 时间轴语义 | 阶段名旁 ⚠️ icon |
| P-06 整页 | **Q005** 互动 Wave 0 | **顶部固定黄色 StatusTag**（不可关闭）："Wave 0 占位，等待 Q005 甲方决策" |
| P-08 超期阈值 14d/30d | **K-O7** 阈值 | 阈值数字旁 ⚠️ icon "团队建议 14d 黄 / 30d 红，待甲方拍板" |

### git 纪律（demo2 main 直推）

- 在 demo2 main 分支 `git add` + `git commit` + `git push`（**只 commit 本沙箱目录文件**，不动其他文件；如果 `App.jsx` 改了 1-3 行路由桥接，一起 commit 但单独说明）
- commit message：`[sandbox] ui-agent 试点：DS-25 软科学成果展示沙箱页`
- commit 作者标记：commit message 末尾加 `[agent:ui-agent]`（团队公约 §3.3）
- **允许直接 git push** 到 origin/main（demo2 自动部署）；push 后约 2-3 min 远端可访问
- **禁止 `git push --force`** / `-f`（团队公约 §6 git 安全协议）
- ⚠️ **仅限 demo2 仓**：lumen 仓仍走 PR 流程，本规则不适用

## DoD（完成定义，逐项打勾）

### 工程自检 10 条（ui.mdc §产物质量自检）

- [ ] 路由 `/sandbox/soft-science-2026-06-17/*` 8 个页面均可访问
- [ ] 覆盖 wireframe 全部 8 页（P0 完整 + P1 完整或 stub 占位明确）
- [ ] 主菜单未变化（`src/data.js` 零改动；`git diff src/data.js` 空）
- [ ] `package.json` / `vite.config.js` / `tailwind.config.js` / `.gitignore` 零改动
- [ ] Mock 数据真实（不是 lorem ipsum）、字段名沿用 ODS、含 `_mock_meta` 批次标识
- [ ] 响应式 1280 / 1440 / 1920 三档不破版
- [ ] 关键交互节点埋点 `console.log('ss.xxx.event')`（沿用 userflow §3 16 个埋点名）
- [ ] `npm run dev` 启动无错误 + HMR 正常
- [ ] `npm run build` 构建通过（无错误，警告可接受）
- [ ] **D9 三件套**：MetricSpecCard + DataLineageDrawer + MockBadge 均实现 + 在 P-01 / P-02 / P-05 至少 3 个统计数字旁能触发

### 设计规范合规自检 18 条（D8 §18）

- [ ] 18 条逐条对照 handoff 末尾表格化勾选；红线项（分析工作台 / 非门户、上升红下降绿、Arco 优先、8px 圆角、文案克制等）100% 过
- [ ] 第 19 条（D9 数据血缘）：每个统计数字可追溯 ✅

### 业务口径未定标 ⚠️ 角标 5 处

- [ ] Q001 软科学口径：学科字段 + 学科筛选挂 ⚠️（P-02 / P-03 / P-04）
- [ ] Q003 市区下钻：P-02 市/区级按钮挂 ⚠️
- [ ] Q004 时间轴语义：P-04 时间轴 + P-08 阶段名挂 ⚠️
- [ ] Q005 互动 Wave 0：P-06 顶部固定 StatusTag
- [ ] K-O7 预警阈值：P-08 阈值数字挂 ⚠️

### git 纪律

- [ ] git add + commit + **push** 到 demo2 origin/main（commit hash 记入 handoff）
- [ ] `git status` 显示 `Your branch is up to date with 'origin/main'`
- [ ] commit message 含 `[agent:ui-agent]` 标记
- [ ] 沙箱页 URL 远端可访问（push 后 2-3 min；根据 demo2 实际路由模式 hash 或 history 回填）

## Handoff 位置与必填项

**位置**：`E:\gkx_src\agent-delivery\agent-handoffs\UI-DS-25-trial.md`

**模板**：参考 ui.mdc handoff 模板 + UX-DS-25-trial.md 章节结构（直接照搬）

必填项：
1. 执行时间 + 任务范围
2. 完成清单对照 DoD（表格：工程 10 条 + §18 18 条 + ⚠️ 5 处 + git 4 项 = 37 项）
3. 产物绝对路径（jsx / mocks / handoff 全部列）
4. 体量统计（jsx 行数 / mock JSON 体量 / 总字符）
5. commit hash + 改动文件数 + push 远端状态
6. 范围与实现（scope_ref / implementation_as_built / data_gaps / variance_note）
7. **§18 18 条对照表**（每条 ✅ / ⚠️ N/A / ❌；红线项必 ✅；UX 阶段已自检 8 条，UI 阶段补 10 条）
8. **D9 数据血缘三组件实现证据**：3 个组件文件路径 + 演示截图（P-01 / P-02 / P-05 各 1 个统计数字触发 MetricSpecCard 截图）+ metrics-catalog.json 路径
9. **业务口径 ⚠️ 角标 5 处实现证据**（每处截图或代码片段）
10. **8 页面截图清单**（每页 1 张 1440 宽截图，放 `agent-handoffs/软科学成果展示-DS25/UI-DS-25-trial-screenshots/`；P-06 占位截图也算）
11. mock 数据规模（条数 + 字段覆盖率 + 空值率）+ 与 ODS 字段对照表（mock 字段名 ↔ `dwd_zh_project.*`）
12. 已知限制（哪些交互未实现、哪些图表降级、哪些组件 stub）
13. 给 PM + UI/UE 评审的"重点看 3 项"建议（K-O3 时间轴 / K-O4 Q005 占位 / K-O8 影响力公式 等可视化决策）
14. 给 frontend-agent 后续 lumen 复刻的提示（哪些组件值得提到 src/components/、哪些 mock 字段对接 Java REST 时需注意）
15. **【试点反馈】**（详见下方）

### 试点反馈要求（本次试点新增章节）

作为团队智能体编排试点 Step 2，你必须在 handoff 末尾额外写一节 `## 试点反馈`，包含：

1. **耗时实测**：实际耗时 vs 估算（计划 45 min）；哪些步骤超时？为什么？
2. **必读文件评价**：上方 17 项必读文件中，哪些**用处大**、哪些**用处小或冗余**？是否有遗漏？
3. **派单话术评价**：本派单话术哪些指令**清晰可直接执行**？哪些**有歧义、需要 PM 澄清**？
4. **UX 产物可用性**：UX Step 1 的 4 份产物 + handoff §10 接力建议，**最有用的 3 项** vs **不够用的 1-2 项**（如某字段没给 / 某组件实现细节缺）
5. **D8 / D9 规范实战落地**：
   - 最容易落地的 3 条规范 vs 最难落地的 3 条
   - Arco Design 在 8 个页面中的覆盖率（哪些组件直接用 Arco / 哪些需自封装）
   - D9 三组件实现工作量评估（如果扩到 7 要素全部页面，单组件成本？）
6. **与 DS-15 沙箱页（pre-D8）对比**：
   - DS-15 用 AntD + Tailwind；DS-25 用 Arco。**视觉气质差异**？
   - DS-15 无 metric_id / 无 ⓘ；DS-25 有 D9 三件套。**汇报场景下数据可信度差异**？
   - DS-15 组件命名口语化；DS-25 严格 §9。**代码可读性差异**？
7. **给 PM 的 3 条改进建议**：用于优化下一次试点的派单话术 / 角色规约 / 编排手册 / D8 D9 规范

## 成本回填（团队公约 §3.7 铁律）

handoff 完成时回填 5 个字段（`agent-delivery/budget-estimate.md` 第 2 节有模型与估算）：

- `estimated_tokens`: 派单前估算（UI 实现类约 150k–250k）
- `actual_tokens`: 实测 in+out 总和
- `model_used`: claude-opus-4.7 / claude-sonnet-4.5 / gpt-5 等
- `actual_cost`: 美元
- `cost_warn`: green / yellow($>5) / orange($>10) / red($>20)

> 单 task 实际 > $10 暂停复盘；> $20 hard stop。

## 最终响应（必须在 Cursor 会话最后一次回复中包含）

1. 沙箱入口 URL（本地 `http://127.0.0.1:4176/#/sandbox/soft-science-2026-06-17` 或对应 history 路由）
2. 远端部署 URL（push 后 2-3 min 可访问的地址）
3. 8 个页面 URL 列表 + 每页一句话状态描述（完整 / stub / 占位）
4. commit hash + 改动文件数 + push 状态（`up to date with 'origin/main'`）
5. §18 18 条对照表摘要（绿 / 黄 / 红 项数量）
6. D9 三件套实现位置（3 个 jsx 文件绝对路径）
7. 5 处 ⚠️ 待甲方角标实现位置（页面 + 字段）
8. mock 数据规模（课题条数 / metric_id 数量 / 字段 ODS 对照覆盖率）
9. 试点反馈中的 3 条改进建议
10. 给 PM + UI/UE 评审的"重点看 3 项"建议

中文产出。开始执行。

## ====== 派单话术结束 ======

---

## PM 在 UI 完成后的评审要点（给你自己留备忘）

### 评审清单（30 分钟内可完成）

| 检查项 | 通过标准 | 阻塞标志 |
|--------|---------|---------|
| 8 个页面 URL 全部可访问 | 本地 + 远端均 200 | 任一 404 / 500 |
| 主菜单未变化 | `git diff src/data.js` 空 | 主菜单出现 DS-25 入口 / 被改 |
| 配置文件零改动 | `git diff package.json` / `vite.config.js` 空 | 出现 `^arco-design/web-react` 之外的新依赖 |
| **Arco vs AntD 隔离** | 沙箱页 100% Arco；同页面无 AntD 混搭 | `import { Card } from 'antd'` 出现在沙箱目录 |
| **token 不硬编码** | 颜色 / 字号 / 间距均引用 token | `color: '#1677ff'` 或 `padding: 16px` 等魔法值 |
| **D9 三件套** | 3 个组件文件存在 + P-01/P-02/P-05 各 1 处 ⓘ 可触发 + 🧪 数字旁可见 | 缺组件 / 缺触发 / 缺 🧪 |
| **5 处 ⚠️ 角标** | Q001/Q003/Q004/Q005/K-O7 落地证据 | 任一缺失 |
| **mock 字段沿用 ODS** | `dwd_zh_project.*` 字段名直接出现在 mock JSON | 出现 `课题名` / `keti_name` 等中文/拼音键 |
| **§18 18 条** | 红线项 100% 过；handoff 末尾有对照表 | 红线项任一未过 |
| 试点反馈 7 节 | 都写了（含与 DS-15 对比） | 跳过 = 失去复盘价值 |

### 评审通过后

1. 与 UE lead 同步评审结果（5 min）
2. 在团队群通报：沙箱页本地 URL + 远端 URL + commit hash
3. 通知 architect-agent 评估 D9 三组件是否升级到 D8 §9 正式清单（15 → 18）
4. 通知 data-agent 按 UX handoff §11.2 优先级注册 26 个 metric_id 到 cfg_metric DDL
5. retro 旁听：把试点反馈整合到 retro 文档，准备 Step 3（下次 DS 试点的派单话术优化）

### 评审不通过（需返工）

- 在 `agent-handoffs/软科学成果展示-DS25/UI-DS-25-trial.md` 末尾加 `## PM 评审意见` 节，列出具体修改项
- 让 UI 同学在原会话内接续修改（不开新会话，保留上下文）
- 严重违反（如改了主菜单 / 装了新依赖 / 大量硬编码 token）：`git checkout` 还原相关文件后让 agent 重做

---

## 角色对齐（团队公约 §6）

| 谁 | 做什么 | 不做什么 |
|----|--------|---------|
| **PM（你）** | 派单 / 评审 / 与 UE 对齐 / 决策推送 | 直接改 UI 产出（违反"决策不外包 + 评审到位"原则） |
| **UI 同学** | 开 Cursor 会话 + 复制话术 + 监督 ui-agent 产出（每 10 min 瞄一眼）+ 完工本地验收 5 min | 写后端 / 改 lumen / 改主菜单 / 装新依赖 |
| **ui-agent（AI）** | 按话术产出 jsx / mocks / 3 D9 组件 / handoff / commit + push | 改 lumen / 改主菜单 / 装新依赖 / 改配置文件 / 替甲方决定业务口径 |
| **UE lead** | 与 PM 联审视觉气质 + 信息层级 + 数据血缘 UI 触发流畅性 | 替 PM 决策 |
| **architect-agent**（评审后） | 评估 D9 三组件是否升级到 D8 §9 正式清单 | 越界改实现代码 |
| **frontend-agent**（评审后） | 评估哪些沙箱组件值得工程化复刻到 lumen `gkx_lumen_fronted_pc/src/components/`（demo2 → lumen 通过重写而非 merge） | 直接 merge demo2 到 lumen（铁律禁止） |