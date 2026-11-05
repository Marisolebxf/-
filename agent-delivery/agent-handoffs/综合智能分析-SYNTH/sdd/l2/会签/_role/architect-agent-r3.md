## SYNTH-L2-COLLAB

- 角色：architect-agent
- 日期：2026-11-05
- 范围：协同册 v1.0.6 现行正文的边契约（§10 修订表不作为现行要求）
- 依据：`M_SYNTH_COLLAB_RELATION_INPUT` 现行口径（全历史累计；`dwd_patent_applicants` 无年份；任职 `start_time` 只排序、不按年截断；合作项目事件为 0）；`architecture-baseline.md` D18
- 结论：同意
- 按稿能否实现：是。`synth_collab_edge` 唯一键已无 `year`，表上无 `year` 列，响应边也无 `year`。`window` 只写入 `window_label`，不按边年份过滤；1 年/3 年/5 年读到的都是同一套全历史边。联合专利只读 `dwd_patent_applicants`，人才流动只读 `dwd_scholar_work_experience`，均按全历史事件实查写入 ADS。多条边用 `source_event_id` 区分，验收不重复键为 `source-target-type-source_event_id`。合作项目 0 行。没有可归城事件则空图，`reason=graph_empty`，不灌演示行。不读 `dwd_scholar_paper_relation`，不用 `M_SYNTH_191_1` 的论文合著网，不做 Nebula 导出。
- 是否违反 D18：否。边落在 ADS `synth_collab_edge`，灌数方为 entan-py 实查，读取接口为 `GET /topic/v1/synth/collaboration/graph`。合作项目 0 行与无事件空图是查询结果，不是接口写死的 mock。禁止 `gapfill_` 与整图演示行。
- 是否与需规叶 139–141 冲突：否。序号 139 仍是企业－机构－人才合作网络的只读查询，并保留产业筛选；全历史边与空图不删该叶。序号 140 的三类关系仍在 `synth_collab_relation_input`（同批 3 行），合作项目边为 0 与该件事件数 0 一致，指数式未改，集群仍是 `clusters=[]`+`reason=cluster_rule_unclosed`。序号 141 的相关性、前端真快照报告、LLM 策略未改。
- 是否把维护技术图谱（34–40）做成了落库：否。`synth_collab_node` / `synth_collab_edge` 是序号 139 的分析读模型，对外只有 GET。没有技术节点或关系的增删、属性编辑、修改历史或版本保存。
- 是否编了规划正文：否。现行边契约按已注册的全历史口径实查，没有把未注册的按年切边写成现行图算法，也没有把后续能力写成当前功能。
