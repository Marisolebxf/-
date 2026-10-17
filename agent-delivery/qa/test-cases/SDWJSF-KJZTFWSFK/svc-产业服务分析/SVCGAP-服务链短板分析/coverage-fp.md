# 服务链短板分析 · 功能点覆盖（svc.gap / L41）

> catalog `svc.gap` · 50897 · path `/industry-service/gap`  
> 用例 `API-服务链短板分析-用例.md`  
> A 线范围：**L41**（`fp-split-by-api-run/work/L41.md`）  
> 功能点键：`L41 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| svc.gap.models | GET | /entan/v1/svc/models | API-000584～API-000588 | catalog `status=unavailable`；本页验收取 `kind=gap` |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L41 \| svc.gap.models \| kind \| 算法输入-kind模型类型 | catalog kind | API-000584、API-000586、API-000587 | 已覆盖 | SVCGAP-01 gap 主路径；非法 kind 见 02/586；非本页 relation 见 03/587 |
| L41 \| svc.gap.models \| gap \| 算法输出-gap短板分析结果体 | catalog gap | API-000588 | 契约占位 | unavailable，禁止 sample 环节/计数作通过条件 |
| L41 \| svc.gap.models \| _empty \| 短板分析无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「kind=gap 必空」试调证据 |
| L41 \| svc.gap.models \| _fail \| 短板分析查询失败 | 契约错误态 | API-000584、API-000585、API-000586、API-000587 | 已覆盖 | 含 catalog 不可用、鉴权失败与 kind 失败语义 |
| L41 \| \| etl_clean_standardize \| 服务机构多维度数据预处理 | 需规（1）采集预处理 | — | 未覆盖 | req_only |
| L41 \| \| quality_efficiency_type_indicators \| 服务质量效益类型指标体系 | 需规指标体系阈值 | — | 未覆盖 | req_only |
| L41 \| \| indicator_weak_link_locate \| 指标计算与短板环节定位 | 需规定位计算 | — | 未覆盖 | req_only |
| L41 \| \| cause_resource_process_match \| 资源流程匹配度成因识别 | 需规成因因素 | — | 未覆盖 | req_only |
| L41 \| \| gap_optimization_advice \| 针对性短板优化建议生成 | 需规（2）优化建议 | — | 未覆盖 | req_only |
| L41 \| \| dynamic_monitor_threshold_refresh \| 动态监测与指标阈值更新 | 需规动态监测 | — | 未覆盖 | req_only |
| L41 \| \| org_tag_dimension_time_scope \| 服务机构标签维度时间区间语义 | 需规（3）调用范围 | — | 未覆盖 | req_only |
| L41 \| \| auto_monitor_trend_alert \| 短板自动监测与趋势预警 | 需规（3）监测预警 | — | 未覆盖 | req_only |
| L41 \| \| locate_cause_advice_outputs \| 短板定位成因三类输出语义 | 需规（2）三类输出 | — | 未覆盖 | req_only |
| L41 \| \| api_sdk_ops_platform \| API SDK 与运营系统集成 | 需规（3）系统对接 | — | 未覆盖 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`kind`、`_fail`） |
| 契约占位 | 1（`gap`） |
| 未覆盖 | 11（含 `_empty` 1 + req_only 10） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-000584～API-000588 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
