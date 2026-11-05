## SYNTH-L2-COLLAB

- 角色：data-agent
- 日期：2026-11-05
- 范围：协同册 v1.0.6 现行 DATA 表（§10 修订表不作为现行要求）
- 依据：`architecture-baseline.md` D18；总册 §11.2 / §11.3；`M_SYNTH_COLLAB_RELATION_INPUT`、`M_SYNTH_COLLAB_DENSITY`、`M_SYNTH_COLLAB_CENTRALITY` 现行口径
- 结论：退回
- 按稿能否实现：否。指标 4 张 `synth_collab_index` / `network_stat` / `relation_input` / `output_corr` 有粒度、唯一键、写入和读批。`synth_collab_cluster` 建表、本期 0 行。`synth_collab_batch_meta` 有粒度、唯一键、列、写入和按 `snapshotId` / `is_latest=1` 的读法。库 `demo_gkxlumenx_ads` / `gkxlumenx_ads`，灌数方 entan-py。快照读 `GET /topic/v1/synth/collaboration/batch-snapshot`，图谱读 `GET /topic/v1/synth/collaboration/graph`。表数与 README、总册 §11.3 一致：指标 4，另有空表 cluster、batch_meta、node、edge。不使用 `gapfill_synth_collab_*`。`synth_collab_node` / `synth_collab_edge` 落不了行。边唯一键已含 `source_event_id`、不含 `year`，但写入只写「按全历史事件」。关系输入件的联合专利事件是一条 `pn`（申请人数 ≥2 算 1 个事件），密度/中心度的边是同一 `pn` 上的申请人对，并要求双方同城、无向、去自环、并行边合并。人才流动在关系输入件里是去重后的一次迁移，在密度件里还要收成无向简单边。稿没有选定表内存哪一套，`source_event_id` 没有取值，`weight` 没有填充规则，节点 `degree` 没有写按简单图还是按事件行计数。`entity_id` / `src_id` / `dst_id` 未写用机构名称还是主数据编码。`entity_type=talent` 与 `industry_code` 没有写入来源。因此这两张表的粒度、唯一键和写入不闭合。
- 是否违反 D18：否。指标与图都在 ADS，灌数方 entan-py，接口只读表。合作项目 0 行、无城内边时空图 `reason=graph_empty`，是查询结果。禁止 `gapfill_`，禁止整图演示行。集群是 `clusters=[]`+`reason=cluster_rule_unclosed`。策略无表，失败回空数组。稿没有要求接口返回写死的 mock。
- 是否与需规叶冲突：否。序号 139 仍是企业－机构－人才合作网络的只读查询，产业筛选仍在。序号 140 的三类关系在 `synth_collab_relation_input`（同批 3 行），合作项目边为 0 与该件事件数 0 一致，指数式未改，集群在 C-02 定稿前为空态，不用完整度 `n/N` 冒充归属。序号 141 的相关性在 `synth_collab_output_corr`，`n<3` 为合法 `insufficient` 行，报告由前端按真快照出 PDF，策略为装包 LLM。
- 是否把维护技术图谱（34–40）做成了落库：否。`synth_collab_node` / `synth_collab_edge` 是序号 139 的合作网络查询结果，只读。没有技术节点或关系的增删、属性编辑、修改历史或版本保存。`batch_meta` 只保存分析快照与 `graph_batch_id` 的对应。
- 是否编了规划正文：否。现行正文没有把未注册的按年切边写成现行图算法。`window_label` 只记请求窗。策略无表。报告正文表、服务端 PDF 归档、文件存储都写明本期不做。`depth` 与 `gapfill_batch_id` 本期没有。
- 退回必改：只改 `synth_collab_node` / `synth_collab_edge` 的落行规则，其他表不动。
  1. 联合专利按同一 `pn` 的申请人对展开。`source_event_id=pn`，非空。同一专利的多对申请人共用该 `pn`，靠两端点区分。人才流动按学者任职序列去重后的一次迁移展开。`source_event_id` 用 `scholar_id` 与该序列中的迁移序号拼成非空键。不用 `start_time` 过滤年份。端点按稳定顺序只存一行。合作项目保持 0 行。
  2. 图事实只写双方同城、无向、去自环的边。跨城不入边表。没有双方同城的边则 `nodes=[]`、`edges=[]`、`reason=graph_empty`，不得用「任一主体可归城」顶替城内边，也不得灌演示行。`relation_input` 的可归城计数仍按该件，不要求等于边行数。
  3. 表内保留未合并的事件边。`network_stat` 的边数 m 与节点 `degree` 按密度/中心度件的简单图计算：并行边合并后再计度。不得把事件行数当成度。
  4. `weight` 恒为 1。该件没有边强度（专利无金额、任职无权重）。此列不表示合作强度，密度不按 `weight` 加权。
  5. `entity_id` / `src_id` / `dst_id` 写明用机构名称还是主数据编码。两张源表抽不出学者节点时，`entity_type=talent` 写 0 行，禁止用机构冒充人才节点。`industry_code` 只读专题库一级分类（C-05 临时默认）；没有映射则该列为空，筛选结果为空，不得编产业标签。
  6. 每次成功发布新生成 `graph_batch_id`。节点和边只插入该批，不更新旧批。旧 `snapshotId` 仍读到自己的 `graph_batch_id`。
