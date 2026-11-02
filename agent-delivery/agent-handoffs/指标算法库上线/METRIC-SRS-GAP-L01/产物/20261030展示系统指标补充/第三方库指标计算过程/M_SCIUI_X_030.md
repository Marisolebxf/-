# 成果规模化阶段判定（M_SCIUI_X_030）

> **类型**：无业务逻辑数值类（阶段判定结论）｜ **域**：科技发展态势·科技创新评估·政策优化建议＞规模化｜ **UI 挂载**：科技创新评估页 → 政策优化建议报告区 → 市场化成熟度图（五阶段轴末端「规模化」）
> **数据支持度**：**完全转换支持**｜ **公式定义人**：仿王惠（推测定义，非招标原文闭合口径）｜ **口径归属**：UI 拆件叶（`_phase3_471_export.json` row_01 166），三份需求说明书未出现该指标名
> **复现脚本**：`code/M_SCIUI_X_030.py`｜ **产物**：`code/M_SCIUI_X_030_out.json`
> **四判定摘要**：直接结构 = 否（三源无「成果」粒度规模化结果面）；直接数据 = 否；依赖结构 = 是（久新 `ads_technology_stage_assessment` 20 列 + 阶段维表 8 阶段）；依赖数据 = 是（38,860 行技术节点全量，产业化档 20,816 行）
> **数据源口径**：三源评估——开发库 `gkxlumenx_*`（10.50.11.76:3306）+ 三方库 `gkx`（183.240.141.251:3318 只读）+ 久新库 `jiuxin_warehouse`（47.93.119.170:29030，db `gkx_technology_analysis_dev`，203 张 `ads_*` 只读）；本件主承载在久新。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别（`gkx` / `gkxlumenx_*` / `jiuxin_warehouse`）。

**本件判定：完全转换支持。** 三源均无「科技成果」粒度的规模化判定现成结果面，但久新 `ads_technology_stage_assessment`（38,860 行、20 列、规则证据基线方法在案）+ `ads_technology_transfer_stage` 阶段维表（8 阶段含两级规模化语义：order 7 产业化 / order 8 市场规模化）构成完整的判定承载——结构在、量在、方法语义锚在，现转即得。降档压力不在数据面而在两处语义偏移：对象轴是技术节点（非成果）、语义最贴档 MARKET_SCALE（市场规模化）结果面 0 行（现有数据最高落在 INDUSTRIALIZATION 产业化档）。

### 批次通用纪律摘要（S3-02 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 派生比 `jiuxin_industrialization_share_pct` 分子分母同表同池 |
| B4 | 负结论带探针 | absence_probe 三源逐一留证（§3.3） |
| B5 | 确定性 | 维表按 stage_order 排序；采样解析无集合序依赖 |
| B6 | 闸门自身被闸 | 本批不自跑闸门，由派单方统一跑 |
| B7 | 产物只由脚本产出 | 改脚本→重跑，产物零手改 |
| B8 | 回执不复收 | 派单方硬复验 |
| B9 | 单位/日期陷阱 | 无年份/金额列；快照日期字符串化处理 |
| B10 | 口径裁定保守交付 | 双口径（INDUSTRIALIZATION/MARKET_SCALE 语义映射）+ 升降档触发器写死（§1.6） |
| B11 | 多本账互推 | 38,860 与共享快照 `ads_technology_stage_assessment` 键零漂移 |

### 判档自检三问（本件 = 完全转换支持）

| 问 | 答 | 证据 |
|---|---|---|
| 判定轴存在吗？ | 存在（技术节点粒度） | `jiuxin_stage_assessment_rows=38,860`（facts） |
| 语义锚闭合吗？ | 闭合（两级） | 维表 8 阶段全枚举 `jiuxin_transfer_stage_dimension`（facts） |
| 现转跑通了吗？ | 跑通 | 分布+样本+证据解析三组读数落产物 |

## 摘要

「成果规模化阶段判定」是科技创新评估页政策优化建议报告区的拆件叶：UI 以「研发验证→样机试制→中试验证→应用示范→规模化」五阶段轴展示市场化成熟度，「规模化」为轴末端。三份需求说明书未出现该指标名，需求侧最近语境是 SRS 科技创新评估 seq 158「政策优化建议」（含德尔菲法+系统仿真模型预判段）。数据侧判定：久新 `ads_technology_stage_assessment`（38,860 行技术节点）是三源唯一的阶段判定结果面——阶段维表明文两级规模化语义（产业化「形成供应链和规模生产能力」/市场规模化「实现持续市场采用和规模增长」），结果面现有 INDUSTRIALIZATION 20,816 行 + ENGINEERING 18,044 行；方法为规则证据基线（论文/专利/企业/项目四类计数证据文本在案）。判**完全转换支持**，语义偏移（对象轴=技术节点非成果、MARKET_SCALE 档 0 行）按 B10 双口径交付。

- 需求判定：UI 拆件叶（需求未明列），语义挂 seq 158 政策优化建议语境。
- 复现状态：脚本已跑通；阶段分布/维表枚举/Top3 样本/企业证据直方图四组读数落产物。
- 档位结论：**完全转换支持**（久新结构+量+语义锚齐备，现转即得）。
- 关键事实：语义最贴档 MARKET_SCALE 结果面 0 行——现有数据最高落在 INDUSTRIALIZATION（产业化，20,816 行）。
- 升档/降档触发器：见 §1.6（对象轴换成果粒度或 MARKET_SCALE 档落行为升档压力；甲方要求 TRL 语义则需重建维表）。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技发展态势/科技创新评估/**政策与条件保障力指标展示**/政策优化建议（1.1.1.1.4.2.2 分支语境；SRS seq 158）。UI 挂载点 `TechInnovationEvaluationPage.tsx:2263`：政策优化建议报告区的「市场化成熟度」图，x 轴为 `['研发验证', '样机试制', '中试验证', '应用示范', '规模化']` 五阶段，双系列（技术成熟度折线 + 商业化准备度柱）按 `evaluationScope.volumeScale` 缩放 mock 值（32→84 / 18→78 区间，演示值不参与支持度结论）。「规模化」作为五阶段轴的末端档位，即本件「成果规模化阶段判定」的字面挂载——判定某项成果是否进入大批量应用阶段，对应轴末端读数。

同页 `:2698` 的实施路径文案（「按基础研究、中试验证和规模化应用分阶段推进」）与 `:3852` 政策优化建议报告面板构成语义闭环：阶段判定不是孤立的读数，而是政策建议的分阶段依据。

### 1.2 为什么需要本指标

政策优化建议的前提是知道「成果现在走到哪一步」：研发验证期的成果需要中试平台投入，规模化期的成果需要市场对接与标准支撑——阶段不同，政策动作完全不同。五阶段轴把连续的技术成熟度离散成可决策的档位，规模化档是产业链承接的分水岭：进入该档意味着政策重心从「补短板」转向「促放量」。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**「成果规模化阶段判定」指标名未出现在三份需求真源（科技创新评估.md / 科技指数.md / 主需求文档）；「规模化」三字在 SRS 仅以「规模化应用」「规模化承接」等路径叙述出现（如 seq 158 段的姊妹文案），无判定标准、无证据规则、无阶段划分定义。检索记录见附录 A。

### 1.4 类似指标权威方法可行性分析概要

技术成熟度/规模化阶段判定的国际权威标尺是 **TRL（Technology Readiness Level）**：NASA 1970s 原创、欧盟 Horizon Europe/EIC 采纳为 9 级制（R1），其 TRL 9「实际系统在运行环境中得到验证（关键使能技术场景下为竞争性制造）」即国际口径的「规模化生产」语义。国内官方序列以科技部国家创新调查制度（R2）下的成果转化阶段监测为参照，但无强制国标。方法族对照：

| 方法族 | 判定轴 | 数据要求 | 与本库匹配 |
|---|---|---|---|
| TRL 九级（欧盟 EIC） | 系统验证/竞争性制造 | 工程验证记录 | **无（需项目级验证数据）** |
| 规则证据基线（久新现役） | 论文/专利/企业/项目计数 | 四类证据计数 | **有（结果面 38,860 行）** |
| 德尔菲+系统仿真（SRS seq 158 叙述） | 专家共识+仿真 | 专家打分流程 | 流程型，无库内承载 |

久新 schema（§24.6）明示其方法「不是 TRL、不是大模型结论」，是规则基线——这恰是三源中唯一有数据落地的族。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:2263` — `xAxis: { type: 'category', data: ['研发验证', '样机试制', '中试验证', '应用示范', '规模化'] }`（市场化成熟度图）；`:2698` 实施路径文案；`:3852` 政策优化建议报告面板。
- SRS：`…/科技发展态势/科技创新评估.md` seq 158（excel_row 161）「政策优化建议」——本件父语境；「规模化」字样未独立成叶。原文见附录 A。
- 主需求文档：《科技信息展示系统和科技专题服务系统.md》「成果规模化」检索 0 命中。

### 1.6 推测原意与推测定义

**推测定义（须披露语义映射）**：

- 口径 A（语义最贴）：成果处于市场化规模采用阶段 ⇔ 久新 `stage_code='MARKET_SCALE'`（市场规模化，维表定义「实现持续市场采用和规模增长」）——**结果面 0 行，现不可交付**；
- **口径 B（建议口径，数据可交付）**：成果已形成规模生产能力 ⇔ `stage_code='INDUSTRIALIZATION'`（产业化，维表定义「形成供应链和规模生产能力」）——20,816 行现成，UI 五阶段轴「规模化」档位按此回填并标注「产业化=规模化前档」。

**降档/升档触发器（B10 模板）**：若甲方认定「规模化」必须指市场规模采用（口径 A）→ MARKET_SCALE 档 0 行，降**部分支持**（判定轴结构在、该档数据缺）；若接受口径 B → 维持完全转换支持；若要求 TRL 语义或成果/专利粒度 → 需重建证据链（对象轴+维表都换），维持现档另议。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所属四级功能 | 科技创新评估（SRS seq 139–158） |
| 本件叶 | 规模化（UI 拆件，`_phase3_471_export.json` row_01 166） |
| 父语境叶 | 政策优化建议（seq 158）／市场化成熟度图 |
| 相邻已承接件 | M_SCIUI_TECHTRK_009 领域技术平均成熟度（同用久新 stage 族表） |
| 本批同族件 | M_SCIUI_P7_003/004（同页系统仿真序列） |

与 TECHTRK_009 的分工：009 取「平均成熟度」数值读数，本件取「是否进入规模化档」的判定结论——同一结果面的两种消费方式，本件复用其表探测事实（38,860 行与共享快照零漂移）。

## 二、计算过程

### 2.1 装载与规模校验

经 pymysql 直连久新库（`gkx_technology_analysis_dev`，只读）。主面 `ads_technology_stage_assessment` 38,860 行与共享快照 `code/_snapshots/_shared_probe_s3_01_out.json` 的 `ads_technology_stage_assessment=38,860` 三方对账零漂移（B11）。对象粒度：38,860 个技术节点（`technology_node_id` 全唯一，facts `jiuxin_stage_distinct_nodes`），快照日期 `metrics_as_of_date=2026-10-16`、`data_version=202610290801`、`metric_definition_version=technology_transfer_stage_alignment_v1`。

### 2.2 阶段语义锚：维表八阶段全枚举

`ads_technology_transfer_stage` 按 stage_order 输出 8 阶段（facts `jiuxin_transfer_stage_dimension` 全枚举在案）：1 基础研究 / 2 概念验证 / 3 实验室验证 / 4 中试验证 / 5 工程化 / 6 监管与标准 / **7 产业化（形成供应链和规模生产能力）** / **8 市场规模化（实现持续市场采用和规模增长）**。这张维表是「规模化」语义的两级锚：产业化对应 UI 五阶段轴「应用示范→规模化」的过渡带，市场规模化对应轴末端。维表把国际 TRL 九级的 DEPLOYMENT 段（TRL 7–9，R1）细化为中文政策语境的三档（工程化/监管标准/产业化+市场规模化），语义映射可核。

### 2.3 阶段分布实测

全表 `GROUP BY stage_code` 实测仅两档有行：**INDUSTRIALIZATION 20,816 行（53.5666%）、ENGINEERING 18,044 行（46.4334%）**——技术节点池整体已越过早期阶段（基础研究/概念验证/实验室验证/中试验证 0 行），MARKET_SCALE 亦 0 行。这一分布形态说明该评估流水线只对「已进入工程化之后」的节点做阶段判定（上游节点不进快照），用作规模化判定时须披露「池前截断」性质。

### 2.4 判定方法与证据构成

全表单方法 `RULE_BASED_EVIDENCE_BASELINE`、单置信 `stage_confidence=0.9000`（38,860 行无例外，facts `jiuxin_stage_method_confidence`）。证据构成落在 `current_status_description` 文本（如 Top1 节点「论文=30; 专利=4349; 企业=29; 项目=19」，facts `jiuxin_industrialization_top3_samples`）——规则基线以四类计数（论文/专利/企业/项目）支撑档位结论。对 INDUSTRIALIZATION 前 5,000 行解析「企业=N」证据（facts `jiuxin_industrialization_company_evidence_hist_sample5000`，采样披露）：企业证据非零占比与分桶分布随产物交付，规模化判定的企业侧证据面可直接消费。

```sql
SELECT stage_code, COUNT(*) c FROM ads_technology_stage_assessment
GROUP BY stage_code ORDER BY c DESC;
-- → INDUSTRIALIZATION 20816 / ENGINEERING 18044（其余 6 档 0 行）
```

### 2.5 稳健性与口径敏感性

两个方向敏感性：其一，口径 A/B 之差——若甲方坚持市场规模化语义，可用面直接归零（0 行），本件以口径 B 交付是数据现实所迫而非方法妥协；其二，池前截断——0 行的早期档不代表「无早期技术」，只代表该流水线不评估早期节点，UI 五阶段轴若全档回填需另接早期评估源。

### 2.6 复现代码结果展示

- 代码：`code/M_SCIUI_X_030.py`（入口：pymysql 直连久新只读 + `_gkxdb.py` 走 gkx 探针；零 `demo_*`）；运行 `python3 code/M_SCIUI_X_030.py`。
- 产物：`code/M_SCIUI_X_030_out.json`。正文数字与产物键逐一对应：`jiuxin_stage_assessment_rows=38860`（§2.1）、`jiuxin_stage_code_distribution`（§2.3）、`jiuxin_transfer_stage_dimension` 八项（§2.2）、`jiuxin_stage_method_confidence`（§2.4）、`jiuxin_industrialization_top3_samples` 三项（§2.4）、派生键 `jiuxin_industrialization_share_pct=53.5666`（§2.3，分子 20,816/分母 38,860）。
- 结果解读：判定面=38,860 技术节点×单方法单置信；规模化可交付档=产业化 20,816 行（口径 B）；证据文本四类计数在案可解析。
- 对照需求功能要求的评审：五阶段轴「规模化」档回填——**有条件通过**：口径 B 可供数（产业化 53.5666% 读数 + 节点明细）；未通过点=市场规模化档 0 行、对象轴为技术节点非成果粒度（触发器见 §1.6）。

### 2.7 分步证据对照表

| 步骤 | 证据项 | 产物键 | 数值 |
|---|---|---|---|
| 装载 | 判定面行数 | `jiuxin_stage_assessment_rows` | 38,860 |
| 装载 | 技术节点数 | `jiuxin_stage_distinct_nodes` | 38,860 |
| 语义锚 | 维表阶段枚举 | `jiuxin_transfer_stage_dimension` | 8 阶段（order 1–8） |
| 分布 | 产业化档行数 | `jiuxin_stage_code_distribution.INDUSTRIALIZATION` | 20,816 |
| 分布 | 工程化档行数 | `jiuxin_stage_code_distribution.ENGINEERING` | 18,044 |
| 分布 | 市场规模化档 | `jiuxin_stage_code_distribution`（无键） | 0 |
| 方法 | 单方法单置信 | `jiuxin_stage_method_confidence` | RULE_BASED_EVIDENCE_BASELINE × 0.9000 |
| 证据 | Top1 节点证据文本 | `jiuxin_industrialization_top3_samples[0].evidence_text` | 论文=30; 专利=4349; 企业=29; 项目=19 |
| 派生 | 产业化档占比 | `jiuxin_industrialization_share_pct` | 53.5666%（20,816/38,860） |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 阶段判定结果面 | jiuxin_warehouse | `ads_technology_stage_assessment`（20 列） | 38,860 | 直查 | **有**（对象=技术节点） |
| D2 | 阶段语义维表 | jiuxin_warehouse | `ads_technology_transfer_stage` | 8 行 | 直查 | **有**（两级规模化语义） |
| D3 | 判定证据（企业侧） | jiuxin_warehouse | 同 D1 `current_status_description` | 5,000 行采样解析 | 部分 | 有（文本解析） |
| D4 | 成果粒度对象轴 | 三源 | — | — | **不存在** | 缺（结构级，见 §四） |

`support_judgment="完全转换支持"`，与文首同档（闸 6）。

### 3.2 D1/D2：判定面与语义锚

38,860 行全量+8 阶段维表全枚举已在 §2.1–2.3 展开。这里补一点数据面事实：20 列结构里除判定列外还有 `development_potential_score`（38,860 行全覆盖，G7 探针 38,860/38,860）与 `action_recommendation`——阶段判定可与潜力分、行动建议联读，政策优化建议报告的「诊断→建议」链路在该表内自洽。

### 3.3 D4 的 absence_probe 全记录

否定性证据三件套：**查了什么**——gkx 280 表 `table_name LIKE '%stage%'/'%matur%'/'%scale%'`（命中 1：`dwd_fund_scale_info` 基金规模信息，非阶段判定面）；dev `gkxlumenx_*` 同关键词（命中 `gkxlumenx_ads.chain_stage` 产业链阶段维、`gkxlumenx_cms.cms_kg_stage_def` 科普图谱阶段定义，均非成果规模化结果面）；**条件**——结果面存在性（表名级）；**命中**——三源均无「成果」粒度阶段判定面。四种缺失情形归属：**表不存在**（需建表或引久新面），修复动作=接久新结果面或新建，非补数据。

## 四、数据缺失情况

### 4.1 成果粒度对象轴缺失（结构级，主因）

「成果」（专利/论文/软科学成果等 discrete 成果对象）粒度的阶段判定在三源均无承载（§3.3 探针在案）。久新面对象=技术节点（technology_node_id，为技术图谱聚类节点），一个节点聚合多项成果——从节点判定到单成果判定存在粒度落差。修复路径：其一，接受节点粒度（UI 按领域聚合展示时不敏感）；其二，在节点→专利/论文映射表（久新 `ads_technology_patent`/`ads_technology_paper` 在案）上下钻传播档位，工程量=一次映射查询。

### 4.2 市场规模化档 0 行（数据级）

语义最贴档 MARKET_SCALE 全表 0 行（§2.3）——评估流水线当前只产出工程化/产业化两档。这是「表存在但该枚举 0 行」的数据级缺口：修复动作=上游规则基线扩展（对产业化档节点加市场采用证据规则）后重跑快照，非建表。口径 B（产业化档）先行可解 UI 即期用数。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 口径 B 先行（产业化=规模化前档） | 产品决策 | 本件即期可交付 | 20,816 行现成，UI 标注档位语义 |
| 节点→成果粒度下钻 | 数据工程 | 本件 + TECHTRK 族 | 复用久新 technology_patent/paper 映射表 |
| MARKET_SCALE 规则扩展 | 上游流水线 | 本件升口径 A | 需久新侧评估规则迭代，跨团队 |

## 参考文献

1. Programme finder (1/3) — Understanding Technology Readiness Level (TRL)[EB/OL]. European Innovation Council, European Commission. https://eic.ec.europa.eu/programme-finder-13_en （R1，2026-11-01 WebSearch 核验可达；TRL 9「actual system proven in operational environment (competitive manufacturing in the case of key enabling technologies)」）
2. 科技部、国家统计局联合印发《国家创新调查制度实施办法》[EB/OL]. 中华人民共和国科学技术部. https://www.most.gov.cn/ztzl/qgkjcxdhzkyzn/gcls/kjb/201705/t20170525_132970.html （R2，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技发展态势/科技创新评估.md》seq 158（excel_row 161）——本件父语境：

> ### 政策优化建议 · 序号 158
> #### 需规功能描述
> 基于评估结果，提供政策优化建议，包括政策重点调整、支持力度加强、实施路径优化等方面，用户可查看详细的政策优化建议报告，为政策制定提供参考。
> 为提升创新未来发展方向评估的准确性，该功能还引入了德尔菲法来预判技术趋势。通过召开德尔菲会议，将科学计量和数据挖掘的数据分析结果提供给专家参考，结合专家的经验和专业素养，做出前瞻性判断。最终，在数据和专家评价的基础上，运用系统工程的视角，构建学术及科技创新系统评估模型。该模型综合考虑传统评估模型及德尔菲法评估结构，同时增加环境因素及愿景分析，涵盖政治、社会和经济领域与被评产业或领域的相互影响关系。基于这样的指标体系，可以模拟成系统仿真模型，实现对各种可能的趋势和前景进行预测，并能得到对评估结论更为直观、可视化的效果。

「成果规模化」在 SRS 三份文件与主需求文档均未独立成句（「规模化」仅以「规模化应用/规模化承接」出现在实施路径类文案）。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 成果规模化 / 规模化阶段判定 | 科技创新评估.md / 科技指数.md / 主需求文档 | 0 |
| 规模化 | 科技创新评估.md（UI 语义源） | 仅实施路径文案（如 :2698） |
| 政策优化建议 | 科技创新评估.md | 1（seq 158，父语境） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_X_030_out.json`（2026-11-01 实跑：阶段分布/维表/样本/证据直方图/派生占比）。
- 共享探针：`code/_probe_lane3_s302_out.json`（A 组 stage 族）/ `_probe_lane3_s302_r2_out.json`（A1r/A6/A7/A8）/ `_probe_lane3_s302_r3_out.json`（G6/G7）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（`ads_technology_stage_assessment=38,860` 零漂移）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_X_030 | 文首 |
| `ui_evidence` | 证据 | 2 条组件：行号 | §1.5 |
| `requirement_trace.named_in_srs` | 事实 | **false**（父语境 seq 158） | §1.1/附录 A |
| `requirement_trace.scale_stage_mapping` | 口径 | 两级规模化语义映射 | §1.6/§2.2 |
| `facts.jiuxin_stage_assessment_rows` | 计数 | 38,860 | §2.1 |
| `facts.jiuxin_stage_distinct_nodes` | 计数 | 38,860 | §2.1 |
| `facts.jiuxin_stage_code_distribution` | 分布 | INDUSTRIALIZATION 20,816 / ENGINEERING 18,044 | §2.3 |
| `facts.jiuxin_stage_method_confidence` | 方法 | RULE_BASED_EVIDENCE_BASELINE×0.9000 | §2.4 |
| `facts.jiuxin_transfer_stage_dimension` | 维表 | 8 阶段全枚举 | §2.2 |
| `facts.jiuxin_industrialization_top3_samples` | 样本 | 3 节点含证据文本 | §2.4 |
| `facts.jiuxin_industrialization_company_evidence_hist_sample5000` | 直方图 | 5,000 行采样解析 | §2.4 |
| `derived[0]` | 派生比 | jiuxin_industrialization_share_pct=53.5666 | §2.3 |
| `absence_probe` | 探针 | 三源 3 条 | §3.3 |
| `support_judgment` | 判档 | 完全转换支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表文献/机构 | 判定轴 | 数据要求 | 本库承载 | 贴合度 |
|---|---|---|---|---|---|
| TRL 九级 | NASA/欧盟 EIC（R1） | 系统验证→竞争性制造 | 工程验证记录 | 无 | 高（语义标尺，不可行） |
| 规则证据基线 | 久新现役（schema §24.6） | 论文/专利/企业/项目计数 | 四类证据计数 | **38,860 行现役** | **最高（现役承载）** |
| 德尔菲+系统仿真 | SRS seq 158 叙述 | 专家共识+环境因素 | 专家流程 | 无（流程型） | 中（口径叙事源） |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 覆盖/质量 | 缺口 |
|---|---|---|---|
| stage_assessment | 38,860 | 全节点单方法单置信 | 对象=技术节点非成果 |
| transfer_stage 维表 | 8 行 | 两级规模化语义 | MARKET_SCALE 档 0 行 |
| 证据文本 | 38,860 | 四类计数可解析 | 文本格式非结构化列 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 口径 B：产业化档判定 + 节点明细 + 证据文本 | 无 |
| v2 | 节点→成果粒度下钻 | 映射表查询工程 |
| v3 | 口径 A：MARKET_SCALE 规则扩展 | 久新评估流水线迭代 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 口径 A/B 混用 | **高** | UI 档位标注「产业化=规模化前档」 |
| 池前截断误读 | 中 | 披露早期档 0 行性质 |
| 节点粒度误当成果粒度 | 中 | 对象轴披露随行 |

### C.5 总判

**完全转换支持**：判定面+语义锚+证据链三件齐备，现转即得；两处语义偏移（对象轴/空档）以 B10 双口径+触发器保守交付，不悬空。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_X_030.py` | 退出码 0，落 `_out.json` |
| gkx 入口 | `_gkxdb.py` | demo_* 直接 raise |
| 分布复核 | `GROUP BY stage_code` | 20,816+18,044=38,860 |
| 派生对账 | 20,816/38,860 | 53.5666%（产物 derived[0]） |
| 共享快照对账 | stage 表 38,860 | 零漂移（B11） |
| 判档一致 | MD 文首 vs `support_judgment` | 完全转换支持 |
