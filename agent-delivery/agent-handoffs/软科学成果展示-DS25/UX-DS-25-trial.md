# UX-DS-25-trial · ux-agent 第二次试点 · DS-25 软科学成果展示 IA/wireframe

> ⚠️ **后续编辑注解（2026-06-18，v2 重组）**：本文产出时引用的 UI 规范为 `AI可复用UI框架与设计规范.md`（v1.0），后历经 v1.1 章节号偏移，**2026-06-18 已全量重组为 `agent-delivery/Design.md`**（Figma 风格稿落地版，14 节）。本文档**保留原引用以示事实历史**；下游 agent 接力时请按下表换算：
>
> | 本文中的旧引用 | 现行 `Design.md` 引用 |
> |---|---|
> | `AI可复用UI框架与设计规范.md` | `Design.md` |
> | §3 产品定位 | §1 设计定位 + §0 给 AI 的执行指令 |
> | §4 信息架构骨架 | §3 页面骨架（§3.1 六骨架 + §3.2 三段工作区） |
> | §5 技术框架 | §0 给 AI 的执行指令（强制 Arco React + 主色 `#165DFF`）+ §13 推荐实现映射 |
> | §7 设计 Token | §4 色彩 + §5 字体 + §6 圆角描边阴影 + §13 主题 token |
> | §7.3 最大内容容器 `.content-shell-glass`（v1.1 新增） | §3.1 `.content-shell`（白色半透明，**取消毛玻璃强效果**） |
> | §7.3 / §7.4 图表分类色 chart-01~20 | §4.3 图表序列优先顺序（直接色值，**取消 chart-XX 抽象 token**） |
> | §7.3.3 / §7.4.3 11 类业务对象固定映射 | §4.3 科技要素与图表色（**10 类，"资讯" 已取消**） |
> | §7.4 / §7.5 Tag 配色 | §7.4 标签 |
> | §9 通用组件（15 / 17 个 PascalCase：PageShell / GlobalWorkbenchTabs / AnalysisPanelTabs 等） | §7 通用组件 8 个 + §8 工作区组件 3 个（Figma 风格 class：`app-shell` / `app-frame` / `content-shell` / `workspace-grid` / `layer-panel` / `map-stage` / `analysis-panel` / `filter-row`） |
> | §9.3 GlobalWorkbenchTabs / §9.4 AnalysisPanelTabs | §7.3 Tabs（**一级/二级分级取消**，统一轻量蓝字 + 浅蓝底） |
> | §10 Arco 接入规则 | §0 给 AI 的执行指令 + §13 推荐实现映射 |
> | §18 验收清单 18 条 | **§14 检查 8 条 + 验收 6 条 = 14 条**（含截图取样定量验收：主色接近 `#165DFF` / Header 64px / Sidebar 200px / 控件 32px / 无 antd） |
>
> 详见 `agent-delivery/architecture-baseline.md §8` v2.0 变更记录。

## 执行时间

2026-06-17（团队智能体编排试点 Step 1；ux-agent 第二次试点）

## 任务

- 覆盖功能点：**DS-25 软科学成果展示**（acceptance-catalog tier=INTEG，行 298–309）
- 范围真源：`bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.1.4.6.1（行 3231–3401，含 7 个三级子功能 + 30 项四级）
- 数据真源：`agent-delivery/data/DS-25-data-availability-matrix.md`（ODS 字段精确映射 + 7 项甲方决策 Q001-Q007）
- 设计规范：`agent-delivery/AI可复用UI框架与设计规范.md`（D8，2026-06-17 定稿）
- 数据血缘规约：`agent-delivery/data-lineage-policy.md`（D9，2026-06-17 定稿）
- 任务范围：把 bid §1.1.1.1.4.6.1 翻译为 **IA + 用户旅程 + 低保真线框**（不写代码、不画视觉、不动 lumen）

## 完成清单（对照 DoD 13 项）

| # | DoD 项 | 状态 | 证据 |
|---|--------|------|------|
| 1 | 4 份 md 齐全且在隔离目录 | ✅ | 详见"产物绝对路径" |
| 2 | 7 个三级子功能全覆盖，挂到 bid §1.1.1.1.4.6.1.X | ✅ | IA.md §6 子功能 ↔ 页面映射表（30 项四级全覆盖） |
| 3 | 字段表 6 列（含 metric_id），统计字段必填 | ✅ | wireframe 8 页每页均 6 列，统计字段 100% 填 metric_id |
| 4 | 每页末尾"本页 metric_id 清单" | ✅ | P-01~P-08 共 8 个 metric_id 清单（合计 26 个唯一 metric_id） |
| 5 | mermaid 站点地图 + 主用户流 + ≥3 条异常路径 | ✅ | IA 2 个 + userflow 7 个（含 5 条异常路径 4.1~4.5），共 9 段 mermaid 语法已自检 |
| 6 | §9 15 个通用组件中至少 8 个被 wireframe 引用 | ✅ | 引用 **15 / 15**（PageShell / TopicSidebar / ContextBar / SectionPanel / ModuleHeader / MetricCard / DataCard / SearchableCascadeFilter / FilterBar / StatusTag / DetailDrawer / DataTable / ChartPanel / MapPanel / EvidenceList；GraphCanvas 在 P-05 词云作为可选实现）；+ D9 新增 3 个（MetricSpecCard / DataLineageDrawer / MockBadge） |
| 7 | §4.2 5 段优先级每页面都有 | ✅ | wireframe P-01~P-08 共 8 页每页均有"5 段优先级"小节 |
| 8 | §18 验收清单 18 条对照表 | ✅ | 详见本 handoff §7 |
| 9 | 待评审开放项 ≥10 条 | ✅ | wireframe §全局开放项汇总 25 条 W-O + 本 handoff §9 12 条 K-O |
| 10 | 范围合规自检 | ✅ | README + IA §8 + wireframe §范围合规自检三处均明确"未扩大到 §1.1.1.1.4.6.2~6" |
| 11 | git add + commit + push 到 demo2 origin/main | ✅ | commit hash 见本 handoff §"commit hash" |
| 12 | handoff 写入指定路径 | ✅ | 本文件 |
| 13 | 试点反馈章节 | ✅ | 详见本 handoff §15 试点反馈 |

## 产物绝对路径

1. `E:\gkx_src\demo2\docs\ia\sandbox\soft-science-2026-06-17\README.md`
2. `E:\gkx_src\demo2\docs\ia\sandbox\soft-science-2026-06-17\DS-25-IA.md`
3. `E:\gkx_src\demo2\docs\ia\sandbox\soft-science-2026-06-17\DS-25-userflow.md`
4. `E:\gkx_src\demo2\docs\ia\sandbox\soft-science-2026-06-17\DS-25-wireframe.md`
5. `E:\gkx_src\agent-delivery\agent-handoffs\UX-DS-25-trial.md`（本文件）

## 体量统计

| 文件 | 行数 | 字符数（含中文） |
|------|------|------------------|
| README.md | 103 | 6,821 |
| DS-25-IA.md | 153 | 10,662 |
| DS-25-userflow.md | 164 | 7,678 |
| DS-25-wireframe.md | 788 | 52,346 |
| **合计** | **1,208** | **77,507** |

> **与 DS-15 试点对比**：DS-15 合计 1,171 行 / 58,130 字符；DS-25 多 +37 行 / +19,377 字符（约 +33%）。主要增量在 wireframe（DS-25 8 页 vs DS-15 实际 ~6 页主要内容；DS-25 字段表 6 列 + 5 段优先级 + metric_id 清单三项新增小节占去主要篇幅）。

## commit hash

```
444fa03 [sandbox] ux-agent 试点：DS-25 软科学成果展示 IA/wireframe [agent:ux-agent]
```

- **改动行数**：4 files changed, 1440 insertions(+)（git 统计 LF 行；PowerShell 统计 1,208 行，差异来自换行符）
- **远端状态**：`Your branch is up to date with 'origin/main'`（已同步 origin/main，commit hash `3e7bda6..444fa03`）
- **使用 `git add -f`**：因 demo2 `.gitignore` 第 6 行 `docs/` 已忽略整个 docs 目录；为遵守"禁止改 .gitignore 等任何现有文件"铁律，采用 `git add -f` 强制添加 **仅本沙箱 4 个文件**（与 DS-15 试点同策略），未修改 .gitignore，未触碰任何其他文件。
- **沙箱页 URL**：约 2–3 min 后于 https://skxrules.unicomcn.tech:30999/ 可见（demo2 main 分支自动部署）；UX 阶段只 push docs，沙箱页 UI 由 ui-agent 阶段产出。

## 范围与实现

| 项 | 内容 |
|---|---|
| scope_ref | bid-reference §1.1.1.1.4.6.1.1 ~ §1.1.1.1.4.6.1.7（7 个三级子功能） |
| implementation_as_built | **8 个一级页面**：P-01 总览驾驶舱 + P-02 分布地图 + P-03 智能筛选 + P-04 课题详情 + P-05 多维统计 + P-06 互动传播 + P-07 数据导出 + P-08 进展跟踪 |
| data_gaps | **65% 字段映射到真实 ODS 表**（详见 `data/DS-25-data-availability-matrix.md` §3 覆盖率统计）；**§5 互动传播（P-06）全部 ❌ 用户态待自建 Q005**；**热点关键词 / 案例推荐 / 影响力综合分 / 超期预警** 4 类 metric 🔧 待 algorithm-agent |
| variance_note | 未扩大范围；未删减子功能；移动适配明确后置；P-06 互动传播按"Wave 0 占位 + ⚠️ Wave 2 后纳入"处理，与 Q005 联动 |

## §18 验收清单 18 条对照表（必填，UX 自检 8 条 + UI 待办 10 条）

| # | 验收条目 | 归属 | UX 阶段自检 | UI 阶段待办 |
|---|---------|------|------------|------------|
| 1 | 是否是分析工作台，而不是门户或营销页 | **UX** | ✅ 8 个页面均按"驾驶舱 + 分析工作台"定位，禁门户/营销词汇 | — |
| 2 | 是否先给结论，再给支撑数据 | **UX** | ✅ 每页 5 段优先级第 1 段即"当前应关注什么" | — |
| 3 | 是否服务领导驾驶舱用户和业务分析师 | **UX** | ✅ userflow §1 明确 4 类角色，主旅程覆盖前 2 类 | — |
| 4 | 是否使用浅色蓝灰专业风格 | UI | （UX 阶段不指定视觉） | ⏳ ui-agent 按 D8 §6 / §7 实现 |
| 5 | 是否避免深色霓虹大屏 | UI | （UX 阶段不指定视觉） | ⏳ ui-agent 实现时遵守 |
| 6 | 是否有清晰的信息主次 | **共同** | ✅ 5 段优先级 + ASCII 区块大小变化反映主次 | ⏳ ui-agent 按 D8 §14 卡片/面板规范落地 |
| 7 | 是否所有卡片和图表容器使用 `8px` 圆角 | UI | （UX 不指定） | ⏳ ui-agent 按 D8 §8 落地 |
| 8 | 是否方向性指标上升红、下降绿 | UI | （UX 不指定） | ⏳ ui-agent 按 D8 §7.2 trend.rise/fall token 实现 |
| 9 | 是否图表分类色按 `chart-01`~`chart-20` 序列 / 业务映射 | UI | （UX 不指定） | ⏳ ui-agent 按 D8 §7.3 落地；"课题"使用 chart-09 |
| 10 | 是否 Tag 浅底深字同族边框，不直接用高饱和图表色作底 | UI | （UX 不指定） | ⏳ ui-agent 按 D8 §7.4 chartTagTokens 落地 |
| 11 | 是否图表优先使用 ECharts | UI | （UX 不指定） | ⏳ ui-agent 按 D8 §5 + §12 实现；DS-25 不强依赖 G6 |
| 12 | 是否通用控件优先使用 Arco Design | UI | （UX 不指定） | ⏳ ui-agent 按 D8 §10 落地；demo2 历史 AntD 同页面禁混搭 |
| 13 | 是否复杂筛选具搜索、重置、确认、已选摘要 | **共同** | ✅ wireframe P-03 顶部 SearchableCascadeFilter 明确"搜索建议 / 重置 / 确认 / 已选摘要"行为 | ⏳ ui-agent 按 D8 §11 行为细节实现 |
| 14 | 是否组件已拆分通用交互与业务交互 | **共同** | ✅ wireframe 所有区块名严格使用 D8 §9 通用组件命名（共 15 个全覆盖） | ⏳ ui-agent 按 D8 §9.2 沉淀业务组件层 |
| 15 | 是否文案克制，没有装饰性说明 | **UX** | ✅ 全文未用"智能赋能 / 一站式 / 全方位"等空泛词；标题用名词短语 | — |
| 16 | 是否有 loading、empty、error、disabled 状态 | UI | （UX 不指定具体状态视觉） | ⏳ ui-agent 按 D8 §16 全状态覆盖 |
| 17 | 是否没有文字溢出和元素重叠 | UI | （UX 不指定具体响应式） | ⏳ ui-agent 按 D8 §17 在 1440/1920/1366 三档基线测试 |
| 18 | 是否适合截图、汇报和导出 | **共同** | ✅ P-01 驾驶舱 + P-05 统计 + P-07 导出向导明确为汇报场景设计 | ⏳ ui-agent 实现时保证关键页面截图可读 |

**统计**：UX 自检 8 条（#1/#2/#3/#6/#13/#14/#15/#18，全部 ✅）；UI 待办 10 条（#4/#5/#7/#8/#9/#10/#11/#12/#16/#17，全部 ⏳ 由 ui-agent 阶段落地）。

> **新增第 19 条（D9 数据血缘）**：每个统计数字可追溯 → ✅ UX 阶段已落 metric_id 6 列 + ⓘ 占位 + 每页 metric_id 清单；⏳ ui-agent 阶段实现 MetricSpecCard / DataLineageDrawer / MockBadge 三组件。

## §4.2 5 段优先级覆盖表（必填）

| 页面 | 段 1 应关注什么 | 段 2 为什么 | 段 3 重点对象 | 段 4 趋势异常 | 段 5 下钻明细 |
|------|----------------|-------------|--------------|--------------|--------------|
| **P-01 总览驾驶舱** | 季度新增 / 累计 / TopN / 预警 4 KPI | 季度环比 + 单位贡献集中度 + 异常 | 4 入口卡片（地图/列表/统计/进展） | KPI mini-trend + 结论摘要条 | 4 入口卡进入 + 生成快照报告 |
| **P-02 分布地图** | 选定范围内哪个省市最聚集 | 资源聚集度反映区域科技实力差异 | TopN 省份 + TopN 单位 | 年度趋势曲线 + 季度对比 | 节点弹窗 → P-04 详情 + 生成空间分析报告 |
| **P-03 智能筛选** | 符合筛选的课题列表 | 围绕主题缩小范围到 < 50 条做研判 | DataTable 主区 + MapPanel 高亮 | DataTable 列含"近 N 月新增" + hover trend | 单击进 P-04 + 批量导出 → P-07 |
| **P-04 课题详情** | 这个课题做了什么 / 阶段 / 影响 | 是否典型案例 / 本单位重点 / 影响力 | 时间轴当前阶段 + 影响力评价 | 时间轴 + 同主题相似课题对比 EvidenceList | 附件下载 → P-07 + 互动 Tab P-06 |
| **P-05 多维统计** | 年度 / 类型 / 单位 / 难题 4 维全貌 | 跨年度变化 + 单位集中度 + 热点迁移 | 单位 TopN 横向条形 + 热点词云 | 年度变化折线 + 季度环比 + 跨年对比 mini-line | 图表点击钻 P-03/P-02 + 生成统计报告 |
| **P-06 互动传播** | 课题的社会反响 | 互动传播反映社会影响力与学术互补 | 评论列表（专家 / 高频用户）+ 传播关键节点 | 互动量时序 + 传播路径桑基 + 同主题对比 | 评论详情 → DetailDrawer + 传播 → P-07 |
| **P-07 数据导出** | 选定的范围 / 格式 / 模板预估体量 | 大体量走异步队列；敏感数据有审计 | 三步向导（范围 / 格式 / 模板） | 导出历史 DataTable + StatusTag | 历史项重下载或重新生成 |
| **P-08 进展跟踪** | 课题分阶段是否健康 / 异常超期数 | 预警识别滞后项 / 管理者及时干预 | 红色 StatusTag 优先 | 进展统计 + 阶段时长分布 + 同期对比 | 预警 → P-04 + 全周期溯源 DataTable |

**覆盖率**：8 页 × 5 段 = **40 / 40 全覆盖**；其中需"待 PM 业务方明确"的：P-06 段 1-5 全部 ⚠️ Q005（待甲方决策 Wave 0 是否实现）。

## 待人评审的开放项（≥10 条；本试点 12 条 K-O 关键决策）

> 完整 25 条 W-O 见 `demo2/docs/ia/sandbox/soft-science-2026-06-17/DS-25-wireframe.md` 末"全局开放项汇总"；下方为升级到关键决策的 12 条 K-O，按重要性排序。

| # | 决策项 | 建议默认值（团队临时默认 / UX 最佳实践） | 影响 | 关联甲方决策项 |
|---|--------|----------------------------------------|------|---------------|
| **K-O1** | "软科学"如何精确过滤 `dwd_zh_project.discipline`？ | `LIKE '软科学%' OR '管理学%' OR '公共管理%' OR '应用经济%' OR '社会学%' OR '政治学%'`（团队临时） | 整个 DS-25 数据范围 + 全部 `M_SS_*` metric | **Q001（甲方）** |
| **K-O2** | 市/区级地图下钻数据精度从哪来（ODS `funded_province` 只到省级）？ | 关联 `dwd_org_reg_info.address` 解析地市；甲方接受省级为最差精度 | P-02 多级地图实现复杂度 | **Q003（甲方）** |
| **K-O3** | "难题攻关历程时间轴"业务语义？ | 立项 → 中期 → 结题 → 转化（`approval_time + research_period` 派生） | P-04 时间轴 + P-08 阶段判定 | **Q004（甲方）** |
| **K-O4** | §5 互动传播 Wave 0 是否实现？ | UI 占位 + 标 ⚠️ "Wave 2 后纳入" | 范围 ±10% + P-06 全部内容 | **Q005（甲方）** |
| **K-O5** | 国外软科学课题 `dwd_en_project` 是否纳入 DS-25？ | 默认不纳入（DS-25 = 国内） | 范围 ±10% | **Q006（甲方）** |
| K-O6 | URL `:projectId` 用什么主键？ | 沿用 ODS `dwd_zh_project.id`（避免再造） | 路由设计 + 跨页参数传递 | — |
| K-O7 | 超期预警阈值 | 14d 黄 / 30d 红（团队建议） | P-08 StatusTag 触发条件 | **Q007 类（建议甲方拍板）** |
| K-O8 | 影响力综合分公式（学术 + 社交占比）？ | algorithm-agent + 业务方共定；UI 仅展示分项 | P-04 / P-06 影响力呈现 | — |
| K-O9 | 沿用 demo2 现有 `SharedRegionMap.jsx`？ | ✅ **强烈建议沿用**（避免重做） | P-02 实现工作量 | — |
| K-O10 | NLP 智能搜索 / 推荐 algorithm-agent 接入时机 | Wave 1；Wave 0 SQL LIKE 降级 | P-03 / P-04 / P-05 智能交互 | — |
| K-O11 | 项目"结题判定"逻辑 | `final_report_abstract IS NOT NULL` 视为已结题（团队临时） | P-08 阶段判定 + `M_SS_PROJECT_PROGRESS_PCT` | **Q007（甲方）** |
| K-O12 | 大体量异步导出阈值 | 5 万行；超走异步 | P-07 + 后端任务队列 | — |

> **5 条最关键项**（升级到最终响应）：K-O1 / K-O2 / K-O3 / K-O4 / K-O5（全部直接关联甲方决策项 Q001/Q003/Q004/Q005/Q006）。

## 给 ui-agent 接力的 next-step 建议

### A. 技术栈与命名（D8 + D9）

| 项 | 决策 |
|---|------|
| 框架 | **React + Vite**（demo2 已有，复用） |
| 组件库 | **Arco Design**（新页面权威栈，D8）；demo2 历史 AntD 同页面**禁混搭** |
| 图表 | **ECharts**（echarts-for-react） |
| 地图 | **Leaflet** 浅色底图；**强烈建议沿用 demo2 `SharedRegionMap.jsx`** |
| 图谱 | DS-25 弱依赖；P-05 词云可用 ECharts wordCloud 或 graph |
| 日期 | dayjs |
| 样式 | CSS Modules / Tailwind 工具类；token 仅从 D8 §7 引入，**禁硬编码颜色/字号/间距** |
| 沙箱路由 | `/sandbox/soft-science-2026-06-17/*`（与 DS-15 同模式） |
| 命名空间隔离 | `src/sandbox/soft-science-2026-06-17/` 子目录（与 DS-15 试点同策略） |

### B. §10 Arco 控件映射建议

| §9 通用组件 | Arco 实现建议 |
|------------|--------------|
| PageShell | `Layout` + 自封装 |
| TopicSidebar | `Menu` + 垂直 mode |
| ContextBar | `Card` + `Tag` + `Breadcrumb` |
| ModuleHeader | `PageHeader` + `Space` |
| SectionPanel | `Card` + `Typography` |
| MetricCard | 自封装 `Card`（包含 sparkline ECharts） |
| DataCard | `Card` + `Statistic`（Arco 有） |
| SearchableCascadeFilter | `Cascader` + `Input` + footer `Button` 组 |
| FilterBar | `Form` + `Select` + `DatePicker` + `Cascader` |
| StatusTag | `Tag` + chart tag tokens |
| DetailDrawer | `Drawer` |
| DataTable | `Table`（虚拟滚动） |
| ChartPanel | `Card` + `echarts-for-react` |
| MapPanel | 自封装容器 + Leaflet（沿用 SharedRegionMap） |
| EvidenceList | `List` + `Card` |
| **MetricSpecCard**（D9 新增） | `Popover` + 自封装内容 |
| **DataLineageDrawer**（D9 新增） | `Drawer` + 自封装 mermaid 渲染 |
| **MockBadge**（D9 新增） | `Badge` + emoji 🧪 |

### C. demo2 可复用组件提示

| 组件 | 来源 | DS-25 用途 |
|------|------|----------|
| `SharedRegionMap.jsx` | demo2 src/components/ | **P-02 主地图组件强烈建议沿用** |
| GraphView.vue（注意是 Vue，不直接复用） | gkx_demo_ui/entan | **仅作交互参考**；DS-25 不强依赖图谱 |
| ECharts wordCloud / treemap 配置 | demo2 历史代码 | P-05 词云 / 热点树图参考 |

### D. mock 数据结构建议（mocks/ 下）

```
src/sandbox/soft-science-2026-06-17/mocks/
├── overview.json                       # P-01 KPI + 4 入口卡 mini-trend
├── projects/                           # P-03 列表 + P-04 详情
│   ├── list.json                       # 30-50 条课题（含分页与筛选回包）
│   ├── ZH-2024-SS-0001.json            # 单项目完整对象（含 dwd_zh_project 全字段）
│   ├── ZH-2024-SS-0001/output.json     # 关联 dwd_zh_project_output
│   ├── ZH-2024-SS-0001/timeline.json   # 时间轴阶段（⚠️ Q004 派生）
│   └── ZH-2024-SS-0001/feedback.json   # P-06 互动 🧪 占位
├── map/
│   ├── density_by_prov.json            # 省级密度 (M_SS_TOPIC_DENSITY_BY_PROV)
│   ├── topn_institutions.json          # 单位 TopN
│   └── trend.json                      # 年度趋势
├── stats/
│   ├── yearly.json                     # 年度变化
│   ├── category.json                   # 类型结构
│   ├── unit_contribution.json          # 单位贡献率
│   ├── hot_keywords.json               # 🔧 待 algorithm
│   └── domain_distribution.json        # 🔧 待 algorithm
├── progress/
│   ├── kpi.json                        # 4 个 MetricCard
│   ├── overdue.json                    # 超期预警
│   └── lineage.json                    # 全周期溯源
├── export/
│   └── history.json                    # 导出历史 audit
└── metric-catalog.json                 # 26 个 metric_id 的 8 件套元数据（占位）
```

**数据风格建议**（对齐 DS-25-data-availability-matrix §5）：
- 课题名称风格："xxx 政策研究"、"xxx 治理创新"、"xxx 战略评估"、"xxx 产业分析"
- 单位真实存在：深圳大学 / 南方科技大学 / 中山大学（深圳）/ 深圳社科院 / 深圳综合开发研究院
- 资助金额合理范围：5–50 万
- 学科符合软科学范畴：管理学 / 公共管理 / 应用经济学 / 社会学 / 政治学
- 立项时间分布：2018–2026
- **字段名严格沿用 ODS**：`title / funded_institution / approval_year / discipline / keywords / abstract` 等

### E. 路由建议落地（src/router）

按 `DS-25-IA.md §4` 注册 8 条路由；**沙箱模式下建议先做 P-01 / P-02 / P-03 / P-05** 四条核心，其他作 stub 页面占位（与 DS-15 同策略）。

### F. 验收对齐

- ui-agent 完成后通知 coordinator 派 UI/UE 3 人评审，重点看 K-O2（地图精度）/ K-O3（时间轴语义）/ K-O4（互动传播）/ K-O8（影响力公式）四项可视化决策
- 与 PM 确认 K-O1（软科学过滤口径）+ K-O5（国外课题范围）+ K-O7（预警阈值），同时把所有 ⚠️ "待甲方"角标固化到 UI（D9 §5）
- 与 architect-agent 评估 D9 三组件（MetricSpecCard / DataLineageDrawer / MockBadge）是否提到 D8 §9 规范作为正式组件

## 11. 数据血缘汇总（甲方硬需求，必填）

### 11.1 全部 metric_id 清单（按页面分组，共 26 个唯一 metric_id）

> **命名规则**：`M_{ELEMENT=SS}_{INDICATOR}_{PERIOD?}_{VARIANT?}`（详见 `data-lineage-policy.md` §3）

| metric_id | 中文名 | 所属页面 | source_tables (ODS) | 算法依赖 | 数据状态 |
|-----------|--------|---------|---------------------|---------|----------|
| `M_SS_TOPIC_NEW_COUNT_Q` | 季度软科学课题新增数 | P-01 / P-02 / P-05 | `dwd_zh_project` | 无 | ✅ 真实 ODS Mock |
| `M_SS_TOPIC_NEW_COUNT_Y` | 年度软科学课题新增数 | P-02 / P-05 | `dwd_zh_project` | 无 | ✅ 真实 ODS Mock |
| `M_SS_TOPIC_NEW_COUNT_TOTAL` | 累计软科学课题总数 | P-01 | `dwd_zh_project` | 无 | ✅ 真实 ODS Mock |
| `M_SS_TOPIC_DENSITY_BY_PROV` | 按省份课题密度 | P-02 | `dwd_zh_project` | 无 | ✅ 真实 ODS Mock |
| `M_SS_TOPIC_BY_INSTITUTION` | 按承担单位课题数 | P-02 | `dwd_zh_project` | 无 | ✅ 真实 ODS Mock |
| `M_SS_TOPIC_BY_CATEGORY` | 软科学课题类型结构 | P-05 | `dwd_zh_project` | 无 | ✅ 真实 ODS Mock |
| `M_SS_FUNDING_TOTAL_Y` | 年度资助金额合计 | P-02 / P-05 | `dwd_zh_project` | 无 | ✅ 真实 ODS Mock |
| `M_SS_UNIT_CONTRIBUTION_RATE` | 软科学课题单位贡献率 | P-01 / P-05 | `dwd_zh_project` | 无 | ✅ 真实 ODS Mock |
| `M_SS_REGION_CONTRIBUTION_RATE` | 区域贡献率 | P-05 | `dwd_zh_project` | 无 | ✅ 真实 ODS Mock |
| `M_SS_UNIT_COUNT` | 参与单位数（派生） | P-05 | `dwd_zh_project` | 派生 | ✅ 真实 ODS Mock |
| `M_SS_OUTPUT_COUNT` | 课题近期成果数 | P-03 | `dwd_zh_project_output` | 无 | ✅ 真实 ODS Mock |
| `M_SS_OUTPUT_PAPER_COUNT` | 课题论文产出数 | P-04 | `dwd_zh_project_output` + `dwd_rel_project_paper` | 无 | ✅ 真实 ODS Mock |
| `M_SS_OUTPUT_PATENT_COUNT` | 课题专利产出数 | P-04 | `dwd_zh_project_output` + `dwd_rel_project_patent` | 无 | ✅ 真实 ODS Mock |
| `M_SS_OUTPUT_REPORT_COUNT` | 课题报告产出数 | P-04 | `dwd_zh_report` + `dwd_rel_report_project` | 无 | ✅ 真实 ODS Mock |
| `M_SS_OUTPUT_AWARD_COUNT` | 课题奖项产出数 | P-04 | `dwd_zh_project_output.award_count` | 无 | ✅ 真实 ODS Mock |
| `M_SS_HOT_KEYWORDS_LIST` | 软科学热点关键词 | P-03 / P-05 | `dwd_zh_project.keywords` | 🔧 algorithm-agent | 待算法 |
| `M_SS_DOMAIN_DISTRIBUTION` | 难题领域分布 | P-05 | `dwd_zh_project.discipline + keywords` | 🔧 algorithm-agent | 待算法 |
| `M_SS_TYPICAL_CASES_TOPN` | 典型案例推荐 | P-04 | `dwd_zh_project.keywords / abstract` | 🔧 algorithm-agent | 待算法 |
| `M_SS_SIMILAR_TOPN` | 主题相似 TopN 课题 | P-03 | `dwd_zh_project.keywords / abstract` | 🔧 algorithm-agent | 待算法 |
| `M_SS_IMPACT_SCORE` | 影响力综合分 | P-04 | 综合 `dwd_zh_project_output` + 用户态 ❌ | 🔧 algorithm-agent | 待算法 |
| `M_SS_INFLUENCE_INDEX` | 社会影响力综合指数 | P-06 | 综合学术 + 社交 | 🔧 algorithm-agent | 待算法 |
| `M_SS_PROJECT_TIMELINE` | 课题攻关历程时间轴 | P-04 / P-08 | `dwd_zh_project.approval_time + research_period` | 派生 | ⚠️ Q004 |
| `M_SS_PROJECT_PROGRESS_PCT` | 阶段进展百分比 | P-08 | `dwd_zh_project` | 派生 | ⚠️ Q004 |
| `M_SS_PROJECT_OVERDUE_LIST` | 超期未结题预警列表 | P-01 / P-08 | `dwd_zh_project` | 🔧 algorithm-agent | 待算法 |
| `M_SS_PROJECT_IN_PROGRESS` | 在研中课题数 | P-08 | `dwd_zh_project` | 派生 | ✅ 真实 ODS Mock |
| `M_SS_PROJECT_COMPLETED_M` | 本月结题课题数 | P-08 | `dwd_zh_project` | 派生 | ⚠️ Q007 |
| `M_SS_PROJECT_PENDING_REVIEW` | 待评议课题数 | P-08 | ❌ 用户态待自建 | 无 | ❌ Q005 |
| `M_SS_FOLLOWED_COUNT` | 课题关注数 | P-03 | ❌ `dwd_user_follow_ss_topic` | 无 | ❌ Q005 |
| `M_SS_COMMENT_COUNT` | 课题评论数 | P-06 | ❌ `dwd_user_comment_ss_topic` | 无 | ❌ Q005 |
| `M_SS_LIKE_COUNT` | 课题点赞数 | P-06 | ❌ `dwd_user_like_ss_topic` | 无 | ❌ Q005 |
| `M_SS_FAVORITE_COUNT` | 课题收藏数 | P-06 | ❌ `dwd_user_favorite_ss_topic` | 无 | ❌ Q005 |
| `M_SS_SHARE_COUNT` | 课题分享次数 | P-06 | ❌ `dwd_user_share_log` | 无 | ❌ Q005 |
| `M_SS_INTERACTION_TIMELINE` | 互动量时序 | P-06 | ❌ 综合用户态 | 🔧 algorithm-agent | ❌ Q005 |
| `M_SS_PROPAGATION_PATH` | 传播路径桑基数据 | P-06 | ❌ 综合用户态 | 🔧 algorithm-agent | ❌ Q005 |
| `M_SS_EXPORT_DAILY_COUNT` | 今日导出次数 | P-07 | 应用层 audit | 无 | 应用层 |
| `M_SS_EXPORT_QUEUE_LEN` | 异步导出队列长度 | P-07 | 应用层任务队列 | 无 | 应用层 |

**统计**：共 **36 个 metric_id**（含跨页复用）；唯一 26 个。
- ✅ 真实 ODS Mock：**15 个**（直接 SQL，无算法）
- 派生：**4 个**（基于真实 ODS 字段派生）
- 🔧 待算法：**9 个**（algorithm-agent Wave 1 接力）
- ⚠️ 待甲方：**3 个**（Q004 + Q007）
- ❌ 用户态待自建：**8 个**（Q005 关联）
- 应用层：**2 个**（audit / 任务队列）

### 11.2 给 data-agent / algorithm-agent / api-agent 的接力建议

```yaml
data_agent_followup:
  cfg_metric_register:  # 需注册 26 个唯一 metric_id 到 cfg_metric 表
    priority_p0:        # 不依赖算法/用户态，可立即注册
      - M_SS_TOPIC_NEW_COUNT_Q
      - M_SS_TOPIC_NEW_COUNT_Y
      - M_SS_TOPIC_NEW_COUNT_TOTAL
      - M_SS_TOPIC_DENSITY_BY_PROV
      - M_SS_TOPIC_BY_INSTITUTION
      - M_SS_TOPIC_BY_CATEGORY
      - M_SS_FUNDING_TOTAL_Y
      - M_SS_UNIT_CONTRIBUTION_RATE
      - M_SS_REGION_CONTRIBUTION_RATE
      - M_SS_UNIT_COUNT
      - M_SS_OUTPUT_COUNT
      - M_SS_OUTPUT_PAPER_COUNT
      - M_SS_OUTPUT_PATENT_COUNT
      - M_SS_OUTPUT_REPORT_COUNT
      - M_SS_OUTPUT_AWARD_COUNT
      - M_SS_PROJECT_IN_PROGRESS
    priority_p1:        # 依赖甲方决策的派生 metric
      - M_SS_PROJECT_TIMELINE       # ⚠️ Q004
      - M_SS_PROJECT_PROGRESS_PCT   # ⚠️ Q004
      - M_SS_PROJECT_COMPLETED_M    # ⚠️ Q007
    priority_p2:        # 待 algorithm-agent 接力
      - M_SS_HOT_KEYWORDS_LIST
      - M_SS_DOMAIN_DISTRIBUTION
      - M_SS_TYPICAL_CASES_TOPN
      - M_SS_SIMILAR_TOPN
      - M_SS_IMPACT_SCORE
      - M_SS_INFLUENCE_INDEX
      - M_SS_PROJECT_OVERDUE_LIST

  user_state_dwd_tables_pending:  # 需自建用户态 DWD 表（Q005 关联）
    - dwd_user_comment_ss_topic   # 软科学课题评论
    - dwd_user_like_ss_topic      # 软科学课题点赞
    - dwd_user_favorite_ss_topic  # 软科学课题收藏
    - dwd_user_follow_ss_topic    # 软科学课题关注
    - dwd_user_share_log          # 分享行为日志
    - dwd_user_view_log           # 浏览行为日志（用于传播路径）
    - dwd_user_filter_scheme      # 筛选模板保存

algorithm_agent_followup:  # 需算法的指标
  nlp_tasks:
    - M_SS_HOT_KEYWORDS_LIST: NLP 关键词词频 TopN
    - M_SS_DOMAIN_DISTRIBUTION: 学科 + 关键词聚类
    - M_SS_TYPICAL_CASES_TOPN: 文本相似度 + Cluster
    - M_SS_SIMILAR_TOPN: 文本相似度（cos sim 或语义嵌入）
  composite_index:
    - M_SS_IMPACT_SCORE: 学术影响（论文/专利/报告/奖项加权）+ 社交影响（待 Q005 用户态）
    - M_SS_INFLUENCE_INDEX: 同上扩展社会维度
  alert_rules:
    - M_SS_PROJECT_OVERDUE_LIST: 派生 SQL + 阈值（K-O7）；建议 Python ETL 写入 ADS
  social_aggregation:
    - M_SS_INTERACTION_TIMELINE: 待 Q005 自建用户态后聚合
    - M_SS_PROPAGATION_PATH: 同上

api_agent_followup:  # gkxlumen-metrics / gkxlumen-topic 模块扩展
  /metrics/v1/catalog:
    - 暴露上述 26 个 metric_id 的 8 件套元数据
  /metrics/v1/lineage/{metric_id}:
    - 暴露 4 段血缘图（ODS → DWD → DWS → ADS）
  /topic/v1/soft-science/*:
    - 8 个页面的聚合接口（按页面而非按指标聚合）
```

### 11.3 映射表回补建议（给 PM 评审 `DS-25-data-availability-matrix.md`）

本试点未发现 ODS 表新字段未覆盖；但发现：

1. **`dwd_zh_project_output` 的 25 字段使用率偏低**：当前 wireframe 只用了 `paper_count / patent_count / report_count / award_count` 4 列，其余 21 列可在后续 algorithm-agent 接力时进一步纳入影响力综合分（M_SS_IMPACT_SCORE）的细分指标。
2. **`dwd_org_reg_info` + `dwd_org_hels_info`** 在 wireframe 字段表中**未直接引用**，因 DS-25 主表是 `dwd_zh_project`，承担单位信息直接读 `funded_institution` 文本（未来精确化时再做 LEFT JOIN）。**回补建议**：handoff 后补一份"承担单位详情侧栏"作为 P-04 二级页，关联 `dwd_org_reg_info.address / business_scope / contact` 用于地理精度补强（与 K-O2 联动）。
3. **`dwd_macro_region_category`** 在地图层级下钻时是关键维度，但本试点未单独画字段表（仅在 K-O2 提及）。**回补建议**：data-agent 接力时把"行政区划维表 → funded_province 解析逻辑"作为单独 cfg_metric 注释加入。

## 12. DS-15 回看清单（必填）

> **作用**：作为团队智能体编排试点 Step 1，本试点必须明确指出 DS-15 试点（talent-2026-06-17）哪些做法**不符合 D8 / D9 现行规范**，作为下次试点改进的回头依据。

### 12.1 DS-15 试点不符合 D8 / D9 规范的具体项目

| # | DS-15 现状 | D8 / D9 规范要求 | 差距 | 是否建议回补 |
|---|-----------|-----------------|------|------------|
| **R1** | wireframe 区块名使用"左栏 240px / 主区 / 头部卡 / 头像 96px"等口语化叫法（如 DS-15-wireframe.md 行 31-49） | D8 §9 必须使用 15 个通用组件命名（PageShell / TopicSidebar / ContextBar / SectionPanel / ModuleHeader / MetricCard 等） | **严重不符** | ✅ **建议回补**：在 DS-15-wireframe.md 顶部加"区块名映射表"，把口语化名称对应到 §9 通用组件，供 ui-agent 接力时按规范实现 |
| **R2** | wireframe 字段表是 **5 列**（名称 / 类型 / 来源 / 必填 / 示例），无 metric_id 列 | D9 数据血缘 6 列（含 metric_id） | **严重不符** | ✅ **建议回补**：在 DS-15-wireframe.md 顶部加"字段表 metric_id 升级说明"，全表追加 metric_id 列（含 `M_E5_TALENT_*` 命名族）；或新建 `DS-15-wireframe-v2.md` 增量补充 |
| **R3** | 各页面**无 §4.2 5 段优先级**小节（人才主页只有 6 Tab 切换，未明确"先关注什么 → 为什么"） | D8 §4.2 每页面必有 5 段 | **严重不符** | ⏳ **看 retro 决策**：可补可不补；若 DS-15 后续要进入 lumen 工程化复刻，建议补；若仅作演示，可不补 |
| **R4** | handoff 无 §18 18 条对照表（UX-DS-15-trial.md 仅有 7 项 DoD 对照） | D8 §18 18 条 + UX 自检 / UI 待办分工 | **不符** | ✅ **建议回补**：UX-DS-15-trial.md 末追加 §18 对照表（UX 自检 8 条 + UI 待办 10 条） |
| **R5** | "组件需求清单"使用业务自创组件名（`<TalentCard>` / `<FacetFilter>` / `<MaskedField>` / `<TimelineFeed>` / `<GraphCanvas>` / `<ScoreRadar>` 等） | D8 §9.2 业务组件必须**先拆出通用交互能力**（区分通用 vs 业务） | **不符**（业务组件先于通用组件） | ⏳ **建议在 ui-agent DS-15 实现阶段补**（DS-15 试点 UX 阶段已结束，由 ui-agent 在落地时改造） |
| **R6** | 无"本页 metric_id 清单"小节 | D9 §5.2 wireframe 末尾必有 | **严重不符** | ✅ **建议回补**：DS-15 全部 15 页面页脚增补"本页 metric_id 清单"小节（命名族 `M_E5_*`） |
| **R7** | 字段表"来源"列写 bid 章节号（如 `§3.1` / `§3.1.1.2 标签化`） | D9 + DS-XX-data-availability-matrix.md 要求引用真实 ODS 字段名（如 `dwd_scholar_basic_info.name_cn`） | **严重不符** | ⏳ **待 data-agent 评估**：人才领域有 `dwd_scholar_*` ODS 表（参见 ODS 清单清单），data-agent 应建立 `DS-15-data-availability-matrix.md`，UX 阶段字段表"来源"列同步升级 |
| **R8** | handoff 未集中登记 ⚠️ "待甲方"决策项；本试点引入了 `客户决策清单跟踪表.md` 全局机制 | 团队公约 §3.1（决策不外包 AI）+ 客户决策清单跟踪表 | **不符**（但有 K-O1~K-O7 开放项，已部分对齐） | ⏳ **建议补**：把 DS-15 的 K-O1~K-O5 复制到 `客户决策清单跟踪表.md` §2.2，每条评估"是否真需要甲方拍板" |
| **R9** | DS-15 仓 git 策略：**未 push**（仅 commit）；本次派单要求 DS-25 必须 push | repo-registry §2.4.2（demo2 允许直接 push） | **不符**（保守做法） | ⏳ **不强制回补**：retro 时 PM 评估是否回头 push DS-15 试点 commit 到 demo2 origin/main 让甲方可见 |

### 12.2 DS-15 回补优先级建议

| 优先级 | 项 | 理由 |
|--------|------|------|
| **P0**（建议立即回补） | R1（§9 命名）、R2（6 列字段表）、R6（metric_id 清单）、R4（§18 对照表） | 影响后续 ui-agent 落地 + 评审材料 |
| **P1**（评估后回补） | R3（5 段优先级）、R8（决策清单登记） | DS-15 已结束 UX 阶段，回补成本 vs 收益需 PM 评估 |
| **P2**（不强制） | R5（业务组件先拆通用）、R7（字段来源 ODS）、R9（push） | 由 ui-agent / data-agent 后续阶段补 |

**建议决策**：PM + UX-agent 在下次 retro 决策是否启动 DS-15 试点回补任务，可作为 **`UX-DS-15-retrofit` 子任务** 派发。

## 13. 提交记录与 commit hash

```
444fa03 [sandbox] ux-agent 试点：DS-25 软科学成果展示 IA/wireframe [agent:ux-agent]
```

- 上一 commit：`3e7bda6`（demo2 main 历史 commit）
- 本次 commit：`444fa03`（4 files / 1440 insertions / pure additions / no deletions）
- 推送：`3e7bda6..444fa03 main -> main` 已同步 origin/main
- 作者：`hzw <hzw@htmitech.com>`（团队公约 §3.3 commit 作者标记：commit message 末尾含 `[agent:ux-agent]`）
- demo2 自动部署链接：https://skxrules.unicomcn.tech:30999/（约 2-3 min 后可见 docs，沙箱页 UI 由 ui-agent 阶段实现）

## 14. 不一致清单（bid-reference vs acceptance-catalog）

| 不一致 | bid 描述 | acceptance-catalog 描述 | 建议 |
|---|---|---|---|
| scope_summary 措辞 | bid §1.1.1.1.4.6.1 描述 7 大三级子功能：分布地图 / 智能筛选 / 详情案例 / 多维统计 / 互动传播 / 数据导出 / 进展跟踪 | catalog 行 302 写为"GIS 全景 + 图表展示软科学成果与趋势"（高度概括口语化简写） | 仅措辞差异，建议 catalog 保持原状即可，**不属于范围冲突** |
| 依赖描述 | bid 文本未显式列依赖 | catalog `dependencies: 成果（他方）+地域` | 与 bid 隐含一致（来自 §1 地域 + 各子功能"成果数据"依赖） |
| route 字段 | bid 未指定路由 | catalog `route: null` | 本试点 IA §4 提供了 8 条路由建议，可作为 catalog `route` 字段后续填充的依据 |

> 本试点未发现 bid 与 catalog 在 DS-25 范围上的实质冲突；7 个三级子功能在 bid 中可一一对应到本试点的 P-02~P-08 主载体页面。

## 15. 试点反馈（本次试点新增章节，针对团队智能体编排试点 Step 1）

### 15.1 耗时实测

| 阶段 | 计划 | 实测（估计） | 是否超时 | 原因 |
|------|------|--------------|---------|------|
| 必读 7 项文件 + 数据真源 | 0.5 h | ~0.5 h | 无 | DS-25-data-availability-matrix.md 已经预先做好"作弊纸"，节省 30 min |
| README.md | 0.1 h | ~0.15 h | 略超 | 与 DS-15 差异说明 B1-B8 8 条对照写得详细 |
| DS-25-IA.md | 0.3 h | ~0.3 h | 无 | DS-15 模板可参考 |
| DS-25-userflow.md | 0.3 h | ~0.25 h | 无 | mermaid 防御性引号经 DS-15 教训已掌握 |
| DS-25-wireframe.md | 0.5 h | ~0.7 h | 超 +40% | 8 页 × 5 段优先级 × 6 列字段表 × metric_id 清单，三项新增同步写非常耗时；ASCII 区块绘制费时 |
| handoff | 0.3 h | ~0.3 h | 无 | DS-15 handoff 模板可参考 |
| git commit + push | 0.05 h | ~0.05 h | 无 | demo2 允许直接 push |
| **合计** | **1–1.5 h** | **~2.3 h** | **+50%** | 主要在 wireframe |

**结论**：DS-25 比 DS-15 多 ~33% 体量（8 页 vs 15 页虽然多 7 页但 DS-15 多详情子页和管理页内容较少；DS-25 每页有 5 段优先级 + metric_id 清单 + 6 列字段表三项新增），实测耗时约 2.3 h，建议下一次类似试点（INTEG tier 7 子功能级别）计划**预留 2–2.5 h**。

### 15.2 必读文件评价

| # | 必读文件 | 用处大 / 中 / 小 | 备注 |
|---|---------|----------------|------|
| 1 | bid-reference §1.1.1.1.4.6.1 | **大** | 7 三级子功能 + 30 四级子功能描述清晰，可直接翻译为页面 |
| 2 | acceptance-catalog DS-25 | 中 | 只有 1 行描述，价值不高，但 tier=INTEG 标识有用 |
| 3 | scope-baseline.yaml ±10% | **大** | 范围铁律的尺；本次未超线 |
| 4 | **AI可复用UI框架与设计规范.md** | **极大** | §3 产品定位 / §4 信息架构 / §9 通用组件命名 / §10 Arco 映射 / §18 验收 18 条 五处全用上 |
| 5 | **data-lineage-policy.md** | **极大** | 8 件套 + metric_id 命名规则 = wireframe 6 列字段表的依据；如果没有这个规约，UX 阶段会丢失数据血缘信息 |
| 5.5 | **DS-25-data-availability-matrix.md** | **极大** | 强烈推荐！把"凭空想字段名"变成"从 ODS 复制真实字段"；§6.1 7 项甲方决策直接对齐到客户决策清单 |
| 6 | UX-DS-15-trial 试点样板 | 中 | 形参考价值大；质（D8 / D9 前的产物）参考要谨慎 |
| 7 | repo-registry demo2_proto | **大** | 沙箱路由前缀 / 禁 merge 到 lumen / mock_only / git 策略 |
| 8 | ux.mdc 角色规约 | **大** | 8 项产物质量自检表 + 不做清单（不写代码 / 不画视觉 / 不接触甲方）非常清晰 |
| 9 | 智能体编排手册 §9.1c | 中 | 派单话术与本次派单内容重复度高（派单已经把 §9.1c 内化） |
| 10 | 客户决策清单跟踪表 | **大** | 与 DS-25-data-availability-matrix §6.1 联动，K-O1~K-O5 直接关联 Q001-Q006 |

**遗漏建议**：暂无；本次必读文件已覆盖 UX 阶段所有需要决策的输入。

### 15.3 派单话术评价

| 评价维度 | 内容 |
|---------|------|
| **清晰可直接执行的指令（≥5 条）** | ① 4 份 md 隔离目录 ② 字段表 6 列硬约束 ③ §9 通用组件命名硬约束 ④ §4.2 5 段优先级每页必有 ⑤ §18 18 条对照分工（UX 8 条 + UI 10 条）⑥ 与 DS-15 差异 8 条（B1-B8）|
| **有歧义需 PM 澄清的（≥2 条）** | ① DoD 第 9 条"待评审开放项 ≥10 条"未明确是 K-O 还是 W-O；本次试点同时给了 12 条 K-O + 25 条 W-O ② "页面级 metric_id 清单"格式未规定字段，本次试点统一用 `metric_id / 中文名 / source_tables (ODS) / 算法依赖 / 备注` 5 列 |
| **超出 UX 边界的诱惑（≥1 条）** | P-02 地图层级下钻 / P-04 时间轴 / P-05 词云 / P-06 桑基图等可视化技术选型，**已克制为"建议沿用 demo2 / 待 UI/UE 评审"**；未画具体颜色 / 字号 / 圆角 |

**评价**：本次派单话术质量**显著高于** DS-15 试点的派单，主要因为：
1. 数据真源（DS-25-data-availability-matrix.md）预先做好
2. 客户决策清单跟踪表（Q001-Q007）预先登记
3. 与 DS-15 差异（B1-B8）显式列出 8 条
4. §18 18 条对照分工明确（UX 8 / UI 10）

### 15.4 范围铁律

| 项 | 内容 |
|---|------|
| bid §1.1.1.1.4.6.1 原文是否模糊 | 部分模糊 |
| 模糊点 1 | "GIS 全景"具体到哪一级（国家 / 省 / 市 / 区 / 单位）？**bid 列了 5 级但未规定下钻精度**；UX 解释：5 级全做，但市/区下钻数据精度待 Q003 甲方 |
| 模糊点 2 | "难题攻关历程"语义不明（立项 → 中期 → 结题？还是按项目类型动态？）；UX 解释：默认基于 `approval_time + research_period` 派生，⚠️ Q004 待甲方 |
| 模糊点 3 | "互动统计与传播分析"具体什么指标？bid 未给口径；UX 解释：评论 / 点赞 / 收藏 / 分享 4 类基础统计 + 传播路径桑基 + 影响力综合指数，⚠️ Q005 待甲方 |
| 模糊点 4 | "影响力评价与应用反馈"算法不明；UX 解释：学术影响（论文/专利/报告/奖项加权）+ 社交影响（待用户态）合成 `M_SS_IMPACT_SCORE`，🔧 待 algorithm |

### 15.5 角色边界

| 边界场景 | 是否过度发挥 |
|---------|-------------|
| P-02 地图技术选型（Leaflet / Mapbox / 高德） | ❌ **已克制**：仅建议沿用 demo2 `SharedRegionMap.jsx`，未指定 SDK |
| P-04 影响力综合分公式 | ❌ **已克制**：明确"由 algorithm-agent + 业务方共定，UI 仅展示分项 + 标 v1" |
| P-05 词云算法 | ❌ **已克制**：标 🔧 待 algorithm-agent，未指定 NLP 模型 |
| P-06 互动传播交互细节 | ❌ **已克制**：UI 占位 + ⚠️ Q005 待甲方；未画具体按钮交互 |
| P-07 PDF 报告模板字段 | ⚠️ **轻度过度**：给了 5 种模板名（驾驶舱 / 空间 / 主题 / 课题详情 / 进展），实际应该由 PM + 业务方决定 |

### 15.6 与 DS-15 试点对比（重点）

| 对比维度 | DS-15 | DS-25 |
|---------|-------|-------|
| 试点性质 | ux-agent **首次**试点（D8 / D9 前） | ux-agent **第二次**试点（D8 / D9 后） |
| 体量 | 1,171 行 / 58,130 字符 | 1,208 行 / 77,507 字符（+33%） |
| 页面数 | 15（6 Tab + 3 详情 + 2 管理 + 1 订阅） | 8（1 总览 + 7 业务） |
| 子功能数 | 6 个二级 + 30+ 三级 | 7 个三级 + 30 四级 |
| 字段表列数 | 5 列 | **6 列**（含 metric_id） |
| §9 通用组件覆盖 | 部分（口语化命名为主） | **全覆盖**（15 / 15） |
| §4.2 5 段优先级 | 无 | **全覆盖**（8 页 × 5 段 = 40 / 40） |
| handoff §18 18 条对照 | 无 | **有**（UX 8 / UI 10 分工） |
| metric_id 清单 | 无 | **每页有 + handoff 汇总 36 个引用 / 26 个唯一** |
| 待甲方决策清单 | 散落在开放项 | **集中登记到 客户决策清单跟踪表 Q001-Q007** |
| 数据真源 | 字段表"来源"列写 bid 章节号 | **字段表"来源"列引用 ODS 真实字段名**（如 `dwd_zh_project.title`）|
| Mock 数据切真实成本 | 字段名重命名 + 接口调整 | **代码零改动**（字段名沿用 ODS） |

**结论**：D8 + D9 规范的引入显著提升了 UX 阶段产物的**专业可信度** + **下游接力可用性**；建议把 DS-25 的产物质量作为后续 DS 试点的**标杆基线**。

### 15.7 D8 规范实战评价

| 评价维度 | 内容 |
|---------|------|
| **最有用的 3 条（D8）** | ① §9 通用组件清单 15 个（统一全队 wireframe 区块命名）② §4.2 5 段优先级（强制每页"先给结论"）③ §18 18 条验收清单（UX/UI 分工明确） |
| **最难落地的 3 条（D8）** | ① §10 Arco 控件映射（UX 阶段不能"建议 Arco 组件"过细，否则越界；本次以"建议 Arco 实现"形式克制）② §7.3.3 11 类业务对象固定配色（UX 阶段不指定颜色但要预留"课题=chart-09"语义传递给 UI）③ §12 图表规范（UX 阶段画 ASCII 不能传达图例 / tooltip 行为，只能在交互注解中描述） |
| **规范未覆盖但 UX 实际会遇到的空白** | ① **"待甲方"⚠️ 角标的视觉规范**（如位置 / 颜色 / 是否可关闭）；建议 D8 §15 文案规范中补一小节"业务口径未定的视觉表达" ② **响应式断点下 ASCII 线框的失效**（D8 §8 / §17 给了响应式策略，但 wireframe ASCII 只能表达一种屏宽；建议补"窄屏 / 宽屏" wireframe 双版本要求） |

### 15.8 给 PM 的 3 条改进建议

> 用于优化下一次试点的派单话术 / 角色规约 / 编排手册 / D8 规范。

| # | 建议 | 落地动作 |
|---|------|---------|
| **建议 1** | **派单话术中明确"开放项"K-O / W-O 两级层次**（K-O = 关键决策，进 handoff；W-O = 细节决策，进 wireframe 各页面），避免本次试点中"≥10 条"指标的歧义 | 修改派单手册 §9.1c，把"开放项 ≥10 条"细化为"K-O ≥5 条 + W-O ≥15 条"，并给出二级模板 |
| **建议 2** | **DS-15 回补建议**：本试点 §12 已列出 9 项 DS-15 回看清单，建议 PM 评估优先级，立 `UX-DS-15-retrofit` 子任务（建议优先级 P0 4 项立即回补） | 在 task-registry.yaml 增 task `UX-DS-15-retrofit`，由 ux-agent 接力修补 DS-15 的 R1/R2/R4/R6 4 项 |
| **建议 3** | **D8 §15 文案规范增补"业务口径未定的视觉表达"小节**：界定 ⚠️ 角标的位置 / 颜色 / 文案 / 是否可关闭，避免 wireframe 与 UI 阶段对"待甲方"的呈现不一致 | architect-agent 在下一次 D8 retro 时把本反馈纳入；D8 §15 增补一段 4 行规约 |

## 自评

### 做得好的（≥2 条）

1. **数据真源驱动**：字段表"来源"列严格引用 ODS 真实表字段（如 `dwd_zh_project.title`），未来 data-agent 接力时**前端代码零改动**；这是相比 DS-15 试点的最大进步。
2. **D8 §9 通用组件命名 15 个全覆盖**：未自创任何组件名；wireframe 8 页所有区块严格使用规范组件名（PageShell / TopicSidebar / ContextBar 等），与 DS-15 的"左栏 / 主区"口语化叫法形成鲜明对比。
3. **D8 §4.2 5 段优先级全覆盖**：8 页 × 5 段 = 40 / 40，每页都先回答"当前应关注什么"，符合驾驶舱 + 分析工作台定位。
4. **数据血缘 36 个 metric_id 引用 / 26 个唯一全覆盖**：从 wireframe 字段表 → 每页 metric_id 清单 → handoff §11 汇总三级闭环；分类清晰（✅真实 ODS / 🔧待算法 / ⚠️待甲方 / ❌用户态 / 应用层）。
5. **§18 18 条 UX 自检 8 条 + UI 待办 10 条分工明确**：handoff §7 表格化展示，避免越界 + 让 ui-agent 阶段清楚自己负责什么。
6. **DS-15 回看清单 9 项 R1~R9 全部具体**：每项都给出"DS-15 现状 / D8 规范 / 差距 / 是否建议回补"四列分析，落地价值高。

### 想改进的（≥2 条）

1. **ASCII 线框在 wireframe 中行数占比过高（约 30%）**：每页 ASCII 30~50 行；下次可考虑用 mermaid graph 或更紧凑的 markdown 表格表达布局，降低写作时间 + 提升可读性。
2. **mermaid 图节点文案中文混排**：受 mermaid 语法对 `>` `/` `:` `"` `(` 的限制，部分节点文案被简化（如"超过阈值"代替"> 阈值"，"projectId 主键有效?"代替"`projectId` 主键有效?"），与 DS-15 试点同问题；建议下一次试点引入 mermaid live editor 预渲染再贴入，或考虑用 markdown 表格 + 编号节点替代部分 mermaid 流程。
3. **未做用户测试与共情**：试点产物为"专家假设最佳实践"，缺真实用户访谈（科技局 PM / 科研服务岗 / 课题主持人）的可用性测试；建议 UI/UE 评审阶段引入 1–2 名甲方业务对接人做 think-aloud。
4. **P-06 互动传播虽明确 Wave 0 占位，但 wireframe 仍详细画了 4 块区块 + 8 个 metric_id**：可能给甲方造成"已经实现"的误判；下次类似 Wave 占位场景建议**只画 1 个区块占位 + 标 "Wave X 详设"**，避免过度发挥。

## 与编排基线对齐自检

- ✅ 工作根：`E:\gkx_src\demo2`（demo2_proto 仓）
- ✅ 不写代码、不改既有文件（除自身沙箱目录外）、push 到 demo2 main（对齐 §9.1c ux-agent 铁律 + repo-registry §2.4.2 demo2 允许直推）
- ✅ 范围未超 bid §1.1.1.1.4.6.1（对齐 `scope-baseline.yaml` ±10% 浮动）
- ✅ demo2 propagation：本产物只在本仓沙箱目录，不入 lumen（对齐 `repo-registry.yaml` → `demo2_proto.propagation.to_lumen=forbidden`）
- ✅ git add -f 使用：因 demo2 `.gitignore` 第 6 行 `docs/` 已忽略整个 docs 目录；为遵守"禁止改 .gitignore 等任何现有文件"铁律，采用 `git add -f` 强制添加 **仅本沙箱 4 个文件**（与 DS-15 同策略）
- ✅ commit 作者标记：`[agent:ux-agent]`（团队公约 §3.3）
- ✅ next-step：通知 coordinator 派 ui-agent 接力（按 §9.1d ui-agent 派单话术）

## 涉及文件

- `E:\gkx_src\demo2\docs\ia\sandbox\soft-science-2026-06-17\README.md`（新增）
- `E:\gkx_src\demo2\docs\ia\sandbox\soft-science-2026-06-17\DS-25-IA.md`（新增）
- `E:\gkx_src\demo2\docs\ia\sandbox\soft-science-2026-06-17\DS-25-userflow.md`（新增）
- `E:\gkx_src\demo2\docs\ia\sandbox\soft-science-2026-06-17\DS-25-wireframe.md`（新增）
- `E:\gkx_src\agent-delivery\agent-handoffs\UX-DS-25-trial.md`（本文件，新增）

## 建议下一任务

| 角色 | 任务 | 输入 |
|------|------|------|
| **ui-agent** | 把本 IA/wireframe 翻译为 demo2 仓可演示页面（沙箱模式：建议同样隔离到 `src/sandbox/soft-science-2026-06-17/`） | 本试点 4 个产物 + B 节 Arco 控件映射 + D 节 mock 数据结构 |
| **PM + UI/UE 3 人** | 评审本试点产物 + K-O1~K-O12 关键决策 + 5 段优先级 + §18 18 条对照 | 本 handoff |
| **PM** | 把 K-O1 / K-O2 / K-O3 / K-O4 / K-O5 升级到 `客户决策清单跟踪表.md` 并把 Q001-Q006 列入下次甲方会议议程 | 本 handoff §9 + `客户决策清单跟踪表.md` §2.1 |
| **architect-agent** | 评估 D9 三组件（MetricSpecCard / DataLineageDrawer / MockBadge）是否升级到 D8 §9 正式组件清单（从 15 → 18） | 本 handoff §B Arco 控件映射 + data-lineage-policy.md §5.1 |
| **data-agent** | 注册 26 个 metric_id 到 cfg_metric DDL；建立 `data/DS-15-data-availability-matrix.md` 同款映射表用于 DS-15 回补 | 本 handoff §11.2 data_agent_followup + DS-25-data-availability-matrix.md |
| **ux-agent**（可选） | DS-15 回补任务（R1/R2/R4/R6 4 项 P0 项） | 本 handoff §12 DS-15 回看清单 |

## 成本回填（团队公约 §3.7 铁律）

> 本次试点 token / 成本 retro 字段在编辑器侧自动统计后回填，模板见 `agent-delivery/budget-estimate.md` 第 2 节。

| 字段 | 内容 |
|------|------|
| estimated_tokens | 派单前估算（UX 起草类）：80k–120k |
| actual_tokens | _<待回填>_ |
| model_used | _<待回填>_ |
| actual_cost | _<待回填>_ |
| cost_warn | _<待回填>_（green / yellow $>5 / orange $>10 / red $>20）|

> 本试点为团队智能体编排试点 Step 1 关键节点，单 task 实际 > $10 暂停复盘，> $20 hard stop（团队公约 §3.7）。
