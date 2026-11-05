## SYNTH-L2-COLLAB

- 角色：api-agent
- 日期：2026-11-05
- 轮次：第四轮
- 稿本：协同册 v1.0.7 现行正文的 API（§3；空窗与读接口对照 §1、§2、§7）。§10 修订表不作为现行要求
- 范围：只复审 API。不改设计正文，不新建任务
- 结论：同意
- 按稿能否实现：是。`GET /topic/v1/synth/collaboration/graph` 对 `1y/3y/5y` 返回 `nodes=[]`、`edges=[]`、`reason=no_year_on_source`。无 meta 仍是 HTTP 200、`nodes=[]`、`reason=batch_meta_missing`，不用 404；传了 `snapshotId` 却无 meta 时不改读最新批。快照缺数据为 HTTP 200，指数、完整度、中心度、密度为 `null`+`reason=no_year_on_source`。关系输入不把全历史计数抄进这三个窗。响应里不出现 191 的密度，也不把 191 写入 `synth_collab_network_stat`。请求没有 `depth`，边对象没有 `year`。报告 PDF 由前端按已成功快照本地生成，没有服务端 PDF 接口。Java 只透传，Python 读 ADS。
- 是否违反 D18：否。指数、网络统计、关系输入、相关系数、空集群、`synth_collab_batch_meta`、`synth_collab_node` / `synth_collab_edge` 都在 `demo_gkxlumenx_ads` / `gkxlumenx_ads`。灌数方 entan-py。快照与图谱只读这些表。三窗不写 node/edge。空图和四项 null 是读空表后的结果，不是接口写死的业务数。策略无表，失败为 `strategies=[]`+reason。
- 是否与需规叶冲突：否。139 仍是企业–机构–人才合作网络的只读查询、产业筛选和密度/中心性；源无年则空图，不删该叶。140 的指数式未改，四项为 null+reason，集群仍是 `clusters=[]`+`reason=cluster_rule_unclosed`。141 仍是相关性、前端真实快照 PDF 和策略建议。
- 是否把维护技术图谱（34–40）做成了写接口或落库：否。对外图谱只有 `GET /topic/v1/synth/collaboration/graph`。`synth_collab_node` / `edge` 是序号 139 的主体合作读模型，本期 0 行，主体类型是 enterprise/institution/talent。没有技术节点增删、技术关系增删、属性编辑、修改历史或版本保存接口。`batch_meta` 只保存分析快照与 `graph_batch_id` 的对应。
- 是否编了规划正文：否。§3 是本期快照、图谱和前端报告契约。三窗空图、四项 null、不读 191、不写 `year`、没有 `depth`、没有服务端 PDF，都是现行约束。
- 退回必改：无
