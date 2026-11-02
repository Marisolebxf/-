# 综合力度指数（M_SCIUI_POLCMP_046）

> **类型**：需业务建模类｜ **域**：科技政策跟踪·政策分析评价·政策画像（DS-11）·综合力度指数｜ **UI 挂载**：科技信息展示系统 → 政策跟踪 → 政策分析评价（三画像区）→ 政策画像卡 KPI「综合力度指数 86 分」（`pages/policy-tracking/policyData.js:2178`；metrics 首行「发布密度 128 项/季」见 `:2183`；消费组件 `analysis/PortraitTrio.jsx:40`）
> **数据支持度**：**完全不支持**｜ **公式定义人**：无（export 自认口径需立项调研；父代理裁定 NEW：政策力度组合口径未调查，无候选）｜ **口径归属**：UI 功能拆件（`_phase3_471_export.json`），三份需求真源未出现指标名；语义源=算法库 :1031-1039「政策力度评估模型」（效果/覆盖/成本三维，无权重无算式）
> **复现脚本**：`code/M_SCIUI_POLCMP_046.py`｜ **产物**：`code/M_SCIUI_POLCMP_046_out.json`
> **四判定摘要**：直接结构 = 否（三源无力度评估结果面）；直接数据 = 否；依赖结构 = 部分（dev `policy_intensity_eval` 23 列与算法库三维**逐列同构**——intensity_index/effect_score/coverage_score/cost_score/intensity_level，且含排名/趋势/预测列）；依赖数据 = 否（该表及 3 张邻表全 0 行——模型规划过、从未运行；gkx 33 列无力度量化列，唯一扶持列 policy_support 占位全 'null'）
> **数据源口径**：三源（开发库 live `gkxlumenx_*` 非 demo + 三方库 gkx + 久新 `jiuxin_warehouse`）逐一探针留证；`demo_*` 禁引。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全不支持。** 组合口径未立项（父代理裁定 NEW：政策力度组合口径未调查无候选；export 自认需立项调研）+ 力度结果面三源 0 行。最有信息量的证据在 dev：`policy_intensity_eval` 表 **23 列**与算法库 :1031-1039「政策力度评估模型」**逐列同构**——`intensity_index`（力度指数）+ 三维分 `effect_score`/`coverage_score`/`cost_score`（效果/覆盖/成本，与算法库三类指标一字不差）+ `intensity_level`（力度等级）+ `rank_nationwide`/`rank_province`（排行榜，对应算法库「支持排行榜」）+ `trend_analysis`/`prediction_result`（趋势跟踪/预测）——开发库完整规划过该模型的落位，但**全表 0 行**，模型从未运行；邻表 `policy_support_rank`（intensity_index 列）、`policy_time_analysis`（density_index_series/intensity_trend_series）、`policy_support_assessment`（strategy_guidance/policy_support/funding_support/project_support/implementation_effect 五维分+composite_score）同样全部 0 行——整族评估面「规划过、全空载」。gkx 侧 33 列扫 intensity/strength/force/power/weight/score/index/rank/level 仅命中 `rank`（位次列非力度列），唯一扶持列 `policy_support` 占位三证（20,000/20,000 全 'null'、DISTINCT={'null'}、% 模式 0 命中——与 POLCMP_009 共证零漂移）；文本「力度」3,919 行（19.595%）是政策自述修辞（「加大支持力度」类），非量化承载。久新实测 210 张（探测日）扫 policy/intensity/strength/power：policy 词根命中 4 张全部语义排除（`ads_research_problem_policy_evidence`/`ads_research_problem_policy_yearly_metrics`/`ads_technology_policy_evidence` 是科研问题-政策关联证据与年度计数，`ads_institution_technology_power` 是机构技术实力——均非政策力度评估）；intensity/strength/power 词根 0 命中。

### 批次通用纪律摘要（S3-03 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 3,919/20,000 叙述面占比同表同基 |
| B4 | 负结论带探针 | absence 四件（gkx/dev/jiuxin/doc，§3.3） |
| B5 | 确定性 | 词族表固定；列扫清单固定；表列表 sorted |
| B6 | 闸门自身被闸 | 不自跑闸门，派单方统一 |
| B7 | 产物只由脚本产出 | 改脚本→重跑→同步本 MD |
| B8 | 回执不复收 | 探针 SQL 幂等可复验 |
| B9 | 单位/日期陷阱 | 指数（分）与资助额（万元）量纲分开登记 |
| B10 | 口径裁定保守交付 | NEW 无候选不擅拟权重；mock 86 分不参与结论 |
| B11 | 多本账互推 | policy_support 占位与 009 零漂移；dev 4 表族级旁证一致 |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有力度指数结果面吗？ | 无（dev 同构表 0 行） | §3.3 其二；§3.2 |
| 口径（维度+权重）有裁定吗？ | 无（NEW；算法库只给三维名） | §1.3；裁定登记簿 |
| 输入侧可现在转换出指数吗？ | 不可（资助金额/层级评分无结构化） | §3.1 D3/D4 |

## 摘要

「综合力度指数」是政策分析评价·政策画像卡（DS-11）的 KPI 读数（mock 86 分），是三画像卡三件 KPI 之一（与 038 人才卡、037 企业卡并列）。核心证据是 dev `policy_intensity_eval`：23 列与算法库「政策力度评估模型」效果/覆盖/成本三维**逐列同构**（intensity_index/effect_score/coverage_score/cost_score + 全国/省内排名 + 趋势/预测列）——开发库完整规划过模型落位但全表 0 行，连同 3 张邻表（support_rank/time_analysis/support_assessment 五维分）整族空载，「规划过、从未运行」。gkx 33 列无力度量化列（唯一 rank 是位次列）、policy_support 占位全 'null'（与 009 共证）；「力度」文本 3,919 行（19.6%）是政策修辞非数据；久新 policy 词根 4 张全部语义排除。组合口径本身未立项（裁定 NEW：无候选；算法库只给三维框架无权重无算式）。判**完全不支持**——结构同构但空载 + 口径未裁 + 输入侧（资助金额结构化/政策层级评分）无承载三层缺。

- 需求判定：指标名三份需求真源 0 命中；语义源=算法库 :1031-1039 政策力度评估模型（三维框架，非闭合定义）。
- 复现状态：指数登记键留空（`composite_policy_intensity_index=null`）；叙述面读数落产物。
- 档位结论：**完全不支持**（口径 NEW + 结果面族性 0 行 + 输入维缺）。
- 关键事实：dev 评估面 4 表全 0 行——`policy_intensity_eval`/`policy_support_rank`/`policy_time_analysis`/`policy_support_assessment`，整族「结构在、从未运行」。
- 升档路径：力度模型立项（算法库三维+学术赋权）+ 输入侧结构化（资助金额抽取/层级评分）+ dev 表回填 → 升完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技政策跟踪/**政策分析评价**·政策画像（DS-11 政策/企业/人才三画像）·综合力度指数。UI 容器是 `PortraitTrio.jsx`（三卡+Drawer 详情）：政策画像卡（`policyData.js:2175` 起）KPI 位是「综合力度指数 86 分」（`:2178`，本件），点开 Drawer 后 detail.metrics 四行：发布密度 128 项/季（`:2183`）、平均资助强度 3200 万元、跨部门协同率 68%（`:2185`=053 件）、免申即享占比 24%。组件行为：纯展示 mock，无后端取数。挂载形态说明「综合力度指数」是政策画像的**头部综合分**——mock 作者把 metrics 四行设计为其组成读数（发布密度=量维、资助强度=额维、协同率=组织维、免申即享=兑现维），这一布局是推测组合口径的最强 UI 侧线索（但仍无权重语义）。

### 1.2 为什么需要本指标

政策对比的最终诉求是「哪个政策更值钱/更给力」：单项特征（金额/条款数/层级）都只反映一个切面，需要一个综合分把力度折成可排序的单一读数——画像卡 KPI 位、算法库「排行榜」输出、dev 表的全国/省内排名列，三处设计都指向排序用途。学术上这是政策文本量化的经典议题（政策力度=颁布层级×政策属性等维度加权，R1 熵值法框架；R2/R3 PMC 指数族把力度作为一级变量纳入政策评价）。

### 1.3 需求文档是否给出定义方法

**需求文档未给出闭合定义。**「综合力度指数」指标名在三份需求真源 0 命中；语义源是算法库 :1031-1039「政策力度评估模型」：效果维（政策目标达成度）、覆盖维（受益面）、成本维（财政投入）三类指标+阈值设定+权重赋值与综合加权 → 政策力度指数，支持趋势跟踪与排行榜——**给了维度名但无权重表、无算式、无数据映射**。export 行自认「对某方面能力或状态的量化评价（科技政策库场景）——计算方法需要立项调研后才能确定」；父代理裁定 NEW（政策力度组合口径未调查，无候选）。

### 1.4 类似指标权威方法可行性分析概要

政策力度量化三族先例：①**多维加权系**（R1 分级诊疗研究）：政策措施/目标/反馈/协同/力度（行政级别）/力度（政策属性）6 维熵值法定权，428 份政策算「政策价值」——力度本身是被测维度之一（法律类政策价值均值 3.11 最高、部门协同数增多价值 2.16→3.27 递增）；②**PMC 指数系**（R2 国务院创新政策/R3 分级诊疗英文研究）：政策性质/时效/功能/工具/受体等二级变量 0/1 赋值，一级均值汇总 PMC 得分——纯文本可算但语义是「政策质量」非「力度」；③**算法库三维系**（招标文件）：效果/覆盖/成本加权——结构最贴合 dev 落位但权重未给。三族共同输入要求：政策层级评分、资助金额结构化、（PMC 系）全文编码——库内仅层级可从机关列近似推导（053 件的词表资产可复用），金额与编码面均无。完整版见附录 C。

### 1.5 引用来源

- UI：`repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2178`（KPI 86 分）、`:2183`（发布密度）、`:2185`（协同率，053 件）、`analysis/PortraitTrio.jsx:40`（消费组件）。
- 算法库 :1031-1039（政策力度评估模型三维框架——语义源）。
- 学术方法：R1 福建分级诊疗政策文本量化（熵值法 6 维）；R2 国务院创新政策 PMC 指数模型；R3 分级诊疗 PMC-Index 英文研究。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义（口径未闭合，不擅拟权重）**：$\text{CPI} = f(\text{effect}, \text{coverage}, \text{cost})$——算法库三维框架，f 未定（权重/合成法则/阈值均待立项）；UI 布局暗示的第 4 候选是「量/额/组织/兑现」四维（mock metrics 行），仅登记为候选不采信。**权威参照维度库**（R1 六维含力度、R2/R3 PMC 族）可作立项时的维度菜单。**本件交付**：负结论登记（`composite_policy_intensity_index=null`）+ 三源 absence 留证 + dev 结构同构证据链。**降档/升档触发器**：①力度评估模型立项（三维或其扩展+学术赋权方法定权重）+ 输入侧结构化（资助金额抽取——与 049 窄窗管线共享；层级评分回填——与 053 机关词表共享）+ dev `policy_intensity_eval` 运行回填 → 升**完全转换支持**；②接受 PMC 类纯文本口径 → NLP 量化管线立项（不依赖金额面），单独一条转换路径；③均不做 → 长期完全不支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 挂靠四级功能（export 口径） | 多维政策对比·综合力度指数 |
| UI 实际容器 | `PortraitTrio.jsx` 政策画像卡 KPI 位（DS-11 Wave0 扩展 mock） |
| 语义源叶 | 算法库 :1031-1039 政策力度评估模型（三维框架） |
| 批内姊妹件 | POLCMP_053 跨部门协同率（同一画像卡 metrics 行——mock 设计为 046 的组成读数，R1 证据链还显示部门协同数与政策价值正相关，两件在学术口径上交联）；POLCMP_038 留用意愿指数（三画像卡 KPI 位同族）；POLCMP_049 加计扣除（力度输入侧金额面与 049 制度值面共享抽取管线） |
| 依赖链 | 结果面 ← dev 同构表 0 行；输入面 ← 资助金额（缺）/层级评分（053 词表可派生）/覆盖面（缺）；口径 ← NEW 待立项 |

## 二、计算过程

从缺（完全不支持档：组合口径未立项（NEW）+ 结果面三源 0 行（dev 同构表空载）+ 输入侧金额/覆盖维无结构化承载，无计算过程可展示；「力度」叙述面 3,919 行是政策修辞工作量指示器，非指数输入，量纲不同不入计算）。探针与读数见 §三/§附录 B。

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 力度指数结果面 | dev | `policy_intensity_eval`（23 列） | 0 | 空表 | **缺（结构同构、数据空）** |
| D1' | 排名面 | dev | `policy_support_rank`（intensity_index 列） | 0 | 空表 | 缺（族性空载） |
| D1'' | 趋势面 | dev | `policy_time_analysis`（density/intensity_trend 序列） | 0 | 空表 | 缺（族性空载） |
| D1''' | 综合评估面 | dev | `policy_support_assessment`（五维分+composite） | 0 | 空表 | 缺（族性空载） |
| D2 | 力度结构化列 | gkx | `dwd_policy_base` 33 列扫 | 仅 rank | 无力度列 | **缺（结构级）** |
| D3 | 资助金额维（成本/强度输入） | gkx/dev | 金额结构化列 | 0 | 无承载 | **缺（结构级）** |
| D4 | 层级评分维 | gkx | ministry 派生（053 词表） | 19,989 非空 | 可派生 | 部分（需评分规则立项） |
| D5 | 力度评估面（三源） | jiuxin | policy 词族 4 张 | 语义排除 | **不存在** | **缺（结构级）** |
| D6 | 政策自述叙述面 | gkx | 「力度」文本 | 3,919 | 直查 | 不入计算（修辞非数据） |

`support_judgment="完全不支持"`、产物与文首一致（闸 6）。

### 3.2 dev 评估面整族空载（D1 族——本件核心证据）

四表连环证据：`policy_intensity_eval` 23 列与算法库三维**逐列同构**（intensity_index 总分 + effect/coverage/cost 三维分 + intensity_level 等级 + rank_nationwide/rank_province 双排名 + dimension_report/trend_analysis/prediction_result 报告与趋势预测 + eval_model_version/threshold_config 模型版本与阈值配置）——落位设计完整到模型版本管理层面，说明开发侧曾按算法库规划过完整评估管线；`policy_support_rank`（intensity_index 排名面）、`policy_time_analysis`（density_index_series/intensity_trend_series 时序面）、`policy_support_assessment`（strategy_guidance/policy_support/funding_support/project_support/implementation_effect 五维分 + composite_score）三张邻表同步空载——**整族 0 行**。这是「规划过、从未运行」的族级形态：比单表空载更强的负证据——不是遗漏建表，而是模型从未执行过（与 POLCMP_008 `policy_public_opinion`、053 `dept_distribution` 同属 dev 空载族，但本件是四表连环）。

### 3.3 力度面 absence_probe 全记录

否定性证据四件套：**其一（gkx）**——`dwd_policy_base` 33 列扫 intensity/strength/force/power/weight/score/index/rank/level 词族仅命中 `rank`（位次列非力度列）；唯一扶持列 `policy_support` 占位三证（20,000/20,000 全 'null'、DISTINCT={'null'}、% 模式 0 命中——与 POLCMP_009 探针零漂移共证）。**其二（dev）**——四表族性空载（§3.2）。**其三（jiuxin）**——实测 210 张（探测日）扫 policy/intensity/strength/power：policy 词根命中 4 张逐表语义排除（`ads_research_problem_policy_evidence`/`ads_research_problem_policy_yearly_metrics`/`ads_technology_policy_evidence` 是科研问题-政策关联证据与年度计数，`ads_institution_technology_power` 是机构技术实力面）；intensity/strength/power 词根 0 命中——分析仓无政策力度评估面。**其四（doc）**——指标名三份需求真源 0 命中；算法库 :1031-1039 只给三维框架（无权重无算式）；export 自认需立项调研；父代理裁定 NEW（无候选）。

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| gkx 列扫 | 33 列力度词族仅 rank；policy_support 占位三证（与 009 零漂移） |
| gkx 叙述面 | 「力度」3,919 行（title 层 23 行），占比 19.595% |
| dev 同构表 | policy_intensity_eval 23 列 0 行（三维+双排名+趋势预测列） |
| dev 邻表 | support_rank / time_analysis / support_assessment 全 0 行（族性空载） |
| 久新排除 | 210 表（探测日）policy 词根 4 张语义排除；intensity/strength/power 0 命中 |
| 脚本形态 | 三源串行只读；零 demo_*；产物无耗时键 |

## 四、数据缺失情况

### 4.1 组合口径未立项（口径级，主因）

父代理裁定 NEW：政策力度组合口径未调查、无候选。算法库三维框架（效果/覆盖/成本）不是闭合定义——权重表、合成法则（线性加权？乘积？TOPSIS？）、阈值与等级切分（dev 表 intensity_level 的分档规则）全部缺位。UI 侧唯一线索是 mock 的 KPI+metrics 布局（86 分居首、四读数居次），可登记为「四维候选」但无权重语义。学术方法族（R1 熵值法/R2R3 PMC）可补维度菜单与赋权方法，但立项前任何自拟权重都违反 B10 保守纪律。

### 4.2 结果面族性空载与输入维缺失（数据级+结构级，次因）

结果面：dev 四表 0 行（§3.2）——即便口径今天裁定，也没有可校验的历史评分。输入面三缺：**金额维**（成本/资助强度的核心输入）——政策条款金额无结构化列，gkx 全文含「万元」的表述散在长文本，抽取工程与 049 窄窗管线同型但目标更泛（金额值域宽）；**覆盖维**（受益面）——受益企业规模/行业面无承载；**层级维**——可从 ministry 19,989 非空行派生（053 机关词表资产复用：部委/省厅/市局三级评分），是唯一可低成本闭合的输入维。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 力度评估模型立项 | 口径立项 | 本件（主）+ 政策画像族 | 三维或扩展维+赋权方法（R1 熵值法/R2 PMC 菜单）；dev 表结构可直接承接 |
| 资助金额抽取管线 | 解析工程 | 本件 + 049 + 资助强度类 | 窄窗规则法（049 管线共享），gold 标注集起步 |
| 层级评分回填 | 轻量工程 | 本件 + 053 | 机关词表三级评分，库内原料足量 |
| dev 评估面回填 | 数据工程 | 本件 | 模型运行写入 policy_intensity_eval（结构现成） |
| `policy_support` 列激活 | 数据工程 | 本件 + 009 | 占位列回填（与量化管线联动） |

档位后果：立项+输入侧两维闭合（金额抽取+层级评分）+ 回填 → **完全转换支持**（覆盖维可用受益面文本代理，披露口径）；仅层级维闭合 → 维持不支持（三维缺二）；PMC 纯文本路径 → 另立口径分支评估。推荐：随画像族合并立项——046/053/038 三件共享「组合/主观评价无承载」缺口，层级词表与金额管线是公共资产。

## 参考文献

1. 健康中国背景下分级诊疗政策文本量化分析——以福建省为例[EB/OL]. 福建医科大学学报（哲学社会科学版）. https://fjmuxbskb.fjmu.edu.cn/fjykdxsk/article/abstract/20230602 （R1，2026-11-01 WebSearch 核验可达：428 项政策 6 维熵值法——政策力度（行政级别）/政策力度（政策属性）作为独立维度入模，法律类政策价值均值 3.11 最高、部门协同数增加则政策价值 2.16→3.27 递增——力度=层级×属性的多维加权先例，且与 053 协同维交联）
2. 国务院创新政策量化评价——基于 PMC 指数模型[EB/OL]. 科技进步与对策. https://www.kjjb.org/fileup/HTML/2017-34-17-019.htm （R2，2026-11-01 WebSearch 核验可达：国务院 12 项创新政策 PMC 指数评价——政策性质/时效/功能/工具/受体等变量 0/1 赋值的纯文本量化路径，力度作为隐含一级变量的 PMC 族方法锚）
3. Policy texts and actions: quantitative evaluation of the hierarchical medical system policy in China based on the PMC-Index model[EB/OL]. BMC Public Health. https://bmcpublichealth.biomedcentral.com/articles/10.1186/s12889-025-22358-3 （R3，2026-11-01 WebSearch 核验可达：分级诊疗政策 PMC-Index 量化评价——工具-主体协同理论框架下的政策文本量化国际期刊范式，文本编码可行性参照）

# 附件

## 附录 A 原始需求原文摘录

**三份需求真源均未出现「综合力度指数」。**语义源算法库 :1031-1039（政策力度评估模型）：

> 建立政策力度评估模型，从政策效果、覆盖范围、财政投入（成本）三个维度设定指标……通过阈值设定和权重赋值，综合加权得到政策力度指数，支持政策力度的趋势跟踪和排行榜。

（维度名忠实转述；算法库原文无权重表与算式——非闭合定义。）

export 行口径自认：

> 综合力度指数——对某方面能力或状态的量化评价（科技政策库场景）——计算方法需要立项调研后才能确定。

UI 层 `policyData.js:2178`（政策画像卡 KPI）与 `:2183`（metrics 首行）：

> kpi: { label: '综合力度指数', value: '86 分' }
> { label: '发布密度', value: '128 项/季' }

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 综合力度指数 | 主需求 + SRS 政策族四文件 + 核增 17 叶 | 0 |
| 力度指数 | 三份需求真源 | 0 |
| 政策力度 | 算法库 | 1（:1031-1039 评估模型，语义源） |
| 综合力度指数 | `policyData.js` | 1（:2178 政策画像卡 KPI） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_POLCMP_046_out.json`（2026-11-01 实跑：gkx 33 列力度词族扫 + policy_support 占位三证 + 叙述面 + dev 四表 DESC/COUNT 同构验证 + 久新语义排除）。
- 共享探针：`code/_snapshots/_shared_probe_s3_01_out.json`（政策底表 20,000 行）；policy_support 占位读数与 POLCMP_009 产物零漂移对账。

### B.2 本件产物逐键清单（`code/M_SCIUI_POLCMP_046_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.gkx_policy_col_count` | 计数 | 33 | §〇/§3.3 |
| `facts.gkx_policy_intensity_cols` | 探针 | ['rank']（仅位次列） | §〇/§3.3 |
| `facts.gkx_policy_rows` | 计数 | 20,000 | §3.3 |
| `facts.gkx_policy_support_nonnull` | 计数 | 20,000 | §3.3 占位三证 |
| `facts.gkx_policy_support_distinct_sample` | 形态 | ['null'] | §3.3 |
| `facts.gkx_text_lidu_rows` | 计数 | 3,919 | §〇/§3.4 |
| `facts.gkx_text_lidu_title_rows` | 计数 | 23 | §〇 |
| `facts.dev_policy_intensity_eval_cols` | 结构 | 23 列（三维同构+双排名+趋势预测） | §〇/§3.2 |
| `facts.dev_policy_intensity_eval_rows` | 计数 | 0 | §〇/§3.2 |
| `facts.dev_policy_support_rank_rows` | 计数 | 0（intensity_index 列） | §3.2 |
| `facts.dev_policy_time_analysis_rows` | 计数 | 0（density/intensity_trend 序列） | §3.2 |
| `facts.dev_policy_support_assessment_rows` | 计数 | 0（五维分+composite_score） | §3.2 |
| `facts.jiuxin_table_count` | 计数 | 210（探测日） | §3.3 |
| `facts.jiuxin_policy_intensity_like_tables` | 探针 | 4 张语义排除 | §3.3 |
| `derived[0]` | 派生比 | `lidu_share_pct=19.595`（3,919/20,000） | §〇/§二 从缺注 |
| `derived[1]` | 登记 | `composite_policy_intensity_index=null` | §〇/§2 |
| `absence_probe` | 探针 | 四件（gkx/dev/jiuxin/doc） | §3.3 |
| `support_judgment` | 判档 | 完全不支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 输入要求 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 算法库三维加权 | 效果/覆盖/成本 | 三维评分+权重 | dev 同构表 0 行；金额/覆盖维缺 | **最贴合（口径+落位均在，输入缺）** |
| 熵值法多维 | R1 分级诊疗 6 维 | 维度编码全集 | 层级维可派生，金额/覆盖缺 | 高（赋权方法候选） |
| PMC 指数 | R2/R3 文本 0/1 编码 | 全文编码手册 | 文本在库（20,000 全文），编码工程大 | 中（纯文本路径） |
| AHP+TOPSIS | 学术常用组合 | 专家判断矩阵 | 无专家面 | 低（权重主观源缺） |

### C.2 数据矩阵

| 依赖 | gkx | dev | jiuxin |
|---|---|---|---|
| 指数结果面 | 无列（33 列扫） | 四表 0 行（同构空载） | 0 命中（语义排除） |
| 金额维（成本输入） | 长文本散述，无结构化列 | 无承载 | — |
| 层级维 | ministry 19,989 非空（可派生） | publish_organization 39,989 | — |
| 覆盖维 | 无承载 | 无承载 | — |
| 叙述面 | 3,919 行（修辞） | 同步 | — |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | 负结论登记 + 族性空载证据链 | — |
| v1 | 层级评分维闭合（053 词表复用）+ 金额抽取管线（049 共享） | 两项轻量工程 |
| v2 | 力度模型立项（维度菜单+赋权）+ dev 表回填 | 口径立项 |
| v3 | 排行榜/趋势产品化（rank/trend 列激活） | v2 运行 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 自拟权重违反 B10 | **高** | 立项前只登记维度候选，不产出任何指数值 |
| mock 86 分被当真实评分引用 | 中 | 披露词随行（DS-11 Wave0 演示值） |
| 金额抽取精度不足拖累成本维 | 中 | 窄窗规则+gold 标注集（049 管线经验） |
| 覆盖维长期无源 | 中 | 受益面文本代理（披露口径限制）或外部统计源 |

### C.5 总判

**完全不支持**：口径 NEW（无候选）+ 结果面族性空载（dev 四表 0 行，结构同构是唯一亮点）+ 输入维三维缺二（仅层级可低成本闭合）。但本件是三画像 KPI 三件中修复路径最清晰的一件——dev 落位结构现成、两项输入工程（金额管线/层级词表）均可与 049/053 共享资产，立项后升档最快。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_POLCMP_046.py` | 退出码 0，落 `_out.json` |
| 数据入口 | `_gkxdb.py`（gkx）+ 直连 dev/久新 | demo_* 直接 raise |
| 判档一致 | 文首 vs `support_judgment` | 完全不支持 |
| 负证据探针 | 产物 `absence_probe` 四件 | gkx/dev/jiuxin/doc 各一 |
| 零漂移对账 | policy_support 占位 vs POLCMP_009 产物 | 20,000/'null'/0% 三读数一致 |
| §二形态 | 「从缺」一句（002 纪律） | 无计算过程展示 |
| 幂等重跑 | SQL 全只读、词族/列扫清单固定 | 逐位一致 |
