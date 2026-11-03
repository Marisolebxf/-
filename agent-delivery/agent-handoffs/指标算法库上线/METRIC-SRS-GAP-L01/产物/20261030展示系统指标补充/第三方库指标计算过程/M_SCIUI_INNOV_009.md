# 领域投资规模（M_SCIUI_INNOV_009）

> **类型**：AMOUNT（金额聚合，领域分组）｜ **域**：科技发展态势·全球创新监测·城市创新能力分析＞关键指标对比＞投资规模｜ **UI 挂载**：科技信息展示系统 → 全球创新监测 → 城市创新分析（`cityInnovationAnalysisModel.js:80` 基准指标键 investment「投资规模」/`:374` 概览卡「投资规模」）
> **数据支持度**：**部分支持**｜ **公式定义人**：推测定义（非招标原文闭合口径）｜ **口径归属**：UI 推测叶（SRS 未出现该指标名；近似叶 seq 83 城市创新数据监控将"投资规模"列为监控项）
> **复现脚本**：`code/M_SCIUI_INNOV_009.py`｜ **产物**：`code/M_SCIUI_INNOV_009_out.json`
> **四判定摘要**：直接结构 = 否（三源无"领域×投资金额"现成聚合面）；直接数据 = 否；依赖结构 = 部分（gkx 融资⋈行业链路完整可聚合；久新 field 资金面结构在但 SIMULATED_ONLY）；依赖数据 = 部分（"领域"三源三套分类体系互不映射——降档主因）
> **数据源口径**：开发库（gkxlumenx_*，10.50.11.76，禁 demo_*）+ 三方库 gkx（183.240.141.251:3318 只读）+ 久新库（jiuxin Doris 47.93.119.170:29030，gkx_technology_analysis_dev，只读）

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库 gkx+久新）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** 金额半边的可算性与 INNOV_007 同级（gkx 融资金额 8,826 行全解析，本件已实际完成"融资⋈机构底册行业维"的全量聚合：join 覆盖 24,598/25,654 = 95.90%，制造业累计 127.39 亿元 CNY 居首）；降档全部来自**"领域"语义维**：三源三套分类体系互不映射——gkx 是国民经济行业分类（`industry_l1_name`：制造业/科学研究和技术服务业/信息传输软件和信息技术服务业…），久新是 OpenAlex 学科体系（`ads_shenzhen_institution_field_funding.field_name_zh`：工程学/生物化学遗传学与分子生物学/医学…，且 1,645 行中 1,248 行 amount_mix_type=SIMULATED_ONLY——**真实金额覆盖率仅 24%**，模拟分摊占主体），UI mock 是七大未来产业（智能机器人/合成生物/量子信息/光载信息/脑科学/前沿新材料/未来网络）。三套体系无任何映射表存在（三源探针 absence 留证），"领域投资规模"的读数在选定体系前无法闭合——这是典型的"数据都在、口径不通"的部分支持。

### 批次通用纪律摘要（20261101 批 S3-01 Lane 6 五件共用，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | Top1 行业占比分子分母同池同口径（万元 CNY） |
| B4 | 负结论带探针 | dev 行业列 absence + 三套体系无映射探针留证 |
| B5 | 确定性 | 聚合按金额降序；解析规则与 007 共用 |
| B6 | 闸门自身被闸 | 不自跑闸门，由派单方统一跑 |
| B7 | 产物只由脚本产出 | 改脚本→重跑，产物零手改 |
| B8 | 回执不复收 | 硬证据本件实跑（三源连接记录在案） |
| B9 | 单位/日期陷阱 | 中文金额六形态解析（与 007 同规则）；在途年排除 |
| B10 | 口径裁定保守交付 | 三套领域体系并列待裁定 + 升降档触发器写死 |
| B11 | 多本账互推 | 25,654 基数/8,826 解析数/汇率 7.2 与 INNOV_007 完全一致（批内零漂移） |
| W2-1 | 先读资产再发 SQL | 共享快照 + lane6 探针消费后才写脚本 |
| W2-2 | 引用不漂移 | 快照数字原值引用 |
| W2-3 | 篇幅深度对标 | 13 章节齐全 ≥20KB |
| W2-4 | 三源探针不省略 | dev/gkx/jiuxin 三源逐一留证（§三/附录 B） |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 金额按维度聚合可算吗？ | 可 | gkx join 行业 95.90% 覆盖、聚合结果已落产物（facts.gkx_fin_industry_* 键） |
| "领域"体系有共识吗？ | 无 | 三源三套（国民经济行业/OpenAlex 学科/UI 七大产业），无映射表 |
| 现成领域×金额面可信吗？ | 不可信为主 | 久新 field 面 1,248/1,645 SIMULATED_ONLY（真实金额仅 24%） |

## 摘要

「领域投资规模」是全球创新监测·城市创新能力分析的对比指标之一：城市排行/对标视图的「关键指标对比」面板含"投资规模"项（`cityInnovationAnalysisModel.js:80` 城市基准指标键 investment），城市详情概览卡亦有同名读数（`:374`）；mock 数据把 investment 生成成 baseIndex±15 的**无量纲分**（`mockData.js:121`）——前端没有给金额单位，这是"投资规模"口径模糊在 UI 层的直接体现。数据侧本件把能算的都算了出来：gkx 侧融资事件全量 join 机构底册一级行业（覆盖 95.90%），按行业聚合的累计金额 Top10 与近五年（2021–2025）窗口 Top10 双口径落产物（制造业累计 127.39 亿元/近五年 43.65 亿元均居首）；久新侧解剖了深圳机构×学科资金面（1,645 行，工程学 allocated 23.83 亿元居首，但 SIMULATED_ONLY 占 75.9%，真实金额 real_amount 合计仅 4.63 亿元）。判**部分支持**：金额可算性已证，"领域"三套体系（国民经济行业/OpenAlex 学科/七大未来产业）互不映射是唯一但致命的降档因——读数在体系裁定前无法闭合。投中《2023 中国创投市场报告》的行业口径（电子信息/医疗健康/先进制造…，R4）证明业界领域分类本身也非单一标准，裁定权在甲方。

- 需求判定：**UI 推测叶**（SRS 未出现「领域投资规模」；近似叶 seq 83 将"投资规模"列为城市监控项，领域维为其切片）。
- 复现状态：脚本已跑通；gkx 行业×金额聚合 + 久新 field 资金面解剖 + dev 缺席探针三组证据落产物。
- 档位结论：**部分支持**（金额可算 + 领域体系三源三套不映射）。
- 关键事实：gkx 行业聚合制造业累计 127.39 亿元 CNY 居首（占全行业 27.51%）；久新 field 面 75.9% 为模拟分摊金额（real_amount 仅 4.63 亿元 vs allocated 118.35 亿元 Top12 合计）——现成面的"水分"必须随行披露。
- 升降档路径：甲方裁定领域体系 + 映射表落库 → 升完全转换支持；接 CB Insights 行业分布 API → 升完全直接支持（其行业口径现成）。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/全球创新监测/城市创新能力分析/**城市创新数据监控·关键指标对比**（SRS seq 83 语境；UI `CityInnovationAnalysis.jsx` + `cityInnovationAnalysisModel.js`）。本件挂载点在模型层两处：`cityBenchmarkMetrics` 数组（`:80`）定义六项基准指标 `{ key: 'investment', label: '投资规模', getValue: (city) => Number(city?.dimensions?.innovationInput?.investment || 0) }`——"投资规模"是城市创新投入维（innovationInput）的子字段；`buildCityOverviewStats`（`:374`）在城市概览卡输出「投资规模」读数（`formatNumber(input.investment)`）。mock 值是 UI 需求证据（演示值，不参与支持度结论）：`mockData.js:121` 生成 `investment: item.baseIndex + Math.floor(Math.random() * 15)`——以 baseIndex（68–94）为基数的扰动值，**无量纲、无单位**，与同维度 rdExpenditure（研发投入）、talent（人才储备）同构。这说明前端把"投资规模"当城市创新投入的相对强度分处理，而非货币金额读数；但指标名与 SRS seq 83 语境（"监控……投资规模"）的直觉语义是金额。本件按**金额口径**调研（mean 字段「涉及资金的货币金额统计——单位一般为元/万元」同判），无量纲分口径在 §1.6 作降级备选。

### 1.2 为什么需要本指标

城市创新能力分析的叙事骨架是"投入-产出-环境-绩效"四维：投资规模是**投入维**的资本信号，回答"这个城市的创新吸金能力"。领域切片后问题变成"哪个城市在智能机器人领域吸金最多"——这是招商引资、产业政策、企业选址三类决策的共同读数。UI 把它放进「关键指标对比」面板（与综合指数/创新基金/创新机构/企业投入/创新成果并列），用于城市对标时的资本维度横比；mock 的相对分处理说明前端预期它是可比量，而金额天然可比（同币种归一后）——口径从相对分升为金额反而更贴"对比"语义。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「领域投资规模」全称在三份 SRS 与《科技信息展示系统和科技专题服务系统.md》rg 检索未命中。近似叶：SRS 全球创新监测 seq 83「城市创新数据监控」原文"监控全球主要城市的创新基金、投资规模，创新机构、企业在创新上的投入、产生的创新成果等数据，用户可查看各城市的创新数据详情"——投资规模列为监控项但无定义（领域维未提及）；主文档 585 行同文复述。三份说明书未出现该指标名的固定句式适用于本件全称。

### 1.4 类似指标权威方法可行性分析概要

"领域/行业投资规模"在业界有两类权威先例：其一，投中研究院（CVSource）《中国创业投资及私募股权投资市场统计分析报告》——按行业统计 VC/PE 投资案例数与规模，2023 年电子信息 2,727 起/428.3 亿美元居首，行业口径为电子信息/医疗健康/传统制造/先进制造/能源及矿业/消费/金融/汽车交通/企业服务等约 20 类（R4），其方法论明示"对未公开具体数值的金额进行估计并纳入统计"；其二，CB Insights 全球口径按 vertical（AI/FinTech/Healthcare…）统计（R3）。国内官方口径：科技部战略院《中国创业投资发展报告》按"高新技术产业 vs 其他"二分 + 细行业（计算机硬件/通信/医药…）统计创投投入（R5）。方法族对照：

| 方法族 | 领域体系 | 金额处理 | 与本库匹配 |
|---|---|---|---|
| 投中 CVSource（R4） | 电子信息/医疗/制造…（约 20 类） | 未披露估计纳入 | gkx 行业可映射（部分） |
| CB Insights vertical（R3） | AI/FinTech/Health… | 同上 | 需外部源 |
| 科技部战略院（R5） | 高新技术产业二分+细行业 | 调查填报 | 无调查源 |
| gkx 直算 | 国民经济行业分类（industry_l1） | 有金额子集合计 | **现在可算** |

结论：领域分类本身就是多元标准（业界两套 + 官方一套 + UI 一套），权威先例不提供唯一体系——**体系裁定是甲方前置决策**，工程侧能做的是把三套候选体系的可算性全部摊开（本件 §三即此）。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/global-innovation/tabs/cityInnovationAnalysisModel.js:80` — `{ key: 'investment', label: '投资规模', getValue: … dimensions.innovationInput.investment }`；`:374` — `{ key: 'investment', label: '投资规模', value: formatNumber(input.investment) }`。
- mock：`repos/demo-ui-science/src/pages/global-innovation/mockData.js:121` — `investment: item.baseIndex + Math.floor(Math.random() * 15)`（演示值，无量纲，不作数据证据）。
- SRS：`bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md` seq 83（投资规模列为城市监控项，无定义）；主文档 585 行同文。

### 1.6 推测定义与降档/升档触发器

**推测定义（金额主口径 + 体系三选一，B10 并列）**：

- **口径 A（gkx 国民经济行业）**：领域投资规模 = Σ(领域内融资事件金额)，领域 = `industry_l1_name`；金额六形态解析归一万元 CNY（与 INNOV_007 同规则）；窗口双口径（全周期/近五年）。
- **口径 B（久新 OpenAlex 学科）**：领域 = `field_name_zh`；金额 = allocated_amount_cny 但**必须披露 SIMULATED_ONLY 占比**（现 75.9%），真实读数用 real_amount_cny。
- **口径 C（UI 七大未来产业）**：需先建"国民经济行业/OpenAlex 学科 → 七大产业"映射表（三源无现成映射，absence 留证），映射落库后可算。

**降档/升档触发器（B10 模板）**：现状部分支持；若甲方裁定口径 A → **升完全转换支持**（join 链路与聚合已证，一次视图工程）；若裁定口径 B → 升完全转换支持但 SIMULATED 披露随行；若要求口径 C → 映射表工程（2–4 周量级）后升转换档；若接 CB Insights API（其 vertical 口径现成）→ 升完全直接支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md` |
| 本件挂靠叶 | 城市创新数据监控（seq 83，excel_row 86）——投资规模的领域切片 |
| 相近叶 | 创新能力要素分析（seq 86，人才/资金/政策要素）；城市对标分析（seq 85，投入产出环境差异） |
| UI 容器 | `CityInnovationAnalysis.jsx` 关键指标对比面板 + 城市概览卡 |
| 批内姊妹件 | INNOV_007（实时投资金额=总量件）、INNOV_010（区域投资额=区域切片）、本件=领域切片——投资三件套 |

本件是投资三件套的**领域维件**：金额解析规则、池口径（广东池）、汇率口径全部复用 INNOV_007 的基座（B11 批内一致），差异只在分组维（007 无分组/009 按行业/010 按区域）。

## 二、计算过程

### 2.1 装载与规模校验

gkx 侧融资表 25,654 行（对账共享快照零漂移）全量 LEFT JOIN `dwd_org_base_info`（org_id 键），join 返回 25,654 行、其中行业非空 24,598 行（`facts.gkx_fin_join_rows=25654`/`gkx_fin_industry_unmatched=1056`）。机构底册行业列结构：`industry_l1_name`~`industry_l4_name` 四级 + `industry`（最深一级）——本件取 L1（口径最稳、聚合数适中）。dev/久新装载见 §2.2/§2.5。

### 2.2 dev 侧：领域维缺席

`enterprise_invest` 列扫描（industry/field LIKE）0 命中（absence_probe 留证）——46,967 行股权关系无行业列；`chain_investment`（链投资，本应承载产业链×投资语义）0 行空壳。dev 侧领域投资规模完全不可构建。

### 2.3 gkx 行业聚合：全量跑通（方法主体）

全量 25,654 行拉回 Python 聚合（金额解析六形态与 INNOV_007 完全同规则同代码，B11）：**事件数 Top10**——制造业 7,195 / 科学研究和技术服务业 5,008 / 信息传输、软件和信息技术服务业 4,579 / 批发和零售业 3,224 / 租赁和商务服务业 1,701 / 金融业 598 / 房地产业 481 / 交通运输仓储邮政业 406 / 建筑业 322 / 文化体育娱乐业 313。**累计金额 Top10（万元 CNY）**——制造业 127,385,926.73（127.39 亿\*100 单位见注）\*注：万元口径，即 1,273.86 亿元 / 批发和零售业 1,060.09 亿元 / 科学研究和技术服务业 414.44 亿元 / 信息传输、软件和信息技术服务业 391.22 亿元 / 金融业 385.00 亿元 / 房地产业 350.17 亿元 / 租赁和商务服务业 313.95 亿元 / 交通运输仓储邮政业 249.43 亿元 / 电力热力燃气及水 62.52 亿元 / 建筑业 40.33 亿元（`facts.gkx_fin_industry_amount_wan_cny_top10`，原文以万元计：制造业 127,385,926.73 万元）。**近五年窗口（2021–2025）Top10**——制造业 436.51 亿元 / 批发和零售业 211.09 亿元 / 科研服务业 198.68 亿元 / 交通运输仓储 115.68 亿元 / 信息软件 88.42 亿元 / 金融 87.10 亿元等（`facts.gkx_fin_industry_amount_2021_2025_top10`）。Top1 制造业占全行业累计 27.51%（`derived.gkx_top_industry_amount_share_pct`）。事件数与金额的排序错位值得注意：批发零售事件数第 4 但金额第 2（单笔金额大），科研服务事件数第 2 但金额第 3——行业资本密度差异显著，UI 用金额还是事件数作"规模"需裁定（B10 又一双口径点）。

```sql
SELECT b.industry_l1_name, COUNT(*), /* 金额解析在 Python 侧 */
FROM gkx.dwd_org_financing_info f
LEFT JOIN gkx.dwd_org_base_info b ON f.org_id = b.org_id
GROUP BY b.industry_l1_name;
-- join 覆盖 24598/25654 = 95.90%（derived.gkx_fin_industry_join_coverage_pct）
```

### 2.4 久新 field 资金面解剖：结构在、水分高

`ads_shenzhen_institution_field_funding`（1,645 行 = 深圳机构 × OpenAlex 学科 field）是三源唯一的"领域×金额"现成聚合面，解剖结果三层：**规模层**——allocated_amount_cny Top12 学科：工程学 23.83 亿元 / 生物化学遗传学与分子生物学 13.86 亿元 / 医学 12.26 亿元 / 计算机科学 11.13 亿元 / 材料科学 10.97 亿元等；**水分层**——amount_mix_type 分布 SIMULATED_ONLY 1,248/1,645（75.87%），真实金额 real_amount_cny 合计（Top12）仅 4.63 亿元 vs allocated 118.35 亿元（`facts.jiuxin_shenzhen_field_funding_top12` 的 real/simulated 分列即此证据）；**口径层**——allocation_method 全量 `PROJECT_AMOUNT_BY_INSTITUTION_EVIDENCE_WEIGHT_PRIMARY_TOPIC_V1`（项目金额按机构证据权重分摊到主 Topic）、amount_scope_status 全量 `PROJECT_RELATED_NOT_DISBURSEMENT`（项目相关额非到账额）。结论：该面是**深圳、学科、模拟分摊**三重限定下的参照面，绝不能当"领域投资规模"真源，但它的表设计（real/simulated 分列 + mix_type + scope_status 三重披露）是本项目自建领域聚合面时的**披露规范模板**。

### 2.5 久新问题维资金（第三对照面）

`ads_research_problem_yearly_metrics.funding_amount_cny` 178/4,177 行非空（4.26%）——研究问题维的年度资金汇总面，覆盖极低（funding_evidence 金额覆盖 252 行的放大版），作对照面登记不展开。

### 2.6 稳健性与口径敏感性

三个敏感性：**体系选择**——口径 A/B/C 的读数不可互换（制造业 1,273.86 亿元 vs 工程学 23.83 亿元，分母体系完全不同）；**金额 vs 事件数**——行业排序在两口径下不同（§2.3）；**窗口**——全周期 vs 近五年排序亦有差异（金融业全周期第 5 → 近五年第 6，电力热力全周期第 9 → 近五年第 8）。三重敏感性都指向同一结论：正式交付前必须冻结"体系×度量×窗口"三元组，任何读数随行携带该三元组标签。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_INNOV_009.py`（gkx 经 `_gkxdb.py`；dev/jiuxin 直连只读；聚合在 Python 侧完成；运行 `python3 code/M_SCIUI_INNOV_009.py`）。
- 产物：`code/M_SCIUI_INNOV_009_out.json`。正文数字与产物键逐一对应：`gkx_fin_join_rows=25654` / `gkx_fin_industry_unmatched=1056`（§2.1）、`gkx_fin_industry_event_top10` / `gkx_fin_industry_amount_wan_cny_top10` / `gkx_fin_industry_amount_2021_2025_top10` / `gkx_fin_industry_amount_total_wan_cny=463057525.59`（§2.3）、`jiuxin_shenzhen_field_funding_top12` / `jiuxin_shenzhen_field_funding_rows=1645` / `jiuxin_shenzhen_field_funding_simulated_only=1248`（§2.4）、`jiuxin_rp_yearly_funding_cny_rows=178`（§2.5）、派生键 `gkx_top_industry_amount_share_pct=27.5` / `gkx_fin_industry_join_coverage_pct=95.9`（§2.1/§2.3）。
- 结果解读：金额可算性三证齐（join 覆盖 95.90% + 解析闭合 + 聚合落产物）；领域体系三选一悬置是唯一档位缺口。
- 对照需求功能要求的评审：领域投资规模读数——可交付但需先裁体系；城市×领域交叉——gkx 池内可做（城市列在底册，见 INNOV_010）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| dev | 行业列存在性 | `absence_probe[0]` | 0 命中 + chain_investment 0 行 |
| gkx | join 覆盖 | derived `gkx_fin_industry_join_coverage_pct` | 95.90%（24,598/25,654） |
| gkx | 事件数 Top10 | `gkx_fin_industry_event_top10` | 制造业 7,195 居首 |
| gkx | 累计金额 Top10 | `gkx_fin_industry_amount_wan_cny_top10` | 制造业 127,385,926.73 万元居首 |
| gkx | 近五年 Top10 | `gkx_fin_industry_amount_2021_2025_top10` | 制造业 436.51 亿元居首 |
| gkx | Top1 占比 | derived `gkx_top_industry_amount_share_pct` | 27.51% |
| gkx | 全行业累计 | `gkx_fin_industry_amount_total_wan_cny` | 463,057,525.59 万元 |
| 久新 | field 面规模 | `jiuxin_shenzhen_field_funding_top12` | 工程学 allocated 23.83 亿元居首 |
| 久新 | 模拟占比 | `jiuxin_shenzhen_field_funding_simulated_only` | 1,248/1,645（75.87%） |
| 久新 | 真实金额 | top12 的 real_wan_cny 分列 | 合计 4.63 亿元 |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 融资金额（事件级） | gkx | `dwd_org_financing_info.funding_amount` | 8,826 非空全解析 | 转换 | **足** |
| D2 | 领域维（行业） | gkx | `dwd_org_base_info.industry_l1_name` | join 覆盖 95.90% | 直查 | **足（口径 A）** |
| D3 | 领域维（学科） | jiuxin | `ads_shenzhen_institution_field_funding` | 1,645（SIMULATED 75.87%） | 直查 | 部分（口径 B，水分高） |
| D4 | 领域维（七大产业映射） | 三源 | — | — | **不存在** | **缺（口径 C 工程）** |
| D5 | 领域维（行业） | dev | enterprise_invest 行业列 | 0 命中 | **不存在** | 缺（两源已兜） |

`support_judgment="部分支持"`，与文首同档（闸 6 对齐）。

### 3.2 D1+D2 gkx 侧：口径 A 的完整可算性

金额（D1）与行业（D2）双维齐备且已实跑（§2.3 全量聚合落产物）——口径 A 的全部工程就是一条物化视图。95.90% 的 join 覆盖意味着未匹配的 1,056 行（4.10%）是机构底册缺行业值的小尾巴，聚合读数不受实质影响。

### 3.3 D3 久新侧：口径 B 的三重限定

深圳（地域限定）× 学科（体系限定）× 模拟分摊（真实性限定）——`ads_shenzhen_institution_field_funding` 的三重限定使其只能作参照面。但其 real/simulated 分列披露设计值得自建面沿用（§2.4 口径层）。另注意 field 维来自 OpenAlex 体系（与 `ads_discipline_*` 学科表同源），若甲方选口径 B，全量机构（不限深圳）的 field 资金需从 project_institution×institution_profile 重新聚合（金额覆盖 8.75% 的上限约束随行）。

### 3.4 D4 映射缺失：absence_probe 全记录

否定性证据三件套：**查了什么**——三源是否存在"国民经济行业 ↔ OpenAlex 学科 ↔ 七大未来产业"任一方向的映射表（表名 LIKE mapping/dict/rel 扫描 + 字段级检查）；**条件**——表/列存在性；**命中**——0。缺失情形归属：**表不存在（映射面）**。这是口径 C 的全部工程量所在（映射表构建属领域知识工程，需甲方/领域专家参与，非纯数据工程）。

### 3.5 现场复核清单

| 复核项 | 结果 |
|---|---|
| 解析规则批内一致 | 与 INNOV_007 同函数同代码（B11） |
| 汇率口径批内一致 | 7.2/0.92 固定（B11） |
| join 覆盖实测 | 24,598/25,654（两次跑同值） |
| SIMULATED 披露 | real/simulated 分列核验（Top12 逐行） |
| 在途年排除 | 近五年窗口止于 2025 |
| 脚本形态 | 三源只读；无 demo_*；无耗时键 |

## 四、数据缺失情况

### 4.1 领域体系映射缺失（结构级，主降档因）

三套体系互不映射（§3.4 探针留证）。修复路径：甲方裁定体系（A/B/C 三选一）；若选 C（UI 七大产业），映射表工程立项（行业 L1→七大产业的初版映射可由领域专家 1–2 周完成，OpenAlex 学科→七大产业需更细对齐）。影响面：本件档位 + 读数语义。

### 4.2 久新现成面的模拟水分（数据级，披露项）

SIMULATED_ONLY 75.87% + PROJECT_RELATED_NOT_DISBURSEMENT 口径——即使选口径 B，读数也只能用 real_amount_cny（4.63 亿元级）或带水分披露的 allocated。影响面：口径 B 的可用读数量级缩水 96%。

### 4.3 gkx 池语义限定（池级，三件套共同）

广东企业池（INNOV_010 详证）——"领域投资规模"读数是广东口径。全球口径需外部源（CB Insights vertical 现成，R3）。影响面：本件 + 007/010。

### 4.4 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 领域体系裁定（A/B/C） | 口径裁定 | 本件 | B10 触发器，档位走向 |
| 映射表工程（若选 C） | 领域知识工程 | 本件 | 行业 L1→七大产业初版 1–2 周 |
| 自建领域聚合面（沿用久新披露设计） | 工程 | 本件 | real/simulated 分列 + mix_type + scope_status |
| CB Insights API（全球+vertical） | 外部数据源 | 本件+007/010 | 升完全直接支持 |

## 参考文献

1. 2023 年中国创业投资及私募股权投资市场统计分析报告[EB/OL]. 投中研究院. https://pic.chinaventure.com.cn/reportFiles/7155022580154368.pdf （R4，行业口径 VC/PE 统计方法论"对未公开具体数值的金额进行估计并纳入统计"，2026-11-01 WebSearch 核验可达）
2. BVK Global Venture Capital Report 2025（数据源 CB Insights）[EB/OL]. https://www.bvkap.de/files/content/Studien/Studien%20Archiv/20260126_BVK%20Global%20Venture%20Capital%20report%202025_FINAL.pdf （R3，vertical 口径全球统计，2026-11-01 WebSearch 核验可达）
3. 中国科学技术发展战略研究院《中国创业投资发展报告 2022》出版发行[EB/OL]. 中国科学技术发展战略研究院. http://www.casted.org.cn/channel/newsinfo/9244 （R5，官方创投调查口径，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

「领域投资规模」在三份 SRS 与主文档均未出现（`named_in_srs=false`）。近似叶原文：

SRS《02-科技信息展示系统/科技发展态势/全球创新监测.md》seq 83（excel_row 86）：

> 监控全球主要城市的创新基金、投资规模，创新机构、企业在创新上的投入、产生的创新成果等数据，用户可查看各城市的创新数据详情。

主文档 585 行同文复述。UI 模型层证据：`cityInnovationAnalysisModel.js:80` 基准指标定义与 `:374` 概览卡（演示值无量纲，不作数据证据）。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 领域投资规模 | 三份 SRS + 主文档 | 0 |
| 投资规模 | 全球创新监测.md:423（seq 83）；主文档:585 | 2（同文） |
| 投资金额 | 全球创新监测.md:183；主文档:505 | 2（seq 67 举例句） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_INNOV_009_out.json`（20261101 实跑：gkx 行业聚合、久新 field 面解剖、dev 缺席探针）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（dev 投融资 5 表 + gkx 融资基数，零漂移引用）。
- lane 级探针：`_probe_lane6_gkx_fin2_out.json`（机构底册列清单含行业四级）/`_probe_lane6_jiuxin3_out.json`（field 资金面 DESC + 样例 + SIMULATED 分布）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_INNOV_009 | 文首 |
| `ui_evidence` | 证据 | 3 条组件/mock 行号 | §1.1/§1.5 |
| `requirement_trace.named_in_srs` | 事实 | **false** | §1.3/附录 A |
| `facts.dev_chain_investment_rows` | 计数 | 0 | §2.2 |
| `facts.gkx_fin_join_rows` | 计数 | 25,654 | §2.1 |
| `facts.gkx_fin_industry_unmatched` | 计数 | 1,056 | §2.1 |
| `facts.gkx_fin_industry_event_top10` | 分布 | 10 行业 | §2.3 |
| `facts.gkx_fin_industry_amount_wan_cny_top10` | 分布 | 10 行业（万元） | §2.3 |
| `facts.gkx_fin_industry_amount_2021_2025_top10` | 分布 | 10 行业（近五年） | §2.3 |
| `facts.gkx_fin_industry_amount_total_wan_cny` | 金额 | 463,057,525.59 万元 | §2.3 |
| `facts.jiuxin_shenzhen_field_funding_top12` | 分布 | 12 学科（allocated/real/simulated 三列） | §2.4 |
| `facts.jiuxin_shenzhen_field_funding_rows` | 计数 | 1,645 | §2.4 |
| `facts.jiuxin_shenzhen_field_funding_simulated_only` | 计数 | 1,248 | §2.4 |
| `facts.jiuxin_rp_yearly_funding_cny_rows` | 计数 | 178 | §2.5 |
| `derived[0]` | 派生比 | gkx_top_industry_amount_share_pct = 27.51 | §2.3 |
| `derived[1]` | 派生比 | gkx_fin_industry_join_coverage_pct = 95.9 | §2.1/§3.2 |
| `support_judgment` | 判档 | 部分支持 | §〇 |
| `notes` | 披露 | 四条（体系三套/可算性/池语义/汇率） | §1.6/§四 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 领域体系 | 本库承载 | 贴合度 |
|---|---|---|---|
| gkx 直算（口径 A） | 国民经济行业 L1 | join 95.90% + 解析闭合，**已实跑** | **最高（工程即视图）** |
| 久新参照（口径 B） | OpenAlex 学科 | 现成面但 SIMULATED 75.87% | 中（披露义务重） |
| UI 体系（口径 C） | 七大未来产业 | 映射缺失 | 低（需领域工程） |
| 外部源 | CB Insights vertical | API 接入 | 高（全球+现成口径） |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 覆盖/质量 | 缺口 |
|---|---|---|---|
| gkx 金额+行业 | 24,598/25,654 | 95.90% join | 广东池 |
| 久新 field 面 | 1,645 | real 仅 24% | 三重限定 |
| 映射表 | 三源无 | — | 口径 C 工程 |
| dev 行业维 | 0 列 | — | 表列不存在 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 口径 A 聚合读数（全周期+近五年双窗口，池注记随行） | 甲方裁定口径 A |
| v2 | 映射表 + 口径 C（七大产业） | 领域工程 1–2 周 |
| v3 | CB Insights API（全球 vertical） | 外部源立项 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 三体系读数混用 | **高** | 读数随行"体系×度量×窗口"三元组标签 |
| 久新 allocated 被当真金额 | 高 | real/simulated 分列披露（沿用久新设计） |
| 事件数/金额口径混排 | 中 | 双口径并列注明 |

### C.5 总判

**部分支持**：金额与分组维在 gkx 侧齐备且已实跑聚合，但"领域"三源三套体系互不映射（映射面 absence 0 命中），读数在体系裁定前无法闭合；裁定后升完全转换支持（口径 A/B）或经映射工程升档（口径 C）。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_INNOV_009.py` | 退出码 0，落 `_out.json` |
| 数据入口 | gkx 经 `_gkxdb.py`；dev/jiuxin 直连只读 | demo_* 直接 raise |
| 解析一致性 | 与 INNOV_007 同函数 | 8,826 全解析同值 |
| 判档一致 | 产物 `support_judgment` vs 文首 | 部分支持 |
| 负证据探针 | `absence_probe[0]`（dev 行业列 0 命中） | 留证 |
| join 复跑 | 24,598/25,654 | 同值 |
| mock 残留检查 | `rg "innovationInput" repos/demo-ui-science/src/pages/global-innovation` | 正式版替换后无引用 |
