# algorithm-agent 会签意见
- 角色：algorithm-agent
- 日期：2026-11-05
- 轮次：第二轮（只读 v1.0.5 现行正文；各册 §10 修订表不作为现行要求）
- 范围：三册 METRIC 为主，五问覆盖全册
- 核对方式：MCP `metric-get`（`M_SYNTH_VIT_INDEX` / `M_SYNTH_VIT_WEIGHT` / `M_SYNTH_186_1` / `M_SYNTH_ELEM_WEIGHT` / `M_SYNTH_ELEM_FOUR_DIM_SCORE` / `M_SYNTH_COLLAB_INDEX` / `M_SYNTH_COLLAB_RELATION_INPUT` / `M_SYNTH_191_1`）+ 对照 `agent-delivery/metrics/calc-logic/SYNTH/` 同名 md（另读 `M_SYNTH_ELEM_INDEX`、`M_SYNTH_COLLAB_COMPLETENESS`、`M_SYNTH_COLLAB_OUTPUT_CORR`、`M_SYNTH_COLLAB_DENSITY`、`M_SYNTH_COLLAB_CENTRALITY` 的公式与时间口径）。未读 seed YAML。`M_SYNTH_ELEM_FOUR_DIM_SCORE` 返回 Metric not found。

## SYNTH-L2-VIT-AI-TABLES
- 结论：同意
- 按稿能否实现：是。五张结果在 `demo_gkxlumenx_ads` / `gkxlumenx_ads`，装包只读表。三档与已注册口径一致：`WEIGHT_MAIN` 0.30/0.35/0.20/0.15（`M_SYNTH_VIT_WEIGHT`，`main_is_official=false`），`INDEX_MAIN` 0.30/0.30/0.20/0.20（`M_SYNTH_VIT_INDEX`，用 `weight_provenance_metric_id` 标成指数件口径），`EQUAL` 0.25×4（`M_SYNTH_186_1` 四维等权）。同 profile 配对读。产业维缺行不补 0。权重无行则 null+reason，装包不得回填三档向量。
- 是否违反 D18：否。做得到的指数与维分实算后写入 ADS 再读；做不到的预填行 `is_mock=1` 也在 ADS，接口不写死 JSON。三张 `gapfill_synth_*` 只作既有输入，不是结果表。
- 是否与需规叶冲突：否。本册不覆盖序号 137、139–141，也没有把这四叶写成已交付。
- 是否把维护技术图谱（34–40）做成了落库：否。只有活力结果表与装包，无技术节点增删改、历史或版本保存。
- 是否编了规划正文：否。三档数值都能在对应 calc-logic 里对上，并标明不是官方标定。

## SYNTH-L2-ELEM
- 结论：同意
- 按稿能否实现：是。当前 8 张在 ADS，装包只读。类型/层次/领域/综合沿 `M_SYNTH_187_1`–`M_SYNTH_190_1` 与 `M_SYNTH_ELEM_INDEX`。权重本期只有 `EQUAL`，与 `M_SYNTH_ELEM_WEIGHT` 的占位主口径（类型/层次/领域各 1/3，`main_is_official=false`）一致；无行不得填 1/3。全景无表，装包查 DWD。`M_SYNTH_ELEM_FOUR_DIM_SCORE` 仍未注册，接口固定 `evaluationDimensions=[]`+`reason=metric_not_registered`。
- 是否违反 D18：否。8 张是 ADS 灌行再读。全景 DWD 有实数，按真实聚合查询，不建结果表、不走 gapfill。四维公式未定稿则不出数；空态不算违反。
- 是否与需规叶冲突：否。序号 137 的规模/质量/结构/活跃度写明本期不覆盖、不建表、不灌数、不出数，不写成设计落位齐，也不写成照册可满足需规。类型/层次/领域单列，不顶替这四维。总册 §2.2 同句为 blocked。
- 是否把维护技术图谱（34–40）做成了落库：否。要素全景是 DWD 聚合读，无技术节点增删改、历史或版本保存。
- 是否编了规划正文：否。四维不写表结构、不写公式；候选方向写明只供 `human:唐绍祖` 参考，定稿并注册后才建 `synth_elem_four_dim_score`。1/3 是已注册占位，不是新公式。

## SYNTH-L2-COLLAB
- 结论：退回
- 按稿能否实现：否。指数、网络统计、相关性、集群空态、批次表可以按稿做：指数式与 `M_SYNTH_COLLAB_INDEX` 一致；`n<3` 的 Pearson 行作 `insufficient` 与 `M_SYNTH_COLLAB_OUTPUT_CORR` 一致；集群 0 行且 `clusters=[]`+`reason=cluster_rule_unclosed`。边表做不到。§2 要求按 `M_SYNTH_COLLAB_RELATION_INPUT` 实查写入边，§3.2 又把 `window` 定义成边年份闭区间，边唯一键含 `year`。该件 calc-logic 写明三类事件全历史累计、申请人表无年份、`start_time` 只用于排序且不按年截断、时间趋势不可得。不能既按该件实查，又给每条边一个年份再按 1 年/3 年/5 年截断。同段把 `dwd_scholar_paper_relation` 写成边源，但三类事件公式不用这张表。§5 还要求图谱导出记 Nebula space，与「边从 DWD 实查进 ADS」不是同一条链路。
- 是否违反 D18：否。指标与图都在 ADS，禁止 `gapfill_synth_collab_*`。联合专利与人才流动可以实查；合作项目按该件不能构成跨机构事件，写 0 边。无真源不灌整图演示行。验收允许 `nodes=[]`+`reason=graph_empty`，不得用演示行凑非空。空态不算违反。
- 是否与需规叶冲突：否。序号 139 仍是合作网络只读查询，无真源可空图。序号 140 的集群/孤立写明本期不覆盖、不出归属行，不用完整度 `n/N` 顶替。序号 141 的相关性不足则 `insufficient`，报告与策略仍在，没有改成不做，也没有用 `M_SYNTH_191_1` 顶协同指数。
- 是否把维护技术图谱（34–40）做成了落库：否。`synth_collab_node` / `synth_collab_edge` 是序号 139 的合作网络查询结果。没有技术节点增删改、修改历史或版本保存。
- 是否编了规划正文：是。已注册口径是全历史累计、年份不可得。稿把 `year` 放进边的当前身份，并按窗口做年份闭区间，等于把未注册的按年切边当成现行图算法。`start_time` 按年切开也是改口径。
- 退回必改：边不要按年切。删掉边唯一键中的 `year`，删掉 `window`「边年份闭区间」。`window_label` 只作请求条件，不得把全历史事件标成最近 1/3/5 年。在 `M_SYNTH_COLLAB_RELATION_INPUT` 改口径并完成注册之前，不编年份，不用 `start_time` 切年；按年过滤做不到则该窗 `nodes=[]`、`edges=[]` 加 reason。边只按事件公式展开：联合专利用 `dwd_patent_applicants`，人才流动用 `dwd_scholar_work_experience`，合作项目保持 0 边。`dwd_scholar_paper_relation` 不得作为边源。`dwd_patent` 全量共同申请人在该件中不可用，不得另写抽取。`M_SYNTH_191_1` 的论文合著网不得写入 `synth_collab_edge`。删 §5「图谱导出任务记 Nebula space」。指数继续用 `Index=(1/3)*[minmax(Completeness)+minmax(Centrality_avg)+minmax(Density)]`，禁止密度×强度，禁止用 191 的密度冒充 `collabIndex`。集群保持 0 行与 `cluster_rule_unclosed`。
