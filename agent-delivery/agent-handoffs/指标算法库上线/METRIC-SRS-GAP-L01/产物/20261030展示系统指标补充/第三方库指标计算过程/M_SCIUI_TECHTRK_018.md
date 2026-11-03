# 技术竞争力水平与潜力评估（M_SCIUI_TECHTRK_018）

> **类型**：SCORE-SET（区域竞争力五卡+维度 TOP5+对标排名的组合读数）｜ **域**：科技发展态势·技术发展跟踪·竞争力水平与潜力评估（UI 侧挂科技发展规划页重点领域规划 Tab）｜ **UI 挂载**：`TechDevelopmentPlan.tsx:3015`（Card「竞争力水平与潜力评估」）
> **数据支持度**：**部分支持**｜ **公式定义人**：库侧既成（久新 region_assessment/institution_power 两套评分）+ 工程侧组合定义（五卡→库表映射）｜ **口径归属**：**需求明列叶**（跨页面同名：《科技发展规划.md》seq 186「竞争力水平与潜力评估」，excel_row 189；主文档 1129/1135 行同名词）——注意该叶属科技发展规划页，与本件 UI 挂载同页同名，三份指定说明书本身未出现该指标名
> **复现脚本**：`code/M_SCIUI_TECHTRK_018.py`｜ **产物**：`code/M_SCIUI_TECHTRK_018_out.json`
> **四判定摘要**：直接结构 = 部分（久新 region_assessment 有区域潜力分+证据计数+强弱文本；无五维分项结构）；直接数据 = 是（2,708,162 行、7,816 区域×19,430 节点全量有分）；依赖结构 = 部分（对标粒度失配：库侧最细市级、UI 需园区/城区级；开放协同需另表聚合）；依赖数据 = 部分（单轮快照；政策/市场证据未接入 PARTIAL_INTERNAL_EVIDENCE）
> **数据源口径注记**：三源评估——开发库（`gkxlumenx_*`，禁 `demo_*`）+ gkx（只读 280 表）+ 久新 jiuxin_warehouse（只读 203 表）。本件主数据面在久新。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（三源）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** 本件是 Lane 3 唯一的需求同名词件（「竞争力水平与潜力评估」在《科技发展规划.md》seq 186 与主文档 1129/1135 行出现，UI 挂载组件恰是科技发展规划页的重点领域规划 Tab——指标名、页面、组件三方对齐，需求原文明确定义「评估区域科技创新的竞争力水平和潜力情况…提供与对标区域的对比分析」）。库侧承载厚实但结构错位：久新 `ads_technology_region_assessment` 2,708,162 行给 7,816 个区域×19,430 技术节点逐一评出 regional_potential_score（0–100）+四类证据计数+强弱项文本+建议，`ads_institution_technology_power` 64,698 机构带四分项加权科技力量分，`ads_institution_collaboration_yearly` 1,438 万行协作对可撑开放协同——但 UI 的五卡结构（综合指数/创新能力/产业基础/开放协同/发展潜力）在区域粒度无分项承载（只有单一总分），对标粒度失配（UI 对标行是南山区/深圳湾合作区/香港科技园等园区级，库侧 location 最细到市级），且全量 2,708,162 行 evidence_coverage_status 单值 PARTIAL_INTERNAL_EVIDENCE（政策/市场证据未接入）。总分有、结构半、粒度错，判部分支持。

### 批次纪律摘要（B1–B11 对照，skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 两派生键分子分母同源同表（jiuxin region_assessment） |
| B4 | 负结论带探针 | absence_probe 四条（dev/gkx 结果面、五维结构、园区粒度） |
| B5 | 确定性 | 聚合 ORDER BY AVG() 表达式排序；重点城市固定 IN 清单 |
| B6 | 闸门自身被闸 | 本件不跑闸门，派单方统一跑 |
| B7 | 产物只由脚本产出 | 实跑产出，无手改 |
| B8 | 回执不复收 | 城市聚合/Top5 机构/协作量亲自实跑 |
| B9 | 单位/日期陷阱 | 深圳命名无「市」字；Doris ORDER BY 别名报错改表达式；双版本去重 |
| B10 | 口径裁定保守交付 | 「市级总分先行」vs「园区级对标」双口径（§1.6） |
| B11 | 多本账互推 | 2,708,162/64,698/14,380,246 与探针快照零漂移 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 区域竞争力分存在吗？ | 存在且巨量 | region_assessment 2,708,162 行全量有分（0–100） |
| 五维分项存在吗？ | 不存在（区域粒度） | 仅单一总分+证据计数；institution_power 四分项主体是机构 |
| 对标粒度匹配吗？ | 不匹配 | UI 园区/城区级 vs 库侧市级最细（区域名 Top15 探针） |

## 摘要

「技术竞争力水平与潜力评估」是重点领域规划 Tab 的评估面板：五张竞争力卡（综合指数 78.5/创新能力 88/产业基础 85/开放协同 62/发展潜力 82，mock）、维度得分 TOP5 进度条、对标区域排名表（南山区/深圳湾合作区/广州天河区等五档）。库侧实测三个结果面：一、`ads_technology_region_assessment`——7,816 个区域对 19,430 个技术节点逐一评估，regional_potential_score 全量 0–100（北京市 21,918 行均分 48.89、上海 47.93、广州市 47.06、深圳 47.05），每行带 paper/patent/project/institution/company 五类证据计数与强弱项文本（「现有论文、专利、机构和项目证据形成的区域比较优势」/「政策、市场和真实应用案例尚未接入」）；二、`ads_institution_technology_power`——64,698 机构四分项（论文/引用/人才/主题）加权科技力量分，Top5 为中国科学院 99.999/国科大/北大/浙大/上交；三、协作网络 1,438 万对可聚合开放协同。缺口三处：区域粒度无五维分项（五卡只能总分+机构分项拼装）、对标粒度失配（园区级无 location）、证据覆盖恒 PARTIAL（政策/市场缺席）。判**部分支持**：需求明列+总分海量，结构适配是主战场。

- 需求判定：**需求同名词命中**（seq 186 跨页面同页 Tab；主文档 1129/1135）——Lane 3 唯一需求侧确证件。
- 复现状态：脚本已跑通；区域统计、重点城市聚合、机构 Top5、协作量落产物。
- 档位结论：**部分支持**（五维结构缺+对标粒度错+证据覆盖部分三因）。
- 关键事实：全量 evidence_coverage_status=PARTIAL_INTERNAL_EVIDENCE——竞争力结论必须带覆盖度标签。
- 升档路径：区域五维分项建模（素材在库）+园区级 location 扩充 → 面板全格可填。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/**科技发展规划**/重点领域规划/竞争力水平与潜力评估（SRS《科技发展规划.md》seq 186，excel_row 189）。UI 侧承载是 `TechDevelopmentPlan.tsx:3015` 的 Card「竞争力水平与潜力评估」（重点领域规划 Tab 的网格中区卡片），内部三块：

```text
// TechDevelopmentPlan.tsx:862-876（mock 数据源）
const keyAreaCompetitivenessMetrics = [
  { key: 'composite', label: '综合指数', value: 78.5, change: '12.3%' },
  { key: 'innovation', label: '创新能力', value: 88, change: '8.6%' },
  { key: 'industry', label: '产业基础', value: 85, change: '6.2%' },
  { key: 'openness', label: '开放协同', value: 62, change: '5.4%' },
  { key: 'potential', label: '发展潜力', value: 82, change: '10.1%' },
];
const keyAreaDimensionScores = [ /* 维度得分 TOP5：创新资源 92 / 科研产出 88 /
  产业竞争力 85 / 人才支撑 78 / 开放协同 72 */ ];
const keyAreaBenchmarkRows = [ /* 对标：南山区 78.5 / 深圳湾合作区 74.2 / 广州天河区 71.3 /
  香港科技园 69.1 / 珠海横琴新区 66.8 */ ];
```

卡片头部还有区域切换（`formatKeyAreaRegionName(selectedRegionProfile.name)`）——面板是**可切换区域**的评估视图。mock 注记：五卡值与 change%、维度百分比、对标分均为演示值（不参与支持度结论），但**结构**（五卡+TOP5+对标）与**粒度**（区域/城区级对标）是真实需求证据。另 `techDevelopmentPlan.js:39` 时间线事件「2023-08 上海：竞争力水平与潜力评估纳入产业、技术和空间承载指标」给出维度线索：产业、技术、空间承载。

### 1.2 为什么需要本指标

重点领域规划的回答对象是「这个区域值不值得布局这个领域」：竞争力水平回答「现在强不强」，潜力回答「将来强不强」，对标回答「跟谁比、差多少」。三块合一才有决策闭环——只看总分不知道短板在哪个维，只看维度不知道相对位置，只看对标不知道绝对水平。这也是为什么 UI 把五卡+TOP5+对标排成一个 Card：它是规划 Tab 的「体检报告」页。库侧 region_assessment 的强弱项文本（strength_summary/weakness_summary）与建议（recommendation）恰好是这套叙事的文本侧素材，分项结构则是缺口所在。

### 1.3 需求文档是否给出定义方法

**需求文档给出了功能定义但未给出计算方法。** SRS seq 186 原文（附录 A）：「评估区域科技创新的竞争力水平和潜力情况，用户可查看竞争力指标体系和评估结果，提供与对标区域的对比分析」——明确了对象（区域科技创新）、交付物（指标体系+评估结果+对标分析），但「竞争力指标体系」的具体维度、权重、算法未定义。主文档 1129 行列举功能名、1135 行同。UI mock 的五卡结构（综合/创新/产业基础/开放协同/发展潜力）是前端对「指标体系」的一种实现猜测，与时间线事件的「产业、技术和空间承载」线索部分重叠（产业基础✓、技术→创新能力近似、空间承载无对应卡）。

### 1.4 类似指标权威方法可行性分析概要

区域创新竞争力评估的权威方法族：OECD/JRC 复合指标手册（R1）是「指标体系」的方法论总纲——理论框架→维度选定→标准化→加权→敏感性分析，手册专章讨论国家/区域竞争力指数的构建风险（指标混搭输入产出、权重主观）；Oslo 手册（R2）第 11 章给区域创新指标的数据组织规范（企业/机构向区域的归属、空间分摊）；OECD 区域统计框架（R3，Regions and Cities at a Glance 的指数方法章）是多层级区域（国家/大区/城市）对标的实践参照。方法族对照：

| 方法族 | 代表 | 结构形态 | 与本库匹配 |
|---|---|---|---|
| 多维加权指数 | OECD/JRC（R1） | 维度×权重→总分 | **部分**（institution_power 四分项是此形态；区域粒度无分项） |
| 区域归属分摊 | Oslo（R2） | 主体→区域 | 有（region_yearly_metrics 三级 location） |
| 多层级对标 | OECD 区域统计（R3） | 层级内排名 | 部分（库侧有 rank 列；层级只到市级） |

结论：方法学完备、机构粒度已有四分项先例，区域五维分项可循 institution_power 模式自建（素材在库）。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/TechDevelopmentPlan.tsx:3015`（Card 标题）、`:862-876`（三组 mock）、`:3019-3050`（渲染结构）；`techDevelopmentPlan.js:39`（时间线维度线索）。
- SRS：`bid-reference/srs/02-科技信息展示系统/科技发展态势/科技发展规划.md` seq 186（excel_row 189），原文见附录 A。
- 主需求文档：《科技信息展示系统和科技专题服务系统.md》:1129（功能列举）、:1135（1.1.1.1.4.1.9.2.2 章节号）。

### 1.6 推测原意与推测定义

**推测定义（双口径并列，B10）**：

- 口径 A（**市级总分+机构分项拼装**，库侧现状可即期组装）：综合指数=AVG(regional_potential_score)（区域切片）；创新能力/产业基础≈institution_power 的 paper_score/citation_score 与 topic_score/talent_score 分项经区域聚合（机构→城市映射）；发展潜力=016 件潜力分的区域切片；开放协同=collaboration 表国际协作对聚合——五卡四张有算式，但「区域分项」由机构侧聚合近似，非官方区域分项；
- 口径 B（**区域五维分项官方建模**，升档路径）：循 institution_power 模式（R1 十步法）在 region 粒度建维度表——institution/company/paper/patent/project 五类证据计数已在每行齐备，标准化+定权即可出分。

**降档/升档触发器**：若甲方接受口径 A（机构侧近似分项+覆盖度标签）→ 维持部分支持但五卡可上线；若口径 B 建模落地 → 五卡官方化；若园区级 location 扩充（对标粒度）→ 对标表可填；三者齐备升完全转换支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/科技发展规划.md` |
| 所属四级功能 | 科技发展规划（seq 179–194 等） |
| 所属面板 | 重点领域规划（seq 185–189：空间布局分析/**竞争力水平与潜力评估**/土地用途与效益/科技载体分布/产业与领域筛选联动） |
| 本件叶 | **竞争力水平与潜力评估（seq 186，excel_row 189）——需求明列** |
| 同面板相邻叶 | 空间布局分析（seq 185）/ 土地用途与效益（seq 187）/ 载体分布（seq 188，Lane 5 INNOV 系关联） |
| UI 容器 | TechDevelopmentPlan.tsx 重点领域规划 Tab 网格中区 Card |

批内坐标：本件是 Lane 3 的「区域聚合枢纽」——总分承 016（同一节点分的区域切片）、证据计数承 014（同一数据覆盖体系）、开放协同独享协作表；与 Lane 5 的 M_SCIUI_INNOV_014（区域能力评分）是全局近亲（创新监测板块的区域评分），两件若同期立项应共用区域分组建模。需求侧它是 5 件中唯一同名词命中件，附录 A 粘原文的义务成立。

## 二、计算过程

### 2.1 装载与规模审计

直连久新 Doris（只读）。`ads_technology_region_assessment` 全表 2,708,162 行——审计拆解：19,430 节点×~139 区域均值×2 版本；`COUNT(DISTINCT location_id)`=7,816、`COUNT(DISTINCT technology_node_id)`=19,430（与 profile 同基，产物键齐备）。注意行数奇点：location_id 数（7,816）远大于 location_name_zh 非空数（Top15 探针显示 231 万行 location_name_zh 为 NULL——大量 location 无中文名回填），区域聚合时必须按 location_id 或非空中文名双口径防漏。双 model_version（v1/v2）同内容，单版本 1,354,081 行。

### 2.2 区域总分实测与重点城市聚合

分数统计（产物键 `jiuxin_regional_potential_score_stats`）：n=2,708,162 全量有分、min 0.0 / max 100.0 / avg 39.83。重点城市聚合（`jiuxin_region_key_cities`，固定 IN 清单确定性）：北京市 21,918 行（10,959 节点）均分 48.889888、上海 47.926008、广州市 47.059274、深圳 47.054993（库内命名「深圳」无「市」字——B9 陷阱产物留证）、南京市 46.698112、杭州市 46.518457。派生键 `jiuxin_beijing_avg_regional_score`=48.889888 与 `jiuxin_beijing_vs_shenzhen_score_gap`=1.834895（北京−深圳）。城市梯度合理（一线城市 47–49 区间），但分差极小（首尾 2.37 分）——竞争力总分对头部城市的区分度有限，五维分项的必要性由此反证。

### 2.3 证据计数与强弱项文本（区域体检报告的素材）

北京市 Top 样本（探针 `_probe_lane3_jiuxin4_out.json`）：node tcn_01ad…（rank 1，100.0 分）paper_evidence_count=5 / patent=0 / project=2930 / institution=458 / company=5；strength_summary=「现有论文、专利、机构和项目证据形成的区域比较优势」、weakness_summary=「政策、市场和真实应用案例尚未接入」。全表 evidence_coverage_status 单值 PARTIAL_INTERNAL_EVIDENCE（2,708,162/2,708,162）——库方自评证据面只到内部部分覆盖。stage 分布（`jiuxin_region_stage_code_dist`）：EARLY_RESEARCH 2,691,146（99.3%）/ ENGINEERING_VALIDATION 12,968 / EARLY_COMMERCIALIZATION 4,048——区域×技术组合绝大多数还在早期研究档。

### 2.4 机构科技力量与开放协同（五卡的分项素材）

`ads_institution_technology_power` 64,698 机构（`jiuxin_power_score_stats`：min 9.18 / max 99.999227 / avg 50.0——恰好均值 50，百分位模型特性）；Top5（`jiuxin_power_top5`）：中国科学院 99.999227（论文 177,917/被引 47,813,35/人才 19,241）、中国科学院大学、北京大学、浙江大学、上海交通大学。四分项（paper_score/citation_score/talent_score/topic_score）+四权重列——这是三库中**唯一**已落地的多维加权评分结构（R1 形态），区域五维分项可直接复用其建模模式。开放协同：`ads_institution_collaboration_yearly` 14,380,246 行协作对（其中国际协作对——collaborator_country_code 非空——见产物键 `jiuxin_collaboration_intl_pair_rows`），样本含国家/省/城市三级协作者地理属性，「开放协同」卡可由此聚合。

### 2.5 对标粒度核查

UI 对标行五档全部是园区/城区级（南山区/深圳湾合作区/广州天河区/香港科技园/珠海横琴新区）；库侧区域名 Top15（按行数）全部是市级（北京市/上海/广州市/南京市/广州市…），LIKE 探针（'%深圳%'）只命中「深圳」「深圳市」两种市级写法（后者实为同名异写），无任何园区/合作区级 location。粒度断层一档（市级→园区级），且香港科技园等跨境主体在库侧 location 体系中是否存在未探明（如存在也非园区语义）。

### 2.6 稳健性与口径敏感性

三个读数陷阱：其一，NULL 中文名 231 万行——按中文名聚合会丢 85% 行量，必须 location_id 口径为主；其二，region_assessment 的 regional_rank 是**技术内区域排名**（每个 technology_node_id 内 1–N），不是区域内技术排名，直接当「区域排名」用会语义翻转；其三，五卡若按口径 A 拼装，机构→区域的归属分摊（R2 规范）需显式规则（机构注册地 vs 多校区分摊），collaboration 表虽有地理列但机构表无城市列直连，聚合链路要经 region_yearly_metrics 的三级 location 桥接。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_TECHTRK_018.py`（直连久新只读；运行 `python3 code/M_SCIUI_TECHTRK_018.py`）。
- 产物：`code/M_SCIUI_TECHTRK_018_out.json`。正文数字与产物键逐一对应：`jiuxin_region_assessment_rows_total=2708162`（§2.1）、`jiuxin_regional_potential_score_stats`（§2.2）、`jiuxin_region_key_cities` 六城（§2.2）、`jiuxin_region_stage_code_dist`（§2.3）、`jiuxin_institution_power_rows=64698`+`jiuxin_power_top5`（§2.4）、`jiuxin_collaboration_yearly_rows=14380246`（§2.4）、派生 `jiuxin_beijing_avg_regional_score=48.889888` / `jiuxin_beijing_vs_shenzhen_score_gap=1.834895`。
- 结果解读：总分海量+证据计数+强弱文本+机构分项先例+协作网络——面板素材七成在库，缺的是区域分项结构与园区粒度。
- 对照需求功能要求的评审：「竞争力指标体系和评估结果」——结果✓（总分+文本）、指标体系半✓（机构侧有先例、区域侧待建）；「与对标区域的对比分析」——市级✓（rank+城市梯度）、园区级✗。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 规模 | 总行/区域数/节点数 | `…_rows_total` / `…_locations` / `…_nodes_single_version` | 2,708,162 / 7,816 / 19,430 |
| 总分 | 统计三读数 | `jiuxin_regional_potential_score_stats` | 0.0 / 100.0 / 39.83 |
| 城市 | 六城聚合 | `jiuxin_region_key_cities` | 北京 48.89 … 杭州 46.52 |
| 派生 | 北京均分/京深差 | `derived[0]` / `derived[1]` | 48.889888 / 1.834895 |
| 阶段 | 三档分布 | `jiuxin_region_stage_code_dist` | 2,691,146/12,968/4,048 |
| 机构 | 行数+统计 | `jiuxin_institution_power_rows`+`jiuxin_power_score_stats` | 64,698；avg 50.0 |
| 机构 | Top5 | `jiuxin_power_top5` | 中科院 99.999 居首 |
| 协同 | 协作对 | `jiuxin_collaboration_yearly_rows` | 14,380,246 |
| 潜力 | 同源复用 | `jiuxin_potential_*` 两键 | 38,860 / 19,430 |
| absence | 五维结构/园区粒度 | §3.4 四件套 | 0 / 0 |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 区域竞争力总分 | jiuxin | `region_assessment.regional_potential_score` | 2,708,162 全量有分 | 直查 | **有** |
| D2 | 证据计数+强弱文本 | jiuxin | 同表 5 计数列+3 文本列 | 同上 | 直查 | 有 |
| D3 | 机构四分项先例 | jiuxin | `institution_power` 四分项+权重 | 64,698 | 直查 | 有（机构粒度） |
| D4 | 开放协同 | jiuxin | `collaboration_yearly` | 14,380,246 | 聚合可得 | 有（需桥接） |
| D5 | 区域五维分项 | 三库 | —（区域粒度仅总分） | 0 | **不存在** | **缺（主降档因）** |
| D6 | 园区级对标粒度 | 三库 | —（location 最细市级） | 0 | 不存在 | 缺（次因） |

`support_judgment="部分支持"` 与文首一致（闸 6 对齐）。

### 3.2 D1–D4 素材七成在库

§2.2–§2.4 已列全。面板三块的映射现状：五卡——综合指数/发展潜力可直取（D1+016 切片）、创新/产业/开放三卡需机构侧聚合或建模；维度 TOP5——institution_power 四分项+region 证据计数可拼（口径 A）；对标排名——市级梯度现成（D1 城市聚合+regional_rank 技术内排名），园区级无。

### 3.3 D5 区域五维分项：从「有素材」到「有维度」的距离

institution_power 证明了库方具备多维加权建模能力（四分项+四权重+合成分+排名一应俱全），且 region_assessment 每行已带五类证据计数（paper/patent/project/institution/company）——建区域五维分项的原料（计数列）与配方（R1 十步法+机构表先例）都在库内，缺的是评估管线在区域粒度的一次重跑。这不是数据缺口而是建模决策，故本件不因 D5 判「数据不够」而因「结构未建」维持部分支持（区别于完全转换支持的「现在就能算」——五维分项需要甲方定维度框架与权重，非纯机械转换）。

### 3.4 D5/D6 absence_probe 全记录

否定性证据四件套：**查了什么**——① dev `gkxlumenx_dwd` compet/assess/eval/score 关键词（0 命中技术竞争力类，仅政策侧 4 表）；② gkx 280 表 compet/score/potential 关键词（0 命中）；③ jiuxin 区域五维分项结构（region_assessment 列清单逐一核对——仅单一总分列 regional_potential_score，无 dimension 类列；institution_power 的分项在机构主体）；④ jiuxin 园区级 location（区域名 Top15 全市级 + LIKE '%深圳%' 仅市级命中）。**条件**——区域粒度维度分列/园区级地点。**命中**——0/0/0/0。归属：**结构未建**（③）与**粒度未扩**（④），修复在评估管线与地点体系，非数据回填。

### 3.5 现场复核清单

| 复核项 | 结果 |
|---|---|
| 双版本去重 | 2,708,162=1,354,081×2 |
| NULL 中文名 | 231 万行空，location_id 口径防漏 |
| 城市聚合 | 六城固定 IN 清单，「深圳」命名陷阱产物留证 |
| Doris 方言 | ORDER BY 别名报错 → 改 AVG() 表达式（B9） |
| 机构均值 | 恰 50.0（百分位模型特性） |
| 协作对 | 14,380,246，国际对键单列 |
| 脚本形态 | 只读、零 demo_*、单进程 |

## 四、数据缺失情况

### 4.1 区域五维分项未建（主因）

UI 五卡需要维度级读数，区域粒度只有总分。原料（五类证据计数每行齐备）与配方（机构表四分项先例+R1 方法）都在，缺甲方定框架（维度定义+权重）与库方管线重跑。这是本批 5 件中修复路径最清晰的一项——不采新数据、不接新源，一次建模决策+一次管线重跑。

### 4.2 园区级粒度与证据覆盖（次因）

对标行需要园区/城区级 location（南山区/深圳湾合作区等），库侧最细市级——地点体系需扩充（政区划表可补，非技术缺口）。另全量 PARTIAL_INTERNAL_EVIDENCE：政策/市场证据未接入（与 014 件资讯源缺失同根），竞争力结论的「产业基础」「开放协同」两卡实际只吃到内部论文/专利/项目证据，覆盖度标签必须随行。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 口径 A 先行（总分+机构分项拼装+覆盖标签） | 产品决策 | 本件即期 | 五卡四张可拼 |
| 区域五维分项建模 | 评估管线 | 本件（D5）→ 升档 | 原料配方在库，需甲方定框架 |
| 园区级 location 扩充 | 地点体系 | 本件对标表+INNOV_014 | 政区划表补录 |
| 政策/市场证据接入 | 数据工程 | 本件+014+017 | 同一资讯入链工程 |

档位后果：口径 A → 部分支持语义闭合；+五维建模+园区粒度 → 完全转换支持；+证据全覆盖 → 完全直接支持。推荐：即期口径 A，中期五维建模立项（本件升档性价比最高的一步）。

## 参考文献

1. Handbook on Constructing Composite Indicators: Methodology and User Guide[EB/OL]. OECD/JRC, 2008. https://www.oecd.org/content/dam/oecd/en/publications/reports/2008/08/handbook-on-constructing-composite-indicators-methodology-and-user-guide_g1gh9301/9789264043466-en.pdf （R1，2026-11-01 WebSearch 核验可达）
2. Use of innovation data for statistical indicators and analysis: Oslo Manual 2018[EB/OL]. OECD. https://www.oecd.org/en/publications/oslo-manual-2018_9789264304604-en/full-report/component-18.html （R2，2026-11-01 WebSearch 核验可达）
3. Indexes and estimation techniques[EB/OL]. OECD Regions and Cities at a Glance 2022. https://doi.org/10.1787/bcf1f6fa-en （R3，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技发展态势/科技发展规划.md》seq 186（excel_row 189）：

> ### 竞争力水平与潜力评估 · 序号 186
> - path: 智能服务集群/科技信息展示系统/科技发展态势/科技发展规划/重点领域规划/竞争力水平与潜力评估
>
> 评估区域科技创新的竞争力水平和潜力情况，用户可查看竞争力指标体系和评估结果，提供与对标区域的对比分析。

《科技信息展示系统和科技专题服务系统.md》:1129：「重点领域规划的具体功能包括区域科技创新空间布局分析、竞争力水平与潜力评估、土地用途与效益分析、科技载体分布展示、产业与领域筛选联动、资源配置优化建议。」；:1135 章节号 1.1.1.1.4.1.9.2.2 同名。

**口径披露**：该叶属《科技发展规划.md》（科技发展规划页），不在派单书指定的三份说明书（《科技全域态势》《技术发展跟踪》《全球创新监测》）之内——三份指定说明书本身未出现该指标名。因 UI 挂载组件恰为科技发展规划页同名功能（`TechDevelopmentPlan.tsx:3015`），本件按需求同名词命中处理（named_in_srs=true，note 双披露），检索与原文均留档。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 竞争力水平与潜力评估 | 科技发展规划.md:125（seq 186）；主文档:1129/1135 | 3（叶名+功能列举+章节号） |
| 同词 | 三份指定说明书 | 0 |
| 竞争力指标体系 | 科技发展规划.md seq 186 功能描述 | 1（未定义维度） |
| 对标区域 | 同上 | 1（未定义对标集） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_TECHTRK_018_out.json`（2026-11-01 实跑：区域统计、城市聚合、机构 Top5、协作量）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（`ads_technology_application_case`=181,735 等同库行数零漂移）。
- Lane 3 探针快照：`_probe_lane3_jiuxin2_out.json`（region/power DESC+COUNT）、`_probe_lane3_jiuxin3_out.json`（区域统计/阶段分布/机构 Top5/区域 Top）、`_probe_lane3_jiuxin4_out.json`（北京样本/区域名 Top15）、`_probe_lane3_jiuxin6_out.json`（协作表 DESC/COUNT/层级非空率/京沪深聚合）、`_probe_lane3_gkx_out.json`（dev/gkx 关键词）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_TECHTRK_018 | 文首 |
| `ui_evidence` | 证据 | TechDevelopmentPlan.tsx:3015/862-876 + plan.js:39 | §1.1/§1.5 |
| `requirement_trace.named_in_srs` | 事实 | **true**（seq 186 跨页同名，note 双披露） | §1.3/附录 A |
| `facts.jiuxin_region_assessment_rows_total` | 计数 | 2,708,162 | §2.1 |
| `facts.jiuxin_region_assessment_locations` | 计数 | 7,816 | §2.1 |
| `facts.jiuxin_regional_potential_score_stats` | 统计 | 0.0/100.0/39.83 | §2.2 |
| `facts.jiuxin_region_key_cities` | 聚合 | 六城均分 | §2.2 |
| `facts.jiuxin_region_stage_code_dist` | 分布 | 三档 | §2.3 |
| `facts.jiuxin_region_coverage_status` | 事实 | PARTIAL_INTERNAL_EVIDENCE | §2.3 |
| `facts.jiuxin_institution_power_rows`+`jiuxin_power_top5` | 计数/榜单 | 64,698；中科院 99.999 | §2.4 |
| `facts.jiuxin_collaboration_yearly_rows`+`…_intl_pair_rows` | 计数 | 14,380,246 / 国际对 | §2.4 |
| `facts.ui_mock_competitiveness_metrics` | mock 登记 | 78.5/88/85/62/82 | §1.1 |
| `derived[0..1]` | 派生 | 48.889888 / 1.834895 | §2.2 |
| `absence_probe` | 负证据 | 4 条 | §3.4 |
| `support_judgment` | 判档 | 部分支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| 多维加权指数 | OECD/JRC（R1） | institution_power 四分项先例；区域待建 | 高（机构）/待建（区域） |
| 区域归属分摊 | Oslo（R2） | region_yearly_metrics 三级 location | 中高 |
| 多层级对标 | OECD 区域统计（R3） | regional_rank+城市梯度；无园区级 | 中 |

### C.2 数据矩阵

| 依赖 | 行数 | 质量 | 缺口 |
|---|---|---|---|
| 区域总分 | 2,708,162 | 全量+证据计数+文本 | 无分项 |
| 机构力量 | 64,698 | 四分项+权重 | 主体是机构 |
| 协作网络 | 14,380,246 | 三级地理 | 需桥接聚合 |
| 园区 location | 0 | — | 粒度未扩 |
| 政策/市场证据 | 0（PARTIAL 标签） | — | 与 014 同根 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1 | 总分卡+潜力卡+市级对标（口径 A） | 无 |
| v2 | 五维分项官方建模 | 甲方定框架+管线重跑 |
| v3 | 园区级对标+证据全覆盖 | 地点扩充+资讯入链 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| regional_rank 语义翻转误用 | **高** | 使用说明写死「技术内区域排名」 |
| NULL 中文名丢 85% 行 | 高 | location_id 口径为主 |
| 头部城市分差过小（首尾 2.37） | 中 | 五维分项增强区分度 |
| 机构→区域分摊规则争议 | 中 | R2 规范显式化 |

### C.5 总判

**部分支持**：需求同名词+总分海量+素材七成在库；降档三因（区域分项未建/园区粒度未扩/证据覆盖部分）修复路径全部在库内或行政性（地点补录）；五维建模是本件乃至本批性价比最高的升档单项。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_TECHTRK_018.py` | 退出码 0，落 `_out.json` |
| 城市聚合 | `facts.jiuxin_region_key_cities` | 六城 46.5–48.9 梯度 |
| 机构 Top5 | `facts.jiuxin_power_top5` | 中科院 99.999227 居首 |
| 京深差 | `derived.jiuxin_beijing_vs_shenzhen_score_gap` | 1.834895 |
| 探针对账 | `_probe_lane3_jiuxin*` 快照 | 行数零漂移 |
| 判档一致 | 产物 `support_judgment` vs 文首 | 均为部分支持 |
| demo 禁引 | 脚本 grep demo_ | 0 命中 |
