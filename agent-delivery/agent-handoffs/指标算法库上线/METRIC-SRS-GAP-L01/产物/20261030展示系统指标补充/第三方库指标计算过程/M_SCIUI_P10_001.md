# M_SCIUI_P10_001 专利交易与创新流动 —— 指标信息 MD

> **类型**：简单统计类｜ **域**：科技成果展示·时空演进 New·要素总览 ElementCard·专利交易（`SpaceTimeEvolutionNewPage.jsx:1073`）｜ **UI 挂载**：科技信息展示系统 → 创新载体孵化载体 New（时空演进页）→ 要素卡「专利交易与创新流动」（件）
> **数据支持度**：**部分支持**｜ **公式定义人**：无（指标名三源 0 命中；年度总量口径可由交易表直算，流动路径口径无定义）｜ **口径归属**：UI 挂载件（SRS 无同名指标；上位叶=时空演进展示·序号 505「专利交易与创新流动分析」）
> **复现脚本**：`code/M_SCIUI_P10_001.py`（薄壳，指向共享探针 `code/_shared_s308_laneb_probe.py`）｜ **产物**：`code/M_SCIUI_P10_001_out.json`
> **铁律：本指标所有信息，均以第二章的“最新指标调研报告”为准。第一章指标信息为历史版本，不用作参考。**
> **四判定摘要**：直接结构=无（三源无「交易总量+流动路径」成对面）；直接数据=无；依赖结构=部分（dev/gkx `dwd_patent_transfer` 22,809 行交易事件面可用，路径列从缺）；依赖数据=部分（年度计数可算 2021-2026 六年序列；权利人→地名匹配率 0/200，路径不可算）
> **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源中存在数据量充分的相关表/字段，仅需口径转换/间接计算（无额外数据采集）即可产出本指标 |
| **部分支持** | 三源中存在部分可复用表/字段，**只可计算本指标的部分子项**（或关键维度缺失） |
| **完全不支持** | 三源均无承载，需新建数据链路/外部接入 |

**本件判定：部分支持。** 降档根因是「流动维度从缺」：卡片名为「专利交易与创新流动」双语义——交易侧（年度总量）dev/gkx `dwd_patent_transfer` 22,809 行已证可直算（本批独立复核，与派单一致）；流动侧（跨区域路径 from→to）需权利人名称→机构画像地名解析，200 样本精确名/别名匹配 0 命中（jiuxin `ads_institution_profile` 83,745 行，name_zh 仅覆盖 5,180），名称体系不交叠，路径维度无库内构建路径。交易半边可用、流动半边从缺，关键维度缺失判部分支持。

### 批次通用纪律摘要（S3-08 批共用）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 2026 强度=同表同年计数相除（share_basis 注记） |
| B4 | 负结论带探针 | absence_probe 四条（含权利人匹配 0/200 专项） |
| B5 | 确定性 | 年份键 sorted；匹配样本 sorted 前 200 |
| B6 | 闸门自身被闸 | 不自跑闸门；派单方统一跑 |
| B7 | 产物只由脚本产出 | 薄壳脚本重跑产出 |
| B8 | 回执不复收 | 共享快照可重跑复验 |
| B9 | 单位/日期陷阱 | 287 行无年份单列（`dev_no_year_rows`）；日期为 varchar 取前 4 位 |
| B10 | 口径裁定保守交付 | 双口径并列（总量口径 A 可算/路径口径 B 从缺），触发器写死 §1.6 |
| 基期三键 | base_years_used/missing/note | 产物全键 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 判定轴存在吗？ | 部分 | 交易事件面有（22,809 行）；跨区域路径列无 |
| 代理轴可信吗？ | 部分 | 年度计数可算六年序列；路径需名称解析匹配率 0 |
| 子盘能撑多少？ | 半边 | 总量读数可切真（2024=7,711 件）；流动路径全 mock |

## 摘要

「专利交易与创新流动」是时空演进 New 页「全球要素总览」卡组的第三张 ElementCard（`SpaceTimeEvolutionNewPage.jsx:1073`）：stat 显示 `kpis.patents`（件），desc「全球年度专利交易总量」，点击下钻 `ste-b-patent` 分析区块（P10_002 同族件）。mock 侧该值由 26 城 `base.patents` 指数外推求和（`mockData.js:401-407`，纯演示）。数据侧判定：**部分支持**——dev `gkxlumenx_ods.dwd_patent_transfer`（与 gkx 同构同值）22,809 行、18 列、`transfer_effective_date` 覆盖 2021-2026 六年（2021:326/2022:1,670/2023:3,770/2024:7,711/2025:5,799/2026:3,246，另 287 行无年份），年度交易总量一步计数即得；但「创新流动」语义需权利人（`transfer_before`/`transfer_after` JSON）→ 机构画像地名归属构建跨区域路径，实测 200 样本对 jiuxin `ads_institution_profile`（83,745 行）精确名/别名匹配 0 命中——中文注册名体系与 OpenAlex 英文名体系不交叠，路径维度从缺。判部分支持：总量半边可切真、流动半边维持 mock。

- 需求判定：**UI 挂载件**（SRS 无同名；上位叶=序号 505「专利交易与创新流动分析」功能覆盖）。
- 复现状态：薄壳已跑通；年度读数落本件产物 + 共享快照。
- 档位结论：**部分支持**（交易面可算，路径面零承载）。
- 关键事实：22,809 行 / 国别 CN 16,848·AU 5,421·BR 493·CA 43·AT 4——权属变更事件库，非全球交易总盘。
- 升档路径：权利人名称归一（工商库/OpenAlex 别名对齐）→ 路径可算升完全转换支持；接入带买卖方地名的交易台账 → 完全直接支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技成果展示 → 时空演进展示（New 页族：`achievement-preview-new/space-time-evolution-new/`）→「全球要素总览」四联 ElementCard 第三卡「专利交易与创新流动」（`SpaceTimeEvolutionNewPage.jsx:1073`，icon=IconFile，color=#722ED1）。卡组另三卡：学术论文时空动态（论文合计）、科技资金投入（亿美元）、科技人员流动动态（人，P10_022）。每卡 stat 绑 `kpis.*`（`SpaceTimeEvolutionNewPage.jsx:240-241` useMemo 由 `getGlobalTotals(year)` 聚合），onClick 经 `scrollToBlock('ste-b-patent')` 下钻到「专利交易与创新流动分析」区块（`:1153` 起，P10_002）。

mock 数据链：`mockData.js:401-407` `getGlobalTotals` → `aggregateStats(CITY_PROFILES.map(getCityStats))`；`getCityStats`（`:233-243`）按 `yearlyValue(base.patents, growth*0.9, phase+0.8, year)` 逐年外推。即 mock 的「专利交易」是 26 城基准值指数外推的**演示总量**，无任何真实交易语义。

### 1.2 为什么需要本指标

专利交易是创新流动的货币化读数：交易量上行=成果产权流转活跃，管理者以年度总量判断技术要素市场的活跃度（SRS 序号 505 需规描述「支持自动整合专利交易和转让数据……查看科技成果流动路径及高价值专利聚集」——总览卡承载「整合数据」的量化入口，明细区块承载路径与聚集下钻）。

### 1.3 需求文档是否给出定义方法

**三份说明书未给出该指标的计算方法。**「专利交易与创新流动」卡片名未在需求文档出现（检索记录见附录 A）；上位叶 505 只给功能行为（时间区间+区域选择、流动路径查看、报告导出），无年度总量的分母口径（全球/全国/涉深）、事件定义（权属变更 vs 商业化交易）、计量单位裁定。

### 1.4 类似指标权威方法可行性分析概要

权威口径方法族（完整版指向附录 C）：①专利转移/许可统计（国家知识产权局《专利统计年报》：转让/许可合同件数与金额，事件计数口径）；②技术市场成交额（科技部火炬中心全国技术合同登记，合同面非专利面）；③OECD 技术国际转移（Transfers of Technology，跨境许可与转让对）。三族与本库 `dwd_patent_transfer` 的事件计数口径同构（口径①可直接对齐）；「流动路径」侧无权威国标——路径属平台自设可视化语义，需地名归属工程。完整版见附录 C。

### 1.5 引用来源

1. 国家知识产权局. 专利统计年报（专利转让/许可统计口径）. https://www.cnipa.gov.cn/col/col61/
2. 科技部火炬中心. 全国技术合同成交数据（技术市场统计口径）. https://www.chinatorch.gov.cn/
3. OECD. Technology Balance of Payments / Transfers of Technology（国际技术转移口径）. https://www.oecd.org/sti/ind/technology-balance-of-payments.htm

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **口径 A（年度交易总量，已实现）**：年度专利交易量 = COUNT(`dwd_patent_transfer` 中 `transfer_effective_date` 落在该年的行)，按年分组——权属变更事件计数（国知局口径①对齐）。
- **口径 B（创新流动路径，未实现）**：年度流动 = SUM(按 `transfer_before`→`transfer_after` 权利人地名归属构建的 from→to 区域对流量)——需名称→画像匹配，本批已证 0/200。
- **降档触发器**：若 UI 强约束「全球」总盘口径（库 CN/AU/BR/CA/AT 五国非全球盘），总量读数语义降为「在库五国权属变更量」，仍部分支持但须披露总盘错位。
- **升档触发器**：权利人名称归一工程（工商库/别名表对齐画像 83,745 行）→ 路径可算升完全转换支持；接入带买卖双方地名/金额的交易台账 → 完全直接支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技成果展示/科技时空演进展示.md` |
| 所属四级功能 | 1.1.1.1.4.6 科技成果展示（域）|
| 所属页面 | 时空演进 New（创新载体孵化载体 New 页族）|
| 本件叶 | 要素总览卡「专利交易与创新流动」（UI 挂载件；上位叶=序号 505 专利交易与创新流动分析）|
| 相近叶 | 学术论文时空动态 / 科技资金投入（同卡组 mock 同构）；P10_002 分析区块（同根下钻位）|
| UI 容器 | `SpaceTimeEvolutionNewPage.jsx:1060-1080` ElementCard 四联卡 |

## 二、计算过程

### 2.1 口径裁定（B10 多口径并列）

- **口径 A（年度交易总量，已实现）**：COUNT(*) GROUP BY 年份，权属变更事件计数（与国知局年报口径①同构）。
- **口径 B（流动路径，未实现）**：from→to 区域对流量，需权利人名称→地名归属。
- **裁定**：A 结构+数据均足（六年序列），承载卡片 stat 读数；B 前置匹配 0/200 已证不可行，登记为升档路径非本件判档依据。半边可用 → 部分支持。

### 2.2 探针读数实测

```sql
SELECT LEFT(transfer_effective_date,4) y, COUNT(*) n
FROM gkxlumenx_ods.dwd_patent_transfer
GROUP BY LEFT(transfer_effective_date,4) ORDER BY y;
```

实读（dev，gkx 同构同值）：2021=326 / 2022=1,670 / 2023=3,770 / 2024=7,711 / 2025=5,799 / 2026=3,246 / 无年份=287，合计 22,809。国别分布：CN 16,848 / AU 5,421 / BR 493 / CA 43 / AT 4。权利人形态（2024 年 1,000 行样本）：机构形 1,745 / 个人形 426。

### 2.3 读数落盘与同基核对

2026 不完整年强度 = 3,246 / 5,799 × 100 = 56.0%（产物 `derived[1]`，分子分母同表同年计数，B3 同基）。mock 全球总量作 ui_demo_fallback 披露，不混入真读数。

### 2.4 稳健性与口径敏感性

无年份 287 行（1.26%）单列不入序列（B9）；`transfer_effective_date` 为 varchar 取前 4 位，'0' 前缀脏值已隔离；2026 强度 56.0% 提示收录进行中，年度对比须截断标注。若口径 B 未来实现，读数语义将从「事件量」变为「区域对流量」，两口径并列不改本件判档。

### 2.5 基期年份可用性

`base_years_used`=2021-2026 六年；`missing`=2019-2020（序列前无数据）；基期建议 2021（序列首年）；2026 截断标注。note 详附录 B。

### 2.6 需求符合性预评

总览卡 stat 可直切真数（口径 A 六年序列，2024=7,711 件）；「全球年度」desc 与库五国总盘存在口径差须披露（§2.2）；流动语义在卡片层不呈现（路径归 P10_002 区块）。

### 2.7 复现代码结果展示

复现入口 `python3 code/M_SCIUI_P10_001.py`（薄壳：共享快照断言 + 年度序列落盘）；产物 `code/M_SCIUI_P10_001_out.json`；关键读数：`derived[0]` 六年计数、`derived[1]` 2026 强度 56.0%、`derived[2]` 路径负结论 null 登记。

### 2.8 分步证据对照表

| 步 | MD 论断 | 产物键 |
|---|---|---|
| 1 | 交易面 22,809 行（dev=gkx 同构同值） | facts.dev_rows / facts.gkx_rows |
| 2 | 六年序列 326→3,246 | derived[0] |
| 3 | 无年份 287 行 | facts.dev_no_year_rows |
| 4 | 国别五国盘 CN 16,848 | facts.dev_country_dist |
| 5 | 2026 强度 56.0%（同基） | derived[1] |
| 6 | 权利人匹配 0/200 | absence_probe[3] |
| 7 | 判档 部分支持 | support_judgment |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 交易事件（专利权属变更） | dev `gkxlumenx_ods.dwd_patent_transfer` / gkx 同构 | **有**（22,809 行，18 列） |
| 生效时点（年度轴） | 同表 `transfer_effective_date` | **有**（varchar，287 行无年份） |
| 权利人（前后变更对） | 同表 `transfer_before`/`transfer_after`（JSON） | **有**（名称串，无地名） |
| 权利人地名归属（路径前置） | jiuxin `ads_institution_profile` | **语义不可用**（匹配 0/200） |
| 交易金额/合同面 | dev/gkx/jiuxin | **无表**（技术合同登记未入湖） |

### 3.2 现场复核清单

UI 链实读：`SpaceTimeEvolutionNewPage.jsx:1073` ElementCard stat 绑 `kpis.patents`；`:240-241` useMemo→`getGlobalTotals`；mock 源 `mockData.js:401-407`。三源实连复核（本批共享探针 `_shared_s308_laneb_probe.py`）：dev 542 表 transfer 词族命中 1（dwd_patent_transfer）；gkx 280 表命中 3（另两表语义错位）；jiuxin 218 表（SHOW TABLES 实数）命中 1（阶段码表 8 行）。权利人匹配专项：2024 年 500 行抽 200 名对画像精确名/别名双查 0 命中。

## 四、数据缺失情况

### 4.1 缺口清单

①权利人名称→地名归一字典缺失（路径维主因）；②交易金额/合同语义缺失（只有权属变更事件，无商业化面）；③全球总盘错位（五国盘 vs mock 全球语义）；④287 行无年份（1.26% 弃用）。

### 4.2 修复建议与影响面

短期：卡片 stat 切口径 A 真数（六年序列现成）+ desc 改「在库五国专利权属变更量」。中期：权利人归一（工商库对齐）→ P10_002 路径区块升档。远期：技术合同登记入湖（金额面）→ 交易规模可算。同族联动：P10_002（分析页）同根因独立留证。

### 4.3 影响面

总览四卡中本卡 stat 可切真（口径 A）；流动路径呈现全部维持 mock；P10_002 明细区块同判。

## 参考文献

1. 国家知识产权局. 专利统计年报. https://www.cnipa.gov.cn/col/col61/
2. 科技部火炬中心. 全国技术合同登记数据. https://www.chinatorch.gov.cn/
3. OECD. Technology Balance of Payments. https://www.oecd.org/sti/ind/technology-balance-of-payments.htm

# 附件

## 附录 A 原始需求原文摘录

- 检索记录：`rg 专利交易与创新流动` 三份说明书 → 卡片名 0 命中（清单挂点 SpaceTimeEvolutionNewPage.jsx:1073 实查定位）。
- 上位叶 SRS《科技时空演进展示.md》序号 505（excel_row 508）：「支持自动整合专利交易和转让数据，用户可选择时间区间和区域，查看科技成果流动路径及高价值专利聚集。可视化明细及报告快速导出，为企业和研发团队进行战略布局和技术转化提供支撑。」
- mock 参照：`getGlobalTotals` 外推演示值（无固定数）。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_P10_001_out.json`）

metric_id/batch=S3-08/ui_evidence（2 条组件行号）/requirement_trace（named_in_srs=false + SRS 锚 505）/facts（ui_mount/ui_kpis_source/ui_mock_note/dev_table/dev_rows=22809/gkx_rows/dev_year_counts 六年/dev_no_year_rows=287/dev_columns_18=18 列/dev_country_dist/dev_holder_name_form_sample/jiuxin_transfer_table/dev_table_total=542/gkx_table_count=280/jiuxin_table_count_live=218）/derived[0]（六年计数）/derived[1]（2026 强度 56.0 同基）/derived[2]（路径负结论 null）/absence_probe（4 条含匹配专项）/support_judgment=部分支持/notes（5 条）/base_years 三键/ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：国知局转让/许可事件计数（口径①，本件口径 A 对齐）→ 火炬技术合同登记（合同金额面）→ OECD 技术国际转移（跨境对）。数据矩阵：事件面 22,809 行六年序列可用；路径前置匹配 0/200；金额面零承载。分期方案：一期 stat 切真（口径 A）、二期权利人归一（路径升档）、三期合同台账入湖（金额面）。风险登记：权属变更冒充商业化交易（语义披露）、五国总盘 vs 全球语义（desc 修正）、2026 收录中（截断）。总判：部分支持（半边真半边 mock，升档路径明确）。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_P10_001.py` | 退出码 0，落 `_out.json` |
| 共享探针 | `python3 code/_shared_s308_laneb_probe.py` | 快照三源读数零漂移 |
| 判档一致 | MD 文首「部分支持」= out.json `support_judgment` | 一致 |
| 负证据 | absence_probe 4 条（含匹配 0/200） | 逐一可复验 |
| mock 披露 | mock 外推值仅 §1.1 语义描述 | 不参与支持度结论 |
