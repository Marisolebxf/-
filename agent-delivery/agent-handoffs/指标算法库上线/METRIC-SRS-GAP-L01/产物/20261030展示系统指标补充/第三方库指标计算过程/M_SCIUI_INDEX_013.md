# 指标权重展示（M_SCIUI_INDEX_013）

> **类型**：无业务逻辑数值类（配置/说明类读数）｜ **域**：科技发展态势·科技指数·指标展示＞指标权重展示｜ **UI 挂载**：科技指数页 → 指标展示 Tab →「查看指标权重展示」按钮弹窗（方法/赋权依据/一级权重/说明）
> **数据支持度**：**部分支持**｜ **公式定义人**：仿王惠（推测定义，非招标原文闭合口径）｜ **口径归属**：**需求明列叶**（SRS 科技指数.md seq 163 / excel_row 166）
> **复现脚本**：`code/M_SCIUI_INDEX_013.py`｜ **产物**：`code/M_SCIUI_INDEX_013_out.json`
> **四判定摘要**：直接结构 = 否（三源无「科技指数三级树」权重配置面）；直接数据 = 否；依赖结构 = 部分（久新 power/capability 两表权重列在案但体系不同构；dev `index_weight` 属载体/城市指数配置）；依赖数据 = 部分（power 权重全表单组合 0.35/0.30/0.25/0.10 可查，但非本指标体系的权重）
> **数据源口径**：三源评估——开发库 `gkxlumenx_*` + 三方库 `gkx`（183.240.141.251:3318 只读）+ 久新库 `jiuxin_warehouse`（47.93.119.170:29030 只读）。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** 本件是 Lane 3 唯一的**需求明列叶**（SRS seq 163 明文「清晰展示各指标在评价体系中的权重分配，用户可查看权重设置的方法和依据」），但三源均无「科技指数三级指标树」粒度的权重配置面：UI mockData 的三级树 41 权重（一级 0.40/0.30/0.20/0.10）+ AHP×德尔菲方法叙事均为演示值；三源仅有的权重承载各有所属——久新 `ads_institution_technology_power` 四权重列（全表单组合 0.35/0.30/0.25/0.10，加权合成校验 abs_diff=0.0）与 `ads_talent_industry_capability_simulation` 两权重列（0.75/0.25，但 99.5% 行 is_synthetic=1）是**别的体系**的权重；dev `gkxlumenx_cfg.index_weight` 2 行是载体/城市指数的 AHP×熵权配置（版本号 w_v1.0-demo）。权重数据「存在但非本体系」是本件判部分支持的语义根据；升档依赖体系级赋权立项（B10 触发器写死）。

### 批次通用纪律摘要（S3-02 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键；加权合成校验落产物 |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 本件无比值派生；合成校验同表同列 |
| B4 | 负结论带探针 | 三源权重面探针逐一留证（§3.3） |
| B5 | 确定性 | 权重组合 GROUP BY 全枚举排序输出 |
| B6 | 闸门自身被闸 | 本批不自跑闸门 |
| B7 | 产物只由脚本产出 | 改脚本→重跑 |
| B8 | 回执不复收 | 派单方硬复验 |
| B9 | 单位/日期陷阱 | 权重 decimal(5,4)；effective_date 字符串化 |
| B10 | 口径裁定保守交付 | 双口径（借体系权重/立项赋权）+ 触发器（§1.6） |
| B11 | 多本账互推 | dev 2 行配置与 E2/E4 探针对账零漂移 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 权重列存在吗？ | 存在（两表三组） | `jiuxin_power_weight_combinations` / `jiuxin_capability_weight_combinations`（facts） |
| 是本体系的权重吗？ | 不是 | 三级树粒度三源无承载（absence_probe） |
| 合成可校验吗？ | 可（借体系） | `jiuxin_power_weighted_sum_check_top1.abs_diff=0.0`（facts） |

## 摘要

「指标权重展示」是需求明列叶（SRS seq 163）：弹窗展示权重设置方法（UI 叙事为 AHP 结合德尔菲）、赋权依据与一级权重。数据侧判定：三源无「科技指数三级指标树」粒度权重面——久新两表权重列（power 四列 0.35/0.30/0.25/0.10 单组合 64,698 行；capability 两列 0.75/0.25 但 99.5% 合成行）分属机构科技实力/人才产业能力两个别体系，dev `index_weight` 2 行属载体/城市指数（AHP×熵权配置真实在案但体系不同）；UI 三级树 41 权重为 mock。判**部分支持**：权重「存在但非本体系」+ 三级树粒度结构缺失双因；本件交付三项可用中间结果——久新 power 权重的加权合成校验（abs_diff=0.0，证明权重-得分-总分链路自洽可复算）、dev 双指数 AHP×熵权配置全案（方法可平移）、三级树权重清单与 mock 结构对照。

- 需求判定：**需求明列叶**（seq 163），功能行为有定义、权重值与赋权流程无库内承载。
- 复现状态：脚本已跑通；权重组合/合成校验/dev 配置三组读数落产物。
- 档位结论：**部分支持**（体系级权重缺失是结构级缺口）。
- 关键事实：UI mock 权重（0.40/0.30/0.20/0.10）与久新 power 权重（0.35/0.30/0.25/0.10）数值相近但体系不同——不得混用。
- 升档路径：体系赋权立项（AHP+德尔菲流程落库）→ 升完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/科技指数/**指标展示**/指标权重展示（1.1.1.1.4.2.6 分支；SRS seq 163、excel_row 166——**需求明列叶**）。UI 挂载点 `pages/tech-index/index.jsx:224-269`：指标展示 Tab 顶部「用户可查看指标权重展示与赋权依据」提示条 + 「查看指标权重展示」按钮（`:228`）打开 Modal（`:241` `title="指标权重展示"`）。弹窗四段结构：**设置方法**（`indicatorWeightSetting.method`=「层次分析法（AHP）结合德尔菲专家赋权」+ methodDetail 两两比较判断矩阵/特征向量归一/CR<0.1/两轮德尔菲）；**赋权依据**（overallBasis：一级 40/30/20/10，「对标国家创新调查制度及科技评价通行做法」）；**一级权重清单**（三级树 L1 四项 `Math.round(weight*100)%`）；**说明**（`note`：「演示口径（Mock）。正式环境以指标委员会赋权纪要为准」——前端作者自证 mock 待回填）。

弹窗不是静态说明页：左侧指标树的每个节点都标注同级权重（`:224`「左侧树节点已标注同级权重」），`indicatorWeightBasisById`（mockData `:362-397`）为 41 个树节点逐个写了赋权依据文案——「权重展示」的完整语义是**三级树全节点权重+依据**的可查体系，这个粒度是判档的关键标尺。

### 1.2 为什么需要本指标

权重是综合评价的「立法文件」：榜单名次由权重结构决定，用户质疑「为什么 A 排在 B 前」时，唯一站得住的答案是权重及其依据可查。SRS 把「增强排名的透明度和可信度」写成排行榜族的验收语言（seq 173 排名详情查看），权重展示就是这套透明机制的配置面——它把评价体系的价值观（创新 40% > 保障 10%）显性化，供用户校验与甲方修订。

### 1.3 需求文档是否给出定义方法

**需求文档给出了功能行为但没给权重值与赋权方法。** seq 163 明文「清晰展示各指标在评价体系中的权重分配，用户可查看权重设置的方法和依据，了解不同指标在综合评价中的相对重要性」——这是对「展示什么」的定义（权重分配+方法+依据）；但「权重是多少」「方法是什么」（AHP？熵权？德尔菲？）三份需求真源均无定义。UI 的 AHP×德尔菲叙事是前端作者的演示实现。检索记录见附录 A。

### 1.4 类似指标权威方法可行性分析概要

赋权方法谱系：主观赋权以 **AHP 层次分析法**为国际经典（Saaty 1977，R1——两两比较矩阵主特征向量求归一权重、CR<0.1 一致性检验，UI 叙事即此法）；客观赋权以熵权法/CRITIC 为代表（数据驱动，dev index_weight 的「AHP×熵权」即主客观组合式）；德尔菲法（专家多轮收敛）作为 AHP 判断矩阵的输入流程（R1 体系内）。中国官方范式：国家创新调查制度（R2）的各级指标体系即专家赋权+制度发布。方法族对照：

| 方法族 | 代表 | 数据要求 | 与本库匹配 |
|---|---|---|---|
| AHP+德尔菲（UI 叙事） | Saaty 1977（R1） | 专家两两比较 | **流程型无库内承载**（需立项） |
| AHP×熵权组合（dev 现役） | 载体/城市指数 | 判断矩阵+分布数据 | **有配置（2 行，别体系）** |
| 固定权重落表（久新现役） | power/capability 表 | 权重列+分项分 | **有列（两组，别体系）** |

完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/tech-index/index.jsx:241` — `<Modal title="指标权重展示">`；`:228` 触发按钮；`:224` 树节点权重标注提示。
- mockData：`repos/demo-ui-science/src/pages/tech-index/mockData.js:347-360` — `indicatorWeightSetting`（method/methodDetail/overallBasis/note 四段）；`:362-397` — `indicatorWeightBasisById` 41 节点赋权依据；`:9-335` — 三级树 weight 字段（一级 0.40/0.30/0.20/0.10）。
- SRS：`…/科技发展态势/科技指数.md` seq 163（excel_row 166），原文见附录 A。

### 1.6 推测原意与推测定义

**推测定义**：对科技指数三级指标树 $T$ 的每个非叶节点 $v$，展示其子节点归一权重向量 $w_v$（同级和=100%）+ 方法标签（赋权流程名）+ 逐节点依据文案。

- 口径 A（借体系权重）：以久新 power 四权重（0.35/0.30/0.25/0.10，论文/被引/人才/主题）作「一级权重展示」替代供数——现成可查（全表单组合）、合成可校验（abs_diff=0.0），但体系语义偏移须显式标注「机构科技实力权重，非科技指数权重」；
- **口径 B（建议口径：体系赋权立项）**：为科技指数三级树跑 AHP+德尔菲流程（UI 叙事的正式版），判断矩阵→特征向量→CR 检验→权重落配置表——工程量=专家流程+一次配置面建设。

**降档/升档触发器（B10 模板）**：口径 A 被接受 → 升**完全转换支持**（借体系权重+标注）；口径 B 立项落库 → 升**完全转换支持**（本体系闭合）；若要求权重「历史版本可追溯」（mockData `indicatorVersionHistory` 有版本史形态）→ 三源均无权重版本表，需建表（版本维度为增量工程）。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/科技指数.md` |
| 所属四级功能 | 科技指数·指标展示（seq 159–164） |
| 本件叶 | **指标权重展示（seq 163，excel_row 166）——需求明列** |
| 同面板相邻叶 | 指标意义解读（seq 162）/ 专家H指数排行可视化（seq 164） |
| 联动件 | M_SCIUI_INDEX_001 企业榜（口径 B 权重的前置）/ M_SCIUI_INDEX_003 全部得分汇总（权重消费方） |
| 本批同 Lane | P7 族（同页仿真语境）、X_030、INDEX_001 |

权重件在 INDEX 族的枢纽地位：001（榜单）与 003（得分汇总）的分数都是「权重×分项」的产出，权重面不闭合则下游件的口径悬空——本件是 Lane 3 内两个「完全转换支持」件（001）的语义上游，这也是它必须按 B10 双口径保守交付的原因：它的口径选择会向下传导。

## 二、计算过程

### 2.1 装载与权重面盘点

pymysql 直连久新只读库。三源权重承载盘点（本件核心探针）：①久新 `ads_institution_technology_power` 四权重列——`GROUP BY` 全枚举实测**全表单组合** paper 0.3500/citation 0.3000/talent 0.2500/topic 0.1000（64,698 行无例外，facts `jiuxin_power_weight_combinations`）；②久新 `ads_talent_industry_capability_simulation` 两权重列——activity 0.7500/commercial_value 0.2500 单组合 397,964 行（facts `jiuxin_capability_weight_combinations`）；③dev `gkxlumenx_cfg.index_weight` 2 行——载体/城市双指数 AHP×熵权配置（facts `dev_index_weight_configs`）。

### 2.2 加权合成校验（口径 A 的可用性证明）

取 power 榜首机构：四分项分×四权重重算 $\sum w_i s_i$ 与存储总分对账——**abs_diff=0.0**（facts `jiuxin_power_weighted_sum_check_top1`：recomputed 99.999227 = stored_total 99.999227）。这一读数证明久新权重链路（权重列→分项分→总分）自洽可复算，「展示权重」与「展示分数」在同一张表内闭环——口径 A 借用该体系时，用户可以现场验算权重怎么变成名次，这正是 seq 163「透明度」语义的实质满足。

```sql
SELECT paper_score, paper_weight, citation_score, citation_weight,
       talent_score, talent_weight, topic_score, topic_weight,
       technology_power_score
FROM ads_institution_technology_power ORDER BY technology_power_rank LIMIT 1;
-- → Σ(w×s)=99.999227 = technology_power_score（abs_diff=0.0）
```

### 2.3 合成性质披露（capability 表降权处理）

`ads_talent_industry_capability_simulation` 权重列虽在，但其加权对象分全部为合成值：`is_synthetic=1 & value_nature=SYNTHETIC_SIMULATION` 397,964 行（全表；其中确定性哈希回退 DETERMINISTIC_HASH_FALLBACK 396,187 行、技术加权 TECHNOLOGY_WEIGHTED 1,777 行）（facts `jiuxin_capability_value_nature` + `jiuxin_capability_coverage_breakdown`）。该表权重只作「权重面存在性」证据，不作数值承载——skill P4.1b「互认不等于独立验证」纪律的同族处理：合成面的一致性不构成证据。

### 2.4 dev 配置面细读（方法可平移性）

`gkxlumenx_cfg.index_weight` 2 行：载体创新能力指数（ahp 先验 output 0.35/quality 0.30/activity 0.20/performance 0.15 → final 组合权重 0.3518/0.2235/0.1199/0.3048）与城市创新能力指数（output 0.3406/resource 0.2563/environment 0.1990/institution 0.2041），`method='AHP×熵权'`、effective_date=2026-01-01、版本号 `w_v1.0-demo`。披露两点：其一，版本号含 demo 字样但属**配置参数面**（非 skill P4.1 黑名单的 `demo_*` 造数库分值——黑名单针对分值/排名结果，配置行是真实工程配置）；其二，「AHP 先验×熵权客观」的组合赋权法与 UI 叙事（纯 AHP+德尔菲）方法同族可平移——若口径 B 立项，此配置面即为现成的落库模板（表结构/字段语义直接复用）。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_INDEX_013.py`（pymysql 直连久新 + dev + `_gkxdb.py` 走 gkx 探针）；运行 `python3 code/M_SCIUI_INDEX_013.py`。
- 产物：`code/M_SCIUI_INDEX_013_out.json`。正文数字对应键：`jiuxin_power_weight_combinations`（§2.1）、`jiuxin_power_weighted_sum_check_top1`（§2.2）、`jiuxin_capability_weight_combinations`（§2.1）、`jiuxin_capability_value_nature`（§2.3）、`dev_index_weight_configs`（§2.4）、`gkx_dim_index_attribute_rows=867`（§3.3）。
- 结果解读：三组权重读数+合成校验+性质披露齐——「权重存在性」与「体系归属」两个维度同时落地，判档证据闭合。
- 对照需求功能要求的评审：权重展示弹窗回填——**有条件通过**：口径 A 可即期供一级权重+方法标签+可验算链路（标注借体系）；未通过点=三级树全节点粒度无承载、本体系赋权流程未立项（触发器见 §1.6）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 | 数值 |
|---|---|---|---|
| 盘点 | power 权重组合 | `jiuxin_power_weight_combinations` | 单组合 0.35/0.30/0.25/0.10 ×64,698 行 |
| 盘点 | capability 权重组合 | `jiuxin_capability_weight_combinations` | 单组合 0.75/0.25 ×397,964 行 |
| 校验 | 加权合成对账 | `jiuxin_power_weighted_sum_check_top1` | abs_diff=0.0 |
| 性质 | capability 合成占比 | `jiuxin_capability_value_nature` | 397,964/397,964 全合成（细分 396,187+1,777 见 coverage_breakdown） |
| 配置 | dev 双指数配置 | `dev_index_weight_configs` | 2 行（AHP×熵权） |
| 对照 | mock 一级权重 | `ctx_refs.refs` | 40/30/20/10（演示值登记） |
| absence | gkx 权重面 | `absence_probe[0]` | 0 命中 |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 权重结果列（借体系） | jiuxin_warehouse | power 四权重列 / capability 两权重列 | 64,698 / 397,964 | 直查 | 有（别体系） |
| D2 | 权重配置面（方法+依据） | dev | `gkxlumenx_cfg.index_weight` | 2 | 直查 | 有（载体/城市指数） |
| D3 | 科技指数三级树权重 | 三源 | — | — | **不存在** | **缺（主因）** |
| D4 | 权重版本史 | 三源 | — | — | **不存在** | 缺（触发器③） |

`support_judgment="部分支持"`，与文首同档（闸 6）。

### 3.2 D1/D2 的可用边界

久新 power 权重的可用性已由合成校验背书（§2.2）；其边界在体系语义：论文/被引/人才/主题的学术四分族与科技指数三级树（创新/影响/潜力/保障 41 节点）是两棵树——数值结构（四维归一）同构但语义不同族，mock 一级 0.40 与久新 0.35 的相近纯属巧合，产物 notes 已写死「不得混用」。dev 配置面的可用性在方法模板（§2.4）；其边界在指数归属（载体/城市非科技指数）与版本状态（v1.0-demo 未定稿）。

### 3.3 D3/D4 的 absence_probe 全记录

否定性证据三件套：**查了什么**——gkx 280 表 `table_name LIKE '%weight%'`（0 命中）+ `dwd_dim_index_attribute`（867 行指标属性维表）逐列核对（dwd_id/index_code/rid/uid 等 8 列，无权重列）；dev `gkxlumenx_ads.eval_weight`（评估权重表）实测 **0 行**（共享探针 E5）+ `index_weight` 体系核对（仅 carrier/city 两键，无科技指数键）；久新 130 表权重关键词扫描（schema 索引 `_schema_kw.json` 核对：power/capability 两表已在案，无第三张权重表）；**条件**——「科技指数体系」粒度的权重列/配置行/版本表存在性；**命中**——三源均无。四种缺失情形归属：D3/D4 均为「表/行不存在」级——修复=建面（口径 B 落库）或借面（口径 A 标注），非补数据。

## 四、数据缺失情况

### 4.1 科技指数三级树权重缺失（体系级，主因）

41 节点×归一权重的本体系配置在三源无任何承载（§3.3 探针在案）。这不是「数据没同步」而是「体系未建设」：权重值本身不存在于任何源，只能通过赋权流程（AHP 判断矩阵由专家组填写）新生。修复路径即口径 B：专家流程产出判断矩阵→特征向量归一→CR 检验→落 `index_weight` 式配置表（dev 表结构可复用为模板）→UI 三级树回填。工程量集中在流程组织（专家两轮），数据工程量小（一张配置表）。

### 4.2 权重版本史缺失（增量级）

UI mockData `indicatorVersionHistory`（:422-434）有五版本形态（2021-v1→2024-v1 权重变迁+变更说明）——正式版若需「权重修订可追溯」，三源均无权重版本表。修复=配置表加版本键（dev 模板已有 version 字段语义），增量工程；若甲方不要求追溯则不构成缺口。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 口径 A 先行（借体系+标注） | 产品决策 | 本件即期 | 一级权重+可验算链路 |
| 口径 B 赋权立项 | 流程+工程 | 本件+001+003 | AHP×熵权（dev 模板）或纯 AHP+德尔菲（UI 叙事） |
| 版本键增列 | 增量工程 | 本件（如需追溯） | dev 模板复用 |

## 参考文献

1. Saaty, T. L. A scaling method for priorities in hierarchical structures[EB/OL]. Journal of Mathematical Psychology, 1977, 15(3): 234–281. https://doi.org/10.1016/0022-2496(77)90033-5 （2026-11-01 WebSearch 核验可达；AHP 奠基论文：两两比较矩阵主特征向量求归一权重、λmax=n 一致性条件）
2. 科技部、国家统计局联合印发《国家创新调查制度实施办法》[EB/OL]. 中华人民共和国科学技术部. https://www.most.gov.cn/ztzl/qgkjcxdhzkyzn/gcls/kjb/201705/t20170525_132970.html （2026-11-01 WebSearch 核验可达；官方指标体系专家赋权+制度发布的范式）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技发展态势/科技指数.md》seq 163（excel_row 166）——**需求明列叶**：

> ### 指标权重展示 · 序号 163
> - path: 智能服务集群/科技信息展示系统/科技发展态势/科技指数/指标展示/指标权重展示
>
> #### 需规功能描述
> 清晰展示各指标在评价体系中的权重分配，用户可查看权重设置的方法和依据，了解不同指标在综合评价中的相对重要性。

UI 弹窗四段（method/methodDetail/overallBasis/note）与 41 节点赋权依据为前端演示实现（mockData 自证「演示口径（Mock）。正式环境以指标委员会赋权纪要为准」）。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 指标权重展示 | 科技指数.md | **1（seq 163，需求明列）** |
| 指标权重展示 | 主需求文档 | 0 |
| 权重设置的方法和依据 | 科技指数.md | 1（seq 163 功能描述内） |
| 赋权 / AHP / 层次分析法 | 三份需求真源 | 0（方法名未出现） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_INDEX_013_out.json`（2026-11-01 实跑）。
- 共享探针：`_probe_lane3_s302_out.json`（B6/B8 权重组）、`_probe_lane3_s302_r2_out.json`（B3r/E2/E4/E5 dev 配置与空表）、`_probe_lane3_s302_r3_out.json`（G4 版本分布）。
- 久新 schema 索引：`20261026_久新指标 gap 调研/久新数据库调研/_work/_schema_kw.json`（权重表族核对）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_INDEX_013 | 文首 |
| `ui_evidence` | 证据 | 3 条组件：行号 | §1.5 |
| `requirement_trace.named_in_srs` | 事实 | **true**（seq 163/excel_row 166） | §1.1/附录 A |
| `facts.jiuxin_power_weight_combinations` | 权重 | 单组合×64,698 行 | §2.1 |
| `facts.jiuxin_power_contribution_samples` | 样本 | 3 机构贡献结构 | §2.2 |
| `facts.jiuxin_power_weighted_sum_check_top1` | 校验 | abs_diff=0.0 | §2.2 |
| `facts.jiuxin_capability_weight_combinations` | 权重 | 0.75/0.25×397,964 | §2.1 |
| `facts.jiuxin_capability_value_nature` | 性质 | 397,964 全合成 | §2.3 |
| `facts.jiuxin_capability_coverage_breakdown` | 细分 | 396,187 回退/1,777 加权 | §2.3 |
| `facts.dev_index_weight_rows` | 计数 | 2 | §2.4 |
| `facts.dev_index_weight_configs` | 配置 | 双指数 AHP×熵权全案 | §2.4 |
| `facts.gkx_dim_index_attribute_rows` / `_columns` | 对照 | 867 行/无权重列 | §3.3 |
| `absence_probe` | 探针 | 三源 3 条 | §3.3 |
| `support_judgment` | 判档 | 部分支持 | §〇 |
| `ctx_refs.refs` | 登记 | 40/30/20/10（mock 演示值） | §1.1 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 落库形态 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| AHP+德尔菲 | Saaty（R1）/UI 叙事 | 判断矩阵→配置表 | 无（需立项） | **最高（口径 B）** |
| AHP×熵权组合 | dev 现役 | index_weight 配置行 | 2 行（载体/城市） | 高（模板可平移） |
| 固定权重落表 | 久新现役 | 权重列+分项分 | 两组（别体系） | 中（口径 A） |

### C.2 数据矩阵

| 依赖 | 行数 | 质量 | 缺口 |
|---|---|---|---|
| power 权重列 | 64,698 | 单组合/合成校验 0 差 | 体系=学术四分族 |
| capability 权重列 | 397,964 | 99.5% 合成 | 仅存在性证据 |
| dev index_weight | 2 | AHP×熵权/未定稿 | 键=载体/城市 |
| 科技指数树权重 | 0 | — | **体系未建设** |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 口径 A：借 power 权重+标注+可验算链路 | 无 |
| v2 | 口径 B：AHP 流程→配置表落库→三级树回填 | 专家流程立项 |
| v3 | 版本键+修订史 | 如需追溯 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| mock 权重被当正式口径 | **高** | UI note 自证+产物 notes 写死不得混用 |
| 借体系权重语义误植 | **高** | 弹窗标注「机构科技实力权重」 |
| 合成面权重被引用 | 中 | §2.3 降权处理在案 |

### C.5 总判

**部分支持**：三源权重「存在但非本体系」+三级树粒度结构缺失；口径 A 即期可用（合成校验背书）、口径 B 立项路径明确（dev 模板可平移），双触发器不悬空。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_INDEX_013.py` | 退出码 0，落 `_out.json` |
| 合成校验复算 | Σ(w×s) vs total | abs_diff=0.0 |
| dev 配置对账 | index_weight 行数 | 2（与 E2 零漂移） |
| 空表复核 | eval_weight | 0 行 |
| 判档一致 | MD 文首 vs `support_judgment` | 部分支持 |
