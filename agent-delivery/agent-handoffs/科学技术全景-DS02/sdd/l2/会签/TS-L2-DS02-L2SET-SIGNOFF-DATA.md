# TS-L2-DS02-L2SET-SIGNOFF-DATA · 科学技术全景 · 二级四单 · 数据会签

- 角色：`agent:data-agent`
- 日期：2026-11-07
- 对象：`TS-L2-DS02-{GRAPH,ENTITY,PATH}-{ARCH,API,METRIC,DATA}`（12 份 as-built），重点 `*-DATA`、`*-METRIC`
- 监管：`human:淮政玮`
- 指标查询：2026-11-07 经 MCP `user-metric-registry` `metric-get`。未读 `metrics/registry` 下 YAML，未写 seed
- 代码只读抽查：`lumen-algo-py` `tech_graph.py`（写入 `_TAGS` / `_EDGES`）、`tech_graph_read.py`、`scripts/seed/seed_technology_panorama_score.py`；`lumen-topic-py` `gkx_svc_service/jx_dict.py`
- 本页不改库、不灌数、不改代码，不 commit，不写 task-registry

## 总结论

| 二级 | 第一轮 | 已改 | 第二轮 |
|---|---|---|---|
| GRAPH（17–21） | 不同意 | 是 | 有条件同意 |
| ENTITY（22–27） | 不同意 | 是 | 同意 |
| PATH（28–33） | 同意 | — | — |

## 1. GRAPH（序号 17–21）

### 第一轮：不同意

| 文件 · 段落 | 问题 | 要改成 |
|---|---|---|
| `GRAPH-DATA` 第 5 节末段 | 只写「MySQL 只读」，没写读哪个库。抽查 `jx_dict.py`：`JX_ADS_DATABASE` 默认 `gkx_technology_analysis_dev`，`JX_ADS_HOST` 默认 `47.93.119.170`。不是 `demo_gkxlumenx_ads`，也不是供应方库 `gkx` | 写明库名、主机；注明该库 `technology_node_id` 与图上编号是否同批未核 |
| `GRAPH-DATA` 第 7 节 | 列了搜索 `CONTAINS` 依赖索引，漏了领域收窄 `technology_node_id IN [...]` 同样是属性 `WHERE` | 补上，并引写入侧注释「WHERE 在 `demo_gkx_chain` 上会 IndexNotFound」作佐证；写「未建单」 |
| `GRAPH-ARCH` 第 6 节「领域筛选」 | 同第 5 节，未写读库 | 补库名（随架构会签同改） |

### 已改

上表三处已改。

### 第二轮：有条件同意

| 项 | 稿 | 抽查 | 判定 |
|---|---|---|---|
| 点属性 | DATA 第 2 节列 8 个属性，读 5 个 | `_TAGS["tech_point"]` 同为 8 个，名称、类型逐一对上；`community_id`、`graph_release_id`、`data_version` 不读 | 一致 |
| `tech_rel` 属性 | DATA 第 3 节：`first_evidence_year` 写入侧无 | `_EDGES["tech_rel"]` 只有 `relation_type`、`evidence_level`、`relation_confidence_score`、`direction_status` | 如实。`relations[].year` 与 `timeline.years / events` 会一直空 |
| 需规 21「描述 / 发展状态 / 层级」 | DATA 第 2 节：`tech_point` 无此属性，抽屉行空 | 同 | 如实，不造数 |
| 写入归属 | DATA 第 4 节：点 L01 进行中、边 L02 backlog | 本页只读 | 一致。本页不写图、不调 `/ops/v1/tech-graphs/**` |
| 不读 ODS / DWD / 供应方库 / `gapfill_` | DATA 第 8 节 | 图谱主链一致 | 一致。子学科走外部 `_dev` 库，见条件 D1 |

条件：

- **D1**：子学科收窄依赖外部库 `gkx_technology_analysis_dev`（`_dev` 后缀，主机 `47.93.119.170`）。正式链路依赖一个开发库，须由数据侧登记该库归属、正式库名与切换时点，并核一次 `ads_technology_paper.technology_node_id` 与 `demo_gkx_chain` 上 `tech_point.technology_node_id` 是否同一批编号（不同批则领域筛选恒空，表现为 `GRAPH_EMPTY`）。本页不建单，交 coordinator。
- **D2**：详情抽屉「关系强度」卡显示的是点上 `weighted_degree`（`index.vue` 第 527 行），是界面上的统计数字但没有 `metric_id`，也没有红问号。D9 要求每个统计数字有 ⓘ，或 D1 `missing` 时显红问号。`GRAPH-METRIC` 写「图上属性，不是指标」不足以豁免。须交 `DS-02-METRIC-OPEN-L01` 判定身份（挂已在册 ID，或登记为 D1 missing 显红问号）。本页不新造 ID。

## 2. ENTITY（序号 22–27）

### 第一轮：不同意

| 文件 · 段落 | 问题 | 要改成 |
|---|---|---|
| `ENTITY-DATA` 第 3 节倒数第 1 段 | 写「边的属性名、是否带强度与年份，由 L02 落边时定」。抽查 `tech_graph.py` `_EDGES`：写边规格已在代码里，`tech_has_paper / patent / institution` 属性为空元组，`tech_has_person` 只有 `source_paper`、`source_topic`。L02 照现规格落边，强度、年份仍是空 | 写明现规格；要加须先改写边规格（归 L02），读图补取未建单 |
| `ENTITY-DATA` 第 6 节 | 漏登记：`subject_id` 无类型前缀，论文 / 专利 / 机构编号同串会落同一行（灌数按 (`subject_id`, `score_kind`) 合并） | 补第 4 条；注明 mock 值只由 (`kind`, `subject_id`) 决定，撞号时值相同不串，接真算前须加类型维 |
| `ENTITY-METRIC` 第 3 节 | 漏登记：`M_TECH_ENTITY_INFLUENCE` 的 `extras.ui_mount` 指向「技术评估 · 技术关系网络 + 创新主体评估」，不是本页。PATH 分册对同类问题已登记，本分册没有 | 补一句，回填归 data-agent |

### 已改

上表三处已改。

### 第二轮：同意

| 项 | 稿 | 抽查 / 注册表 | 判定 |
|---|---|---|---|
| 四类实体 Tag、VID、属性 | DATA 第 2 节 | `_TAGS` 中 `tech_paper / patent / institution` 各有 `technology_node_id`；`tech_person` 有 `source_paper`、`source_topic` | 一致 |
| 分数表 DDL | DATA 第 4 节：主键 (`subject_id`, `score_kind`)，CHECK 闭集三种，`DOUBLE NOT NULL` | 与模块级数据会签核的库 `demo_gkxlumenx_ads` 一致 | 一致。D18 表，不是 D16 `gapfill_` 表 |
| 行数 | 252,363 = 108,337 + 126,484 + 17,542；合计 271,793 = 252,363 + 19,430 | 算术自洽。2026-11-07 未复查库 | 如实标注了截止日期 |
| 四条 metric 读数 | METRIC 第 2、3 节 | `M_TECH_ENTITY_INFLUENCE` D3 full、`M_TECH_PAPER_PATENT_CNT` `acceptance_unit_id=TOPIC-TECH-05`、D2 均 provisional，与 `metric-get` 相同 | 一致 |
| D4 | 全 mock，不改 live | 同 | 一致 |

## 3. PATH（序号 28–33）

结论：同意。

| 项 | 稿 | 抽查 / 注册表 | 判定 |
|---|---|---|---|
| `tech_path_step` 规格 | DATA 第 2.1 节：起点 `previous_technology_node_id`、终点 `technology_node_id`、属性 `path_id` string / `step_order` int | `_EDGES["tech_path_step"]` 相同 | 一致 |
| `path_id` 为空时退为 `{起点}->{终点}`，读图与灌数同规则 | 第 2.1 节 | 两处规则对上 | 一致。第 6 节已登记「L02 须保证 `path_id` 非空」 |
| 分数值域 | 第 3 节：中心度 40.000–48.999、优先级 70.000–78.999 | 灌数 `mock_value` = 基数 + (sha256 前 2 字节 % 9000) / 1000 | 一致 |
| `path_priority` 0 行 | 第 4 节 | 图上无 `tech_path_step` | 如实。L02 后重跑 `--apply` |
| 三条注册读数 | METRIC 第 2 节：D2 partial provisional、D3 partial、D4 mock、阶段清单 `ods_synced / dwd_loaded / verified` todo、`es_indexed / graph_loaded` n/a | `metric-get` 相同 | 一致 |
| `ui_mount` 指向专题、`srs_refs` 空 | METRIC 第 7 节已登记 | 同 | 如实。是否把 SRS 序号 29、31 回填 `srs_refs`、补挂展示页 `ui_mount`，由 data-agent 按 `metrics/README.md` 另做，不在本会签内改 seed |

## 签收边界

本页不把任务标 done，签收由 `human:淮政玮` 做。同意会签不是签收。D4 不得改 live。条件 D1、D2 交 coordinator 建单或转 `DS-02-METRIC-OPEN-L01`，本页不写 task-registry、不写 seed。
