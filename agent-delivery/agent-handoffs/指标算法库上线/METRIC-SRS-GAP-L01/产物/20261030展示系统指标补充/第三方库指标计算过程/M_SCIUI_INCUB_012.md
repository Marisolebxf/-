# M_SCIUI_INCUB_012 在孵企业毕业率 —— 指标信息 MD

> **类型**：无业务逻辑数值类｜ **域**：创新载体孵化载体·匹配对象·毕业率（IncubationCarrierNewPage.jsx:1396 新版+IncubationCarrierPage.jsx:665/:706 旧版）
> **数据支持度**：**部分支持**｜ **UI 挂载**：科技信息展示系统 → 孵化载体(新) → 匹配对象「毕业率」（`IncubationCarrierNewPage.jsx:1396` 新版+`IncubationCarrierPage.jsx:665/:706` 旧版）｜ **公式定义人**：无（指标名三源 0 命中；UI 算式 graduated/(inIncubation+graduated)×100 为口径锚）
> **复现脚本**：`code/M_SCIUI_INCUB_012.py`｜ **产物**：`code/M_SCIUI_INCUB_012_out.json`
> **口径归属**：UI 挂载件，SRS 无同名指标｜ **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估
> **铁律：本指标所有信息，均以第二章的“最新指标调研报告”为准。第一章指标信息为历史版本，不用作参考。**
> **四判定摘要**：直接结构=无；直接数据=无；依赖结构=部分（分母侧 tenant=39 近似独活）；依赖数据=部分（分母近似可算、分子毕业数 null，新旧页口径分裂已登记）

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源中存在数据量充分的相关表/字段，仅需口径转换/间接计算（无额外数据采集）即可产出本指标 |
| **部分支持** | 三源中存在部分可复用表/字段，**只可计算本指标的部分子项**（或关键维度缺失） |
| **完全不支持** | 三源均无承载，需新建数据链路/外部接入 |

**本件判定：部分支持。**（分母侧可近似：tenant=39 在驻；分子侧毕业语义零承载——单一比率缺分子）。

### 批次通用纪律摘要（S3-07 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B） |
| B5 | 列表 sorted() | 比率列表/基期/ctx_refs sorted |
| B7 | 数字-出处核对 | 旧版五载体率 22/25/23/17/18 由 mock 对实算复核；新版区间 0.15-0.38 对 mockData 行号 |
| B10 | ui_demo_fallback 披露 | 双页 mock 披露（含新旧口径形态差） |
| 基期三键 | base_years_used/missing/note | 产物全键 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有现成毕业率结果面吗？ | 无 | 指标面两表 0 行；gkx/jiuxin 词族 0 命中 |
| 分母可算吗？ | 近似可 | carrier_org_rel tenant=39 在驻（SOFTSCI_007 同证） |
| 分子可算吗？ | 不可 | rel_type 域={self,tenant} 无毕业态、end_date 全 NULL、无毕业名单 |

## 摘要

「在孵企业毕业率」有两页三处读数：①新版孵化载体页（achievement-preview-new）载体详情抽屉「毕业率」`(graduateRate×100).toFixed(1)%`（mock 19 载体 0.15-0.38 小数制）+ KPI「平均毕业率」（enterpriseCount 加权，`:392`）；②旧版孵化载体页孵化毕业统计图毕业率折线（`:706-710`，五载体 22%/25%/23%/17%/18%，分母=在孵+已毕业）。数据侧判定：**部分支持**——与 SOFTSCI_007 同数据根因（毕业语义零承载）但本件为 rate 字件独立留证：分母侧可近似（`dim.carrier_org_rel` tenant=39 在驻企业），分子侧零承载（rel_type 域={self,tenant} 无毕业态、end_date 全 NULL、`dwd.enterprise_innovation_carrier`/`ads.carrier_index` 0 行空壳）；分子分母不同源同裂，禁拼半真指标。权威口径：火炬 2019 指标体系孵化效率 2.2（毕业企业数/在孵总数，权重 4 分）、工信部 2025 标准级达标线「上年度至少 10% 在孵企业毕业」——mock 19 载体全部 ≥15% 高于达标线，仅量级参照。

- 需求判定：指标名三份说明书未出现（附录 A）。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技成果展示：
- **新版页**（achievement-preview-new/incubation-carrier-new）：`IncubationCarrierNewPage.jsx:1396` 载体详情抽屉详细资料 Descriptions 行「毕业率」；`:392` KPI avgGraduateRate=Σ(graduateRateᵢ×enterpriseCountᵢ)/ΣenterpriseCount×100（enterpriseCount 加权）；mock 源 `mockData.js`（19 载体，`:48,60,72,84,96,108,120,132,144,156,168,180,192,204,216,228,240,252,264,276,288,300` 行 graduateRate 字段）。
- **旧版页**（achievement-preview/modules/incubation-carrier）：`IncubationCarrierPage.jsx:706-710` 孵化毕业统计图第三系列毕业率折线（round(graduated/(inIncubation+graduated)×100)，右轴 max=100）——与 SOFTSCI_007 同图，本件挂折线系列行。

### 1.2 为什么需要本指标

毕业率是孵化载体产出效率的核心比率：工信部 2025 将 ≥10% 设为标准级孵化器达标线，管理者按载体分解识别低产出载体并驱动动态管理（不合格摘牌机制）。

### 1.3 需求文档是否给出定义方法

三份说明书未出现该指标名（检索记录见附录 A）。**固定句式：三份说明书未给出该指标的计算方法。**

### 1.4 类似指标权威方法可行性分析概要

权威口径方法族（完整版指向附录 C）：①火炬 2019 指标体系孵化效率 2.2：考核期内毕业企业数量 ÷ 在孵企业总数（权重 4 分）；②工信部 2025 管理办法第六条（八）：上年度至少 10% 在孵企业成为毕业企业（达标线）+ 第九条毕业 4 条件；③科技部办法：国家级认定累计毕业 20 家（存量口径）。三口径分母均为**在孵企业总数**；旧版 UI 分母（在孵+已毕业）为期末存量口径变体。

### 1.5 引用来源

1. 工业和信息化部. 科技型企业孵化器管理办法（2025）——第六条（八）10% 达标线、第九条毕业条件. https://www.miit.gov.cn/jgsj/kjs/wjfb/art/2025/art_0f6e1cd393bd40c5b5a09566156a3f34.html
2. 科技部火炬中心. 科技企业孵化器评价指标体系（国科火字〔2019〕239 号）——孵化效率 2.2. http://www.chinatorch.gov.cn/fhq/zcfg/202602/bf58a7e77266425e94fa7cc512518095.shtml
3. 科技部. 科技企业孵化器管理办法——第六条累计毕业 20 家. https://www.ncsti.gov.cn/kcfw/cxfzyjs/sjkjqyfhqrd/zcyj6/202502/t20250213_195496.html

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **推测原意**：单载体年度毕业率（当年毕业企业在孵企业占比）+ 全市加权均值（新版 KPI 按入驻企业数加权）。
- **操作化定义（权威重建式，本件仅分母侧可近似）**：毕业率 = 当年毕业企业数 ÷ 在孵企业总数 × 100%（火炬 2.2）；分母近似 = COUNT(carrier_org_rel WHERE rel_type='tenant' AND end_date IS NULL)。
- **降档触发器**：tenant 在驻若证实为租赁语义非孵化入驻，分母近似作废 → 完全不支持。
- **升档触发器**：rel_type 扩毕业态或毕业名单表落库 → 完全转换支持（分子分母同源即活）。

### 1.7 需求叶定位与相近叶关系

- 本叶：孵化载体（新版）·载体详情/ KPI·毕业率；孵化载体（旧版）·孵化毕业统计·毕业率折线。
- 相近叶：SOFTSCI_007（孵化毕业统计，旧版页同一图的双柱+折线族件——本件挂折线系列，007 挂整图，同根因独立留证）；INCUB_011（成长分，同页画像卡）。

## 二、计算过程

### 2.1 口径裁定（B10 多口径并列）

- **口径A（UI 新版页式）**：各载体毕业率区间呈现（`IncubationCarrierNewPage.jsx:1396`，15%–38% 区间条）。
- **口径B（UI 旧版页式）**：毕业率 = graduated ÷ (inIncubation + graduated) ×100（`IncubationCarrierPage.jsx:665/:706`，mock 22/25/23/17/18）。
- **裁定**：分母侧（在孵近似）同 SOFTSCI_007 口径A可算（tenant=39）；分子（毕业数）零承载判 null——分子分母不同源同裂，禁拼半真指标（分母真 39 + 分子 mock 会产生伪真实率）。

### 2.2 探针与读数实测

分母探针（独立重跑）：`carrier_org_rel` rel_type 域={self:18, tenant:39}，end_date 全 NULL → 在孵(近似)=39。分子负结论探针：毕业词族三源 0 命中；rel_type 无毕业态；两指标面（`dwd.enterprise_innovation_carrier`/`ads.carrier_index`）0 行空壳。

### 2.3 读数落盘与同基核对

derived[0] carrier_graduate_rate=null、derived[1] avg_graduate_rate_weighted=null（负结论 null 登记而非 0 值）；derived[2] mock_reference 双页参照（新版区间 [0.15,0.38]/旧版 [22,25,23,17,18]）作 ui_demo_fallback 披露，不混入真读数。

### 2.4 稳健性与口径敏感性

新旧页口径分裂（区间 vs 百分比）已登记待产品裁定；分母近似上界偏误同 SOFTSCI_007 2.4；毕业态接入后两页口径需分别重算，本件不改判。

### 2.5 基期年份可用性

无年度序列（同 SOFTSCI_007 单时点）；`base_years_used=[]`、missing=全序列、note 详附录 B。

### 2.6 需求符合性预评

新版页区间条与旧版页百分比列均不可切真数（分子缺）；仅分母可核。满足匹配对象列表的静态展示，不满足毕业率监控诉求。

### 2.7 复现代码结果展示

复现入口 `code/M_SCIUI_INCUB_012.py`，产物 `code/M_SCIUI_INCUB_012_out.json`；负结论幂等重跑一致。关键读数键见附录 B 逐键清单。

### 2.8 分步证据对照表

| 步 | MD 论断 | 产物键 |
|---|---|---|
| 1 | 分母在孵近似 39 | derived[0] 关联 facts |
| 2 | 分子毕业数零承载 | absence_probe |
| 3 | 判档 部分支持 | support_judgment |
| 4 | 双页 mock 参照 | derived[2] mock_reference |

## 三、数据支撑情况

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 载体维 | dev `dim.carrier` | **有**（28 行） |
| 分母·在孵企业 | dev `dim.carrier_org_rel` | **近似**（tenant=39） |
| 分子·毕业企业 | dev/gkx/jiuxin | **无表**（无毕业态/名单/迁出时间） |
| 结果面 | dev `dwd.enterprise_innovation_carrier`/`ads.carrier_index` | **0 行空壳** |
| gkx / jiuxin 孵化域 | — | **0 命中**（280/218 表） |

### 3.2 现场复核清单

UI 链实读：新版 `IncubationCarrierNewPage.jsx:1392-1396` 抽屉 Descriptions（graduateRate×100 toFixed(1)）+ `:390-392` KPI 加权式；旧版 `IncubationCarrierPage.jsx:706-710` 折线系列。mock 实读：新版 `mockData.js` 19 载体 graduateRate（0.36/0.33/0.29/0.22/0.27/0.38/0.30/0.31/0.20/0.32/0.34/0.28/0.19/0.37/0.30/0.26/0.29/0.24/0.33/0.18/0.21/0.15 区间 0.15-0.38）；旧版五载体率实算复核 22/25/23/17/18。dev 实连复核（本件脚本）：rel={self:18, tenant:39}、carrier=28 断言通过。

## 四、数据缺失情况

### 4.1 缺口清单

①分子（毕业企业）无表（毕业态/名单/迁出时间三层缺）；②两指标面空壳；③新旧两页口径形态分裂（新版小数制+加权 KPI vs 旧版整数制+期末分母）——接入时需统一；④tenant 在驻≈在孵的近似失真风险（同 SOFTSCI_007）。

### 4.2 修复建议与影响面

短期：`carrier_org_rel` 增毕业语义（rel_type 扩 'graduated' 或 end_date+exit_reason='graduate'）→ 本件与 SOFTSCI_007 双件升完全转换支持。中期：指标面灌火炬年报口径（在孵/毕业双计数）。远期：火炬统计年报接口直连 → 完全直接支持。新版页 KPI「平均毕业率」「势能评分」「入驻企业」三读数联动受益。

### 4.3 影响面

新版页载体详情抽屉毕业率行 + KPI 平均毕业率、旧版页毕业率折线均为 mock 演示态；两页均无后端接口调用。

## 参考文献

1. 工业和信息化部. 科技型企业孵化器管理办法（2025）——10% 达标线+毕业 4 条件. https://www.miit.gov.cn/jgsj/kjs/wjfb/art_2025/art_0f6e1cd393bd40c5b5a09566156a3f34.html
2. 科技部火炬中心. 科技企业孵化器评价指标体系（国科火字〔2019〕239 号）. http://www.chinatorch.gov.cn/fhq/zcfg/202602/bf58a7e77266425e94fa7cc512518095.shtml
3. 科技部. 科技企业孵化器管理办法. https://www.ncsti.gov.cn/kcfw/cxfzyjs/sjkjqyfhqrd/zcyj6/202502/t20250213_195496.html

# 附件

## 附录 A 原始需求原文摘录

- 检索记录：`rg 在孵企业毕业率|毕业率` 三份说明书 + 主需求 → 指标名 0 命中。
- 语义锚：新版页抽屉/KPI 为孵化载体信息展示功能族；旧版页看板描述句同 SOFTSCI_007。
- mock 参照：新版 `mockData.js` 19 载体 graduateRate；旧版 `incubationCarrierMock.js:280-284` 五载体对。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_INCUB_012_out.json`）

facts（ui_mount_drawer/ui_mount_kpi/ui_mount_old_line/ui_mock_new_rates 0.15-0.38/ui_mock_old_rates 22-18/ui_mock_note 口径形态差披露/dev_carrier_rows=28/dev_rel_type_domain self18+tenant39/denominator_note/numerator_note/dev_empty_indicator_tables 两表 0 行/gkx_table_count=280/jiuxin_table_count_live=218/named_in_srs=false/named_note）；derived[0]（carrier_graduate_rate 负结论 null）/derived[1]（avg_graduate_rate_weighted 负结论 null）/derived[2]（mock_reference 双页+权威达标线披露）；absence_probe（三件）；support_judgment=部分支持；base_years 三键（used=[] / missing=2021-2026 / note）；ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：火炬 2.2（毕业数/在孵总数，权重 4 分）→ 工信部 2025（10% 达标线+毕业 4 条件：专精特新或高新/融资>500 万/连续两年营收>1000 万/并购上市）→ 科技部办法（累计毕业 20 家存量口径）。数据矩阵：分母近似有（tenant 39）、分子三层缺（毕业态/名单/迁出时间）、指标面空壳。分期方案：一期 rel 扩毕业语义（与 SOFTSCI_007 双件同升完全转换支持）、二期指标面灌年报口径、三期年报接口直连（完全直接支持）。风险登记：新旧两页口径分裂需统一（小数/整数、加权/简单、期末分母/在孵分母）、tenant 近似失真、半真指标拼接禁令。总判：部分支持（分母侧独活，升档与 007 同路径）。
