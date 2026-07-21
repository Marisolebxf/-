# Wireframe-ENT-RISK.md

> **模块**：风险洞察（ENT-RISK / E-28 / E-29）
> **对应 IA**：`IA-ENT-RISK.md`
> **对应 USM / TRACE**：`USM-ENT-RISK.md` / `TRACE-ENT-RISK.yaml`
> **版本**：v1.10 · 2026-07-21
> **阶段**：原需求与当前实现复核后修订，作为 V1 高保真首轮输入；不代表门 1 已通过
> **屏幕 / 轨道**：medium · Track-MS

## 1. Frame 清单

| Frame | 触发入口 | 目的 | 原始需求 / TRACE |
| --- | --- | --- | --- |
| F-RISK-01 分析配置 | 对比篮分发或风险洞察菜单 | 确认对象、模式、范围并创建分析任务 | E-28 / E-29；`US-ENT-RISK-OBJECT` |
| F-RISK-04 分析过程 | 点击“开始分析” | 查看真实后台阶段并允许离开恢复 | `US-ENT-RISK-PROCESS` |
| F-RISK-02 供应链结果 | 供应链任务完成 | 查看图谱、关键节点、断链风险和报告 | E-28；`US-ENT-RISK-SUPPLY` |
| F-RISK-03 痛难点结果 | 痛难点任务完成 | 查看问题、成因、最佳实践、解决方向和报告 | E-29；`US-ENT-RISK-PAIN` |
| F-RISK-05 最近分析 | “发展痛难点”后的第三个页面级 Tab | 找回任务、结果和配置 | `US-ENT-RISK-HISTORY` |
| F-RISK-06 报告任务 | 结果页创建 / 查看报告 | 查看生成状态、下载当前报告或去资产中心 | `US-ENT-RISK-REPORT` |

内部评审追溯不是独立业务 Frame；它以环境级 `reviewMode` 覆盖挂载在 F-RISK-01～06 的稳定业务标题上。

## 2. F-RISK-01｜分析配置

### 2.1 线框

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ 分析对象 · 来自对比篮 · 50 家                        [返回对比篮补充] │
│ [企业 A ×] [企业 B ×] [企业 C ×] [管理全部对象（50 家）]                 │
├──────────────────────────────────────────────────────────────────────────┤
│ [供应链关系] [发展痛难点] [最近分析]                                      │
├──────────────────────────────────────────────────────────────────────────┤
│ 供应链：关系类型 [供应商✓ 客户✓ 合作伙伴✓]  结果支持节点按需逐层展开     │
│ 痛难点：诊断维度 [技术研发✓ 市场拓展✓ 融资✓ 管理✓]                       │
├──────────────────────────────────────────────────────────────────────────┤
│ 数据与权限预检：对象有效 / 图谱或诊断数据 / 模型状态 / 缺失说明           │
├──────────────────────────────────────────────────────────────────────────┤
│ 页面底部操作栏                                                [开始分析] │
└──────────────────────────────────────────────────────────────────────────┘
```

### 2.2 区块、字段与指标

| # | 区块 / 控件 | 用户目的 | 字段 / 状态 | 数据 / 来源 | metric_id |
| ---: | --- | --- | --- | --- | --- |
| 1 | 来源摘要 | 确认两个分析 Tab 共享的工作现场 | `source` / `return_context_id` / count | 对比篮契约 | N/A |
| 2 | 对象标签 | 在 Tab 上方确认或当次移除共享对象 | `enterprise_codes[]` / valid / permission | 对象服务 | N/A |
| 2a | 管理全部对象抽屉 | 在大量对象下定位并调整当次草稿 | keyword / page / page_size=10 / remove | 当次共享对象草稿；不回写对比篮 | N/A |
| 3 | 页面级 Tab | 选择供应链、痛难点或最近分析；最近分析固定为第三项 | `analysis_type` / `view=history` | 路由状态 | N/A |
| 4 | 关系类型 | 限定图谱关系 | supplier / customer / partner | 图谱查询配置 | N/A |
| 5 | 展开说明 | 建立结果交互预期 | 默认一级 / 节点按需展开 / 系统最多三级 | 产品交互规则 | N/A |
| 6 | 诊断维度 | 选择问题维度 | technology / market / finance / management | 专题系统 Bid 四维；Q018 负责底层指标域映射 | N/A |
| 7 | 数据预检 | 判断能否分析 | coverage / missing / model_status | Java 聚合结果 | 相关七项当前可见 metric_id |
| 8 | 页面底部操作栏 / 开始分析 | 创建不可变任务；作为配置页唯一主提交动作 | `riskTaskId` / enabled / disabled_reason | 风险任务服务 | N/A |

### 2.3 交互与禁止行为

| 触发 | 页面行为 | 不应发生的行为 |
| --- | --- | --- |
| 从对比篮进入 | 自动带入有效对象和来源，不要求再次选择 | 不清空对比篮，不在本页复制搜索器 |
| 对象区空态 | 居中展示说明与蓝色主按钮“前往对比篮选择企业” | 标题右侧不显示同功能次按钮；不出现两个重复入口 |
| 对象区已有对象 | 展示来源标签、可关闭对象标签，标题右侧显示“返回对比篮调整对象” | 不在空态和标题区同时提供返回入口 |
| 对象数 1–5 家 | 完整显示所有可移除对象标签 | 不额外增加抽屉入口，不折叠可读对象 |
| 对象数 6–50 家 | 仅显示快照顺序前三家和“管理全部对象（N 家）”；抽屉支持名称搜索、每页 10 家和当次移除 | 不平铺全部标签；不在抽屉新增对象，不回写对比篮 |
| 移除对象 | 仅更新当次草稿 | 不回写对比篮 |
| 返回补充对象 | 通过 `return_context_id` 恢复对比篮现场 | 不丢失筛选、勾选或滚动位置 |
| 切换到供应链 | 对象超过 2 家时保留上下文并提示缩减 | 不静默取前两家 |
| 切换 Tab | 来源与对象在 Tab 上方保持不变；保存并恢复各 Tab 的当次草稿配置 | 不重置对象，不展示用户侧层级选择，不把系统最大深度映射成诊断配置 |
| 点击最近分析 | 第三个 Tab 独占选中并进入 F-RISK-05；返回前两个 Tab 时清除历史态并恢复对应配置 | 不在标题区保留重复“最近分析”按钮，不让分析 Tab 与历史 Tab 同时选中 |
| 数据与权限预检 | 只展示校验状态、缺失项、阻断原因和对应数据说明 | 不在预检卡片标题栏放“开始分析”，不让状态区同时承担页面提交操作 |
| 页面底部“开始分析” | 预检通过后创建任务并进入 F-RISK-04；作为页面唯一主提交动作固定置于底部操作栏右侧 | 不在其他区块重复按钮；不增加风险洞察不具备的“保存为个人模板”；不在前端直接生成正式风险结果 |

### 2.4 状态

| 状态 | 表现 | 用户下一步 |
| --- | --- | --- |
| 默认 | 显示共享对象、Tab、当前 Tab 配置和预检；底部操作栏右侧显示“开始分析” | 调整配置并开始分析 |
| 无对象 | 对象区稳定空态；底部“开始分析”禁用，预检区显示原因 | 前往对比篮 |
| 对象超限 | 预检区显示当前数量 / 上限和具体提示；底部“开始分析”禁用 | 当次移除或返回对比篮 |
| 对象失效 | 只保留有效交集并列出不可用数量 | 调整对象 |
| 加载 | 分区骨架，保留页面结构 | 等待 |
| 数据不足 | 逐对象 / 维度说明缺失和影响 | 调整对象或继续允许的 DEMO 分析 |
| 无权限 | 不渲染敏感值，保留原因和申请入口 | 申请权限或返回 |
| 模型未就绪 | 标记 Q017 / Q018 与 DEMO 状态 | 不生成正式结论 |

### 2.5 页面底部操作栏规则

- 操作栏属于 F-RISK-01 页面级提交区，不属于“数据与权限预检”卡片。
- 中屏下固定在配置内容末尾并保持可见；主按钮位于右侧，文案固定为“开始分析”。
- 风险洞察当前没有个人模板能力，因此不照搬企业评估的“保存为个人模板”，不为视觉对齐创造新能力。
- `canStart=true` 时主按钮可用；对象为空、对象超限、预检未通过或无权限时按钮禁用，具体原因由预检区承载，不只依赖 disabled 状态表达。
- 配置区不得再出现第二个“开始分析”，避免重复提交入口和操作归属不清。

## 3. F-RISK-04｜分析过程

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ 任务摘要卡                                                             │
│ 分析结果已生成                                                [已完成]  │
│ 任务 ID：RISK-...  分析类型：供应链关系  企业数量：2 家  已用：18 秒     │
└──────────────────────────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────────────────────┐
│ 可视化分析过程                                                         │
│ [任务提交✓]—[权限与配置校验✓]—[数据汇聚✓]—[算法计算✓]—[结果组装✓]      │
│   已完成          已完成             已完成        已完成       已完成   │
│ ┌ 成功 Alert：分析结果已生成                                           │
│ │ 任务快照已固化，可以进入结果页查看风险洞察结论。                      │
│ └────────────────────────────────────────────────────────────────────── │
│                                            [查看最近分析] [查看分析结果] │
└──────────────────────────────────────────────────────────────────────────┘
```

- 上方任务摘要卡展示任务 ID、分析类型、企业数量、已用时间和状态 Tag；标题栏只承载标题追溯与状态，不承载过程动作。
- 下方“可视化分析过程”卡与企业评估使用同构样式：阶段标题纵向排布，每阶段显示已完成 / 进行中 / 等待中 / 失败。
- 当前反馈使用语义 Alert：处理中为 `info`、完成为 `success`、失败为 `error`。
- 所有过程动作位于 Alert 下方右侧：处理中显示“稍后查看”，完成显示“查看最近分析 / 查看分析结果”，失败显示“按此配置新建分析”；不放入标题栏。
- 通用阶段：任务提交、权限与配置校验、数据汇聚、算法计算、结果组装。
- 供应链阶段可细化为关系子图提取、中心性 / 风险计算；痛难点阶段可细化为特征匹配、问题装配。
- 只显示后台可证明的当前 / 已完成阶段和已用时间，不显示伪造百分比。
- 完成后停留在 F-RISK-04，不自动跳转；状态改为“分析结果已生成”，主动作“查看分析结果”由用户主动进入对应结果，辅助动作“查看最近分析”。
- 失败保留阶段、错误编号和配置快照，并提供“重新尝试 / 按此配置新建分析”；不得把失败任务伪装成可查看结果。

## 4. F-RISK-02｜供应链结果

### 4.1 线框

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ ← 风险洞察  供应链关系 · RISK-...              [按此配置新建分析]       │
│ 对象 1–2 家 · 数据时间 · 算法版本 · 权限范围                             │
├────────────────────────────────────────────┬─────────────────────────────┤
│ 供应链图谱                                 │ 关键节点与断链风险 ⓘ        │
│ 当前展示：1级 · 节点4个 · 共同节点1个       │ [关键节点] [断链风险]       │
│ [只看关键] [只看风险] [展开下一层]          │ 列表与图谱双向定位          │
│                                            │ 处置提示：建议提前制定      │
│                                   ● 中心企业│ 备份方案                    │
│                    ● 供应商 ● 客户 ● 合作伙伴│                             │
├────────────────────────────────────────────┴─────────────────────────────┤
│ 数据来源、更新时间、缺失与 Q017 / DEMO 说明                              │
├──────────────────────────────────────────────────────────────────────────┤
│ 供应链分析报告                                        [创建报告]         │
│ 报告继承当前不可变任务快照；生成中可后台继续，完成后查看或下载。          │
└──────────────────────────────────────────────────────────────────────────┘
```

### 4.2 区块、字段与指标

| # | 区块 / 控件 | 用户目的 | 字段 / 状态 | 数据 / 来源 | metric_id |
| ---: | --- | --- | --- | --- | --- |
| 1 | 任务摘要 | 确认不可变上下文 | task / object / config / version / permission | 任务快照 | N/A |
| 2 | 关系概览 | 了解网络规模 | supplier_count / relation_count | 图谱聚合 | `M_ENT_SUPPLIER_COUNT` |
| 2a | 图谱状态行 | 了解当前观察状态 | current_level / visible_node_count / shared_node_count | 当前图谱视图状态 | N/A |
| 2b | 关系类型图例 | 识别节点颜色语义 | center / supplier / customer / partner | 静态视觉映射 | N/A |
| 3 | 图谱节点 | 查看企业与关系类型 | enterprise / node_type / level / flags | NebulaGraph 经 Java 聚合 | `M_ENT_NODE_CENTRALITY` |
| 4 | 图谱边 | 查看关系与来源 | relation_type / level / source | NebulaGraph 经 Java 聚合 | `M_ENT_RELATION_STRENGTH` |
| 5 | 核心供应商 | 识别关键依赖 | core_supplier / centrality / reason | 算法结果，Q017 | `M_ENT_CORE_SUPPLIER_COUNT`、`M_ENT_NODE_CENTRALITY` |
| 6 | 断链风险 | 查看风险线索并形成处置意识 | type / node / path / evidence / backup_prompt | 算法结果，Q017；固定业务提示 | `M_ENT_SUPPLY_CHAIN_RISK` |
| 7 | 数据说明 | 判断可用性 | source / updated_at / missing / mapping_status | 数据与指标服务 | 对应 metric_id |
| 8 | 独立报告区块 | 沉淀当前分析 | report_fingerprint / status / primary_action | 报告服务；位于业务结果之后 | N/A |

### 4.3 图谱规则

- 单企业：目标企业居中；供应商上游、客户下游、合作伙伴横向；默认一级，最多三级。
- 两企业：双中心布局；共同节点居中，A / B 独有节点分区；不做两企业混合大图。
- 图谱顶部只显示轻量状态文本“当前展示：N 级 · 节点 N 个 · 共同节点 N 个”；这些内容不是业务 KPI，不使用 KPI 卡、Tag 或按钮样式。
- 中心企业、供应商、客户、合作伙伴图例以“色点＋文字”静态显示在图谱画布右下角；图例不可点击，不与顶部状态、筛选标签或“只看关键 / 只看风险”操作混排。
- 配置页不提供展开层级选择。结果初始只呈现一级；仅确认存在下一层且未达三级的节点显示可展开标识。
- “系统最多 3 级”不单独占用标签或状态项，仅在“展开下一层”动作的 hover / focus 提示中说明；达到上限后动作置为“已到最大深度”。
- 点击可展开节点时就地显示加载态，成功后追加下一层并更新“当前路径 / 第 N 层”；再次点击或使用折叠动作收起该分支。
- 无子节点显示“暂无下级关系”；加载失败保留现有图谱并允许只重试当前节点；到达三级显示“已达最大展开深度”。任何状态都不得表现为点击无响应。
- 节点点击打开详情并可定位列表；列表点击高亮图谱节点或路径。展开 / 折叠属于观察状态，不修改分析任务快照。
- 断链风险仅包含单点依赖、节点异常、路径脆弱；Q017 未闭合时显式标 DEMO / 待确认。
- 关键节点风险和断链风险项显示固定业务提示“建议提前制定备份方案”；提示不包含替代对象、方案内容或处置承诺。
- 不显示企业供应链总评分、企业排名、替代供应商、替代路径、备选名单或备份方案生成按钮。
- 结果页顶部任务摘要只提供“按此配置新建分析”，该动作创建新草稿 / 新任务，不修改当前结果快照；报告动作不得与其混排。
- 独立报告区块按状态显示“创建报告 / 生成中 / 查看报告或下载当前报告”，不得使用“创建 / 查看报告”合并表达不同状态。

## 5. F-RISK-03｜痛难点结果

### 5.1 线框

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ ← 风险洞察  发展痛难点 · RISK-...              [按此配置新建分析]       │
│ 对象 50 家 · 企业 A、企业 B、企业 C 等 50 家                            │
│ [查看全部对象]                                                           │
│ 数据时间 · 诊断版本 · 权限范围                                           │
├──────────────────────────────────────────────────────────────────────────┤
│ [技术研发：影响31家] [市场拓展：27家] [融资：18家] [管理：12家]        │
├──────────────────────────────────────────────────────────────────────────┤
│ 共性问题 Top 5                                      [查看完整问题]       │
│ 问题 → 影响企业数 / 比例 → 典型企业（最多3家） [查看受影响企业]         │
│ 选中问题 → 命中依据 → 成因 → 行业最佳实践 → 解决方向                    │
├──────────────────────────────────────────────────────────────────────────┤
│ 数据来源、缺失影响、Q018 / DEMO 说明                                     │
├──────────────────────────────────────────────────────────────────────────┤
│ 发展痛难点分析建议报告                                [创建报告]         │
│ 报告继承当前不可变任务快照；生成中可后台继续，完成后查看或下载。          │
└──────────────────────────────────────────────────────────────────────────┘
```

### 5.2 区块、字段与指标

| # | 区块 / 控件 | 用户目的 | 字段 / 状态 | 数据 / 来源 | metric_id |
| ---: | --- | --- | --- | --- | --- |
| 1 | 紧凑对象摘要 / 全部对象抽屉 | 确认单企 / 集合上下文 | object / source / industry / region / validity / data_status / search / page | 任务快照；1–5 家全显，6–50 家前三家 + 等 N 家；按钮在摘要下方左对齐，抽屉只读 | N/A |
| 2 | 维度总览 | 快速定位问题 | dimension / issue_count / severity / data_status | 诊断结果，Q018 | `M_ENT_PAINPOINT_COUNT`、`M_ENT_PAINPOINT_SEVERITY` |
| 3 | 共性问题 Top 5 / 完整问题视图 | 查看重点与完整问题 | issue / evidence / severity / affected_count / affected_ratio / dimension / search / filter / page | 集合诊断；首屏按影响企业数展示 5 项，完整视图只读 | `M_ENT_PAINPOINT_COUNT`、`M_ENT_PAINPOINT_SEVERITY` |
| 4 | 成因分析 | 理解问题形成原因 | cause / evidence_source | 专家知识库 + 数据 | N/A |
| 5 | 行业最佳实践 | 获取参照 | practice / applicable_scope / source | 专家知识库 | N/A（当前为解释性文本） |
| 6 | 解决方向 | 形成服务沟通材料 | direction / service_suggestion | 诊断结果 | N/A |
| 7 | 共性分布 / 典型与受影响企业 | 了解集合共性并定位对象 | affected_count / ratio / typical_enterprises / affected_enterprises / enterprise_hit_summary | 集合诊断；典型企业最多 3 家；受影响名单只读 | `M_ENT_PAINPOINT_COUNT` |
| 8 | 独立报告区块 | 沉淀建议报告 | report_fingerprint / status / primary_action | 报告服务；位于业务结果之后 | N/A |

### 5.3 结果规则

- 单企业：对象摘要 → 四维总览 → 分维度问题 → 问题详情 → 报告。
- 企业集合：紧凑对象摘要 → 四维影响分布 → 共性问题 Top 5 → 典型企业入口 → 完整受影响企业 / 企业命中摘要 → 集合报告。
- 1–5 家显示全部对象名称；6–50 家只显示任务快照顺序中的前三家与“等 N 家”。“查看全部对象”单独置于摘要文字下方并左对齐；按钮打开只读抽屉，支持名称搜索、有效性 / 数据状态筛选和每页 10 家，不允许增删任务对象。
- 只读对象抽屉底部在评审模式显示“对象列表只读，顺序固定为任务创建时的对象快照；搜索与筛选不改变任务。”；业务模式完全不渲染该说明，不以隐藏占位影响抽屉布局。
- 共性问题首屏按 `affected_count` 从高到低展示 5 项；并列时保持后端结果顺序，不以未闭合严重度阈值创造排序。完整问题视图支持名称搜索、维度 / 数据状态筛选和分页。
- 每个共性问题最多显示 3 家典型企业；“查看受影响企业”打开只读名单，支持名称搜索、有效性 / 数据状态筛选和分页。查看企业只展示该企业在当前集合任务中的问题命中摘要，关闭后恢复原问题、筛选、分页和滚动位置。
- 严重度高 / 中 / 低只用于阅读优先级；不参与企业评分或排名。
- 数据不足显示“数据不足，暂不判断”，不得补 0、推断无问题或生成伪造行业差距。
- 四张维度卡片只在实际 `问题项数 / 严重度 / 影响企业数` 数值旁显示各自唯一的指标说明；标题不显示指标、Mock 或 Pending 徽标。
- “行业最佳实践”不等同于量化行业差距；当前没有实际可见差距值，因此不渲染 `M_ENT_PAINPOINT_GAP` 指标挂点。
- 结果页顶部任务摘要只提供“按此配置新建分析”，不使用“修改配置并重新分析”；报告动作独立置于业务结果之后，并按创建、生成中、查看 / 下载状态切换。

## 6. F-RISK-05｜最近分析

F-RISK-05 由页面级第三个 Tab 进入，顺序固定在“发展痛难点”之后；历史态只选中“最近分析”，页面标题区不再设置同名快捷按钮。

| # | 区块 / 控件 | 用户目的 | 字段 / 状态 | 数据 / 来源 | metric_id |
| ---: | --- | --- | --- | --- | --- |
| 1 | 历史行 | 识别正式任务 | task_id / analysis_type / object_summary / status | 风险任务服务 | N/A |
| 2 | 版本信息 | 判断可复现性 | data / algorithm / config / permission version | 任务快照 | N/A |
| 3 | 恢复结果 | 回到不可变结果 | task_id / result_route | 结果服务 | N/A |
| 4 | 按此配置新建 | 复用配置创建新草稿 | source_task_id | 新任务草稿 | N/A |
| 5 | 关联报告 | 查看当前任务产物 | report_ids / report_count | 报告服务 | N/A |

最近分析与个人资产中心读取同一任务源；不提供团队协作、审批流、复杂版本比较、批量删除审计记录或第二套报告计数。

## 7. F-RISK-06｜报告任务

| 阶段 | 页面表现 | 允许动作 |
| --- | --- | --- |
| 已提交 | 显示报告任务 ID、类型和提交时间 | 关闭抽屉，后台继续 |
| 数据准备 | 显示对象、权限和结果快照校验中 | 查看详情 |
| 内容组装 | 显示供应链结构或痛难点章节组装中 | 查看详情 |
| 图表生成 | 显示图表生成中 | 查看详情 |
| 报告生成 | 显示 PDF 生成中 | 查看详情 |
| 已完成 | 显示有效期、水印、脱敏 / 审批标记 | 下载当前报告 / 去个人资产中心 |
| 失败 | 显示失败阶段和审计错误编号 | 重试 / 联系管理员 |

- 供应链报告指纹至少包含对象、关系范围、数据 / 图谱 / 算法版本、权限范围、结果任务、报告模板版本。
- 痛难点报告指纹至少包含对象、诊断维度、数据 / 知识库 / 算法版本、权限范围、结果任务、报告模板版本。
- 供应链报告正文至少包含对象与范围、关系结构、多级路径摘要、关键节点、断链风险、判断依据、数据来源 / 缺失 / 版本说明，并在适用风险项后显示“建议提前制定备份方案”；不得包含替代供应商、备选名单或自动生成的备份方案内容。
- 痛难点报告正文至少包含对象、四维诊断结论、问题、成因、行业最佳实践、解决方向、判断依据和数据来源 / 缺失 / 版本说明。
- 重复提交先查服务端；不以前端缓存判断报告是否存在。
- “下载当前报告”只在报告完成且用户有权限时可用，并绑定当前 `riskTaskId`。

## 8. 内部评审追溯覆盖（非业务 Frame）

- 只允许挂载在页面、Tab 或稳定业务区块标题；禁止挂在普通按钮、筛选控件、分页器、表格行、图谱节点 / 边和临时浮层触发器上。
- `requirement_trace`、`metric_spec`、`mock_data`、`pending_source` 四类 Marker 分开呈现，不得用一个状态冒充另一种含义。
- 业务模式不得出现 Marker；评审模式点击 Marker 后弹出来源关系、原文定位、Story / Frame、指标或 Q 项及当前数据状态。

评审挂点统一遵循以下宿主规则：稳定区块标题只挂 `requirement_trace`；`metric_spec` 只挂在实际统计值旁；`mock_badge` / `pending_badge` 只挂在对应值或统一数据说明区域。一个 `mount_id` 只对应一个稳定宿主；无实际可见量化字段时不创建指标挂点。

```yaml
review_trace_contract:
  - mount_id: ENT-RISK-F01-SUPPLY-TITLE
    frame_id: F-RISK-01
    host_label: Tab 下方供应链关系配置标题
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [E-28, REQ-ENT-008, US-ENT-RISK-SUPPLY]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F01-PAIN-TITLE
    frame_id: F-RISK-01
    host_label: Tab 下方发展痛难点配置标题
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [E-29, US-ENT-RISK-PAIN]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F01-Q017
    frame_id: F-RISK-01
    host_label: 供应链数据预检标题
    marker_type: pending_badge
    source_relation: product_interpretation
    trace_refs: [Q017]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F01-Q018
    frame_id: F-RISK-01
    host_label: 痛难点数据预检标题
    marker_type: pending_badge
    source_relation: product_interpretation
    trace_refs: [Q018]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F04-PROCESS-TITLE
    frame_id: F-RISK-04
    host_label: 分析过程标题
    marker_type: review_copy
    source_relation: product_interpretation
    trace_refs: [US-ENT-RISK-PROCESS, E-28, E-29]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F02-GRAPH-TITLE
    frame_id: F-RISK-02
    host_label: 供应链图谱标题
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [E-28, US-ENT-RISK-SUPPLY]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F02-KEYRISK-TITLE
    frame_id: F-RISK-02
    host_label: 关键节点与断链风险标题
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [E-28, REQ-ENT-008, US-ENT-RISK-SUPPLY]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F02-OVERVIEW-METRIC
    frame_id: F-RISK-02
    host_label: 图谱状态行关系概览实际数值
    marker_type: metric_spec
    source_relation: direct_requirement
    trace_refs: [M_ENT_SUPPLIER_COUNT, M_ENT_RELATION_STRENGTH]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F02-KEYNODE-METRIC
    frame_id: F-RISK-02
    host_label: 关键节点卡片节点影响度实际数值
    marker_type: metric_spec
    source_relation: direct_requirement
    trace_refs: [M_ENT_CORE_SUPPLIER_COUNT, M_ENT_NODE_CENTRALITY]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F02-RISK-METRIC
    frame_id: F-RISK-02
    host_label: 断链风险项风险类型或等级实际值（仅实际展示时）
    marker_type: metric_spec
    source_relation: direct_requirement
    trace_refs: [M_ENT_SUPPLY_CHAIN_RISK, Q017]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F02-MOCK
    frame_id: F-RISK-02
    host_label: 图谱数据说明标题
    marker_type: mock_badge
    source_relation: product_interpretation
    trace_refs: [E-28]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F03-DIAGNOSIS-TITLE
    frame_id: F-RISK-03
    host_label: 四维诊断标题
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [E-29, US-ENT-RISK-PAIN]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F03-ISSUES-TITLE
    frame_id: F-RISK-03
    host_label: 问题清单或共性问题标题
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [E-29, REQ-ENT-009, US-ENT-RISK-PAIN]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F03-TECH-METRIC
    frame_id: F-RISK-03
    host_label: 技术研发维度卡片问题项数或严重度实际值
    marker_type: metric_spec
    source_relation: direct_requirement
    trace_refs: [M_ENT_PAINPOINT_COUNT, M_ENT_PAINPOINT_SEVERITY, Q018]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F03-MARKET-METRIC
    frame_id: F-RISK-03
    host_label: 市场拓展维度卡片问题项数或严重度实际值
    marker_type: metric_spec
    source_relation: direct_requirement
    trace_refs: [M_ENT_PAINPOINT_COUNT, M_ENT_PAINPOINT_SEVERITY, Q018]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F03-FINANCE-METRIC
    frame_id: F-RISK-03
    host_label: 融资维度卡片问题项数或严重度实际值
    marker_type: metric_spec
    source_relation: direct_requirement
    trace_refs: [M_ENT_PAINPOINT_COUNT, M_ENT_PAINPOINT_SEVERITY, Q018]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F03-MANAGEMENT-METRIC
    frame_id: F-RISK-03
    host_label: 管理维度卡片问题项数或严重度实际值（仅实际展示时）
    marker_type: metric_spec
    source_relation: direct_requirement
    trace_refs: [M_ENT_PAINPOINT_COUNT, M_ENT_PAINPOINT_SEVERITY, Q018]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F03-MOCK
    frame_id: F-RISK-03
    host_label: 诊断数据说明标题
    marker_type: mock_badge
    source_relation: product_interpretation
    trace_refs: [E-29]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F03-OBJECT-SNAPSHOT-NOTE
    frame_id: F-RISK-03
    host_label: 全部分析对象抽屉底部快照说明
    marker_type: review_copy
    source_relation: product_interpretation
    trace_refs: [US-ENT-RISK-OBJECT, US-ENT-RISK-PAIN, ENT-RISK-USM-24]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F05-HISTORY-TITLE
    frame_id: F-RISK-05
    host_label: 最近分析标题
    marker_type: review_copy
    source_relation: product_interpretation
    trace_refs: [US-ENT-RISK-HISTORY]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F06-SUPPLY-REPORT
    frame_id: F-RISK-06
    host_label: 供应链分析报告标题
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [E-28, US-ENT-RISK-REPORT]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
  - mount_id: ENT-RISK-F06-PAIN-REPORT
    frame_id: F-RISK-06
    host_label: 痛难点分析建议报告标题
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [E-29, US-ENT-RISK-REPORT]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent
```

## 9. 页面状态矩阵

| 状态 | 配置 | 结果 / 历史 / 报告 |
| --- | --- | --- |
| 默认 | 配置态在 Tab 上方显示共享对象，并显示当前 Tab 配置和预检 | 历史显示最近任务 |
| 加载 | 分区骨架且布局稳定 | 任务摘要、图谱 / 诊断区骨架 |
| 空对象 | 显示前往对比篮入口 | 不产生结果 |
| 对象超限 | 预检区指明当前 / 上限，底部“开始分析”禁用 | 不产生结果 |
| 部分数据缺失 | 按对象 / 维度说明缺失影响 | 缺失原因持续可见 |
| 痛难点对象 6–50 家 | 配置态显示前三家 + 管理全部对象；管理抽屉可搜索、每页 10 家并移除当次对象 | 摘要前三家 + 等 N 家；按钮位于摘要下方左对齐；全部对象抽屉只读可检索，关闭后保留结果焦点 |
| 共性问题 >5 项 | N/A | 首屏显示影响企业数最高的 5 项；完整问题视图可检索、按维度 / 数据状态筛选并分页 |
| 单个问题影响企业 >3 家 | N/A | 首屏最多 3 家典型企业；完整受影响名单可检索、筛选、分页并查看企业命中摘要 |
| 图谱无关系 | 允许提交前阻断或结果稳定空态 | 不补造节点或边 |
| 图谱一级初始态 | N/A | 仅一级可见；存在子级的节点显示可展开标识 |
| 图谱节点展开中 | N/A | 当前节点显示加载态，现有图谱与路径保持稳定 |
| 图谱节点展开成功 | N/A | 追加下一层、更新路径 / 深度，可折叠该分支 |
| 图谱节点无子级 | N/A | 显示“暂无下级关系”，不表现为点击无响应 |
| 图谱节点展开失败 | N/A | 保留现状并允许只重试当前节点 |
| 图谱三级上限 | N/A | 显示“已达最大展开深度”，不继续请求下一层 |
| Q017 / Q018 未闭合 | DEMO / 评审态明确待核对 | 不显示正式批准口径 |
| 生成中 | 进入独立过程页，可离开 | 最近分析和资产中心显示同一处理中任务 |
| 生成完成 | 停留过程页，显示“分析结果已生成” | 用户主动点击“查看分析结果”或“查看最近分析”；不得自动跳转 |
| 生成失败 | 显示失败阶段和错误编号 | 可重试 / 按此配置新建 |
| 无权限 | 保留结构并说明原因 | 敏感值不渲染，报告下载受限 |
| 报告已存在 | N/A | 复用处理中或有效报告 |

## 10. 响应式、视觉与禁止项

- **屏幕层级**：medium；本期不单列 small，不以简单缩放伪造小屏交付。
- **设计系统**：`agent-delivery/Design.md` 浅蓝白 + Arco；V1 位于 `demo-ui-topic` 参照沙箱。
- 图谱在中屏优先使用“画布 + 右侧列表 / 抽屉”；信息密度不足时列表可下移，但不把关系图缩成不可读缩略图。
- 对象、过程、报告、历史交互复用企业评估范式；业务差异只体现在对象上限、配置项、结果结构和报告模板。
- 配置页最终提交动作复用企业评估的页面级底部操作栏范式；风险洞察仅保留“开始分析”主按钮，预检卡片不承载提交动作。
- 禁止分析完成后自动跳转结果页；禁止把“按此配置新建分析”和报告动作堆在任务摘要同一动作组；禁止用“创建 / 查看报告”掩盖报告任务状态。
- 禁止在页面标题区重复设置“最近分析”按钮；最近分析仅作为模式区第三个页面级 Tab 呈现。
- 禁止把过程状态按钮放在任务摘要卡或“可视化分析过程”卡标题栏；过程动作只能位于语义 Alert 下方右侧。
- 禁止把“开始分析”放回“数据与权限预检”标题栏或在配置页生成第二个同功能入口；禁止为对齐布局而新增模板能力。
- 禁止配置态平铺 6–50 家对象标签；禁止把“管理全部对象”抽屉变成新增企业入口或将当次移除回写对比篮。
- 禁止在风险洞察页新增企业搜索、风险总览榜、企业评分、替代供应商推荐、一企一策或服务派单。
- 禁止在痛难点结果摘要平铺 6–50 家对象、无限展开全部共性问题或典型企业；禁止把影响企业数、影响比例或严重度转换成企业排名。
- 禁止从集合结果下钻时创建隐式单企任务、第二份报告指纹或重复历史记录。
- 禁止由前端计算正式风险等级、中心性、严重度或行业差距；禁止使用 Mock 冒充 FULL。

## 11. Wireframe 自检

- [x] 六个业务 Frame 覆盖对象、配置、过程、两类结果、历史和报告；评审追溯作为跨 Frame 覆盖，不伪造业务 Frame。
- [x] 七项当前可见统计字段均落到字段表第六列 metric_id；`M_ENT_PAINPOINT_GAP` 仅登记，不冒充当前可见字段。
- [x] 默认、加载、空对象、超限、缺失、无关系、失败、无权限和报告状态齐全。
- [x] 企业选择、报告、历史和资产交互与企业评估同构，差异项明确。
- [x] E-28 / E-29 都有独立结果和报告落点，未静默删除供应链导出能力。
- [x] F-RISK-01～F-RISK-06 的边界、任务流、两类结果、报告 / 历史 / 状态已由 `human:高颖` 确认，并于 2026-07-20 完成偏差修订。
- [x] 用户侧不出现展开层级选择；多级下钻具备初始、可展开、加载、成功、折叠、无子级、失败和三级上限状态。
- [x] 来源与分析对象位于两个分析 Tab 上方；切换 Tab 不改变对象，并分别保留关系范围与诊断维度草稿。
- [x] 页面级 Tab 顺序为“供应链关系 / 发展痛难点 / 最近分析”；历史态仅第三个 Tab 选中，标题区无重复入口。
- [x] 图谱顶部轻量状态行、右下角静态图例、展开提示和右侧分析结果职责分离，不使用 KPI 卡或标签混淆状态与图例。
- [x] “关键节点与断链风险”标题具备独立原需求追溯挂载；风险项和供应链报告承接备份方案提示且不扩展为方案生成能力。
- [x] 标题、实际数值和数据说明区域的评审挂点职责分离；痛难点问题清单追溯已恢复，四维指标均为唯一挂点，未创建无量化字段的行业差距挂点。
- [x] 分析完成后停留过程页并由用户主动查看结果；两类结果页顶部动作和末尾独立报告区块与企业评估范式一致。
- [x] F-RISK-01 的“开始分析”归位为底部页面级唯一主提交动作；预检区仅承载状态与阻断原因。
- [x] F-RISK-04 使用任务摘要卡 +“可视化分析过程”卡；纵向阶段、语义 Alert 和底部右对齐操作行与企业评估样式一致。
- [x] 痛难点多对象结果已定义紧凑摘要、全部对象抽屉、共性问题 Top 5、典型企业上限、完整受影响名单与企业命中摘要，供应链 1–2 家规则不变。
- [x] 配置态多对象已定义前三家摘要、可编辑管理抽屉、名称搜索、每页 10 家和当次移除；结果对象按钮位于摘要下方左对齐，快照说明仅评审模式显示。
- [x] `review_trace_contract` 覆盖每个业务 Frame，业务模式隐藏评审 Marker。
