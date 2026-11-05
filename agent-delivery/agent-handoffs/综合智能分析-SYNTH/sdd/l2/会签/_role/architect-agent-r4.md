## SYNTH-L2-COLLAB

- 角色：architect-agent
- 日期：2026-11-05
- 范围：协同册 v1.0.7 现行正文（§1–§9；§10 修订表不作为现行要求）
- 依据：现行口径（1y/3y/5y 不回全历史边；源无年则 `nodes=[]`、`edges=[]`、`reason=no_year_on_source`；指数与完整度/中心度/密度为 null+同一 reason；不读 `M_SYNTH_191_1`；node/edge 本期 0 行；仍在 ADS；集群空态；策略 LLM 无表）；`architecture-baseline.md` D18；需规叶 139–141；维护技术图谱序号 34–40
- 结论：同意
- 按稿能否实现：是。请求窗只有 `1y/3y/5y`。关系输入源没有年，该窗不返回全历史边，`synth_collab_node` / `synth_collab_edge` 本期写 0 行。图谱 `GET /topic/v1/synth/collaboration/graph` 只读这两张 ADS 表里 `metric_id=M_SYNTH_COLLAB_RELATION_INPUT` 的行，无行则 `nodes=[]`、`edges=[]`、`reason=no_year_on_source`。无 `synth_collab_batch_meta` 时仍是 HTTP 200、`reason=batch_meta_missing`。指数式保持 `Index=(1/3)*[minmax(Completeness)+minmax(Centrality_avg)+minmax(Density)]`；该窗图为空时指数、完整度、中心度、密度为 null+`reason=no_year_on_source`，不把无窗截面抄进三个窗，不读 `M_SYNTH_191_1`，不把 191 的密度写入 `synth_collab_network_stat`。边响应不带 `year`。集群 0 行，`clusters=[]`+`reason=cluster_rule_unclosed`。相关性仍按已注册的按年配对 Pearson；组不出年样本则 `insufficient` 或效果区空态。策略走装包 LLM，无表；失败为 `strategies=[]`+reason。成功发布写入 `synth_collab_batch_meta`，按 `snapshotId` 读取。Java 只透传，不写 nGQL。
- 是否违反 D18：否。表在 ADS：`synth_collab_index`、`synth_collab_network_stat`、`synth_collab_relation_input`、`synth_collab_output_corr`、`synth_collab_cluster`、`synth_collab_node`、`synth_collab_edge`、`synth_collab_batch_meta`。灌数方为 entan-py。读取接口为 `GET /topic/v1/synth/collaboration/batch-snapshot` 与 `GET /topic/v1/synth/collaboration/graph`。本期 0 行和 null 是按「源无年、不能把全历史放进 1y/3y/5y」读表后的结果，不是接口写死的指标 JSON，不用 `gapfill_`，不灌演示行。
- 是否与需规叶 139–141 冲突：否。序号 139 仍是企业－机构－人才合作网络的只读查询，产业筛选仍在图谱接口上；空图不删该叶。序号 140 的三类关系仍在 `synth_collab_relation_input` 与 `relation_types`，全历史计数不抄进三个窗；指数式未改，图空则为 null；集群仍是 `clusters=[]`+`reason=cluster_rule_unclosed`，不用完整度 `n/N` 写归属。序号 141 的相关性、前端真快照报告、LLM 策略未改，无报告正文表。
- 是否把维护技术图谱（34–40）做成了落库：否。`synth_collab_node` / `synth_collab_edge` 是序号 139 的分析读模型，主体类型是 enterprise/institution/talent，对外只有 GET，本期 0 行。没有技术节点或关系的增删、属性编辑、修改历史或版本保存。`synth_collab_batch_meta` 只保存分析快照与 `graph_batch_id` 的对应。
- 是否编了规划正文：否。现行正文没有把未注册的按年切边写成现行图算法，没有把全历史边或全历史计数标成 1y/3y/5y，没有把 `M_SYNTH_191_1` 写成密度上游或边源。`depth`、`gapfill_batch_id`、服务端 PDF、Nebula 导出都写明本期不做。
- 退回必改：无
