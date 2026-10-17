# 人力资源服务机构技术力评估 · 功能点覆盖（svc.tech-hr / L45）

> catalog `svc.tech-hr` · 50897 · path `/industry-service/tech-hr`  
> 用例 `API-人力资源服务机构技术力评估-用例.md`  
> A 线范围：**L45**（`fp-split-by-api-run/work/L45.md`）  
> 功能点键：`L45 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| svc.tech-hr.models | GET | /entan/v1/svc/models | API-00609～API-00613 | catalog `status=unavailable`；本页验收取 `kind=tech` |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L45 \| svc.tech-hr.models \| kind \| 算法输入-kind模型类型 | catalog kind | API-00609、API-00611、API-00612 | 已覆盖 | SVCTECHHR-01 tech 主路径；非法 kind 见 02/00611；非本页 gap 见 03/00612 |
| L45 \| svc.tech-hr.models \| tech \| 算法输出-tech技术力结果体 | catalog tech | API-00613 | 契约占位 | unavailable，禁止 sample 指数/排名作通过条件 |
| L45 \| svc.tech-hr.models \| _empty \| 技术力评价无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「kind=tech 必空」试调证据 |
| L45 \| svc.tech-hr.models \| _fail \| 技术力评价查询失败 | 契约错误态 | API-00609、API-00610、API-00611、API-00612 | 已覆盖 | 含 catalog 不可用、鉴权失败与 kind 失败语义 |
| L45 \| \| etl_clean_standardize \| 招聘服务与客户反馈多源标准化 | 需规（1）采集清洗 | — | 未覆盖 | req_only |
| L45 \| \| core_indicator_threshold_weight \| 核心指标与阈值权重体系 | 需规指标体系阈值 | — | 未覆盖 | req_only |
| L45 \| \| feature_metric_compute \| 特征提取与指标数值计算 | 需规指标计算 | — | 未覆盖 | req_only |
| L45 \| \| ml_aggregate_tech_index \| 机器学习多维聚合技术力指数 | 需规 ML 聚合 | — | 未覆盖 | req_only |
| L45 \| \| horizontal_rank_compare \| 横向对比行业排名语义 | 需规横向排名 | — | 未覆盖 | req_only |
| L45 \| \| subscore_threshold_outputs \| 分项得分与阈值对比输出语义 | 需规（2）分项阈值 | — | 未覆盖 | req_only |
| L45 \| \| trend_analysis_report \| 趋势分析报告语义 | 需规（2）趋势报告 | — | 未覆盖 | req_only |
| L45 \| \| dynamic_monitor_weight_refresh \| 动态监测与指标权重更新 | 需规动态监测 | — | 未覆盖 | req_only |
| L45 \| \| org_time_dimension_scope \| 机构与时间维度查询语义 | 需规（3）调用范围 | — | 未覆盖 | req_only |
| L45 \| \| auto_eval_continuous_monitor \| 自动化评估与持续监测 | 需规（3）系统对接 | — | 未覆盖 | req_only |
| L45 \| \| api_sdk_viz_platform \| API SDK 与可视化平台调用 | 需规（3）API/SDK | — | 未覆盖 | req_only |

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
| 编号 | API-00609～API-00613 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
