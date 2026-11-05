# api-agent 会签意见（第二轮）

- 角色：api-agent
- 轮次：第二轮
- 日期：2026-11-05
- 稿本：三册 v1.0.5 现行正文；对照总册 §11、基线 D18 原文、需规叶 133–141 与维护技术图谱 34–40
- 范围：API 为主，五问覆盖全册。修订表旧口径不作为退回依据

## SYNTH-L2-VIT-AI-TABLES

- 结论：同意
- 按稿能否实现：是。五张 `synth_vit_*`、灌数脚本和 `GET /topic/v1/synth/vitality/batch-snapshot` 已写明 `weight_profile` 与可选 `snapshotId`：传入只读该批，不传按 `cache_key` 取最新成功批再读 ADS，`snapshotId` 用 `snap:{calc_batch_id}`，400/404/200+null 可以装包。
- 是否违反 D18：否。表在 `demo_gkxlumenx_ads` / `gkxlumenx_ads`，灌数方 entan-py，Java/Python 只读该表；权重缺行只回 `null`+`reason`+`confidence`，预填行 `is_mock=1`。
- 是否与需规叶冲突：否。133 分项、134 加权指数（需规为加权或机器学习，加权路径满足字面）、135 指数与排名仍由五张结果表和活力任务交付。
- 是否把维护技术图谱（34–40）做成了落库或写接口：否。只有分析结果整批写入和快照读取，没有技术节点或关系的增删、属性编辑、修改历史、版本保存接口。
- 是否编了规划正文：否。三档权重、`legacy_unknown` 和 `snapshotId` 都是本期快照规则，接口正文没有需规之外的未来计划。

## SYNTH-L2-ELEM

- 结论：同意
- 按稿能否实现：是。八张 `synth_elem_*` 读 succeeded 最新批，全景有 `page_size`、`element_types` 和 `panorama[]` DTO，404 与 200+null、`evaluationDimensions=[]`+`reason=metric_not_registered` 足够 Java 门面转发。
- 是否违反 D18：否。八张表在 ADS，灌数方 entan-py，快照只读该表；全景按 DWD 真查、无结果表；四维不出数；权重缺行不填 1/3。
- 是否与需规叶冲突：否。136 仍汇聚企业、机构、人才、资金；137 四维保持空态且写明不顶替类型/层次/领域；138 走 `synth_elem_contrib`。
- 是否把维护技术图谱（34–40）做成了落库或写接口：否。无技术节点或关系的增删、属性编辑、修改历史、版本保存接口。
- 是否编了规划正文：否。§3 只有本期快照、TopN 与四维空态，没有把未注册四维写成当前出数接口。

## SYNTH-L2-COLLAB

- 结论：同意
- 按稿能否实现：是。快照与 `GET /topic/v1/synth/collaboration/graph` 已写明 `synth_collab_batch_meta` 的表名和列；无 meta 只回 HTTP 200、`nodes=[]`、`reason=batch_meta_missing`；节点有 `name` 和 `industry_code`，边有 `weight`，本期没有 `depth`。
- 是否违反 D18：否。指标表、空集群、batch_meta、node/edge 都在 ADS，灌数方 entan-py，快照和图谱只读这些表；无真源不灌演示行、不进 `gapfill_`；策略走 LLM，失败为 `strategies=[]`+reason。
- 是否与需规叶冲突：否。139 仍是企业–机构–人才合作网络的只读筛选与密度/中心性；140 的指数与三类关系可算，集群为空态且不用完整度冒充归属；141 是相关性、前端真实快照 PDF 和建议。
- 是否把维护技术图谱（34–40）做成了落库或写接口：否。`synth_collab_node/edge` 是序号 139 的分析读模型，对外只有 GET，没有技术节点增删、关系增删、属性编辑、修改历史或版本保存接口。
- 是否编了规划正文：否。§3.3 把报告定为前端用已成功快照渲染；集群 `clusters=[]`+`reason=cluster_rule_unclosed` 是诚实空态。
