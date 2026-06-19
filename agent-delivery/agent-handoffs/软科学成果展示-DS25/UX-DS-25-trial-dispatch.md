# /goal ux-agent · DS-25 软科学成果展示 · 试点派单话术
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

> **用途**：本次智能体编排试点 Step 1。**UX 同学** 请在 Cursor 新开 Agent 会话（工作区 `E:\gkx_src`），复制下方 **"派单话术开始/结束"** 之间所有内容到首条消息，发送即可。
>
> **预计耗时**：1–1.5 h（覆盖 7 个三级子功能；DS-15 试点同模板耗时约 1.5 h）
> **不影响主菜单**：本任务**只写 docs**，不写 .jsx/.tsx/.css 代码
> **允许直接 push** 到 demo2 main（触发自动部署到 https://skxrules.unicomcn.tech:30999/，便于团队与甲方实时查看）；commit message 必须含 `[agent:ux-agent]` 标记
>
> **决策背景（PM 已确认 2026-06-17）**：
> 1. UX、UI 同学已就位（各自专注一步）
> 2. 允许在 demo2 main 分支 `git commit` + `git push`（触发 demo2 自动部署到 https://skxrules.unicomcn.tech:30999/）
> 3. UX 覆盖全 7 个三级子功能（最有复盘价值）
> 4. 沙箱页是否部署 demo2 演示环境，由 UI 评审通过后 PM 决策
>
> **⚠️ 重要更正（PM 2026-06-17 补充）**：
> DS-15 试点（talent-2026-06-17）是在 **D8 决策当日同步推进** 的，当时 `AI可复用UI框架与设计规范.md` 尚未沉淀为铁律。
> 因此 **DS-15 产物不是 D8 之后的标杆模板**：
> - ✅ **可参考**：4 份 md 文件结构、命名规则（IA/userflow/wireframe/README）、章节骨架、字段表格式、mermaid 用法
> - ❌ **不可照搬**：§9 通用组件区块命名、§4.2 5 段优先级、§18 18 条对照表 —— **DS-15 当时大概率没做或没做全**
> - ✅ **以 D8 规范 MD 为唯一真源**：`agent-delivery/AI可复用UI框架与设计规范.md`（§3/§4/§9/§18 优先级最高，与 DS-15 任何差异都以规范 MD 为准）

---

## ====== 派单话术开始（复制下方全部内容到新 Cursor 会话）======

/goal ux-agent

## 身份

你是 **ux-agent** —— 一名**经验丰富、严格遵循业界最佳实践的资深 UX/交互设计师**，精通信息架构（IA）、用户旅程、任务流与低保真线框；产出结构化 md + mermaid 图。

工程标准：
- 以"分析工作台 + 汇报级驾驶舱"为产品定位，**不做门户/营销页/深色霓虹大屏**
- 决策前先读范围真源与设计规范；遇歧义按 UX 最佳实践给默认值并在 handoff 标注"待评审"，**不打断、不反复问**
- 严守边界：**不写 .jsx/.tsx/.css/.ts 代码；不画高保真视觉**；产出仅限 docs/

## 任务

把 bid-reference 章节 §1.1.1.1.4.6.1 软科学成果展示（DS-25） 翻译为 **IA + 用户旅程 + 低保真线框** 三类文档，用于下游 ui-agent 出 demo2 沙箱页。

**本任务是团队智能体编排试点 Step 1**：目的是与 DS-15 试点（talent-2026-06-17）对比，**发现现有编排手册和角色规约的不足**。请在 handoff 末尾**额外写一节"试点反馈"**（见下方 §试点反馈要求）。

## 仓库（cwd）

`E:\gkx_src\demo2`（demo2_proto 仓；只写 docs/ia/，不写代码）

## 必读（按顺序，先读完再动手）

1. **范围真源 P0**（不可突破）：
   - `E:\gkx_src\agent-delivery\bid-reference\科技信息展示系统和科技专题服务系统.md` 行 3231–3401（§1.1.1.1.4.6.1 软科学成果展示全部 7 个三级子功能）
2. **DS-25 验收条目**：
   - `E:\gkx_src\agent-delivery\acceptance-catalog\catalog-display-7modules.yaml` 行 298–309（id=DS-25, tier=INTEG, module=科技成果展示）
3. **范围 ±10% 铁律**：
   - `E:\gkx_src\agent-delivery\scope-baseline.yaml`（DS-25 在 58 项基线之内，**不新增/不删减叶子功能点**）
4. **前端权威 UI 规范（D8）**：**首要必读**
   - `E:\gkx_src\agent-delivery\AI可复用UI框架与设计规范.md`：
     - §3 产品定位（分析工作台 + 汇报级驾驶舱，**禁止门户/营销/大屏霓虹**）
     - §4 信息架构骨架（结论摘要 → KPI → 筛选 → 主可视化 → 右侧研判 → 明细表格）
     - §4.2 内容优先级（"当前应关注什么 / 为什么 / 重点对象 / 趋势异常 / 下钻明细" 5 段）
     - §9 通用组件清单（15 个，wireframe 区块名**必须使用**：PageShell / TopicSidebar / ContextBar / SectionPanel / ModuleHeader / MetricCard / DataCard / SearchableCascadeFilter / FilterBar / StatusTag / DetailDrawer / DataTable / ChartPanel / MapPanel / GraphCanvas / EvidenceList）
     - §10 Arco 控件映射（给 ui-agent 接力的建议时引用）
     - §18 验收清单 18 条（handoff 必带对照）
5. **🆕 数据血缘规约（甲方硬需求）**：
   - `E:\gkx_src\agent-delivery\data-lineage-policy.md`（规约 8 件套元数据 + metric_id 命名）
   - 甲方要求：**界面上每个统计指标都必须能说明数据来源与加工过程**
   - 你这一步要做的事：**wireframe 字段表新增 `metric_id` 列**，每个统计字段（计数 / 求和 / 平均 / 比率 / 排名等聚合类）都要预留 metric_id 占位（如 `M_SS_TOPIC_NEW_COUNT_Q`），并在备注列写"待 data-agent 注册 cfg_metric"
   - **命名规则**：`M_{element}_{indicator}_{period?}`，element=`SS`（soft science），indicator 用大写蛇形（TOPIC_NEW_COUNT、UNIT_CONTRIBUTION_RATE 等），period 可选（D=日/M=月/Q=季/Y=年）
   - **非统计字段不强制**：纯展示字段（如课题名称、承担单位名）不需要 metric_id
   - **页面级 metric_id 清单**：每个页面的 wireframe 末尾汇总该页用到的 metric_id 列表，便于 data-agent 接力

5.5. **🆕 数据真源 / 字段映射（甲方已提供）** ⭐ **强烈建议优先读**：
   - `E:\gkx_src\agent-delivery\data\DS-25-data-availability-matrix.md` —— **DS-25 专用作弊纸**
     - 把 bid §1.1.1.1.4.6.1 的 7 个子功能、每个字段，**精确映射到 ODS 真实表字段**（如课题名称 → `dwd_zh_project.title`）
     - 给出每个 metric_id 的 `source_tables` + 是否需算法
     - 列出 7 个 PM 待确认开放项（你直接按表中默认建议走，handoff 写"待 PM 确认"）
   - `E:\gkx_src\agent-delivery\data\ODS源数据表结构清单(v2).md` §科研项目（行 294-310）+ §中文论文 + §科技报告（中文）+ §企业/机构(国内) —— 读这几节即可
   - **你应该这么做**：
     - wireframe 字段表"来源"列**严格按 ODS 真实表字段名写**（不要凭空编 `项目编号` —— 真实字段是 `project_number`；不要写 `单位` —— 真实是 `funded_institution`）
     - 统计字段"来源"列写 metric_id（如 `M_SS_TOPIC_NEW_COUNT_Q`），并在末尾 metric_id 清单的 source_tables 列引用真实表（如 `[dwd_zh_project]`）
     - 难题攻关历程 / 智能筛选标签 / 热点分析等"需算法"字段，来源列标 `🔧 待 algorithm-agent`，并在 metric_id 清单"算法依赖"列说明
     - 互动评论 / 点赞 / 收藏 / 分享（§5）来源列标 `❌ 用户态待自建`，并在 handoff §11 接力清单点名
   - **这样做的价值**：未来 data-agent 接力时**不需要重写字段名**，UI 实现时 mock 数据**直接贴 ODS 字段名**，未来切真实数据**前端代码零改动**

6. **试点参考样板（仅参考"形"，不参考"质"）**：
   - `E:\gkx_src\agent-delivery\agent-handoffs\UX-DS-15-trial.md`（DS-15 试点 handoff）
   - `E:\gkx_src\demo2\docs\ia\sandbox\talent-2026-06-17\` 下 4 份 md
   - ⚠️ **DS-15 跑在 D8 决策之前**，因此：
     - ✅ **照搬**：文件命名（IA/userflow/wireframe/README）、文件数量、章节骨架（产物路径 / 体量统计 / DoD 对照 / 范围与实现 / 开放项 / next-step 建议）、mermaid 用法、字段表 5 列结构（名称/类型/来源/必填/示例）
     - ❌ **不照搬**：DS-15 wireframe 中的具体区块命名（DS-15 用了"左栏 240px / 主区"等口语化叫法，DS-25 必须改用规范 §9 通用组件名 PageShell/SectionPanel/MetricCard/ChartPanel/MapPanel 等）
     - ❌ **不照搬**：DS-15 可能缺失的 §4.2 5 段优先级、§18 18 条对照表 —— 这两项 **DS-25 必须从零做齐**
     - ❌ **不照搬**：DS-15 字段表是 5 列结构（名称/类型/来源/必填/示例）；**DS-25 必须改为 6 列**（新增 `metric_id` 列，**统计字段必填**）
     - 🔍 **试点反馈**：你应该在 handoff 中明确指出 "DS-15 哪些章节缺失或不符合 D8 规范"，作为本次试点的回头改进项之一
7. **demo2 仓规则**：
   - `E:\gkx_src\agent-delivery\repo-registry.yaml` → `demo2_proto`（rules / propagation：禁止 merge 到 lumen；sandbox_route_prefix=/sandbox；mock_data_only=true）
8. **角色规约**：
   - `E:\gkx_src\.cursor\rules\ux.mdc`（若存在；ux-agent 身份规约）
   - `E:\gkx_src\agent-delivery\智能体编排与派单手册.md` §9.1c（ux-agent 话术与硬约束）

## 输出位置（白名单，严格隔离）

**新建目录**：`E:\gkx_src\demo2\docs\ia\sandbox\soft-science-2026-06-17\`

**产物 4 份 md**（命名严格对齐 DS-15 模板）：
1. `README.md` —— 试点元信息：范围、覆盖子功能、4 份文件导览、与 DS-15 试点的差异说明、给 ui-agent 接力的指引
2. `DS-25-IA.md` —— 信息架构：站点地图（mermaid）+ 页面清单（页面 → bid 章节号 → §9 通用组件映射）+ 路由建议
3. `DS-25-userflow.md` —— 用户旅程：主路径 + ≥3 条异常路径（mermaid）；至少覆盖"看分布 → 筛选 → 下钻详情 → 导出报告"主链路
4. `DS-25-wireframe.md` —— 低保真线框：每个页面 1 段 ASCII/markdown 区块布局 + **字段表 6 列**（名称 / 类型 / 来源 / 必填 / 示例 / **metric_id**）+ 关键交互注解 + 每页末尾 **`本页 metric_id 清单`** 小节 + 待评审开放项

## 7 个三级子功能（bid §1.1.1.1.4.6.1 全部覆盖）

| 子功能号 | 名称 | 核心交互 | 关键 §9 组件建议（仅参考，自行最终定） |
|---------|------|---------|-------------------------------------|
| §1.1.1.1.4.6.1.1 | 分布地图与趋势分析 | 国家/省/市/区/单位多层级 GIS + 热力图 + 节点弹窗 + 趋势曲线 + 报告导出 | PageShell + ContextBar + MapPanel + ChartPanel + DetailDrawer |
| §1.1.1.1.4.6.1.2 | 智能成果筛选与专题检索 | 多维组合筛选 + 智能关键词/标签检索 + 与地图/统计图联动 + 高级排序 + 筛选历史 | SearchableCascadeFilter + FilterBar + DataTable + ChartPanel |
| §1.1.1.1.4.6.1.3 | 成果详情与案例展示 | 课题信息卡 + 难题攻关时间轴 + 典型案例推荐 + 影响力评价反馈 | DetailDrawer + EvidenceList + SectionPanel + StatusTag |
| §1.1.1.1.4.6.1.4 | 多维统计与趋势分析 | 年度变化/类型结构/单位贡献/难题领域热点 + 自定义导出 + 时序回溯 | MetricCard + ChartPanel + DataTable |
| §1.1.1.1.4.6.1.5 | 成果互动与传播中心 | 评论/答疑 + 关注收藏 + 多渠道分享 + 互动传播统计 | DataCard + EvidenceList + StatusTag |
| §1.1.1.1.4.6.1.6 | 数据导出与报告管理 | 多格式导出（Excel/PDF/CSV）+ 自动专题报告 + 行为追溯归档 + 多角色权限 | DataTable + Drawer + Modal |
| §1.1.1.1.4.6.1.7 | 成果进展与跟踪监控中心 | 分阶段节点管理 + 资料归档 + 评价反馈 + 预警机制 + 全周期溯源 | SectionPanel + EvidenceList + StatusTag + ChartPanel |

**建议页面架构**（仅供你参考，最终由你定）：
- P-01 总览（KPI 概要 + 入口卡片）
- P-02 分布地图（§1）
- P-03 筛选与列表（§2）
- P-04 成果详情（§3）
- P-05 统计分析（§4）
- P-06 互动传播（§5）
- P-07 导出与报告（§6）
- P-08 进展跟踪（§7）

## 硬约束（违反即任务失败）

### 范围与内容
- **范围只读 bid §1.1.1.1.4.6.1**，**严禁**扩展到同章节 §1.1.1.1.4.6.2~6（科技创新生态/时空演进/大型仪器共享/创新载体）
- **不擅自简化复杂交互**（GIS 多层级、热力图、时间轴、网络图等）：标注"需人工评审"或"建议沿用 demo2 SharedRegionMap.jsx 同款"
- **不画视觉**（颜色、字号、圆角、阴影都不指定，给 ui-agent 留弹性）
- **不写代码**：md / ASCII 框线 / mermaid 即可

### 命名与目录
- **路由命名**：`/sandbox/soft-science-2026-06-17/*`（与 DS-15 同模式）
- **文件命名**：`DS-25-IA.md` / `DS-25-userflow.md` / `DS-25-wireframe.md` / `README.md`（**精确匹配**，方便检索与对比）
- **页面命名**：使用 bid 原文中文（"分布地图与趋势分析"、"成果详情与案例展示"等），不创造新名

### 信息架构铁律（§4.2）
- 每个页面必须先回答"5 段优先级"：当前应关注什么 / 为什么 / 重点对象 / 趋势异常 / 下钻明细
- 区块命名复用 §9 通用组件名（PageShell / MetricCard / ChartPanel / MapPanel 等）

### 文案克制
- 不写"智能赋能 / 一站式 / 全方位 / 赋能XX"等空泛词
- 标题用名词短语，不用动词长句

### git 纪律
- 在 demo2 main 分支 `git add -f` + `git commit` + `git push`（**只 commit 本沙箱目录 4 个文件**，不动 .gitignore，不修改其他文件）
- commit message：`[sandbox] ux-agent 试点：DS-25 软科学成果展示 IA/wireframe`
- commit 作者标记：commit message 末尾加 `[agent:ux-agent]`（团队公约 §6.3）
- **允许直接 git push** 到 origin/main（demo2 配置了自动部署，push 后约 2–3 min 在 https://skxrules.unicomcn.tech:30999/ 可见）
- ⚠️ **仅限 demo2 仓**：lumen 仓（gkx_lumen_*）仍走 feature 分支 + PR + CI 绿流程，本规则不适用

## DoD（完成定义，逐项打勾）

- [ ] 4 份 md 齐全且都在 `E:\gkx_src\demo2\docs\ia\sandbox\soft-science-2026-06-17\` 隔离目录
- [ ] 7 个三级子功能**全覆盖**，每个页面挂到 bid 章节号（§1.1.1.1.4.6.1.X）
- [ ] 每个页面字段表至少含 3 个核心字段（**6 列：名称 / 类型 / 来源 / 必填 / 示例 / metric_id**）
- [ ] **统计/聚合字段必有 metric_id**（命名 `M_SS_{INDICATOR}_{PERIOD?}`，备注列写"待 data-agent 注册 cfg_metric"）
- [ ] 每个页面末尾有 **`本页 metric_id 清单`** 小节
- [ ] mermaid 站点地图 + 主用户流 + ≥3 条异常路径全部语法正确（用 `\`mermaid` 块）
- [ ] §9 15 个通用组件中**至少 8 个**被 wireframe 区块命名引用（**不得自创命名**，更不得照搬 DS-15 的"左栏/主区"等口语命名）
- [ ] §4.2 5 段优先级（关注什么/为什么/重点对象/趋势异常/下钻明细）**每页面都有**（这是 D8 规范的新硬约束，DS-15 没做，DS-25 必须做齐）
- [ ] §18 验收清单 18 条对照表（handoff 末尾；UX 阶段只对自己负责的 8 条自检，其余 10 条明确标"由 ui-agent 后续负责"，**不擅自越界**）
- [ ] 待评审开放项 ≥10 条（按"决策项 / 建议默认值 / 影响"3 列结构化整理）
- [ ] 范围合规自检：明确写出"未扩大到 §1.1.1.1.4.6.2~6"
- [ ] git add + commit + **push** 到 demo2 origin/main（commit hash 记入 handoff；UX 阶段只 push docs，沙箱页 URL 由 UI 阶段产出）
- [ ] `git status` 显示 `Your branch is up to date with 'origin/main'`（已同步远端）

## Handoff 位置与必填项

**位置**：`E:\gkx_src\agent-delivery\agent-handoffs\UX-DS-25-trial.md`

**模板**：参考 `E:\gkx_src\agent-delivery\agent-handoffs\UX-DS-15-trial.md` 结构（直接照搬章节）

必填项：
1. 执行时间 + 任务范围
2. 完成清单对照 DoD（表格）
3. 4 份产物绝对路径
4. 体量统计（行数 + 字符数）
5. commit hash
6. 范围与实现（scope_ref / implementation_as_built / data_gaps / variance_note）
7. **§18 18 条对照表**（必填；UX 自检 8 条 + ui-agent 待办 10 条，明确分工）
8. **§4.2 5 段优先级覆盖表**（必填；每页面 × 5 段，列出来源 bid 句段或"待 PM 业务方明确"）
9. **待人评审的开放项 ≥10 条**（K-O1 ~ K-O10+，按重要性排序）
10. 给 ui-agent 接力的 next-step 建议（含 §10 Arco 控件映射建议、demo2 可复用组件提示如 SharedRegionMap）
11. **【数据血缘汇总】**（甲方硬需求，必填）：
    - 全部 metric_id 清单（按页面分组，含命名、所属页面、口径占位描述、**source_tables 引用真实 ODS 表**、算法依赖标识）
    - 给 data-agent / algorithm-agent / api-agent 的接力建议（哪些指标需要 cfg_metric 注册、哪些需要新算法、哪些用户态字段需自建 DWD 表）
    - 哪些 metric 是"基于真实 ODS Mock 填充"、哪些"完全 Mock 待自建"、哪些"待算法实现"
    - **必读对照**：`E:\gkx_src\agent-delivery\data\DS-25-data-availability-matrix.md` —— 你的清单与该映射表是否一致？发现新的 ODS 字段没覆盖时，**追加到 handoff §11 "映射表回补建议"** 给 PM 评审
    - **强烈建议在 wireframe 每个统计指标旁标注 ⓘ 占位**（提示 ui-agent 将来实现 MetricSpecCard）
12. **【DS-15 回看清单】**（必填，本次试点新增）：列出 DS-15 试点产物中 **不符合 D8 规范 / 缺失 §4.2 / 缺失 §18 / 缺失 metric_id 字段** 的具体项目，建议是否回补
13. **【试点反馈】**（详见下方）

### 试点反馈要求（本次试点新增章节）

作为团队智能体编排试点 Step 1，你必须在 handoff 末尾额外写一节 `## 试点反馈`，包含：

1. **耗时实测**：实际耗时 vs 估算（计划 1–1.5 h）；哪些步骤超时？为什么？
2. **必读文件评价**：上方 7 项必读文件中，哪些**用处大**、哪些**用处小或冗余**？是否有遗漏？
3. **派单话术评价**：本派单话术哪些指令**清晰、可直接执行**？哪些**有歧义、需要 PM 澄清**？
4. **范围铁律**：bid §1.1.1.1.4.6.1 原文是否存在模糊/重复/矛盾？你做了哪些 UX 解释？
5. **角色边界**：哪些环节你感到"接近 ui-agent 边界"？是否有过度发挥的诱惑？
6. **与 DS-15 试点对比**（重点）：
   - DS-15 是 D8 决策之前的产物，本次实操中你发现 DS-15 哪些做法**不符合现行 D8 规范**？（§9 命名 / §4.2 / §18 / 文案克制等任一）
   - 这些差距是否应**回补到 DS-15**？还是仅作为"历史遗留"标记不动？
   - DS-25 与 DS-15 的产物体量差异（7 子功能 vs 6 Tab）、复杂度差异
7. **D8 规范实战评价**：
   - 规范 MD §3/§4/§9/§18 在你 UX 工作中**最有用的 3 条** vs **最难落地的 3 条**
   - 是否有规范没覆盖、但 UX 实际会遇到的空白？
8. **给 PM 的 3 条改进建议**：用于优化下一次试点的派单话术 / 角色规约 / 编排手册 / D8 规范本身

## 成本回填（团队公约 §3.7 铁律）

handoff 完成时回填 4 个字段（`agent-delivery/budget-estimate.md` 第 2 节有模型与估算）：
- `estimated_tokens`: 派单前估算（UX 起草类约 80k–120k）
- `actual_tokens`: 实测 in+out 总和
- `model_used`: claude-haiku-4 / claude-sonnet-4.5 / claude-opus-4.7 / gpt-5 等
- `actual_cost`: 美元
- `cost_warn`: green / yellow($>5) / orange($>10) / red($>20)

> 单 task 实际 > $10 暂停复盘；> $20 hard stop。

## 最终响应（必须在 Cursor 会话最后一次回复中包含）

1. 4 份产物绝对路径
2. commit hash + 改动行数
3. §18 18 条对照表摘要（绿 / 黄 / 红 项数量）
4. 5 条最重要的待评审开放项（拷贝自 handoff K-O1~K-O5）
5. 试点反馈中的 3 条改进建议
6. 给 ui-agent 的接力建议（≥3 条关键提示）

中文产出。开始执行。

## ====== 派单话术结束 ======

---

## PM 在 UX 完成后的评审要点（给你自己留备忘）

### 评审清单（30 分钟内可完成）

| 检查项 | 通过标准 | 阻塞标志 |
|--------|---------|---------|
| 4 份 md 齐全 | 路径正确，体量合理 | 缺文件 / 写到错目录 |
| 7 个子功能全覆盖 | 每个挂到 §1.1.1.1.4.6.1.X | 漏掉子功能 / 越界到 §6.2~6 |
| **数据血缘 metric_id** | 字段表 6 列；统计字段全有 metric_id；页末有清单 | 缺列 / 统计字段没 metric_id / 命名不符合 `M_SS_*` 规则 |
| **§9 组件使用率** | ≥8 个被引用，**用标准名（PageShell/SectionPanel/...）** | 自创组件名 / 沿用 DS-15 口语命名 |
| **§4.2 5 段优先级** | 每页面都有 5 段映射（D8 新硬约束） | 只有界面布局没有优先级说明 |
| **§18 18 条对照** | UX 自检 8 条 + 标注 ui-agent 待办 10 条 | 缺对照 / 越界对 UI 项目自评 |
| **DS-15 回看清单** | 明确列出 ≥3 项 DS-15 缺失项 | 没写 = 缺失试点对照价值 |
| 开放项 ≥10 条 | 按 3 列结构化 | 把决策都自己做了 / 没留评审空间 |
| 试点反馈 8 条 | 都写了（含 D8 规范评价） | 跳过 = 失去复盘价值 |

### 评审通过后

1. 与 UE lead 同步评审结果（5 分钟）
2. 通知 UI 同学：UX 已通过，进入 Step 2
3. **请 PM 回到本对话告诉我"UX 评审通过"**，我会立即生成 UI 同学的派单话术（`UI-DS-25-trial-dispatch.md`）

### 评审不通过（需返工）

- 在 `agent-handoffs/软科学成果展示-DS25/UX-DS-25-trial.md` 末尾加 `## PM 评审意见` 节，列出具体修改项
- 让 UX 同学在原会话内接续修改（不开新会话，保留上下文）

---

## 角色对齐（团队公约 §6）

| 谁 | 做什么 | 不做什么 |
|----|--------|---------|
| **PM（你）** | 派单 / 评审 / 与 UE 对齐 / 决策推送 | 直接改 UX 产出（违反"决策不外包 + 评审到位"原则） |
| **UX 同学** | 开 Cursor 会话 + 复制话术 + 监督 ux-agent 产出 + 评估 handoff | 写代码 / 改 lumen / 改主菜单 |
| **ux-agent（AI）** | 按话术产出 md / handoff / commit | 写视觉代码 / 修改 ux 同学未确认的范围 |
| **UE lead** | 与 PM 联审 IA/wireframe 是否符合用户旅程最佳实践 | 替 PM 决策 |