# T11 正式线 `gkx_chain` 结构覆盖对照清单（KG-COMPLY-T11-COVERAGE）

- 作者：唐绍祖
- 日期：2026-11-12
- 适用：`KG-COMPLY-LOAD-T11`（建议执行人 李周）、WBS-07-00G / 00H 责任人消费
- 基线来源：STRUCT §1 + [T07 总账对账口径](./KG-COMPLY-T07-总账对账口径.md) + **2026-11-12 15:40 现场 `SHOW SPACES` / `SHOW TAGS` / `SHOW EDGES` / `DESCRIBE` 实测**
- 约束：**本任务不往 `gkx_chain` 写任何点边**，本文件全程只读

---

## 一、先说一个必须知道的前提

**正式线 `gkx_chain` 目前不存在。**

2026-11-12 现场执行 `SHOW SPACES`（`10.50.75.136:9669`），返回结果只有一个：

```
demo_gkx_chain
```

这与 [architecture-baseline](../../../../architecture-baseline.md) v2.2.15 的决议一致——「只迁 `demo_gkx_chain`；**不建正式名 `gkx_chain`**」。也就是说，本期全部合规成果都落在演示空间里，正式线要不要建、什么时候建、建在哪个实例，**尚未决策**。

### 1.1 这决定了本清单的口径

SDD T11 卡给了退路：「只读 `gkx_chain` schema（若有权限）+ 本地基线文件；**无权限则基于 STRUCT 文档对照**」。

现在不是「没权限」，是**空间本身没有**。所以本清单：

- **所有行一律标「待补」**——因为正式线一行都还没有；
- 我用来对照的，是 `demo_gkx_chain` 的**真实 schema**（不是文档推测），这样正式线照单建的时候，属性名和类型能一次对上；
- 「不适用」项**必须有书面理由**，且理由要区分「本期数据形态不可照搬」与「正式线根本不需要」。

> ⚠️ 不要把本清单读成「正式线已经差这么多就欠这么多」。它是**结构覆盖要求**，不是进度欠账。

---

## 二、A 段：七要素层 9 个 Tag（最低覆盖，逐行）

「正式线状态」列：**待补** = 必须建；**不适用** = 有书面理由不建。

| # | Tag | 正式线状态 | 必须一致的 VID 规则（demo 实测样例） | demo 属性字段 | 备注 |
|---|---|---|---|---|---|
| A1 | `enterprise` | 待补 | `ent:<32位hex>`，例 `ent:0002a237784776879ffbbe8645661cbc` | `name` `enterprise_code` `chain_role` `weight` `props` `node_type` | 属性最全，`node_type` 用于区分同类节点 |
| A2 | `segment` | 待补 | `segment:<环节码>`，例 `segment:INB120401010102` | `name` `segment_key` `chain_id` `chain_stage` `weight` `props` | 环节码只用 12 链 `INB12xx–25xx`，**禁止 INB17/18** |
| A3 | `research` | 待补 | **`inst:<institution_id>`**，例 `inst:ins_00016093458a42deab916030a51c1575` | `name` `props` | ⚠️ 前缀是 `inst:` 而**不是** `research:`，见 §五 陷阱 1 |
| A4 | `person` | 待补 | `person:<talent_id>`，例 `person:tal_000cf97faa054fa19eb1d579c949178f` | `name` `props` | |
| A5 | `paper` | 待补 | **无样例**（demo 内 0 个点） | `name` `props` | 正式线若建，VID 规则需新定并留档 |
| A6 | `patent` | 待补 | `patent:<patent_id>`，例 `patent:pat_000934c365dd480ebac3c7c0f5d7fa0e` | `name` `props` | |
| A7 | `project` | 待补 | **`proj:<project_id>`**，与 Tag 名不同形，例 `proj:prj_004142a37c174be38d0fb1051259fbc0` | `name` `props` | ⚠️ 前缀 `proj:`，见 §五 陷阱 2 |
| A8 | `policy` | 待补 | `pol:<policy_id>`，例 `pol:18318870` | `name` `weight` `props` | 唯一用 `pol:` 的 |
| A9 | `institution` | 待补 | **`institution:<32位hex>`**，例 `institution:000a2e639fab06e2a83f84871d620c8f` | `name` `institution_type` `weight` `props` | ⚠️ 与 A3 的 `inst:` 只差几个字母，极易混，见 §五 陷阱 1 |

**A 段合格标准**：9 行全部「同名 Tag + VID 规则一致」；属性**可升列，不得删除**（SDD §3.2 原话）。

---

## 三、B 段：七要素层 24 条必须边（最低覆盖，逐行）

「正式线状态」全为**待补**（24 条无例外，SDD 要求「同名同端点同方向，一字不改」）。

| # | M | 边型 | 端点方向 | demo 边属性字段 | 本期实测条数 | 备注 |
|---|---|---|---|---|---|---|
| B1 | M01 | `cooperate` | `person`→`person` | `weight` `props` | 2,525,789 | |
| B2 | M02 | `cooperate` | `research`→`research` | `weight` `props` | 3,442,271 | |
| B3 | M03 | `cooperate` | `person`→`research` | `weight` `props` | 0 | 空态（源端点 100% 为企业） |
| B4 | M04 | `belong` | `person`→`research` | `weight` `props` | 72,099 | |
| B5 | M05 | `belong` | `research`→`research` | `weight` `props` | 0 | 空态 |
| B6 | M06 | `cite` | `paper`→`paper` | `weight` `props` | 0 | 空态（无源） |
| B7 | M07 | `participate` | `person`→`project` | `weight` `props` | 0 | 空态（无源） |
| B8 | M08 | `participate` | `research`→`project` | `weight` `props` | 17,426 | |
| B9 | M09 | `author_of` | `person`→`patent` | `weight` `props` | 85,069 | |
| B10 | M10 | `publish` | 见 L03 | `weight` `props` | 0 | 空态 |
| B11 | M11 | `policy_relate` | 见 L03 | `weight` `props` | 0 | 空态 |
| B12 | M12 | `policy_apply_to` | 见 L03 | `weight` `props` | 0 | 空态 |
| B13 | M13 | `policy_apply_to` | 见 L03 | `weight` `props` | 0 | 空态 |
| B14 | M14 | `policy_apply_to` | 见 L03 | `weight` `props` | 0 | 空态 |
| B15 | M15 | `depends_on` | `segment`→`segment` | **`dependency_type`** `weight` `props` | 1,073 | 多一个专用字段 |
| B16 | M16 | `cite` | 见 L03 | `weight` `props` | 0 | 空态 |
| B17 | M17 | `participates` | `enterprise`→`segment` | **`chain_role` `participation_depth` `chain_score` `props`（无 `weight`）** | 178,731 | ⚠️ **唯一没有 `weight` 的边型**，见 §五 陷阱 3 |
| B18 | M18 | `participates` | `institution`→`segment` | 同 B17 | 0 | 空态 |
| B19 | M19 | `research_coop` | `research`→`research` | `weight` `props` | 0 | 空态（与 M02 同源重复） |
| B20 | M20 | `talent_coop` | `person`→`person` | `weight` `props` | 0 | 空态（与 M01 同源重复） |
| B21 | M21 | `service_provide` | 见 L03 | `weight` `props` | 0 | 空态 |
| B22 | M22 | `cooperate` | `enterprise`→`enterprise` | `weight` `props` | 94,824 | **形态不可用（501）**，见 §四 D3 |
| B23 | M23 | `supply` | 见 L03 | `weight` `props` | 0 | 空态 |
| B24 | M24 | `parent_sub` | 见 L03 | `weight` `props` | 0 | 空态 |

### 3.1 边型去重后只有 15 种

24 条 M 关系压在 15 个边型上（`cooperate` 装 4 条、`cite` 装 2 条、`belong`/`participate`/`participates`/`policy_apply_to` 各装 2 条、其余各 1 条）。**正式线建 schema 时按 15 个边型建，不要按 24 条建重名边型**——Nebula 同一空间内边型不能重名。

「空态」在这一段只表示**本期没灌数**，不代表正式线不建 schema。**24 条边的 schema 全部要建。**

---

## 四、C 段：技术点层 B1–B6（可选夹带，不计入最低覆盖）

按 SDD §3.2，技术点层是**可选**：正式线可用可不用；不用的话需一句书面说明，**不影响**「结构至少盖住 M01–M24」的验收口径。

| # | 对象 | 类型 | demo 实测规模 | 正式线状态 |
|---|---|---|---:|---|
| C1 | `tech_point` | Tag（10 字段：`technology_node_id` `name_zh` `name_en` `community_role` `weighted_degree` `community_id` `graph_release_id` `data_version` `description` `development_status`） | 19,430 | 可选 |
| C2 | `tech_paper` | Tag | 108,337 | 可选 |
| C3 | `tech_patent` | Tag | 126,484 | 可选 |
| C4 | `tech_institution` | Tag | 17,542 | 可选 |
| C5 | `tech_person` | Tag | 15,235 | 可选 |
| C6 | `tech_rel` | Edge | 541,428 | 可选 |
| C7 | `tech_has_paper` | Edge | 108,337 | 可选 |
| C8 | `tech_has_patent` | Edge | 172,644 | 可选 |
| C9 | `tech_has_person` | Edge | 111,578 | 可选 |
| C10 | `tech_has_institution` | Edge | 51,000 | 可选 |
| C11 | `tech_path_step` | Edge | 35,018 | 可选 |


> 边与点的比例差异是有意义的：`tech_has_paper` 108,337 与 `tech_paper` 108,337 是 **1:1**；而 `tech_has_patent` 172,644 / `tech_patent` 126,484 ≈ **1.36:1**、`tech_has_person` 111,578 / `tech_person` 15,235 ≈ **7.3:1**、`tech_has_institution` 51,000 / `tech_institution` 17,542 ≈ **2.9:1**。说明同一专利/人才/机构会被多个技术点引用——正式线若复用，**不要以为点边是一对一**。

> SDD 概括为「5 Tag + 6 边」，与实测一致（Tag：`tech_point` / `tech_paper` / `tech_patent` / `tech_institution` / `tech_person`；边：`tech_rel` / `tech_has_paper` / `tech_has_patent` / `tech_has_person` / `tech_has_institution` / `tech_path_step`）。

**若正式线复用技术点层，必须先解决一件事**：`tech_point.weighted_degree` 与当前边集不自洽（榜首存 1,010.90780192，当前入射+出射 2,914 边 Σconfidence÷100 = 1,478.05，比值 0.684 且逐点漂移）。详见 [T02/T09 验收记录 §四](./KG-COMPLY-ACCEPT-T02-T09-技术验收记录.md)。**把这个字段原样搬到正式线，等于把陈旧数据一起搬过去。**

---

## 五、D 段：「不适用」清单（每项都有书面理由）

| # | 项 | 为什么不适用 |
|---|---|---|
| D1 | **空间名 `demo_gkx_chain`** | `demo_` 是演示线命名。正式线叫 `gkx_chain`，**照搬空间名会把演示数据混进正式口径**。执行器必须参数化 space 名（这也是 T13 的要求）。 |
| D2 | **本期批号体系 `comply-2026111x-t0x`** | 批号只用于本期追踪溯源。正式线批号体系可不同（SDD §3.2 明写「批号体系可与本期不同」）。**要继承的是「必须打批号」这条纪律，不是具体批号值。** |
| D3 | **M22 的当前数据形态（企业→企业 94,824 条碎片化合作网）** | 边型 `cooperate` 本身要建（B22「待补」），但**这批数据的形态被判定为 501「有数据但不可用」**（碎片化、无法支撑产业链合作分析）。正式线若要这块，必须按正式定义重建，不能把这 94,824 条照搬。 |
| D4 | **`apply_to` / `support` / `belongs_to` 三条历史混装边** | 共 22,273 条（10,957 + 10,957 + 359），端点语义与 M12–M18 均不符，是 T06 的处理对象。正式线**不需要复制这批历史包袱**。 |
| D5 | **`institution`→`institution` 的 `participates` 34,769 条** | 同上，历史混装，不属 M17/M18。正式线不要复制。 |
| D6 | **技术点层 5 Tag + 6 边** | 可选夹带，不计入最低覆盖（见 C 段）。正式线若不用，需一句书面说明。 |

---

## 六、E 段：三处口径不一致，正式线建之前必须先定

这三条都是我在实测中发现、文档里没写清的，**不确认就建会返工**：

### 陷阱 1：`research` 的前缀是 `inst:`，`institution` 的前缀是 `institution:`

| Tag | VID 前缀 |
|---|---|
| `research`（科研机构，七要素层） | `inst:` |
| `institution`（服务机构，历史 Tag） | `institution:` |

两者只差几个字母，且都表示「机构」，但一个是七要素层的科研机构、一个是历史服务机构 Tag。**正式线照抄时极易串成一套**，导致 M02/M04 的机构点落到错误的 Tag 上。

### 陷阱 2：`project` 的 Tag 名与前缀不同形

Tag 叫 `project`，VID 前缀是 `proj:`（例 `proj:prj_...`）。`patent` 则前后一致（`patent:pat_...`）。建 schema 时别按「Tag 名 + 冒号」的直觉写。

### 陷阱 3：`participates` 是唯一没有 `weight` 的边型

```sql
DESCRIBE EDGE participates;
-- chain_role, participation_depth, chain_score, props   ← 没有 weight
DESCRIBE EDGE cooperate;
-- weight, props
```

SDD §3.2 写「24 条必须边 + 边属性 `weight` / `props` / `first_year`」，但实际：

- **`participates` 没有 `weight`**，改用 `chain_role` / `participation_depth` / `chain_score`；
- **`first_year` 不是独立列**，它存在于 `props` 这个 JSON 字符串里（实测 T02 的 props 为 `{"first_year":2023,...,"batch":"comply-20261111-t02",...}`）。

**给正式线的建议**：要么照本期实现（`first_year` 留在 `props` 内、`participates` 用三个专用字段），要么正式线升成独立列——但**必须二选一并写进契约**，不能一半一半。

---

## 七、F 段：待正式线责任人确认的 6 个问题

本清单只能写到「demo 侧结构长什么样」，下面 6 件必须由 WBS-07-00G / 00H 责任人回答，否则正式线无法开工：

1. **正式线建在哪个实例？** 当前 `10.50.75.136:9669` 只有 `demo_gkx_chain`。正式线是同实例新建空间，还是另一套集群？
2. **空间名最终是否叫 `gkx_chain`？** architecture-baseline v2.2.15 原话是「不建正式名 `gkx_chain`」，与 T11 的任务前提冲突，需要决策一句话。
3. **VID 规则是否照抄？** 尤其 §六 陷阱 1、2 两处不一致，要确认是「统一改名」还是「原样保留」。
4. **`first_year` 独立列还是留在 `props`？** 见陷阱 3。
5. **`participates` 要不要补 `weight`？** 见陷阱 3。
6. **技术点层是否复用？** 若复用，`weighted_degree` 必须先重算（见 C 段末）。

---

## 八、附录：实测证据

```
# 1) 空间清单（2026-11-12 15:40）
SHOW SPACES;
→ demo_gkx_chain            ← 无 gkx_chain

# 2) Tag 清单（15 个）
SHOW TAGS;
→ chain, enterprise, institution, paper, patent, person, policy,
  project, research, segment, tech_institution, tech_paper,
  tech_patent, tech_person, tech_point

# 3) Edge 清单（26 个）
SHOW EDGES;
→ apply_to, author_of, belong, belongs_to, cite, cooperate, depends_on,
  parent_sub, participate, participates, policy_apply_to, policy_relate,
  publish, regulate, research_coop, service_provide, supplies, supply,
  support, talent_coop, tech_has_institution, tech_has_paper,
  tech_has_patent, tech_has_person, tech_path_step, tech_rel

# 4) VID 样例（每个 Tag 取第一条）
enterprise       ent:0002a237784776879ffbbe8645661cbc
segment          segment:INB120401010102
research         inst:ins_00016093458a42deab916030a51c1575
person           person:tal_000cf97faa054fa19eb1d579c949178f
paper            （0 个点，无样例）
patent           patent:pat_000934c365dd480ebac3c7c0f5d7fa0e
project          proj:prj_004142a37c174be38d0fb1051259fbc0
policy           pol:18318870
institution      institution:000a2e639fab06e2a83f84871d620c8f
tech_point       tech_point:tcn_000f21ac06aceb9cdd0575e82d0d85fc
tech_paper       tech_paper:W1014257459
tech_patent      tech_patent:000217f8b059784d874d4565ad9bf95af20b648a24b6a4cf0741fd4a30a8f012
tech_institution tech_institution:ins_00011782b2254cc19c6050fc818e9cef
tech_person      tech_person:tal_00168343984a41dba926e78c6ba9daf3
```

---

## 九、给执行人的用法

1. **A 段 9 行 + B 段 24 行 = 最低覆盖**，逐行核对正式线是否具备；
2. **C 段单列**，不计入最低覆盖行数；
3. **D 段 6 项「不适用」** 直接引用，理由已在表内；
4. **E 段 3 处口径冲突先找责任人定性**，再让正式线动手；
5. 交 WBS-07-00G / 00H 责任人消费，**`gkx_chain` 一行都不写**。
