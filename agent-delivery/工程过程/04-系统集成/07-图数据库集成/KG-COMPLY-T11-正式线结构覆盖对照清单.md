# T11 正式线结构覆盖对照清单（KG-COMPLY-T11-COVERAGE）

- 原清单：唐绍祖，书面决定回填：李周
- 日期：2026-11-12
- 适用：`KG-COMPLY-LOAD-T11`（执行人 李周）、WBS-07-00G / 00H 责任人消费
- 基线来源：STRUCT §1 + [T07 总账对账口径](./KG-COMPLY-T07-总账对账口径.md) + **2026-11-12 15:40 现场 `SHOW SPACES` / `SHOW TAGS` / `SHOW EDGES` / `DESCRIBE` 实测**
- 书面依据：2026-11-12 淮政玮飞书答复，六项决定见 §七。T11 仅做只读结构对照。

---


## 一、本期范围与对照口径

淮政玮于 2026-11-12 书面确认，正式线本期不建设，T11 继续以 `10.50.75.136:9669` 的 `demo_gkx_chain` 作结构对照。本期沿用该实例和空间。正式线采用与当前演示库一致的逻辑结构，对接上线后切换到线上总集的大批量数据源。正式空间名留待后续决定。

15:40 现场 `SHOW SPACES` 记录仅有 `demo_gkx_chain`，与 [architecture-baseline](../../../architecture-baseline.md) v2.2.15 的本期空间安排一致。A 段 9 个 Tag 和 B 段 24 条关系继续作为后续正式线的最低结构覆盖基线。「不适用（本期）」表示本期无正式线实例和空间可核验，表中的演示库结构及边数保留供后续对照。技术点层单列。

---

## 二、A 段：七要素层 9 个 Tag（最低覆盖，逐行）

「正式线状态」采用 §一 的本期范围，VID 和字段列保留后续对照所需的演示库基线。

| # | Tag | 正式线状态 | 必须一致的 VID 规则（demo 实测样例） | demo 属性字段 | 备注 |
|---|---|---|---|---|---|
| A1 | `enterprise` | 不适用（本期） | `ent:<32位hex>`，例 `ent:0002a237784776879ffbbe8645661cbc` | `name` `enterprise_code` `chain_role` `weight` `props` `node_type` | 属性最全，`node_type` 用于区分同类节点 |
| A2 | `segment` | 不适用（本期） | `segment:<环节码>`，例 `segment:INB120401010102` | `name` `segment_key` `chain_id` `chain_stage` `weight` `props` | 环节码只用 12 链 `INB12xx–25xx`，**禁止 INB17/18** |
| A3 | `research` | 不适用（本期） | **`inst:<institution_id>`**，例 `inst:ins_00016093458a42deab916030a51c1575` | `name` `props` | ⚠️ 前缀是 `inst:` 而**不是** `research:`，见 §六 陷阱 1 |
| A4 | `person` | 不适用（本期） | `person:<talent_id>`，例 `person:tal_000cf97faa054fa19eb1d579c949178f` | `name` `props` | |
| A5 | `paper` | 不适用（本期） | **无样例**（demo 内 0 个点） | `name` `props` | 演示库无点样例，后续以正式数据口径补充核验 |
| A6 | `patent` | 不适用（本期） | `patent:<patent_id>`，例 `patent:pat_000934c365dd480ebac3c7c0f5d7fa0e` | `name` `props` | |
| A7 | `project` | 不适用（本期） | **`proj:<project_id>`**，与 Tag 名不同形，例 `proj:prj_004142a37c174be38d0fb1051259fbc0` | `name` `props` | ⚠️ 前缀 `proj:`，见 §六 陷阱 2 |
| A8 | `policy` | 不适用（本期） | `pol:<policy_id>`，例 `pol:18318870` | `name` `weight` `props` | 唯一用 `pol:` 的 |
| A9 | `institution` | 不适用（本期） | **`institution:<32位hex>`**，例 `institution:000a2e639fab06e2a83f84871d620c8f` | `name` `institution_type` `weight` `props` | ⚠️ 与 A3 的 `inst:` 只差几个字母，极易混，见 §六 陷阱 1 |

**A 段合格标准**：9 行全部「同名 Tag + VID 规则一致」；属性**可升列，不得删除**（SDD §3.2 原话）。

---

## 三、B 段：七要素层 24 条必须边（最低覆盖，逐行）

24 条关系按 SDD 保留边型、端点和方向。本期正式线状态与 A 段一致，演示库边数沿用归档实测。

| # | M | 边型 | 端点方向 | demo 边属性字段 | 本期实测条数 | 正式线状态 | 备注 |
|---|---|---|---|---|---|---|---|
| B1 | M01 | `cooperate` | `person`→`person` | `weight` `props` | 2,525,789 | 不适用（本期） | |
| B2 | M02 | `cooperate` | `research`→`research` | `weight` `props` | 3,442,271 | 不适用（本期） | |
| B3 | M03 | `cooperate` | `person`→`research` | `weight` `props` | 0 | 不适用（本期） | 空态（源端点 100% 为企业） |
| B4 | M04 | `belong` | `person`→`research` | `weight` `props` | 72,099 | 不适用（本期） | |
| B5 | M05 | `belong` | `research`→`research` | `weight` `props` | 0 | 不适用（本期） | 空态 |
| B6 | M06 | `cite` | `paper`→`paper` | `weight` `props` | 0 | 不适用（本期） | 空态（无源） |
| B7 | M07 | `participate` | `person`→`project` | `weight` `props` | 0 | 不适用（本期） | 空态（无源） |
| B8 | M08 | `participate` | `research`→`project` | `weight` `props` | 17,426 | 不适用（本期） | |
| B9 | M09 | `author_of` | `person`→`patent` | `weight` `props` | 85,069 | 不适用（本期） | |
| B10 | M10 | `publish` | 见 L03 | `weight` `props` | 0 | 不适用（本期） | 空态 |
| B11 | M11 | `policy_relate` | 见 L03 | `weight` `props` | 0 | 不适用（本期） | 空态 |
| B12 | M12 | `policy_apply_to` | 见 L03 | `weight` `props` | 0 | 不适用（本期） | 空态 |
| B13 | M13 | `policy_apply_to` | 见 L03 | `weight` `props` | 0 | 不适用（本期） | 空态 |
| B14 | M14 | `policy_apply_to` | 见 L03 | `weight` `props` | 0 | 不适用（本期） | 空态 |
| B15 | M15 | `depends_on` | `segment`→`segment` | **`dependency_type`** `weight` `props` | 1,073 | 不适用（本期） | 多一个专用字段 |
| B16 | M16 | `cite` | 见 L03 | `weight` `props` | 0 | 不适用（本期） | 空态 |
| B17 | M17 | `participates` | `enterprise`→`segment` | **`chain_role` `participation_depth` `chain_score` `props`（无 `weight`）** | 178,731 | 不适用（本期） | 淮政玮确认沿用现有字段，见 §六 |
| B18 | M18 | `participates` | `institution`→`segment` | 同 B17 | 0 | 不适用（本期） | 空态 |
| B19 | M19 | `research_coop` | `research`→`research` | `weight` `props` | 0 | 不适用（本期） | 空态（与 M02 同源重复） |
| B20 | M20 | `talent_coop` | `person`→`person` | `weight` `props` | 0 | 不适用（本期） | 空态（与 M01 同源重复） |
| B21 | M21 | `service_provide` | 见 L03 | `weight` `props` | 0 | 不适用（本期） | 空态 |
| B22 | M22 | `cooperate` | `enterprise`→`enterprise` | `weight` `props` | 94,824 | 不适用（本期） | **形态不可用（501）**，见 §五 D3 |
| B23 | M23 | `supply` | 见 L03 | `weight` `props` | 0 | 不适用（本期） | 空态 |
| B24 | M24 | `parent_sub` | 见 L03 | `weight` `props` | 0 | 不适用（本期） | 空态 |

### 3.1 边型去重后只有 15 种

24 条 M 关系压在 15 个边型上（`cooperate` 装 4 条、`cite` 装 2 条、`belong`/`participate`/`participates` 各装 2 条、`policy_apply_to` 装 3 条，其余各 1 条）。**正式线建 schema 时按 15 个边型建，不要按 24 条建重名边型**——Nebula 同一空间内边型不能重名。

「空态」记录本期演示库的供数状态。后续正式线的最低结构覆盖仍按 24 条逻辑关系、15 个边型核对。

---

## 四、C 段：技术点层 B1–B6（结构保留，单列）

淮政玮确认保留技术点层现有结构。按 SDD §3.2，技术点层单列，不计入 A、B 两段的最低覆盖范围。

| # | 对象 | 类型 | demo 实测规模 | 结构决定 |
|---|---|---|---:|---|
| C1 | `tech_point` | Tag（10 字段：`technology_node_id` `name_zh` `name_en` `community_role` `weighted_degree` `community_id` `graph_release_id` `data_version` `description` `development_status`） | 19,430 | 保留现有结构 |
| C2 | `tech_paper` | Tag | 108,337 | 保留现有结构 |
| C3 | `tech_patent` | Tag | 126,484 | 保留现有结构 |
| C4 | `tech_institution` | Tag | 17,542 | 保留现有结构 |
| C5 | `tech_person` | Tag | 15,235 | 保留现有结构 |
| C6 | `tech_rel` | Edge | 541,428 | 保留现有结构 |
| C7 | `tech_has_paper` | Edge | 108,337 | 保留现有结构 |
| C8 | `tech_has_patent` | Edge | 172,644 | 保留现有结构 |
| C9 | `tech_has_person` | Edge | 111,578 | 保留现有结构 |
| C10 | `tech_has_institution` | Edge | 51,000 | 保留现有结构 |
| C11 | `tech_path_step` | Edge | 35,018 | 保留现有结构 |


> 边与点的比例差异是有意义的：`tech_has_paper` 108,337 与 `tech_paper` 108,337 是 **1:1**；而 `tech_has_patent` 172,644 / `tech_patent` 126,484 ≈ **1.36:1**、`tech_has_person` 111,578 / `tech_person` 15,235 ≈ **7.3:1**、`tech_has_institution` 51,000 / `tech_institution` 17,542 ≈ **2.9:1**。说明同一专利/人才/机构会被多个技术点引用——正式线若复用，**不要以为点边是一对一**。

> SDD 概括为「5 Tag + 6 边」，与实测一致（Tag：`tech_point` / `tech_paper` / `tech_patent` / `tech_institution` / `tech_person`；边：`tech_rel` / `tech_has_paper` / `tech_has_patent` / `tech_has_person` / `tech_has_institution` / `tech_path_step`）。

**上线后随线上总集数据源重算技术点层指标。** 演示库的 `tech_point.weighted_degree` 只作为本期实测记录，正式指标取上线后重算值。现有指标与边集差异见 [T02/T09 验收记录](./KG-COMPLY-ACCEPT-T02-T09-技术验收记录.md)。

---

## 五、D 段：「不适用」清单（每项都有书面理由）

| # | 项 | 为什么不适用 |
|---|---|---|
| D1 | **把当前演示空间名作为正式线定名** | 本期沿用 `demo_gkx_chain`，后续正式空间名另行决定。执行器按 T13 参数化空间名。 |
| D2 | **本期批号体系 `comply-2026111x-t0x`** | 批号只用于本期追踪溯源。正式线批号体系可不同（SDD §3.2 明写「批号体系可与本期不同」）。**要继承的是「必须打批号」这条纪律，不是具体批号值。** |
| D3 | **M22 的当前数据形态（企业→企业 94,824 条碎片化合作网）** | 边型 `cooperate` 属于后续正式线最低结构覆盖（见 B22），但**这批数据的形态被判定为 501「有数据但不可用」**（碎片化、无法支撑产业链合作分析）。正式线若要这块，必须按正式定义重建，不能把这 94,824 条照搬。 |
| D4 | **`apply_to` / `support` / `belongs_to` 三条历史混装边** | 共 22,273 条（10,957 + 10,957 + 359），端点语义与 M12–M18 均不符，是 T06 的处理对象。正式线**不需要复制这批历史包袱**。 |
| D5 | **`institution`→`institution` 的 `participates` 34,769 条** | 同上，历史混装，不属 M17/M18。正式线不要复制。 |
| D6 | **演示库现有技术点指标作为正式指标** | 技术点层保留现有结构。上线后随线上总集数据源重算，演示库的 `weighted_degree` 仅供本期对照。 |

---

## 六、E 段：VID 与边属性的对照口径

以下为演示库实测结构与淮政玮书面确认的沿用口径。

### 陷阱 1：`research` 的前缀是 `inst:`，`institution` 的前缀是 `institution:`

| Tag | VID 前缀 |
|---|---|
| `research`（科研机构，七要素层） | `inst:` |
| `institution`（服务机构，历史 Tag） | `institution:` |

两者只差几个字母，且都表示「机构」，但一个是七要素层的科研机构、一个是历史服务机构 Tag。**正式线照抄时极易串成一套**，导致 M02/M04 的机构点落到错误的 Tag 上。

### 陷阱 2：`project` 的 Tag 名与前缀不同形

Tag 叫 `project`，VID 前缀是 `proj:`（例 `proj:prj_...`）。`patent` 则前后一致（`patent:pat_...`）。建 schema 时别按「Tag 名 + 冒号」的直觉写。

### 陷阱 3：`first_year` 和 `participates` 的属性口径

```sql
DESCRIBE EDGE participates;
-- chain_role, participation_depth, chain_score, props   ← 没有 weight
DESCRIBE EDGE cooperate;
-- weight, props
```

SDD §3.2 写「24 条必须边 + 边属性 `weight` / `props` / `first_year`」，但实际：

- **`participates` 没有 `weight`**，改用 `chain_role` / `participation_depth` / `chain_score`；
- **`first_year` 不是独立列**，它存在于 `props` 这个 JSON 字符串里（实测 T02 的 props 为 `{"first_year":2023,...,"batch":"comply-20261111-t02",...}`）。

淮政玮确认沿用实测结构。`first_year` 放在 `props`，`participates` 继续使用 `chain_role`、`participation_depth`、`chain_score` 和 `props`。

---


## 七、F 段：淮政玮书面确认的六项决定

依据 2026-11-12 淮政玮给李周的飞书书面回复，回填原待确认事项。

| # | 原待确认事项 | 书面决定 |
|---|---|---|
| F1 | 正式线实例落点 | 本期和 T11 均不建设正式线。本期不新起实例，继续使用 `10.50.75.136:9669`。 |
| F2 | 正式空间名 | 本期不新建空间，继续使用 `demo_gkx_chain`。正式空间名不在 T11 另定，本期不建 `gkx_chain`。正式线沿用当前逻辑结构，对接上线后切换至线上总集的大批量数据源。 |
| F3 | VID 规则 | 沿用演示库。科研机构 `research` 用 `inst:`，服务机构 `institution` 用 `institution:`，项目 `project` 用 `proj:`。 |
| F4 | `first_year` | 沿用现有结构，存入 `props`。 |
| F5 | `participates.weight` | 不增设 `weight`。继续使用 `chain_role`、`participation_depth`、`chain_score` 和 `props`。 |
| F6 | 技术点层 | 保留现有结构。上线后随线上总集数据源重算，演示库的 `weighted_degree` 仅用于本期对照。 |

本清单用于结构对照，供 WBS-07-00G / 00H 参考。T11 继续只读，本期建设范围以以上书面决定为准。

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

## 九、后续对照用法

1. A 段 9 行和 B 段 24 行作为后续最低结构覆盖基线，正式线具备核验条件时逐行对照。
2. C 段记录技术点层的结构及上线重算口径，D 段列明具体不适用的项目。
3. WBS-07-00G / 00H 以 E 段的 VID 和属性口径及 F 段的书面决定为准。
