# data-agent 会签意见（第二轮）
- 角色：data-agent
- 日期：2026-11-05
- 轮次：第二轮
- 范围：三册 DATA 为主，五问覆盖全册。只评 v1.0.5 正文；修订表旧口径不作为现行要求
- 依据：`architecture-baseline.md` D18 原文；总册 §11；`表落点与gapfill说明.md`

## SYNTH-L2-VIT-AI-TABLES
- 结论：同意
- 按稿能否实现：是。五张 `synth_vit_*` 都有粒度、唯一键、写入（entan-py 实算/预填整批）和读批（`succeeded` 最新批，按 `calc_batch_created_at`）。库 `demo_gkxlumenx_ads` / `gkxlumenx_ads`，灌数方 entan-py `seed_synth_vit_*.py`，读取接口 `GET /topic/v1/synth/vitality/batch-snapshot` 与 `GET /internal/v1/synth/vitality/batch-snapshot`。表数 5，与 README、总册 §11.3 的活力 5 张一致。
- 是否违反 D18：否。五张结果在 ADS，预填 `is_mock=1`，装包只读表。权重缺行只返回 `null`+`reason`+`confidence`，不在接口里填三档向量。既有三张 `gapfill_synth_new_product_sales_ratio` / `rd_employee` / `policy_effect` 仍是已登记输入，本册不新建、不把结果放进 `gapfill_` 或 `gkxlumenx_ai`。
- 是否与需规叶冲突：否。序号 133 分项在 `synth_vit_indicator`，134 加权指数在 `synth_vit_index` / `dim_score` / `weight`（需规为加权或机器学习，加权路径即满足），135 指数、分项与排名有落表。
- 是否把维护技术图谱（34–40）做成了落库：否。本册无技术节点或关系的增删改、属性编辑、修改历史、版本保存表。
- 是否编了规划正文：否。五张都是当前必建，对应序号 133–135。`legacy_unknown` 与可选 `snapshotId` 是本期读旧批规则。
- 退回必改：无

## SYNTH-L2-ELEM
- 结论：同意
- 按稿能否实现：是。当前必建 8 张都有粒度、唯一键、写入和读批。库 `demo_gkxlumenx_ads` / `gkxlumenx_ads`，灌数方 entan-py，读取接口 `GET /topic/v1/synth/elements/batch-snapshot`，装包只读这 8 张。文首、§2、§8 与 README、总册 §11.3 都是 8 张；`synth_elem_four_dim_score` 不在本期 DDL。全景无表，不计入张数。
- 是否违反 D18：否。8 张结果在 ADS，权重缺行不在装包里填 1/3。全景是 DWD 真查，不建结果表、不进 `gapfill_`。四维本期不建不灌，接口 `[]`+`reason=metric_not_registered`，不用其他分数顶替，也不把 mock 行放进 `gapfill_`。
- 是否与需规叶冲突：否。序号 136 仍汇聚企业、机构、人才、资金（另含空间），走 DWD。137 四维标 blocked，类型/层次/领域不顶替四维。138 贡献在 `synth_elem_contrib`。
- 是否把维护技术图谱（34–40）做成了落库：否。全景是 DWD 聚合读，无技术节点或关系的增删改、修改历史、版本保存表。
- 是否编了规划正文：否。四维只写注册前不建不灌，不写表结构、不当实现依据。缓存表写明另裁定、本册不预支。本期权重只有 `EQUAL`。
- 退回必改：无

## SYNTH-L2-COLLAB
- 结论：同意
- 按稿能否实现：是。灌数 4 张 `synth_collab_index` / `network_stat` / `relation_input` / `output_corr` 有粒度、唯一键、写入和读批。`synth_collab_cluster` 建表、本期 0 行。`synth_collab_node` / `edge` / `batch_meta` 有粒度、唯一键、列、写入和读法。库 `demo_gkxlumenx_ads` / `gkxlumenx_ads`，灌数方 entan-py。快照读 `GET /topic/v1/synth/collaboration/batch-snapshot`，图谱读 `GET /topic/v1/synth/collaboration/graph`。表数与 README、总册 §11.3 一致：指标 4，另有空表 cluster、batch_meta、node、edge。不使用 `gapfill_synth_collab_*`。
- 是否违反 D18：否。指标在 ADS，预填进表后接口只读。已有真源的边按 `M_SYNTH_COLLAB_RELATION_INPUT` 实查写入 `synth_collab_node` / `edge`（`is_mock=0`），图谱只读这两张 ADS 表。合作项目在该件不能构成跨机构事件，写 0 行。无真源不灌整图演示行，空图 `reason=graph_empty`。集群不派生，`clusters=[]`+`reason=cluster_rule_unclosed`。策略走 LLM，无表。
- 是否与需规叶冲突：否。序号 139 为只读合作网络与产业筛选，密度/中心性在 `synth_collab_network_stat`。140 的三类关系与协同指数有落表；集群/孤立在 C-02 定稿前为空态，不用完整度 `n/N` 冒充归属。141 相关性在 `synth_collab_output_corr`，报告由前端按真快照出 PDF，策略为装包 LLM，未改叶义。
- 是否把维护技术图谱（34–40）做成了落库：否。node/edge 是序号 139 的主体合作事实，只读查询。无技术节点或关系的增删改、属性编辑、修改历史、版本保存。`batch_meta` 只保存分析快照与 `graph_batch_id` 的对应。
- 是否编了规划正文：否。策略无表。报告正文表、服务端 PDF 归档、文件存储都写明本期不做。`depth` 与 `gapfill_batch_id` 本期没有。
- 退回必改：无
