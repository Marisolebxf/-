# 服务关系链 · 功能点覆盖（svc.relation）

> catalog `svc.relation` · 50897 · path `/industry-service/relation`  
> 用例 `API-服务关系链-用例.md`  
> A 线范围：**L42**（`fp-split-by-api-run/work/L42.md`）  
> 功能点键：`L42 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| svc.relation.models | GET | /entan/v1/svc/models | API-000589～API-000593 | catalog `status=unavailable`；验收 **kind=relation**；§0 **未试调** |
| svc.relation.graph | GET | /entan/v1/svc/graph | API-000594～API-000598 | catalog `status=unavailable`；合 path 按 `endpoint_id` 与 L13 区分；§0 **未试调** |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L42 \| svc.relation.models \| kind \| 算法输入-kind模型类型 | catalog kind | API-000589、API-000591、API-000592 | 已覆盖 | MOD-01 relation 主路径；MOD-02 非法；MOD-03 非本页 kind 串验防护 |
| L42 \| svc.relation.models \| relation_summary.density \| 算法输出-relation_summary.density关系密度 | catalog relation_summary.density | API-000589、API-000593 | 契约占位 | unavailable，禁止 sample density 数值作通过条件 |
| L42 \| svc.relation.models \| relation_top \| 算法输出-relation_top关键机构列表 | catalog relation_top | API-000589、API-000593 | 契约占位 | unavailable，禁止 sample centrality/机构名作通过条件 |
| L42 \| svc.relation.models \| _empty \| 关系链模型无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「kind=relation 合法必空」试调证据 |
| L42 \| svc.relation.models \| _fail \| 关系链模型查询失败 | 契约错误态 | API-000589、API-000590、API-000591、API-000592 | 已覆盖 | 含 catalog 不可用、鉴权失败与 kind 失败语义 |
| L42 \| svc.relation.graph \| limit \| 算法输入-limit节点上限 | catalog limit | API-000594、API-000596、API-000597 | 已覆盖 | GRF-01 limit=40 + 非正/负 limit 失败 |
| L42 \| svc.relation.graph \| nodes \| 算法输出-nodes网络节点 | catalog nodes | API-000594、API-000598 | 契约占位 | unavailable，禁止 sample 节点列表作通过条件 |
| L42 \| svc.relation.graph \| edges \| 算法输出-edges关系边 | catalog edges | API-000594、API-000598 | 契约占位 | unavailable，禁止 sample 边列表作通过条件 |
| L42 \| svc.relation.graph \| _empty \| 关系链图谱无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「合法 limit 必空图」试调证据 |
| L42 \| svc.relation.graph \| _fail \| 关系链图谱查询失败 | 契约错误态 | API-000594、API-000595、API-000596、API-000597 | 已覆盖 | 含 catalog 不可用、鉴权失败与 limit 失败语义 |
| L42 \| \| etl_clean_standardize \| 多源关系数据标准化预处理 | 需规（1）采集预处理 | — | 未覆盖 | req_only |
| L42 \| \| strength_layer_density_indicators \| 关系强度层次密度指标体系 | 需规三维指标阈值 | — | 未覆盖 | req_only |
| L42 \| \| stability_closeness_compute \| 网络稳定性与合作紧密度计算 | 需规定量计算 | — | 未覆盖 | req_only |
| L42 \| \| risk_coop_optimization_semantic \| 潜在风险与合作优化语义 | 需规风险与建议 | — | 未覆盖 | req_only |
| L42 \| \| structure_analysis_report \| 结构分析报告输出语义 | 需规（2）结构报告 | — | 未覆盖 | req_only |
| L42 \| \| key_org_match_scheme \| 关键机构匹配与 relation_top 协同 | 需规（2）关键机构 | — | 未覆盖 | req_only |
| L42 \| \| org_type_industry_time_scope \| 机构类型产业类别时间区间语义 | 需规（3）调用范围 | — | 未覆盖 | req_only |
| L42 \| \| report_chart_risk_trend_outputs \| 报告图表风险清单与趋势分析 | 需规（3）输出形式 | — | 未覆盖 | req_only |
| L42 \| \| auto_monitor_dynamic_refresh \| 自动化监测与动态报告刷新 | 需规（3）动态监测 | — | 未覆盖 | req_only |
| L42 \| \| api_sdk_regulatory_platform \| API SDK 与监管业务平台集成 | 需规（3）系统对接 | — | 未覆盖 | req_only |

---

## 3. 统计

| 状态 | 条数（契约 field + 哨兵） |
|------|---------------------------|
| 已覆盖 | 4（`kind`、`limit`、两处 `_fail`） |
| 契约占位 | 4（`relation_summary.density`、`relation_top`、`nodes`、`edges`） |
| 未覆盖 | 12（`_empty`×2 + req_only×10） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | **10**（2 endpoint × 5） |
| 编号 | **API-000589**～**API-000598** |
| `_empty` 未覆盖 | **2** |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | **0** |
| code-registry | **未改**（父控回写） |
