# Wireframe-ENT-RECRUIT.md

> **模块**：引育推荐（ENT-RECRUIT / E-26 / E-27）
> **对应 IA**：`IA-ENT-RECRUIT.md`
> **对应 USM / TRACE**：`USM-ENT-RECRUIT.md` / `TRACE-ENT-RECRUIT.yaml`
> **版本**：v1.6 · 2026-07-23
> **阶段**：`v1_hifi_round1`；核心产品包修订稿，用于 UX 深化与 V1 高保真首轮评审，不代表门 1 PDR 已闭合

## 1. 页面 / Frame 清单

| Frame | 触发入口 | 目的 | 原始需求 / TRACE |
| --- | --- | --- | --- |
| `F-RECRUIT-A-CONFIG` 招引推荐条件 | 引育推荐 → 招引推荐 | 设置全国企业筛选条件并显式执行分析 | E-26 / `US-ENT-RECRUIT-A1` |
| `F-RECRUIT-A-RESULT` 招引推荐结果 | 招引分析成功 | 查看完整优选企业清单、稳定分页、排名、联动详情、企业风险与信用复核、报告和导出 | E-26 / `US-ENT-RECRUIT-A2/A3/R1`；`US-ENT-RECRUIT-R2` 为已批准产品增强 |
| `F-RECRUIT-C-CONFIG` 培育推荐条件 | 引育推荐 → 培育推荐 | 设置深圳市内企业筛选条件并显式执行分析 | E-27 / `US-ENT-RECRUIT-C1` |
| `F-RECRUIT-C-RESULT` 培育推荐结果 | 培育分析成功 | 查看完整企业排名、稳定分页、行业分布、联动详情、企业风险与信用复核、报告和导出 | E-27 / `US-ENT-RECRUIT-C2/C3/R1`；`US-ENT-RECRUIT-R2` 为已批准产品增强 |
| `F-RECRUIT-CANDIDATES` 引育候选工作台 | 招引 / 培育视图 → 候选工作台，或跨模块加入后到达 | 管理人工线索、发起指定对象复核、送入对比篮研判并人工确认 | `US-ENT-RECRUIT-L1/L2/L3` · 已批准产品解释 / 增强 |
| `F-RECRUIT-PROCESS` 可视化分析过程 | 招引 / 培育点击执行推荐分析 | 展示统一五阶段、当前阶段和后台继续 / 恢复入口 | `US-ENT-RECRUIT-R3` · `DEC-SYS-ANALYSIS-JOBS-20260723` |
| `F-RECRUIT-SERVICE-CONTRACT` 模型服务契约 | 评审模式服务契约摘要；业务模式不渲染 | 追溯 RESTful API、SDK、在线平台三种调用形态及架构边界 | `DR-ENT-RECRUIT-A-09/C-09` · 直接需求 |

> 前六个 Frame 共享 `/enterprise/recommendation` 页面壳层；`F-RECRUIT-SERVICE-CONTRACT` 是非业务页面契约 Frame。“招引 / 培育”是独立产品状态，不预先锁定 URL 参数实现。

## 2. 页面壳层

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ 企业分析 / 引育推荐                                                        │
│ [招引推荐 E-26] [培育推荐 E-27]                                           │
│ [条件筛选推荐] [候选工作台]                                        │
├────────────────────────────────────────────────────────────────────────────┤
│ 当前视图的分析条件 / 结果 / 详情 / 报告与导出                              │
└────────────────────────────────────────────────────────────────────────────┘
```

| 控件 | 用户目的 | 默认与联动规则 | 禁止行为 |
| --- | --- | --- | --- |
| 招引 / 培育视图切换 | 选择业务任务 | 只切换当前视图；分别保留各自未提交条件 | 不把全国 / 深圳范围、筛选、指标和结果互相复制 |
| 页面标题与对象范围 | 确认当前分析语境 | 招引显示“全国企业”；培育显示“深圳市内企业” | 不用模糊“企业范围”隐藏差异 |
| 条件筛选推荐 / 候选工作台 | 选择对象获取方式 | 条件筛选从全量对象池优选；候选工作台只处理人工线索 | 不把人工线索标为已推荐，不共享招引 / 培育候选集合 |
| 数据更新时间 | 判断结果时效 | 成功或部分缺失状态显示服务端时间 | 不由前端推算或伪造 |

## 3. F-RECRUIT-A-CONFIG 招引推荐条件

### 3.1 线框图

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ 招引推荐 · 全国企业                                  [切换到培育推荐]      │
├────────────────────────────────────────────────────────────────────────────┤
│ 企业标签 [选择]   目标特征 [高成长/关键技术/隐形冠军/专精特新]             │
│ 行业领域 [选择]   地域来源 [选择]                                      │
│                                                                            │
│ 综合模型说明：产业相关度 · 政策匹配度 · 深圳连接度                        │
│ 高潜挖掘依据：技术匹配度 · 成长性 · 区域适配性                            │
│                                                        [执行推荐分析]      │
└────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 字段与指标

| 区块 / 控件 | 用户目的 | 字段 / metric_id | 默认与联动规则 |
| --- | --- | --- | --- |
| 企业标签 | 按企业特征筛选 | 对象字段，无 metric_id | 可筛选；具体标签字典由数据契约提供 |
| 目标特征 | 聚焦 Bid 明确的招引对象 | 高成长性、关键技术型、隐形冠军、专精特新；对象 / 认定字段，无统一 metric_id | 认定字典和来源由数据 / 模型契约提供；不用普通企业标签冒充认定 |
| 行业领域 | 限定目标产业领域 | 对象字段，无 metric_id | 可筛选；与培育产业类别不共享选择状态 |
| 地域来源 | 限定全国来源范围 | 对象字段，无 metric_id | 可筛选；不把深圳本地设为招引硬边界 |
| 综合模型说明 | 理解推荐指数构成 | 产业相关度 `M_ENT_INDUSTRY_MATCH_SCORE`（候选校准）；政策匹配度 `M_ENT_POLICY_MATCH_SCORE`；深圳连接度 `GAP-RECRUIT-METRIC-01` | 只读说明，不提供公式 / 权重编辑 |
| 高潜挖掘依据 | 理解企业为何进入推荐 | 技术匹配度、成长性、区域适配性（解释字段） | 只有显示数值时才登记独立 metric_id |
| 执行推荐分析 | 显式产生结果 | 非统计操作 | 接口校验通过后进入 `loading`；bid 未定义的必填条件不在前端臆设 |

### 3.3 交互与禁止行为

| 触发 | 页面行为 | 不应发生的行为 |
| --- | --- | --- |
| 调整筛选 | 更新当前招引条件草稿 | 不自动刷新为新名单，不联动培育条件 |
| 点击执行推荐分析 | 固定本次输入并进入分析中状态 | 不显示上一次结果冒充本次结果，不重复提交 |
| 查看模型说明 | 解释三类核心维度和证据层级 | 不展示未确认公式、阈值或权重编辑器 |

### 3.4 F-RECRUIT-PROCESS 招引 / 培育共用异步过程

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ 可视化分析过程                                                             │
│  ✓ 任务提交 ── ✓ 权限与配置校验 ── ③ 数据汇聚 ── ④ 算法计算 ── ⑤ 结果组装 │
│    已完成           已完成              进行中          等待中         等待中 │
│ ┌────────────────────────────────────────────────────────────────────────┐ │
│ │ 当前阶段：数据汇聚                                                     │ │
│ │ 可离开当前页面，任务将在后台继续；可从系统任务浮层或个人中心恢复。     │ │
│ └────────────────────────────────────────────────────────────────────────┘ │
│                                                               [稍后查看] │
└────────────────────────────────────────────────────────────────────────────┘
```

| 元素 / 操作 | 页面行为 | 禁止行为 |
| --- | --- | --- |
| 五阶段 Steps | 招引与培育均按任务提交、权限与配置校验、数据汇聚、算法计算、结果组装显示已完成 / 进行中 / 等待中 | 不伪造百分比，不省略当前阶段 |
| 当前阶段提示 | 显示排队位置或当前阶段，并说明任务可后台继续 | 不使用旧结果填充过程区 |
| 稍后查看 | 离开当前页面；任务继续运行，可由系统任务浮层或个人中心恢复 | 不取消任务，不丢失当前任务引用 |
| 任务隔离 | 招引与培育使用独立 `task_type` 与恢复路由 | 不共享条件快照、任务或结果 |

## 4. F-RECRUIT-A-RESULT 招引推荐结果

### 4.1 线框图

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ 招引企业推荐分析结果 / 人工线索复核结果 · 分析模式 · 对象范围      │
│ 模型 v… · 数据 v… · 生成时间 · 数据覆盖摘要 · [有可用更新/重新计算中]       │
│ [调整分析条件] [加入对比篮] [导出数据] [生成分析报告]                 │
│ 共分析 X 家 · 当前筛选 Y 家 · 已选 Z 家                                │
│ [企业名称] [行业领域] [地域来源] [目标特征] [重置]                      │
├──────────────────────────────────────────────┬─────────────────────────────┤
│ 优选企业清单（完整结果）                     │ 推荐企业详情                │
│ □ 排名 企业名称 行业领域 地域来源 目标特征 推荐指数 操作 │ 企业名称             │
│ 01   企业 A   领域 A   地区 A   —            │ 产业相关度                  │
│ 02   企业 B   领域 B   地区 B   —            │ 政策匹配度                  │
│ 03   企业 C   领域 C   地区 C   —            │ 深圳连接度                  │
│                                              │ ─────────────────────────  │
│ 企业行业领域排名：GAP 时不展示伪数值         │ 技术匹配度 / 成长性 /       │
│                                              │ 区域适配性证据              │
│                                              │ 目标特征 / 识别依据         │
│                                              │ 核心优势 / 关键指标         │
│                                              │ 企业风险与信用 [查看明细]   │
│                                              │ 合作价值                    │
├──────────────────────────────────────────────┴─────────────────────────────┤
│ 已选 Z 家  [取消选择] [全选当前筛选结果 Y 家] [加入对比篮]               │
│ 共 X 家  [20 条/页 ▾]                         ‹ 1 2 3 ›                   │
└──────────────────────────────────────────────┴─────────────────────────────┘
```

### 4.2 字段与指标

| 区块 | 字段 | 用户目的 | metric_id / 状态 | 表达规则 |
| --- | --- | --- | --- | --- |
| 列表 | 排名 | 判断优先顺序 | 招引推荐指数派生顺序 | 排序范围和并列规则未闭合时标记 GAP |
| 列表 | 企业名称 | 识别对象 | 对象字段 | 不脱离当前结果新增全库搜索 |
| 列表 | 行业领域 | 判断业务领域 | 对象字段 | 与当前行业筛选语义一致 |
| 列表 | 地域来源 | 判断来源区域 | 对象字段 | 不显示培育专属企业规模替代它 |
| 列表 | 招引推荐指数 | 快速排序与复核 | `M_ENT_ATTRACTION_INDEX` · `semantic_revision_required` · Q015 | 现有“生态连接度”须按 bid 校准为“深圳连接度”；缺失不为 0 |
| 列表 / 详情 | 目标特征与识别依据 | 确认企业为何属于 Bid 目标对象 | 对象字段 / 认定证据；数值化时登记 metric_id | 区分高成长、关键技术型、隐形冠军、专精特新；不将自定义标签当作权威认定 |
| 列表 / 补充 | 企业行业领域排名 | 查看企业在领域中的排序 | `GAP-RECRUIT-METRIC-03` | 未明确排名范围、排序字段和并列规则前不显示正式数值 |
| 结果摘要 | 完整结果数 / 当前筛选数 / 已选数 | 理解当前结果和批量范围 | 非指标计数；受权限约束 | 无权限时不泄露数量；筛选不改变完整结果数 |
| 结果内筛选 | 企业名称 / 行业领域 / 地域来源 / 目标特征 | 缩小当前展示集合 | 对象字段，无 metric_id | 只影响展示，不重跑模型、不改变结果版本 |
| 分页 | 页码 / 每页数量 | 稳定浏览完整结果 | 默认 20；选项 20 / 50 / 100 | 服务端稳定分页；保留完整结果原始排名 |
| 详情 | 产业相关度 | 解释产业契合 | `M_ENT_INDUSTRY_MATCH_SCORE` · 候选语义校准 | “产业匹配度”不得未经确认直接改名冒充 |
| 详情 | 政策匹配度 | 解释政策契合 | `M_ENT_POLICY_MATCH_SCORE` · Q015 | 无正式口径时显示 pending |
| 详情 | 深圳连接度 | 解释与深圳经济联系 | `GAP-RECRUIT-METRIC-01` | 不与区域适配性静默合并 |
| 详情 | 技术匹配度 / 成长性 / 区域适配性 | 解释高潜挖掘依据 | 解释字段；数值化时分别登记 metric_id | 可展示证据摘要，不展示伪分数 |
| 详情 | 核心优势 | 判断企业优势 | 文本 / 标签字段 | 需与数据依据绑定，不生成总分 |
| 详情 | 关键指标 | 查看关键事实 | `GAP-RECRUIT-METRIC-05` 动态集合 | 每个统计项携带自身 metric_id |
| 详情标题 / 风险区 | 风险摘要状态 | 快速判断是否需要继续复核 | 非评分状态：存在 N 项需关注 / 当前公开数据未检出 / 风险数据待核验 | 不使用“无风险”，不以颜色或文案暗示法律结论 |
| 详情 / 风险区 | 司法涉诉记录数 | 复核公开司法线索 | `GAP-RECRUIT-RISK-COUNT-01` | 语义与数据映射未闭合前不得显示正式计数；缺失不为 0 |
| 详情 / 风险区 | 失信被执行记录数 | 复核公开失信线索 | `GAP-RECRUIT-RISK-COUNT-02` | 同上；不得把一般司法记录等同失信 |
| 详情 / 风险区 | 经营异常记录数 | 复核公开经营异常线索 | `GAP-RECRUIT-RISK-COUNT-03` | 同上；须显示当前状态与数据更新时间 |
| 详情 / 风险区 | 行政处罚记录数 | 复核公开行政处罚线索 | `GAP-RECRUIT-RISK-COUNT-04` | 同上；不得仅凭数量生成风险等级 |
| 详情 / 风险区 | 最近事件时间 / 摘要 / 查看风险明细 | 了解最新风险线索并进入逐条核验 | 明细字段，无统一 metric_id | 来源覆盖不足时显示“风险数据待核验”；不阻断其他详情 |
| 详情 | 合作价值 | 判断招商合作意义 | 文本字段 | 不自动转为投资结论或落地承诺 |
| 状态条 | 模型版本 / 数据版本 / 生成时间 / 数据覆盖 / 更新状态 | 判断结果时效与可追溯性 | 非指标结果字段 | 有更新时保留旧版本标识；新版完成前不静默替换 |

### 4.3 交互与禁止行为

| 触发 | 页面行为 | 不应发生的行为 |
| --- | --- | --- |
| 选择名单行 | 右侧详情同步切换到该企业 | 不改变推荐结果集合，不重新运行模型 |
| 结果内筛选 | 只缩小当前展示集合并更新“当前筛选 Y 家” | 不重新运行模型、不改变结果版本、不重编号原始排名 |
| 翻页 / 调整每页数量 | 按稳定排序读取对应结果页；默认 20，可切换 20 / 50 / 100 | 不使用无限滚动替代分页，不因翻页清除跨页选择 |
| 表头全选 | 仅选择当前页可选企业 | 不默认选择全部筛选结果 |
| 全选当前筛选结果 | 在底部操作栏明确显示 Y 家并跨页选择 | 不隐藏作用范围，不与当前页全选混淆 |
| 取消选择 | 清除当前跨页选择集合 | 不重置结果内筛选或分析条件 |
| 加入对比篮 | 将选中企业与引育任务上下文写入对比篮，生成 `return_context_id`；超出剩余容量时整批阻断 | 不在对比篮改写招引指数或候选状态，不静默截断 |
| 查看指定对象复核结果 | 显示“人工线索复核结果”和本次指定对象集合 | 不将集合内排名表述为全国全量排名 |
| 查看风险明细 | 打开当前企业的风险明细抽屉，保留名单、筛选、选择和详情上下文 | 不跳转到风险洞察，不改变推荐指数、排名或候选状态 |
| 动态更新状态变化 | 显示新政策 / 新数据触发的“有更新 / 重新计算中 / 已更新”及版本 | 不静默改变指数、排名或分析时间 |
| 调整分析条件 | 返回条件区并保留当前结果，重新执行后再替换 | 不静默实时刷新造成结果语境变化 |
| 生成分析报告 | 当前页面显示生成中 / 可用 / 失败 | 不新增历史任务或资产中心 |
| 导出数据 | 按权限导出当前范围；不超过暂定 1,000 家直接生成，超过后后台生成 | 不预设 bid 未定义的文件格式和字段范围，不创建通用任务中心 |

## 5. F-RECRUIT-C-CONFIG 培育推荐条件

### 5.1 线框图

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ 培育推荐 · 深圳市内企业                              [切换到招引推荐]      │
├────────────────────────────────────────────────────────────────────────────┤
│ 产业类别 [选择]   政策导向 [选择]   企业规模 [选择]                        │
│                                                                            │
│ 综合模型说明：产业相关度 · 政策匹配度 · 企业潜力                          │
│ 本地潜力依据：技术壁垒 · 市场增速 · 团队背景                              │
│                                                        [执行推荐分析]      │
└────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 字段与指标

| 区块 / 控件 | 用户目的 | 字段 / metric_id | 默认与联动规则 |
| --- | --- | --- | --- |
| 产业类别 | 限定培育产业 | 对象字段，无 metric_id | 可筛选；不复用招引行业领域选择状态 |
| 政策导向 | 限定政策方向 | 对象 / 政策字段，无 metric_id | 可筛选；不直接等于政策匹配度数值 |
| 企业规模 | 限定企业范围 | 对象字段，无 metric_id | 可筛选；对象池仍固定为深圳市内企业 |
| 综合模型说明 | 理解推荐指数构成 | 产业相关度 `M_ENT_INDUSTRY_MATCH_SCORE`（候选校准）；政策匹配度 `M_ENT_POLICY_MATCH_SCORE`；企业潜力 `GAP-RECRUIT-METRIC-02` / `M_ENT_GROWTH_POTENTIAL` 候选 | 只读说明，不提供公式 / 权重编辑 |
| 本地潜力依据 | 理解企业为何进入推荐 | 技术壁垒、市场增速、团队背景（解释字段） | 只有显示数值时才登记独立 metric_id |
| 执行推荐分析 | 显式产生结果 | 非统计操作 | 接口校验通过后进入 `loading` |

### 5.3 交互与禁止行为

| 触发 | 页面行为 | 不应发生的行为 |
| --- | --- | --- |
| 调整筛选 | 更新当前培育条件草稿 | 不改变深圳市内企业硬边界，不联动招引条件 |
| 点击执行推荐分析 | 固定本次输入并进入分析中状态 | 不把筛选结果直接当作建议培育名单 |
| 查看模型说明 | 解释三类核心维度和证据层级 | 不展示旧四维公式或无依据权重编辑器 |

## 6. F-RECRUIT-C-RESULT 培育推荐结果

### 6.1 线框图

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ 培育企业推荐分析结果 / 人工线索复核结果 · 分析模式 · 对象范围      │
│ 模型 v… · 数据 v… · 生成时间 · 数据覆盖摘要 · [有可用更新/重新计算中]       │
│ [调整分析条件] [加入对比篮] [导出数据] [生成分析报告]                 │
│ 共分析 X 家 · 当前筛选 Y 家 · 已选 Z 家                                │
│ [企业名称] [产业类别] [企业规模] [重置]                                │
├──────────────────────────────────────────────┬─────────────────────────────┤
│ [企业排名] [行业分布]                        │ 培育企业详情                │
│                                              │ 企业名称                    │
│ 企业排名（主）                               │ 产业相关度                  │
│ 排名 企业名称 产业类别 企业规模 推荐指数     │ 政策匹配度                  │
│ 01   企业 A   类别 A   规模 A   —            │ 企业潜力                    │
│ 02   企业 B   类别 B   规模 B   —            │ ─────────────────────────  │
│                                              │ 技术壁垒 / 市场增速 /       │
│ 行业分布（补充视图）                         │ 团队背景证据                │
│ 统计口径未闭合时显示 GAP，不绘制伪图         │ 发展瓶颈 → 培育建议         │
│                                              │ → 所需支持 / 一企一策依据    │
│                                              │ 企业风险与信用 [查看明细]   │
├──────────────────────────────────────────────┴─────────────────────────────┤
│ 已选 Z 家  [取消选择] [全选当前筛选结果 Y 家] [加入对比篮]               │
│ 共 X 家  [20 条/页 ▾]                         ‹ 1 2 3 ›                   │
└──────────────────────────────────────────────┴─────────────────────────────┘
```

### 6.2 字段与指标

| 区块 | 字段 | 用户目的 | metric_id / 状态 | 表达规则 |
| --- | --- | --- | --- | --- |
| 列表 | 排名 | 判断培育优先顺序 | 培育推荐指数派生顺序 | 缺失指数时不生成伪排名 |
| 列表 | 企业名称 | 识别对象 | 对象字段 | 只显示当前结果企业 |
| 列表 | 产业类别 | 判断产业分布 | 对象字段 | 与行业分布分类口径一致 |
| 列表 | 企业规模 | 判断企业体量 | 对象字段 | 不与招引地域来源混用 |
| 列表 | 培育推荐指数 | 快速排序与复核 | `M_ENT_CULTIVATION_INDEX` · `semantic_revision_required` · Q015 | 现有四维定义须按 bid 三维校准；缺失不为 0 |
| 详情 | 产业相关度 | 解释产业契合 | `M_ENT_INDUSTRY_MATCH_SCORE` · 候选语义校准 | 与招引共用同一语义卡后才能正式显示 |
| 详情 | 政策匹配度 | 解释政策契合 | `M_ENT_POLICY_MATCH_SCORE` · Q015 | 无正式口径时显示 pending |
| 详情 | 企业潜力 | 解释培育价值 | `GAP-RECRUIT-METRIC-02`；`M_ENT_GROWTH_POTENTIAL` 仅候选 | 数据评审前不直接等同“成长潜力” |
| 详情 | 技术壁垒 / 市场增速 / 团队背景 | 解释本地潜力识别依据 | 解释字段；数值化时分别登记 metric_id | 可展示证据摘要，不展示伪分数 |
| 详情 | 所需支持 | 支撑精准培育 | 文本 / 分类字段 | 不自行发明支持分类，不自动生成工单 |
| 详情 | 发展瓶颈 / 瓶颈证据 | 理解企业为何需要培育 | 文本 / 证据引用；数值化时登记 metric_id | 由培育模型直接输出；不以风险洞察报告替代 |
| 详情 | 培育建议 | 理解针对瓶颈的措施方向 | 文本 / 分类字段 | 必须可追溯到对应瓶颈与所需支持；不扩展为完整一企一策 |
| 详情标题 / 风险区 | 风险摘要状态 | 快速判断是否需要继续复核 | 非评分状态：存在 N 项需关注 / 当前公开数据未检出 / 风险数据待核验 | 不使用“无风险”，不以风险线索替代培育模型的瓶颈判断 |
| 详情 / 风险区 | 司法涉诉 / 失信被执行 / 经营异常 / 行政处罚记录数 | 复核四类公开风险线索 | `GAP-RECRUIT-RISK-COUNT-01~04` | 各类别独立计数和溯源；语义未闭合或缺失时不显示为 0 |
| 详情 / 风险区 | 最近事件时间 / 摘要 / 查看风险明细 | 了解最新风险线索并进入逐条核验 | 明细字段，无统一 metric_id | 来源覆盖不足时显示“风险数据待核验”；不阻断其他详情 |
| 补充视图 | 行业分布 | 查看高培育价值企业的行业结构 | `GAP-RECRUIT-METRIC-04` | 统计量、分母、分类和 metric_id 未闭合时不显示真实图值 |
| 结果摘要 | 完整结果数 / 当前筛选数 / 已选数 | 理解当前结果和批量范围 | 非指标计数；受权限约束 | 无权限时不泄露数量；筛选不改变完整结果数 |
| 结果内筛选 | 企业名称 / 产业类别 / 企业规模 | 缩小当前展示集合 | 对象字段，无 metric_id | 只影响展示，不重跑模型、不改变结果版本 |
| 分页 | 页码 / 每页数量 | 稳定浏览完整结果 | 默认 20；选项 20 / 50 / 100 | 服务端稳定分页；保留完整结果原始排名 |
| 状态条 | 模型版本 / 数据版本 / 生成时间 / 数据覆盖 / 更新状态 | 判断结果时效与可追溯性 | 非指标结果字段 | 有更新时保留旧版本标识；新版完成前不静默替换 |

### 6.3 交互与禁止行为

| 触发 | 页面行为 | 不应发生的行为 |
| --- | --- | --- |
| 企业排名 / 行业分布切换 | 切换同一培育分析的两种结果表达；点击行业分布可局部筛选名单 | 不重新运行模型，不用行业分布取代名单主工作区，不重编号原始排名 |
| 选择名单行 | 右侧详情同步切换到该企业 | 不把所需支持自动生成完整一企一策 |
| 结果内筛选 | 只缩小当前展示集合并更新“当前筛选 Y 家” | 不重新运行模型、不改变结果版本、不重编号原始排名 |
| 翻页 / 调整每页数量 | 按稳定排序读取对应结果页；默认 20，可切换 20 / 50 / 100 | 不使用无限滚动替代分页，不因翻页清除跨页选择 |
| 表头全选 | 仅选择当前页可选企业 | 不默认选择全部筛选结果 |
| 全选当前筛选结果 | 在底部操作栏明确显示 Y 家并跨页选择 | 不隐藏作用范围，不与当前页全选混淆 |
| 取消选择 | 清除当前跨页选择集合 | 不重置结果内筛选或分析条件 |
| 加入对比篮 | 将选中企业与培育任务上下文写入对比篮，生成 `return_context_id`；超出剩余容量时整批阻断 | 不在对比篮改写培育指数或候选状态，不静默截断 |
| 查看指定对象复核结果 | 显示“人工线索复核结果”和本次指定对象集合 | 不将集合内排名表述为深圳全量排名 |
| 查看风险明细 | 打开当前企业的风险明细抽屉，保留名单、筛选、选择和详情上下文 | 不跳转到风险洞察，不改变推荐指数、排名、培育建议或候选状态 |
| 动态更新状态变化 | 显示新政策 / 新市场 / 新企业数据触发的“有更新 / 重新计算中 / 已更新”及版本 | 不静默改变指数、排名或分析时间 |
| 生成分析报告 | 当前页面显示生成中 / 可用 / 失败 | 不创建历史任务中心 |
| 导出数据 | 按权限导出当前范围；不超过暂定 1,000 家直接生成，超过后后台生成 | 不混入招引名单或全国企业数据，不创建通用任务中心 |

### 6.4 招引 / 培育共用的企业风险与信用明细抽屉

```text
┌──────────────────────────────────────────────┐
│ 企业风险与信用 · 企业名称              [关闭]│
│ 风险数据更新时间 · 来源覆盖说明               │
├──────────────────────────────────────────────┤
│ [全部] [司法涉诉] [失信被执行] [经营异常] [行政处罚] │
│ 风险类型｜事件摘要｜发生日期｜当前状态｜信息来源 │
│ ...                                          │
├──────────────────────────────────────────────┤
│ 仅展示可追溯公开风险线索，不构成专业法律意见。 │
└──────────────────────────────────────────────┘
```

| 字段 / 操作 | 用户目的 | 来源 / 状态 | 表达与禁止规则 |
| --- | --- | --- | --- |
| 风险类型 | 区分风险线索 | 司法涉诉 / 失信被执行 / 经营异常 / 行政处罚 | 不把不同法律含义的记录合并为单一“法律风险” |
| 事件摘要 | 快速理解事项 | 可追溯明细字段 | 不生成未经数据或人工确认的法律判断 |
| 发生日期 / 当前状态 | 判断时效与是否仍需关注 | 明细字段 | 已解除、已移出等状态须原样表达，不静默保留为当前异常 |
| 信息来源 / 数据更新时间 | 判断证据覆盖与新鲜度 | 数据契约字段 | 来源或时间缺失时标记待核验，不伪造 |
| 类别筛选 | 聚焦某类记录 | 只筛选当前企业明细 | 不改变摘要计数、推荐结果或候选状态 |
| 关闭抽屉 | 回到原企业详情 | 恢复原列表与详情上下文 | 不清空筛选、分页、跨页选择或当前企业 |

## 7. F-RECRUIT-CANDIDATES 引育候选工作台

### 7.1 线框图

```text
┌───────────────────────────────────────────────────────────────────────┐
│ 招引 / 培育候选工作台 · 人工线索                                        │
│ [全部状态] [线索来源] [企业名称]                    [从对比篮导入]    │
├────────────────────────────────────────────────────────────────────────┤
│ □ 企业名称  人工线索  来源  加入人/时间  范围预检  当前状态  研判证据   │
│ □ 企业 A   人工线索  企业查询  …          通过      待分析    —        │
│ □ 企业 B   人工线索  对比篮    …          不通过    待分析    —        │
├────────────────────────────────────────────────────────────────────────┤
│ 已选 X 家  [执行指定对象复核] [加入对比篮] [确认候选] [待定] [排除]    │
└─────────────────────────────────────────────────────────────────────────┘
```

### 7.2 字段与状态

| 字段 / 操作 | 用户目的 | 来源 / 状态 | 表达与禁止规则 |
| --- | --- | --- | --- |
| 线索类型 | 区分人工发现与模型推荐 | 固定为“人工线索” | 未执行复核前不显示为“已推荐” |
| 来源 / 加入人 / 加入时间 | 追溯线索 | 企业查询或对比篮的入站 payload | 不用当前操作人覆盖原始加入人 |
| 培育范围预检 | 确认是否可用培育模型 | 深圳市内 / 范围不符 / 校验失败 | 范围不符时禁用培育复核，可显式转为招引线索 |
| 候选状态 | 了解处理进度 | 待分析 / 分析中 / 已分析·待确认 / 研判中 / 已确认候选 / 待定 / 已排除 | 评估 / 风险返回时不自动转为已确认或已排除 |
| 执行指定对象复核 | 分析人工线索 | 复用当前招引 / 培育模型；暂定单次不超过 50 家 | 不创建新模型；排名只在本次指定集合内有效；超限整批阻断并提示分批 |
| 加入对比篮 | 发起更深研判 | 携带引育上下文和 `return_context_id` | 不自动发起评估 / 风险任务 |
| 研判证据 | 查看补充依据 | 任务 ID、结果版本、证据摘要、结果入口 | 不拷贝评分改写引育指数 |
| 确认 / 待定 / 排除 | 完成人工决策 | 用户显式操作 | 不按阈值或风险等级自动决策 |

## 8. F-RECRUIT-SERVICE-CONTRACT 模型服务契约

> 本 Frame 只在评审模式展示契约摘要，业务模式不渲染页面、按钮或入口。它承接 Bid 明确的 RESTful API / SDK 调用形态，不是新的业务页面。

| 契约 | 调用形态 | 能力范围 | 输入 / 输出必备元数据 | 架构与未决项 |
| --- | --- | --- | --- | --- |
| 招引模型 | RESTful API / SDK / 在线平台 | 按企业标签、行业领域、地域来源查询；执行分析；获取报告与导出 | 模型参数版本、`model_version`、`data_version`、`generated_at`、数据覆盖 / 缺失摘要 | 对外经网关 / Java 聚合，不暴露 Python 内部接口；URL、认证、版本、错误码和 SDK 语言待闭合 |
| 培育模型 | RESTful API / SDK / 在线平台 | 按产业类别、政策导向、企业规模查询；执行分析；获取报告与导出 | 模型参数版本、`model_version`、`data_version`、`generated_at`、数据覆盖 / 缺失摘要 | 对外经网关 / Java 聚合，不暴露 Python 内部接口；URL、认证、版本、错误码和 SDK 语言待闭合 |

**禁止行为：**

- 不因在线页面已存在就删除 RESTful API 或 SDK 交付。
- 不在四件套中臆造 URL、认证方式、SDK 语言、发布包名或错误码。
- 不让前端、第三方调用方或 Java 聚合层编写官方推荐算法。

## 9. 共享页面状态

| 状态 | 表现 | 用户下一步 | 禁止行为 |
| --- | --- | --- | --- |
| 初始 | 展示当前视图条件，无推荐结果 | 设置条件并执行分析 | 不显示默认名单或虚构分数 |
| 分析中 | 保留条件，稳定结果容器，展示五阶段、当前阶段与稍后查看入口，防重复提交 | 等待或从系统任务浮层 / 个人中心恢复 | 不展示旧结果冒充本次结果，不伪造百分比 |
| 成功 | 展示名单 / 排名、联动详情、更新时间、报告和导出入口 | 查看、生成报告或导出 | 不隐藏指标 pending / GAP 状态 |
| 空结果 | 明确“分析成功但无匹配企业”，保留条件 | 调整条件后重试 | 不自动放宽条件或跨范围填充名单 |
| 部分缺失 | 保留可用结果；具体字段显示“暂无数据” | 查看可用结果 | 不把缺失值显示为 0，不由前端估算 |
| 风险数据待核验 | 推荐结果和其他详情保持可读；风险摘要及四类记录显示待核验 | 稍后重试或转线下尽调 | 不显示为 0 条、“无风险”或自动降低推荐指数 |
| 当前公开数据未检出 | 显示未检出状态、数据更新时间和来源覆盖说明 | 继续复核或查看其他企业 | 不把“未检出”表述为企业不存在风险 |
| 失败 | 保留条件和错误反馈 | 按原条件重试 | 不表现为空结果或半成品排名 |
| 无权限 | 隐藏结果数值、名单、详情和导出 | 返回或申请授权 | 不通过数量、排序、错误详情泄露数据 |
| 报告未生成 | 当前结果可用，报告入口可用 | 生成报告 | 不显示历史报告资产 |
| 报告生成中 | 当前结果保持可读，报告操作显示处理中 | 等待 | 不清空结果或跳到任务中心 |
| 报告可用 | 当前页提供报告访问 / 下载入口 | 使用报告 | 不预设 bid 未定义的格式 |
| 报告 / 导出失败 | 当前结果保持可读，显示操作失败 | 重试 | 不把操作失败解释为分析失败 |
| 大结果集 | 显示完整结果总数、当前筛选数、已选数和稳定分页 | 局部筛选、翻页或调整每页数量 | 不默认截断 Top N，不以无限滚动替代稳定分页 |
| 跨页选择 | 保留已选集合并持续显示已选数 | 查看已选对象、取消选择或执行批量操作 | 不因翻页或局部筛选丢失选择 |
| 对比篮容量不足 | 整批阻断并显示剩余容量 | 缩小选择范围后重试 | 不静默加入前若干家 |
| 大批量导出 | 不超过暂定 1,000 家直接生成；超过后后台生成并在当前页面反馈 | 继续浏览或等待完成 | 不跳转到通用任务中心，不把后台生成误报为失败 |
| 人工线索待分析 | 显示来源和待分析状态，无推荐分数 | 选择对象并执行复核 | 不使用 DEMO 分数充当分析结果 |
| 培育范围不符 | 标记非深圳市内企业，禁用培育复核 | 转招引线索或移除 | 不静默转类或放宽培育范围 |
| 研判上下文失效 | 保留候选记录，证据引用标记失效 | 手工关联已有结果或重新研判 | 不自动排除企业 |
| 有可用更新 | 保留当前结果与模型 / 数据版本，标记更新来源 | 等待自动更新或按契约重试 | 不静默重排名单 |
| 重新计算中 | 旧结果保持可读，明确标识其版本与时间 | 等待新版本 | 不清空结果，不用无版本中间值替换 |
| 版本错误 | 不合并不同模型 / 数据版本的排名、指数或证据 | 重试或等待版本对齐 | 不省略错误不一致 |

## 10. 响应式与视觉约束

- **屏幕层级**：Track-MS；`medium` 为主设计，`small` 为响应式裁剪。
- **设计系统**：`agent-delivery/Design.md` 浅蓝白 + Arco；本四件套只规定产品与交互层级，不提前冻结 VI 视觉稿。
- **中屏**：名单 / 排名为主列，企业详情在右侧联动；培育“企业排名 / 行业分布”位于结果区内。表格固定选择 / 排名 / 企业名称等首列和操作尾列，中间业务字段可横向滚动。
- **小屏**：条件纵向排列；名单保持主内容；选中企业后详情在名单后展开或进入同路由详情态，不隐藏对象范围和 pending / GAP 状态。
- **风险明细**：中屏使用右侧 Drawer；小屏使用同路由全宽抽屉 / 详情态，必须保留企业名称、风险数据更新时间、来源覆盖说明和关闭返回路径。
- **结果与候选工作台**：中屏保留底部固定批量操作区；结果区依次显示“已选 Z 家 / 取消选择 / 全选当前筛选结果 Y 家 / 加入对比篮”。小屏将次要动作收入更多菜单，但已选数量与主操作始终可见。
- **无 KPI 填充**：bid 未定义的汇总数字不得用卡片置于名单之前。
- **指标展示**：数值、单位、更新时间和状态贴近字段；`GAP / pending_data_lead` 不因正式模式而隐藏。
- **系统色**：成功 / 失败色只表示系统状态，不表达企业优劣或推荐高低。
- **过程一致性**：招引与培育共用同一五阶段 Steps、信息提示条和右下角“稍后查看”布局；不得保留仅转圈的页面私有加载态。

## 11. 显式开放项

| ID | 开放项 | 当前处理 |
| --- | --- | --- |
| Q015 | 推荐指数、维度阈值和权重 | 无临时正式默认；字段显示 pending，等待语义闭合 |
| GAP-RECRUIT-METRIC-01 | 深圳连接度 metric_id | 登记独立指标，不与区域适配性合并 |
| GAP-RECRUIT-METRIC-02 | 企业潜力 metric_id | 评审后修订现有成长潜力指标或新增 ID |
| GAP-RECRUIT-METRIC-03 | 企业行业领域排名语义 | 明确排名范围、排序字段、并列规则和 ID |
| GAP-RECRUIT-METRIC-04 | 行业分布统计口径 | 明确统计量、分母、分类和 ID |
| GAP-RECRUIT-METRIC-05 | 关键指标集合 | 每个实际指标携带自身 metric_id |
| GAP-RECRUIT-UX-01 | 权限矩阵 | 当前只定义通用无权限态，不推断角色权限 |
| GAP-RECRUIT-EXPORT-01 | 报告模板 / 导出格式 | 当前只保留能力入口，不声明格式 |
| GAP-RECRUIT-DATA-01 | 数据来源实体、标准化与覆盖契约 | 等待 Data / GDF / 架构评审；不臆造源表与字段 |
| GAP-RECRUIT-MODEL-01 | 历史样本、训练优化、版本和动态更新触发规则 | 展示版本 / 状态落点，触发阈值与时序待算法 / 数据评审 |
| GAP-RECRUIT-API-01 | RESTful API / SDK 精确契约 | 保留三种调用形态，URL、认证、版本、错误码和 SDK 语言待架构 / 后端评审 |
| GAP-RECRUIT-BATCH-01 | 大结果集分页、指定对象复核和导出性能阈值 | 暂定每页 20 / 50 / 100、复核 50 家、直接导出 1,000 家；V1 会签前由前端 / 后端 / 算法完成性能验证 |
| GAP-RECRUIT-RISK-CREDIT-01 | 企业风险与信用的数据范围、来源覆盖、去重、状态值和更新时间契约 | 先保留风险摘要、四类记录与明细抽屉结构；Data / GDF / 合规闭合前统一显示待核验，不臆造正式记录或结论 |
| GAP-RECRUIT-RISK-COUNT-01~04 | 司法涉诉、失信被执行、经营异常、行政处罚记录数 | 各类别需独立 metric_id 或经语义评审确认为明细计数；闭合前不显示正式计数 |

## 12. 评审追溯挂载契约

```yaml
review_trace_contract:
  - frame_id: F-RECRUIT-PROCESS
    review_mounts:
      - mount_id: SYS-JOBS-F03-PROCESS-TITLE
        host_label: 引育推荐可视化分析过程标题
        marker_type: requirement_trace
        source_relation: product_enhancement
        trace_refs: [US-ENT-RECRUIT-R3, DEC-SYS-ANALYSIS-JOBS-20260723]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
  - frame_id: F-RECRUIT-A-CONFIG
    review_mounts:
      - mount_id: ENT-RECRUIT-F01-CONFIG-TITLE
        host_label: 招引推荐条件标题
        marker_type: requirement_trace
        source_relation: direct_requirement
        trace_refs: [US-ENT-RECRUIT-A1]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
  - frame_id: F-RECRUIT-A-RESULT
    review_mounts:
      - mount_id: ENT-RECRUIT-F02-RESULT-TITLE
        host_label: 招引推荐结果标题
        marker_type: requirement_trace
        source_relation: direct_requirement
        trace_refs: [US-ENT-RECRUIT-A2, US-ENT-RECRUIT-A3]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
      - mount_id: ENT-RECRUIT-F02-MANUAL-RESULT-TITLE
        host_label: 招引人工线索复核结果标题
        marker_type: requirement_trace
        source_relation: product_interpretation
        trace_refs: [US-ENT-RECRUIT-L2, DEC-ENT-RECRUIT-CLOSED-LOOP-20260721]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
      - mount_id: ENT-RECRUIT-F02-METRIC-DETAIL
        host_label: 招引推荐指数与维度说明
        marker_type: metric_spec
        source_relation: direct_requirement
        trace_refs: [M_ENT_ATTRACTION_INDEX, M_ENT_INDUSTRY_MATCH_SCORE, M_ENT_POLICY_MATCH_SCORE, GAP-RECRUIT-METRIC-01]
        required_payload: [metric_id, definition, source_systems, update_freq, version]
        review_mode: present
        business_mode: absent
      - mount_id: ENT-RECRUIT-F02-MODEL-STATUS
        host_label: 招引模型与数据状态条
        marker_type: requirement_trace
        source_relation: direct_requirement
        trace_refs: [DR-ENT-RECRUIT-A-06, DR-ENT-RECRUIT-A-07]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
      - mount_id: ENT-RECRUIT-F02-LARGE-RESULT
        host_label: 招引完整结果摘要、分页与底部批量操作栏
        marker_type: requirement_trace
        source_relation: product_interpretation
        trace_refs: [US-ENT-RECRUIT-R1, DEC-ENT-RECRUIT-LARGE-RESULT-20260721]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
      - mount_id: ENT-RECRUIT-F02-RISK-CREDIT
        host_label: 招引企业详情的企业风险与信用区
        marker_type: requirement_trace
        source_relation: product_enhancement
        trace_refs: [US-ENT-RECRUIT-R2, DEC-ENT-RECRUIT-RISK-CREDIT-20260722]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
  - frame_id: F-RECRUIT-C-CONFIG
    review_mounts:
      - mount_id: ENT-RECRUIT-F03-CONFIG-TITLE
        host_label: 培育推荐条件标题
        marker_type: requirement_trace
        source_relation: direct_requirement
        trace_refs: [US-ENT-RECRUIT-C1]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
  - frame_id: F-RECRUIT-C-RESULT
    review_mounts:
      - mount_id: ENT-RECRUIT-F04-RESULT-TITLE
        host_label: 培育推荐结果标题
        marker_type: requirement_trace
        source_relation: direct_requirement
        trace_refs: [US-ENT-RECRUIT-C2, US-ENT-RECRUIT-C3]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
      - mount_id: ENT-RECRUIT-F04-MANUAL-RESULT-TITLE
        host_label: 培育人工线索复核结果标题
        marker_type: requirement_trace
        source_relation: product_interpretation
        trace_refs: [US-ENT-RECRUIT-L2, DEC-ENT-RECRUIT-CLOSED-LOOP-20260721]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
      - mount_id: ENT-RECRUIT-F04-METRIC-DETAIL
        host_label: 培育推荐指数与维度说明
        marker_type: metric_spec
        source_relation: direct_requirement
        trace_refs: [M_ENT_CULTIVATION_INDEX, M_ENT_INDUSTRY_MATCH_SCORE, M_ENT_POLICY_MATCH_SCORE, GAP-RECRUIT-METRIC-02]
        required_payload: [metric_id, definition, source_systems, update_freq, version]
        review_mode: present
        business_mode: absent
      - mount_id: ENT-RECRUIT-F04-MODEL-STATUS
        host_label: 培育模型与数据状态条
        marker_type: requirement_trace
        source_relation: direct_requirement
        trace_refs: [DR-ENT-RECRUIT-C-06, DR-ENT-RECRUIT-C-07]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
      - mount_id: ENT-RECRUIT-F04-LARGE-RESULT
        host_label: 培育完整结果摘要、分页与底部批量操作栏
        marker_type: requirement_trace
        source_relation: product_interpretation
        trace_refs: [US-ENT-RECRUIT-R1, DEC-ENT-RECRUIT-LARGE-RESULT-20260721]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
      - mount_id: ENT-RECRUIT-F04-RISK-CREDIT
        host_label: 培育企业详情的企业风险与信用区
        marker_type: requirement_trace
        source_relation: product_enhancement
        trace_refs: [US-ENT-RECRUIT-R2, DEC-ENT-RECRUIT-RISK-CREDIT-20260722]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
  - frame_id: F-RECRUIT-CANDIDATES
    review_mounts:
      - mount_id: ENT-RECRUIT-F05-CANDIDATE-TITLE
        host_label: 引育候选工作台标题
        marker_type: requirement_trace
        source_relation: product_enhancement
        trace_refs: [US-ENT-RECRUIT-L1, US-ENT-RECRUIT-L2, US-ENT-RECRUIT-L3, DEC-ENT-RECRUIT-CLOSED-LOOP-20260721]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
  - frame_id: F-RECRUIT-SERVICE-CONTRACT
    review_mounts:
      - mount_id: ENT-RECRUIT-F06-SERVICE-CONTRACT
        host_label: RESTful API / SDK / 在线平台契约摘要
        marker_type: requirement_trace
        source_relation: direct_requirement
        trace_refs: [DR-ENT-RECRUIT-A-09, DR-ENT-RECRUIT-C-09]
        required_payload: [source_location, source_summary, current_placement, source_relation]
        review_mode: present
        business_mode: absent
```

- 禁止挂载在企业名称、候选状态、操作按钮、导出文件名或业务结论文案中；追溯标记不得改变字段、权限或状态。
- 每个挂载的 popover 只展示契约中的 `required_payload`；业务模式必须完全移除评审标记，不留占位。

## 13. 本页 metric_id 清单

- `M_ENT_ATTRACTION_INDEX`
- `M_ENT_CULTIVATION_INDEX`
- `M_ENT_INDUSTRY_MATCH_SCORE`
- `M_ENT_POLICY_MATCH_SCORE`
- `M_ENT_GROWTH_POTENTIAL`（仅候选校准）
- `GAP-RECRUIT-METRIC-01~05`（待语义闭合，不作为正式 metric_id）
- `GAP-RECRUIT-RISK-COUNT-01~04`（四类风险记录数待语义与数据映射闭合，不作为正式 metric_id）

## 14. Wireframe 自检

- [x] 六个业务 Frame 与一个非页面服务契约 Frame 均有 IA / TRACE / USM 落点。
- [x] 招引与培育的对象范围、筛选、核心维度、证据字段和结果未混用。
- [x] 统计字段均关联已注册 `metric_id`、候选校准状态或显式 GAP。
- [x] 初始、分析中、成功、空结果、部分缺失、失败、无权限、报告和导出状态已定义。
- [x] 报告与数据导出按算法 bid 保留为必备能力。
- [x] 候选工作台、指定对象复核、对比篮研判返回与人工确认已落位，且未引入公式编辑、前端算法或完整一企一策。
- [x] 六个 Frame 均有唯一的评审追溯挂载清单，业务模式明确不渲染挂载。
- [x] 招引目标特征、培育瓶颈 / 建议 / 所需支持链、模型 / 数据版本和动态更新状态已落位。
- [x] RESTful API / SDK / 在线平台三种调用形态已进入非页面契约 Frame。
- [x] 大结果集完整名单、稳定分页、局部筛选、跨页选择、底部批量操作与超容量阻断已落位。
- [x] 企业风险与信用摘要、四类记录、明细抽屉、缺失态与禁止自动决策规则已落位。
- [x] 招引与培育已统一为五阶段异步过程，支持后台继续和系统任务恢复，且两类任务保持隔离。
- [ ] Q015、9 项指标 GAP 及数据、模型、API、权限、报告 / 导出、批量性能、风险数据契约未闭合前，本线框不能宣告 PDR-ready。
