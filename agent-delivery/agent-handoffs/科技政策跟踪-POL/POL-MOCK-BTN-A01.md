# POL-MOCK-BTN-A01 · 政策缺项表总表与空表补建

> 2026-11-09。只盘点并补建空表。不灌数，不改算法生成，不清已有缺项行。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 开工时已是 `in_progress`。本单不改任务状态，不调用 `task-update-status` / `task-claim`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只补还没有的表，已有表不重建、不清空。未用 YAGNI 跳过 D16：缺项只进 `gkxlumenx_gapfill.gapfill_*`，不写 ODS / 正式 DWD / ADS / 供应方库。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `stores/README.md` 算法库 ER（无独立 diagram_id）。`POLICY-STORAGE-FLOW` 未改 |
| 图 diff | ER 增加八个缺项实体，并用 `policy_id` / `policy_id_a` 连到 `policy_base_info` |
| 会签态 | `stores/README.md` frontmatter 仍是 `draft`。未把已 approved 的流图改绿 |
| 说明 | 细表继续 draft。本单不是存储流图会签 |

## 问题清单

- 总控把 210/211 写成现网缺表。盘点时两表已在，且有行。本单不重建。
- 说明书第 11.2 节把评价 222–226 写成 `gapfill_policy_eval_focus`、`gapfill_policy_eval_summary`、`gapfill_policy_eval_shell`。现网没有前两张。以现网和已签收解读分册为准，见总表备注。
- `gapfill_policy_qry_*`、`gapfill_policy_trend_*`、`gapfill_policy_theme_dist` 现网没有 `is_mock` 列。本单不改已有表。
- 237 的文本解析在现网 `gapfill_policy_sim_result.row_kind` 里没有对应种类。总控没有单列新表名，本单不另建。

## 修改内容

库：`gkxlumenx_gapfill`（演示连接上的缺项库）。写前 `assert_demo_mysql_targets`，当时 ODS/DWD/ADS 为 `demo_gkxlumenx_ods` / `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads`。

新建且行数为 0：

| 表 | 需规 | 业务键 |
|----|------|--------|
| `gapfill_policy_semantic` | 606 | `policy_id` + `facet_name` |
| `gapfill_policy_xcmp` | 610 | `policy_id_a` + `policy_id_b` + `relation_name` |
| `gapfill_policy_xcmp_viz` | 611 | `chart_kind` + `policy_id_a` + `policy_id_b` + `item_name` |
| `gapfill_policy_xcmp_summary` | 613 | `policy_id_a` + `policy_id_b` + `summary_kind` |
| `gapfill_policy_report_analysis` | 614 | `policy_id` + `aspect_name` |
| `gapfill_policy_report_insight` | 615 | `policy_id` + `insight_kind` |
| `gapfill_policy_report_body` | 616（618 只读） | `policy_id` + `section_name` |
| `gapfill_policy_report_trace` | 617 | `policy_id` + `direction_name` + `conclusion_key` |

已存在、未重建、行数未变：

| 表 | 本单执行后行数 |
|----|----------------|
| `gapfill_policy_audience_feedback` | 591 |
| `gapfill_policy_assessment_report` | 2 |
| 其余已有 `gapfill_policy_*`（含 DS12 的预测/结果/意见） | 与执行前 `COUNT(*)` 相同 |

DDL 文档：`agent-delivery/data/data-design/storage/POLICY/stores/mysql/gapfill.md`。可执行脚本：`demo-algo-ent-analysis/scripts/ensure_gapfill_policy_btn_tables.py`。

## 可读标准（总控 §5.2）

B 段回执和写入的文字按下面执行。本单没有灌样例行。

1. 中文自然句，读起来是一句完整的话。
2. 不出现占位符：`TODO`、`TBD`、`xxx`、`{字段}`、「待补充」、「测试数据」、`N/A`。
3. 不出现字面量 `null`，不用空字段名或只有标点的格子当内容。回执摘抄的那一句必须是非空中文。
4. 不用英文枚举码。关系写「共性 / 差异 / 互补 / 冲突」，渠道写「问卷 / 在线评价 / 意见征集」，图种写「对比表 / 柱 / 雷达」。
5. 行上有 `policy_id`（或 `policy_id_a` / `policy_id_b`）时，键必须已经在演示库 `demo_gkxlumenx_dwd.policy_base_info`。没有政策键的行，必须在地区列或主题列写明中文地区或主题，例如「深圳市」「科创发展」。
6. 回执里的一条样例不超过 60 个字（按字符计）。表里的正文可以更长，回执只摘一句。
7. 八张新表写入时 `is_mock=1`，`metric_id` 留空，不新造指标。D4 仍是 mock。
8. 检索三表和动向四表现网没有 `is_mock` 列。不要为了加这一列去重建或清空。中文句标准仍然适用。

## 缺项表总表

接口前缀一律 `/display/v1/policy/`。页面是展示系统七页。灌数脚本在 `lumen-algo-py/scripts/`。表名与说明书第 11 节不一致处，备注列写明，以现网为准。

### 全景

| 序号 | 表 | 行粒度 | 业务键 | 读取 | 灌数脚本 | 备注 |
|------|----|--------|--------|------|----------|------|
| 197、198、200 | `gapfill_policy_qry_stat`；目录另见 `gapfill_policy_qry_doc` | 一个统计维度一行；目录一政策一行 | 统计：`metric_id` + 该行启用的级别/省/区/年/文种。目录：`policy_id` 唯一 | 全景 `GET panorama/stats`、`GET panorama/search` | `seed_gapfill_policy_qry.py` | 总控序号格只写了 199，表名单含 `qry_*`。现网无 `is_mock` |
| 199 | `gapfill_policy_qry_rank`；目录同 `gapfill_policy_qry_doc` | 一政策一个排序维一行 | `rank_dim` + `rank_no`；`rank_dim` + `policy_id` | 全景 `GET panorama/rank` | 同上 | 只有名次，无分数 |
| 205 | `gapfill_policy_trend_hotspot`、`gapfill_policy_trend_impact`、`gapfill_policy_trend_report` | 热点：领域+名称；影响：领域+对象；报告：一篇一行 | 现网仅主键 | 全景 `POST panorama/jobs` | `seed_gapfill_policy_trend.py` | 趋势图本身读已有时序，不在这三表。现网无 `is_mock` |
| 206 | `gapfill_policy_theme_dist` | 一个主题一行 | `theme_name`（现网仅主键） | 全景 `GET panorama/stats` | 同上 | 总控序号格未单列 206，表名单有 `theme_dist` |
| 209 | `demo_gkxlumenx_ads.policy_effect` | 已有 ADS 行 | 沿用现表 | 全景实施效果，已有 `run()` | 无缺项灌数脚本 | 不新建缺项表。本单不写 ADS |
| 210 | `gapfill_policy_audience_feedback` | 一条反馈一行 | 现网仅主键；`policy_id` 可空 | 全景 `GET panorama/feedback` | `seed_gapfill_policy_audience.py`；算法库合成另写本表 | 已存在 591 行。未重建 |
| 211 | `gapfill_policy_assessment_report` | 一份评估正文一行 | 无 `policy_id`；范围在 `scope_text` | 全景 `GET panorama/assessment-report` | `seed_gapfill_policy_assessment.py` | 已存在 2 行。未重建 |
| 212 | `demo_gkxlumenx_ads.policy_match` | 已有 ADS 行 | 沿用现表 | 全景匹配，已有 `run()` | 无缺项灌数脚本 | 不新建缺项表。本单不写 ADS |
| 213 | `gapfill_policy_version_diff` | 一政策一对发布日的一种增改删 | `policy_id` + 两个发布日 + `change_type`（索引非唯一） | 全景 `GET panorama/version-diff` | `seed_gapfill_policy_cmp.py`；合成入口另写 | 说明书与现网同名 |
| 214 | `gapfill_policy_detail_compare` | 一政策一行 | `policy_id` 唯一 | 全景 `GET panorama/{id}/detail` | 同上；合成入口另写 | 条件与材料。力度分不在本表 |
| 215 | `gapfill_policy_impl_dept` | 区域+部门+方面一行 | `region_name` + `impl_dept` + `aspect` 唯一 | 全景 `GET panorama/stats` | `seed_gapfill_policy_cmp.py` | 说明书把四表写在 213–218 一行，现网表名即此 |
| 216 | 不建表。读 `demo_gkxlumenx_ads.policy_intensity` | 已有力度行 | 沿用现表 | 全景 `GET panorama/stats` | 已有 `run()`，不进缺项灌数 | 说明书写明不建 `gapfill_policy_benchmark_viz` |
| 217 | `gapfill_policy_benchmark_report` | 对标对象+对照字段一行 | `benchmark_object` + `compare_field` 唯一 | 全景 `GET panorama/benchmark-report` | `seed_gapfill_policy_cmp.py` | 正文在行里 |
| 218 | 不建表。读 `demo_gkxlumenx_ads.policy_intensity` | 已有力度行 | 沿用现表 | 全景 `POST panorama/jobs` | 已有 `run()` | 与 216 同一张力度表 |

201、202、204 是用户数据，不建缺项表、不灌假记录。203、207、208 读已有目录或子图，不在本按钮建表。

### 评价

| 序号 | 表 | 行粒度 | 业务键 | 读取 | 灌数脚本 | 备注 |
|------|----|--------|--------|------|----------|------|
| 219 | `gapfill_policy_eval_trend` | 切换维+位置+指标名一行 | `switch_dim` + `dim_value` + `metric_name` 唯一 | 评价 `POST evaluation/jobs` | `seed_gapfill_policy_eval_viz.py` | 无 `policy_id`。位置列承载地区或类别 |
| 220 | `gapfill_policy_eval_partition` | 对象种类+名称一行 | `object_kind` + `object_name` + `resource_direction` 唯一 | 同上 | 同上 | 对象名是地区、行业或群体 |
| 221 | 不建表 | — | — | 已有子图 | 无 | 说明书写明只消费已有子图 |
| 222 | `gapfill_policy_eval_template` | 模板+周期+维度+图种一行 | 四列唯一 | 评价 `GET evaluation/shells` | `seed_gapfill_policy_eval_template.py` | 说明书 11.2 未单列此表名。现网就是这张 |
| 223 短板 | `demo_gkxlumenx_ads.policy_effect`（`scope_type=region_gap`） | 已有 ADS | 沿用现表 | 评价 `GET evaluation/counts` | 已有 `gap.run`，不新建缺项表 | 不建 `gapfill_policy_eval_focus` |
| 223 焦点 | `demo_gkxlumenx_ads.policy_focus`（`policy_id` 非空） | 一政策一行 | `policy_id` | 评价 `POST evaluation/jobs` | 已有 `focus.run` | 焦点说明在 `ext`，不另建缺项表 |
| 224、225 | `gapfill_policy_eval_shell` | 一条解读或一条多媒体说明 | `entry_kind` + `gap_item` | 评价 `GET evaluation/shells` | `seed_gapfill_policy_eval_shell.py` | 无 `policy_id`。专题名/标题即主题键 |
| 226 | `demo_gkxlumenx_ads.policy_text_parse` | 已有解析行 | `policy_id` | 评价 `POST evaluation/jobs` | 已有解析 `run()` | 不建 `gapfill_policy_eval_summary` |
| 227–230 | `gapfill_policy_eval_scheme` | `row_kind` + 方案一行 | `row_kind` + `scheme_name`（参数行再加 `param_band`） | 评价 `POST evaluation/jobs`；意见也可在 `shells` | `seed_gapfill_policy_eval_scheme.py` | 路径行 `metric_id` 只用已有 `M_POLICY_DS_11_POLICY_EVAL_015` |
| 231 | 不建表、不灌文件 | — | — | 导出未做则空 | 无 | 方案脚本明确不灌导出文件 |

### 推演

| 序号 | 表 | 行粒度 | 业务键 | 读取 | 灌数脚本 | 备注 |
|------|----|--------|--------|------|----------|------|
| 232 | `gapfill_policy_sim_forecast` | 未出台仿真一行 | 政策类型+覆盖+力度+实施时间+目标产业 唯一 | 推演 `POST simulation/jobs` | `seed_gapfill_policy_sim_forecast.py`；合成入口另 upsert 一行 | `metric_id=M_POLICY_SIMULATE`。`policy_id` 可空 |
| 233 | 同表 | 新出台预测一行 | `policy_id` 唯一 | 同上 | 同上 | 必须是演示库里的真实 `policy_id` |
| 234 | 同表 | 区域空间一行 | `region_name` + `policy_type` 唯一 | 同上 | 同上 | 地区键在 `region_name` |
| 235、238、239、241、242 | `gapfill_policy_sim_result` | 按 `row_kind` | 多维评估：`dimension_name` 唯一；路径：`policy_id`+`stage_name`；解读：`policy_id`+`section_name` | 同上 | `seed_gapfill_policy_sim_result.py` | 种类是中文：多维评估、重点、影响范围、路径环节、解读段落 |
| 236 | `gapfill_policy_sim_stakeholder` | 一条参与意见 | 现网仅主键 | 同上 | 同上 | 无 `policy_id`。角色是「决策者 / 评估者 / 利益攸关方」 |
| 237 | 不另建表 | — | — | 同上 | 无独立脚本 | 现网结果表没有「文本解析」种类。本单不新建 |
| 240 | 不建表 | — | — | 已有子图 | 无 | 关联分析不灌缺项行 |

### 治理

| 序号 | 表 | 行粒度 | 业务键 | 读取 | 灌数脚本 | 备注 |
|------|----|--------|--------|------|----------|------|
| 602、603 | 不建表 | — | — | 治理 `GET governance/results` | 无 | 只读第 6 项已有结果。按钮不灌 |
| 604 | `gapfill_policy_lineage_index` | 原文条款或条款结论一行 | `policy_id` + `clause_no`（另有结论键） | 治理 `GET governance/lineage-index` | `seed_gapfill_policy_lineage_index.py` | 不与 617 的研报溯源合并 |
| 605 | `gapfill_policy_indicator_lib` | 一政策一个维度一条指标 | `policy_id` + `dimension_name` | 治理 `GET governance/indicator-library` | `seed_gapfill_policy_indicator_lib.py` | 维度是扶持力度、适用范围、实施时效、申请条件。`metric_id` 留空 |

### 拆解

| 序号 | 表 | 行粒度 | 业务键 | 读取 | 灌数脚本 | 备注 |
|------|----|--------|--------|------|----------|------|
| 606 | `gapfill_policy_semantic` | 一政策一面一行 | `policy_id` + `facet_name`（主旨、适用场景、约束、条款分类） | 拆解 `POST parse/jobs` | 无。本单只建空表 | 新表 |
| 607、608 | 不建表 | — | — | 拆解 `GET parse/clauses` | 无 | 读已落库条款 |
| 609 | 不建表 | — | — | 已有子图 | 无 | 不设资源 |

### 对比

| 序号 | 表 | 行粒度 | 业务键 | 读取 | 灌数脚本 | 备注 |
|------|----|--------|--------|------|----------|------|
| 610 | `gapfill_policy_xcmp` | 一对政策一种关系一行 | `policy_id_a` + `policy_id_b` + `relation_name` | 对比 `POST compare/jobs` | 无。本单只建空表 | 关系只用中文四词。件数复用全景统计，不进本表 |
| 611 | `gapfill_policy_xcmp_viz` | 图种+政策对+对照项一行 | `chart_kind` + 两个政策键 + `item_name` | 同上 | 无 | 图种：对比表、柱、雷达 |
| 612 | 不建表 | — | — | 用户配置，无记录则空 | 无 | 不灌假配置 |
| 613 | `gapfill_policy_xcmp_summary` | 一对政策一种输出一行 | 两个政策键 + `summary_kind` | 同上 | 无 | 对比摘要、核心结论。不灌导出文件 |

对比页统计仍走 `GET compare/stats`，复用全景已有分布，不读这三张新表。

### 研报

| 序号 | 表 | 行粒度 | 业务键 | 读取 | 灌数脚本 | 备注 |
|------|----|--------|--------|------|----------|------|
| 614 | `gapfill_policy_report_analysis` | 一政策一面一行 | `policy_id` + `aspect_name` | 研报 `POST report/jobs` | 无。本单只建空表 | 实施效果、经济社会、产业影响、趋势 |
| 615 | `gapfill_policy_report_insight` | 一政策一种洞察一行 | `policy_id` + `insight_kind` | 同上 | 无 | 观点、建议、风险、机遇 |
| 616 | `gapfill_policy_report_body` | 一政策一模块一行 | `policy_id` + `section_name` | 同上 | 无 | 正文在行里 |
| 617 | `gapfill_policy_report_trace` | 一政策、一方向、一条结论 | `policy_id` + `direction_name` + `conclusion_key` | 同上 | 无 | 方向：结论到原文、原文到结论 |
| 618 | 不建文件表。只读 `gapfill_policy_report_body` | 同 616 | 同 616 | 同上 | 无 | 不灌 PDF / Word。无正文则导出空 |

## 核对结果

2026-11-09 本机直连演示库（未走 SSH）。

- `--check`：通过。语句只有 `CREATE TABLE IF NOT EXISTS`，库名只有 `gkxlumenx_gapfill`，每张表都有 `is_mock`、`gapfill_batch_id`、`fill_method`，没有 `DROP` / `DELETE` / `INSERT`。
- `--apply`：`applied 10`，`describe_ok 8`。八张新表 `COUNT(*)=0`。反馈表仍 591 行，评估报告仍 2 行。其余已有 `gapfill_policy_*` 的行数与执行前相同。
- 八张新表的列名顺序与 `stores/mysql/gapfill.md` 的 CREATE 一致。唯一键：`uk_policy_facet`、`uk_pair_relation`、`uk_chart_pair_item`、`uk_pair_kind`、`uk_policy_aspect`、`uk_policy_kind`、`uk_policy_section`、`uk_policy_direction_key`。
- 210/211 的列与 `lumen-algo-py/scripts/mysql/gapfill_policy_audience.sql`、`gapfill_policy_assessment.sql` 的 CREATE 一致。

## 测试结果

- `python scripts/ensure_gapfill_policy_btn_tables.py --check` 退出码 0。
- `python scripts/ensure_gapfill_policy_btn_tables.py --apply` 退出码 0。
- 未跑仓内其它测试，未改生成逻辑。

## 遗留风险

- 八张新表是空的。展示读口在 C 段接上之前，对应区块仍是空态。灌数是 B02–B07，本单不做。
- 评价 focus/summary 的说明书表名与现网不一致。B 段不要按说明书去建那两张表。
- 检索表和动向表没有 `is_mock`。B 段若要强行加列，会碰到已有行，不在本单范围。
- 237 没有缺项行种类。B03 若把 237 算进行数大于 0，需要先有产品确认读哪一列，不能在本单结构上臆造。

## CI/CD（必填）

- 分支：`dev` → `origin/dev`
- demo-algo-ent-analysis commit：`597906c4b0459b8f33f6420f1f35388e887815da`
- gkx-orchestration commit：与本 handoff 同一次提交（推送后以 `git log -1` 为准）
- pipeline：本单提交后由远端 CI 触发，此处未抄运行结果
- 部署：缺项表已在演示库建好，不依赖本次镜像发布才存在
- K8s rollout：无新镜像要求
- 未把连接口令写入本文件

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python，本单不改算法 | 符合。只建表 |
| 调用链不越层 | 符合。未改 Java / 前端 / 内部接口 |
| 图谱不写 Neo4j、不写 nGQL | 符合。未碰图 |
| D16 缺项只进 `gapfill_` | 符合。库 `gkxlumenx_gapfill`，写前拒绝非 `demo_` 的 ODS/DWD/ADS |
| 不写 ODS、正式 DWD、ADS、供应方库 | 符合。209/212/216/218/223/226 只登记已有表，没有写入 |
| 不新造 `metric_id`，D4 仍 mock | 符合。新表该列可空 |
| D18 接口不返回写死 mock | 符合。本单不改接口。空表供后续只读 |
| D12 不把 demo 并进 lumen | 符合。脚本在 `demo-algo-ent-analysis`，未改 `lumen-algo-py` |
| 可观测 / D8 / D10 | 本单无新接口、无页面 |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 400000（估算，含本会话上下文，非控制台精确值） |
| model_used | `grok-4.7` |
| actual_cost | 1.20（按 data 任务量级估算，美元） |
| cost_warn | `green` |

## 涉及文件

- `repos/demo-algo-ent-analysis/scripts/ensure_gapfill_policy_btn_tables.py`（新建）
- `agent-delivery/data/data-design/storage/POLICY/stores/mysql/gapfill.md`
- `agent-delivery/data/data-design/storage/POLICY/stores/README.md`
- `agent-delivery/data/data-design/storage/POLICY/CHANGELOG.md`
- 本 handoff
