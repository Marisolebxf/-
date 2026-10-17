# G5 证据卡 · 瓶颈 / 卡脖子 / COMPUTE / 挂起系（9 条）

> **只读证据卡，待 human:徐滕强 逐条拍板，禁止直接落盘。**
> 任务：CHAIN-METRIC-COVER-STAT-L01 · G5 组 · data-agent · 2026-10-13
> 真源：`agent-delivery/metrics/registry/cfg_metric-CHAIN-seed.yaml` · `metric-readiness-matrix-CHAIN.yaml` · `agent-delivery/metrics/calc-logic/CHAIN/*.md`
> 探库实测：主会话 2026-10-13（本卡直接引用，不重复连库）

## 0. 组级事实与共享缺口

| 项 | 实测 |
|---|---|
| `dwd.industry_bottleneck` | **demo 库不存在（全缺）**，seed 三条 BOTTLENECK 均挂它作源 |
| `chain_panorama` / `svc_chain_gap` 类汇总壳 | **不存在**（旧细稿所述 `gkxlumenx_ads.chain_bottleneck` 8 行 / `chain_panorama_nodes` 41 行 / `chain_layout_recommend` 8 行 / `chain_sz_panorama` / `chain_sz_advantage` 均**不在现网**） |
| `demo_gkxlumenx_dwd.industry_chain` | **43 链**；`enterprise_industry_chain` **= 0 行** |
| `dwd_patent` | 293 万行，**无产业链字段**；`industry_chain_patent` 不存在 |
| 矩阵覆盖 | 本组 9 条中**仅 2 条有矩阵行**（SZ_ADVANTAGE_RANK、CHOKE_LINK_COUNT），其余 7 条**缺行**（记忆：CHAIN 矩阵仅覆盖深圳专题及部分页面，B 类缺行 20 条） |
| QC 状态 | QC01/02/04/08/09 全部 🟡 待甲方（客户决策清单跟踪表 221–229 行） |
| 模式参照 | SVC 波先例：`M_SVC_SZ_CHAIN_COMPLETENESS` v0.2.0 = 「公式未签+环节无源→不写可执行公式，写解挂条件」；`M_SVC_CHAIN_SEGMENT_AVG_DEPTH` v0.2.0 = 「锁目标口径 + 双缺口 + 禁冒充清单」；`M_SVC_REC_CANDIDATE_CNT` = **废止**（实时结果集条数非指标） |

**共享缺口声明（BOTTLENECK 三兄弟 + CHOKE_LINK_COUNT + LAYOUT_RECOMMEND_COUNT 共用）**：

```text
（缺口）dwd.industry_bottleneck「瓶颈判定表」不存在。
该表定义为算法判定产物（瓶颈识别模型输出），当前：无模型输出、无 ODS 源、无 ADS 落表。
凡以该表为唯一/主要源的指标（BOTTLENECK_COUNT / SEVERITY / TYPE_DIST / CHOKE_LINK_COUNT /
LAYOUT_RECOMMEND_COUNT 的第三源），在表落库前一律不可执行。
```

**本组各条引用共享缺口时写「见组级共享缺口 §0」即可，不重复展开。**

---

## 1. M_CHAIN_BOTTLENECK_COUNT（瓶颈堵点数）

### 现稿画像

- seed v0.1.0：`pending_ref: QC04`，`definition_status: pending_data_lead`，`is_mock: true`
- definition：产业链中识别出的瓶颈/堵点数；瓶颈类型细分口径(5维是否完整)待甲方确认
- formula：`COUNT(DISTINCT id) FROM dwd.industry_bottleneck`（**可执行形态但源不存在**）
- source_tables：`dwd.industry_bottleneck <- 算法判定` + `dwd.industry_chain_enterprise`
- calc-logic（2026-08-21 调研稿）：源 `gkxlumenx_ads.chain_bottleneck`（8 行；bottleneck_dims），「按当前演示规则识别」
- **无矩阵行**

### 探库实测引用

- `dwd.industry_bottleneck` 不存在（§0 共享缺口）
- calc-logic 所述 `gkxlumenx_ads.chain_bottleneck` 8 行**不在现网**（ADS 壳不存在）
- `enterprise_industry_chain` = 0 行（第二源也空）

### 建议：锁目标口径 + 留缺口（v0.2.0）

沿 SVC「AVG_DEPTH」模式——公式语义清晰可锁，源不存在留缺口，QC04 部分内容（类型 5 维）另拆到 TYPE_DIST。

- **锁定口径**：指定产业链在统计窗内，由瓶颈识别模型判定入库的瓶颈/堵点去重数（`COUNT(DISTINCT bottleneck_id)`）
- **缺口**：见组级共享缺口 §0；QC04 瓶颈识别口径（5 维是否完整、判定阈值）🟡
- **改前→改后**：
  - definition：`pending_data_lead(QC04)：…待甲方确认` → `瓶颈识别模型判定入库的瓶颈/堵点去重数。判定口径挂 QC04（阈值/维度未签）；源表见组级共享缺口。禁止用图谱演示角标数、资讯 NLP 抽取数冒充`
  - formula：`COUNT(DISTINCT id) FROM dwd.industry_bottleneck` → `目标口径：SELECT COUNT(DISTINCT bottleneck_id) FROM dwd.industry_bottleneck WHERE chain_id = {chain_id}（缺口：见 §0，表不存在不可执行）`
  - source_tables：现值 → `["（缺口）dwd.industry_bottleneck <- 算法判定（QC04 未签 + 表不存在）"]`
  - 矩阵：**补行** d1=draft/QC04、d2=pending、d3=none（源表全缺）、d4=mock
  - version 0.1.0 → 0.2.0，pending_ref 保持 QC04

### 风险点与待拍清单

1. 瓶颈识别模型本身未立项/未签（QC04 🟡）——本条 D3=none 是**真缺口**，不是漂移
2. calc-logic 旧稿「演示规则」与 seed「算法判定」叙事不一致——改后统一为「模型判定入库」
3. UI 现值 3（IndustryCenterPage 演示固定值）非本条真数——保留 🧪 角标，不接线
4. **待拍**：口径方向（模型判定入库数）是否认可；缺口表述是否入 seed

---

## 2. M_CHAIN_BOTTLENECK_SEVERITY（瓶颈严重度）

### 现稿画像

- seed v0.1.0：`pending_ref: QC04`，`definition_status: pending_data_lead` + **`formula_status: pending_algorithm`**
- definition：瓶颈严重度评分（0-100，取最高严重度）；评分口径同 QC04
- formula：`pending_algorithm（MAX(severity_score) FROM dwd.industry_bottleneck）`——**算法未签**
- source_tables：仅 `dwd.industry_bottleneck`（单源）
- calc-logic：`chain_bottleneck.severity` 直读，「待建：严重度分级规则正式定义」
- **无矩阵行**

### 探库实测引用

- 同 §0 共享缺口；ADS 壳 `chain_bottleneck.severity` 不在现网
- 且严重度评分**算法本身未签**（formula_status: pending_algorithm）——比 COUNT 多一层缺口

### 建议：挂起（沿 M_SVC_SZ_CHAIN_COMPLETENESS 模式）

公式未签 + 源表不存在 = 双缺口，SVC 同款 → **不写可执行公式，写解挂条件**。

- **锁定目标口径**（仅语义层）：指定产业链瓶颈集合中严重度评分的最大值（0-100）
- **不写可执行公式**；解挂条件：① QC04 严重度评分算法签发（唐绍祖/算法侧）② dwd.industry_bottleneck 落库
- **改前→改后**：
  - definition → `瓶颈严重度评分最大值（0-100）。评分算法未签（QC04）+ 源表不存在（见 §0），双缺口挂起。解挂：QC04 算法签发 + industry_bottleneck 落库。禁止用演示分级（中高/中低）或前端 fixture 冒充`
  - formula → `挂起（不写可执行 SQL）：目标口径 MAX(severity_score)；解挂后按已签算法落 seed`
  - 矩阵：**补行** d1=draft/QC04、d2=pending、d3=none、d4=mock
  - version 0.1.0 → 0.2.0

### 风险点与待拍清单

1. 算法未签是主缺口——不能像 COUNT 那样只留表缺口就锁「目标口径可执行」
2. calc-logic 旧稿源（chain_bottleneck.severity ADS 壳）不在现网——改后 calc-logic 同步改写，旧述「ADS 有 severity」作废
3. **待拍**：挂起方案（vs 锁目标口径+缺口）是否认可

---

## 3. M_CHAIN_BOTTLENECK_TYPE_DIST（瓶颈类型分布）

### 现稿画像

- seed v0.1.0：`pending_ref: QC04`，`definition_status: pending_data_lead`
- definition：按瓶颈类型（技术/人才/市场/资本/政策）的分布统计
- formula：`COUNT(*) GROUP BY bottleneck_type FROM dwd.industry_bottleneck`（可执行形态但源不存在）
- calc-logic：展开 `bottleneck_dims`（JSON/文本）后 GROUP BY——**解析规则需固化**（待建字段）
- **无矩阵行**

### 探库实测引用

- 同 §0 共享缺口
- 额外：`bottleneck_dims` 是 JSON 数组字段（一条瓶颈可属多类型），「展开后计数」与「主类型计数」两种口径**未定**——QC04 明确「5 维是否完整待确认」

### 建议：锁目标口径 + 留缺口（v0.2.0）

- **锁定口径**：指定产业链瓶颈按五维类型（技术/人才/市场/资本/政策）的计数分布
- **缺口**：① §0 共享缺口；② QC04 类型字典与计数方式（一瓶颈多类型时按主类型 1 次还是按维度展开多次）未定
- **改前→改后**：
  - definition → `瓶颈按五维类型（技术/人才/市场/资本/政策）的分布计数。类型字典与一多映射计数方式挂 QC04；源表见 §0。禁止用资讯关键词分类冒充`
  - formula → `目标口径：SELECT bottleneck_type, COUNT(*) FROM dwd.industry_bottleneck WHERE chain_id={chain_id} GROUP BY bottleneck_type（一多映射方式待 QC04；缺口：见 §0）`
  - 矩阵：**补行** d1=draft/QC04、d2=pending、d3=none、d4=mock
  - version 0.1.0 → 0.2.0

### 风险点与待拍清单

1. **类型字典未定**（本条主缺口）：五维是 QC04 临时默认；一瓶颈多类型时展开计数会重复计数，按主类型计数则丢信息——须甲方拍
2. calc-logic「bottleneck_dims 解析规则需固化」= 同一缺口，改后 calc-logic 同步
3. **待拍**：五维字典 + 计数方式是否走 QC04 一并问；口径方向是否认可

---

## 4. M_CHAIN_CHOKE_LINK_COUNT（卡脖子环节数）

### 现稿画像

- seed v0.1.0：`pending_ref: GAP-ALGO-TYPE-UNSIGNED`，**`acceptance_unit_id: TOPIC-DIAG-017`**，`owner_human: human:淮政玮`
- definition：`瓶颈∧severity=高；⊆ 瓶颈数；与图谱角标同计数 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份`
- formula：`pending_cosign: human:唐绍祖（未签）`
- source_tables/source_systems：`[pending_ods]`；`is_mock: true`，`mapping_status: ⏳`
- register_task / open_task：`ALGO-LIB-T0X-REGISTER-L01`
- 矩阵行存在：d1=draft / `GAP-ALGO-TYPE-UNSIGNED`（「T0-X 分析清单身份注册；禁止把 A1 表2 type 当已签」）、d2=pending、d3=pending_ods（「未核 ≠ 已确认缺口」）、d4=mock、lifecycle_stage: open

### 探库实测引用

- 卡脖子判定源（瓶颈∧severity=高）依赖 §0 共享缺口（industry_bottleneck 不存在）；severity 算法同时未签（见第 2 条）
- calc-logic 所述 `chain_panorama_nodes` 41 行 ADS 壳不在现网（「卡脖子标签字段未在 panorama_nodes 中显式存在」）
- seed 自己声明「与图谱角标同计数」——图谱角标当前来自前端演示数据，非算法判定

### 建议：维持 OPEN 挂起（不动公式），补与 BOTTLENECK_COUNT 的包含关系表述

本条已是标准 OPEN draft（pending_cosign 唐绍祖），**不需要也不应该**在本批写公式。要做的是把「⊆ 瓶颈数」的包含关系写实：

- **锁定关系表述**：`卡脖子环节数 = 瓶颈集合中 severity=高 的子集计数 ⊆ M_CHAIN_BOTTLENECK_COUNT（同窗同链）；前提是 QC04 判定与 severity 算法签发`
- **改前→改后**：
  - definition：现值 → 现值 + `与 M_CHAIN_BOTTLENECK_COUNT 恒有：0 ≤ 卡脖子环节数 ≤ 瓶颈数（同链同窗）；卡脖子=瓶颈∧severity=高，判定未签前不得用其他口径（如仅技术类瓶颈）替代`
  - formula：保持 `pending_cosign: human:唐绍祖（未签）` **不动**
  - 矩阵：现值基本准确，d3 备注「未核 ≠ 已确认缺口」保留；**无矩阵改动需求**
  - version 不动（OPEN 身份不动）
- **不与本批 BOTTLENECK_COUNT 联动锁口径**——CHOKE 是 ALGO-LIB 注册轨（T0-X），与 COVER-STAT 轨不同管线，唐绍祖未签前保持 OPEN

### 风险点与待拍清单

1. **最大风险**：图谱前端「卡脖子角标」与算法判定脱钩——若页面先上真数（≠演示角标），会出现 UI 显示数与指标库对不上的口径事故；UI 须保持角标为演示态
2. severity 算法未签传导：卡脖子判定（severity=高）被第 2 条的算法缺口阻塞——**CHOKE 解挂 ⊇ SEVERITY 解挂**
3. **待拍**：包含关系表述是否入 definition；是否维持 OPEN 不动公式（建议：是）

---

## 5. M_CHAIN_LAYOUT_RECOMMEND_COUNT（重点布局推荐数）★本组最重要判定点

### 现稿画像

- seed v0.1.0：`pending_ref: QC09`，`definition_status: pending_data_lead`
- definition：算法推荐的重点布局产业链/环节数；推荐算法权重与阈值待甲方确认
- formula：`COUNT(DISTINCT chain_id) WHERE 布局优先级评分 >= 阈值`
- source_tables：`dwd.industry_chain` + `dwd.industry_region_index` + `dwd.industry_bottleneck`（**后两张不存在**）
- calc-logic：`chain_layout_recommend` 建议列表 COUNT（ADS 壳 8 行，不在现网）
- **无矩阵行**
- demo UI 实况（IndustryCenterPage 发展方案态）：`发展方案数=3`（**前端硬编码固定清单**「强化关键设备…」等 3 条），另显示「优先布局方向=5」（挂 M_CHAIN_LAYOUT_PRIORITY_SCORE）

### 探库实测引用

- `dwd.industry_region_index` / `dwd.industry_bottleneck` 不存在（§0）；`chain_layout_recommend` 壳不在现网
- `demo_gkxlumenx_dwd.industry_chain` = 43 链（第一源有数）
- demo 页面「发展方案 3 条」为**写死文案列表**，非任何模型输出

### 建议：**废止**（沿 M_SVC_REC_CANDIDATE_CNT 先例）——待拍

**判定论证（是否与 REC_CANDIDATE_CNT 同款风险）**：

| 维度 | M_SVC_REC_CANDIDATE_CNT（已废止） | M_CHAIN_LAYOUT_RECOMMEND_COUNT（本条） |
|---|---|---|
| 数字来源 | 推荐名单生成后 `results.length` | 发展方案建议列表条数（当前 demo=写死 3 条） |
| 随筛选/条件变？ | 是（产业方向+筛选条件实时变） | **是**——`WHERE 布局优先级评分 >= 阈值`，阈值是用户/甲方参数（QC09 未签），“推荐数”随阈值与权重实时变 |
| 预聚合意义 | 无（数的是结果集不是实体） | **无**——数的是「过了阈值的建议」这一**模型输出切片**，不是库内实体存量 |
| 语义 | 「共 N 家候选」页面副词 | 「发展方案 N 项」页面副词 |
| SVC 处置 | 废止；页面可显示 N 但不出指标卡 | —— |

**同款成立**：布局推荐名单是**模型输出**（M_CHAIN_LAYOUT_PRIORITY_SCORE 是 MODEL），对模型输出过阈值再 COUNT，得到的是「当前参数下的名单长度」，随 QC09 权重/阈值变化而变，**不是统计指标**。三条源表两缺 + 阈值未签 + demo 写死，进一步支持。
但注意一个差异：若甲方真要「按固定权重季度跑一次、过阈值链数入库 ADS」的预聚合口径，则可救活为 STAT——**这正是 QC09 要问的**。

- **改前→改后（若拍废止）**：
  - definition → `2026-10-13 废止。布局推荐名单是模型输出（LAYOUT_PRIORITY_SCORE，MODEL）过阈值后的结果集，条数随 QC09 权重/阈值参数实时变化，非预聚合统计指标（同 M_SVC_REC_CANDIDATE_CNT 先例）。保留 ID 防冲突。页面可显示「方案 N 项」，不要 MetricSpecCard，不要 Java/Python 出数，不要灌 ADS`
  - formula → `废止（不写公式）`
  - 矩阵：**补行**标 d1=deprecated（或按现行枚举 draft + note「已废止 2026-10-13」）
  - version 0.1.0 → 0.2.0（废止也升版留痕）
- **改前→改后（若甲方要预聚合口径，备选）**：锁目标口径 `COUNT(DISTINCT chain_id) FROM ads.layout_recommend_snapshot WHERE snapshot_date={季度快照日} AND priority_score>=已签阈值` + 缺口：QC09 权重阈值未签 + region_index/bottleneck 无源 + 无快照表

### 风险点与待拍清单

1. **本组最重要待拍项**：废止 vs 预聚合救活。建议倾向**废止**（与 SVC 波对齐、避免模型输出计数指标化），除非甲方明确要季度快照口径
2. 若废止：UI 现挂的 metricId 需摘除（页面显示 3 保留但去掉 ⓘ 卡）——涉及 demo-ui-topic 改动，另开 UI 任务
3. POLICY 域有同构指标 `M_POLICY_LAYOUT_REC_COUNT`（QPOL-02，同款「COUNT(WHERE 优先级评分>=阈值)」写法）——若本条废止，POLICY 条下次复核时应同判，避免域间双标
4. **待拍**：废止 or 救活；若救活，快照频率（季度/年度）入 QC09 追问

---

## 6. M_CHAIN_CONCENTRATION_INDEX（产业集中度）★COMPUTE 交唐绍祖

### 现稿画像

- seed v0.1.0：`pending_ref: QC02`，`definition_status: pending_data_lead` + `formula_status: pending_algorithm`，**algorithm_type: COMPUTE**
- definition：产业链企业分布的集中度指数（HHI 或 CR_N）；口径与 N 值待甲方确认
- formula：`pending_algorithm（HHI = SUM(企业市场份额^2) 或 CR_N = TopN企业市场份额之和）`
- source_tables：`dwd.industry_chain_enterprise <- ods: dwd_org_industry_chain_dtl.chain_score`（**表名漂移**：现网为 `enterprise_industry_chain`=0 行）
- calc-logic（调研稿）：名称写「市场集中度」，源 `chain_key_node.market_concentration_score`（41 行，不在现网），映射「中高/中低」分级——**与 seed 叙事已分叉**（seed=企业分布集中度，calc-logic=环节集中度分级）
- **无矩阵行**

### 探库实测引用

- `industry_chain_enterprise` 不存在；真源 `dwd_org_industry_chain_dtl` 派生壳 `enterprise_industry_chain` = **0 行**——**无企业份额数据**
- `chain_key_node` ADS 壳不在现网
- 即使有链上企业名单（`dwd_org_industry_tags`），也**无企业级营收挂链**——份额分子无源（QC06 已定营收口径但企业×链营收聚合表未建）

### 建议：挂起 + 两案对比表交唐绍祖（不写可执行公式）

**HHI vs CR_N 对比**：

| 维 | HHI（赫芬达尔） | CR_N（前 N 集中度） |
|---|---|---|
| 公式 | HHI = Σ(企业份额²)，份额以小数计，∈(0,1] | CR_N = 前 N 名企业份额之和，∈(0,1] |
| 直觉 | 捕捉**全部**企业的分散/集中，头部尾部都算 | 只看头部，尾部不影响 |
| 数据需求 | **全量**链上企业份额 | 只需 TopN 企业份额（但排序仍需全量） |
| 对小企业误差 | 敏感（每家都进公式） | 不敏感（不入前 N 即忽略） |
| 美国司法部阈值惯例 | <0.01 分散 / 0.01–0.15 未集中 / 0.15–0.25 中度 / >0.25 高集中（可借用叙事） | CR4>60% 寡占等（行业经济惯例，链场景需自定） |
| 链场景适配 | 链上企业长尾多、微小企业多，平方项使其天然抗小企业噪声，**对份额精度要求低**（小企业份额误差平方后可忽略） | N 值要拍（CR4/CR8？），且头部边界企业份额精度要求高 |
| 可解释性 | 单一数字，阈值体系成熟 | 直观（「前4家占了X%」），甲方易理解 |
| 现网可算性 | **不可算**（无企业份额源） | **不可算**（同左） |

**份额分母用什么（决策点 3）候选**：a) 链上企业年报营收（QC06 已定口径，但企业×链聚合表未建）b) 链上企业专利数（dwd_patent 293 万行可关联，但「份额=专利份额」语义漂移到创新集中而非市场集中）c) 链上企业数（每家 1/N → HHI≡退化为「有效企业数倒数」，无区分度，**否决**）

**建议倾向（不替甲方/唐绍祖拍）**：HHI + 营收份额。理由：链上企业长尾多，HHI 平方项天然稀释小企业份额噪声、对数据精度容忍度高；CR_N 的 N 值是一个额外决策点（少一个要拍的参数）；阈值体系成熟可借司法部分级叙事。风险：营收聚合表未建，解挂成本高于 CR_N 无差别（两者都卡在份额源）。

**决策点清单（交 human:唐绍祖）**：
1. HHI or CR_N（若 CR_N，N=4 还是 8）
2. 份额基准：营收 / 专利 / 其他（建议营收）
3. 统计对象：链内环节级（每环节一个集中度）还是全链级（一个数）——seed 现稿「企业分布」未明；calc-logic 旧稿是环节级（key_node），分叉待并
4. 输出形态：连续指数 or 分级（中高/中低）——calc-logic 旧稿是分级，若保留分级需阈值表
5. update_freq weekly 是否合理（营收年更，建议 yearly，与 CYCLE_STAGE 同步）

- **改前→改后**：
  - definition → `产业集中度指数（HHI 或 CR_N 待签）。份额基准与统计粒度待唐绍祖决策卡；企业份额源不存在（enterprise_industry_chain=0 行）。挂起不写可执行公式。禁止用 chain_score（链企匹配分）冒充市场份额`
  - formula → `挂起：两案骨架见 calc-logic 决策卡（HHI=Σ份额² / CR_N=TopN份额和）；解挂=算法签发+企业份额源落库`
  - source_tables → `["（缺口）企业×链份额表（enterprise_industry_chain=0 行；营收聚合未建）"]`
  - 矩阵：**补行** d1=draft/QC02+算法未签、d2=pending、d3=none、d4=mock
  - version 0.1.0 → 0.2.0；algorithm_type 保持 COMPUTE

### 风险点与待拍清单

1. **seed 与 calc-logic 已分叉**（企业集中度 vs 环节集中度分级）——无论签哪案，calc-logic 需重写并留分叉记录
2. `chain_score` 字段是**链企匹配置信分**不是市场份额，若被误用会造成语义事故——改后在 definition 明写禁止项
3. 现网 0 行意味着即使签了算法也无数据可算——解挂双条件（算法+数据），建议与 QC06 营收聚合表任务并轨
4. **待拍**：挂起方案；两案与 5 个决策点是否照此清单交唐绍祖

---

## 7. M_CHAIN_INTERNATIONALIZATION_INDEX（产业链国际化程度）★COMPUTE 交唐绍祖

### 现稿画像

- seed v0.1.0：`definition_status: pending_data_lead` + `formula_status: pending_algorithm`，**algorithm_type: COMPUTE**，**无 pending_ref**（QC 项缺失，definition 只写「口径与权重待确认」）
- formula：`pending_algorithm（海外企业占比*w1+海外专利占比*w2+进出口数据*w3）`
- source_tables：`dwd.industry_chain_enterprise`（不存在→漂移 0 行）+ `dwd.industry_chain_patent`（**不存在**）
- **无 calc-logic 文件**（89 个 CHAIN calc-logic 中无本条——文档缺口）
- **无矩阵行**

### 探库实测引用

- `industry_chain_enterprise` 不存在 / `enterprise_industry_chain` = 0 行
- `industry_chain_patent` 不存在；真源 `dwd_patent` 293 万行**无链字段**——专利挂链须经 `dwd_org_industry_chain_pat_dtl`（ODS 侧链专利明细，行数未核）+ 申请人名匹配（TECH_MATURITY_SCORE 同款路径，已知有匹配误差）
- 「进出口数据」：系统内**无进出口/海关源**（全库无此表），w3 项**无源**
- 「海外企业」判定：`dwd_org_base_info` 有 city/province 字段，海外企业判定规则（注册地境外？国别字段？）未定义

### 建议：挂起 + 候选公式骨架 + 决策点交唐绍祖

**候选公式骨架（两案，均不落 seed 可执行态）**：

- 案 A（专利侧单因子，现网最近源）：`国际化指数 = 链上专利中海外申请人专利占比`（海外=P-ctRY 申请人国别≠CN，dwd_patent 若无国别字段则用申请人名匹配海外机构名单——精度差，需核字段）
- 案 B（三因子加权，seed 现稿方向）：`指数 = w1×海外企业数占比 + w2×海外专利占比 + w3×进出口强度`——w3 无源，须供方新增或砍因子

**决策点清单（交 human:唐绍祖）**：
1. 因子集合：三因子（企业/专利/贸易）还是先落专利单因子（现网唯一近源）
2. 「海外」判定基准：申请人国别 / 企业注册地 / 专利同族含海外局（dwd_patent 无同族字段，若选此项需供方扩字段）
3. 权重 w1/w2/w3（若多因子）：等权还是差异化
4. 指数形态：0-100 分还是占比直读（%）
5. 是否与 M_CHAIN_SZ_ADVANTAGE_SCORE 的城市对标框架统一（对「国际化」做城市对比时口径复用）

- **改前→改后**：
  - definition → `产业链国际化程度指数。因子集合与海外判定基准未签（无 QC 号，需补登记决策项）；企业份额源 0 行、链专利表不存在、进出口无源。挂起不写可执行公式`
  - formula → `挂起：两案骨架见本卡（案A 专利海外占比单因子 / 案B 三因子加权）；解挂=因子签发+对应源落库`
  - source_tables → `["（缺口）enterprise_industry_chain（0 行）", "（缺口）industry_chain_patent（不存在；真源 dwd_patent 无链字段，须经 dwd_org_industry_chain_pat_dtl 挂链）", "（缺口）进出口数据（全库无源）"]`
  - 补 pending_ref：**新开决策项**（建议 QC12 或并入 QC02 组）——本条现无 QC 号是登记缺口
  - 矩阵：**补行** d1=draft/待补 QC 号、d2=pending、d3=none、d4=mock
  - calc-logic：**新建文件**（挂起版，含两案骨架与决策点）——这是 89 文件清单中本条缺失的补齐动作
  - version 0.1.0 → 0.2.0；algorithm_type 保持 COMPUTE

### 风险点与待拍清单

1. **无 QC 号**是本条独有登记缺口——不补号则决策无追踪载体，建议随本卡一并拍「开新 QC 项」
2. 进出口因子无源——若甲方坚持三因子，须列入供方新增需求（成本项），倾向案 A 起步
3. 申请人名匹配海外机构（案 A 兜底路径）有已知误差（TECH_MATURITY_SCORE 先例）——指数作 COMPUTE 交付时误差叙事要进 calc-logic
4. **待拍**：挂起方案；补 QC 号；两案与 5 决策点交唐绍祖

---

## 8. M_CHAIN_SZ_COMPLETENESS（深圳产业链完整度）

### 现稿画像

- seed v0.1.0：`pending_ref: QC01`，`definition_status: pending_data_lead`
- definition：深圳覆盖的产业链环节数占全链环节数比例；完整度口径（按节点数/按企业覆盖/按产值覆盖）**三选一待甲方确认**
- formula：`pending_algorithm（深圳覆盖环节数 / 全链环节数 * 100）`
- source_tables：`dwd.industry_chain_enterprise`（漂移 0 行）+ `dwd.industry_chain`
- calc-logic：`covered_nodes/total_nodes`；源 `chain_sz_panorama`（不在现网）
- **无矩阵行**
- 注意：SVC 侧 `M_SVC_SZ_CHAIN_COMPLETENESS` 已拍挂起（服务链完整度），但**链条轴不同**（SVC=服务链六环节，本条=产业链环节），两者互不替代——本条是产业链轴，有 `dwd_industry_chain_info` 环节字典可依

### 探库实测引用

- `dwd_industry_chain_info`（43 链、环节字典 industry_link_code 层级）**有数**——分母侧「全链环节数」可算
- `enterprise_industry_chain` = 0 行——「深圳覆盖环节」判定依赖链上企业挂接（企业×环节×地域），分子侧**无源**
- 产值路径：QC06 营收口径已定但企业×链营收聚合未建——产值覆盖分母同样无源

### 建议：锁目标口径 + QC01 三案对照表（不替甲方拍）

**QC01 三选一案**（各有含义/数据依赖/风险）：

| 方案 | 含义 | 数据依赖 | 风险 |
|---|---|---|---|
| 甲：按节点数 | 深圳有主体入驻的环节数 / 全链环节总数 | 环节字典（**已有**）+ 主体×环节挂接×深圳地域（**0 行**） | 「有主体」阈值未定（1 家即算覆盖？）；环节粒度影响大（拆细则覆盖率虚降） |
| 乙：按企业覆盖 | 深圳链上企业数 / 全链企业数 | 链上企业名录（tags 表**有**）+ 地域字段（**有**）——**三案中唯一现网可算** | 语义漂移：企业数比例≠「链的完整度」（深圳企业多但都挤在下游也算高）；与「环节覆盖」直觉冲突，甲方易质疑 |
| 丙：按产值覆盖 | 深圳链上企业营收合计 / 全链营收合计 | 企业×链营收聚合（**未建**，QC06 后置任务） | 口径最贴产业政策叙事，但解挂最慢；营收年份选择（哪年？）要拍 |

**建议倾向（不替甲方拍）**：甲（按节点数）——语义最贴「链完整/断链」直觉（断在哪一环可视化），与图谱全景页（chain_panorama 节点视角）同轴；「1 家即覆盖」阈值作随附决策点。乙虽现网可算但语义易被挑战；丙解挂最慢可作二期升级。

- **改前→改后**：
  - definition → `深圳产业链完整度 = 深圳覆盖环节数 / 全链环节数 × 100%。覆盖口径三选一挂 QC01（节点数/企业覆盖/产值覆盖，对照表见 calc-logic）；分子侧企业×环节×深圳挂接 0 行。禁止用 chain_sz_panorama 壳或演示 8 链固定值冒充`
  - formula → `目标口径（以案甲为例）：SELECT COUNT(DISTINCT link) WHERE 深圳 INTO SELECT COUNT(DISTINCT link) FROM dwd_industry_chain_info WHERE chain_id={chain_id} × 100（覆盖判定阈值与三案选择待 QC01；缺口：企业×环节×深圳挂接无源）`
  - 矩阵：**补行** d1=draft/QC01、d2=pending、d3=partial（分母字典有、分子挂接无）、d4=mock
  - version 0.1.0 → 0.2.0

### 风险点与待拍清单

1. 三案语义差异大（同一链可能算出 30% / 70% / 55% 三种「完整度」）——**必须**甲方拍，本卡只给对照与倾向
2. 环节字典粒度（industry_link_code 层级取几级）是隐藏决策点——随 QC01 一并问
3. 与 SVC 服务链完整度（已挂起）同名不同轴——UI 侧不得互相引用，两卡都要写清轴定义
4. **待拍**：倾向案甲是否作为团队默认建议随 QC01 上会；公式骨架按案甲写是否认可

---

## 9. M_CHAIN_SZ_ADVANTAGE_RANK（深圳优势排名）

### 现稿画像

- seed v0.1.0：`pending_ref: QC08`，`definition_status: pending_data_lead` + `formula_status: pending_algorithm`
- definition：深圳在产业链中的优势排名（与对标城市比较）；对标城市集合同 QC08
- formula：`pending_algorithm（RANK() OVER ORDER BY 优势评分 DESC）`
- source_tables：`派生自 M_CHAIN_SZ_ADVANTAGE_SCORE`
- calc-logic：`RANK() OVER ORDER BY advantage_index DESC`；源 `chain_sz_advantage`（8 行，不在现网）
- **矩阵行存在**：d1=draft/QC08、d2=pending/provisional、d3=partial（「派生自 ADVANTAGE_SCORE」）、d4=mock
- 父指标 M_CHAIN_SZ_ADVANTAGE_SCORE（v1，2026-08-27）：四维（企业/专利/政策/人才）加权 MODEL，**默认对标 C={北京、上海、广州、深圳}**，algo_server_location 已落 demo-algo-science

### 探库实测引用

- `chain_sz_advantage` ADS 壳不在现网
- 父指标 ADVANTAGE_SCORE 的源（tags/base_info/patent/policy/scholar 全系 dwd 表）**均有数**——派生链路「可算但未落 ADS」
- QC08 🟡：对标城市集合「北上广深苏杭（与企业域 Q016 对标集合宜一并确认）」——父指标代码现用 C={北上广深}（无苏杭），**决策清单与实现已不一致**

### 建议：锁目标口径 + QC08 城市集合候选与排序键决策点

- **锁定口径**：指定产业链上，深圳在已签对标城市集合内按 M_CHAIN_SZ_ADVANTAGE_SCORE 降序的名次（RANK，并列同名次）
- **排序键锁定**：唯一排序键 = ADVANTAGE_SCORE 综合分（四维加权，父指标已 v1）；**不引入第二排序键**（如专利数破并列），破并列规则（并列取小名次/平均名次）作决策点
- **QC08 对标城市集合候选**：
  - 候选 1：北上广深（父指标现实现 C，4 城）
  - 候选 2：北上广深苏杭（决策清单现默认建议，6 城）——注意与企业域 Q016 对标集宜对齐（跨域一致性问题）
  - 候选 3：重点产业链城市（按链定制，如半导体加无锡/成都）——精准但每链要拍一次，管理成本高
- **建议倾向（不替甲方拍）**：候选 2（北上广深苏杭），理由：决策清单已有倾向、6 城样本使排名区分度更好、与企业域 Q016 一并确认可跨域统一；代价：父指标 C 集要扩 2 城重算（demo-algo-science 改动小）
- **改前→改后**：
  - definition → `深圳在已签对标城市集合（QC08 未签；候选：北上广深 / +苏杭 / 按链定制）内按 M_CHAIN_SZ_ADVANTAGE_SCORE 降序的名次。父指标签名后本条即派生可算；排名并列规则待签`
  - formula → `目标口径：RANK() OVER (PARTITION BY chain_id ORDER BY score DESC) FROM <M_CHAIN_SZ_ADVANTAGE_SCORE 按城市展开>（缺口：QC08 城市集合未签；ADS 落表未建）`
  - 矩阵：d3=partial 保留（父可算、子未落表）；其余不动
  - version 0.1.0 → 0.2.0
  - **不写 metric: 引用**到父（避免父 QC08 未签传导误解为子已签）——参照 AVG_DEPTH「不写 metric: 引用」先例

### 风险点与待拍清单

1. **决策清单（苏杭）与父指标实现（北上广深）已分叉**——若 QC08 拍 6 城，父指标需重算+重落 ADS，本条排名随动——改后 definition 要写明「随父指标集合联动」
2. 与企业域 Q016 对标集的**跨域一致性**：若两域拍不同集合，同一页面（产业对比）会出现两套「对标城市」，UI 叙事冲突——建议 QC08 上会时把 Q016 捆绑同拍
3. RANK 并列规则（取小/平均）虽小但影响展示（「并列第 2」vs「第 3」）——随 QC08 附带拍
4. **待拍**：候选 2 倾向是否作为团队建议；派生锁定+不写 metric: 引用是否认可

---

## 附：本卡未做的事（边界声明）

- 未改任何 seed / 矩阵 / calc-logic 文件（只读任务）
- 未替甲方拍任何 QC 项（QC01/02/04/08/09 全部维持 🟡）
- 未替唐绍祖签任何算法（CONCENTRATION / INTERNATIONALIZATION / CHOKE / SEVERITY 决策点仅列清单）
- INTERNATIONALIZATION 的 QC 号补登记、LAYOUT_RECOMMEND 废止后的 UI 摘卡，均为拍板后另开任务的项
