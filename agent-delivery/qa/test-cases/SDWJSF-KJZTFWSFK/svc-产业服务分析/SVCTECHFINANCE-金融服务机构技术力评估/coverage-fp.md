# 金融服务机构技术力评估 · 功能点覆盖（svc.tech-finance / L43）

> catalog `svc.tech-finance` · path `#/industry-service/tech-finance`  
> A 线真源：`fp-split-by-api-run/work/L43.md`  
> B 线用例：`FUNC-金融服务机构技术力评估-用例.md`（第三轮 **FUNC-00884**～**FUNC-00891**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| svc.tech-finance.models | GET | /entan/v1/svc/models | FUNC-00884～00886 | unavailable |
| svc.tech-finance.m_svc_deep_174_1 | POST | /entan/v1/svc-metric/metric/M_SVC_DEEP_174_1/compute | FUNC-00887～00889 | available |
| （页面清单） | — | — | FUNC-00890、00891 | — |

---

## 功能点 → 用例矩阵（挂 L43.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L43 \| svc.tech-finance.models \| kind \| 算法输入-kind模型类型 | catalog kind | FUNC-00884、00885、00886 | 已覆盖 | 主路径 kind=tech + 省略可选 kind + 非法 kind=__invalid__ |
| L43 \| svc.tech-finance.models \| tech \| 算法输出-tech技术力结果体 | catalog tech | FUNC-00884、00885 | 已覆盖 | 主流程断言 tech 元素 org_id、service_type、score、ext、dimension_scores；备选同结构 |
| L43 \| svc.tech-finance.models \| _empty \| 技术力评价无数据空态 | 契约空结果 | — | 未覆盖 | sampleResponse.tech 为两条非空机构，无稳定空名单构造条件，不单开空态用例 |
| L43 \| svc.tech-finance.models \| _fail \| 技术力评价查询失败 | 契约错误态 | FUNC-00886 | 部分覆盖 | 仅非法 kind 反向，预期 message 或 msg 指出 kind 非法 |

---

## req_only 行（无 endpoint 挂接）

L43.md 中 `etl_clean_standardize`、`scale_cost_risk_service_indicators`、`standardize_weight_tech_index`、`dimension_scores_in_tech`、`strength_weakness_analysis`、`cross_org_trend_reports`、`org_name_tag_time_scope`、`batch_auto_monitor_refresh`、`bundled_outputs_in_tech`、`api_sdk_finance_platform` 共 10 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 FUNC 用例。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L43 \| \| etl_clean_standardize \| 财务融资风险服务多源预处理 | 需规（1）采集预处理 | — | 无对应功能点 | req_only |
| L43 \| \| scale_cost_risk_service_indicators \| 四维指标与阈值体系 | 需规指标体系阈值 | — | 无对应功能点 | req_only |
| L43 \| \| standardize_weight_tech_index \| 标准化加权与技术力指数 | 需规定量计算 | — | 无对应功能点 | req_only |
| L43 \| \| dimension_scores_in_tech \| 各维度单项分值输出语义 | 需规（2）维度分值 | — | 无对应功能点 | req_only；维度分已写入 models 正向预期的 dimension_scores，不另开用例 |
| L43 \| \| strength_weakness_analysis \| 能力优势与不足分析 | 需规（2）优劣势 | — | 无对应功能点 | req_only |
| L43 \| \| cross_org_trend_reports \| 跨机构比较与历年趋势 | 需规（2）比较趋势 | — | 无对应功能点 | req_only |
| L43 \| \| org_name_tag_time_scope \| 机构名称标签时间周期语义 | 需规（3）调用范围 | — | 无对应功能点 | req_only |
| L43 \| \| batch_auto_monitor_refresh \| 批量处理与自动化趋势监测 | 需规（3）批量监测 | — | 无对应功能点 | req_only |
| L43 \| \| bundled_outputs_in_tech \| 四类核心输出语义打包 | 需规（2）四类输出 | — | 无对应功能点 | req_only |
| L43 \| \| api_sdk_finance_platform \| API SDK 与金融监管平台集成 | 需规（3）系统对接 | — | 无对应功能点 | req_only |

---

## B 线独有（A 线未列 endpoint）

| endpoint_id | 对应用例编号 | 状态 | 说明 |
|-------------|--------------|------|------|
| svc.tech-finance.m_svc_deep_174_1 | FUNC-00887～00889 | 无对应功能点 | L43 未列该 compute endpoint 的 field_key；用例仍按 catalog 编写 |

sampleResponse 中 tech 元素的 org_id、service_type、score、ext.name、ext.rank_no、dimension_scores（patents、rdInvestment、experts、cases、standards）已写入 models 正向预期；A 线只列顶层 field_key `tech`，不按子成员拆行。compute 的 sampleResponse 只有 metric_id、hint，responseFields 另列 tech 且无元素示例，正向预期已分开写明。
