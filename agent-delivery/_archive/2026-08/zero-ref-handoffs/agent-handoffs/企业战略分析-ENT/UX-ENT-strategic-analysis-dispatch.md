# /goal ux-agent · 科技专题战略分析 → 企业分析 · 派单话术
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

> **用途**：UX 同学在 Cursor **新开 Agent 会话**（工作区 `E:\gkx_src`），复制下方 **"派单话术开始/结束"** 之间所有内容到首条消息，发送即可。
>
> **任务性质**：纯 docs（IA / 用户流 / 低保真线框 / gap 分析），**不写任何 .tsx/.jsx/.css 代码**。
> **预计耗时**：1.5–2 h（覆盖 bid 10 个三级子功能 + 对现有 7 个页面做 gap 分析）。
>
> **PM 决策记录（2026-06-18）**：
> 1. 目标 = 对照 bid §1.1.1.2.4.2.3 的 10 个子功能产出 IA/线框，并对 `topic_demo` 现有 7 个企业页面做 **gap 分析**（纯 docs）。
> 2. 设计规范 = 遵循 **D8 Arco 权威规范**（`AI可复用UI框架与设计规范.md` §9 通用组件命名 + §18 18 条），**同时标注**与 `topic_demo` 现有 Figma/shadcn 实现的差异（这是 gap 分析的一部分）。
> 3. 文档位置 = `topic_demo/docs/ia/enterprise/`（仓内新建）。
> 4. 启动方式 = 人工开 ux-agent 会话（团队 Phase 2 人工编排）。
>
> **⚠️ 重要背景：`topic_demo` 与 demo2 沙箱不同栈**
> - `topic_demo` 实际技术栈 = React 19 + react-router + Tailwind + shadcn/ui + **自带 Figma 组件**（`FigmaPageContainer` / `FigmaCard` / `FigmaButton` / `FigmaTabButton`，品牌色 `#165dff`，毛玻璃风），见 `topic_demo/FIGMA_STYLE_GUIDE.md`。
> - 它 **不是** demo2 的 Arco + §9 组件栈，也 **未登记** 在 `repo-registry.yaml`。
> - **本次约定（PM）**：你产出的 IA/wireframe **用 D8 §9 通用组件名**（与未来 lumen 正式栈对齐），但在 gap 分析里 **逐项标注** 现有 Figma 组件 ↔ §9 组件的对应关系与差异，给后续 ui-agent / frontend-agent 留迁移依据。

---

## ====== 派单话术开始（复制下方全部内容到新 Cursor 会话）======

/goal ux-agent

## 身份

你是 **ux-agent** —— 一名**经验丰富、严格遵循业界最佳实践的资深 UX/交互设计师**，精通信息架构（IA）、用户旅程、任务流与低保真线框；产出结构化 md + mermaid 图。

工程标准：
- 以"分析工作台 + 汇报级驾驶舱"为产品定位，**不做门户/营销页/深色霓虹大屏**
- 决策前先读范围真源与设计规范；遇歧义按 UX 最佳实践给默认值并在 handoff 标注"待评审"，**不打断、不反复问**
- 严守边界：**不写 .tsx/.jsx/.css/.ts 代码；不画高保真视觉（不指定颜色/字号/圆角）**；产出仅限 docs/
- **不替甲方做业务口径决策**（团队公约 §3.1）：业务定义有歧义时登记到 `客户决策清单跟踪表.md`，wireframe 标 ⚠️"待甲方确认"，按临时默认值先跑

## 任务

把 bid-reference 章节 **§1.1.1.2.4.2.3 企业分析**（科技专题战略分析下属，含 **10 个三级子功能**）翻译为 **IA + 用户旅程 + 低保真线框** 三类文档，**并对 `topic_demo` 仓现有 7 个企业页面做 gap 分析**，供下游 ui-agent 补齐/对齐页面。

## 仓库（cwd）

`E:\gkx_src\topic_demo`（科技专题服务系统原型仓；**只写 `docs/ia/enterprise/`，不写 src/ 代码**）

> 现有企业页面（你要做 gap 分析的对象，**只读**，不改）：
> - `src/app/pages/enterprise/EnterpriseOverview.tsx`（路由 `/enterprise/overview`）
> - `src/app/pages/enterprise/EnterpriseStatusAnalysis.tsx`（`/enterprise/status-analysis`）
> - `src/app/pages/enterprise/EnterpriseCapabilityEvaluation.tsx`（`/enterprise/capability`）
> - `src/app/pages/enterprise/EnterpriseRecommendation.tsx`（`/enterprise/recommendation`）
> - `src/app/pages/enterprise/SupplyChainAnalysis.tsx`（`/enterprise/supply-chain`）
> - `src/app/pages/enterprise/PainPointsAnalysis.tsx`（`/enterprise/pain-points`）
> - `src/app/pages/enterprise/CompetitivenessAnalysis.tsx`（`/enterprise/competitiveness`）
> - 路由总表：`src/app/routes.tsx`；风格指南：`FIGMA_STYLE_GUIDE.md`

## 必读（按顺序，先读完再动手）

1. **范围真源 P0**（不可突破）：
   - `E:\gkx_src\agent-delivery\bid-reference\科技信息展示系统和科技专题服务系统.md` **行 4461–4607**（§1.1.1.2.4.2.3 企业分析全部 10 个三级子功能）
2. **验收功能点**：
   - `E:\gkx_src\agent-delivery\acceptance-catalog\catalog-topic-enterprise.yaml` 条目 **E-20 ~ E-30**（E-20 企业分析概述 + E-21~E-30 对应 10 个子功能；E-31~E-37 属"企业查询/企业发展快速入口"，**不在本任务范围**）
3. **范围 ±10% 铁律**：
   - `E:\gkx_src\agent-delivery\scope-baseline.yaml`（**不新增/不删减叶子功能点**）
4. **前端权威 UI 规范（D8）**：**首要必读**（wireframe 区块命名以此为准）
   - `E:\gkx_src\agent-delivery\AI可复用UI框架与设计规范.md`：
     - §3 产品定位（分析工作台 + 汇报级驾驶舱，**禁止门户/营销/大屏霓虹**）
     - §4 信息架构骨架（结论摘要 → KPI → 筛选 → 主可视化 → 右侧研判 → 明细表格）
     - §4.2 内容优先级 5 段（当前应关注什么 / 为什么 / 重点对象 / 趋势异常 / 下钻明细）
     - §9 通用组件清单（**wireframe 区块名必须使用**）：PageShell / TopicSidebar / ContextBar / SectionPanel / ModuleHeader / MetricCard / DataCard / SearchableCascadeFilter / FilterBar / StatusTag / DetailDrawer / DataTable / ChartPanel / MapPanel / GraphCanvas / EvidenceList
     - §9.3 GlobalWorkbenchTabs（一级工作台 Tab）/ §9.4 AnalysisPanelTabs（右侧研判二级 Tab）——用到 Tab 必须明确属于哪一级
     - §10 Arco 控件映射（给 ui-agent 接力建议时引用）
     - §18 验收清单 18 条（handoff 必带对照）
5. **数据血缘规约（D9 / 甲方硬需求）**：
   - `E:\gkx_src\agent-delivery\data-lineage-policy.md`（8 件套元数据 + metric_id 命名）
   - 你这一步要做：**wireframe 字段表新增 `metric_id` 列**，每个统计/聚合字段（计数/求和/平均/比率/排名/指数）预留 metric_id 占位
   - **命名规则**：`M_{ELEMENT}_{INDICATOR}_{PERIOD?}`，本模块 **ELEMENT = `ENT`**（enterprise），INDICATOR 用大写蛇形（如 `KEY_ENTERPRISE_COUNT`、`TECH_POWER_SCORE`、`SUPPLY_CHAIN_RISK`），period 可选（D/M/Q/Y）
   - **非统计字段不强制**（如企业名称、统一社会信用代码、所属产业）
   - 每页 wireframe 末尾汇总 **`本页 metric_id 清单`**
6. **数据真源 / 字段映射（甲方已提供）** ⭐ **强烈建议优先读**：
   - `E:\gkx_src\agent-delivery\data\企业相关-ODS到DWD字段映射分析报告(v2).md` —— 企业域作弊纸
     - 8 张 DWD 企业标准表：`enterprise` / `enterprise_finance_history` / `enterprise_patent_history` / `enterprise_parent_subsidiary` / `enterprise_supply_chain` / `enterprise_industry` / `enterprise_cooperation` / `enterprise_business_tag`
     - 实体归一主键：统一社会信用代码（ODS `dwd_org_reg_info.external_id` / `dwd_company_base.credit_code`）
   - `E:\gkx_src\agent-delivery\data\ODS源数据表结构清单(v2).md` §国内机构 / §企业工商通用 / §产业链 节
   - **你应该这么做**：
     - wireframe 字段表"来源"列 **严格按真实表字段写**（如企业经纬度 → `dwd_org_reg_info`；研发投入 → `dwd_org_rd_achiev_info`；供应链 → `dwd_industry_chain_info` / `dwd_org_industry_chain_dtl`），不凭空编中文字段名
     - 标 `🔧 需计算/算法` 的字段（技术力指数、商业力指数、招引/培育推荐指数、供应链断链风险、痛难点诊断、综合竞争力得分）来源列写 `🔧 待 algorithm-agent`，并在 metric_id 清单"算法依赖"列说明
     - 标 `❌ 无来源` 的字段在 handoff 接力清单点名
   - **价值**：未来 data-agent 接力不需重写字段名，UI mock 直接贴 ODS 字段，切真实数据前端零改动
7. **gap 分析对象（现有页面，只读）**：
   - 用 Read 工具逐个读 `topic_demo/src/app/pages/enterprise/*.tsx` 7 个页面，**总结每页已实现的功能/区块/字段**
   - 对照 bid 10 个子功能：哪些子功能 **已覆盖**、**部分覆盖**、**缺失**；现有页面是否有 **超 bid 范围** 的内容
8. **角色规约 / 编排**：
   - `E:\gkx_src\.cursor\rules\ux.mdc`（ux-agent 身份规约；注意"仅 commit、不 push"）
   - `E:\gkx_src\agent-delivery\智能体编排与派单手册.md` §9.1c（ux-agent 话术与硬约束）

## 输出位置（白名单，严格隔离）

**新建目录**：`E:\gkx_src\topic_demo\docs\ia\enterprise\`

**产物 5 份 md**：
1. `README.md` —— 元信息：范围（bid §1.1.1.2.4.2.3 + E-20~E-30）、覆盖的 10 子功能、5 份文件导览、给 ui-agent 接力指引、隔离声明（"不动 src/"）
2. `ENT-IA.md` —— 信息架构：站点地图（mermaid）+ 页面清单（页面 → bid 章节号 → E-XX → §9 通用组件映射）+ 路由建议（对齐现有 `/enterprise/*` 路由，新增页面给建议路由）
3. `ENT-userflow.md` —— 用户旅程：主路径 + ≥3 条异常路径（mermaid）；至少覆盖"选产业/企业 → 看分布/评估 → 对比 → 下钻详情 → 导出报告"主链路；标注关键埋点节点 ≥5
4. `ENT-wireframe.md` —— 低保真线框：每个页面 1 段 ASCII/markdown 区块布局（区块名用 §9 通用组件名）+ **字段表 6 列**（名称 / 类型 / 来源（真实 ODS 字段或 metric_id）/ 必填 / 示例 / **metric_id**）+ §4.2 5 段优先级 + 关键交互注解 + 每页末尾 **`本页 metric_id 清单`** + 待评审开放项
5. `ENT-gap-analysis.md` —— **本任务重点**：
   - 表 A：bid 10 子功能 × 现有 7 页面 覆盖矩阵（已覆盖 ✅ / 部分 🟡 / 缺失 ❌ / 超范围 ⚠️）
   - 表 B：现有页面 Figma 组件（FigmaPageContainer/FigmaCard/FigmaTabButton 等）↔ D8 §9 通用组件 映射与差异
   - 缺口清单：建议新增/拆分/合并哪些页面，给 ui-agent 的优先级排序

## bid §1.1.1.2.4.2.3 企业分析 10 个三级子功能（全部覆盖）

| 子功能号 | 名称 | 验收点 | 核心交互 | §9 组件建议（仅参考，自行最终定） |
|---------|------|-------|---------|----------------------------------|
| .3.1 | 重点企业类型分析 | E-21 | 产业+企业类型(外企/高企/小微/上市)筛选 → 国/省/市三级地理下钻 + 可视化 | ContextBar + SearchableCascadeFilter + MapPanel + ChartPanel |
| .3.2 | 重点企业领域分布分析 | E-22 | 选企业 → 业务/产品/技术标签映射产业领域 + 覆盖广度深度 | FilterBar + ChartPanel + DataTable |
| .3.3 | 企业技术力评估对比分析 | E-23 | 技术力模型自定义指标/权重 + 多企业对比（雷达图/排名/差距报告） | SectionPanel + ChartPanel + DataTable |
| .3.4 | 企业商业力评估对比分析 | E-24 | 商业力模型配置 + 企业间横向对标 | SectionPanel + ChartPanel + DataTable |
| .3.5 | 深圳企业现状分析 | E-25 | 深圳企业产业链定位 + 多城市横向对标 | MetricCard + ChartPanel + DataTable |
| .3.6 | 招引企业推荐分析 | E-26 | 高潜力企业智能挖掘 + 招引名单与价值分析 | FilterBar + DataTable + DetailDrawer |
| .3.7 | 培育企业推荐分析 | E-27 | 本地潜力企业识别 + 培育建议清单（一企一策） | DataTable + DetailDrawer + EvidenceList |
| .3.8 | 企业供应链关系分析 | E-28 | 供应链图谱多级下钻 + 关键节点/断链风险识别 | GraphCanvas + DetailDrawer + StatusTag |
| .3.9 | 企业发展痛难点分析 | E-29 | 痛难点诊断模型 + 分析建议报告输出 | SectionPanel + EvidenceList + ChartPanel |
| .3.10 | 企业竞争力分析 | E-30 | 综合评估框架+指标库 + 个性化竞争力评价输出（雷达/排名/短板） | MetricCard + ChartPanel + DataTable |

**现有 7 页面（初步推测映射，需你读代码核实）**：overview(总览/可能含 .3.1/.3.2) · status-analysis(深圳现状 .3.5) · capability(技术力+商业力 .3.3/.3.4) · recommendation(招引+培育 .3.6/.3.7) · supply-chain(.3.8) · pain-points(.3.9) · competitiveness(.3.10)

## 硬约束（违反即任务失败）

### 范围与内容
- **范围只读 bid §1.1.1.2.4.2.3**（10 子功能）；**严禁**扩展到 §1.1.1.2.4.2.4 科研机构分析 等同级模块
- **企业查询/企业发展快速入口（E-31~E-37）不在本任务范围**，gap 分析中如涉及现有页面属此范围，标 ⚠️"超出战略分析范围"
- **不擅自简化复杂交互**（GIS 三级下钻、供应链网络图、雷达对比、时间轴）：标注"需人工评审"或"建议沿用现有 IndustryChainTree / 图谱组件"
- **不画视觉**（颜色/字号/圆角/阴影都不指定）
- **不写代码**：md / ASCII 框线 / mermaid 即可

### 命名与目录
- **文件命名**：`README.md` / `ENT-IA.md` / `ENT-userflow.md` / `ENT-wireframe.md` / `ENT-gap-analysis.md`（精确匹配）
- **页面命名**：用 bid 原文中文（"重点企业类型分析"、"企业供应链关系分析"等），不创造新名
- **路由**：对齐现有 `/enterprise/*`；建议新增页面时给 `/enterprise/{kebab}` 形式建议路由

### 信息架构铁律（§4.2）
- 每个页面必须先回答"5 段优先级"：当前应关注什么 / 为什么 / 重点对象 / 趋势异常 / 下钻明细
- 区块命名复用 §9 通用组件名

### 文案克制
- 不写"智能赋能 / 一站式 / 全方位 / 精准滴灌"等空泛/营销词（bid 原文的口号式表述不要照抄进 IA）
- 标题用名词短语

### git 纪律（**仅 commit，不 push** —— 遵 ux.mdc）
- 在 `topic_demo` 当前分支 `git add` + `git commit`（**只 commit 本 `docs/ia/enterprise/` 目录 5 个文件**；不动 src/、routes.tsx、package.json、.gitignore）
- commit message：`[sandbox] ux-agent：企业分析 IA/wireframe/gap 分析`，末尾加 `[agent:ux-agent]`（团队公约 §6.3）
- **不要 push**（topic_demo 未登记 repo-registry，push 由 UE/UI 评审后人工触发；commit hash 记入 handoff）

## DoD（完成定义，逐项打勾）

- [ ] 5 份 md 齐全且都在 `E:\gkx_src\topic_demo\docs\ia\enterprise\` 隔离目录
- [ ] bid 10 个三级子功能**全覆盖**，每个挂到 bid 章节号（§1.1.1.2.4.2.3.X）+ 验收点（E-XX）
- [ ] **gap 分析表 A（10 子功能 × 7 现有页面 覆盖矩阵）+ 表 B（Figma 组件 ↔ §9 组件映射）齐全**
- [ ] 每个页面字段表至少含 3 个核心字段（**6 列：名称 / 类型 / 来源 / 必填 / 示例 / metric_id**）
- [ ] **统计/聚合字段必有 metric_id**（命名 `M_ENT_{INDICATOR}_{PERIOD?}`，备注列写"待 data-agent 注册 cfg_metric"）
- [ ] 每页末尾有 **`本页 metric_id 清单`** 小节
- [ ] mermaid 站点地图 + 主用户流 + ≥3 条异常路径 语法正确
- [ ] §9 通用组件中**至少 10 个**被 wireframe 区块命名引用（**不得自创命名**）
- [ ] §4.2 5 段优先级**每页面都有**
- [ ] §18 验收清单 18 条对照表（handoff 末尾；UX 阶段自检自己负责的条目，其余明确标"由 ui-agent 后续负责"）
- [ ] 待评审开放项 ≥10 条（"决策项 / 建议默认值 / 影响"3 列）
- [ ] 范围合规自检：明确写出"未扩大到科研机构分析等同级模块；未含 E-31~E-37 企业查询"
- [ ] git commit（**不 push**），commit hash 记入 handoff

## Handoff 位置与必填项

**位置**：`E:\gkx_src\agent-delivery\agent-handoffs\UX-ENT-strategic-analysis.md`

必填项：
1. 执行时间 + 任务范围（bid §1.1.1.2.4.2.3 + E-20~E-30）
2. 完成清单对照 DoD（表格）
3. 5 份产物绝对路径 + 体量统计（行数/字符数）
4. commit hash（**注明未 push**）
5. 范围与实现（scope_ref / implementation_as_built / data_gaps / variance_note）
6. **gap 分析摘要**（表 A 覆盖率统计：✅/🟡/❌/⚠️ 各几项；缺口页面建议清单）
7. **§18 18 条对照表**（UX 自检 + ui-agent 待办分工）
8. **§4.2 5 段优先级覆盖表**（每页面 × 5 段）
9. **待人评审开放项 ≥10 条**（K-O1~K-O10+，按重要性排序）
10. 给 ui-agent 接力的 next-step 建议（含 §10 Arco 控件映射建议、现有 Figma 组件迁移提示、缺口页面优先级）
11. **【数据血缘汇总】**：全部 metric_id 清单（按页面分组，含命名/口径占位/source_tables 真实 ODS 表/算法依赖标识）+ 给 data/algorithm/api-agent 的接力建议
12. **【topic_demo ↔ D8 规范差异清单】**（本任务新增）：现有 Figma/shadcn 实现与 D8 Arco §9 规范的具体差异，建议未来 lumen 复刻时如何对齐
13. **【业务口径开放项】**：企业类型口径（外企/高企/小微/上市定义）、技术力/商业力/竞争力指标权重、招引/培育推荐阈值、行政区划精度等若有歧义，登记到 `客户决策清单跟踪表.md` 并在此列出

## 成本回填（团队公约 §3.7 铁律）

handoff 完成时回填：`estimated_tokens`（UX 起草类约 90k–130k）/ `actual_tokens` / `model_used` / `actual_cost` / `cost_warn`（green/yellow$>5/orange$>10/red$>20）。单 task >$10 暂停复盘，>$20 hard stop。

## 最终响应（Cursor 会话最后一次回复必须包含）

1. 5 份产物绝对路径
2. commit hash + 改动行数（注明未 push）
3. gap 分析摘要（10 子功能覆盖率：✅/🟡/❌ 各几项）
4. §18 18 条对照摘要（绿/黄/红 数量）
5. 5 条最重要待评审开放项（K-O1~K-O5）
6. 给 ui-agent 的接力建议（≥3 条关键提示）

中文产出。开始执行。

## ====== 派单话术结束 ======

---

## PM 评审要点（完成后自用）

| 检查项 | 通过标准 | 阻塞标志 |
|--------|---------|---------|
| 5 份 md 齐全 | 路径正确，在 topic_demo/docs/ia/enterprise/ | 缺文件 / 写错目录 / 误改 src/ |
| 10 子功能全覆盖 | 每个挂 §1.1.1.2.4.2.3.X + E-XX | 漏子功能 / 越界到科研机构 / 混入 E-31~E-37 |
| **gap 分析** | 表 A + 表 B 齐全，缺口页面有优先级 | 没读现有页面代码 / 只有 IA 没有 gap |
| 数据血缘 metric_id | 字段表 6 列；统计字段全有 `M_ENT_*`；页末有清单 | 缺列 / 命名不符 / 没引用真实 ODS 字段 |
| §9 组件使用率 | ≥10 个被引用，用标准名 | 自创命名 / 照搬 Figma 组件名当区块名 |
| §4.2 5 段优先级 | 每页面都有 | 只有布局没有优先级 |
| §18 18 条对照 | UX 自检 + 标注 ui-agent 待办 | 缺对照 |
| topic_demo↔D8 差异清单 | 明确列出 Figma↔§9 差异 | 没写 = 失去迁移依据 |
| 开放项 ≥10 条 | 3 列结构化 | 把决策都自己做了 |

### 评审通过后
1. 与 UE lead 同步评审结果
2. 通知 UI 同学进入 ui-agent 阶段（按 gap 分析缺口优先级补齐 topic_demo 页面）
3. 回本对话告知"UX 评审通过"，由 coordinator 生成 ui-agent 派单话术

### 评审不通过
- 在 `agent-handoffs/企业战略分析-ENT/UX-ENT-strategic-analysis.md` 末尾加 `## PM 评审意见` 节，列具体返工项；UX 同学在原会话续改（不开新会话）

---

## 角色对齐（团队公约 §6）

| 谁 | 做什么 | 不做什么 |
|----|--------|---------|
| **PM** | 派单 / 评审 / 与 UE 对齐 / 决策推送 | 直接改 UX 产出 |
| **UX 同学** | 开会话 + 复制话术 + 监督产出 + 评估 handoff | 写代码 / 改 src/ |
| **ux-agent（AI）** | 按话术产出 md / handoff / commit（不 push） | 写视觉代码 / 改现有页面 / 越范围 |
| **UE lead** | 联审 IA/wireframe/gap 是否符合用户旅程最佳实践 | 替 PM 决策 |