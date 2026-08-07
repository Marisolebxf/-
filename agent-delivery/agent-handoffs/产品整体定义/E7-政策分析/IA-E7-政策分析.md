# IA-E7-政策分析.md

> **模块**：E7 政策分析（科技专题服务系统）  
> **阶段**：门 1 PDR 输入 · POLICY-PACK-L01  
> **体验 Owner**：高颖  
> **范围真源**：`bid-reference/科技信息展示系统和科技专题服务系统.md` → `§1.1.1.2.4.2.6`  
> **对应**：`USM-E7-政策分析.md` · `TRACE-E7-政策分析.yaml`  
> **版本**：v1.4.5 · 2026-08-07（产业 Tab 发起政策三项；**移除对比篮政策 Tab**）

## 1. 模块边界

- **解决的问题**：以产业/技术领域为锚点，经系统对比篮产业 Tab 发起政策演进洞察、区域对标与深圳三维评估；系统自动关联相关政策；并能恢复分析任务、查看不可变结果及生成/下载报告；同时承接门户政策扶持展示与维护管理。
- **承接内容**：
  - **政策查询**（政策文档发现与画像；复用企业/产业查询页面模式；**不入对比篮、不直接发起分析**）
  - **门户政策扶持展示**（P-17~P-22，单壳 `/policy-portal/overview` 四 Tab；展示浏览；无政策文档入篮；无页级全局筛选）
  - **系统对比篮 · 产业 Tab**（政策三项分析发起入口：勾选产业 →「政策分析」分组分发）
  - **系统任务浮层接入**（分析/报告统一规则；本包只注册政策域类型与落点）
  - **维护管理**（复用企业 ENT-OPS 菜单形态：内容运营 / 图谱运营 / 分析配置）
  - 政策时序分析（P-70）、区域政策对比（P-72）、深圳政策现状分析·三维框架（P-73）
- **不承接内容**：
  - 对比篮「政策」文档 Tab；政策查询/门户「加入对比篮」写政策文档
  - 展示系统「科技政策跟踪」及核增「政策对比功能升级」前端页（另包 DS10-12）
  - 查询结果「深度分析」直达分析页，或任何绕过系统对比篮的分析发起（页面直选产业为增强路径，见 DEC）
  - 对比篮浮层壳层、多对象 Tab 编排、与系统任务避让等共享实现（归属 `ENT-COMPARE` / 系统 Shell）
  - 系统任务队列、槽位、阅读器、PDF 下载管道、模板库内部实现（归属 `SystemTaskLayer` / 共享报告框架）
  - ENT-OPS 企业字段/企业内容类型原样硬套；独立政策任务中心、结果/报告收藏
  - 独立竞争力报告页（P-74）、独立优势短板报告页（P-75）— Wave2
  - 前端直连算法 / Nebula；算法经 Java REST → Python `/internal/*`
  - 单独「统一智能检索模块」全站页（其它厂商范围）

## 2. 用户入口与产品角色

| 产品角色 | 入口 | 核心目标 |
| --- | --- | --- |
| 政府科技主管部门 | 产业查询入篮 → 产业 Tab 发起政策分析；维护管理（权限态） | 选定产业 → 窗口期研判、对标、短板定位 |
| 产业园区 | 同上 | 选定产业 → 区域补贴/准入差异与招商策略 |
| 投资机构 | 同上 | 选定产业 → 区域政策竞争力与产业适配判断 |
| 研究团队 | 同上 | 经产业篮完成三项分析并经系统任务生成/下载报告 |
| 内容运营 / 数据治理 | `/policy/maintenance`（复用 ENT-OPS） | 政策新闻与主体维护、分析配置 |

> 角色依据：`§1.1.1.2.4.2` 战略分析总述原文。默认落在中屏工作台 `medium_1440_1920`，无小屏轨。

## 3. 信息架构

```text
政策分析（E7）
├─ 门户政策扶持（展示）        /policy-portal/overview    ← P-17~P-22 · 二级菜单第 1 位（对齐产业总览单壳多 Tab）
│  ├─ Tab 政策概览（默认）     ?tab=overview&view=stats|map|rank  ← P-17+P-18+P-20
│  │     stats：产业 Cascader + geo + 同级对照；map：产业+geo、件数热力、无对照
│  │     rank：省/市榜 · Top3 领奖台+单表（不绑产业）；见 RANK-PRESENTATION
│  │     DEC-E7-PORTAL-STATS-INDUSTRY-COMPARE + STATS-MAP-DENSITY
│  ├─ Tab 产业覆盖             ?tab=coverage              ← P-19
│  ├─ Tab 最新政策动态         ?tab=latest                ← P-21
│  ├─ Tab 深圳政策             ?tab=shenzhen&szView=…     ← P-22（S1 四段镜像 + 各区对照；无力度榜）
│  └─ 展示浏览（不发起分析；无政策文档入篮）；无页级全局 ContextBar
│     DEC-E7-PORTAL-TAB-MERGE-A + NO-GLOBAL-FILTER + RANK-PRESENTATION + SHENZHEN-MIRROR
├─ 政策查询（政策文档发现）  /policy/search
│  ├─ 普通查询工作台（ElementSearchWorkbench 共享壳）
│  │  ├─ 模式栏：智能检索 | 查政策 | 高级筛选→
│  │  ├─ SearchHub：输入 / SmartChip / 示例 / 热门政策
│  │  ├─ RecentSearchPanel（按模式过滤）
│  │  └─ 推荐态 / 结果态（政策卡/画像；无「加入对比篮」；无深度分析）
│  └─ 高级筛选下级页           /policy/search?mode=advanced
├─ 政策时序分析                /policy/overview          ← P-70
│  └─ 经产业对比篮分发进入 · 配置 → 任务 → 结果 → 报告
├─ 区域政策对比                /policy/analysis           ← P-72
│  └─ 同上
├─ 深圳政策现状分析            /policy/recommendation     ← P-73
│  └─ 同上
├─ 维护管理                    /policy/maintenance        ← 复用 ENT-OPS
└─ 共享系统能力（非二级菜单；与企业/产业共用）
   ├─ ① 系统对比篮浮层 · **产业 Tab**（政策三项发起；**无政策 Tab**）
   ├─ ② 系统任务浮层 · analysis / report（过程恢复）
   └─ ③ 分析报告模板框架 · ENT-EXPORT（统一模板 → HTML 预览 → PDF）
```

**对象流**（双路径；`DEC-E7-POLICY-SCOPE-MUTEX-20260807`）：

```text
路径甲 · 产业篮：
  产业查询 → 加入对比篮·产业 Tab → 发起「政策分析」→ 配置页（object_type=industry，可改选产业）
路径乙 · 页内直选：
  菜单进分析配置页 → 对象类型「产业|技术领域」XOR
    · 产业：恰好 1（页选或预填篮）
    · 技术领域：可多选 ≥1（仅页内，暂不进篮）
  → 关联政策概要 → 配置参数 → 系统任务 → 结果 → 报告
```

- **禁止**：产业与技术领域同时生效；技术领域入对比篮；政策文档入篮；查询「深度分析」直达。  
- 无产业分发且尚未页选锚点时：可打开产业篮 **或** 在页内选产业/技术领域。  
- 「打开对比篮」→ `compare_object_type=industry`（技术领域无篮入口）。

### 3.1 系统对比篮 · 产业 Tab 发起政策分析（交接合同）

> 决策：`DEC-E7-POLICY-LAUNCH-FROM-INDUSTRY-BASKET-20260807`（修订/废止原 `DEC-E7-COMPARE-ACTIVATE` 中政策文档 Tab 条款）。共享浮层壳层规则继承 `ENT-COMPARE`。

| 项 | 合同 |
| --- | --- |
| 分析对象类型 | `industry`（恰好 1）**XOR** `tech_field`（可多选 ≥1）；见 SCOPE-MUTEX |
| 发起 Tab | 系统对比篮 **产业 Tab** 仅分发产业；技术领域不进篮 |
| 政策 / 技术领域 Tab | **均不挂载** |
| 容量（发起·篮） | 单次篮分发 **1** 个产业；页内技术领域可多选 |
| 分发 / 页选 URL | `object_type=industry|tech_field&object_ids[]&object_names[]&analysis_type&source=compare-basket|page` |
| 页内配置（不进篮） | 对象类型与技术领域多选、对标区域、时序粒度、三维权重等 |
| 分发任务 | ① 时序 → `/policy/overview` ② 区域对比 → `/policy/analysis` ③ 深圳三维 → `/policy/recommendation` |
| 分发后 | 目标页显示「来自对比篮 · 产业」；调整对象 → `compare_object_type=industry` |
| 空态引导 | 读**产业**篮 count：`0` → 去产业查询；`≥1` → 去查询或打开产业篮发起 |
| 决策 | `DEC-E7-POLICY-LAUNCH-FROM-INDUSTRY-BASKET-20260807`（修订原政策文档唯一经篮发起） |
| 篮内禁止 | 不生成分析结果；不执行核增「多维政策对比」结果页职责 |

### 3.2 系统任务浮层合同（共享能力 ②）

> 决策：`DEC-E7-SYSTEM-TASK-REUSE-20260805`。复用企业/产业链已落地的 `SystemTaskLayer`；政策只注册领域 `analysis_type` / 阶段文案与结果路由。

**分析旅程（三项计算型分析共用）**：

```text
对比篮分发 → 分析页配置 → 「生成分析」→ 过程 Steps
  → succeeded 后显式「查看结果」→ 不可变结果
  → （可选）进入 §3.3 报告模板旅程
```

| 项 | 合同 |
| --- | --- |
| 任务种类 | `kind=analysis` 与 `kind=report`（报告生成过程）共用系统浮层 |
| 注册身份 | `analysis_type`、对象/配置摘要、`stage_definitions`、结果路由、`report_task_type` / fingerprint |
| 建议类型键 | `policy_timeseries_analysis` / `policy_region_compare` / `policy_sz_3d_assessment`；报告后缀 `_report` |
| 过程壳层 | 任务摘要 + StageSteps + 当前阶段反馈；**禁止**虚构百分比 / 单一 Spinner |
| 阶段文案 | 按政策类型注册，不得照搬企业文案 |
| 并发 / 撤回 | 同 `analysis_type` 最多 1 个进行中；`queued` 可撤回；`running` 无取消 |
| 结果 | 不可变快照；完成**不**自动跳结果 |
| 恢复 | 系统任务浮层跨模块恢复；不建政策私有任务中心 |
| 与对比篮避让 | 同屏可并存入口，同一时间只展开一个面板 |

### 3.3 分析报告模板合同（共享能力 ③）

> 决策：`DEC-E7-REPORT-TEMPLATE-HTML-PDF-20260805`。第三共享能力 = 统一分析报告模板框架（`ENT-EXPORT` / 共享报告阅读器）；与企业评估、产业链分析同一生成形态。政策只注入章节数据与 `report_template_id`，不自建阅读器或 PDF 引擎。

**报告旅程（固定顺序）**：

```text
有效不可变分析结果
  → 「生成报告」→ 系统 report 任务（按统一模板装载章节）
  → 先打开系统性只读 HTML 预览页（共享阅读器）
  → 用户确认后「下载 PDF」
  → PDF 与当前 HTML 绑定同一 report_revision / fingerprint
```

| 项 | 合同 |
| --- | --- |
| 模板 | 系统统一模板形态；政策注册 `report_template_id` + 章节 payload，不另起私有排版引擎 |
| 生成入口 | 仅成功且有效结果页「生成报告」；同 fingerprint 复用进行中/已完成报告任务 |
| HTML 预览 | 必经步骤；只读系统性预览页（目录/章节/来源与局限说明）；**先于** PDF 下载 |
| PDF 下载 | 自 HTML 预览页或同源动作触发；A4；与 HTML **同一修订**，禁止 HTML/PDF 各绑不同数据 |
| 失败降级 | PDF 缺失/过期时 HTML 仍可读并可在授权下重生成 PDF；过期分析源结果不可新开正式报告 |
| 维护侧 | 维护管理「报告导出模板」tab 配置模板元数据（复用 ENT-OPS）；不在前台分析页编辑模板 |
| 禁止 | 跳过 HTML 直接出 PDF 作为唯一交付；政策私有下载中心；结果/报告收藏；查询/篮内生成报告；DOCX/PPTX 等 V1 范围外格式 |

## 4. 页面 / Tab 职责

| 节点 | 页面职责 | 路由 / 状态 | 原始需求 / TRACE |
| --- | --- | --- | --- |
| 门户政策扶持 | 展示浏览；**二级菜单第 1 位**；单壳 **4 Tab**；概况/地图同发布量域（热力密度）；力度另轴；**无页级全局筛选**；无政策文档入篮 | `/policy-portal/overview?tab=` | P-17~P-22 / US-E7-POL-08 / TAB-MERGE-A / NO-GLOBAL-FILTER / STATS-MAP-DENSITY |
| 政策查询 | 发现政策文档与画像；**不入对比篮**、不发起分析 | `/policy/search?mode=smart\|policy\|advanced` | §1.1.1.2.4.2.6.1.1 / .2.1；浏览承接 |
| 智能检索 | 多字段可解释匹配（非 LLM）；SmartChip 可逐项移除 | `mode=smart` | 产品解释；对齐企业/产业查询 |
| 查政策 | 仅政策标题/名称类关键词模糊查询 | `mode=policy` | 产品解释；对齐「查企业/查产业」 |
| 高级筛选 | 政策字段条件构造；独立下级页，不在蓝色 Hero 内嵌 | `mode=advanced` | 产品解释 |
| 系统对比篮·产业 Tab | 暂存产业；「政策分析」三项分发；**无政策 Tab** | `app-shell#system-compare-basket?active_type=industry` | `US-E7-POL-05`；DEC-E7-POLICY-LAUNCH-FROM-INDUSTRY-BASKET |
| 政策时序分析 | 配置→任务→结果→报告；回答演进与窗口期 | `/policy/overview`（+过程/结果态） | §1.1.1.2.4.2.6.1 / P-70 / US-E7-POL-02 |
| 区域政策对比 | 同上壳层；回答区域差异与竞争优势 | `/policy/analysis` | §1.1.1.2.4.2.6.2 / P-72 / US-E7-POL-03 |
| 深圳政策现状分析 | 同上壳层；回答三维优劣势与优化方向 | `/policy/recommendation` | §1.1.1.2.4.2.6.3 / P-73 / US-E7-POL-04 |
| 系统任务浮层 | 跨模块恢复 analysis/report 任务 | `app-shell#system-task-layer` | US-E7-POL-06；共享能力 ② |
| 报告 HTML 预览 / PDF | 统一模板生成；先 HTML 后 PDF | 共享阅读器 + report 任务 | US-E7-POL-07；`ENT-EXPORT`；共享能力 ③ |
| 维护管理 | 复用 ENT-OPS 三组菜单 | `/policy/maintenance` | US-E7-POL-09 |

## 5. 查询页面模式复用合同（与企业 / 产业同构）

> 决策：`DEC-E7-SEARCH-REUSE-20260805`（会话用户确认：政策按企业查询与产业链查询同一套页面模式继续复用）。

| 区域 / 能力 | 共享承载 | 政策注入 | 禁止行为 |
| --- | --- | --- | --- |
| 普通查询工作台 | `ElementSearchWorkbench`：模式栏 → 输入/反馈 → 快捷入口 → 最近检索 → 推荐/结果 | 页面标识「政策查询」、模式标签、placeholder、示例与热门项 | 复制 Hero/最近检索/结果容器形成政策私有平行结构 |
| 检索中枢 | 泛化 `SearchHub`（Arco 搜索框、模式 Tab、SmartChip、示例/热门） | `smart / policy / advanced`；政策 parser；热门跳转高筛 preset | 继承「查企业/查产业」文案、企业/产业 test id 或字段 |
| 最近检索 | `RecentSearchPanel`：按模式过滤、标题去重、最多 10 条、30 天、恢复重跑、清除 | 独立 storage key：`gkx-policy-search-recents:v1` | 与企业/产业/门户共用存储；另起一套 Tag UI |
| 推荐/结果工作区 | 共享标题、工具栏宿主、loading/empty/error/permission 容器与区块顺序 | 政策推荐卡、结果卡、画像入口 | 「加入对比篮」写政策文档；「深度分析」直达；页内聚合对比篮按钮；在查询页发起分析或出分析图 |
| 高级筛选 | `FilterPanel` 独立页形态 | 政策字段库、条件、方案、热门 preset | 在蓝色 Hero 内嵌高筛；继承企业/产业 field schema |
| 摘要与后续动作 | 共享 Drawer / 焦点恢复语义 | 政策画像摘要 | 从 Drawer 入篮/「深度分析」直达分析页；跳展示系统政策跟踪 |

共享层只拥有结构、可访问性和状态宿主，不拥有领域字段、数据、权限结论或业务动作。视觉一致性不得仅靠复制 CSS 达成。

## 6. 跨模块边界

| 来源或去向 | 可携带内容 | 不可携带 / 不可承担内容 |
| --- | --- | --- |
| 产业查询 → 系统对比篮·产业 Tab | `industry_id` 信封字段、来源路由/条件摘要 | 政策文档入篮；分析配置；页内第二套篮 UI |
| 系统对比篮产业 Tab → 三项分析 | 勾选 1 个产业、`object_type=industry`、任务类型 | 篮内分析结果；产业链对象发起政策三项；跨 Tab 混选 |
| 三项分析 → 系统对比篮 | `open_compare_basket=1` + `compare_object_type=industry` 原位展开 | 页内第二套篮；清空篮内容作为「返回」 |
| 政策查询 / 门户 → 三项分析 | **禁止直达**；须经产业对比篮分发 | 政策文档入篮；携带 policy_ids 跳分析页 |
| 三项分析 → 系统任务浮层 | 提交 analysis/report；`task_id` 恢复 | 不自建政策任务队列/下载中心 |
| 系统任务浮层 → 三项分析 | 恢复过程/结果/报告弹层或路由 | 不改写业务结论；不自动跳过「查看结果」 |
| 结果页 → 共享报告模板 | `source_task_id` / `source_result_id` / fingerprint / `report_template_id` / 政策章节数据 | 不重复建设模板库、HTML 阅读器与 PDF 管道；禁止跳过 HTML 只出 PDF |
| 三项分析 → 政策查询 | 返回时恢复查询条件与结果焦点 | 分析配置不写回查询方案 |
| 综合智能分析 → 政策分析 | 领域/产业关键词、来源摘要 | 不在本模块生成跨要素综合结论 |
| 政策分析 → 产业链/企业 | 领域上下文 | 不嵌企业画像或产业链图谱编辑；不把政策对象写入企业/产业 Tab |
| 专题政策查询 ↔ 门户政策检索 | 无自动合并 | 路由、storage、菜单必须隔离 |
| 政策分析 ↔ 展示系统政策跟踪 | 无 | 不同系统不同入口 |

## 7. 与 bid-reference 差异说明

| 原始功能 | IA 归位 / 重组方式 | 追溯动作 |
| --- | --- | --- |
| 政策数据自动关联 | 选定产业后任务内自动关联；政策查询为浏览承接 | P-70；不增叶子 |
| 跨区域政策采集 | 对比页筛选区域；采集链路后台 | P-72；P-71 后台 |
| 时序模型智能分析 | 时序分析页 | P-70 |
| 标准化对比 / 三维框架 | 对比页 / 现状页 | P-72 / P-73 |
| 政策密度指数 | 时序页代理指标 | GAP-E7-01 |
| 系统对比篮政策文档 Tab | **已移除**；改为产业 Tab 发起 | DEC-E7-POLICY-LAUNCH-FROM-INDUSTRY-BASKET-20260807 |
| 分析过程 | 复用系统任务浮层 | DEC-E7-SYSTEM-TASK-REUSE-20260805 |
| 报告模板 / HTML / PDF | 统一模板 → HTML 预览 → PDF（ENT-EXPORT） | DEC-E7-REPORT-TEMPLATE-HTML-PDF-20260805；不增叶子 |

## 8. IA 自检

- [x] P-70/P-72/P-73 均有分析落点；对象=产业，系统关联政策。
- [x] 政策查询/门户/产业篮/系统任务/报告职责分离；与展示系统隔离。
- [x] 明确复用查询壳、系统对比篮产业 Tab（政策三项）、系统任务浮层与 ENT-OPS；无政策 Tab；禁止政策文档入篮与查询直达分析。
- [x] 与 TRACE、USM、DEC-E7-POLICY-LAUNCH-FROM-INDUSTRY-BASKET 边界一致；`screen_tier=medium_1440_1920`。
