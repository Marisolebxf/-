## SYNTH-L2-COLLAB

- 角色：algorithm-agent
- 日期：2026-11-05
- 轮次：第三轮（只读 v1.0.6 现行正文；§10 修订表不作为现行要求）
- 范围：边与指数
- 核对方式：MCP `metric-get`（`M_SYNTH_COLLAB_INDEX` / `M_SYNTH_COLLAB_RELATION_INPUT` / `M_SYNTH_191_1`）+ 对照 `metrics/calc-logic/SYNTH/` 同名 md，以及 `M_SYNTH_COLLAB_DENSITY`、`M_SYNTH_COLLAB_COMPLETENESS`、`M_SYNTH_COLLAB_CENTRALITY` 的公式与时间口径。未读 seed YAML。
- 结论：退回
- 按稿能否实现：否。两类边可以实查：联合专利只读 `dwd_patent_applicants`，人才流动只读 `dwd_scholar_work_experience`，合作项目 0 边。`year` 列、闭区间、`dwd_scholar_paper_relation`、191 论文合著网入边、Nebula 导出，这几处已经从现行正文拿掉。指数式仍是 `Index=(1/3)*[minmax(Completeness)+minmax(Centrality_avg)+minmax(Density)]`。集群仍是 0 行、`clusters=[]`+`reason=cluster_rule_unclosed`。做不到的是窗口。`M_SYNTH_COLLAB_RELATION_INPUT` 写明三类事件全历史累计、申请人表无年份、`start_time` 只排序不按年截断、合作项目不能成事件、时间趋势不可得。§2/§3.2 仍把必填 `window=1y/3y/5y` 写进边的唯一键，并把全历史事件写入该 `window_label` 后返回。这不是该窗的边集。头部又写 `M_SYNTH_191_1` 只作密度上游。191 的边是 2021–2024 论文共同署名，密度式却是同一张协同边上的 `rho=2m/[n(n-1)]`（m 为联合专利+合作项目+人才流动）。两套边不能合成同一个 Index。
- 是否违反 D18：否。边与指数都在 ADS，灌数方 entan-py，接口只读表。禁止 `gapfill_synth_collab_*`，无真源不灌整图演示行。空图与 null 不是接口写死的 mock。
- 是否与需规叶冲突：否。序号 139 仍是合作网络只读查询，无真源可空图，产业筛选仍在。序号 140 的三类关系与指数式仍在；集群/孤立写明本期不覆盖，不用完整度 `n/N` 顶替。序号 141 的相关性不足则 `insufficient`，报告与策略仍在，没有改成不做。
- 是否把维护技术图谱（34–40）做成了落库：否。`synth_collab_node` / `synth_collab_edge` 是序号 139 的合作网络查询结果。没有技术节点增删改、修改历史或版本保存。
- 是否编了规划正文：是。已注册口径没有年份窗口。把全历史事件放进 `window_label=1y/3y/5y` 再当该窗的图返回，就是自编年份。把 191 论文合著网写成密度上游，就是自编边源。
- 退回必改：`window=1y/3y/5y` 不得装入全历史边。按年过滤做不到时，该窗 `nodes=[]`、`edges=[]`，并带 reason，标明关系输入是全历史累计、不能按年截断。`window_label` 只许留在请求和批次 meta 里，不得据此返回全历史边。指数、完整度、中心度、密度同样没有已注册年份窗口：不得把无窗口截面复制进三个窗。该窗图为空，则这四项 null+reason，不得用全历史截面顶上。指数式保持 `Index=(1/3)*[minmax(Completeness)+minmax(Centrality_avg)+minmax(Density)]`，禁止密度×强度。删掉「`M_SYNTH_191_1` 只作密度上游」。密度只在协同边集上算 `rho=2m/[n(n-1)]`，m 只计联合专利与人才流动（合作项目加 0）。不得把 191 的密度返回值写入 `synth_collab_network_stat`，也不得代入 Index。`dwd_scholar_paper_relation` 与 191 论文合著网不得写入 `synth_collab_edge`。`dwd_patent` 全量共同申请人不得另写抽取。不做 Nebula 导出。集群保持 0 行与 `cluster_rule_unclosed`。
