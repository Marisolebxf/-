# 市场营销服务机构技术力评估 · 功能点覆盖（svc.tech-mkt / L46）

> catalog `svc.tech-mkt` · 50897 · path `/industry-service/tech-mkt`  
> 用例 `API-市场营销服务机构技术力评估-用例.md`  
> A 线范围：**L46**（`fp-split-by-api-run/work/L46.md`）  
> 功能点键：`L46 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| svc.tech-mkt.models | GET | /entan/v1/svc/models | API-000614～API-000618 | catalog `status=unavailable`；本页验收取 `kind=tech` |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L46 \| svc.tech-mkt.models \| kind \| 算法输入-kind模型类型 | catalog kind | API-000614、API-000616、API-000617 | 已覆盖 | TMKT-01 tech 主路径；非法 kind 见 02/616；非本页 gap 见 03/617 |
| L46 \| svc.tech-mkt.models \| tech \| 算法输出-tech技术力结果体 | catalog tech | API-000618 | 契约占位 | unavailable，禁止 sample 分值/排名作通过条件 |
| L46 \| svc.tech-mkt.models \| _empty \| 技术力评价无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「kind=tech 必空」试调证据 |
| L46 \| svc.tech-mkt.models \| _fail \| 技术力评价查询失败 | 契约错误态 | API-000614、API-000615、API-000616、API-000617 | 已覆盖 | 含 catalog 不可用、鉴权失败与 kind 失败语义 |
| L46 \| \| etl_clean_standardize \| 调研策划案例多源标准化 | 需规（1）采集清洗 | — | 未覆盖 | req_only |
| L46 \| \| core_indicator_threshold_weight \| 三维度指标与阈值权重体系 | 需规指标体系阈值 | — | 未覆盖 | req_only |
| L46 \| \| feature_metric_compute \| 三维度特征与指标数值计算 | 需规指标计算 | — | 未覆盖 | req_only |
| L46 \| \| weighted_aggregate_tech_index \| 加权聚合技术力指数 | 需规加权聚合 | — | 未覆盖 | req_only |
| L46 \| \| horizontal_rank_compare \| 横向对比行业排名语义 | 需规横向排名 | — | 未覆盖 | req_only |
| L46 \| \| subscore_weight_level_outputs \| 维度得分权重与水平分类输出 | 需规（2）分项权重分类 | — | 未覆盖 | req_only |
| L46 \| \| trend_analysis_report \| 趋势分析报告语义 | 需规（2）趋势报告 | — | 未覆盖 | req_only |
| L46 \| \| dynamic_monitor_weight_refresh \| 动态监测与指标权重更新 | 需规动态监测 | — | 未覆盖 | req_only |
| L46 \| \| org_industry_region_scope \| 机构行业地域查询语义 | 需规（3）调用范围 | — | 未覆盖 | req_only |
| L46 \| \| batch_auto_report \| 批量分析与自动化报告 | 需规（3）批量报告 | — | 未覆盖 | req_only |
| L46 \| \| api_sdk_embed \| API SDK 与业务系统嵌入 | 需规（3）API/SDK | — | 未覆盖 | req_only |

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
| 编号 | API-000614～API-000618 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
