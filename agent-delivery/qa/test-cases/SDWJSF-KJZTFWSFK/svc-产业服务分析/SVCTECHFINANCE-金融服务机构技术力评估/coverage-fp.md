# 金融服务机构技术力评估 · 功能点覆盖（svc.tech-finance / L43）

> catalog `svc.tech-finance` · 50897 · path `/industry-service/tech-finance`  
> 用例 `API-金融服务机构技术力评估-用例.md`  
> A 线范围：**L43**（`fp-split-by-api-run/work/L43.md`）  
> 功能点键：`L43 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| svc.tech-finance.models | GET | /entan/v1/svc/models | API-000599～API-000603 | catalog `status=unavailable`；本页验收取 `kind=tech` |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L43 \| svc.tech-finance.models \| kind \| 算法输入-kind模型类型 | catalog kind | API-000599、API-000601、API-000602 | 已覆盖 | STF-01 tech 主路径；非法 kind 见 02/601；非本页 gap 见 03/602 |
| L43 \| svc.tech-finance.models \| tech \| 算法输出-tech技术力结果体 | catalog tech | API-000603 | 契约占位 | unavailable，禁止 sample 分值/排名/维度分作通过条件 |
| L43 \| svc.tech-finance.models \| _empty \| 技术力评价无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「kind=tech 必空」试调证据 |
| L43 \| svc.tech-finance.models \| _fail \| 技术力评价查询失败 | 契约错误态 | API-000599、API-000600、API-000601、API-000602 | 已覆盖 | 含 catalog 不可用、鉴权失败与 kind 失败语义 |
| L43 \| \| etl_clean_standardize \| 财务融资风险服务多源预处理 | 需规（1）采集预处理 | — | 未覆盖 | req_only |
| L43 \| \| scale_cost_risk_service_indicators \| 四维指标与阈值体系 | 需规指标体系阈值 | — | 未覆盖 | req_only |
| L43 \| \| standardize_weight_tech_index \| 标准化加权与技术力指数 | 需规定量计算 | — | 未覆盖 | req_only |
| L43 \| \| dimension_scores_in_tech \| 各维度单项分值输出语义 | 需规（2）维度分值 | — | 未覆盖 | req_only |
| L43 \| \| strength_weakness_analysis \| 能力优势与不足分析 | 需规（2）优劣势 | — | 未覆盖 | req_only |
| L43 \| \| cross_org_trend_reports \| 跨机构比较与历年趋势 | 需规（2）比较趋势 | — | 未覆盖 | req_only |
| L43 \| \| org_name_tag_time_scope \| 机构名称标签时间周期语义 | 需规（3）调用范围 | — | 未覆盖 | req_only |
| L43 \| \| batch_auto_monitor_refresh \| 批量处理与自动化趋势监测 | 需规（3）批量监测 | — | 未覆盖 | req_only |
| L43 \| \| bundled_outputs_in_tech \| 四类核心输出语义打包 | 需规（2）四类输出 | — | 未覆盖 | req_only |
| L43 \| \| api_sdk_finance_platform \| API SDK 与金融监管平台集成 | 需规（3）系统对接 | — | 未覆盖 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`kind`、`_fail`） |
| 契约占位 | 1（`tech`） |
| 未覆盖 | 11（含 `_empty` 1 + req_only 10） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-000599～API-000603 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
