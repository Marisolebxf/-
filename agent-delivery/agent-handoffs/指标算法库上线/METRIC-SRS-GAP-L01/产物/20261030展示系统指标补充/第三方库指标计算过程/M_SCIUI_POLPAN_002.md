# 分区/群体对比分析图（M_SCIUI_POLPAN_002）

> **类型**：MULTIVIEW（分组对比图表族）｜ **域**：科技政策跟踪·政策分析评价·政策分析报告可视化呈现｜ **UI 挂载**：科技信息展示系统 → 政策分析评价页 → 分析区「分区/群体对比分析图」Card（`pages/policy-tracking/analysis/RegionGroupCompare.jsx:175`）
> **数据支持度**：**部分支持**｜ **公式定义人**：仿王惠（推测定义，非招标原文闭合口径）｜ **口径归属**：需求明列叶（SRS seq 220 / excel_row 223）
> **复现脚本**：`code/M_SCIUI_POLPAN_002.py`｜ **产物**：`code/M_SCIUI_POLPAN_002_out.json`
> **四判定摘要**：直接结构 = 否（无分区×群体×效果现成结果面）；直接数据 = 否；依赖结构 = 部分（分区/行业/群体三维骨架列在，效果值列全缺）；依赖数据 = 部分（骨架维 100% 可算，效果四指标三源 0 承载）
> **数据源口径**：三源（开发库 live `gkxlumenx_*` + 三方库 gkx + 久新 `jiuxin_warehouse`）均探；`demo_*` 禁引。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：部分支持。** 需求是「批量展示各地区、行业或目标群体间的**政策效果**数据」——x 轴三维（地区/行业/群体）与 y 轴四指标（支持力度/落实率/满意度/创新贡献）的矩阵。实测：x 轴三维在 gkx 政策底表全量可算（province 非空率 100%、行业/群体关键词代理覆盖），**y 轴效果值三源全无**——gkx 33 列无效果值列（effect 类命中仅 implementation_date 实施日期；policy_support 列 20,000 行全为字面 `null`）；dev 政策效果五表 + ads 三表全 0 行；久新政策 evidence 无效果值列且 1,252 行中 96.88% 是 LLM 合成语境。效果维始终缺 → 部分支持。

### 批次通用纪律摘要（S3-02 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除 | 三个派生比分子分母同表同池 |
| B4 | 负结论带探针 | 效果维 absence 三源四件（§3.3） |
| B5 | 确定性 | 关键词计数固定词典序；TOP 排序键固定 |
| B6 | 闸门自身被闸 | 不自跑闸门，派单方统一 |
| B7 | 产物只由脚本产出 | 改脚本→重跑 |
| B8 | 回执不复收 | 硬证据可复验 |
| B9 | 单位/日期陷阱 | 关键词 LIKE 逐条转义；金额不做加总 |
| B10 | 口径裁定保守交付 | 效果代理需甲方确认才升档（触发器在案） |
| B11 | 多本账互推 | 政策 20,000 行/省级分布与 dev ads 面、共享快照零漂移 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| x 轴三维可算吗？ | 可算 | province 100% 非空；行业/群体关键词命中 |
| y 轴效果值有源吗？ | 无 | 三源效果列/表 0 承载（absence 四件） |
| 代理能闭合吗？ | 不能 | 支持力度仅文本存在性，落实率/满意度无任何代理 |

## 摘要

「分区/群体对比分析图」是政策分析报告可视化呈现的首图组件（需求明列叶 seq 220）：柱状+热力双图，地区/行业/群体三 Tab × 支持力度/落实率/满意度/创新贡献四指标，配套资源投向（资金/人才/平台/税收）筛选。骨架侧（x 轴）三源数据充足——gkx 政策底表 20,000 行 province 100% 非空（Top10：北京 1,932/上海 1,842/广东 1,612…），行业五关键词、群体四关键词、资源投向四类全部可切。**效果侧（y 轴）三源零承载**：这是与姊妹件 POLPAN_003（区域政策差异性分析，三维全代理可算）命运分岔的地方——003 要「环境差异」可自建，本件要「效果数据」无源。判**部分支持**。本件交付三 Tab 可算骨架全套读数 + 效果维四件 absence 证据。

- 需求判定：**需求明列叶**（seq 220 / excel_row 223），但仅四指标名、无定义方法。
- 复现状态：骨架读数已跑通落产物；效果值无可算读数（负结论）。
- 档位结论：**部分支持**（x 轴足量 + y 轴三源 0 承载）。
- 关键事实：dev 效果五表全 0 行——结构现成等数据（B4 情形②），是「补数据」不是「建表」问题。
- 升档路径：政务兑现台账/满意度调查数据源接入 → 效果维闭合。

## 一、需求定义概述

### 1.1 所属功能模块

智能服务集群/科技信息展示系统/科技政策跟踪/政策分析评价/**政策分析报告可视化呈现**/分区/群体对比分析图（1.1.1.1.4.2.2.1.2；SRS seq 220、excel_row 223）。UI 实现在政策分析评价页（`PolicyAnalysis.jsx`）分析区：`RegionGroupCompare.jsx` 组件渲染 Card「分区/群体对比分析图」（标题在 175 行 Card 声明处），内部三 Tab（地区/行业/群体，`TAB_KEYS`），柱状图+热力图双联，右上资源投向 Select（资金/人才/平台/税收）与效果数据 Switch（评审门）。数据源是 `policyData.js:2391` 的 `regionGroupCompareData`——地区 Tab 五市（北上深广杭）× 四指标（支持力度 92/89/94…、落实率 88/85/91…）的 mock 矩阵，行业 Tab 五领域同构，群体 Tab 七群体带解读文案。

注意 UI 的一个门控细节：`hasEffectData` Switch 关掉时组件显示「未具备政策效果数据，不可生成对比分析图」——前端作者把「效果数据」作为本图的前置条件写进了交互逻辑，这从 UI 侧印证了本件判档的核心：**效果数据是这张图的命门**。

### 1.2 为什么需要本指标

政策效能评估的结论最终要落在「谁做得好」的对比上。单指标的时序图（多维指标趋势图）回答「整体走势」，分区/群体对比图回答「结构差异」——哪些地区政策效果领先、哪些行业受惠更深、哪些群体获得感更强，是资源投向优化（需求原文明列「筛选资源投向，识别区域差异和优化政策着力点」）的直接依据。三 Tab 设计对应三种决策视角：地区 Tab 服务区域对标、行业 Tab 服务产业政策评估、群体 Tab 服务精准施策。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**SRS seq 220 给的是展示行为（柱状图/热力图、批量展示、对比绩效优劣），四指标名（支持力度/落实率/满意度/创新贡献）仅出现在 UI mock 与组件 metrics 数组中，需求原文一个都没点名；每个指标怎么算（支持力度按资金强度？落实率按兑现比？满意度按调查得分？）无任何定义。

### 1.4 类似指标权威方法可行性分析概要

分组对比的效果评估在官方体系有三条路径：其一，国务院第三方评估制度（R1，2014 年起制度化，企业座谈+问卷+实地回访的定性定量结合法）；其二，工信部减轻企业负担调查的「应享尽享率」口径（R2，政策落实效果的企业自报调查，八成以上为达标线）；其三，OECD 政策组合跨国比较（R3，政策清单×工具×主题的对应分析+聚类）。前两条的共同点是**效果数据来自政务台账或专项调查**（兑现记录、企业问卷），第三条是存量结构比较（不涉效果值）。

| 方法族 | 代表 | 效果数据源 | 与本库匹配 |
|---|---|---|---|
| 第三方评估调查 | 国务院（R1） | 回访/问卷 | 无（需新调查） |
| 应享尽享率调查 | 工信部（R2） | 企业自报 | 无（需政务台账） |
| 政策组合聚类 | OECD STIP（R3） | 不需要 | **可算**（存量结构） |

方法谱系的启示：效果维（落实率/满意度）在权威口径里也全部依赖调查/台账数据，从未从政策文本库推得——本库效果维缺不是工程短板而是数据源属性。完整版见附录 C。

### 1.5 引用来源

- UI：`repos/demo-ui-science/src/pages/policy-tracking/analysis/RegionGroupCompare.jsx:175` — Card title="分区/群体对比分析图"；`RegionGroupCompare.jsx:14-18` — TAB_KEYS（地区/行业/群体）；`policyData.js:2391-2421` — regionGroupCompareData mock 矩阵；`PolicyAnalysis.jsx:1644` — 挂载点。
- SRS：`bid-reference/srs/02-科技信息展示系统/科技政策跟踪/政策分析评价.md` seq 220（excel_row 223），原文见附录 A。
- 主需求：`科技信息展示系统和科技专题服务系统.md` 1.1.1.1.4.2.2.1.2 同文。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义（双口径并列）**：

- 口径 A（即期骨架版，本件交付）：x 轴三维的政策存量强度矩阵——$\text{PolicyStock}(g) = |\{p : \text{region/industry/group}(p) \ni g\}|$，g 为地区/行业/群体分组，配套资源投向关键词过滤。这是「政策投入面」对比，不是需求原文的「政策效果数据」。
- 口径 B（需求完整版）：效果四指标矩阵——每个分组 g 的支持力度（资金强度）/落实率（兑现/应享）/满意度（受众评价）/创新贡献（创新产出归因）——其中落实率依赖 POLCMP_001 的兑现台账（该件已判完全不支持），满意度依赖调查数据源。

**降档/升档触发器**：口径 A 已可算但不满足需求原意（保守不升档）；若甲方接受存量强度作效果代理 → 可升完全转换支持（需书面确认）；若接入政务兑现台账+满意度调查 → 口径 B 的落实率/满意度闭合可升完全转换支持；创新贡献需政策归因模型（超本件范围）。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技政策跟踪/政策分析评价.md` |
| 所属四级功能 | 1.1.1.1.4.2.2 政策分析评价（13 叶，excel_rows 222-234） |
| 所属面板 | 政策分析报告可视化呈现（seq 219-222） |
| 本件叶 | **分区/群体对比分析图（seq 220，excel_row 223）——需求明列** |
| 同面板相邻叶 | 多维指标趋势图（seq 219）/ 多维结构关联图（seq 221，POLPAN_005 承接）/ 报告模板定制与批量导出（seq 222） |
| UI 容器 | PolicyAnalysis.jsx 分析区首图 |
| 姊妹件 | POLPAN_003（PolicyPanorama 页区域差异卡）——同为「区域对比」但三维可代理；POLCMP_001（落实率）是本件 y 轴落实率指标的依赖件 |

## 二、计算过程

### 2.1 方法选择（文献依据）

骨架侧选政策存量强度法（OECD R3 的存量结构比较思路——政策清单按维度分组计数），效果侧按 R1/R2 权威口径确认其数据源属性（调查/台账）后如实记缺，不做文本代理硬算。依据：skill P3「不要轻易说完全不可能」与 F11「轻易判不可能」的平衡点是——能自建的维度自建（骨架三维），必须外源的维度如实披露（效果三维），不造伪公式。

### 2.2 分区 Tab：省级/城市级政策存量分布

```sql
SELECT province, COUNT(*) c FROM gkx.dwd_policy_base
WHERE province IS NOT NULL AND province != '' AND province != 'NULL'
GROUP BY province ORDER BY c DESC LIMIT 10;
-- → 北京市 1932 / 上海市 1842 / 广东省 1612 / 山东省 1284 / 浙江省 1214 …
```

省级 Top10（`gkx_policy_province_top10`）：北京 1,932、上海 1,842、广东 1,612、山东 1,284、浙江 1,214、陕西 861、江苏 852、河南 748、天津 666、安徽 630——与 dev `gkxlumenx_ads.policy_national_dist`（33 行，2026-10-29 批）零漂移（B11）。城市级 Top5（`gkx_policy_city_top5`）：北京 2,268、上海 1,841、深圳 879、天津 666、杭州 446——UI mock 的五市（北上深广杭）全部有数。省级非空率 100%（`gkx_policy_province_nonnull=20000`，派生键 `gkx_policy_province_nonnull_pct=100.0`）：分区 Tab 的 x 轴全量可算。

### 2.3 行业 Tab：关键词代理分布

```sql
SELECT COUNT(*) FROM gkx.dwd_policy_base
WHERE title LIKE '%人工智能%' OR abstract LIKE '%人工智能%';  -- → 73
```

五行业命中（`gkx_policy_industry_kw_hits`）：新能源 256、生物医药 104、人工智能 73、半导体 36、先进材料 10。UI mock 行业 Tab 的五个领域（人工智能/生物医药/新能源/半导体/先进材料）全部有非零存量——行业 Tab x 轴可算，但量级分层明显（新能源是先进材料的 25.6 倍），热力图色阶会集中头部。行业专列缺失是政策库通病（gkx 无 industry 列），关键词代理的误纳/漏判方向已在 POLPAN_003 §四 同款披露。

### 2.4 群体 Tab 与资源投向过滤

群体四关键词（`gkx_policy_group_kw_hits`）：企业 6,861、机构 3,026、人才 1,020、创业 865——企业导向是该政策库的绝对主体（企业命中占全库 34.3050%，与 `gkx_policy_funding_share_pct` 同法同池的姊妹读数，分子=企业命中行数）。资源投向四类（`gkx_policy_resource_target_hits`）：funding（资金/补贴/经费）2,319、platform（平台）1,410、talent（人才）911、tax（税收）232。UI 的资源投向 Select 交互可即期接通：筛选后重算分组计数即可——但切出来的仍是存量计数，不是效果值。

### 2.5 效果维探针（负结论核心证据）

**gkx**：`SHOW COLUMNS FROM gkx.dwd_policy_base` 33 列逐一核对，effect/satisf/implement/fulfil 关键词命中仅 `implementation_date`（实施日期，非效果值；`gkx_policy_effect_like_cols=['implementation_date']`）；`policy_support` 列（支持力度的结构候选）实测 20,000 行全部为字面 `null`（JSON_LENGTH>0 且非 null 值 0 行，`gkx_policy_support_real_rows=0`）——**结构在、值全空**。**dev**：`policy_effect_eval`/`policy_support_assessment`/`policy_public_opinion`/`shenzhen_policy_status`/`policy_support_rank` 五表全 0 行（`dev_policy_effect_table_rows`）；ads 层 `policy_effect`/`policy_intensity`/`policy_metric_timeseries` 三表亦全 0 行。**久新**：政策 evidence 面 45 列无效果值列（仅 relation_confidence/alignment_score 对齐置信度），且 1,252 行中 1,213 行 `is_synthetic=1`（96.88%，派生键 `gkx_policy_synth_share_pct_jiuxin`）——LLM 合成的政策语境不是政策效果实测。

### 2.6 稳健性与口径敏感性

骨架读数的稳健性：分区计数与 dev ads 面双源对账一致；行业/群体关键词是固定词典（版本化在脚本内），重跑逐位一致。敏感性披露：企业关键词 34% 的占比意味着群体 Tab 的热力图几乎单色——如果按篇均效果值（口径 B）重算，企业维的权重会进一步放大；行业关键词的「新能源 256」含大量电力/储能政策（宽口径），若收窄为「战略性新兴产业」标准名录口径会显著缩量——两向口径差已在附录 C 风险表登记。

### 2.7 复现代码结果展示

- 代码：`code/M_SCIUI_POLPAN_002.py`（三 Tab 骨架 + 资源投向 + 效果维三源探针；运行 `python3 code/M_SCIUI_POLPAN_002.py`）。
- 产物：`code/M_SCIUI_POLPAN_002_out.json`。正文数字与产物键逐一对应：`gkx_policy_rows=20000`（§2.2）、`gkx_policy_province_top10`（§2.2）、`gkx_policy_city_top5`（§2.2）、`gkx_policy_industry_kw_hits`（§2.3）、`gkx_policy_group_kw_hits` / `gkx_policy_resource_target_hits`（§2.4）、`gkx_policy_effect_like_cols=['implementation_date']` / `gkx_policy_support_real_rows=0` / `dev_policy_effect_table_rows` / `dev_ads_policy_effect_table_rows` / `jiuxin_policy_evidence_synthetic_rows=1213`（§2.5）。
- 结果解读：三 Tab 骨架全套可算读数 + 效果维三源四件负证据——「图能画、值没有」是本件复现结论的准确概括。
- 对照需求功能要求的评审：批量展示地区/行业/群体对比——**部分满足**（存量强度版即期可画）；展示政策效果数据——**不满足**（三源无效果值，需外部数据源）。

### 2.8 分步证据对照表

| 步骤 | 证据项 | 产物键 / 事实 | 数值 |
|---|---|---|---|
| 装载 | 政策底表 | `gkx_policy_rows` | 20,000 |
| 分区 | 省级非空 | `gkx_policy_province_nonnull` | 20,000（100%） |
| 分区 | 省级 Top10 | `gkx_policy_province_top10` | 北京 1,932 / 上海 1,842 / 广东 1,612… |
| 分区 | 城市 Top5 | `gkx_policy_city_top5` | 北京 2,268 / 深圳 879 / 杭州 446… |
| 行业 | 五行业命中 | `gkx_policy_industry_kw_hits` | 新能源 256 / 生物医药 104 / AI 73… |
| 群体 | 四群体命中 | `gkx_policy_group_kw_hits` | 企业 6,861 / 机构 3,026 / 人才 1,020… |
| 投向 | 四类命中 | `gkx_policy_resource_target_hits` | funding 2,319 / platform 1,410… |
| 效果 | gkx 效果列 | `gkx_policy_effect_like_cols` | []（0 列） |
| 效果 | gkx 支持力度值 | `gkx_policy_support_real_rows` | 0 行 |
| 效果 | dev 效果五表 | `dev_policy_effect_table_rows` | 全 0 行 |
| 效果 | dev ads 三表 | `dev_ads_policy_effect_table_rows` | 全 0 行 |
| 效果 | 久新合成占比 | `gkx_policy_synth_share_pct_jiuxin` | 96.88%（1,213/1,252） |

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 地区分维 | gkx | policy_base.province/city | 20,000（100% 非空） | 直查 | **足量** |
| D2 | 行业维 | gkx | title/abstract 关键词 | 五行业 10-256 行 | 代理 | 可算（宽口径） |
| D3 | 群体维 | gkx | title/abstract 关键词 | 四群体 865-6,861 行 | 代理 | 可算 |
| D4 | 资源投向维 | gkx | abstract 关键词 | 四类 232-2,319 行 | 代理 | 可算 |
| D5 | 支持力度值 | gkx/dev | policy_support 列/效果表 | 0 行真值 | **不存在值** | **缺** |
| D6 | 落实率/满意度值 | 三源 | — | 0 承载 | **不存在** | **缺**（POLCMP_001 同源） |

`support_judgment="部分支持"`，与 §〇 定义一致（闸 6）。

### 3.2 D1-D4 骨架面：三 Tab 全量可算

分区维是质量最高的骨架维：province/city 双列 100% 非空且与 dev ads 面双源对账零漂移。行业/群体/投向三维走关键词代理——词典固定、可版本化、重跑确定，但口径宽窄随甲方标准名录可调（附录 C 风险表）。骨架面合计覆盖 20,000 行全库，任何分组组合的存量读数即期可出。

### 3.3 D5/D6 效果维 absence_probe 全记录（三源四件）

**gkx 列级**：33 列逐一核对 + effect/satisf/implement/fulfil 关键词扫 → 仅 implementation_date（实施日期，非效果值）；policy_support 列在但全 `null`（0 行真值）——**表存在但关键列无值**。**dev 表级**：dwd 层效果五表 + ads 层效果三表 → 全 0 行——**表存在但 0 行**（B4 情形②：补数据同步问题，非建表问题；修复动作是接数据不是改 schema）。**dev 列级**：`policy_base_info` 45 列 effect 类命中仅 implementation_date（实施日期，非效果值）。**久新**：evidence 45 列无效果值列 + 96.88% 合成——**样例级且合成**（B4 情形③叠加造数标识，双重症）。

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| 省级分布 | 与 dev ads.policy_national_dist（2026-10-29 批）零漂移 |
| 行业/群体关键词 | 固定词典（脚本内版本化），重跑逐位一致 |
| policy_support 值 | DISTINCT 前缀唯一值 = 'null'（20,000 行） |
| dev 效果表 | 八表逐一 COUNT，全 0 |
| 久新合成标识 | is_synthetic=1 1,213 行（96.88%） |
| 脚本形态 | 三源顺序查询，零 demo_*，产物无耗时键 |

## 四、数据缺失情况

### 4.1 缺口清单（可构建但存在缺口）

| 缺失项 | 类型 | 对档位的影响 |
|---|---|---|
| 支持力度真值（资金强度） | 数据缺（列在值空） | y 轴 1/4 缺 → 主降档因之一 |
| 落实率/满意度值 | 数据源缺 | y 轴 2/4 缺 → 主降档因之二 |
| 创新贡献归因值 | 方法+数据双缺 | y 轴 1/4 缺 → 需政策归因模型 |
| 行业标准名录映射 | 口径工程 | 关键词宽窄可调 → 影响骨架精度非档位 |

四项中前三项共占 y 轴全部——本件是「x 轴满、y 轴空」的典型部分支持形态。

### 4.2 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 接政务兑现台账 | 外部数据源 | 本件 + POLCMP_001 + POLCMP 族 | 落实率/资金到位闭合 |
| 接满意度调查数据 | 外部数据源 | 本件 | 满意度闭合（R1 第三方评估口径） |
| policy_support 值回填 | 数据工程 | 本件 | gkx 供应商侧回填支持力度结构化值 |
| 存量强度版即期上线 | 产品决策 | 本件 | 口径 A 先行，效果维标注「数据接入中」 |

四条路径中前两条是外部源立项（决定升档），第三条依赖供应商，第四条是即期可做的产品决策。

## 参考文献

1. 国务院督查政策落实首次引入第三方评估[EB/OL]. 中国政府网. https://www.gov.cn/zhuanti/2014-09/01/content_2783647.htm （R1，2026-11-01 WebSearch 核验可达）
2. 国务院减轻企业负担部际联席会议办公室有关负责人就清欠工作接受记者采访[EB/OL]. 工业和信息化部. https://www.miit.gov.cn/jgsj/yxj/jqqyfdgz/art/2020/art_f043f779bc454a2bb4f98e94603d8713.html （R2，2026-11-01 WebSearch 核验可达）
3. Evidence-based portfolios of innovation policy mixes: A cross-country analysis[EB/OL]. Technological Forecasting and Social Change. https://doi.org/10.1016/j.techfore.2021.120708 （R3，2026-11-01 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技政策跟踪/政策分析评价.md》seq 220（excel_row 223）：

> ### 分区/群体对比分析图 · 序号 220
> #### 需规功能描述
> 平台支持通过柱状图、热力图等形式，批量展示各地区、行业或目标群体间的政策效果数据，帮助用户对比不同空间、对象的绩效优劣，筛选资源投向，识别区域差异和优化政策着力点。

《科技信息展示系统和科技专题服务系统.md》1.1.1.1.4.2.2.1.2 同文（主需求与 SRS 逐字一致）。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 分区/群体对比分析图 | 政策分析评价.md | 1（seq 220 叶） |
| 分区/群体对比分析图 | 主需求 | 1（1.1.1.1.4.2.2.1.2） |
| 支持力度/落实率/满意度/创新贡献 | 三份需求真源 | 0（仅 UI mock metrics 数组） |
| 政策效果数据 | 政策分析评价.md | 1（seq 220 描述句） |
| 分区对比 | 核增需求 | 0（核增 17 叶无此图） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_POLPAN_002_out.json`（三 Tab 骨架 + 效果维三源探针全量在案）。
- 共享快照：`code/_snapshots/_shared_probe_s3_01_out.json`（fix2 政策底表 20,000 行对账键）。
- 依赖件：POLCMP_001（落实率 absence 探针互证）；POLPAN_003（province 分布同源复算）。

### B.2 本件产物逐键清单（`code/M_SCIUI_POLPAN_002_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `metric_id` | 标识 | M_SCIUI_POLPAN_002 | 文首 |
| `ui_evidence` | 证据 | 3 条组件：行号 | §1.5 |
| `requirement_trace.named_in_srs` | 事实 | **true**（seq 220） | §1.1/附录 A |
| `facts.gkx_policy_rows` | 计数 | 20,000 | §2.2 |
| `facts.gkx_policy_province_top10` | 分布 | 10 省 | §2.2 |
| `facts.gkx_policy_city_top5` | 分布 | 5 市 | §2.2 |
| `facts.gkx_policy_industry_kw_hits` | 分布 | 5 行业 | §2.3 |
| `facts.gkx_policy_group_kw_hits` | 分布 | 4 群体 | §2.4 |
| `facts.gkx_policy_resource_target_hits` | 分布 | 4 投向 | §2.4 |
| `facts.gkx_policy_effect_like_cols` | 探针 | [] | §2.5/§3.3 |
| `facts.gkx_policy_support_real_rows` | 探针 | 0 | §2.5/§3.3 |
| `facts.dev_policy_effect_table_rows` | 探针 | 五表全 0 | §2.5/§3.3 |
| `facts.dev_ads_policy_effect_table_rows` | 探针 | 三表全 0 | §2.5/§3.3 |
| `facts.jiuxin_policy_evidence_synthetic_rows` | 探针 | 1,213 | §2.5 |
| `derived[0]` | 派生比 | gkx_policy_province_nonnull_pct=100.0 | §2.2 |
| `derived[1]` | 派生比 | gkx_policy_synth_share_pct_jiuxin=96.88 | §2.5 |
| `derived[2]` | 派生比 | gkx_policy_funding_share_pct=11.595 | §2.4 |
| `support_judgment` | 判档 | 部分支持 | §〇 |

### B.3 共享快照消费

消费 `_shared_probe_s3_01_out.json` 的 `fix2.政策底表行数=20000` 与 `资讯政策类表 LIKE`（四表清单）；province 分布经 dev `policy_national_dist` 33 行二次对账。

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 效果数据源 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 第三方评估 | 国务院（R1） | 座谈/问卷/回访 | 无 | 高（需新调查） |
| 应享尽享调查 | 工信部（R2） | 企业自报台账 | 无 | 高（需政务源） |
| 政策组合聚类 | OECD STIP（R3） | 不需要（存量） | **gkx 20,000 行** | **最高（即期）** |
| 文本效果代理 | 本件排除 | — | 摘要金额存在性 | 低（仅支持力度） |

### C.2 数据矩阵

| 依赖 | 行数/状态 | 覆盖/质量 | 缺口 |
|---|---|---|---|
| province/city | 20,000（100%） | 双源对账一致 | 无 |
| 行业/群体/投向关键词 | 232-6,861 | 固定词典 | 名录口径待裁 |
| policy_support 值 | 0 真值 | 列在全 null | 值回填 |
| dev 效果八表 | 全 0 行 | 结构现成 | 数据接入 |
| 久新 evidence | 1,252（96.88% 合成） | 对齐置信度在 | 效果值无 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 口径 A 存量强度三 Tab 图（效果维标「数据接入中」） | 无 |
| v2 | 支持力度维接入（供应商回填或金额抽取工程） | 数据工程 |
| v3 | 落实率/满意度接入（口径 B 闭合） | 政务台账+调查源立项 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 存量强度被误读为政策效果 | **高** | 图表标题限定「政策存量强度」+效果维显式留白 |
| 行业关键词宽口径虚高 | 中 | 标准名录映射触发器 |
| 久新合成数据混入 | 中 | is_synthetic 过滤硬规则 |

### C.5 总判

**部分支持**：骨架三维（地区/行业/群体/投向）三源足量即期可画，效果四指标三源零承载（gkx 列在值空、dev 八表 0 行、久新 96.88% 合成且无效果列）——y 轴是本件的命门，升档唯一路径是外部数据源。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_POLPAN_002.py` | 退出码 0，落 `_out.json` |
| 分区对账 | facts.gkx_policy_province_top10 vs dev policy_national_dist | 零漂移 |
| 效果探针复核 | facts.dev_policy_effect_table_rows | 八表全 0 |
| 词典版本 | 脚本内 INDUSTRY_KWS/GROUP_KWS/TARGET_KWS | 固定可版本化 |
| mock 残留 | `rg "regionGroupCompareData" repos/demo-ui-science` | 正式版替换后无引用 |
