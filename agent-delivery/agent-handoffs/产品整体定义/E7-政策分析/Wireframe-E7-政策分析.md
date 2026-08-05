# Wireframe-E7-政策分析.md

> **模块**：E7 政策分析  
> **对应 IA**：`IA-E7-政策分析.md`  
> **对应 USM / TRACE**：`USM-E7-政策分析.md` / `TRACE-E7-政策分析.yaml`  
> **阶段**：门 1 PDR 输入；通过后作为 V1 高保真设计基线  
> **版本**：v1.4.3 · 2026-08-05（分析页空态按政策篮有无对象分支引导）  
> **task**：POLICY-PACK-L01

## 1. 页面 / Frame 清单

| Frame | 触发入口 | 目的 | 原始需求 / TRACE |
| --- | --- | --- | --- |
| F-POL-00 政策查询 | 菜单 → `/policy/search` | 发现政策对象；**仅入篮**，不发起分析 | US-E7-POL-01 · DEC-E7-BASKET-ONLY-LAUNCH |
| F-POL-CMP 系统对比篮·政策 Tab | 系统 Shell 浮层 `active_type=policy` | 暂存政策文档并分发三项分析 | US-E7-POL-05 · DEC-E7-COMPARE-ACTIVATE-20260805 |
| F-POL-PORTAL 门户政策扶持展示 | `/policy-portal/*` | 展示浏览；加入/移出对比篮 | P-17~P-22 / US-E7-POL-08 |
| F-POL-01 政策时序分析 | **仅**对比篮分发（菜单进为空态）→ `/policy/overview` | 配置→任务→结果→报告（时序） | P-70 / US-E7-POL-02 |
| F-POL-02 区域政策对比 | **仅**对比篮分发 → `/policy/analysis` | 配置→任务→结果→报告（区域） | P-72 / US-E7-POL-03 |
| F-POL-03 深圳政策现状分析 | **仅**对比篮分发 → `/policy/recommendation` | 配置→任务→结果→报告（三维） | P-73 / US-E7-POL-04 |
| F-POL-OPS 维护管理 | `/policy/maintenance` | 复用 ENT-OPS 三组菜单 | US-E7-POL-09 · DEC-E7-OPS-REUSE |
| F-POL-TASK 系统任务过程与恢复 | `app-shell#system-task-layer`；分析页过程态 | 阶段过程、恢复、queued 撤回 | US-E7-POL-06 · DEC-E7-SYSTEM-TASK-REUSE-20260805 · `SYS-ANALYSIS-JOBS` |
| F-POL-REPORT 报告模板与 HTML/PDF | 结果页「生成报告」→ HTML 预览 → PDF | 统一模板；先预览后下载 | US-E7-POL-07 · ENT-EXPORT · DEC-E7-REPORT-TEMPLATE-HTML-PDF |

`review_trace_applicability: applicable`。

三项计算型分析统一状态机（与企业评估 / 产业链专题分析同合同）：

```text
object_empty → draft → validating → created → prechecking → queued → running
                                      └──────────────→ failed / terminated
queued → withdrawn
running → succeeded --显式查看结果→ result_available → result_readonly --生成报告→ report_handoff
```

统一壳层插槽（复用，不复制企业/产业字段）：

```text
ConfigView → ProcessingView(StageSteps) → ResultView → [生成报告]
```

| 插槽 | 统一规则 | 政策差异 |
| --- | --- | --- |
| `task_summary` | task_id / 类型 / 对象摘要 / 状态 / 队列或已用时 | 政策 analysis_type + 配置快照 |
| `stage_steps` | 完成/进行/等待/失败；**禁止**虚构百分比 | 注册政策阶段文案（关联/建模/计分等） |
| `result_action` | 仅 succeeded 启用「查看结果」；不自动跳 | 各分析页 result_route |
| `report_action` | 仅成功且有效结果「生成报告」 | `*_report` + fingerprint |

壳层布局、队列槽位、与对比篮互斥展开归属 `SystemTaskLayer` / `SYS-ANALYSIS-JOBS`；本包只定义政策注册键与页面落点。

---

## 2. F-POL-00 政策查询（共享查询页面模式）

### 2.1 线框图

```text
┌─ 政策查询主页面 /policy/search ─────────────────────────────────────┐
│ [智能检索] [查政策] [高级筛选→]                                      │
│ 关键词查询区（SearchHub）                                            │
│ SmartChip 已匹配关键词（可逐项关闭）                                   │
│ 示例查询 · 热门政策→                                                 │
│ 最近检索（RecentSearchPanel · 当前模式）                               │
│ 推荐政策 / 结果列表（ElementSearchWorkbench 结果宿主）                 │
│   政策卡 · 查看摘要 · [加入对比篮|已加入]（无深度分析）                  │
│ （工具栏禁止常驻「对比篮」聚合按钮；管理入口=系统 Shell）               │
└─────────────────────────────────────────────────────────────────────┘
             │ 高级筛选 / 热门政策（携带 preset）
             ▼
┌─ 政策查询 / 高级筛选 /policy/search?mode=advanced ──────────────────┐
│ 面包屑：政策查询 / 高级筛选                                          │
│ FilterPanel：左侧字段库 · 右侧条件 · 方案 · Footer 应用/编辑         │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 企业 / 产业查询共享复用矩阵

| 区域 / 能力 | 共享承载 | 政策注入 | 禁止行为 |
| --- | --- | --- | --- |
| 普通查询工作台 | `ElementSearchWorkbench`；固定模式栏、输入/反馈、快捷入口、最近检索、推荐/结果顺序与稳定容器 | 页面标识「政策查询」、模式标签、placeholder、示例和热门项 | 复制 Hero、最近检索或结果容器形成政策私有平行结构 |
| 检索中枢 | 泛化 `SearchHub`；Arco 搜索框、模式 Tab、SmartChip 宿主、示例与热门入口 | `smart / policy / advanced`；政策 parser；热门跳转 | 继承「查企业/查产业」文案、企业/产业 test id 或字段 |
| 最近检索 | `RecentSearchPanel`；当前模式过滤、标题去重、最多 10 条、30 天、恢复重跑、清除 | storage：`gkx-policy-search-recents:v1` | 与企业/产业/门户共用存储；另起一套 Tag UI |
| 推荐/结果工作区 | 共享标题、说明、工具栏宿主、loading/empty/error/permission 容器和区块顺序 | 政策推荐卡、结果卡、选择、加入对比篮 | 「深度分析」直达；页内聚合对比篮按钮；在查询页发起分析 |
| 高级筛选 | 现有 `FilterPanel` 页面形态 | 政策字段库（产业/技术领域/区域/时间/类型/效力层级/发布机关等）、方案、热门 preset | 在蓝色 Hero 内嵌高筛；继承企业/产业 field schema |
| 摘要与后续动作 | 共享 Drawer / 焦点恢复语义 | 政策画像摘要；入篮 | Drawer「深度分析」直达；跳展示系统政策跟踪；Drawer 未关闭时叠加对比篮 |
| 系统对比篮 | 系统 Shell 浮层（`ENT-COMPARE` 壳） | 激活 `policy` Tab：存储、X/50、分发三任务 | 政策模块内再做一个篮页面；篮内出分析图 |

共享层只拥有结构、可访问性和状态宿主，不拥有领域字段、数据、权限结论或业务动作。企业、产业、政策页面必须通过同一共享组件挂载点消费该结构；视觉一致性不得仅靠复制 CSS 达成。

### 2.3 字段与模式规则

| 模式 | 召回口径 | URL | 禁止行为 |
| --- | --- | --- | --- |
| 智能检索 | 多字段可解释匹配（标题/机关/类型/区域/关键词等）；非 LLM | `?mode=smart` | 承诺自然语言大模型理解 |
| 查政策 | 仅政策标题/名称类关键词模糊查询 | `?mode=policy` | 检索曾用编号以外的隐式全字段并伪装为「查政策」 |
| 高级筛选 | 字段条件构造；需应用后执行 | `?mode=advanced` | Hero 内嵌条件编辑器；自动应用热门 preset |

| 触发 | 页面行为 | 不应发生的行为 |
| --- | --- | --- |
| 智能检索提交 | 框下显示字段化 SmartChip；结果按全部 Tag 匹配 | 在结果卡重复匹配关键词说明 |
| 移除 SmartChip | 按剩余 Tag 立即重算 | 清空其它条件或要求重点搜索按钮 |
| 高级筛选 / 热门政策 | 进独立高筛页；热门预置可编辑条件 | 未应用即出结果；写入最近检索 |
| 有效执行查询 | 写入当前模式最近检索；去重置顶≤10 | 跨模式混显历史 |
| 加入对比篮 | 按 `policy_id` 写入政策 Tab；按钮切「已加入」；Shell 角标同步；停留原页 | 跳独立篮页；工具栏出现第二套数量 |
| 已加入 | 可按既有契约移除并回到「加入对比篮」 | 伪造未入篮状态 |
| 清空输入 | 回推荐/初始态 | 删除全部最近检索（清除历史用专门「清除」）；清空对比篮 |
| 任何「深度分析」/直达分析 | **禁止** | 引导加入对比篮后由系统篮发起 |

### 2.4 状态

| 状态 | 表现 | 用户下一步 |
| --- | --- | --- |
| 初始/推荐 | 确定性推荐政策 + 理由（不冒充实时排序） | 点卡摘要或开始检索 |
| loading | 卡片骨架 | 等待 |
| 结果 | 结果列表 + 工具栏（按能力） | 选择 / 加入对比篮 |
| empty（已执行零命中） | 模式对应空态；不回退伪造成功 | 调整或清空 |
| error / permission | 错误条或锁态卡 | 重试 / 申请 |

### 2.5 review mounts（F-POL-00）

```yaml
  - mount_id: E7-POL-F00-PAGE-TITLE-TRACE
    frame_id: F-POL-00
    host_label: 政策查询评审页头（标题和说明）
    marker_type: requirement_trace
    source_relation: product_interpretation
    trace_refs: ["§1.1.1.2.4.2.6.1.1", DEC-E7-SEARCH-REUSE-20260805]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: E7-POL-F00-MOCK
    frame_id: F-POL-00
    host_label: 推荐/结果批次
    marker_type: mock_badge
    source_relation: product_interpretation
    trace_refs: [batch=mock_20260623]
    required_payload: [is_mock, batch_id]
    review_mode: present
    business_mode: absent
```

---

## 3. Frame：F-POL-CMP 系统对比篮 · 政策 Tab

> 壳层布局、拖动避让、与任务窗互斥展开等继承 `ENT-COMPARE` / `UX-SPEC-ENT-COMPARE`。本 Frame 只描述**政策 Tab 激活后**的内容与分发。

### 3.1 线框图

```text
┌─ 系统对比篮浮层（非模态）──────────────────────────────────────────┐
│ 对比篮 · 共 N 项（含政策）                              [⋯] [收起] │
│ [企业 x/50] [产业…] [政策 X/50] [服务机构] [区域]   ← 政策非「开发中」│
├────────────────────────────────────────────────────────────────────┤
│ 搜索/轻筛 · 全选当前筛选 · 列表（政策标题/级别/类型/地区/来源）     │
│ 已选 X 份 · [取消选择]                                              │
├────────────────────────────────────────────────────────────────────┤
│ [清空本 Tab]                         [发起分析]                     │
└────────────────────────────────────────────────────────────────────┘
        │ 发起分析
        ▼
┌─ 选择分析任务 ─────────────────────────────────────────────────────┐
│ ○ 政策时序分析 → /policy/overview                                   │
│ ○ 区域政策对比 → /policy/analysis                                   │
│ ○ 深圳政策现状分析 → /policy/recommendation                         │
│                              [取消] [下一步：前往配置]               │
└────────────────────────────────────────────────────────────────────┘
```

### 3.2 字段与规则

| 字段 / 区块 | 规则 | metric_id |
| --- | --- | --- |
| `object_type` | 固定 `policy` | — |
| `object_id` / `policy_id` | 稳定唯一键；去重 | — |
| `display_name` | 政策标题 | — |
| `level` / `type` / `region` | 列表摘要；可轻筛 | — |
| `source_route` / `source_context` | 来源可追溯；卡片默认折叠详情 | — |
| Tab 计数 | `X/50`；角标「共 N 项」须计入政策 | 交互计数，非业务 KPI |
| 分析配置 | **不进篮**（领域对标、粒度、权重在目标页） | — |

### 3.3 交互

| 触发 | 页面行为 | 禁止 |
| --- | --- | --- |
| 打开政策 Tab | 显示可操作列表，不再显示「政策对比篮开发中」空页 | 继续用 developing 占位冒充已交付 |
| 发起分析 | 仅三任务；校验数量与类型后分发 | 跨 Tab 混选；篮内出图 |
| 目标分析页无分发上下文空态（对比篮能力） | 读政策 Tab 可用数：`0`→只引导查询入篮；`≥1`→引导查询入篮或打开对比篮 | 空篮仍给「打开对比篮」主 CTA；分析页自建对象选择器 |
| 下一步成功 | 收起面板、保留入口、写 `return_context_id` | 清空篮内容 |
| 取消/失败 | 面板保持展开 | 静默跳转 |
| 目标页调整对象 | `open_compare_basket=1&compare_object_type=policy` 原位展开 | 政策模块内嵌第二套篮页 |

### 3.4 review mount

```yaml
  - mount_id: E7-POL-FCMP-POLICY-TAB-TRACE
    frame_id: F-POL-CMP
    host_label: 政策 Tab 标题区
    marker_type: requirement_trace
    source_relation: product_interpretation
    trace_refs: [DEC-E7-COMPARE-ACTIVATE-20260805, ASC-ENT-COMPARE-MULTI-OBJECT-SHELL-20260731]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
```

---

## 4. Frame：F-POL-01 政策时序分析

`analysis_type=policy_timeseries_analysis` · `report_task_type=policy_timeseries_analysis_report`

### 4.1 线框图（配置 / 结果）

```text
┌─ ContextBar：对象/领域摘要 · 来自查询或对比篮 · [返回政策查询]      │
│              [调整对象→系统对比篮]                                   │
│ 政策时序分析 ⓘtrace                    [粒度:年|季|月]              │
│                                              [生成分析]              │
├─ 配置态 ───────────────────────────────────────────────────────────┤
│ 关联政策概要：N 条 · 批次 🧪mock · 粒度与条件摘要                     │
├─ 结果态（显式查看结果后）──────────────────────────────────────────┤
│ 结果身份：对象 / 配置 / 模型 / 数据批次 / 生成时间（只读）           │
│ 发布数量时序 ⓘmetric  │ 支持强度趋势 ⓘmetric                        │
│ 关键节点时间轴 · 节点政策明细表                                       │
│                                              [生成报告]              │
└────────────────────────────────────────────────────────────────────┘
```

过程态见 `F-POL-TASK`；报告见 `F-POL-REPORT`。ContextBar **无**页内「导出」；交付物走系统报告合同。

### 4.2 区块、字段与指标

| 区块 / 控件 | 用户目的 | 字段 / metric_id | 默认与联动规则 |
| --- | --- | --- | --- |
| ContextBar | 确认篮分发上下文 | `domain` / `policy_ids` / 条件摘要 / `return_context_id` | 无分发上下文→对象空态（见 §4.3） |
| 调整对象 | 原位打开系统对比篮政策 Tab | `open_compare_basket=1&compare_object_type=policy` | **不是**页内第二套篮 |
| 时序粒度 | 配置聚合窗口 | `granularity∈{year,quarter,month}` | 默认 `year`；提交后写入任务配置快照 |
| 生成分析 | 创建系统 analysis 任务 | `policy_timeseries_analysis` | 同类型已有进行中→引导恢复，不新建 |
| 发布数量时序 | 看演进密度 | `M_POLICY_TOTAL_COUNT`（代理密度，GAP-E7-01） | 结果只读；随任务配置 |
| 支持强度趋势 | 看力度变化 | `M_POLICY_INTENSITY_SCORE` / `M_POLICY_INTENSITY_INDEX` | ⚠️ QPOL-02 |
| 关键节点 / 明细 | 识别窗口期 | `node_*` + 政策行 | 点选驱动明细 |
| 生成报告 | 进入报告故事 | `policy_timeseries_analysis_report` | 仅成功且有效结果；见 F-POL-REPORT |

### 4.3 交互与状态

| 触发 / 状态 | 页面行为 | 禁止 / 下一步 |
| --- | --- | --- |
| 无分发上下文 + 政策篮空 | 对象空态；主 CTA **仅**「去政策查询入篮」 | 伪造全库；提供无效的「打开对比篮」主 CTA；页内第二套篮 |
| 无分发上下文 + 政策篮有对象 | 对象空态；主 CTA「去查询入篮」**与**「打开对比篮」（系统浮层 `active_type=policy`） | 假装已分发进入配置态；私有对象 Select |
| 生成分析 | 进 ProcessingView（F-POL-TASK） | 页内 Spinner 冒充过程；完成自动跳结果 |
| 切换粒度（配置态） | 仅改草稿 | 静默改写已成功结果 |
| 点选节点（结果态） | 明细刷新 | 跳转展示系统政策跟踪 |
| 生成报告 | 系统 report 任务 | 查询页/篮内直接出正式报告；页内私有下载中心 |
| loading/empty/error/无权限 | 同模块通用模式 | 重试 / 回查询 / 申请 |

---

## 5. Frame：F-POL-02 区域政策对比

`analysis_type=policy_region_compare` · `report_task_type=policy_region_compare_report`

### 5.1 线框图

```text
┌─ ContextBar：对象/领域摘要 · [返回政策查询] [调整对象→系统对比篮]   │
│ 区域政策对比 ⓘtrace   [区域多选] [视图:矩阵|雷达|热力]  [生成分析] │
├─ 结果态 ───────────────────────────────────────────────────────────┤
│ 结果身份（只读）                                                     │
│ 对比矩阵 ⓘmetric · 雷达 / 热力 · 差异结论 · 结构化条款明细         │
│                                              [生成报告]              │
└────────────────────────────────────────────────────────────────────┘
```

### 5.2 字段与指标

| 区块 | metric_id / 字段 | 规则 |
| --- | --- | --- |
| 区域多选 | `region_codes[]` | 默认长三角、粤港澳大湾区；提交写入任务快照 |
| 矩阵/图 | `M_POLICY_SUPPORT_STRENGTH`, `M_POLICY_INDUSTRY_FIT`, `M_POLICY_IMPLEMENTATION_EFFECT`, `M_POLICY_INTENSITY_SCORE` | 结果只读；⚠️ QPOL-02/03/05 |
| 国际政策 | — | 默认不并入综合分（QPOL-05）；评审 ⚠️ |
| 生成报告 | `policy_region_compare_report` | 仅有效结果；F-POL-REPORT |

交互：切换视图不改数字；区域为空不创建任务；不打开门户政策页；无页内「导出」。

---

## 6. Frame：F-POL-03 深圳政策现状分析

`analysis_type=policy_sz_3d_assessment` · `report_task_type=policy_sz_3d_assessment_report`

### 6.1 线框图

```text
┌─ ContextBar：对象/领域摘要 · [返回政策查询] [调整对象→系统对比篮]   │
│ 深圳政策现状分析 ⓘtrace                                              │
├─ 配置态 ───────────────────┬───────────────────────────────────────┤
│ 三维框架（指标+权重=100%）  │ 校验反馈                                │
│                            │                         [生成分析]     │
├─ 结果态 ───────────────────┴───────────────────────────────────────┤
│ 结果身份 · 仪表盘 + 三数字卡片 ⓘmetric · 优势/短板雷达               │
│ 短板成因下钻 · 优化策略建议卡                          [生成报告]    │
└────────────────────────────────────────────────────────────────────┘
```

### 6.2 字段与指标

| 区块 | metric_id | 规则 |
| --- | --- | --- |
| 支持力度 / 产业适配性 / 落地实效性 | `M_POLICY_SUPPORT_STRENGTH` / `M_POLICY_INDUSTRY_FIT` / `M_POLICY_IMPLEMENTATION_EFFECT` | 权重合计 100%；⚠️ QPOL |
| 短板数 / 建议数 | `M_POLICY_SHORTBOARD_COUNT` / `M_POLICY_LAYOUT_REC_COUNT` | 点选下钻 |
| 生成报告 | `policy_sz_3d_assessment_report` | 仅有效结果；P-74/P-75 独立报告页 Wave2，本页不宣称关闭 |

权重≠100% **不创建任务**；算分走 API，禁止前端杜撰公式；无页内「导出」。

---

## 6b. Frame：F-POL-TASK 系统任务过程与恢复

> 共享真源：`SYS-ANALYSIS-JOBS` / `SystemTaskLayer`；企业评估与产业链分析已落地。本 Frame 只写政策接入落点。

### 6b.1 线框图

```text
┌─ 分析页内 ProcessingView ──────────────────────────────────────────┐
│ 任务摘要：政策时序分析 · 对象摘要 · task_id · 状态 · 队列/已用时     │
│ StageSteps：预检 → 排队 → 政策关联 → 时序建模 → 完成（示例阶段）     │
│ CurrentStageAlert：当前阶段说明 · 可离开，后台继续                   │
│ [稍后查看]（离页不终止）  queued 时 [撤回任务]（二次确认）            │
│ succeeded 后 [查看结果]（显式，不自动跳）                            │
└────────────────────────────────────────────────────────────────────┘
        ▲ 恢复
┌─ 系统任务浮层（App Shell，收起/展开）──────────────────────────────┐
│ 政策 analysis / report 条目 · 状态 · [进入过程|查看结果|查看报告]   │
│ 与对比篮入口同屏可并存；同一时间只展开一个面板                       │
└────────────────────────────────────────────────────────────────────┘
```

| 规则 | 合同 |
| --- | --- |
| 生命周期 | created / prechecking / queued / running / succeeded / failed / withdrawn |
| 撤回 | 仅 queued + 发起人；→ withdrawn，不产结果 |
| running | 普通用户无取消；离页不终止 |
| 失败/终止 | 只可复制配置为新草稿 + 新 task_id |
| 并发 | 同 analysis_type 最多 1 个进行中；全局上限读服务端配置 |
| 禁止 | 政策私有任务中心；虚构百分比；完成后自动跳结果 |

阶段文案必须按政策类型注册，不得照搬「企业数据汇聚」等企业文案。

---

## 6c. Frame：F-POL-REPORT 统一报告模板 · HTML 预览 · PDF

> 共享能力 ③：`ENT-EXPORT`（企业/产业链已落地）。决策：`DEC-E7-REPORT-TEMPLATE-HTML-PDF-20260805`。

### 6c.1 线框图

```text
┌─ 结果页动作条 ─────────────────────────────────────────────────────┐
│ [查看配置] [生成报告] / [查看报告]                                   │
└────────────────────────────────────────────────────────────────────┘
                              ▼ report 任务（统一模板装载章节）
┌─ 系统性 HTML 预览页（必经）────────────────────────────────────────┐
│ 报告身份：template_id · fingerprint · revision · 生成时间            │
│ 目录 · 章节正文（政策域注入）· 来源/局限说明                         │
│ [返回结果] [下载 PDF]（与本 HTML 同一 revision）                     │
└────────────────────────────────────────────────────────────────────┘
                              ▼
┌─ PDF 产物（A4，同源修订）──────────────────────────────────────────┐
│ 下载 / 权限复核 / 过期重生成（HTML 仍可读）                          │
└────────────────────────────────────────────────────────────────────┘
```

| 规则 | 合同 |
| --- | --- |
| 模板 | 系统统一模板形态；政策绑定 `report_template_id` + 章节 payload |
| 顺序 | **必须先 HTML 预览，再 PDF**；禁止跳过 HTML 仅交付 PDF |
| 同源 | HTML 与 PDF 同一 `report_revision_id` / fingerprint |
| 入口 | 仅成功且有效结果页「生成报告」 |
| 复用 | 同 fingerprint 复用进行中/已完成报告任务 |
| 过期源结果 | 不可新开正式报告；分析结果仍可读 |
| PDF 缺失 | HTML 可继续读；授权下重生成 PDF |
| 框架未激活 | 失败关闭并说明（GAP-E7-06）；保留结果阅读 |
| V1 格式 | 仅 HTML + PDF（无 DOCX/PPTX） |
| 禁止 | 查询/篮内生成报告；私有阅读器/PDF 引擎；结果/报告收藏 |

---

## 7. 响应式与视觉约束

- **屏幕层级**：`medium_1440_1920`；不提供 small / 大屏轨。
- **设计系统**：`Design.md` + Arco；主色 `#165DFF`，页底 `#D8E7FC`。
- **查询壳**：蓝色搜索主视觉仅用于 `/policy/search` 普通模式；高筛页保持浅色工作台，不继承 Hero。
- **分析页**：ContextBar + Config / Processing / Result；图表 ECharts；任务/报告浮层走系统 Shell。

---

## 8. review_trace_contract（分析页）

```yaml
review_trace_contract:
  # F-POL-00 见 §2.5；F-POL-CMP 见 §3.4
  - mount_id: E7-POL-F01-PAGE-TITLE-TRACE
    frame_id: F-POL-01
    host_label: 页面标题「政策时序分析」
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [P-70, "§1.1.1.2.4.2.6.1"]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: E7-POL-F01-COUNT-METRIC
    frame_id: F-POL-01
    host_label: 发布数量时序标题
    marker_type: metric_spec
    source_relation: direct_requirement
    trace_refs: [M_POLICY_TOTAL_COUNT]
    required_payload: [metric_id, metric_name_zh, definition, formula, source_tables, source_systems, update_freq, version]
    review_mode: present
    business_mode: absent
  - mount_id: E7-POL-F01-INTENSITY-METRIC
    frame_id: F-POL-01
    host_label: 支持强度趋势标题
    marker_type: metric_spec
    source_relation: direct_requirement
    trace_refs: [M_POLICY_INTENSITY_SCORE]
    required_payload: [metric_id, metric_name_zh, definition, formula, source_tables, source_systems, update_freq, version]
    review_mode: present
    business_mode: absent
  - mount_id: E7-POL-F01-MOCK
    frame_id: F-POL-01
    host_label: 关联政策概要批次
    marker_type: mock_badge
    source_relation: product_interpretation
    trace_refs: [batch=mock_20260623]
    required_payload: [is_mock, batch_id]
    review_mode: present
    business_mode: absent
  - mount_id: E7-POL-F02-PAGE-TITLE-TRACE
    frame_id: F-POL-02
    host_label: 页面标题「区域政策对比」
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [P-72, "§1.1.1.2.4.2.6.2"]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: E7-POL-F02-MATRIX-METRIC
    frame_id: F-POL-02
    host_label: 对比矩阵标题
    marker_type: metric_spec
    source_relation: direct_requirement
    trace_refs: [M_POLICY_SUPPORT_STRENGTH, M_POLICY_INDUSTRY_FIT, M_POLICY_IMPLEMENTATION_EFFECT]
    required_payload: [metric_id, metric_name_zh, definition, formula, source_tables, source_systems, update_freq, version]
    review_mode: present
    business_mode: absent
  - mount_id: E7-POL-F02-MOCK
    frame_id: F-POL-02
    host_label: 对比结果批次
    marker_type: mock_badge
    source_relation: product_interpretation
    trace_refs: [batch=mock_20260623]
    required_payload: [is_mock, batch_id]
    review_mode: present
    business_mode: absent
  - mount_id: E7-POL-F02-PENDING-QPOL
    frame_id: F-POL-02
    host_label: 国际政策口径说明
    marker_type: pending_badge
    source_relation: product_interpretation
    trace_refs: [QPOL-05]
    required_payload: [question_id, temporary_default]
    review_mode: present
    business_mode: absent
  - mount_id: E7-POL-F03-PAGE-TITLE-TRACE
    frame_id: F-POL-03
    host_label: 页面标题「深圳政策现状分析」
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [P-73, "§1.1.1.2.4.2.6.3"]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: E7-POL-F03-DIM-METRIC
    frame_id: F-POL-03
    host_label: 三维数字卡片组
    marker_type: metric_spec
    source_relation: direct_requirement
    trace_refs: [M_POLICY_SUPPORT_STRENGTH, M_POLICY_INDUSTRY_FIT, M_POLICY_IMPLEMENTATION_EFFECT]
    required_payload: [metric_id, metric_name_zh, definition, formula, source_tables, source_systems, update_freq, version]
    review_mode: present
    business_mode: absent
  - mount_id: E7-POL-F03-SHORTBOARD-METRIC
    frame_id: F-POL-03
    host_label: 短板数
    marker_type: metric_spec
    source_relation: direct_requirement
    trace_refs: [M_POLICY_SHORTBOARD_COUNT]
    required_payload: [metric_id, metric_name_zh, definition, formula, source_tables, source_systems, update_freq, version]
    review_mode: present
    business_mode: absent
  - mount_id: E7-POL-F03-MOCK
    frame_id: F-POL-03
    host_label: 评估结果批次
    marker_type: mock_badge
    source_relation: product_interpretation
    trace_refs: [batch=mock_20260623]
    required_payload: [is_mock, batch_id]
    review_mode: present
    business_mode: absent
  - mount_id: E7-POL-F03-PENDING-WEIGHT
    frame_id: F-POL-03
    host_label: 权重配置区
    marker_type: pending_badge
    source_relation: product_interpretation
    trace_refs: [QPOL-02]
    required_payload: [question_id, temporary_default]
    review_mode: present
    business_mode: absent

entry_marker_projection: "D1 definition → DataHealthBadge(D2+D3) → D4 ingestion; max_markers: 3; spacing_px: 4"
mode_invariant: 评审模式不得改变查询结果、得分、区域选择、权重或权限；业务模式不渲染上述挂载
```

### 禁止挂载位置

- 不在图表绘图区叠发散标签。
- 不在 PDF/报告正文强制插入评审挂载。
- 不把 `pending_badge` 做成阻断主路径的模态。

---

## 9. 模块排除

- 展示系统科创政策全景 / 分析评价 / 效果推演 / 核增政策对比结果 UI
- 查询/门户「深度分析」或绕过对比篮发起分析
- 为政策另起一套私有查询壳或第二套对比篮页面
- 复制企业 ENT-OPS 的企业字段/内容类型而不替换为政策域
- 页内常驻聚合「对比篮 / 查看对比篮」按钮（管理入口仅系统 Shell）
- 在对比篮内生成时序/对比/三维分析结果或正式报告
- 独立政策任务中心、私有下载中心、结果/报告收藏
- 页内「导出」替代系统 report 任务；虚构百分比进度
- 前端「一键训练 NLP」或直连图数据库
- 小屏专用导航或大屏投屏壳

## 10. Wireframe 自检

- [x] F-POL-00 与企业/产业查询复用矩阵完整。
- [x] F-POL-CMP 激活预留政策 Tab：入篮、容量、分发三任务、无分析图。
- [x] 分析仅由系统对比篮发起；查询/门户无深度分析直达。
- [x] 分析页无分发上下文空态按政策篮有无对象分支（空篮仅查询；有对象可开篮）。
- [x] 分析页仅通过系统浮层调整对象，无页内第二套篮。
- [x] F-POL-PORTAL 入篮合同与 F-POL-OPS ENT-OPS 复用已定义。
- [x] F-POL-TASK / F-POL-REPORT 对齐系统任务与 ENT-EXPORT（模板→HTML→PDF）；分析页无页内导出。
- [x] 每个分析 Frame 对应 IA / USM；无上下文空态已定义。
- [x] 统计字段含 metric_id 或 GAP。
- [x] 默认/加载/空/错误/无权限已覆盖。
- [x] `review_trace_contract` mount_id 唯一。
- [x] 未引入门户/展示系统页面。
