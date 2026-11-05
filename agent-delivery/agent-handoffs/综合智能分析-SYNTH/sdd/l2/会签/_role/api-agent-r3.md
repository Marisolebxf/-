# api-agent 会签意见（第三轮）

- 角色：api-agent
- 轮次：第三轮
- 日期：2026-11-05
- 稿本：协同册 v1.0.6 现行正文（§2 DATA、§3 API）。修订表旧口径不作为现行要求
- 依据：基线 D18；需规叶 139–141；维护技术图谱序号 34–40
- 范围：只复审 SYNTH-L2-COLLAB。不改设计正文，不新建任务

## SYNTH-L2-COLLAB

- 结论：同意
- 按稿能否实现：是。`synth_collab_edge` 唯一键与列都没有 `year`，响应边对象也没有 `year`。必填 `window` 只写入 `window_label`，读图不按边的年份过滤，关系输入按全历史累计。返回边为 `source,target,type,weight,source_event_id`，验收以 `source-target-type-source_event_id` 区分多条边。无 meta 时图谱固定 HTTP 200、`nodes=[]`、`reason=batch_meta_missing`；正常空图用 `reason=graph_empty`。快照、任务与 `GET /topic/v1/synth/collaboration/graph` 的表、批次和截断足够 Java 透传、Python 读 ADS。
- 是否违反 D18：否。指数、网络统计、关系输入、相关系数、空集群、`synth_collab_batch_meta`、`synth_collab_node` / `synth_collab_edge` 都在 `demo_gkxlumenx_ads` / `gkxlumenx_ads`。灌数方 entan-py。快照与图谱只读这些表。有真源的边实查写入，合作项目 0 行，无归城事件保持空图。策略由装包 LLM 生成，失败为 `strategies=[]`+reason。
- 是否与需规叶冲突：否。139 仍是企业–机构–人才合作网络的只读查询、产业筛选和密度/中心性。140 的联合专利、合作项目、人才流动仍落在 `synth_collab_relation_input`，指数式未改；合作项目 0 行是源上构不出跨机构事件，集群保持 `clusters=[]`+`reason=cluster_rule_unclosed`。141 仍是相关性、前端真实快照 PDF 和策略建议。
- 是否把维护技术图谱（34–40）做成了写接口或落库：否。对外图谱只有 `GET /topic/v1/synth/collaboration/graph`。`synth_collab_node` / `edge` 是序号 139 的主体合作读模型，主体类型是 enterprise/institution/talent。没有技术节点增删、技术关系增删、属性编辑、修改历史或版本保存接口。`batch_meta` 只保存分析快照与 `graph_batch_id` 的对应。
- 是否编了规划正文：否。§3 是本期快照、图谱和前端报告契约。不写年份、不做 Nebula 导出、本期没有 `depth` 与 `gapfill_batch_id`、不建报告正文表，都是现行约束。
- 退回必改：无
