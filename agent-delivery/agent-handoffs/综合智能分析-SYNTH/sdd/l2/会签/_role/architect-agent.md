# architect-agent 会签意见（第二轮）

- 角色：architect-agent
- 日期：2026-11-05
- 范围：三册当前正文；各册文末「修订」表不作为现行要求
- 依据：`architecture-baseline.md` D18 原文（2026-11-03）。总册 §11 v1.0.5 与三册正文对齐 ADS 落点。真查做得到时实查写入 ADS 再读；空图与集群空态是合法空态。

## SYNTH-L2-VIT-AI-TABLES

- 结论：同意
- 按稿能否实现：是。五张 `synth_vit_*` 建在 `demo_gkxlumenx_ads` / `gkxlumenx_ads`，由 `seed_synth_vit_*.py` 整批写入，`GET /topic/v1/synth/vitality/batch-snapshot` 与 internal 同路径只读这些表；`snapshotId` 含 `calc_batch_id`，旧批可按该 ID 回读。
- 是否违反 D18：否。预填行 `is_mock=1` 在新建 ADS 表，不是 `gkxlumenx_ai`，也不是 `gapfill_` 结果表；权重缺行只回 `null`+`reason`，装包不返回三档向量；三张 `gapfill_synth_*` 只作输入。
- 是否与需规叶冲突：否。序号 133–135 的指标体系、加权指数、排名都有表和快照落点；总册对区级映射仍标待定，本册没有把南山区默改成深圳。
- 是否把维护技术图谱（34–40）做成了落库：否。本册没有技术节点或关系的增删、属性编辑、修改历史或版本保存。
- 是否编了规划正文：否。三档权重是写入 `synth_vit_weight` 的现口径，不是另写的路线图功能。

## SYNTH-L2-ELEM

- 结论：同意
- 按稿能否实现：是。当前 8 张建在 ADS，entan-py 灌行，`GET /topic/v1/synth/elements/batch-snapshot` 只读这 8 张；全景无表、装包查 DWD；四维不建表，接口固定 `evaluationDimensions=[]`+`reason=metric_not_registered`。
- 是否违反 D18：否。8 张是新建 ADS，不是 `gkxlumenx_ai`；权重缺行不填 1/3。全景是 DWD 真查，不是接口写死 mock。四维空数组是指标未注册的诚实空态。
- 是否与需规叶冲突：否。序号 136 由装包查询 DWD 交付；序号 137② 写明本期不覆盖，类型/层次/领域不顶替四维；序号 138 落在 `synth_elem_contrib`。
- 是否把维护技术图谱（34–40）做成了落库：否。本册没有技术图谱增删改、修改历史或版本保存。
- 是否编了规划正文：否。四维只保留「注册并定稿后才建 ADS 表」，没有表结构，并写明不当实现依据。

## SYNTH-L2-COLLAB

- 结论：退回
- 按稿能否实现：否。`synth_collab_edge` 唯一键含 `year`，§3.2 把必填 `window` 定义成边年份闭区间，但同册要求按 `M_SYNTH_COLLAB_RELATION_INPUT` 实查，该件现行口径是全历史累计：`dwd_patent_applicants` 无年份，任职 `start_time` 只用于排序、不按年截断，合作项目写 0 行，实查填不满 `year`，已写入的联合专利边也会被年份闭区间滤掉。
- 是否违反 D18：否。四张指标在 ADS，图事实在 `synth_collab_node` / `synth_collab_edge` 且禁止 `gapfill_` 与整图演示行，`synth_collab_batch_meta` 按 `snapshotId` 落表，集群是 `clusters=[]`+`reason=cluster_rule_unclosed`，策略是无表 LLM、失败回空数组。
- 是否与需规叶冲突：否。序号 139 仍是只读关系图与产业筛选；序号 140 的指数与网络统计有表，集群空态不另造归属算法；序号 141 的相关性、前端快照报告和 LLM 策略都有落点。
- 是否把维护技术图谱（34–40）做成了落库：否。只有 `GET /topic/v1/synth/collaboration/graph` 查询，没有技术节点或关系的增删、属性编辑、修改历史或版本保存。
- 是否编了规划正文：否。当前正文没有把后续能力写成现行功能；集群空态与策略无表都能回溯到序号 140/141 和已登记的 Q-SYNTH-C-02 / C-04。
- 退回必改：改 §2 `synth_collab_edge` 与 §3.2 的 `window`。`year` 退出唯一键，列可空，禁止编造年份。`window` 只作为条件上下文写入 `window_label`，不按边年份做闭区间过滤；1 年/3 年/5 年在源没有年份时允许看到同一套全历史边。联合专利、人才流动按该件全历史事件实查写入 ADS，`is_mock=0`；唯一键用源事件号区分多条边（联合专利用 `pn`，人才流动用能区分一次迁移的源侧键），`weight` 按该件事件口径填写。`dwd_zh_project` 仍写 0 行。无归城事件时保持 `nodes=[]` 且 `reason=graph_empty`，不得改灌演示行。
