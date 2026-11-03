# spec · TS-INDDISC-01 · 科技全域态势：产业领域 ↔ 学科领域 关联筛选（修订版 v3）

> 状态：**v3 待批准**。改动一律停本地，等 `human:李伟` 走查，不 commit / 不 push。
> **v3 修订原因（2026-11-02 用户裁定，推翻 v2 的 D2 双下拉并存与 D5 路径A诚实提示）**：「学科领域挂载产业领域，前端只展示产业领域，选择完产业领域后台再去看是查询久新还是企业库。企业库就直接使用产业领域匹配，久新库就用挂到产业领域的学科领域去查，而不是两个筛选都展示。」
> **v3 可行性新证据（2026-11-02 实查）**：① 企业侧 `enterprise_base.org_id = enterprise_industry_chain.org_id` JOIN 已用真实 SQL 验证（INB1309 精确匹配 186,963 家；7 位父码 `LIKE 前缀%` 可含 9 位子码）；② 久新 `ads_geo_yearly_discipline_metrics`（10.15M 行，2000-2026）有 `location_id × statistics_year × subfield_id`（CITY/COUNTRY/PROVINCE/CONTINENT 级，湾区 9 市全有数），市域聚合与年度趋势可按子学科过滤；③ `dim.subfield_topic_map.subfield_id` 与久新 `ads_discipline_subfield.subfield_id` 同码（sub_ 前缀，252 个），产业→子学科反查结果可直接喂给久新。
> 监管人：`human:李伟` ｜ 前端 `lumen-ui-science-pc` ｜ BFF `lumen-svc-platform/gkxlumen-display` ｜ 数据参考 `demo-svc-platform/gkx-innov`（算法中台）
> v2 修订原因：v1 只查了 `/fields`，得出「`subfield_topic_map` 接不上」的结论。按用户指令回到**算法中台维护管理**核查三张映射后，路径成立为「产业(CL/INB) → 子学科(subfield_id) → 带子学科的要素」，但**事件侧仍不可达**。v1 的「换成 D-*」建议作废。

---

## 0. 用户指令（原文）

> 「现在调解时间范围数据并没有变化 ，并且刚才同步了一下 SYSINT-INDDISC-02-L01 任务已经做了 现在已经有产业领域和学科领域的关联绑定了，现在在分析学科领域筛选框是否可以换成产业领域并且和学科领域做关联查询久新要素数据和科创事件了」

> 「现在我看没有查到产业领域和学科领域的关联 ，现在算法中台的维护管理里面有映射关系，产业集群和产业的映射，子学科与专题的映射 技术节点与产业映射都有 先去查看算法中台再重新分析」

---

## 1. 算法中台实查结果（本轮一手证据）

### 1.1 维护管理三张映射（`demo-ui-system-test` → 网关 `/ops/**`，`@/views/ops/opsMenuConfig.ts`）

| 映射 | 菜单 / 路由 | 维护页 | 后端 | 落库 |
|---|---|---|---|---|
| 产业集群 ↔ 产业 | 产业集群映射 `/ops/cluster-map` | `ClusterMapPage.vue` | [IndustryClusterController.java](../../../repos/demo-svc-platform/gkx-innov/src/main/java/com/topcomm/gkx/innov/cluster/IndustryClusterController.java) `PUT /v1/industry-cluster-maps/{clusterId}` | `{dim}.industry_cluster` + `{dim}.industry_cluster_map` |
| 子学科 ↔ 专题（产业节点） | 子学科与专题映射 `/ops/subfield-topic` | `SubfieldTopicPage.vue` | [SubfieldTopicController.java](../../../repos/demo-svc-platform/gkx-innov/src/main/java/com/topcomm/gkx/innov/subfield/SubfieldTopicController.java) `/v1/subfield-topic-maps/{sync,link,stats,query}` | `{dim}.subfield_topic_map` |
| 技术节点 ↔ 产业 | 技术节点与产业映射（**本仓代码尚未出现**） | — | 方案：[方案-SYSINT-TECHMAP-02-L01.md](../工程过程/04-系统集成/02-对接三要素/方案-SYSINT-TECHMAP-02-L01.md) | `dwd_tech_node_industry_map`（`technology_node_id` + 产业 `node_id` + 集群） |

> ⚠️ 本仓 `opsMenuConfig.ts` 现只有前 2 项；第 3 项 `SYSINT-TECHMAP-02-L01` 在 registry 为 **in_progress**，代码仓内**搜不到 `dwd_tech_node_industry_map` 任何实现**。故本轮**不把技术节点映射当作已可用能力**，只登记为后续可选路径。

### 1.2 产业集群↔产业现状（`GET /v1/meta/industry-clusters?include_l0=true` 实测，:7090）

- 共 **15 个集群**（10 个 `sei` 战略性新兴 + 5 个 `fut` 未来产业），政策版本 `sz-10+5-2026`。
- **9 个已映射（mapped）**：
  CL-SEI-01 新一代信息技术 → INB1303 集成电路 / INB1323 传感器 / INB1309 人工智能 / INB1333 智能终端 / INB1306 软件与信息服务；
  CL-SEI-02 生物产业 → INB2503 生物医药；CL-SEI-06 智能网联新能源汽车 → INB1209；
  CL-SEI-08 低空经济与空天 → INB1236；CL-SEI-09 传统与创意产业 → INB1502；
  CL-FUT-01 未来制造 → INB1204 机器人 / INB1354 具身智能；CL-FUT-02 未来信息 → INB1306 / INB1309；
  CL-FUT-04 未来空间 → INB1236；CL-FUT-05 未来健康 → INB2505 合成生物。
- **6 个 pending_vendor（无产业）**：CL-SEI-03 新能源、CL-SEI-04 新材料、CL-SEI-05 高端装备、CL-SEI-07 绿色环保、CL-SEI-10 海洋产业、CL-FUT-03 未来能源。
- **影响**：这 6 个集群反查子学科必然为空 → UI 必须显式提示，禁止回落全量。

### 1.3 子学科↔专题现状

- 表 `demo_gkxlumenx_dim.subfield_topic_map`，列 `subfield_id / name_zh / node_id / node_name / industry_id(INB*) / industry_name / cluster_id(CL-*) / cluster_name / model_name`。
- 代码 [SubfieldTopicService.loadCatalog()](../../../repos/demo-svc-platform/gkx-innov/src/main/java/com/topcomm/gkx/innov/subfield/SubfieldTopicService.java#L434-L545) 的候选集就是「集群 CL-* → 产业 INB* → 产业链节点 node_id」三级，与本页需要的口径完全一致。
- 已映射规模：**已直连库复核（2026-11-01）**，`demo_gkxlumenx_dim.subfield_topic_map` = **390 行**，与 registry 备注（390 行 / 130 个已映射子学科，`SYSINT-TFMAP-02-L01` done）一致。

### 1.4 页面当前「学科领域」下拉其实是第四套编码（关键错配）

- 前端 `fetchSituationFields` → display `POST /v1/situation/fields` → innov `gkxlumenx_dim.tech_domain`，实测 10 项：
  `D-AI 人工智能 / D-AIC AI芯片 / D-AS 商业航天 / D-BIO 生物医药 / D-ES 储能 / D-IC 集成电路 / D-NE 新能源 / D-QI 量子信息 / D-ST 智能终端 / D-SW 工业软件`。
- **D-\* 与 CL-\*/INB\*/subfield_id 三者之间没有任何已落库映射**；中台三张映射都不覆盖 `tech_domain`。
- 事件 `POST /internal/innov/v1/bay/achievements` 实测只带 `domains:["D-NE"]` / `domain:"新能源"`，**无 `subfield_id`、无 CL/INB、无 node_id**。

### 1.5 二次复核（2026-11-01，按用户指令「先去查看算法中台再重新分析」）

#### 1.5.1 中台三张映射：线上数据实测（非引用）

`GET :7090/v1/meta/industry-clusters?include_l0=true` → 15 集群 / 9 `mapped` / 6 `pending_vendor`（与 §1.2 一致）。
逐集群反查 `GET :7090/v1/meta/industry-clusters/industry-subfields?cluster_id=...`：

| 集群 | map_status | L0 产业 | 反查到的子学科数 |
|---|---|---|---|
| CL-SEI-01 新一代信息技术 | mapped | INB1303 / INB1323 / INB1309 / INB1333 / INB1306 | **39** |
| CL-SEI-02 生物产业 | mapped | INB2503 | **25** |
| CL-SEI-06 智能网联新能源汽车 | mapped | INB1209 | **20** |
| CL-SEI-08 低空经济与空天 | mapped | INB1236 | **14** |
| CL-SEI-09 传统与创意产业 | mapped | INB1502 | **5** |
| CL-FUT-01 未来制造 | mapped | INB1204 / INB1354 | **13** |
| CL-FUT-02 未来信息 | mapped | INB1306 / INB1309 | **17** |
| CL-FUT-04 未来空间 | mapped | INB1236 | **14** |
| CL-FUT-05 未来健康 | mapped | INB2505 | **53** |
| CL-SEI-03/04/05/07/10、CL-FUT-03 | pending_vendor | 无 | 0（`emptyReason` 如实返回） |

- `POST :7099/v1/situation/subfields`（`{clusterId:"CL-SEI-01", industryId:"INB1303"}`）→ `code:0`、`mapped:true`、**7 条**子学科（计算机图形学与计算机辅助设计 / 计算数学 / 无机化学 / 离散数学与组合数学 / 材料化学 / 表面、涂层与薄膜 / 数值分析）。
- **结论①：中台的数据、innov 反查、display 透传、前端下拉，全链路已通。**

#### 1.5.2 页面实测：联动确实生效（上一轮「不联动」为误判）

直接对 `.arco-checkbox` 派发 `mousedown/mouseup/click` 后观测：
- 捕获请求体 `{"clusterId":"CL-SEI-01","industryId":"INB1303"}` → `/api/display/v1/situation/subfields` ✅
- 「学科领域」已解除禁用（无 `disabled` 类），占位文案回到「选择子学科（可多选）」✅
- 同批 `map/overview/influence/cluster/compare` 请求体均带 `selectedFieldValues:["CL-SEI-01","INB1303"]`

> **但真实用户点「集成电路」文字无反应**：Arco `cascader-option.js` 多选模式下只有 **Checkbox 的 onClick** 会选中（`isLeaf && !multiple` 才在 label 点击时选中）。这是交互体感问题，不是数据问题 → 需在 UI 上给出提示或改为可点文字。

#### 1.5.3 真正的断点：下游无消费方（本轮核心结论）

| 断点 | 证据 |
|---|---|
| display 筛选翻译层**不消费**产业编码 | `SituationController` Scope javadoc（L193-L210）明写「`selectedFieldValues`（学科领域）→ **不参与**：企业主表没有 domain 列」；L571-L573 同口径 |
| `subfieldIds` **全仓无消费方** | 全仓 grep：仅出现在 `/subfields` 返回体中，`map/overview/influence/cluster/compare` 均未读取 |
| element 侧无领域/子学科列 | `{dwd}.enterprise_base` 无 domain/subfield 列（javadoc L72-L74 诚实声明）；`gkxlumen-element` 全仓 grep `subfield` **0 命中** |
| 「产业 → 企业实体」JOIN 通路在现网数据上**不通** | 见下 |

#### 1.5.4 数据侧桥接可行性（MySQL 直查 `10.50.11.76` / demo 库）

| 表 | 行数 | 关键列 / 实测结论 |
|---|---|---|
| `dim.subfield_topic_map` | 390 | `subfield_id / node_id / industry_id / cluster_id`；CL-SEI-01+INB1303 的 `node_id` 实为 `INB13030201`(EDA) / `INB13030102`(晶圆制造材料) / `INB13030103`(后道封装材料) |
| `dwd.enterprise_industry_chain` | 388,824 | `org_id / enterprise_code / chain_code / node_id / node_name`；**`node_id` 为空 378,290 行**，非空仅 10,534 行且**全为 `node-bio-general`** |
| 同上 · `chain_code` | — | 只有 7 位 / 9 位两种；Top `INB1309`(186,964)、`INB170102`、`INB2503`(5,267)、`INB1204`(1,110)、`INB1354`(921)、`INB1323`(67)、`INB2505`(51)；**集成电路在链上用的是 `INB170101`，与集群表的 `INB1303` 不是同一套码** |
| `dwd.enterprise_base` | 189,115 | 无领域 / 子学科列（与 element javadoc 一致） |
| `ods.dwd_org_industry_tags` | 2,283,762 | `credit_code + industry_code(INB* 字面量)`，暂无与 `org_id` 的已核验连接键 |
| `dwd.industry_chain_entity_rel` | 178,731 | `node_id + entity_id + entity_type`（`node_id` 与 `subfield_topic_map.node_id` 口径待核） |
| `dwd.industry_chain_node` | 1,220 | 产业链节点字典 |
| `dwd.industry_chain_event_entity_rel` | 112 | 事件↔实体关系，样本过小 |

- **结论②**：`产业(INB) → 子学科(subfield) → node_id → 企业 → 久新要素` 这条 JOIN 在**现网数据上尚无可用干道**（`node_id` 98% 为空 + `INB1303`↔`INB170101` 两套码）。
- **结论③**：「查不到产业领域与学科领域的关联」的真因不是中台缺映射，而是**下游指标/要素侧根本没有领域维度列**，选了也不会改变数字。

---

## 2. 重新分析结论（能否做 / 边界）

| 目标 | 结论 | 依据 |
|---|---|---|
| 把「学科领域」换成**产业领域**（集群 CL → 产业 INB） | ✅ 可做，且数据源现成 | §1.2 接口公开可用；前端已有 `IndustrySelect` + `resolve.ts` |
| 产业领域 → **学科领域（子学科）** 反查 | ✅ 可做 | §1.3 `subfield_topic_map` 带 `cluster_id`/`industry_id` |
| 用子学科过滤**久新要素** | ✅ **可做**（v3 再更正：不走 enterprise JOIN，走久新自有学科维度） | v3 实查：市域聚合/趋势 → `ads_geo_yearly_discipline_metrics(subfield_id)`；论文 KPI → `ads_paper_profile.primary_topic_id → ads_discipline_topic`；课题 → `ads_research_problem_discipline.subfield_id`；成果 → `ads_research_outcome_discipline.topic_id → ads_discipline_topic`；专利/项目经费无学科维度 → 诚实 null+note |
| 用产业码过滤**企业要素** | ✅ **可做**（v3 新增） | v3 实测：`enterprise_base.org_id = enterprise_industry_chain.org_id`；`chain_code` 精确 + `LIKE 前缀%`（7 位父码含 9 位子码）；无命中自然返空，不回落全量 |
| 用子学科/产业过滤**科创事件** | ❌ **本轮不可做** | §1.4 事件只有 D-*；D-* ↔ 子学科/产业 无映射 |
| 产业领域多选「点文字没反应」 | ⚠️ 交互体感缺陷 | §1.5.2：Arco 多选级联只有 Checkbox 可选中 |
| 用技术节点映射做中转 | ⏸ 暂不可用 | §1.1 `dwd_tech_node_industry_map` 本仓未实装（in_progress） |

**因此最终形态不是「一个下拉替代另一个」，而是两套领域并存、各管一段：**

- **产业领域**（集群→产业，`CL-*/INB*`）→ 只作用于**久新要素**（且仅限带子学科的要素，经 `subfield_topic_map` 展开）。
- **技术领域**（原 `D-*`）→ 只作用于**科创事件**（现状已生效，仅需正名，不再叫「学科领域」）。

> 若用户要求「事件也必须按产业领域过滤」，必须新开数据侧任务给 `innovation_event` 补 `subfield_id` 或产业码，本轮不做、不由前端编造。

---

## 3. 待批准决策点（默认已落 §4）

- **D1 · 产业领域编码**：默认 = 产业集群(CL) → 产业(INB)（中台「产业集群映射」维护的那套），**放弃** v1 的「沿用 D-*」。
- **D2 ·（v3 用户裁定，推翻 v2）单下拉 + 后台分流**：前端**只展示**「产业领域（集群→产业）」一组筛选；「学科领域（细化）」下拉隐藏不渲染（内部仍自动反查 subfieldIds 随请求体下发）。后台按数据源分流：企业 → element 按产业码 `chain_code` 过滤；久新要素 → 按产业关联的子学科过滤；科创事件 → 仍走 D-* 技术领域（已实现，不动）。
- **D3 ·（v3 更新）要素范围**：企业 → 产业码 `chain_code` 过滤；论文/人才/项目/机构/课题/成果 → 子学科过滤；专利/项目经费无学科维度 → 过滤态返 null+note；园区/服务/期刊/会议维持现状口径。
- **D4 · 本轮是否允许改后端**：允许改 display BFF（Scope 翻译 + 透传）、element（chain_code 过滤）、python gkx_show_service（subfield_ids 过滤，无该参数时行为一字不变）；**不允许**在任何一层编造 join 或造数。
- **D5 ·（v3 用户裁定，推翻路径 A）筛选真生效**：删除路径 A 诚实提示，改为真实过滤生效说明；无维度指标（专利/项目经费）在过滤态诚实返 null+note，不补 0、不回落全量。
- **D8 ·（v3 新增）跨码组如实标注**：产业链上存在两套码（如集群表 INB1303 vs 链上 INB170101），按精确+前缀匹配，命多少算多少；命中 0 家就返空+说明，禁止编造码桥、禁止回落全量。
- **D6 ·（2026-11-01 用户裁定）修级联「点文字即选中」**：不改 Arco 原生行为的前提下让叶子文字点击可选中。
- **D7 ·（2026-11-01 用户裁定）时间范围问题实测定位并修**。

---

## 4. 实施方案（decision-complete）

### P0 · 产业领域下拉换成中台目录（前端 + display 透传）

**F1** `repos/lumen-svc-platform/gkxlumen-display/.../SituationController.java`
- 新增只读端点 `POST /v1/situation/industry-domains`：Feign 透传 innov `GET /v1/meta/industry-clusters?include_l0=true`（已实测公开可访问），返回 `{ clusters: [{ clusterId, name, mapStatus, l0: [{ industryId, name }] }] }`。
- 保留 `POST /v1/situation/fields` 不动（供事件侧「技术领域」用），但 javadoc 与响应字段里的「学科领域」措辞改为「技术领域（D-*）」。
- `@NoToken` 与 innov 侧放行方式对齐（仓内既有约定，漏配表现为全空）。

**F2** `repos/lumen-svc-platform/gkxlumen-display/.../feign/RemoteInnovClient.java`
- 新增 `industryClusters()`（`GET /v1/meta/industry-clusters`，`include_l0=true`）。

**F3** `repos/lumen-ui-science-pc/src/api/situation/index.ts`
- 新增 `fetchSituationIndustryDomains`（`defineApi` 双轨，风格对齐 `fetchSituationFields`）。

**F4** `repos/lumen-ui-science-pc/src/views/situation/overview/components/SituationFilterBar.vue`
- 原「学科领域」块改为 **产业领域**：三级/两级级联「集群 → 产业」，复用 `IndustrySelect`（该组件已 import）与 `@/lib/industryCluster/resolve.ts` 的 `toSelectedFieldSet`，值仍落到 `fieldValues: string[]`（`[clusterId, industryId]` 形态）。
- 新增 **技术领域** 块（源 `fieldOptions`，即 D-*），仅事件 Tab 显示；空态不编造选项。

**F5** `repos/lumen-ui-science-pc/src/views/situation/overview/index.vue`
- `loadFieldOptions()` 拆两路：`loadIndustryOptions()`（新）与 `loadFieldOptions()`（D-*，仅事件）。
- 要素 watch（L645-L711）改传 `industryFieldValues`；事件 watch 传 `techFieldValues`；两个 store 字段分离（禁止同一 `store.fieldValues` 双关两套编码）。
- 集群 `mapStatus !== 'mapped'` 时不请求下游，直接展示「该集群尚未映射产业」。

### P1 · 子学科反查 + 要素过滤（需 D3/D4 批准）

**F6** display `SituationController` 新增 `POST /v1/situation/subfields`
- 入参 `{ clusterId, industryId }`；出参 `{ subfieldIds: string[], mapped: boolean, source: 'subfield_topic_map' }`。
- 数据来源二选一（按 D4）：
  - 优先复用 innov `GET /v1/subfield-topic-maps/query`（需 token，display 走 `@NoToken` + 下游 `@Inner` 配对）；
  - 或新增只读反查接口 `GET /v1/subfield-topic-maps/by-industry?cluster_id=&industry_id=`（推荐，查询走已落库表，不在查询路径上同步/关联 —— 遵循 `SYSINT-06-19` 的约束）。
- 无命中时返回空数组 + `emptyReason`，**不回落全量**。

**F7** element 侧（仅在 D3 确认后）
- 对带子学科的要素表（人才 `ads_talent*` 的 `subfield_ids`）增加 `subfieldIds` 过滤参数并按真实列过滤。
- 无子学科列的要素（企业/园区/机构/服务）→ 响应 `field_filter_supported=false`，前端置灰并说明。

### P2 · 事件侧（本轮只正名 + 诚实提示）

- 事件筛选保留 D-*；下拉文案「技术领域」，并标注「事件侧只有技术领域编码，产业/学科领域暂不适用于事件」。
- 不新增任何伪造映射。

---

## 5. 验收标准

- P0：筛选栏出现「产业领域（集群→产业）」与「技术领域」两组；产业集群选项 15 条、未映射的 6 条肉眼可辨；`pnpm type-check` + `npm run build` 通过。
- P1：选 CL-SEI-01/INB1303 → `/subfields` 返回非空子学科集合并落到要素请求；选 CL-SEI-03（pending_vendor）→ 显式「尚未映射产业」，要素列表不返回全量。
- P2：事件选 D-NE 后条数与下拉标注一致；切产业领域不影响事件列表且 UI 有说明。
- **诚实性**：任何「不支持」场景都不得用全量数据冒充筛选结果。

## 6. 风险与边界

- `dwd_tech_node_industry_map` 未实装（SYSINT-TECHMAP-02-L01 in_progress）→ 本轮不依赖它。
- `subfield_topic_map` 行数/覆盖率引用 registry 备注，未直连库复核 → 开工前复核。
- 6 个集群 pending_vendor → 天然无子学科，必须显式提示。
- 事件侧无子学科 → 不承诺；需要则另开数据侧派单。
- 全部改动停本地，不 commit/push，等 `human:李伟` 走查。

## 7. 影响文件

| 层 | 文件 |
|---|---|
| BFF | `gkxlumen-display/.../SituationController.java`、`.../feign/RemoteInnovClient.java` |
| FE | `src/api/situation/index.ts`、`src/views/situation/overview/components/SituationFilterBar.vue`、`src/views/situation/overview/index.vue`、`src/lib/industryCluster/resolve.ts`（复用）、`src/stores/situation.ts`（字段拆分） |
| Element | `gkxlumen-element/.../EnterpriseController.java`（**本轮未动**：D5 走路径 A，见 §8） |
| 编排 | 本 spec、`tasks.md`、`checklist.md` |

## 8. 交接结论（2026-11-02）

### 8.1 本轮落地

| 项 | 结果 |
|---|---|
| 产业领域下拉（集群→产业） | 已上线，选项来自 `POST /v1/situation/industry-domains`（透传 innov），15 集群 / 9 mapped / 6 pending |
| 学科领域（细化）反查 | 已上线，`POST /v1/situation/subfields` → `subfield_topic_map`；CL-SEI-01+INB1303 实测 7 条 |
| 级联「点文字不选中」 | 已修：`IndustrySelect` `#option` 插槽把叶子文字点击转发给同行复选框；集群文字仍展开 |
| 时间范围不变 | 已修：根因是**后端收到区间但没用**（久新 KPI / 年度序列此前不带年份）。`map`/`overview` 现传 `year` 与 `year_from/year_to`；论文/专利/人才补「（xx年）」标签 |
| 要素筛选不生效 | 按 D5 走**路径 A**：已选产业/学科时展示一次性诚实提示，说明两套领域仅用于关联清单，指标数字不随之变化 |
| 事件侧正名 | 「技术领域（D-*）」仅事件 Tab 显示；0 条分三种情况（无数据 / 当期无记录 / 接口未上线） |
| 工程门 | `npx vue-tsc --build` exit 0；`npm run build` exit 0；浏览器实测通过 |

### 8.2 未做及其原因（不得被读成「已实现」）

- **T11 element 侧按 `subfieldIds` 过滤**：`gkxlumen-element` 全仓无 `subfield`；企业主表无领域/子学科列；`enterprise_industry_chain.node_id` 空 378,290/388,824（98%），非空仅 `node-bio-general`；集成电路在链上用 `INB170101`，与集群表 `INB1303` **两套码**。→ 现网数据尚无可用的「产业→企业」JOIN 干道，属**数据侧任务**，非前端可解。
- **路径 B 若启动需先补**：① `INB13xx ↔ INB17xx` 码桥；② 补齐 `enterprise_industry_chain.node_id`；③ 或给 `enterprise_base` / 指标宽表补 `subfield_id`。
- **技术节点映射**：`dwd_tech_node_industry_map` 在本仓仍未实装（SYSINT-TECHMAP-02-L01 in_progress），本轮不依赖。

### 8.3 走查提示

- display 服务已按新代码重建并重启在 `:7099`（旧实例关闭后重启，内存进程，非部署）。
- 全部改动停本地未提交，等 `human:李伟` 走查。

---

## 9. v3 实施方案（decision-complete，2026-11-02，待批准）

> 总原则：无 `subfield_ids` / `industryId` 参数时，各层行为**一字不变**；有参数时按真实列过滤；无维度指标返 null+note；命中 0 返空不回落。

### 9.1 python · `lumen-topic-py/gkx_show_service`（三端点增可选 `subfield_ids`）

**P1 `views/geo_indicator.py` · `factor_metrics`**（现 L381-588）
- 入参增 `subfield_ids: list[str] | None`。
- 有值时：paper/scholar/project/institution 四要素改查 `ads_geo_yearly_discipline_metrics`，`WHERE subfield_id IN (%s…) AND statistics_year=%s AND location_id IN (%s…)`，按市域 SUM；topic → `ads_research_problem_discipline` 按 `subfield_id IN` 计数；result → `ads_research_outcome_discipline.topic_id IN (SELECT topic_id FROM ads_discipline_topic WHERE subfield_id IN …)` 计数；patent 维持 unsupported；notes 注明「口径已切换为产业关联子学科过滤」。
- 无值时：走现有 `ads_geo_yearly_metrics` 逻辑不变。

**P2 `views/monitor_indicator.py` · `overview_kpi`**（现 L506-652）
- 入参增 `subfield_ids`。
- 有值时：paper → `ads_paper_profile WHERE primary_topic_id IN (SELECT topic_id FROM ads_discipline_topic WHERE subfield_id IN …)`；talent/project/institution → `ads_geo_yearly_discipline_metrics` COUNTRY 级 SUM（`location_id` 经 `ads_location` 过滤 `location_level='COUNTRY'`），保留跨国重复计数 caveat；patent、项目经费 → value=null + note「无学科维度，不参与产业过滤」。
- 无值时：现有四段逻辑不变。

**P3 `views/monitor_indicator.py` · `yearly_trend`**（现 L358-431）
- 有 `subfield_ids` 时改查 `ads_geo_yearly_discipline_metrics JOIN ads_location` 按 level 过滤，`GROUP BY statistics_year`；无值时不变。

**P4 验证**：重启 `:8082` uvicorn 后 curl 三端点：`subfield_ids` 用 CL-SEI-01+INB1303 反查的 7 个 sub_*，断言 2024 年深圳论文数 < 无过滤值且 > 0；不传参回归一致。

### 9.2 element · `gkxlumen-element`（产业码过滤）

**P5 `EnterpriseController.appendScope`**（现 L83-105）增 `List<String> industryIds`：非空时追加
`AND {alias}org_id IN (SELECT org_id FROM {dwd}.enterprise_industry_chain WHERE chain_code IN (…) OR chain_code LIKE CONCAT(code,'%') …)`（每码一个精确或前缀条件，OR 连接；片段以空格结尾的既有约定不变）。
**P6** overview/regions/districts/points/trend/influence/cluster 各端点增 `@RequestParam(required=false) List<String> industryId` 透传到 appendScope。
**P7** display `feign/RemoteElementClient.java` 对应方法签名同步加 `industryId`。

### 9.3 display · `SituationController`（Scope 翻译层）

**P8** `Scope` record（现 L211）增 `industryIds: List<String>`（取 `selectedFieldValues` 中 `INB*` 项）+ `clusterId: String`（`CL-*` 首项）；`scopeOf`（L225-294）解析；仅选集群时 `industryIds` = 该集群 mapped 的 L0 产业列表（调 `innovClient.industryClusters()` 取）；`pending_vendor` 集群 → 空列表 → element 返空、久新不加过滤 + notes 如实标注。
**P9** 新增 `resolveSubfieldIds(scope)`：仅产业选中时调 `innovClient.subfieldByIndustry(clusterId, industryId 空=整集群)`；单次请求内缓存复用；失败记日志降级为空 + notes「子学科映射不可用，产业筛选未作用于久新要素」。
**P10** `map()`/`overview()` 三处久新请求体（`kpiBodyOf` L2564、`yearlyTrendBodyOf` L2569、geoFactorMetrics body L402-412）加 `subfield_ids`；element 全部调用点（L350/446/519/559/1242/1371/1452/1957）传 `industryId`；`scopeLabelOf` 补产业生效文案；专利/经费 null+note 透传到 notes。

### 9.4 前端 · `lumen-ui-science-pc`

**P11** `SituationFilterBar.vue`：隐藏 L398-415「学科领域（细化）」`a-select` 整块（v-if 移除，内部逻辑保留）。
**P12** `index.vue`：watch 保留（选产业自动调 `/subfields`，subfieldIds 随 map/overview 请求体下发），`subfieldValues` 不再渲染；L1230-1233 路径A `a-alert` 改为生效说明：「产业领域已生效：企业按产业链匹配；论文/人才/项目/机构/课题/成果按关联子学科过滤；专利与项目经费无学科维度不参与」。

### 9.5 验收（v3）

- python 三端点 curl 实测过滤生效且不传参回归一致；
- `mvn -o -pl gkxlumen-element,gkxlumen-display -am install -DskipTests` 通过；重启后 curl `:7099 /v1/situation/map` 与 `/overview`（body `selectedFieldValues:["CL-SEI-01","INB1303"]`）对比不选产业：企业数显著变小、论文/人才变小且非 0、专利为 null+note；
- 前端 `npx vue-tsc --build` + `npm run build` 双绿；浏览器 `:3000` 实测选产业后数字变化、学科下拉不可见；
- 全部改动停本地，不 commit/push，等 `human:李伟` 走查。

