## SYNTH-L2-COLLAB

- 角色：algorithm-agent
- 日期：2026-11-05
- 轮次：第四轮（只读 v1.0.7 现行正文；§10 修订表不作为现行要求）
- 范围：边与指数
- 核对方式：MCP `metric-get`（`M_SYNTH_COLLAB_INDEX` / `M_SYNTH_COLLAB_RELATION_INPUT` / `M_SYNTH_191_1`）+ 对照 `metrics/calc-logic/SYNTH/` 同名 md（INDEX / RELATION_INPUT / DENSITY / COMPLETENESS / CENTRALITY / OUTPUT_CORR）。未读 seed YAML。需规叶对照专题序号 139–141；维护技术图谱对照展示系统序号 34–40。
- 结论：同意
- 上一轮必改是否已写入现行正文：是。`1y/3y/5y` 不返回全历史边；源无年则该窗 `nodes=[]`、`edges=[]`、`reason=no_year_on_source`。`window_label` 只在请求和 `synth_collab_batch_meta`，不用来复制无窗截面。指数、完整度、中心度、密度在图空时均为 `null`+`reason=no_year_on_source`。已删「`M_SYNTH_191_1` 只作密度上游」；191 的密度不写入 `synth_collab_network_stat`，验收禁止响应出现该密度，图空时指数为 null，进不了 Index。指数式仍是 `Index=(1/3)*[minmax(Completeness)+minmax(Centrality_avg)+minmax(Density)]`，禁止密度×强度。集群本期 0 行，`clusters=[]`+`reason=cluster_rule_unclosed`。不读论文关系表，不做 Nebula 导出，`synth_collab_node` / `synth_collab_edge` 本期 0 行。
- 按稿能否实现：是。关系输入现行口径是全历史累计：申请人表无年份，`start_time` 只排序不按年截断，合作项目构不成事件，时间趋势不可得。指数、完整度、中心度、密度的已注册口径是无年份窗口的截面。稿不把这张截面写进三个窗，三窗空图和四项 null 就是读 ADS 无行。`M_SYNTH_191_1` 的边是 2021–2024 论文共同署名，稿不读、不写入 `network_stat`、不代入指数。`OUTPUT_CORR` 按已注册口径「区域固定、按年组样本、不做跨区域截面」，序列不足则 `n<3` 的 `insufficient`，不拿截面相关系数顶上。
- 是否违反 D18：否。边与指数的表在 ADS，灌数方 entan-py，快照与图谱只读这些表。按年切不到时不灌演示行；空图和 null 是无行的读结果，不是接口写死的指标数字或内存边集。禁止 `gapfill_synth_collab_*`。表名、灌数方、读取接口都写了。
- 是否与需规叶冲突：否。序号 139 仍是企业－机构－人才合作网络的只读查询，产业筛选仍在；源无年则空图，不用别的指标顶密度或中心性。序号 140 的三类关系名和指数式仍在；集群写明本期不覆盖，不用完整度 `n/N` 顶替归属。序号 141 的相关性不足则 `insufficient`，报告与策略仍在，没有改成不做。
- 是否把维护技术图谱（34–40）做成了落库：否。`synth_collab_node` / `synth_collab_edge` 是序号 139 的合作网络读模型，本期 0 行，对外只有 GET。没有技术节点增删、技术关系增删、属性编辑、修改历史或版本保存。`batch_meta` 只保存分析快照与 `graph_batch_id` 的对应。
- 是否编了规划正文：否。没有把未注册的按年切边写成现行图算法，也没有把 191 论文合著网写成密度上游。`no_year_on_source` 只标明源没有年，不新造边源，不改三维 minmax 等权。
- 退回必改：无
