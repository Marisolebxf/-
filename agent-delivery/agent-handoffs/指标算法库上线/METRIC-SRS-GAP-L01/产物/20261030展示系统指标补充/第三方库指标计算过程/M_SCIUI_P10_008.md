# M_SCIUI_P10_008 企业满意度（M_IC_SATISFACTION）—— 指标信息 MD

> **类型**：无业务逻辑数值类｜ **域**：孵化载体 New·运行绩效监控·用户评价与满意度报告（`IncubationCarrierNewPage.jsx:1333`）｜ **UI 挂载**：科技信息展示系统 → 创新载体孵化载体 New → 绩效监控 tab「用户评价与满意度报告」大读数+摘要卡（M_IC_SATISFACTION）
> **数据支持度**：**完全不支持**｜ **公式定义人**：无（M_IC_SATISFACTION 为 UI 自设编号；5 分制问卷口径无库内定义）｜ **口径归属**：UI 挂载件（SRS 无同名指标；上位叶=创新载体孵化载体·序号 556「用户评价与满意度报告」）
> **复现脚本**：`code/M_SCIUI_P10_008.py`（薄壳，指向共享探针 `code/_shared_s308_laneb_probe.py`）｜ **产物**：`code/M_SCIUI_P10_008_out.json`
> **铁律：本指标所有信息，均以第二章的“最新指标调研报告”为准。第一章指标信息为历史版本，不用作参考。**
> **四判定摘要**：直接结构=无（三源无问卷评价面）；直接数据=无；依赖结构=无（satisfaction 词族命中全为债券评级/经营状态/模板配置语义污染）；依赖数据=无（评价流零承载，SOFTSCI_012 同根因复判）
> **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源中存在数据量充分的相关表/字段，仅需口径转换/间接计算（无额外数据采集）即可产出本指标 |
| **部分支持** | 三源中存在部分可复用表/字段，**只可计算本指标的部分子项**（或关键维度缺失） |
| **完全不支持** | 三源均无承载，需新建数据链路/外部接入 |

**本件判定：完全不支持。**（评价数据面三源零承载；SOFTSCI_012 同根因复判成立，本件独立留证）。

### 批次通用纪律摘要（S3-08 批共用）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B4 | 负结论带探针 | absence_probe 三源逐一留证 |
| B5 | 列表 sorted() | 污染清单 sorted |
| B6 | 闸门自身被闸 | 不自跑闸门；派单方统一跑 |
| B7 | 产物只由脚本产出 | 薄壳脚本重跑产出 |
| B9 | 单位/日期陷阱 | 5 分制/样本份数单位披露 |
| B10 | ui_demo_fallback 披露 | mock 4.6/386/优劣项披露 |
| 基期三键 | base_years_used/missing/note | 产物全键（全空登记） |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有问卷/评价面吗？ | 无 | satisfaction 词族命中全污染（债券评级/经营状态/模板配置） |
| 有情感面可代理吗？ | 语义不符 | jiuxin 媒体情感评估为人才舆情非在孵企业问卷 |
| 同族先证一致吗？ | 一致 | SOFTSCI_012（满意度分布）同判完全不支持——复判成立 |

## 摘要

「用户评价与满意度报告」是孵化载体 New 页绩效监控 tab 的报告卡（`IncubationCarrierNewPage.jsx:1333`）：左侧 40px 大读数 4.6 分 + 五星 Rate +「样本 386 份 · 满分 5 分」，右侧优势项/改进项 Tag 归纳；页尾摘要卡（`:1505`）以 metricId=M_IC_SATISFACTION 复现该读数。MetricInfo 口径自述「2026 年上半年在孵企业满意度问卷（386 份），满分 5 分；优劣项为文本归纳结果（演示数据）」。数据侧判定：**完全不支持**——企业满意度需「在孵企业→载体」问卷评价面（主体+客体+评分+批次时间），三源零承载：dev 词族命中为 `code_operating_status`（经营状态码表）、`evaluation_template`（评价模板配置 8 行，模板无数据）、政策舆情演示列；gkx 为债券/机构财务评级污染（`dwd_high_tech_industry_bonds` 等 rating 列）；jiuxin 218 表（SHOW TABLES 实数）表名 0 命中，人才媒体情感评估语义不符。SOFTSCI_012（满意度分布，1-5 星制）S3-07 批已证同根因——本件（5 分均分制）复判成立，两件独立留证互为佐证。火炬统计年报的满意度字段属问卷采集面，非库内可算。

- 需求判定：**UI 挂载件**（SRS 无同名；上位叶=序号 556）。
- 复现状态：薄壳已跑通；负结论落产物。
- 档位结论：**完全不支持**（评价流零承载，复判 SOFTSCI_012）。
- 关键事实：mock 口径自述即带 MockBadge——386 份/4.6 分均为演示设定。
- 升档路径：载体服务平台问卷模块接入（评价表四列：企业/载体/评分/批次）→ 完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技成果展示 → 创新载体孵化载体（New 页族：`achievement-preview-new/incubation-carrier-new/`）→ 运行绩效与增长趋势智能监控 tab →「用户评价与满意度报告」卡（`IncubationCarrierNewPage.jsx:1333`）。卡结构：`:1339-1343` 大读数 `operations.satisfaction.score`（4.6）+ `<Rate readonly allowHalf>` 五星 + 样本数 `responses`（386）份·满分 5 分；`:1345-1351` 优势项归纳 4 Tag（绿）/改进建议 3 Tag（橙）；`:1505-1507` 页尾 KpiTile `label=企业满意度 value=4.6 unit=分 metricId=M_IC_SATISFACTION`。mock 源 `mockData.js:828-834`（score 4.6/responses 386/advantages 4 项/improvements 3 项）。

### 1.2 为什么需要本指标

在孵企业满意度是载体服务质量的直接反馈闭环：均分高低与优劣项归纳直接指向服务改进优先级（SRS 556 需规原文「为载体升级服务标准、增强品牌影响力提供数据支撑」）。与 P10_019（服务频率）同 tab 构成「供给侧频率×需求侧评价」运营双读数。

### 1.3 需求文档是否给出定义方法

**三份说明书未给出该指标的计算方法。** M_IC_SATISFACTION 编号未在需求文档出现（UI KpiTile 自设）；上位叶 556 只给功能行为（循环收集评价和评分、归纳优劣项），无均分口径（算术平均 vs 加权）、无量表（5 分制为 mock 自述）、无抽样规则（全量 vs 抽样）。

### 1.4 类似指标权威方法可行性分析概要

权威口径方法族（完整版指向附录 C）：①火炬统计调查制度（在孵企业满意度调查年报字段——采集口径权威锚）；②GB/T 33169-2016 众包/公共服务满意度（Likert 量表均分法）；③NPS 净推荐值（0-10 推荐者-贬损者）。①需问卷系统对接（非库内计算）；②③需原始评分行——三源零承载，权威方法均不可落地。完整版见附录 C。

### 1.5 引用来源

1. 科技部火炬中心. 中国火炬统计年鉴（在孵企业调查表制度）. https://www.chinatorch.gov.cn/
2. GB/T 33169-2016 众包服务满意度测评（Likert 均分口径）. https://openstd.samr.gov.cn/
3. Reichheld F. The One Number You Need to Grow（NPS 口径）. https://hbr.org/2003/12/the-one-number-you-need-to-grow

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：半年期在孵企业对载体的综合满意度均分（5 分制），附优劣项文本归纳。
- **操作化定义（未实现）**：满意度均分 = AVG(评分)（按批次），样本量 = COUNT(问卷)；优劣项 = 评论文本的归纳面（NLP）。
- **降档触发器**：已处最低档。
- **升档触发器**：载体服务平台问卷模块接入（评价表：企业/载体/评分/批次四列）→ 完全转换支持；评价原始行+文本入湖 → 优劣项归纳可做。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技成果展示/创新载体孵化载体.md` |
| 所属四级功能 | 1.1.1.1.4.6 科技成果展示（域）|
| 所属页面 | 创新载体孵化载体 New |
| 本件叶 | 运行绩效监控·用户评价与满意度报告（UI 挂载件；上位叶=序号 556）|
| 相近叶 | 序号 555 服务频率与资源利用统计（P10_019，同 tab）；SOFTSCI_012 满意度分布（旧页同语义件，已判完全不支持）|
| UI 容器 | `IncubationCarrierNewPage.jsx:1333-1353` SectionCard + `:1505` KpiTile |

## 二、计算过程

从缺。本指标需「在孵企业→载体」问卷评价面（评价主体+客体+评分+批次时间），三源探针（附录 B）证明零承载：dev 542 表 satisfaction/survey/rating/feedback/evaluat 词族双扫命中全为语义污染——`gkxlumenx_dim.code_operating_status`（经营状态码表）、`gkxlumenx_topic_enterprise.evaluation_template`（评价模板配置 8 行，仅 indicators_json/weights_json 模板字段无问卷数据行）、`gkxlumenx_ads.svc_org_card` 0 行空壳；gkx 280 表命中列为债券/机构财务评级（`dwd_high_tech_industry_bonds`/`dwd_org_annual_financial_info` 的 rating 族列）；jiuxin 218 表（SHOW TABLES 实数）表名 0 命中，`ads_talent_media_sentiment_assessment` 为人才媒体舆情情感面、`ads_talent_political_assessment_demo` 带 demo 后缀禁引——均非在孵企业问卷。SOFTSCI_012（1-5 星分布制）S3-07 批已证评价流零承载，本件（5 分均分制）复判成立。禁伪公式；mock 4.6/386/优劣项为演示设定（MetricInfo 自述即带 MockBadge，ui_demo_fallback 披露）。复现代码与证据对照见产物 `derived[0]`（负结论 null 登记）。

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 问卷评价面（企业×载体×评分×批次） | dev/gkx/jiuxin | **无表**（词族命中全污染） |
| 评价模板配置 | dev `gkxlumenx_topic_enterprise.evaluation_template` | **语义不符**（8 行模板定义，无评价数据） |
| 服务要素面 | dev `gkxlumenx_ads.svc_org_card` | **0 行空壳** |
| 人才情感面（代理候选） | jiuxin `ads_talent_media_sentiment_assessment` | **语义错位**（媒体舆情非企业问卷） |

### 3.2 现场复核清单

UI 链实读：`IncubationCarrierNewPage.jsx:1333` SectionCard 标题+extra MetricInfo（口径自述）、`:1339-1343` 大读数/Rate/样本、`:1345-1351` 优劣项 Tag、`:1505-1507` KpiTile metricId=M_IC_SATISFACTION；mock 源 `mockData.js:828-834`。三源实连复核（共享探针 `_shared_s308_laneb_probe.py`）：词族命中清单见 absence_probe 三条；`svc_org_card` 0 行、`evaluation_template` 8 行配置逐表定性见 facts。

## 四、数据缺失情况

### 4.1 缺口清单

①问卷评价面无表（主因，需采集系统）；②量表/均分口径未立项（5 分制为 mock 自述）；③优劣项归纳无文本原料；④批次/时间维无承载（满意度趋势不可算）。

### 4.2 修复建议与影响面

短期：卡片维持 mock 并标注演示态（现状即如此）。中期：载体服务平台问卷模块对接（评价表四列入湖）→ 完全转换支持；同时解 SOFTSCI_012（分布制）。远期：评论文本入湖 → 优劣项自动归纳（NLP）。同族联动：SOFTSCI_012 与本件一次接入两件受益；P10_021（用户评价与满意度报告摘要位）三件同根。

### 4.3 影响面

绩效监控 tab 五卡中本卡与 P10_021 摘要位维持 mock；SRS 556「循环收集」承诺整链无数据支撑（采集系统未接入）。

## 参考文献

1. 科技部火炬中心. 中国火炬统计年鉴. https://www.chinatorch.gov.cn/
2. GB/T 33169-2016 众包服务满意度测评. https://openstd.samr.gov.cn/
3. Reichheld F. The One Number You Need to Grow. Harvard Business Review, 2003. https://hbr.org/2003/12/the-one-number-you-need-to-grow

# 附件

## 附录 A 原始需求原文摘录

- SRS《创新载体孵化载体.md》序号 556（excel_row 559，path=…/运行绩效与增长趋势智能监控/用户评价与满意度报告）：「支持循环收集企业用户评价和满意度评分，自动归纳服务优劣项及改进建议，为载体升级服务标准、增强品牌影响力提供数据支撑。」
- 检索记录：`rg M_IC_SATISFACTION|企业满意度` 三份说明书 → 编号 0 命中；功能叶 556 命中（上位覆盖）。
- 实查定位链：清单挂点 IncubationCarrierNewPage.jsx:1333 直核 → :1505 KpiTile metricId → mockData.js:828-834。
- mock 参照：score 4.6 / responses 386 / advantages ['导师辅导响应及时','空间与配套完善','投融资对接高效','政策解读到位'] / improvements 3 项。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_P10_008_out.json`）

metric_id/batch=S3-08/ui_evidence（3 条组件行号）/requirement_trace（named_in_srs=false + SRS 锚 556）/facts（ui_mount/ui_summary_tile/ui_mock_note/dev_satisfaction_word_tables/dev_satisfaction_semantic_note/gkx_satisfaction_column_tables/gkx_satisfaction_semantic_note/jiuxin_satisfaction_tables/jiuxin_satisfaction_note/sibling_verdict/dev_table_total=542/gkx_table_count=280/jiuxin_table_count_live=218）/derived[0]（负结论 null）/absence_probe（三源三条）/support_judgment=完全不支持/notes（5 条）/base_years 三键（全空）/ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：火炬统计调查（在孵企业满意度问卷字段，采集锚）→ GB/T 33169 Likert 均分 → NPS 净推荐。数据矩阵：评价面三源 0；模板配置 8 行无数据；人才情感面语义错位。分期方案：一期问卷系统对接（评价表四列）、二期批次维（趋势）、三期文本归纳（优劣项）。风险登记：rating 词族金融污染（债券/财务评级三种错义）、demo 后缀表禁引、mock 口径自述冒充真实批次。总判：完全不支持（复判 SOFTSCI_012 成立；升档路径=问卷接入一次解三件）。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_P10_008.py` | 退出码 0，落 `_out.json` |
| 共享探针 | `python3 code/_shared_s308_laneb_probe.py` | 快照词族面零漂移 |
| 判档一致 | MD 文首「完全不支持」= out.json `support_judgment` | 一致 |
| 负证据 | absence_probe 三条（含 svc_org_card 0 行/模板 8 行定性） | 逐一可复验 |
| mock 披露 | 4.6/386/优劣项仅 §1.1 语义描述 | 不参与支持度结论 |
