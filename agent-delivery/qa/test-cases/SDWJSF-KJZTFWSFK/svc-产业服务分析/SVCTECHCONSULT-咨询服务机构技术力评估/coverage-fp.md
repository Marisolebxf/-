# 咨询服务机构技术力评估 · 功能点覆盖（svc.tech-consult / L47）

> catalog `svc.tech-consult` · 50897 · path `/industry-service/tech-consult`  
> 用例 `API-咨询服务机构技术力评估-用例.md`  
> A 线范围：**L47**（`fp-split-by-api-run/work/L47.md`）  
> 功能点键：`L47 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| svc.tech-consult.models | GET | /entan/v1/svc/models | API-000619～API-000623 | catalog `status=unavailable`；本页验收取 `kind=tech` |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L47 \| svc.tech-consult.models \| kind \| 算法输入-kind模型类型 | catalog kind | API-000619、API-000621、API-000622 | 已覆盖 | TCONSULT-01 tech 主路径；非法 kind 见 02/621；非本页 gap 见 03/622 |
| L47 \| svc.tech-consult.models \| tech \| 算法输出-tech技术力结果体 | catalog tech | API-000623 | 契约占位 | unavailable，禁止 sample 分值/排名作通过条件 |
| L47 \| svc.tech-consult.models \| _empty \| 技术力评价无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「kind=tech 必空」试调证据 |
| L47 \| svc.tech-consult.models \| _fail \| 技术力评价查询失败 | 契约错误态 | API-000619、API-000620、API-000621、API-000622 | 已覆盖 | 含 catalog 不可用、鉴权失败与 kind 失败语义 |
| L47 \| \| etl_clean_standardize \| 公开授权调研多源标准化 | 需规（1）采集标准化 | — | 未覆盖 | req_only |
| L47 \| \| consult_four_dim_threshold_weight \| 四维指标与专家权重阈值 | 需规指标体系阈值 | — | 未覆盖 | req_only |
| L47 \| \| dimension_metric_compute \| 四维指标数值计算 | 需规维内计算 | — | 未覆盖 | req_only |
| L47 \| \| weighted_tech_index_synthesis \| 加权合成技术力指数 | 需规加权指数 | — | 未覆盖 | req_only |
| L47 \| \| strength_weakness_gap_list \| 优势与短板分析清单 | 需规（2）优短板清单 | — | 未覆盖 | req_only |
| L47 \| \| improvement_direction_suggestions \| 改进建议与潜在发展方向 | 需规（2）改进方向 | — | 未覆盖 | req_only |
| L47 \| \| trend_analysis_report \| 趋势分析报告语义 | 需规（2）趋势报告 | — | 未覆盖 | req_only |
| L47 \| \| org_name_industry_time_scope \| 机构名称行业类型时间范围 | 需规（3）调用范围 | — | 未覆盖 | req_only |
| L47 \| \| batch_auto_eval_viz \| 批量分析与自动化评估 | 需规（3）批量自动化 | — | 未覆盖 | req_only |
| L47 \| \| bundled_outputs_in_tech \| 四类核心输出语义打包 | 需规（2）四类输出 | — | 未覆盖 | req_only |
| L47 \| \| api_sdk_decision_platform \| API SDK 与政府企业投资平台 | 需规（3）系统对接 | — | 未覆盖 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`kind`、`_fail`） |
| 契约占位 | 1（`tech`） |
| 未覆盖 | 12（含 `_empty` 1 + req_only 11） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-000619～API-000623 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
