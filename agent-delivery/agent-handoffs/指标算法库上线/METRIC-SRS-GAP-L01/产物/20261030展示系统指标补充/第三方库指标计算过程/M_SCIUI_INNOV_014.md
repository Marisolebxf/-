# 区域能力评分（综合）（M_SCIUI_INNOV_014）

> **类型**：COMPOSITE（加权综合评分，双口径 A 加权 [25/25/25/15/10] / 口径 B 等权 20%×5 对照）｜ **域**：科技发展态势·全球创新监测·监测对象详情卡（主）+ 湾区创新监测 + 深圳创新监测（三页同构挂载）｜ **UI 挂载**：`globalInnovationMonitor.js:403` + `bayAreaInnovationMonitor.js:386` + `shenzhenInnovationMonitor.js:461`（三页 metricCards 首张『能力评分』）
> **数据支持度**：**部分支持**｜ **公式定义人**：仿王惠（推测定义，非招标原文闭合口径——权重假设须甲方裁定）｜ **口径归属**：UI 推导叶（`cfg_metric` 无条目；指标名三份说明书 0 命中）
> **复现脚本**：`code/M_SCIUI_INNOV_014.py`｜ **产物**：`code/M_SCIUI_INNOV_014_out.json`
> **四判定摘要**：直接结构 = 否（久新 ads_geo_yearly_index schema 在但 0 行——1.6.0 预留、公式未审定；ads_technology_region_assessment 2,708,162 行是节点内百分位陷阱面）；直接数据 = 否；依赖结构 = 是（ads_geo_yearly_metrics 五维列与 region_assessment 结构均在）；依赖数据 = 部分（五维可加权出分但权重无甲方裁定；region_assessment 分值城市间不可比）
> **数据源口径**：本件支持度按「开发库 gkxlumenx_*（禁 demo_*）+ 三方库 gkx（183.240.141.251:3318 只读）+ 久新 jiuxin（47.93.119.170:29030 只读）」三源评估（20261101 三源铁律）。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** 这是全批「评分类」的**陷阱面典型件**。乍看承载丰富——久新 `ads_technology_region_assessment` 2,708,162 行、389 个地名、带 `regional_potential_score`（0-100）+ `regional_rank`——但实测分值是**节点内百分位制**：每个技术节点内所有地区按分排序后映射 0-100（北京市 v2 模型 10,959 行 AVG=48.8899，10,928 行满分 100.000000 散布于小城镇与北京同分），**城市间不可比**——把「北京 48.89 分」当城市评分回填是全批最危险的误用（正确读法：北京在某技术节点上位列前 1.1%）。真正的区域评分预留表 `ads_geo_yearly_index`（schema：index_code/raw_value/normalized_value）**0 行**——1.6.0 版预留、公式未审定（`metric_definition_version` 列证）。三源其余侧：gkx score/assess/power 0 表（lane1 probe2 官方探针）；dev `gkxlumenx_ads` 3 张 score 表（enterprise_score 120 行企业粒度、industry_chain_region_scorecard 0 行、svc_tech_power_score 0 行）——非区域承载。**转换路径在但有两断点**：①五维原料齐（与 013 件同面板）可加权出分，但**权重无甲方裁定**（SRS seq 73 明言『用户可查看指数计算方法和权重设置』——权重是产品决策非数据决策）；②评分是「结构+数据+公式」三件套，公式侧三源均无审定版本。实测口径 A（仿 UI 创新力指数模板扩五维，权重 [25,25,25,15,10]）：China 90.7862 / United States 42.8663 / United Kingdom 12.8204——Top3 在等权对照（口径 B）下排名不变（敏感性通过）。判**部分支持**。

### 批次通用纪律摘要（批 S3-01 共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 评分归一同表同年 2025 截面；Top1 差值分子分母同榜 |
| B4 | 负结论带探针 | geo_yearly_index 0 行 + region_assessment 百分位实证 + gkx 0 表 + dev 3 表行数 |
| B5 | 确定性 | 榜单按 weighted 降序；权重假设显式声明（B10） |
| B6 | 闸门自身被闸 | 不自跑闸门，由派单方统一跑 |
| B7 | 产物只由脚本产出 | 手改禁令；改脚本→重跑 |
| B8 | 回执不复收 | 派单方抽硬证据复验 |
| B9 | 单位/日期陷阱 | 2025 截面（2026 残年不用）；0-100 制与百分位制区分标注 |
| B10 | 口径裁定保守交付 | 双权重口径并列 + 权重假设声明 + 陷阱面使用警示 |
| B11 | 多本账互推 | 五维面板与 013 件同表同值；region_assessment 行数与 lane1 probe 探针一致 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 有现成区域评分结果面吗？ | 无（预留表 0 行；大表是陷阱面） | `jiuxin_geo_yearly_index_rows=0` |
| 能转换出评分吗？ | 能算但权重未裁定（口径 A 是假设权重） | §1.6 权重声明 |
| region_assessment 能直接用吗？ | 不能（节点内百分位，城市间不可比） | 北京 AVG 48.8899 实证 |

## 摘要

「区域能力评分」三页同构挂载（全球/湾区/深圳创新监测的详情卡首张），mock 是 94/91/86 式手写演示值。三源探测给出全批最重要的**陷阱面警示**：久新 `ads_technology_region_assessment`（2,708,162 行、19,027 技术节点 × 389 地名）看似完美承载——带 0-100 分、带排名——但实测分值是**节点内百分位**：北京 10,959 行平均 48.8899 分、10,928 个满分行散布在小城镇（辽阳市/合作市/福山区等 AVG=50.0）与北京之间。它回答的是「某地区在某技术节点上位列前 X%」，**不是**「某城市创新能力综合 84 分」——直接回填将制造跨城错序。真正的评分预留表 `ads_geo_yearly_index` 0 行（公式未审定）。可走的路是转换：与 013 件共享的五维面板（论文/项目/人才/机构/流入人才）min-max 归一后加权——实测口径 A（权重 [25,25,25,15,10] 仿 UI 创新力指数模板）：China 90.7862 / US 42.8663 / UK 12.8204 / Germany 10.3989 / Hong Kong 7.599；Top3 在等权对照下不变（权重敏感性通过，但第 4 名起洗牌）。**压档三因**：①权重是产品决策（SRS seq 73 要求用户可查看/设置权重——三源无审定公式）；②预留表空载（升档看上游）；③评分的「三页三粒度」（全球国家/湾区城市/深圳区级）需三套基准，本件仅证国家粒度。判**部分支持**：转换路径结构+数据达标，公式侧留白待裁定。

- 需求判定：**UI 推导叶**（指标名三份说明书 0 命中；最近锚 seq 73 创新能力指数计算『基于数据模型……生成创新能力指数，用户可查看指数计算方法和权重设置』——载体级；seq 84 创新能力排名计算为城市级姊妹锚）。
- 复现状态：脚本已跑通；双权重口径 Top12 + 陷阱面实证 + 三源负结论全部落产物。
- 档位结论：**部分支持**（公式未审定 + 预留表空载 + 三页三粒度基准未建）。
- 关键事实：region_assessment 的节点内百分位陷阱（北京 AVG 48.8899 vs 满分行同分）是本件核心发现——该表 2,708,162 行的「可用性」必须以本件警示为前置。
- 升档路径：上游填充 `ads_geo_yearly_index`（公式审定后）→ 直接消费 → 升完全直接支持；或甲方裁定权重 → 口径 A 转正 → 升完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/**全球创新监测**/监测对象详情卡（主）+ 跨页两处（湾区/深圳创新监测）。挂载点实查（三页同构 metricCards 首张）：

- `src/globalInnovationMonitor.js:403`：`metricCards { label: '能力评分', value: target.score ?? '-' }`——全球页详情卡。
- `src/bayAreaInnovationMonitor.js:386`：同构——湾区页详情卡。
- `src/shenzhenInnovationMonitor.js:461`：同构（第三张卡是『区级范围』变体）——深圳页详情卡。
- 姊妹算法（评分公式的 UI 内置模板）：`src/pages/global-innovation/tabs/carrierRankingCompareModel.js:96`——`创新力指数 = 专利产出×35% + 论文影响×25% + 项目转化×25% + 成果活跃×15%`，『各单项指标归一化到 0-100 后按权重加权汇总』——**UI 已内置加权评分公式模板**（载体粒度），mock score 94/91/86/89/82/87/84/79 手写演示值。

三页三粒度：全球页 mock 对象混合城市/项目（旧金山湾区项目 94 分）、湾区页城市、深圳页区级——评分基准需按页分建。

### 1.2 为什么需要本指标

能力评分是创新监测的** headline 数字**：把多源证据压成一个 0-100 的标量，是详情卡首张、排行榜排序键（`RANK_SCORE_DIMENSION='score'`）、趋势线（mock `+18.4%` 式涨幅）的通用燃料。本指标承担三职：①**快速读数**（详情卡 3 秒判断强弱）；②**排序底座**（载体/城市榜的 rank 键）；③**变化追踪**（评分年度序列即能力演进）。数据侧本件是「评分件」的方法论代表：评分 = 结构 + 数据 + **公式**三件套——前两件三源可凑（与 013 件同面板），公式件（权重体系）三源均无审定版本——这类件的判档关键是「公式是否有权威背书 + 是否须产品裁定」，本件两者皆悬。

### 1.3 需求文档是否给出定义方法

**需求文档没给出计算方法，只给了方法治理要求。**「区域能力评分」作为指标名三份说明书 0 命中。全球创新监测.md 两处最近锚：seq 73『基于数据模型对各创新载体的创新成果数据进行计算，生成创新能力指数，用户可查看指数计算方法和权重设置』——明言**权重须可查看/设置**（即权重是产品配置非黑箱）；seq 84『基于数据模型分析计算各大城市的创新能力排名，用户可查看排名结果和计算方法』——同族治理要求（城市粒度）。两处均未给维度构成、归一式、权重值——「数据模型」是需求方对上游的**委托表述**，非定义。本件的双权重口径构造即填补该留白的保守方案（权重显式声明待裁定）。

### 1.4 类似指标权威方法可行性分析概要

区域创新评分的权威范式有三支。**WIPO GII 2025**（R1）：78 指标→21 子支柱→7 支柱→投入/产出双分指数→总分（两分指数算术平均），指标 0-100 归一、**权重树公开**、JRC 独立统计审计（置信区间+敏感性分析）——「加权评分 + 治理透明」的全球标杆；**欧盟 RIS 2025**（R2）：23 指标分位对齐归一后**等权平均**（available indicators 等权）——「等权朴素制」代表（权重敏感性最小化）；**UI 内置模板**（R3，本件姊妹算法）：四维加权 35/25/25/15、归一 0-100、权重用户可调（`getNextCarrierWeightDraft`）——产品侧已内置治理机制。方法族对照：

| 方法族 | 权重 | 归一 | 三源承载 | 匹配度 |
|---|---|---|---|---|
| GII 权重树（R1） | 固定权重树公开 | 0-100 | 五维可承载 | **高（正式版范式）** |
| RIS 等权（R2） | 等权 | 分位对齐 | 五维可承载 | **高（口径 B 同构）** |
| UI 模板（R3） | 用户可调 35/25/25/15 | 0-100 | 五维扩维适配 | 中高（即期） |
| 本件口径 A | [25,25,25,15,10] 假设 | min-max | 同上 | 中（待裁定） |

结论：等权制（口径 B）与 RIS 同构、权重树制（GII）与 UI 模板同构——两制式本件并列实测，Top3 排名两制一致（敏感性通过）；正式版走 GII 式权重树 + 甲方裁定。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/globalInnovationMonitor.js:403`；`…/bayAreaInnovationMonitor.js:386`；`…/shenzhenInnovationMonitor.js:461`（三页详情卡）；`…/pages/global-innovation/tabs/carrierRankingCompareModel.js:96`（权重模板）。
- SRS：`bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md` seq 73（指数计算治理锚）、seq 84（城市排名锚）。
- 数据：`code/_snapshots/_probe_lane5_s3_01_out.json`（ads_geo_yearly_index DESC/COUNT #9/#10 0 行原值）；`code/_lane1_probe_s3_01_out.json`（region_assessment 行数与年份）；`code/_lane1_probe2_s3_01_out.json`（满分行数 10,928）。

### 1.6 推测原意与推测定义

**推测定义（双权重口径，均须披露权重假设）**：

- **口径 A（加权制·仿 UI 模板扩五维）**：`score(c) = Σ_d w_d × norm_d(c)`，d ∈ {papers, projects, talents, institutions, inbound_talents}，w = [25, 25, 25, 15, 10]%（**本件假设权重——仿 carrierRankingCompareModel 四维模板 35/25/25/15 的扩维变体，非甲方审定**），norm = 2025 截面 224 国 min-max 归一 ×100。实测 Top5：China 90.7862 / United States 42.8663 / United Kingdom 12.8204 / Germany 10.3989 / Hong Kong 7.599。
- **口径 B（等权制·RIS 同构对照）**：同式换 w = 20%×5。实测 Top5：China 87.7149 / US 46.345 / UK 13.2657 / Germany 11.0854 / Hong Kong 9.499——**Top3 两制一致**（`jiuxin_country_score_top3_weighted == top3_equal`），第 4-5 名德国/香港位次互换（权重敏感性样本）。
- **陷阱面正确读法**（region_assessment）：`regional_potential_score` = 节点内百分位——北京 100.000000 行应读作「北京在该技术节点的证据覆盖位列所有地区前 1/10959」，跨城聚合（AVG/MAX）均无意义。

**降档/升档触发器（B10 模板）**：若甲方裁定权重（或接受等权制）→ 口径 A/B 转正 → 升完全转换支持；若上游填充 `ads_geo_yearly_index`（公式 `geo_yearly_mvp_v1` 审定后）→ 直接消费 → 升完全直接支持；若湾区/深圳页需城市/区级基准 → geo 池 CITY/PROVINCE 级同式换截面（002 件已证序列连续）→ 各页各建基准，档位不变。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md`（主）+ 跨页两挂载 |
| 所属四级功能 | 全球创新监测（33 叶）+ 湾区/深圳创新监测（跨模块） |
| 本件挂载视图 | 三页详情卡首张（主）+ 载体排行排序键（姊妹） |
| 需求叶对应 | 无同名叶；最近 seq 73/seq 84 治理级锚 |
| 批内相邻件 | M_SCIUI_INNOV_013（能力结构——同五维面板的结构件，本件是标量件）；M_SCIUI_INNOV_004（活跃度——国家级同族复合件）；M_SCIUI_INNOV_017（领域排名——评分作排序键的下游件） |
| 跨模块参照 | 湾区创新监测、深圳创新监测（跨页挂载语境） |

本件与 013 构成「标量/结构」对：同一五维面板，013 消费形状（雷达）、本件消费面积（加权标量）——评分 = 结构的加权和，两件共享归一基准（组内一致性由 B3 保证）。与 004（活跃度）的分工：004 是「存量+流量」双分支诊断件，本件是「单分支加权」评分件——前者答「活跃吗」、后者答「几分」。

## 二、计算过程

### 2.1 装载与规模校验

久新 `ads_geo_yearly_metrics` 171,736 行（五维面板与 013 件同源）；COUNTRY 级 2025 年 222 行（`jiuxin_country_2025_rows_for_score`）作评分样本。`ads_geo_yearly_index` 0 行断言（与官方快照 #10 原值一致）；`ads_technology_region_assessment` 2,708,162 行断言（与 lane1 probe 原值一致，B11 零漂移）。

### 2.2 陷阱面实证：节点内百分位制（主降档证据）

```sql
SELECT COUNT(*), ROUND(AVG(regional_potential_score),4)
FROM ads_technology_region_assessment
WHERE location_name_zh='北京市' AND model_version='technology_insight_mvp_v2_eto_cluster_technology'
```

→ 10,959 行、AVG 48.8899（`jiuxin_region_assessment_beijing_rows_v2` / `jiuxin_region_assessment_beijing_avg_score`）。城市级聚合视角：按地名 GROUP BY 后 AVG 排序，辽阳市/合作市/福山区（2-4 节点小城）AVG=50.0 居首，北京 48.8899 居后、上海 47.9260、广州 47.0593 更后（三值为本件交互探针补测，产物登记北京值）——**小城与一线同分带**，AVG 无区分度；MAX 人人 100.000000（每城都有满分行）。满分行 10,928（lane1 probe2 原值）散布 389 地名——「满分」是节点内 top1 的映射，非能力满分。

### 2.3 gkx/dev 侧负结论（absence_probe）

gkx score/assess/power 三关键字 0 表（lane1 probe2 官方探针，本件登记消费）；dev `gkxlumenx_ads` 3 张 score 类表行数实测：enterprise_score **120**（企业粒度）、industry_chain_region_scorecard **0**、svc_tech_power_score **0**（`dev_ads_score_table_rows=[120,0,0]`）——企业/产业链粒度且基本空载，非区域评分承载。

### 2.4 口径 A：加权评分（2025 截面 222 国）

五维 min-max 归一 ×100 后按 [25,25,25,15,10]% 加权。Top12 见产物 `jiuxin_country_score_2025_top12_weighted`：China 90.7862 / United States 42.8663 / United Kingdom 12.8204 / Germany 10.3989 / Hong Kong 7.599……全球均值 1.273（`jiuxin_country_score_2025_global_mean_weighted`——222 国多数为长尾小国，均值被压低）。Top1 领先差值 47.9199 分（`derived.jiuxin_score_top1_gap_pts` = 90.7862−42.8663）。

### 2.5 口径 B：等权对照（权重敏感性）

等权 20%×5 重算（`jiuxin_country_score_top3_equal`）：Top3 = [China, United States, United Kingdom] 与口径 A 一致——**头部排名对权重不敏感**；第 4-5 名 Germany/Hong Kong 位次互换（10.3989/7.599 → 11.0854/9.499）——腰部对权重敏感。RIS 等权制（R2）与 GII 权重树制（R1）在本数据上的分歧仅现于腰部。

### 2.6 相邻承载：region_assessment 的正确消费方式

该表的合法消费是**单节点透视**（「北京在节点 X 的覆盖分位」）而非城市评分——与 017 件（领域排名）的 topic 视角可拼接（节点→领域→国别排名链）。本件登记此路由防后批误用（附录 C.4 风险表首行）。

### 2.7 复现代码结果展示

| 产物键 | 值（节选） |
|---|---|
| `jiuxin_geo_yearly_index_rows` | 0 |
| `jiuxin_region_assessment_rows` | 2,708,162 |
| `jiuxin_region_assessment_named_locs` | 389 |
| `jiuxin_region_assessment_beijing_avg_score` | 48.8899 |
| `jiuxin_country_score_2025_top12_weighted[0..2]` | China 90.7862；US 42.8663；UK 12.8204 |
| `jiuxin_country_score_top3_weighted == top3_equal` | [China, US, UK] 两制一致 |
| `dev_ads_score_table_rows` | [120, 0, 0] |
| `derived.jiuxin_score_top1_gap_pts` | 47.9199 |

### 2.8 分步证据对照表

| 步骤 | SQL/操作 | 产物键 | 结果 |
|---|---|---|---|
| S1 预留表断言 | COUNT geo_yearly_index | `jiuxin_geo_yearly_index_rows` | 0（与快照一致） |
| S2 大表断言 | COUNT region_assessment | `jiuxin_region_assessment_rows` | 2,708,162（零漂移） |
| S3 百分位实证 | 北京 v2 AVG | `…_beijing_avg_score` | 48.8899 |
| S4 dev 行数 | 3 score 表 COUNT | `dev_ads_score_table_rows` | [120,0,0] |
| S5 口径 A | 五维加权 | `…_top12_weighted` | China 90.7862 居首 |
| S6 口径 B | 等权重算 | `…_top3_equal` | Top3 与 A 一致 |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 源表 | 行数 | 库别 | 状态 |
|---|---|---|---|---|
| D1 评分预留表 | ads_geo_yearly_index | 0 | jiuxin | **空载（主降档因）** |
| D2 五维面板 | ads_geo_yearly_metrics COUNTRY 2025 | 222 | jiuxin | 全量（转换路径原料） |
| D3 陷阱面 | ads_technology_region_assessment | 2,708,162 | jiuxin | 结构在、语义错配（节点内百分位） |
| D4 gkx 评分类 | — | 0 表 | gkx | 三关键字 0 命中 |
| D5 dev 评分类 | gkxlumenx_ads 3 表 | 120/0/0 | dev | 企业粒度+空载 |

### 3.2 D1 空载面明细

schema 完整（location_id/statistics_year/index_code/index_name_zh/raw_value/normalized_value——官方快照 #9 DESC），`metric_definition_version` 列预期 `geo_yearly_mvp_v1` 类版本号——公式侧上游有规划未落地。**升档第一杠杆**。

### 3.3 D3 陷阱面明细（主警示）

2,708,162 行 = 19,027 节点 × 2 model_version × 地名行；389 个地名（`jiuxin_region_assessment_named_locs`）；北京单城 21,918 行（两版本各 10,959；21,918 与节点总数 19,027 为本件交互探针补测值）。分值域 [0,100] 但语义是**节点内百分位**——跨城/跨节点聚合均无效。合法消费见 §2.6。

### 3.4 D4/D5 负结论面

gkx 三关键字 0 表（官方探针）；dev 3 表中 industry_chain_region_scorecard（名字最像区域评分）0 行——两库评分面均不承载。

### 3.5 现场复核清单

- `SELECT COUNT(*) FROM ads_geo_yearly_index` → 0
- `SELECT COUNT(*) FROM ads_technology_region_assessment` → 2,708,162
- `SELECT AVG(regional_potential_score) FROM ads_technology_region_assessment WHERE location_name_zh='北京市' AND model_version='technology_insight_mvp_v2_eto_cluster_technology'` → 48.8899
- 口径 A 复算：五维归一后 [25,25,25,15,10] 加权 → China 90.7862

## 四、数据缺失情况

### 4.1 评分公式未审定（公式级，主降档因）

三源无审定权重体系（gkx/dev 0 承载；久新预留表空载）；SRS seq 73 要求权重可查看/设置——权重是产品决策。**修复建议**：甲方裁定权重（或采纳等权制 R2 范式）→ 口径 A/B 转正。**影响面**：评分卡以「假设权重」标签过渡，正式回填须等裁定。

### 4.2 预留表空载（数据级）

`ads_geo_yearly_index` 0 行——上游公式审定后填充即升档（§1.6 触发器）。**修复建议**：跟踪上游 1.7.x 版本发布。**影响面**：完全直接支持的路径被锁，当前只能走转换。

### 4.3 三页三粒度基准未建（粒度级）

全球页（国家/城市混合 mock）、湾区页（城市）、深圳页（区级）需三套归一基准——本件仅证国家粒度（222 国截面）；城市级可由同表 CITY 级换截面（与 013 件同路径）、区级需深圳区划映射。**修复建议**：各页各建基准卡+权重配置项（UI 已有 `getNextCarrierWeightDraft` 机制可复用）。**影响面**：湾区/深圳页回填延后。

## 参考文献

1. Global Innovation Index 2025 – Appendix I[EB/OL]. WIPO. https://www.wipo.int/web-publications/global-innovation-index-2025/en/appendix-i-conceptual-and-measurement-framework-of-the-global-innovation-index.html （R1，加权评分+权重树公开+JRC 审计范式，2026-11-01 WebSearch 核验可达）
2. Regional Innovation Scoreboard 2025[EB/OL]. European Commission. https://research-and-innovation.ec.europa.eu/document/download/f6019e31-2927-4802-ae56-5f2fd92cb6c3_en （R2，等权平均制复合评分范式，2026-11-01 WebSearch 核验可达）
3. Global Innovation Index 2025 – Appendix II: JRC statistical audit[EB/OL]. WIPO/EU JRC. https://www.wipo.int/web-publications/global-innovation-index-2025/en/appendix-ii-joint-research-centre-jrc-statistical-audit-of-the-2025-global-innovation-index.html （R4，评分敏感性/置信区间审计方法，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

**「区域能力评分」未作为指标名出现在三份说明书。** 检索记录（2026-11-01）：

| 检索词 | 范围 | 命中 |
|---|---|---|
| 能力评分 | 全球创新监测.md | 0 |
| 评分 | 全球创新监测.md | 0（评分/指数语义近邻见 seq 73/84） |
| score | UI 源码 | globalInnovationMonitor.js:403 等 3 页 + carrierRankingCompareModel.js:96（模板） |

最近语义原文：
- seq 73：『基于数据模型对各创新载体的创新成果数据进行计算，生成创新能力指数，用户可查看指数计算方法和权重设置。』
- seq 84：『基于数据模型分析计算各大城市的创新能力排名，用户可查看排名结果和计算方法。』

### A.2 检索记录逐行

（检索工具：ripgrep 于 SRS 目录与 repos/demo-ui-science/src；时间 2026-11-01；命中行号已实查 ±10 行上下文。）

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_INNOV_014_out.json`（20261101 实跑：双权重口径 + 陷阱面实证 + 三源负结论在案）。
- 本 lane 共享探针：`code/_snapshots/_probe_lane5_s3_01_out.json`（geo_yearly_index DESC/COUNT #9/#10）；`code/_lane1_probe_s3_01_out.json`（region_assessment 行数/年份/样例）；`code/_lane1_probe2_s3_01_out.json`（满分行数、gkx score LIKE 0、dev ads score 3 表名）。

### B.2 本件产物逐键清单（`code/M_SCIUI_INNOV_014_out.json`，20261101 实跑）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `jiuxin_geo_yearly_index_rows` | 计数 | 0 | §2.1/§〇 |
| `jiuxin_region_assessment_rows` | 计数 | 2,708,162 | §2.1/§2.2 |
| `jiuxin_region_assessment_named_locs` | 计数 | 389 | §2.2/§3.3 |
| `jiuxin_region_assessment_full_score_rows` | 计数 | 10,928 | §2.2 |
| `jiuxin_region_assessment_beijing_rows_v2` | 计数 | 10,959 | §2.2 |
| `jiuxin_region_assessment_beijing_avg_score` | 实测 | 48.8899 | §2.2/§〇 |
| `jiuxin_country_2025_rows_for_score` | 计数 | 222 | §2.4 |
| `jiuxin_country_score_2025_top12_weighted` | 榜单 | 12 国加权分 | §2.4/§2.7 |
| `jiuxin_country_score_2025_global_mean_weighted` | 均值 | 8.4519 | §2.4 |
| `jiuxin_country_score_top3_weighted` / `_equal` | 敏感性 | [China,US,UK] 两制一致 | §2.5 |
| `dev_ads_score_table_rows` | 行数 | [120, 0, 0] | §2.3 |
| `derived.jiuxin_score_top1_gap_pts` | 派生 | 47.9199 | §2.4 |
| `derived.jiuxin_region_assessment_named_pct` | 派生 | 0.404666 | §3.3 体量参照 |
| `absence_probe` | 探针 | gkx 0 表 + dev 3 表 | §2.3 |
| `support_judgment` | 判档 | 部分支持 | §〇 |

### B.3 共享快照消费（B11 零漂移）

本件消费：官方 lane5 快照 #10（geo_yearly_index 0 行）断言一致；lane1 probe（region_assessment 2,708,162 / model_version 域 v1+v2）；lane1 probe2（满分行 10,928、gkx score LIKE 0 表、dev ads score 3 表名——本件补行数 [120,0,0]）。全部引用原值零漂移。

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 权重制 | 三源承载 | 贴合度 |
|---|---|---|---|
| GII 权重树（R1） | 固定公开 | 五维可承载 | **高（正式版）** |
| RIS 等权（R2） | 等权 | 五维可承载（口径 B 同构） | **高** |
| UI 模板（R3） | 用户可调 | 五维扩维适配 | 中高（即期） |
| 口径 A 假设权重 | [25,25,25,15,10] | 同上 | 中（待裁定） |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 质量 | 缺口 |
|---|---|---|---|
| geo_yearly_index | 0 行 | schema 完整 | 公式未审定（空载） |
| 五维面板 COUNTRY 2025 | 222 | 全量 | 权重未裁定 |
| region_assessment | 2,708,162 | 节点内百分位 | **语义错配（勿当城市评分）** |
| gkx 评分类 | 0 表 | — | 结构缺失 |
| dev 3 score 表 | 120/0/0 | 企业粒度 | 非区域承载 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 口径 B 等权评分（RIS 同构，权重敏感性最小）+「假设权重」标签 | 甲方接受等权过渡 |
| v2 | 甲方裁定权重 → 口径 A 转正 + 权重配置项（复用 UI 模板机制） | 产品决策 |
| v3 | 上游填充 geo_yearly_index → 直接消费 | 上游 1.7.x |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| region_assessment 被当城市评分回填 | **致命** | 本件警示前置 + §2.6 正确读法 |
| 假设权重被当审定口径 | **高** | 「假设权重」标签 + 裁定触发器 |
| 三页三粒度基准混用 | 高 | 各页各建基准卡 |
| min-max 钳制（China 90.78 压扁腰部） | 中 | 分位归一（v2 同步） |

### C.5 总判

**部分支持**：结构+数据可凑（五维面板），公式侧三源均无审定（权重待裁定 + 预留表空载）——评分件「三件套缺一」的典型。陷阱面（region_assessment 百分位）警示与正确路由登记在案，升档双触发器写死 §1.6，按 B10 保守交付。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_INNOV_014.py` | 退出码 0，落 `_out.json` |
| 数据入口 | jiuxin 直连只读；gkx 经 `_gkxdb.py`；dev 经 `_gkxdb.live` | demo_* 直接 raise |
| 陷阱面复核 | 北京 v2 AVG | 48.8899 |
| 口径 A 复算 | 五维归一加权 [25,25,25,15,10] | China 90.7862 |
| 敏感性复核 | 等权重算 Top3 | 与口径 A 一致 |
| 判档一致 | MD 文首 vs 产物 `support_judgment` | 部分支持 |
| mock 残留检查 | `rg "score: 94" repos/demo-ui-science/src/globalInnovationMonitor.js` | 正式版替换后无 mock |
