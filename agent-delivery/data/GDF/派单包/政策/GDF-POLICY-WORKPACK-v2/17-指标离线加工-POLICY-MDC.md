# 17 — Wave D：POLICY-MDC 指标离线加工

> **读者**：GDF。本章说明哪些指标要配成 T+1 之后的 Python 作业，哪些只列表、不配作业。  
> **脚本**：第一批放在本包 `scripts/mdc/`，即本文件所在目录下的 `GDF-POLICY-WORKPACK-v2/scripts/mdc/`，与 `scripts/policy_c1_industry.py` 同在 `scripts/`。**本版还没有这个目录**。落表名已在下面写死。`GDF-POLICY-MDC-STAT-L01` 写入该目录后，GDF 再复制到自己的 Python 节点。目录未出现之前，不要在 GDF 上建 MDC 作业。  
> **不复制** `metrics/repro/M_*.py`。那些文件读冻结快照或供应方库，写出 JSON，不是本节点的作业。  
> **口径真源**：`agent-delivery/metrics/calc-logic/POLICY/`。本章不新发明公式。  
> **讨论收口**：`工程过程/04-系统集成/06-GDF数据治理集成/对接文档/我方/2026-10-26-要素指标加工与图谱拆解思路.md`。

Wave A / B 只洗主表。Wave C（`12`）只做产业抽取和条款结构化。本章是它们之后的指标结果写入，叫 Wave D。

## 0. 三条作业，不要并成一个

| 名字 | 本章 | GDF 怎么配 |
|---|---|---|
| POLICY-MDC | 本章 | 只调度下面「第一批」。口径未闭合的不建作业 |
| POLICY-Graph | `18` | 已有 C1 照旧。实体识别、关系抽取的脚本还没有，先不配 |
| POLICY-MRC | `19` | 不配 T+1，包内不放脚本 |

刷新：

- STAT：按当前行数全量重算，替换该 `metric_id` 的旧结果。
- 全文模型：只重算变更过的 `policy_id`，并带回看窗口。当前全文模型都在口径未闭合名单里，本版不生成、不调度。

## 1. 用数范围（第一批共用）

读 `gkxlumenx_dwd.policy_base_info`。这是用数条件，不是 Wave A/B 的取数条件。

- `source_plane = 'domestic'`。国际行留在主表里，不进这批分母。QPOL-05 仍待甲方，临时默认只计国内，结果里要带上这个限定。
- `is_deleted = 0` 且 `IFNULL(is_history, 0) = 0`。`is_history` 为 NULL 视为当前。
- 行数用 `COUNT(*)`。禁止用 `information_schema.TABLE_ROWS` 当分母。

各级（或各省）行的 `policy_count` 之和必须等于同一批的政策总数。对不上就非 0 退出，不把半成品留在 ADS。

## 2. 第一批可调度（脚本未配）

目标库 `gkxlumenx_ads`（环境变量 `POLICY_ADS_DB`）。列结构对照本包 `14-ADS-MySQL-DDL/ads-creates.md`。该文件里的 `CREATE` 仍写 `demo_gkxlumenx_ads`，产线执行时换成 `gkxlumenx_ads`，不要按 demo 库名建表。本版不新建结果表，不建表。

同一张 `policy_level_dist` 上有两个 `metric_id`。替换时只删本指标的行，不要把另一指标清掉。`calc_batch_id` 用 `gdf_` 前缀，不要用 `mock_`。

| 指标 | 落表 | 写什么 | 留空 |
|---|---|---|---|
| `M_POLICY_TOTAL_COUNT` | `policy_level_dist` | 一行。`level` 为空。`metric_id` 为本指标。`policy_count` = 第 1 节的行数 | `valid_count`、`validity_rate`（有效率未闭合，见第 3 节） |
| `M_POLICY_LEVEL_DIST` | `policy_level_dist` | 按 `rank` 分五行，编码见下表。`metric_id` 为本指标。`ratio` = 该行 `policy_count` / 本批总数 × 100 | 同上 |
| `M_POLICY_NATIONAL_DIST` | `policy_national_dist` | 按 `province` 分组。空串和字面 `'NULL'` 合成一行，`province_name` = `未归省` | `province_code`、`yoy`、`center_lng`、`center_lat` |
| `M_POLICY_SZ_DIST` | `policy_sz_dist` | 只写一行全市合计：`district_name` = `深圳市`，条件 `city` 为 `深圳` 或 `深圳市`。`metric_id` 为本指标 | `district_code`、`yoy`、经纬度。**不写各区行** |
| `M_POLICY_TIMESERIES` | `policy_timeseries` | 只写年：`period_type` = `Y`，`period_key` = `publish_year`，`publish_count` 为该年行数 | `growth_rate`、`continuity_rate`（连续性见 QPOL-07） |

`rank` 写入 `policy_level_dist.level` 时用口径文档的编码，不要用该列注释里的「1 国家 / 2 省 / 3 市 / 4 区县」：

| level | 含义 | rank 里出现 |
|---|---|---|
| 4 | 国家级 | 国家级 |
| 3 | 省级 | 省级（含「市级+省级」，取更高层级） |
| 2 | 市级 | 市级，且没有省级、国家级 |
| 1 | 区县级 | 区级或园区级，且没有更高层级 |
| 0 | 未标注 | rank 为空 |

五行之和 = `M_POLICY_TOTAL_COUNT` 的 `policy_count`。

深圳各区不在第一批。`district` 几乎是字面 `'NULL'`，灌数闸门未开（`20`）。不要为了把 `policy_sz_dist` 填满而按区 `GROUP BY`。

## 3. 口径未闭合（不建作业、不建表、不灌数）

这些指标号没有脚本。看到表就停。

| 决策 | 指标 |
|---|---|
| QPOL-01 类型是主题还是文种 | `M_POLICY_TYPE_DIST`。库里的 `type` 是文种，不能当成产业 / 人才 / 企业扶持发布。不写 `policy_type_dist` |
| QPOL-02 权重、阈值、弹性 | `M_POLICY_DEEP_166_1`、`M_POLICY_FOCUS_INDEX`、`M_POLICY_DEEP_167_1`、`M_POLICY_INTENSITY_INDEX`、`M_POLICY_INTENSITY_SCORE`、`M_POLICY_DEEP_168_1`、`M_POLICY_EFFECT_SCORE`、`M_POLICY_IMPLEMENTATION_EFFECT`、`M_POLICY_DEEP_169_1`、`M_POLICY_SHORTBOARD_COUNT`、`M_POLICY_DEEP_170_1`、`M_POLICY_OPPORTUNITY_COUNT`、`M_POLICY_DEEP_171_1`、`M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DS_07_POLICY_GUARD_001`、`M_POLICY_DS_07_POLICY_GUARD_008`、`M_POLICY_SUPPORT_STRENGTH`、`M_POLICY_TEXT_PARSE`、`M_POLICY_SIMULATE` |
| QPOL-03 相似度 | `M_POLICY_RELATION_DEGREE`、`M_POLICY_INDUSTRY_FIT`、`M_POLICY_MATCH` |
| QPOL-07 连续性 | `M_POLICY_TIMESERIES` 的 `continuity_rate`。发布量行仍在第一批 |
| 主口径未指定 | `M_POLICY_VALIDITY_RATE`（不写 `valid_count` / `validity_rate`，不建废止事实表）、`M_POLICY_INDUSTRY_COVERAGE` |

`M_POLICY_BASE_100_1` 不单开作业。它捆了级别、文种、时序、全国、深圳。可算的子项已在第一批。

扶持事实表 `mt_policy_` 是以后的空表任务（`GDF-POLICY-MT-SUPPORT-L01`），服务 `M_POLICY_SUPPORT_STRENGTH`。该指标仍在 QPOL-02。本版不建表、不加工、不灌数。

## 4. 脚本进包之后怎么跑

生成任务完成前，本节只是约定，节点上还没有文件。

- 目录是本包内 `scripts/mdc/`：本文件所在的 `GDF-POLICY-WORKPACK-v2/scripts/mdc/`，与 `scripts/policy_c1_industry.py` 同在 `scripts/`。一条指标一个 `.py`。`metrics/repro/` 只写在文件头注释里作对照，节点不执行那些文件。脚本先写入本包该目录，再由 GDF 复制到 Python 节点；节点上的存放路径本章不规定。文件头注释写 `metric_id`、口径文档路径、对应 repro 路径、源表、目标表、全量刷新。
- 连接与 C1 相同：`POLICY_MYSQL_*`，`POLICY_DWD_DB` 默认 `gkxlumenx_dwd`，`POLICY_ADS_DB` 默认 `gkxlumenx_ads`。禁止 `demo_gkxlumenx_*`。不配 HTTP。脚本不建表。
- `--self-check` 不连库。退出码 0 才算成功。
- 挂在当日国内、国际两张平面 Wave B 都 `success` 之后，并且在 C1/C2 之外单独跑。失败不回滚 B，也不把 C 标失败。
- 详见 `15`。
