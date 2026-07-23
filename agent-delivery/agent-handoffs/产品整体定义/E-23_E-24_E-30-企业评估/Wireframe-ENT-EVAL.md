# Wireframe-ENT-EVAL.md

> **模块**：企业评估（ENT-EVAL）
> **需求集合**：`E-23 / E-24 / E-30`（`REQ-ENT-003 / 004 / 010`）
> **版本**：v1.11 · 2026-07-23
> **屏幕 / 轨道**：仅 `medium_1440_1920` · Track-MS
> **布局结论**：纵向分区工作台（方案 A），不采用全页横向分栏
> **视觉基线**：`agent-delivery/Design.md` + Arco 组件体系

## 1. Frame 清单

| Frame | 名称 | 路由 / 状态 | 主要 Story |
| --- | --- | --- | --- |
| `F-EVAL-01` | 评估配置工作区 | `?mode=technology|business|competitiveness` | OBJ / TECH / BIZ / COMP / QUALITY |
| `F-EVAL-02` | 评估结果工作区 | `?view=result&task_id=...` | RESULT / REPORT |
| `F-EVAL-03` | 最近评估 | `?view=history` | HISTORY |
| `F-EVAL-04` | 报告任务状态 | 结果页抽屉 / 资产中心链接 | REPORT |
| `F-EVAL-05` | 内部评审追溯层 | 环境级 `reviewMode` | 各模式评审验收 |
| `F-EVAL-06` | 评估生成过程 | `?view=processing&task_id=...` | RESULT |
| `F-EVAL-07` | 指标说明抽屉 | 配置页 Drawer | QUALITY |
| `F-EVAL-08` | 个人中心评估任务 | `/personal/assets` | HISTORY |
| `F-EVAL-09` | 日额度超限简单弹窗（待批准） | 上游“下一步”或配置页“生成评估”动作内状态 | ENTITLEMENT |

## 2. F-EVAL-01｜评估配置工作区

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ {review only: 企业评估 [i]}                                               │
├──────────────────────────────────────────────────────────────────────────┤
│ ① 评估对象                                                             │
│ 来自对比篮 · 50 家 [企业 A ×] [企业 B ×] [企业 C ×]                  │
│ [管理全部对象（50 家）]                         [返回对比篮调整对象] │
├──────────────────────────────────────────────────────────────────────────┤
│ [技术力评估] [商业力评估] [综合竞争力评估] [最近评估]（一级导航）       │
├──────────────────────────────────────────────────────────────────────────┤
│ ② 评估模板                                                             │
│ 评价行业 [目标行业 ▾]  模板 [系统模板 / 我的模板 / 当次配置 ▾]          │
│ 已应用：集成电路行业模拟预览 · 非正式行业评价标准                      │
│ {review only: 正式行业映射与默认权重尚未闭合}                          │
│ 生成后系统自动命名任务（说明仅在评审模式展示）                         │
├──────────────────────────────────────────────────────────────────────────┤
│ ③ 指标与权重                                                           │
│ 分组 / 维度折叠面板                                                     │
│ ☑ 指标名称       数据状态    权重[ 25 ]   数据源    [查看指标说明]       │
│ ...                                      [一键平均分配] 合计 100         │
│ ⚠ 当前使用临时默认权重，待甲方确认                                     │
├──────────────────────────────────────────────────────────────────────────┤
│ ④ 数据覆盖与可信度预检                                                 │
│ [按企业名称定位] [全部可信度 ▾] 当前可见 50 / 50 家                  │
│ 企业覆盖卡 3×3（每页 9 家）                              [1 2 3…]   │
├──────────────────────────────────────────────────────────────────────────┤
│ [保存为个人模板]                                         [生成评估]     │
└──────────────────────────────────────────────────────────────────────────┘
```

### 2.1 区块与字段

| 序号 | 区块 / 控件 | 用户目的 | 字段 / 状态 | 数据 / 来源 | metric_id |
| ---: | --- | --- | --- | --- | --- |
| 1 | 评审标题与一级导航 | 评审追溯 / 明确当前业务模式或历史视图 | `reviewMode`、`mode`、`view=history` | “企业评估 + REQ”整组仅评审模式；一级导航业务态保留，最近评估为第四项 | N/A |
| 2 | 来源与对象标签 | 确认或移除本次评估范围 | `enterprise_codes[]`、`source`、`return_context_id` | 对比篮 / 权限服务；移除仅更新当次配置 | N/A |
| 3 | 任务展示名规则 | 生成后识别任务 | `task_display_name` | 任务服务按模式、企业数量、生成时间创建；规则说明仅评审模式展示 | N/A |
| 4 | 模板选择 | 复用指标配置 | `template_id`、`template_version`、`template_scope` | 模板服务 | N/A |
| 5 | 指标选择 | 控制当次模型 | `indicator_selected` | 指标注册表 | 见 2.2 |
| 6 | 权重整数输入 | 控制当次重要性 | `weight` 0～100、层级合计 100 | 用户输入 / 模板快照 | N/A |
| 7 | 一键平均分配 | 快速形成合法权重 | `equal_distribute` | 前端交互计算，仅配置值 | N/A |
| 8 | 数据状态 | 识别可用 / 缺失 / 无权 | `data_status` | Java 聚合预检 | 对应指标 metric_id |
| 9 | 覆盖度 | 判断可生成性 | `coverage_rate` | 后端预检结果 | N/A（质量状态） |
| 10 | 可信度 | 判断结论强度 | `confidence_level` | 已登记规则 / 后端 | N/A（质量状态） |
| 11 | 指标说明 | 查看业务语义与缺失影响 | 业务抽屉；评审模式追加 `MetricSpecCard` 元数据 | 指标注册表 | 对应指标 metric_id |
| 12 | 生成评估 | 创建正式任务 | `generate` | 后台评估任务 API | N/A |
| 13 | 评价行业与配置状态 | 按行业调整商业评价维度并识别预览 / 自定义状态 | `industry_code`、`industry_preview_state=preview_applied/custom_preserved`、行业适用指标、整数默认权重、待切换行业 | E-24 直接要求；当前 DEMO 为确定性模拟预览，正式产业标签与模板服务受 Q014 阻断 | N/A |
| 14 | 企业中英文名称 | 识别对象并预留国际化 | `enterprise_name`、`enterprise_name_en` | 企业数据；中文为主，英文按可用性展示 | N/A |
| 15 | 待确认提示 | 识别临时默认口径 | `pending_confirmation` | SRS §6 / Q014；业务模式可见 | 对应待确认指标 |
| 16 | 配置对象渐进披露 | 在 50 家范围内确认和当次移除对象 | 1–5 家全部标签；6–50 家前 3 家 + `manage_all_objects`；名称定位 / page=10 / remove | 当前配置对象集合；不回写对比篮 | N/A |
| 17 | 覆盖与可信度可见切片 | 定位特定企业或可信度状态 | enterprise_search / confidence_filter / page=9 / visible_count / total_count | 全量预检结果；控件只改变可见范围 | N/A |
| 18 | 日权益预检 | 在创建任务前识别对应分类剩余额度 | `evaluation_category`、`used_count`、`daily_limit`、`reset_at`、`feature_enabled` | 共享权益服务；前端不维护计数真源 | N/A（权益状态） |

模板下拉按“系统模板 / 我的模板 / 当次自定义配置”分组；“我的模板”只列当前模式已保存的个人历史模板，并显示名称、指标数量与保存时间。三种评估均支持鼠标点击当前值区域或键盘展开选择；选择后恢复指标和权重，不恢复企业对象；个人中心使用同一模板资产源。个人模板名称不写入 `task_display_name`，任务展示名只在生成成功后产生。

### 2.2 模式指标

| 序号 | 模式 / 分组 | 用户目的 | 字段 / 状态 | 数据 / 来源 | metric_id |
| ---: | --- | --- | --- | --- | --- |
| 1 | 技术力 / 综合得分 | 比较技术能力 | score | 算法待 Q014 | `M_ENT_TECH_POWER_SCORE` |
| 2 | 技术力 / 排名 | 识别相对位置 | rank | 算法待 Q014 | `M_ENT_TECH_RANK` |
| 3 | 技术力 / 专利 | 查看创新产出 | patent_grant_count | 专利 ADS | `M_ENT_PATENT_GRANT_COUNT` |
| 4 | 技术力 / 研发投入 | 查看研发强度 | rd_investment_ratio | 数据 / 算法待 Q014 | `M_ENT_RD_INVESTMENT_RATIO` |
| 5 | 商业力 / 综合得分 | 比较商业能力 | score | 算法待 Q014；TRACE 登记 E-23/E-24 错配 | `M_ENT_BUSINESS_POWER_SCORE` |
| 6 | 商业力 / 营收 | 查看经营规模 | revenue_latest | 企业经营 ADS | `M_ENT_REVENUE_LATEST` |
| 7 | 商业力 / 营收增长 | 查看增长性 | revenue_growth_rate | 数据 / 算法待 Q014 | `M_ENT_REVENUE_GROWTH_RATE` |
| 8 | 商业力 / 利润率 | 查看盈利质量 | profit_margin | 数据 / 算法待 Q014 | `M_ENT_PROFIT_MARGIN` |
| 9 | 商业力 / 市占率 | 查看市场位置 | market_share | K-O7 无正式来源；当前决策 Q019 待编号统一 | `M_ENT_MARKET_SHARE` |
| 10 | 综合竞争力 / 得分 | 查看综合能力 | score | 算法待 Q014 | `M_ENT_COMPETITIVENESS_SCORE` |
| 11 | 综合竞争力 / 排名 | 查看相对位置 | rank | 算法待 Q014 | `M_ENT_COMPETITIVENESS_RANK` |
| 12 | 综合竞争力 / 短板数 | 识别改进项 | shortboard_count | 算法待 Q014 | `M_ENT_SHORTBOARD_COUNT` |
| 13 | 综合竞争力 / 创新指数 | 查看创新维度 | innovation_index | 算法待 Q014 | `M_ENT_INNOVATION_INDEX` |
| 14 | 技术力 / 专利引用 | 查看创新影响 | patent_citation | 未登记；不得以专利授权量替代 | `GAP-METRIC-BID-01` |
| 15 | 技术力 / 研发人员占比 | 查看技术人才投入 | rd_personnel_ratio | 未登记；不得以研发投入强度替代 | `GAP-METRIC-BID-02` |
| 16 | 技术力 / 核心技术覆盖度 | 查看核心技术布局 | core_technology_coverage | 未登记 | `GAP-METRIC-BID-03` |
| 17 | 商业力 / 客户集中度 | 判断客户结构风险 | customer_concentration | K-O7 无正式来源 | `GAP-METRIC-BID-04` |
| 18 | 商业力 / 品牌声量 | 判断品牌影响 | brand_voice | K-O7 无正式来源 | `GAP-METRIC-BID-05` |
| 19 | 综合竞争力 / 组织能力 | 承接技术+市场+组织框架 | organization_capability | 未登记 | `GAP-METRIC-BID-06` |

综合竞争力使用两层权重：先配置维度权重，再在每个维度折叠面板中配置指标权重；两层分别校验 100，不合并成一个长表。

### 2.2.1 Bid 维度契约

| 模式 | 必须保留的直接维度 | 当前处理 |
| --- | --- | --- |
| 技术力 | 技术人才、技术创新、技术转化、技术合作、技术投入 | 逐轴 `metric_id` 和归一化规则受 `Q014 / GAP-METRIC-BID-07` 阻断；DEMO 只能显式标记，不进入正式评分。 |
| 商业力 | 市场、产品、品牌、技术合作、产业链覆盖率、关键环节参与度 | 逐维指标与数据源受 `Q014 / K-O7 / GAP-METRIC-BID-08` 阻断。 |
| 综合竞争力 | 技术、市场、组织；并映射规模、财务、人力资源、市场表现 | 组织能力和算法维度映射受 `Q014 / GAP-METRIC-BID-06/09` 阻断；成长性、创新度、抗风险只能作为产品化追加维度。 |

### 2.3 交互规则

- 对象区空态仅显示居中的蓝色主按钮“前往对比篮选择企业”，标题右侧不显示同功能次按钮；存在对象时标题右侧才显示“返回对比篮调整对象”。
- 一级导航顺序固定为“技术力评估 / 商业力评估 / 综合竞争力评估 / 最近评估”。最近评估作为第四个导航 Tab，选中后进入 `view=history`；前三项仍是业务评估模式，第四项不是新的业务模式。
- 不得在页头保留“最近评估”入口。历史视图中点击前三个 Tab 时清除 `view=history` 并进入对应模式配置；不得同时保留页头按钮与第四个 Tab。
- 评估对象是三模式共用的单一上下文，只在配置视图的模式选择器上方渲染一次；切换模式保留同一对象集合，并按技术力 / 商业力至少 2 家、综合竞争力至少 1 家重新校验最少对象数。
- 配置对象 1–5 家完整显示可移除标签；6–50 家显示前 3 家和“管理全部对象（N 家）”。管理抽屉按中英文名称定位、每页 10 家并允许“移出本次评估”；不得在抽屉新增对象或回写对比篮。搜索、翻页和关闭抽屉后仍使用完整当前对象集合校验。
- 模式切换若已有未保存配置，先确认“保留为当前模式草稿 / 放弃并切换”；不把不兼容指标带到新模式。
- 权重只用数字输入，不用滑杆；允许键盘输入与步进，禁止负数、小数和大于 100。
- “一键平均分配”对当前权重层级执行；余数按稳定顺序分配并在执行前说明结果。
- 不静默归一化；合计错误时区块标题和具体输入同时报错。
- 只有预检通过后“生成评估”可用；低可信可确认继续，<50% 或关键指标全缺不可继续。
- 正式数据覆盖与可信度预检由 Java 聚合后端负责；前端先对对象数量、指标选择和权重合计做目标 ≤100ms 的本地校验。对象、模式或已选指标变化时防抖 300～500ms 后触发后端预检；仅权重变化时只做前端本地校验。
- 数据覆盖与可信度卡每页显示 9 家，支持名称定位和可信度筛选，并显示“当前可见 X / N 家”；筛选与分页不得改变全量预检、阻断条件或跨企业可比性提示。
- 后端预检常规响应参考区间为 1～3 秒、普通请求目标 ≤3 秒，P95 ≤5 秒；时延从预检请求发出起算，到前端收到可渲染结果止，不包含触发前防抖。请求发出后等待超过 300ms 保持稳定 loading，超过 5 秒显示“仍在预检”并提供重试。未取得预检通过结论时禁止静默启用“生成评估”；该交互规则为 `product_interpretation`，不改变当前交付阶段。
- 保存个人模板只保存模板名称、指标 / 权重 / 展示偏好，不保存任务展示名、企业对象和未授权字段。
- 商业力首次进入或当前配置未改动时，选择行业后加载该行业适用指标与整数默认权重并保持合计 100%；当前 DEMO 使用确定性模拟预览，业务模式显示“行业模拟预览、非正式行业评价标准”。
- 商业力已有指标或权重改动时，切换行业必须弹出三路径确认：“应用行业配置”放弃改动并加载目标行业预览；“保留自定义配置”只切换行业上下文并保留当前指标 / 权重；“取消”保持行业、指标和权重完全不变。
- 业务与评审模式共享同一行业切换结果和确认流程。评审模式仅追加正式行业映射与默认权重未闭合说明；不得保留“切换行业不会改变本次指标或权重”的旧业务结论。
- 使用 Q014 临时默认值时业务模式持续显示“待甲方确认”；K-O7 数据未完成采购授权与合规确认前保持不可用。
- 限额开关开启时，上游“下一步”已明确模式则先做体验预检；直接进入配置、历史复用或个人中心复用在“生成评估”前预检。预检不扣减。
- 任务创建接口必须再次校验，并原子完成 `task_id` 创建与一次分类额度扣减；预检通过不得作为最终放行凭证。
- 超限打开 `F-EVAL-09`；权益服务异常或配置无效时失败关闭并允许重试。两者都保留对象、模式、模板、指标和权重。

### 2.4 F-EVAL-06｜评估生成过程

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ 评估生成中 · 技术力评估 · 2 家企业 · TASK-...                          │
│ [任务提交 ✓]—[权限与配置校验 ✓]—[企业数据汇聚 ●]—[指标计算]—[可信校验]—[结果组装] │
│ 当前阶段：企业数据汇聚     已用时间：00:18                              │
│ 可离开本页，任务将在后台继续；可从最近评估或个人中心恢复。              │
│                                               [返回配置] [稍后查看]     │
└──────────────────────────────────────────────────────────────────────────┘
```

- 只展示当前阶段、已完成阶段和已用时间，不显示无法由后台证明的百分比。
- 六阶段依次为任务提交、权限与配置校验、企业数据汇聚、指标计算、可信度与可比性校验、结果图表组装。
- 完成态显示“查看评估结果”；失败态保留失败阶段与错误编号，提供“重新尝试”或“按此配置新建评估”。
- 离开页面不取消任务；最近评估和个人中心必须以同一 `task_id` 恢复。

### 2.5 F-EVAL-07｜指标说明抽屉

| 字段 | 业务模式 | 内部评审模式 | 规则 |
| --- | --- | --- | --- |
| 指标名称、衡量目的、所属维度 | 显示 | 显示 | 解释指标用途，不修改配置 |
| 业务口径、单位、指标方向、适用范围 | 显示 | 显示 | 使用业务可理解语言 |
| 数据状态、缺失影响 | 显示 | 显示 | 明确缺失是否降级可信度或阻断生成 |
| `metric_id`、公式、源表、源系统 | 不渲染 | 显示 | 内部指标元数据 |
| 更新频率、版本、`Q014 / K-O7 / GAP-SOURCE-01` | 不渲染 | 显示 | 仅用于评审和口径闭合 |

抽屉由指标行“查看”打开，关闭后保持当前对象、模板、指标选择和权重；不得把 `metric_id`、源表、源系统或开放问题泄露到业务模式。

### 2.6 F-EVAL-09｜日额度超限简单弹窗（待批准）

```text
┌──────────────────────────────────────────────┐
│ 今日技术力评估发起次数已用完            [×] │
├──────────────────────────────────────────────┤
│ 你今日的技术力评估额度已用完。              │
│                                              │
│ 评估类别  技术力评估                        │
│ 今日用量  3 / 3                             │
│ 重置时间  明日 00:00（北京时间）            │
├──────────────────────────────────────────────┤
│                     [我知道了] [联系开通]    │
└──────────────────────────────────────────────┘
```

| 区块 / 控件 | 用户目的 | 字段 / 状态 | 来源与规则 | metric_id |
| --- | --- | --- | --- | --- |
| 标题 | 直接理解拦截原因 | `今日{category_label}发起次数已用完` | ENT-EVAL 分类映射 | N/A |
| 评估类别 | 确认受限的是哪一类 | `evaluation_category` / `category_label` | `technology / business / comprehensive` | N/A |
| 今日用量 | 理解已用与总额 | `used_count / daily_limit` | 权益服务真源 | N/A（权益状态） |
| 重置时间 | 知道何时可再次使用 | `reset_at` | 服务端绝对时间；按北京时间表达 | N/A（时间字段） |
| 联系开通 | 寻求升级 | `contact_channel.channel_type / button_label / target` | 开关启用前必须有效配置 | N/A |
| 我知道了 / 关闭 / Esc | 返回当前工作 | close | 保留对象、模式、模板、指标、权重和来源上下文 | N/A |

- 弹窗不展示完整等级矩阵、套餐价格、支付表单、订单或“立即支付”。
- `contact_channel` 缺失时配置中心禁止开启限额开关，不允许上线无主动作死路。
- 内部评审模式只在标题宿主挂载 `ENT-EVAL-F09-QUOTA-TITLE`；业务模式追溯节点不存在，但上述业务字段不变。
- 权益服务异常不使用本弹窗伪装为超限；就近显示“暂时无法校验权益，请稍后重试”和重试入口。
- 多端竞争导致最终创建校验超限时复用同一弹窗，并保持当前配置。

## 3. F-EVAL-02｜评估结果工作区

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ ← 企业评估  技术力评估 · TASK-20260717-001  [i] [按此配置新建评估]    │
│ 对象 50 家 · 企业 A、企业 B、企业 C 等 50 家                           │
│ [查看全部对象]（第二行、与对象文字左对齐）                             │
│ 系统模板 v2 · 算法 vX · 生成时间                                        │
├──────────────────────────────────────────────────────────────────────────┤
│ [综合得分] [排名] [覆盖度] [可信度]                                     │
│ 结论条：领先维度、主要差距与“不可外推”说明                              │
├──────────────────────────────────┬───────────────────────────────────────┤
│ 模式解释型分析                   │ 综合排名摘要                          │
│ [单企诊断 / 双企对比]            │ 按本次任务综合得分排序                │
│ [搜索企业 A ▾] [搜索企业 B ▾]    │ Top 5（主蓝）                         │
│ 雷达 / 全对象经营指标卡（6家/页）│ —— 类别间隔 ——                        │
│                                  │ Bottom 5（中性灰） [查看完整排名]    │
├──────────────────────────────────┴───────────────────────────────────────┤
│ 技术指标与差距诊断：全对象 / 10家每页 / 综合得分 / 原始指标 / 可信度 │
│ 商业力：[经营诊断（全对象10家/页）] [营收趋势]                         │
│ 综合竞争力与差距诊断：综合得分 / 可信度 / 维度差距 / 优势短板          │
├──────────────────────────────────────────────────────────────────────────┤
│ 评估报告 [创建 PDF 报告] [查看已有报告]                                 │
└──────────────────────────────────────────────────────────────────────────┘
```

| 序号 | 区块 / 控件 | 用户目的 | 字段 / 状态 | 数据 / 来源 | metric_id |
| ---: | --- | --- | --- | --- | --- |
| 1 | 任务摘要 | 确认结果上下文 | task / object / template / batch / algorithm / permission snapshot | 后台任务快照 | N/A |
| 1A | 紧凑对象摘要 / 全部对象抽屉 | 确认任务范围并定位对象 | enterprise_names / object_count / validity / data_status / search / page=10 | 任务快照；1–5 家全显，6–50 家前三家 + 等 N 家；按钮位于文字下方并左对齐；抽屉只读 | N/A |
| 2 | KPI 卡 | 快速读取关键结果 | ≤4 个模式关键指标 | 正式算法结果 | 当前模式 metric_id |
| 3 | 结论条 | 理解主要结论及限制 | conclusion、confidence_warning | 后端结构化结果 / 规则 | N/A |
| 4 | 分析视角 | 切换单企诊断 / 双企对比 | analysis_view | 结果页本地观察状态，不写回任务 | N/A |
| 5 | 企业 A / B 选择 | 从任务对象集选择比较对象 | compare_enterprise_a / compare_enterprise_b | 任务对象快照；不可重复 | N/A |
| 6 | 模式解释型分析 | 比较企业 / 维度 | chart_series | 后端结果；DEMO 值须显式标记，不由图表组件补正式值 | 当前模式 metric_id 或显式 GAP |
| 7 | 排名摘要 / 完整排名二级视图 | 识别重点与完整集合位置 | composite_score / snapshot_rank / confidence / data_status / search / page=10 | 任务快照模式综合得分；≤10 家全显，>10 家 Top 5 主蓝 + Bottom 5 中性灰 + 类别间隔；完整名次固定 | 模式综合得分 / 排名 metric_id |
| 8 | 模式诊断 | 复核综合结果、原始值、可信度和差异 | composite_score / value / unit / per_enterprise_confidence / set_average / set_leader / gap / advantage / shortboard / missing_reason / page | 技术与商业覆盖全对象且每页 10 家；综合竞争力按单企 / A/B；只比较共同可用数据 | 模式综合得分及相关 metric_id |
| 8A | 商业关键经营指标卡 | 查看全对象经营指标 | enterprise_search / revenue / growth / profit / page=6 / visible_count / total_count | 任务快照全部对象；搜索与分页只改变可见范围 | 商业经营指标 metric_id |
| 9 | 趋势 / 建议状态 | 判断后续输出是否可用 | trend_availability / recommendation_availability | 正式时序数据与建议模型；缺失时只显示状态 | 相关 metric_id 或显式 GAP |
| 10 | 可信度说明 | 判断可比性 | per_enterprise_confidence | 后端质量结果 | N/A |
| 11 | 报告入口 | 沉淀材料 | report_fingerprint / status | 报告服务 | N/A |

### 3.1 可视化矩阵

| 模式 | 左侧解释型分析 | 右侧排名 | 下方诊断 |
| --- | --- | --- | --- |
| 技术力 | 统一到 0～100 的技术维度双企雷达；2 家直接使用，≥3 家默认综合得分前两名并允许从任务对象中搜索重选 A / B | ≤10 家完整；>10 家 Top 5 + Bottom 5，完整技术力加权排名进入二级视图 | 单一“技术指标与差距诊断”覆盖任务全部对象、每页 10 家；A/B 只控制雷达，不裁剪诊断表；趋势 / 建议缺失在表前提示 |
| 商业力 | 营业收入、收入增长率、利润率全对象指标卡，不用雷达、不与专利混画；支持企业名称定位并每页 6 家 | ≤10 家完整；>10 家 Top 5 + Bottom 5，完整商业力排名进入二级视图 | “经营诊断”覆盖任务全部对象并每页 10 家；“营收趋势”无连续数据时显示缺失状态，市场份额不可用 |
| 综合竞争力 | 1 家为单企 vs 集合均值 / 领先值；2 家直接双企；≥3 家可切单企诊断 / 双企对比并搜索对象 | ≤10 家完整；>10 家 Top 5 + Bottom 5，完整综合竞争力排名进入二级视图 | 单一“综合竞争力与差距诊断”只展示当前单企或 A / B，保留得分、可信度、均值 / 领先值、差距和优势短板 |

缺失雷达点显示断点 / 缺失标识，不绘制为 0；多企业数据覆盖不同，在图表上方显示可比性警告。技术力雷达轴在 FULL 前必须逐轴登记 `metric_id` 和归一化规则；当前受 `Q014 / GAP-VIS-01` 约束。

### 3.2 技术力结果细节

- 雷达区标题为“技术力多维雷达对比”，选择器位于标题右侧。
- 雷达不得直接使用技术力排名、专利原始数量或研发投入百分比作为同量纲轴。
- 正式维度轴和归一化公式由后端结果返回；未完成指标登记时只能展示明确标注的 DEMO 维度，不进入官方得分。
- 排名区标题为“技术力加权排名”，始终覆盖任务中的全部有效企业。
- 排名默认呈现遵循渐进披露：≤10 家完整展示，>10 家展示 Top 5 + Bottom 5；“查看完整 N 家排名”打开二级视图，支持企业名定位、可信度 / 数据状态筛查和分页，但不重算任务快照名次。
- Top 5 条形使用主蓝，Bottom 5 使用中性灰，两组之间插入一个无数据类别间隔，并在卡片右上方显示同色图例。
- 排名下方只保留一个覆盖任务全部对象、每页 10 家的“技术指标与差距诊断”：技术力综合得分使用 `M_ENT_TECH_POWER_SCORE`，原始指标保留各自单位，可信度读取后端质量结果，差距以任务快照中的技术力综合得分计算。A/B 选择只改变雷达，不裁剪诊断表。
- 不再渲染第二张“指标明细与综合差距”企业表；趋势与改进建议无正式数据时，缺失提示放在“技术指标与差距诊断”内部，不用重复列表表达。
- 结果保留“趋势变化”和“改进建议”落位；无正式时序数据或建议模型时显示 `GAP-OUTPUT-BID-01`，不得用通用文案补造。

### 3.3 商业力结果细节

- KPI 优先展示商业力综合得分、集合排名、最新营业收入、收入增长率或利润率，最多四项。
- 关键经营指标对比采用全对象数值卡，各指标保留亿元 / % 单位和方向；支持企业名称定位并每页显示 6 家，搜索和分页不改变对象集或排名。
- 下方统一为覆盖任务全部对象、每页 10 家的“商业诊断与明细”，在同一表内展示企业、营业收入、收入增长率、利润率、商业力综合得分、数据可信度和诊断结论；不显示排名序号、不提供排序入口或第二套排行结论，也不再叠加通用“指标明细与综合差距”。
- “营收趋势”只有在任务结果含连续年度值时渲染，最多选择两家；不存在历史值时显示“暂无连续年度营收数据”。
- `M_ENT_MARKET_SHARE` 在 K-O7 数据源与 GAP-SOURCE-01 编号冲突闭合前保持不可用，不显示替代值。
- 客户集中度与品牌声量同样受 K-O7 阻断；商业力配置必须保留按行业特性调整维度的入口。
- 结果保留六维分维分析、趋势变化和行业对标落位；未闭合时显示 `GAP-OUTPUT-BID-02`。

### 3.4 综合竞争力结果细节

- 默认“单企诊断”关注综合得分最高企业，可切换当前企业；参照线只使用对象集可计算的均值和领先值，不冒充外部同行标杆。
- “双企对比”从任务对象集中选择 A / B，默认综合得分前两名，二者不可重复。
- 下方只保留一个“综合竞争力与差距诊断”，不再渲染独立“指标明细与综合差距”企业表；右侧“综合竞争力排名”是唯一排名表达。
- 单企态在诊断区顶部显式展示当前企业名称、综合竞争力得分 `M_ENT_COMPETITIVENESS_SCORE` 和数据可信度；维度表展示技术 / 市场 / 组织等维度的当前得分、对象集均值、对象集领先值、差距与优势 / 短板结论。
- 双企态在同一诊断区展示企业 A / B 的综合竞争力得分与各自数据可信度；维度表展示 A / B 得分、差值和差异结论，不重复排名。
- 成长性、创新度、抗风险只有在技术、市场、组织三类直接要求完整保留且指标登记后才能作为产品化追加维度；规模、财务、人力资源、市场表现仍须映射至综合框架或显示显式 GAP。
- 结果保留综合竞争力趋势和分析报告落位；规模、财务、人力资源、市场表现未完成映射时显示 `GAP-METRIC-BID-09 / GAP-OUTPUT-BID-03`。

### 3.5 排名与任务快照

- 对象摘要 1–5 家显示全部名称；6–50 家只显示任务快照顺序中的前三家与“等 N 家”。“查看全部对象”打开只读抽屉，支持名称搜索、有效性 / 数据状态筛选和分页，不允许增删任务对象。
- 单企焦点或 A / B 选择器必须支持在任务对象集中按名称搜索；切换只影响解释型图表与综合竞争力当前诊断，不裁剪技术或商业全对象明细，不进入任务指纹。

- FULL 任务快照必须包含系统生成的 `task_display_name`、`template_id`、模板版本、`selected_indicator_keys`、整数权重、对象、模式、可信度、数据批次、算法版本、权限范围和生成时间。当前 DEMO 数据批次未接入，评审态显示“数据批次未接入”，业务态不显示该内部缺口，任何任务或报告指纹不得生成 `mock_20260618`。
- 排名只使用任务快照中的模式综合得分；不得取第一个已选指标、当前 KPI 卡或前端排序字段代替。
- 切换分析视角或企业 A / B 不改变任务快照、排名、报告指纹和历史结果。

## 4. F-EVAL-03｜最近评估

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ [技术力评估] [商业力评估] [综合竞争力评估] [最近评估●]                 │
├──────────────────────────────────────────────────────────────────────────┤
│ 最近评估                                       [模式筛选] [企业搜索]     │
├──────────────────────────────────────────────────────────────────────────┤
│ 任务 ID │ 模式 │ 企业摘要 │ 模板/版本 │ 数据批次 │ 时间 │ 可信度 │ 报告 │
│ ...                                                     [恢复结果] [⋯]  │
└──────────────────────────────────────────────────────────────────────────┘
```

| 序号 | 区块 / 控件 | 用户目的 | 字段 / 状态 | 数据 / 来源 | metric_id |
| ---: | --- | --- | --- | --- | --- |
| 1 | 历史行 | 识别正式任务 | task_id / mode / enterprise_summary | 评估任务服务 | N/A |
| 2 | 版本信息 | 判断可复现性 | template_version / data_batch / algorithm_version | 任务快照 | N/A |
| 3 | 可信度 | 判断结果质量 | confidence_level | 任务快照 | N/A |
| 4 | 报告数 | 找回产物 | report_count | 资产 / 报告服务 | N/A |
| 5 | 恢复结果 | 回到不可变结果 | task_id | 结果路由 | N/A |
| 6 | 按此配置新建评估 | 复用当前任务配置创建新评估 | source_task_id | 新草稿，不覆盖旧任务 | N/A |
| 7 | 关联报告 | 查看任务产物 | report_ids | 资产中心 | N/A |

不提供团队共享、审批协作、复杂版本对比、批量任务管理或删除正式审计记录。

### 4.1 F-EVAL-08｜个人中心评估任务

个人中心“评估任务”和最近评估读取同一任务源，字段至少包含 `task_id`、状态、模式、企业摘要、创建时间、结果恢复地址和报告数。个人中心只提供跨场景“继续查看 / 查看结果”入口，不复制任务、不维护第二份状态，也不产生与最近评估不同的报告数。

## 5. F-EVAL-04｜报告任务状态

| 阶段 | 页面表现 | 允许动作 |
| --- | --- | --- |
| 已提交 | 显示任务 ID 和提交时间 | 关闭抽屉，后台继续 |
| 数据准备 | 显示数据批次 / 权限校验中 | 查看详情 |
| 评分计算 | 显示当前阶段，不伪造百分比 | 查看详情 |
| 图表生成 | 显示图表组装中 | 查看详情 |
| 报告组装 | 显示 PDF 生成中 | 查看详情 |
| 已完成 | 显示有效期、脱敏 / 审批标记 | 下载当前报告 / 去资产中心 |
| 失败 | 显示失败阶段和审计错误编号 | 重试 / 联系管理员 |

报告指纹至少包含：对象集合、模式、模板版本、权重、数据批次、算法版本、权限范围、报告模板。重复提交先查询后台，不以前端缓存判断事实。

“下载当前报告”只在报告完成且用户有权限时可用；下载必须绑定当前 `task_id` 与不可变结果快照。未完成、无权限或任务不一致时禁用并说明原因。当前 DEMO 未接入数据批次，报告指纹不得写入伪造批次值。

## 6. F-EVAL-05｜内部评审追溯层

| 挂载位置 | 追溯内容 | 禁止位置 |
| --- | --- | --- |
| 页面标题 | 聚合 REQ-ENT-003 / 004 / 010 | 普通按钮、分页、表格行 |
| 当前模式配置标题 | 当前模式 REQ、原始标题 / 摘要、能力链、状态 / Tier / Q、Story / IA / Frame | 每个指标行；指标使用 MetricSpecCard |
| 评价行业配置说明 | 正式行业映射、默认权重、临时模拟处理与闭环条件；仅评审模式展示 | 业务模式的行业预览状态和可执行控件 |
| 数据覆盖标题 | E-23/E-24/E-30 生成约束与四件套质量闸门，标记为产品化展开 | 每家企业覆盖卡重复挂载 |
| 结果子模块标题 | 具体 E-23/E-24/E-30 原需求摘要、来源、当前落位及直接承接/产品化展开关系 | 每张 KPI 卡、图表点、表格行重复挂载 |
| 对象快照说明 | “对象列表只读，顺序固定为任务创建时的对象快照；搜索与筛选不改变任务。”；仅评审模式显示于完整对象抽屉 | 业务模式、配置对象管理抽屉 |
| 排名默认范围说明 | “当前展示 Top 5 与 Bottom 5；按本次评估综合得分排序”；仅评审模式显示于排名摘要 | 业务模式的颜色图例和排名数据 |
| 完整排名快照说明 | “排名固定为任务快照结果；名称定位、可信度与数据状态筛选仅缩小可见范围，不触发重排。”；仅评审模式显示于完整排名抽屉 | 业务模式的搜索、筛选和分页控件 |
| 报告标题 | 继承当前模式 REQ | 最近评估和后台步骤伪造 REQ |

业务模式完全隐藏 `TraceInfoIcon`。评审模式只解释定义，不修改字段可见性，不绕过角色、等级、授权、脱敏或审批规则。

## 7. 页面状态矩阵

| 状态 | 配置页 | 结果 / 历史 / 报告 |
| --- | --- | --- |
| 默认 | 显示模式、对象区和系统模板 | 历史显示最近任务 |
| 加载 | 分区骨架屏，保留页面结构 | 任务摘要与图区骨架 |
| 空对象 | 不预填企业；评估对象和数据覆盖区均显示空态，提供前往对比篮入口 | N/A |
| 对象不足 | 指明当前 / 所需数量，禁用生成 | 不产生结果 |
| 权重错误 | 区块 + 字段双层报错 | 不产生结果 |
| 行业预览已应用 | 显示目标行业与“模拟预览、非正式行业评价标准”；按预览更新适用指标和整数权重 | 任务快照保存实际行业、指标和权重，不把预览声明为正式标准 |
| 行业切换且配置已改动 | 弹出“应用行业配置 / 保留自定义配置 / 取消”；选择前不改变任何配置 | 不产生新结果 |
| 保留自定义配置 | 行业上下文更新，指标与权重保持不变，并标记为自定义配置 | 任务快照保存实际自定义配置 |
| 预检请求发出后等待 >300ms | 数据覆盖区展示稳定 loading，保留页面结构且生成不可用 | 不产生结果 |
| 预检请求发出后等待 >5s | 显示“仍在预检”和重试入口；不得将等待视为通过 | 不产生结果 |
| 部分数据缺失 | 显示缺失和降级可信度 | 缺失点 / 明细原因持续可见 |
| 6–50 家对象 | 配置页对象集合保持不变 | 摘要前三家 + 等 N 家；全部对象抽屉只读可检索，关闭后保留当前焦点与滚动位置 |
| 配置对象 6–50 家 | 前 3 家可移除标签 + “管理全部对象”；管理抽屉按名称定位、每页 10 家并可当次移除 | 配置对象集合随移除更新；不回写对比篮 |
| 数据覆盖对象 >9 家 | 每页 9 家，支持名称定位和可信度筛选，显示当前可见 / 总数 | 全量预检与生成条件不变 |
| 商业关键经营指标对象 >6 家 | 每页 6 家，支持名称定位 | 全对象排名、诊断和报告范围不变 |
| 技术或商业诊断对象 >10 家 | 每页 10 家 | 不用页内序号替代任务快照排名，不新增排序入口 |
| 排名对象 >10 家 | N/A | 首屏 Top 5 + Bottom 5；完整排名二级视图可定位、筛查、分页，快照名次不重算 |
| 技术维度未登记 | 可继续 DEMO 配置 | 雷达明确 DEMO；FULL 不生成官方维度雷达，关联 Q014 |
| 无连续年度营收 | N/A | “营收趋势”页签显示数据不足，不绘制趋势线 |
| Bid 指标未登记 | 显示对应 GAP，不允许冒充正式 metric | 结果保留位置并说明不可用原因，不以相近指标替代 |
| Q014 临时默认 | 显示“待甲方确认” | 结果与报告持续披露临时口径，不呈现为已冻结标准 |
| K-O7 未闭合 | 市场份额、品牌声量、客户集中度不可用 | 不进入正式评分、图表或报告；显示采购授权与合规状态 |
| 低可信 | 强警示，可确认继续 | 结论、图表和报告持续标记 |
| 不可生成 | <50% 或关键指标全缺，说明恢复条件 | 不产生正式历史 |
| 生成中 | 进入独立过程页，显示六阶段、当前阶段、已完成阶段和已用时间，可离开且不取消任务 | 最近评估和个人中心出现同一处理中任务 |
| 生成失败 | 显示阶段和错误编号 | 可重试 / 按此配置新建评估 |
| 无权限 | 保留控件位置并说明原因 | 敏感值不渲染，报告下载受限 |
| 报告已存在 | N/A | 复用处理中或有效报告 |
| 日额度可用 | 权益体验预检通过，继续配置或创建；不提前扣减 | 创建接口再次校验并原子扣减 |
| 日额度超限 | 打开 `F-EVAL-09`，保留全部配置 | 不创建任务；联系开通或等待 `reset_at` |
| 权益服务异常 / 配置无效 | 生成动作失败关闭，显示“暂时无法校验权益，请稍后重试” | 保留配置并重试；不临时放行 |
| 平台故障 / 算法系统错误 / 排队撤回 | 任务保留真实终态 | 服务端按原扣减流水幂等返还并提供审计反馈 |

## 8. 中屏布局与禁止项

- 仅 medium；不输出 small 响应式规则，也不以缩放模拟小屏。
- 内容区采用纵向节奏：对象 → 模板 → 指标 / 权重 → 数据预检 → 动作；长指标表在区块内合理滚动或分页。
- 结果诊断表的带单位长指标表头保持单行；通过列宽和表格横向宽度承载，不拆分指标名称与单位。
- 一级导航横向排列四个 Tab：前三项承担业务模式切换，第四项“最近评估”承担历史视图入口；不代表整页横向布局。
- 模式切换不使用独立卡片背景；配置视图不重复展示全局对比篮交接条，共享对象区只渲染一次；结果视图使用独立的紧凑任务对象摘要。
- 不使用滑杆配权、不自动归一化、不把缺失值补 0、不显示无数据空图表。
- 不在三家及以上使用多边形叠加雷达，不在商业力模式创造无需求来源的雷达维度。
- 不用第一个已选指标代替综合得分排序；技术与商业诊断虽覆盖全对象，但不得显示排名序号、提供排序入口或形成第二套排行结论。
- 不在结果摘要平铺 6–50 家对象，不在首屏无限展开超过 10 家的排名，不用分页后局部序号替代任务快照名次。
- 不把营收与专利放在同一商业力图表，不在无连续年度数据时生成营收趋势。
- 不在配置页、总览或对比篮提供报告导出。
- 不在评估页提供企业搜索、固定企业候选池或对象新增；允许移除本次对象且不回写对比篮，补充对象返回对比篮完成。
- 不伪造生成百分比，不在业务模式泄露指标内部元数据，不复制最近评估与个人中心任务，不生成不存在的数据批次值。
- 不在页头重复放置“最近评估”入口，不把第四个导航 Tab 解释为第四种业务评估模式。
- 不以研发投入强度替代研发人员占比，不以专利授权量替代专利引用，不删除客户集中度、品牌声量或组织能力后宣称 Bid 已覆盖。
- 不把权限 persona 当作 `entitlement_tier`，不由前端本地扣减、返还或计算自然日窗口。
- 不把评估发起额度与报告导出额度合并，不展示虚假在线支付路径。

## 9. Wireframe 自检

- [x] 配置、生成过程、结果、历史、个人中心任务、报告、指标说明、日权益弹窗和评审追溯 Frame 齐全。
- [x] 13 项指标均落到字段表，并区分正式来源、待闭合和无来源。
- [x] 默认、加载、空、错误、无权、缺失、低可信和失败状态齐全。
- [x] 五类角色与 L2 / L3 / L4 操作边界可被页面行为验证。
- [x] 对比篮对象自动带入与返回恢复有明确入口和提示。
- [x] 12 个 Bid 子要求均有页面落位或显式 GAP；当前仅 6/12 完成定义闭合。
- [x] SRS 第 6 章的待确认提示、中英文名称预留和 K-O7 外部数据合规约束已落位。
- [x] 最近评估已作为第四个导航 Tab 归位，历史选中态与返回配置路径明确，页头无重复入口。
- [x] 多对象结果的紧凑摘要、全部对象抽屉、Top 5 + Bottom 5、完整排名二级视图和焦点选择均有字段、状态与禁止项。
- [x] 配置对象、数据覆盖、商业经营指标、技术与商业诊断均定义了完整对象范围和分页边界，分页不裁剪任务。
- [x] Top 5 / Bottom 5 颜色与类别间隔、查看全部对象按钮布局及三段评审说明均有可测试合同。
- [x] 日权益预检、最终校验、简单超限弹窗、服务异常和返还反馈均有字段、状态与禁止项。
- [x] 日权益 Frame 明确为待批准增强，未伪造 Bid 锚点或正式 `approved_scope_change`。

## 10. 机器可检评审挂载契约

```yaml
review_trace_contract:
  version: 1.5
  review_mode: visible
  business_mode: absent
  original_requirement_sources:
    - bid-reference/科技信息展示系统和科技专题服务系统.md#1.1.1.2.4.2.3.3
    - bid-reference/科技信息展示系统和科技专题服务系统.md#1.1.1.2.4.2.3.4
    - bid-reference/科技信息展示系统和科技专题服务系统.md#1.1.1.2.4.2.3.10
    - bid-reference/科技专题服务算法库.md#1.1.1.1.1.1.1.5.1
    - bid-reference/科技专题服务算法库.md#1.1.1.1.1.1.1.5.5
    - bid-reference/科技专题服务算法库.md#1.1.1.1.1.1.1.5.6
  frames:
    - frame_id: F-EVAL-01
      review_mounts:
        - { mount_id: ENT-EVAL-F01-CONFIG-TITLE, host_label: 当前模式配置标题, marker_type: requirement_trace, source_relation: product_interpretation, trace_refs: [BID-E23-01, BID-E24-01, BID-E30-01], required_payload: [source_location, source_summary, current_placement, source_relation], review_mode: present, business_mode: absent }
        - { mount_id: ENT-EVAL-F01-INDUSTRY-PREVIEW-NOTE, host_label: 评价行业配置说明, marker_type: review_copy, source_relation: product_interpretation, trace_refs: [BID-E24-02, GAP-INTERACTION-BID-01, Q014], required_payload: [pending_reason, temporary_treatment, closure_condition, source_relation], review_mode: present, business_mode: absent }
        - { mount_id: ENT-EVAL-F01-QUALITY-TITLE, host_label: 数据覆盖与可信度标题, marker_type: requirement_trace, source_relation: product_interpretation, trace_refs: [US-ENT-EVAL-QUALITY], required_payload: [source_location, source_summary, current_placement, source_relation], review_mode: present, business_mode: absent }
    - frame_id: F-EVAL-02
      review_mounts:
        - { mount_id: ENT-EVAL-F02-RESULT-TITLE, host_label: 评估结果标题, marker_type: requirement_trace, source_relation: product_interpretation, trace_refs: [BID-E23-03, BID-E24-03, BID-E30-03], required_payload: [source_location, source_summary, current_placement, source_relation], review_mode: present, business_mode: absent }
        - { mount_id: ENT-EVAL-F02-OBJECT-SNAPSHOT-NOTE, host_label: 完整对象抽屉快照说明, marker_type: review_copy, source_relation: product_interpretation, trace_refs: [US-ENT-EVAL-OBJ], required_payload: [snapshot_scope, read_only_rule, filter_effect], review_mode: present, business_mode: absent }
        - { mount_id: ENT-EVAL-F02-RANKING-DISCLOSURE-NOTE, host_label: 排名摘要默认范围说明, marker_type: review_copy, source_relation: product_interpretation, trace_refs: [US-ENT-EVAL-RESULT], required_payload: [default_visible_scope, ranking_basis], review_mode: present, business_mode: absent }
        - { mount_id: ENT-EVAL-F02-RANKING-SNAPSHOT-NOTE, host_label: 完整排名抽屉快照说明, marker_type: review_copy, source_relation: product_interpretation, trace_refs: [US-ENT-EVAL-RESULT], required_payload: [snapshot_rank_rule, filter_effect], review_mode: present, business_mode: absent }
        - { mount_id: ENT-EVAL-F02-TECH-RADAR-TITLE, host_label: 技术力多维雷达标题, marker_type: requirement_trace, source_relation: direct_requirement, trace_refs: [BID-E23-03, BID-E23-04], required_payload: [source_location, source_summary, current_placement, source_relation], review_mode: present, business_mode: absent }
        - { mount_id: ENT-EVAL-F02-TECH-RANKING-TITLE, host_label: 技术力排名标题, marker_type: requirement_trace, source_relation: direct_requirement, trace_refs: [BID-E23-03], required_payload: [source_location, source_summary, current_placement, source_relation], review_mode: present, business_mode: absent }
        - { mount_id: ENT-EVAL-F02-TECH-DIAGNOSIS-TITLE, host_label: 技术指标与差距诊断标题, marker_type: requirement_trace, source_relation: product_interpretation, trace_refs: [BID-E23-02, BID-E23-03, BID-E23-04], required_payload: [source_location, source_summary, current_placement, source_relation], review_mode: present, business_mode: absent }
        - { mount_id: ENT-EVAL-F02-BIZ-METRICS-TITLE, host_label: 商业指标对比标题, marker_type: requirement_trace, source_relation: product_interpretation, trace_refs: [BID-E24-01, BID-E24-02, BID-E24-04], required_payload: [source_location, source_summary, current_placement, source_relation], review_mode: present, business_mode: absent }
        - { mount_id: ENT-EVAL-F02-BIZ-RANKING-TITLE, host_label: 商业力排名标题, marker_type: requirement_trace, source_relation: direct_requirement, trace_refs: [BID-E24-03], required_payload: [source_location, source_summary, current_placement, source_relation], review_mode: present, business_mode: absent }
        - { mount_id: ENT-EVAL-F02-BIZ-DIAGNOSIS-TITLE, host_label: 商业诊断标题, marker_type: requirement_trace, source_relation: product_interpretation, trace_refs: [BID-E24-03, BID-E24-04], required_payload: [source_location, source_summary, current_placement, source_relation], review_mode: present, business_mode: absent }
        - { mount_id: ENT-EVAL-F02-COMP-RADAR-TITLE, host_label: 综合竞争力雷达标题, marker_type: requirement_trace, source_relation: direct_requirement, trace_refs: [BID-E30-03], required_payload: [source_location, source_summary, current_placement, source_relation], review_mode: present, business_mode: absent }
        - { mount_id: ENT-EVAL-F02-COMP-RANKING-TITLE, host_label: 综合竞争力排名标题, marker_type: requirement_trace, source_relation: direct_requirement, trace_refs: [BID-E30-03, BID-E30-04], required_payload: [source_location, source_summary, current_placement, source_relation], review_mode: present, business_mode: absent }
        - { mount_id: ENT-EVAL-F02-COMP-DIAGNOSIS-TITLE, host_label: 综合竞争力与差距诊断标题, marker_type: requirement_trace, source_relation: product_interpretation, trace_refs: [BID-E30-03, BID-E30-04], required_payload: [source_location, source_summary, current_placement, source_relation], review_mode: present, business_mode: absent }
        - { mount_id: ENT-EVAL-F02-REPORT-TITLE, host_label: 评估报告标题, marker_type: requirement_trace, source_relation: product_interpretation, trace_refs: [US-ENT-EVAL-REPORT], required_payload: [source_location, source_summary, current_placement, source_relation], review_mode: present, business_mode: absent }
    - frame_id: F-EVAL-03
      review_mounts: []
    - frame_id: F-EVAL-04
      review_mounts:
        - { mount_id: ENT-EVAL-F04-REPORT-TITLE, host_label: 报告任务标题, marker_type: requirement_trace, source_relation: product_interpretation, trace_refs: [US-ENT-EVAL-REPORT], required_payload: [source_location, source_summary, current_placement, source_relation], review_mode: present, business_mode: absent }
    - frame_id: F-EVAL-05
      review_mounts:
        - { mount_id: ENT-EVAL-F05-PAGE-TITLE, host_label: 企业评估评审标题, marker_type: requirement_trace, source_relation: direct_requirement, trace_refs: [REQ-ENT-003, REQ-ENT-004, REQ-ENT-010], required_payload: [source_location, source_summary, current_placement, source_relation], review_mode: present, business_mode: absent }
    - frame_id: F-EVAL-06
      review_mounts:
        - { mount_id: ENT-EVAL-F06-PROCESS-TITLE, host_label: 生成过程标题, marker_type: requirement_trace, source_relation: product_interpretation, trace_refs: [US-ENT-EVAL-RESULT], required_payload: [source_location, source_summary, current_placement, source_relation], review_mode: present, business_mode: absent }
    - frame_id: F-EVAL-07
      review_mounts:
        - { mount_id: ENT-EVAL-F07-METRIC-SPEC, host_label: 指标说明内部元数据, marker_type: metric_spec, source_relation: product_interpretation, trace_refs: [Q014, K-O7], required_payload: [metric_id, formula, source_system, availability], review_mode: present, business_mode: absent }
    - frame_id: F-EVAL-08
      review_mounts: []
    - frame_id: F-EVAL-09
      review_mounts:
        - { mount_id: ENT-EVAL-F09-QUOTA-TITLE, host_label: 日额度超限弹窗标题, marker_type: requirement_trace, source_relation: product_enhancement, trace_refs: [US-ENT-EVAL-ENTITLEMENT, PROPOSED-SCOPE-ENT-DAILY-QUOTA-20260723], required_payload: [source_location, source_summary, current_placement, source_relation, approval_status], review_mode: present, business_mode: absent }
  prohibited_mount_positions: [普通按钮, 表格行, 指标业务值, 分页器]
  business_facing_pending_note: Q014临时默认值的待甲方确认提示属于业务状态，不是内部评审挂载，不受business_mode_absent约束。
  business_facing_simulation_note: 行业配置模拟预览及非正式行业评价标准说明属于业务所需免责声明；不得包含Q、GAP、内部Owner或闭环计划。
  entitlement_business_fields: 评估类别已用总额重置时间和联系开通属于业务反馈；business_mode_absent仅约束追溯节点，不得隐藏业务字段。
```
