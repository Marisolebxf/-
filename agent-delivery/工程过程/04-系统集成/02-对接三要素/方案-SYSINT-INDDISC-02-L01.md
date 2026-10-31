# 方案 · SYSINT-INDDISC-02-L01

展示系统「产业领域」与久新「学科领域」的口径对照。本文件只记录真源和挂载判断。没有可确认的领域对领域映射。未改业务仓，未改指标 seed，未写 ADS，未改 `subfield_topic_map`。

## 1. 已锁定

久新侧「学科领域」= 子学科 `subfield_id`，沿用 WBS-02-08。不是 `technology_node_id`（WBS-02-12），不是正式技术目录 `tech_id`。

## 2. 两侧字典真源

### 2.1 展示系统筛选用的产业字典

页面上的筛选控件文案是「产业分类」，选项是深圳 10+5 产业集群，不是久新学科。

| 项 | 值 |
|---|---|
| 编码种子 | `agent-delivery/data/data-design/storage/CHAIN/seeds/industry-cluster-sz-10+5-2026.yaml` |
| 种子字段 | `policy_version=sz-10+5-2026`，`q068=pending_client`。集群：`cluster_id`、`group`（`sei` / `fut`）、`name`、`sort_order`、`map_status`（`mapped` / `pending_vendor`）。L0：`industry_id`、`name` |
| 集群枚举 | `CL-SEI-01`～`CL-SEI-10`，`CL-FUT-01`～`CL-FUT-05`。有 L0 的才标 `mapped`，空 L0 为 `pending_vendor` |
| L0 枚举 | 种子里已写出的 `industry_id`：`INB1303` 集成电路、`INB1323` 传感器、`INB1309` 人工智能、`INB1333` 智能终端、`INB1306` 软件与信息服务、`INB2503` 生物医药、`INB1209` 智能网联汽车、`INB1236` 低空经济、`INB1502` 数字创意、`INB1204` 机器人、`INB1354` 具身智能、`INB2505` 合成生物。同一 `industry_id` 可出现在多个集群 |
| 现网表 | `{INNOV_DIM_SCHEMA}.industry_cluster`：`cluster_id`、`cluster_group`、`cluster_name`、`display_hint`、`sort_order`、`is_active`。`{INNOV_DIM_SCHEMA}.industry_cluster_map`：`cluster_id`、`industry_id`、`industry_name`、`sort_order`、`is_active`。lumen 专题创新服务缺省库名 `demo_gkxlumenx_dim` |
| 谁维护 | 编码以种子 yaml 为准。展示前端 `lumen-ui-science-pc` 的 `src/lib/industryCluster/seed.ts` 是这份种子的冻结副本。专题侧列表接口读上面两张 DIM 表，不读久新 |
| 展示入口 | `IndustrySelect`，占位「选择产业集群 / 产业 / 产业链」。使用页包括科技发展规划总览、创新评价设定、以及 `industryCluster` 种子覆盖的态势筛选 |

指标和部分 demo 排名表把列名写成「产业领域」。那是文案，不是另一本已经核对过的字典。本叶不把那些列名并进上表。

### 2.2 久新「学科领域」

调研记录 2026-10-22，库为久新 ADS，行数以当时表清单为准。

| 表 | 行数 | 主键 | 本叶是否采用 |
|---|---:|---|---|
| `ads_discipline_domain` | 4 | `domain_id` | 否。上一级 |
| `ads_discipline_field` | 26 | `field_id` | 否。上一级学科 |
| `ads_discipline_subfield` | 252 | `subfield_id` | 是。本叶口径 |
| `ads_discipline_topic` | 4516 | `topic_id` | 否。下一级 |

`ads_discipline_subfield` 字段：`subfield_id`、`openalex_subfield_id`（只作来源映射）、`field_id`、`domain_id`、`name_zh`、`name_en`、`data_version`、`update_time`。枚举是这 252 行，不是我方闭集代码表。维护方是久新。政策三页「技术领域」多选的选项值已经用 `subfield_id`，名称用中文，没有中文不抄英文。

机构挂学科的结果表是 `ads_institution_discipline_profile`（调研时 7,232,894 行）。键是 `institution_id` + `topic_id`，并带 `subfield_id`、`field_id` 及中英文名。表内没有 `industry_id`。

### 2.3 容易混进来的产业表

这些表名字里有产业，但不是展示侧 10+5 字典，也不是学科。

| 表 | 调研行数 | 键 | 和本叶的关系 |
|---|---:|---|---|
| `ads_industry` | 1971 | `taxonomy_id` + `industry_id` | 久新产业分类节点。层级 `industry_level` 1 门类 / 2 大类 / 3 中类 / 4 小类，名称 `section` / `division` / `major_group` / `group`。字典接口已有，政策页产业下拉不改。不是 `INB*` |
| `ads_institution_industry` | 1,354,245 | `institution_id` + `taxonomy_id` + `industry_id` | 机构在久新产业分类上的覆盖。字段含 `industry_code`、`industry_name_zh`、`industry_level`。没有 `subfield_id` |
| `subfield_topic_map` | WBS-02-08 已有结果 | `subfield_id` + 产业链 `node_id` | 子学科对产业节点。行上带本侧 `industry_id`、`cluster_id`。本叶不改这张表 |
| `dwd_tech_node_industry_map` | WBS-02-12 | `technology_node_id` + `node_id` | 技术节点，不是学科 |

`M_ORG_INDUSTRY_COVER`（科研机构产业领域覆盖）：指标支持表写明候选表 `ads_institution_industry`，库内支持「结果表在」，D1 `draft`，D4 `mock`，口径是否等于指标库：还没有。不标已对齐。

## 3. 领域对领域的映射

没有同名 ID，没有已经对齐的字典，本叶不编造名称对照，也不把 LLM 结果抄成领域映射。

| 左侧 | 右侧 | 结论 | 原因 |
|---|---|---|---|
| 展示 `industry_cluster.cluster_id`（`CL-*`） | `ads_discipline_subfield.subfield_id` | 不可映射 | 两套编码。集群表没有 `subfield_id`，子学科表没有 `cluster_id` |
| 展示 `industry_cluster_map.industry_id`（`INB*`） | `subfield_id` | 不可映射 | `INB*` 是深圳集群 L0。子学科主键不是这套码 |
| `ads_industry.industry_id` | `subfield_id` | 不可映射 | 久新产业分类节点，层级是门类到小类，不是 OpenAlex 子学科 |
| `ads_institution_industry` | `ads_discipline_subfield` | 不可映射 | 机构产业表没有 `subfield_id`。机构学科表没有 `industry_id`。两张结果表不能互相当筛选条件 |
| `M_ORG_INDUSTRY_COVER` | 展示 `CL-*` / `INB*` | 不可映射 | 指标候选表是久新产业分类，不是展示集群种子。口径未对齐 |
| `technology_node_id` / `tech_id` | 本叶任一侧 | 排除 | 分别属于 WBS-02-12 和正式技术目录，不是学科领域 |

WBS-02-08 的 `subfield_topic_map` 在关联产业节点时，会从 `industry_cluster` / `industry_cluster_map`（`cluster_id LIKE 'CL-%'`）带出 `industry_id` 和 `cluster_id`。那是子学科对产业链节点，粒度不是领域对领域。任务备注里已有 2026-10-29 的同步和关联结果（390 行，130 个已映射子学科）。本叶未逐条复核，不把这 130 条写成已对齐的领域映射。

## 4. 影响面

| 表面 | 现在的状态 |
|---|---|
| 展示「产业分类」级联（科技发展规划总览、创新评价设定，以及同一 `IndustrySelect`） | 选项来自 10+5 种子或 DIM 集群表，控件本身不是空的。选项键不是 `subfield_id`，按产业筛选对不上久新学科。口径不一致，未接入 |
| 政策三页「技术领域」多选 | 已经用 `subfield_id`。这是学科侧，不是产业领域。本叶不改 |
| `M_ORG_INDUSTRY_COVER` | 候选表有行，口径还没有，D4 为 mock。不能当成展示产业领域已经覆盖 |
| 全景「主流技术路线」 | 读技术节点映射，不属于本叶 |

## 5. 补齐路径

本叶不另开实现叶。

1. 若目标是「子学科能落到展示侧产业集群 / 产业」：归 WBS-02-08。`subfield_topic_map` 已有 `industry_id`、`cluster_id`，目录就是第 2.1 节的集群表。已有行是 LLM 对产业节点的结果，不是领域字典。要当领域映射用，须另做核对；核对之前不标已对齐。本叶不改这张表。
2. 若目标是「`M_ORG_INDUSTRY_COVER` 或 `ads_institution_industry` 按展示 `INB*` / `CL-*` 筛选，或按 `subfield_id` 筛选」：WBS-02-08 不写机构产业表，WBS-02-12 写的是技术节点。两条已有叶都接不住。本叶不新建映射表，不改展示口径。
3. 展示侧把「产业分类」改成子学科或改成 `ads_industry`，属于改口径。本叶不做。
