# M_SCIUI_SOFTSCI_007 孵化毕业统计 —— 指标信息 MD

> **类型**：无业务逻辑数值类｜ **域**：软科学成果展示·孵化载体页·运行绩效监控看板·孵化毕业统计（IncubationCarrierPage.jsx:1009）
> **数据支持度**：**部分支持**｜ **UI 挂载**：科技信息展示系统 → 孵化载体 → 运行绩效监控看板「孵化毕业统计」存量对照图（`IncubationCarrierPage.jsx:1009`）｜ **公式定义人**：无（指标名三源 0 命中；火炬 2.2 口径「毕业企业数/在孵企业总数」为语义锚）
> **复现脚本**：`code/M_SCIUI_SOFTSCI_007.py`｜ **产物**：`code/M_SCIUI_SOFTSCI_007_out.json`
> **口径归属**：UI 挂载件（`_phase3_screen_v3.json` kept_items），SRS 无同名指标｜ **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估
> **铁律：本指标所有信息，均以第二章的“最新指标调研报告”为准。第一章指标信息为历史版本，不用作参考。**
> **四判定摘要**：直接结构=无（毕业态面三源无）；直接数据=无；依赖结构=部分（dim.carrier 28 载体+carrier_org_rel tenant 39 在驻近似）；依赖数据=部分（在孵近似可算、毕业柱/毕业率线 null）

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源中存在数据量充分的相关表/字段，仅需口径转换/间接计算（无额外数据采集）即可产出本指标 |
| **部分支持** | 三源中存在部分可复用表/字段，**只可计算本指标的部分子项**（或关键维度缺失） |
| **完全不支持** | 三源均无承载，需新建数据链路/外部接入 |

**本件判定：部分支持。**（dev 载体链路可算「在孵(近似)」柱；「已毕业」柱与「毕业率」线零承载）。

### 批次通用纪律摘要（S3-07 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B5 | 列表 sorted() | rel_type 域/词族表/基期年份均 sorted |
| B7 | 数字-出处核对 | 火炬 2019 权重 4 分、工信部 2025 10%、科技部办法毕业 4 条件均已核对原文（§1.5） |
| B10 | ui_demo_fallback 披露 | mock 五载体与 tenant 近似口径均已披露 |
| 基期三键 | base_years_used/missing/note | 产物全键（附录 B） |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有现成孵化毕业结果面吗？ | 无 | dev 指标面 enterprise_innovation_carrier/carrier_index 均 0 行空壳 |
| 部分子项可算吗？ | 在孵(近似)可算 | dim.carrier(28)+carrier_org_rel tenant=39 在驻关系 |
| 毕业语义有承载吗？ | 无 | rel_type 域={self,tenant}、end_date 全 NULL、无毕业名单表；gkx/jiuxin 词族 0 命中 |

## 摘要

「孵化毕业统计」是孵化载体页运行绩效监控看板的第一张图：按载体维双柱（在孵企业/已毕业）+右轴折线（毕业率）对照，回答「哪些载体孵化产出高」。UI mock 5 载体（在孵 86/112/64/58/72、毕业 24/38/19/12/16，毕业率 22%/25%/23%/17%/18%）。数据侧判定：**部分支持**——dev 载体链路（`dim.carrier` 28 行 + `carrier_org_rel` 57 行）承载载体维与在驻关系（tenant=39 可近似在孵柱），但毕业语义零承载：rel_type 取值域仅 {self, tenant}、end_date 全 NULL、两个指标面表（`dwd.enterprise_innovation_carrier`/`ads.carrier_index`）0 行空壳；gkx 280 表/久新 218 表孵化词族 0 命中。三系列缺二（已毕业柱、毕业率线不可算），判部分支持。权威口径（火炬 2019 指标体系孵化效率 2.2「考核期内毕业企业数量占在孵企业总数的比例」权重 4 分）与 UI 分母（在孵+已毕业）存在口径差。

- 需求判定：指标名三份说明书未出现；语义锚为孵化载体页「运行绩效监控看板」覆盖句（附录 A）。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技成果展示 → 孵化载体（运行绩效监控）→ 图表卡「孵化毕业统计」（`IncubationCarrierPage.jsx:1009` SoftChartFrame，badge「在孵 vs 毕业」）；图表构建 `:657 buildIncubationGraduationOption`：在孵企业(柱,stack)+已毕业(柱,stack)+毕业率(线,右轴 max=100)，毕业率公式 `:710 Math.round(d.graduated/(d.inIncubation+d.graduated)*100)`。mock 源 `incubationCarrierMock.js:279-284`。

### 1.2 为什么需要本指标

毕业率是孵化器绩效评价的核心产出指标：火炬 2019 指标体系将其列入孵化效率（权重 4 分）、工信部 2025 管理办法将「上年度至少 10% 在孵企业成为毕业企业」设为标准级孵化器达标线。管理者需要按载体分解定位低产出载体（主需求「为孵化载体运行绩效评估提供可视化数据支持」语义族）。

### 1.3 需求文档是否给出定义方法

三份说明书未出现该指标名（检索记录见附录 A）。**固定句式：三份说明书未给出该指标的计算方法。**（页首描述「覆盖孵化毕业、专利产出、服务利用与满意度等核心绩效指标」为语义锚。）

### 1.4 类似指标权威方法可行性分析概要

权威口径方法族（完整版指向附录 C）：①火炬 2019《科技企业孵化器评价指标体系》孵化效率 2.2「考核期内毕业企业数量占在孵企业总数的比例」权重 4 分；②工信部 2025《科技型企业孵化器管理办法》第六条（八）达标线「上年度至少 10% 在孵企业成为毕业企业」+ 第九条毕业 4 条件（专精特新/高新、单笔融资>500 万、连续两年营收累计>1000 万、并购/挂牌/上市）；③科技部《科技企业孵化器管理办法》国家级认定「累计毕业企业 20 家以上」。分母均为**在孵企业总数**，与 UI 分母（在孵+已毕业）不同。

### 1.5 引用来源

1. 科技部火炬中心. 科技企业孵化器评价指标体系（国科火字〔2019〕239 号）. http://www.chinatorch.gov.cn/fhq/zcfg/202602/bf58a7e77266425e94fa7cc512518095.shtml
2. 工业和信息化部. 科技型企业孵化器管理办法（2025）. https://www.miit.gov.cn/jgsj/kjs/wjfb/art/2025/art_0f6e1cd393bd40c5b5a09566156a3f34.html
3. 科技部. 科技企业孵化器管理办法（第六条累计毕业 20 家/第九条毕业条件）. https://www.ncsti.gov.cn/kcfw/cxfzyjs/sjkjqyfhqrd/zcyj6/202502/t20250213_195496.html

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：按载体展示期末在孵企业与累计/当期毕业企业存量对照 + 毕业率折线，用于载体间孵化产出横比。
- **操作化定义（权威重建式，本件仅部分可算）**：当期毕业企业数（毕业态判定）÷ 在孵企业总数 ×100%（火炬 2.2 口径）；在孵(近似) = carrier_org_rel 中 rel_type='tenant' 且 end_date IS NULL 的在驻企业数。
- **降档触发器**：carrier_org_rel 的 tenant 关系若被证明为办公租赁而非孵化入驻（近似失真），在孵近似子项作废 → 完全不支持。
- **升档触发器**：dwd.enterprise_innovation_carrier 灌数（含 carrier_type 级在孵名单）或新增毕业态 rel_type/毕业企业名单表 → 完全转换支持。

### 1.7 需求叶定位与相近叶关系

- 本叶：孵化载体·运行绩效监控·孵化毕业统计（存量对照图）。
- 相近叶：INCUB_012（在孵企业毕业率，IncubationCarrierNewPage.jsx:1396 新版页）——同根因不同页挂载，各自独立留证；SOFTSCI_012（满意度分布）同看板第四张图；INCUB_015（供需匹配率）修复建议已引本件为联动受益件。

## 二、计算过程

### 2.1 口径裁定（B10 多口径并列）

- **口径A（火炬 2.2 权威式，本件仅部分可算）**：毕业率 = 当期毕业企业数 ÷ 在孵企业总数 ×100%；在孵(近似) = `carrier_org_rel` 中 rel_type='tenant' 且 end_date IS NULL 的在驻企业数。
- **口径B（UI 构建函数式）**：毕业率 = graduated ÷ (inIncubation + graduated) ×100（`IncubationCarrierPage.jsx:709-711`）——分母含毕业存量，与口径A分母不同源。
- **裁定**：可算子项仅在孵近似（口径A分母侧）；毕业柱/毕业率线两个子项因毕业语义零承载判 null（见 2.2）。

### 2.2 探针与读数实测

```sql
-- 在孵企业数（近似口径：在驻 tenant 关系）
SELECT c.name AS carrier, COUNT(r.id) AS in_incubation_approx
FROM gkxlumenx_dim.carrier c
JOIN gkxlumenx_dim.carrier_org_rel r ON r.carrier_id = c.carrier_id
WHERE r.rel_type = 'tenant' AND r.end_date IS NULL
GROUP BY c.name ORDER BY carrier;
-- 全市合计 39（tenant 39 行 end_date 全 NULL；start_date 均为 2024-01-01）
```

毕业侧负结论探针：rel_type 域={self:18, tenant:39} 无毕业态；end_date 全 NULL；词族扫描（毕业/graduate/graduat*）dev/gkx/jiuxin 三源 0 命中；`dwd.enterprise_innovation_carrier`（8 列）与 `ads.carrier_index`（9 列）均 0 行空壳且列结构无毕业/在孵计数字段。

### 2.3 读数落盘与同基核对

读数=39（tenant 在驻合计，产物 `facts`/`derived[0]`）与 §三 3.2 现场复核、附录 B 逐键清单三处同数；mock 五载体 (86,24)(112,38)(64,19)(58,12)(72,16) 作为 ui_demo_fallback 对照披露，不混入真读数。

### 2.4 稳健性与口径敏感性

- 近似失真方向：tenant 在驻 ⊃ 在孵认定（在孵需注册+入驻协议+科技型属性），39 为上界近似。
- 口径A/B 分母差：B 含毕业存量、A 不含——若接入毕业数据后两口径将给出不同读数，MD 已并列登记不改判。
- 维度窄风险：28 载体全为 university/research 型，mock 为孵化器/加速器/众创空间语义，横比结论受限。

### 2.5 基期年份可用性

序列仅单时点（start_date 均 2024-01-01，无年度序列可构成基期）；`base_years_used=[]`、missing=2013–2023 全序列、note 详见附录 B——接入毕业数据后首个完整考核年为基期。

### 2.6 需求符合性预评

存量对照图中「在孵」柱可切近似真数（39 家按载体分布）；「已毕业」柱与「毕业率」线保持 mock 演示态。满足部分展示需求，不满足毕业绩效监控核心诉求。

### 2.7 复现代码结果展示

复现入口 `code/M_SCIUI_SOFTSCI_007.py`，产物 `code/M_SCIUI_SOFTSCI_007_out.json`；本件重跑断言 rel={self:18, tenant:39} 与首跑一致（幂等）。关键读数键见附录 B 逐键清单。

### 2.8 分步证据对照表

| 步 | MD 论断 | 产物键 |
|---|---|---|
| 1 | 在孵近似合计 39 | facts / derived[0] |
| 2 | 毕业语义零承载（无毕业态/无名单/空壳面） | absence_probe |
| 3 | 判档 部分支持 | support_judgment |
| 4 | 基期单时点、无年度序列 | base_years_used/missing/note |

## 三、数据支撑情况

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 载体维（名称/类型/级别） | dev `dim.carrier` | **有**（28 行：incubator/provincial 10、research/national 8、university/national 10；source=v1_approx） |
| 在孵企业（在驻关系） | dev `dim.carrier_org_rel` | **近似**（tenant=39，end_date 全 NULL，start_date 均 2024-01-01） |
| 毕业企业名单/毕业态 | dev/gkx/jiuxin | **无表**（词族 0 命中 + rel_type 无毕业态） |
| 指标结果面（在孵/毕业计数） | dev `dwd.enterprise_innovation_carrier`/`ads.carrier_index` | **0 行空壳**（结构在、无数据，且列不含计数字段） |
| gkx / jiuxin 孵化域 | — | **0 命中**（280/218 表词族扫描） |

### 3.2 现场复核清单

UI 链实读（`IncubationCarrierPage.jsx`）：`:1009` SoftChartFrame 挂载 → `:657` 构建函数解构 `{carriers, incubationData}` → `:709-711` 毕业率=round(graduated/(inIncubation+graduated)×100)。mock 源 `incubationCarrierMock.js:280-284` 五载体 (86,24)(112,38)(64,19)(58,12)(72,16)。dev 实连复核（本件脚本）：carrier=28 行 9 列、carrier_org_rel=57 行 7 列（id/carrier_id/org_uid/rel_type/start_date/end_date/attribution_coef）、rel_type 域 self:18(open=18)+tenant:39(open=39)。

## 四、数据缺失情况

### 4.1 缺口清单

①毕业企业名单无表（毕业态判定原料缺）；②在驻关系无退出日期（end_date 全 NULL，无法从历史关系推毕业迁出）；③指标面空壳（enterprise_innovation_carrier/carrier_index 0 行）；④在孵认定近似失真风险（tenant 在驻 ≠ 在孵认定：在孵需注册+入驻协议+科技型属性）；⑤维度窄（28 载体为 university/research 型，mock 为孵化器/加速器/众创空间语义）。

### 4.2 修复建议与影响面

短期：在 `carrier_org_rel` 增列毕业语义（rel_type 扩 'graduated' 或 end_date+exit_reason）→ 本件升完全转换支持（毕业柱+毕业率线即活）。中期：`dwd.enterprise_innovation_carrier` 灌入火炬统计年报口径在孵/毕业数 → 结果面直查。远期：对接火炬中心统计调查制度年报接口 → 完全直接支持。同看板 SOFTSCI_012（满意度）、INCUB_011（成长分）、INCUB_012（新版页毕业率）联动受益。

### 4.3 影响面

孵化载体页运行绩效监控看板第一张图三系列中二系列为 mock 演示态；「在孵」柱可切换近似真数（39 家在驻企业按载体分布，载体覆盖窄）。

## 参考文献

1. 科技部火炬中心. 科技企业孵化器评价指标体系（国科火字〔2019〕239 号）——孵化效率 2.2 毕业企业数量占在孵企业总数比例（权重 4 分）. http://www.chinatorch.gov.cn/fhq/zcfg/202602/bf58a7e77266425e94fa7cc512518095.shtml
2. 工业和信息化部. 科技型企业孵化器管理办法（2025）——第六条（八）10% 毕业达标线、第九条毕业 4 条件. https://www.miit.gov.cn/jgsj/kjs/wjfb/art/2025/art_0f6e1cd393bd40c5b5a09566156a3f34.html
3. 科技部. 科技企业孵化器管理办法——第六条累计毕业 20 家、第九条毕业条件. https://www.ncsti.gov.cn/kcfw/cxfzyjs/sjkjqyfhqrd/zcyj6/202502/t20250213_195496.html

# 附件

## 附录 A 原始需求原文摘录

- 检索记录：`rg 孵化毕业|毕业率|毕业统计` 三份说明书 + 主需求 → 指标名 0 命中。
- 语义锚原文（`IncubationCarrierPage.jsx:1004-1006` SoftSectionHeader）：「运行绩效监控看板——覆盖孵化毕业、专利产出、服务利用与满意度等核心绩效指标。」
- mock 参照（`incubationCarrierMock.js:280-284`）：五载体 inIncubation/graduated 对。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_SOFTSCI_007_out.json`）

facts（ui_mount/ui_build_fn/ui_rate_formula/ui_mock_data/ui_mock_note/dev_table_total=542/dev_carrier_tables 四表列清单+行数/dev_dim_carrier_rows=28/dev_dim_carrier_types/dev_carrier_rel_rows=57/dev_carrier_rel_type_domain self:18+tenant:39/dev_graduation_columns_eic=[]/dev_graduation_columns_ci=[]/dev_empty_indicator_tables 两表 0 行/gkx_table_count=280/jiuxin_table_count_live=218/srs_anchor/named_in_srs=false/named_note）；derived[0]（carrier_in_incubation_approx=39，ui_demo_fallback 近似披露）/derived[1]（graduation_counts_and_rate 负结论 null 登记）；absence_probe（三件）；support_judgment=部分支持；base_years 三键（used=[] / missing=2021-2026 / note）；ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：火炬 2019 指标体系（毕业率=考核期毕业数/在孵总数，权重 4 分）→ 工信部 2025（10% 达标线+毕业 4 条件：专精特新或高新/单笔融资>500 万/连续两年营收累计>1000 万/并购挂牌上市）→ 科技部办法（国家级认定累计毕业 20 家）。数据矩阵：载体维+在驻关系有（近似在孵可算），毕业名单/毕业态/结果面三层缺（两指标面 0 行空壳）。分期方案：一期 rel 扩毕业语义（完全转换支持）、二期指标面灌火炬年报口径（结果面直查）、三期年报接口直连（完全直接支持）。风险登记：tenant 在驻≈在孵的近似失真、28 载体维度窄（university/research 型 vs mock 孵化器语义）、end_date 缺失致迁出时间不可考。总判：部分支持（三系列缺二，升档路径明确）。
