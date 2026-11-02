# M_SCIUI_INCUB_011 在孵企业成长分 —— 指标信息 MD

> **类型**：无业务逻辑数值类｜ **域**：创新载体孵化载体·匹配对象·成长分（IncubationCarrierPage.jsx:419/:954/:961）
> **数据支持度**：**完全不支持**｜ **UI 挂载**：科技信息展示系统 → 孵化载体 → 匹配对象列表「成长分」列（`IncubationCarrierPage.jsx:419/:954/:961`）｜ **公式定义人**：无（指标名三源 0 命中；成长分评分模型无定义）
> **复现脚本**：`code/M_SCIUI_INCUB_011.py`｜ **产物**：`code/M_SCIUI_INCUB_011_out.json`
> **口径归属**：UI 挂载件，SRS 无同名指标｜ **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估
> **铁律：本指标所有信息，均以第二章的“最新指标调研报告”为准。第一章指标信息为历史版本，不用作参考。**
> **四判定摘要**：直接结构=无；直接数据=无；依赖结构=无（enterprise_growth_trend 0 行空壳 8 列无评分列，实连核验）；依赖数据=无（成长月度评分序列三源无）

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源中存在数据量充分的相关表/字段，仅需口径转换/间接计算（无额外数据采集）即可产出本指标 |
| **部分支持** | 三源中存在部分可复用表/字段，**只可计算本指标的部分子项**（或关键维度缺失） |
| **完全不支持** | 三源均无承载，需新建数据链路/外部接入 |

**本件判定：完全不支持。**（企业评分事实面零承载；唯一词族命中 `dwd.enterprise_growth_trend` 0 行空壳且列级无评分列）。

### 批次通用纪律摘要（S3-07 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B5 | 列表 sorted() | 污染清单/月序列/基期 sorted |
| B7 | 数字-出处核对 | mock 月序列/画像分均已对 mock 源行号 |
| B10 | ui_demo_fallback 披露 | mock 月序列与画像分披露（hint 自标「模拟评分」） |
| 基期三键 | base_years_used/missing/note | 产物全键 |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有企业评分结果面吗？ | 无 | semantic_hits=0；enterprise_growth_trend 0 行空壳 |
| 词族命中有语义一致的吗？ | 无 | 命中全为产业链/基金/投资增速语义污染 |
| 部分因子可拼评分吗？ | 不可靠 | 专利/融资因子三源也无企业级月度面（SOFTSCI_007/009 已证载体/项目层缺口） |

## 摘要

「在孵企业成长分」是孵化载体页的两处读数：①企业成长画像卡「成长分」（hint 自标**模拟评分**，同卡专利/项目）；②入驻企业成长轨迹区「成长评分趋势」月度折线（y 轴 70-100，markLine 最高/最低）。mock：画像分四企业 91/88/82/76，月序列三企业 85→91/82→88/76→82（2026.01-06）。数据侧判定：**完全不支持**——成长分为平台自设综合评分（成长阶段/融资轮次/专利/项目多因子），需评分事实面（企业×月份×分值）+评分模型，三源零承载：growth 词族命中全为语义污染（产业链竞争力 growth_score/产业周期/投资增速/基金久期 fund_maturity_date）；唯一潜在承载 `gkxlumenx_dwd.enterprise_growth_trend`（8 列）**0 行空壳且列级无 score 列**。业界最接近口径为企业创新积分制（科技部 2022 试点），三源无积分表。

- 需求判定：指标名三份说明书未出现；画像卡 hint「模拟评分」自证演示属性（附录 A）。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技成果展示 → 孵化载体：
- ①企业成长画像卡（`IncubationCarrierPage.jsx:419` SoftEntitySummaryPanel metrics[0] label=成长分 value=growthScore hint=模拟评分）；
- ②成长评分趋势图（`:940-984 buildGrowthScoreTrendOption` 月度折线 + `:1070` SoftChartFrame title=成长评分趋势 badge=月度变化，入驻企业成长轨迹区，企业 Select 切换）。
mock 源 `incubationCarrierMock.js:317-358`（月序列）/`:374,390,406,422`（画像分）。

### 1.2 为什么需要本指标

成长分是载体孵化服务的产出效率读数：在孵企业综合成长评分的月度变化反映载体培育效果，管理者按企业分解定位高潜企业与培育短板（看板描述「追踪企业融资轮次和成长评分变化趋势」）。

### 1.3 需求文档是否给出定义方法

三份说明书未出现该指标名（检索记录见附录 A）。**固定句式：三份说明书未给出该指标的计算方法。**（UI hint「模拟评分」自证演示属性。）

### 1.4 类似指标权威方法可行性分析概要

权威口径方法族（完整版指向附录 C）：①**企业创新积分制**（科技部 2022 试点，国科发政〔2022〕226 号）：研发投入/知识产权/成长指标（营收/人员增速）加权积分——最接近口径；②火炬统计年报：载体级统计无企业评分；③投后管理 PSF 评分（投资机构自设）：融资里程碑/营收/团队。成长分属平台自设运营指标，无国标强制口径。

### 1.5 引用来源

1. 科技部办公厅. 关于做好企业创新积分制相关工作的通知（国科发政〔2022〕226 号）. https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2022/202211/t20221109_182768.html
2. 科技部火炬中心. 中国高新技术企业与孵化器统计调查制度. https://www.chinatorch.gov.cn/tjzl/tjzd/index.html
3. 国家税务总局. 研发费用加计扣除政策（积分制研发投入因子口径）. https://www.chinatax.gov.cn/chinatax/n810341/n810755/c5171316/content.html

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：在孵企业综合成长评分（0/70-100 制），多因子加权（成长阶段+融资轮次+专利+项目），月度刷新。
- **操作化定义（权威重建式，本件未实现）**：成长分 = w₁×创新因子（专利/研发）+w₂×成长因子（营收/人员增速）+w₃×融资因子（轮次/金额）+w₄×阶段因子，按月计算（参照积分制权重框架）。
- **降档触发器**：已处最低档。
- **升档触发器**：企业创新积分制数据入湖（企业×月×分值）或 `dwd.enterprise_growth_trend` 灌数并扩评分列 → 完全转换支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：孵化载体·企业成长画像/成长轨迹·成长分（评分+月度趋势）。
- 相近叶：SOFTSCI_007（孵化毕业统计，同页部分支持件）/SOFTSCI_012（满意度分布，同看板）；融资历程图（同区相邻图，轮次金额趋势，另 mock 面无独立件）；INCUB_015（供需匹配率）修复建议已引本件为联动受益件。

## 二、计算过程

从缺。本指标需评分事实面（企业×月份×分值）+评分模型权重，三源探针（附录 B）证明零承载：growth 词族命中全为语义污染——dev 9 处（产业链竞争力 `growth_score`/产业周期/企业统计/机构统计/投资 `amount_growth_rate`+`count_growth_rate`/市场规模各 `growth_rate`）、gkx 4 处（`fund_maturity_date` 基金久期/债市股市 `mkv_growth_rate`）；唯一潜在承载 `gkxlumenx_dwd.enterprise_growth_trend` 实连核验 **0 行空壳、8 列无 score/growth/rating 列**（列清单见产物 facts）。无评分面即无分值，禁伪公式。mock 月序列与画像分为演示量级参照（ui_demo_fallback 披露）。复现代码与证据对照见产物 `derived[0]`（负结论 null 登记）。

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 评分事实面（企业×月×分值） | dev/gkx/jiuxin | **无表**（enterprise_growth_trend 0 行空壳且无评分列） |
| 评分因子·专利（企业级） | dev/gkx/jiuxin | **无在孵企业专利面**（载体层缺口 SOFTSCI_007 已证） |
| 评分因子·融资（企业级轮次） | dev/gkx/jiuxin | **无表**（投融资事件流缺） |
| 评分模型权重 | — | **未定义**（业界无强制口径） |

### 3.2 现场复核清单

UI 链实读（`IncubationCarrierPage.jsx`）：`:419` 画像卡 metrics[0]（value=topEnterprise.growthScore，hint=模拟评分）；`:940-984` buildGrowthScoreTrendOption（x=month，y=score，y 轴 min=70/max=100，markLine max/min）；`:1070` 图框挂载。mock 源 `incubationCarrierMock.js:317-324`（ent-sensor 85/87/88/89/90/91）、`:331-341`（ent-vision 82/84/85/87/88/88）、`:348-355`（ent-biochip 76/78/79/80/81/82）、`:374/390/406/422`（画像分 91/88/82/76）。dev 实连复核（本件脚本）：`enterprise_growth_trend` 8 列 0 行，score_like=[]。

## 四、数据缺失情况

### 4.1 缺口清单

①评分事实面无表（唯一词族命中空壳无评分列）；②企业级专利/融资因子面缺失；③评分模型权重未定义（因子集/量纲/刷新频率）；④月度刷新机制未定（月快照 vs 滚动窗口）。

### 4.2 修复建议与影响面

短期：按企业创新积分制框架建评分表（企业×月×分值+因子分项）落 `gkxlumenx_dwd.enterprise_growth_trend` 扩列 → 本件完全转换支持。中期：因子面接入（专利/融资事件流）→ 评分可解释（因子分项展开）。远期：对接高新区企业创新积分制平台接口 → 完全直接支持。同页 SOFTSCI_007（毕业统计）/INCUB_015（供需匹配）联动受益。

### 4.3 影响面

孵化载体页企业成长画像卡与成长评分趋势图均为 mock 演示态（hint 自标模拟评分）；整页无任何后端接口调用。

## 参考文献

1. 科技部办公厅. 关于做好企业创新积分制相关工作的通知（国科发政〔2022〕226 号）. https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2022/202211/t20221109_182768.html
2. 科技部火炬中心. 中国高新技术企业与孵化器统计调查制度. https://www.chinatorch.gov.cn/tjzl/tjzd/index.html
3. 国家税务总局. 研发费用加计扣除政策（积分制研发因子口径）. https://www.chinatax.gov.cn/chinatax/n810755/c5171316/content.html

# 附件

## 附录 A 原始需求原文摘录

- 检索记录：`rg 成长分|成长评分|成长分趋势` 三份说明书 + 主需求 → 指标名 0 命中。
- 语义锚原文（`IncubationCarrierPage.jsx:419`）：「成长分 … hint: 模拟评分」（UI 自证演示属性）。
- mock 参照（`incubationCarrierMock.js`）：月序列 `:317-324/:331-341/:348-355`；画像分 `:374/390/406/422`。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_INCUB_011_out.json`）

facts（ui_mount_card/ui_mount_trend_fn/ui_mount_trend_frame/ui_mock_monthly 三企业 6 点/ui_mock_scores 四企业/ui_mock_note/dev_table_total=542/dev_enterprise_growth_trend 列清单+0 行/dev_egt_score_like_columns=[]/dev_growth_word_polluted_hits 6 条 sorted/gkx_table_count=280/gkx_growth_word_polluted_hits 3 条 sorted/jiuxin_table_count_live=218/named_in_srs=false/named_note）；derived[0]（incubating_enterprise_growth_score 负结论 null 登记）；absence_probe（三件 semantic_hits=0）；support_judgment=完全不支持；base_years 三键（used=[] / missing=2021-2026 / note）；ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：企业创新积分制（科技部 2022 试点，三因子加权——最接近口径）→ 火炬统计年报（载体级无企业评分）→ 投后 PSF 评分（机构自设）。数据矩阵：评分面三源 0 命中（唯一词族命中 enterprise_growth_trend 0 行空壳 8 列无评分列）；因子面（专利/融资企业级）同缺。分期方案：一期积分制评分表落库（完全转换支持）、二期因子事件流（评分可解释）、三期积分制平台对接（完全直接支持）。风险登记：权重口径无国标（需专家裁定）、月度刷新机制、mock 分值区间（70-100）与积分制百分位口径差异。总判：完全不支持（升档路径明确——评分表落库即活）。
