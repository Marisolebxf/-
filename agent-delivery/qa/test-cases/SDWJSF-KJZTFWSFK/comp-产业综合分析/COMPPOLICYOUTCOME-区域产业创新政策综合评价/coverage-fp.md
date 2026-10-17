# 区域产业创新政策综合评价 · 功能点覆盖（comp.policy-outcome / L54）

> catalog `comp.policy-outcome` · 50897 · path `#/industry-comp/policy-outcome`  
> 用例 `API-区域产业创新政策综合评价-用例.md`  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json`（页 `comp.policy-outcome`）  
> 功能点键：`L54 | endpoint_id | field_key | 功能点中文`（矩阵键与 A 线 by-api 对齐）  
> 编排：`algo-lib-api-case-playbook.md` §编写细则 H、§I  

> **path 独占**：`GET /comp/v1/comp/region-policy-outcome` 为本页独占；与同模块 `region-tech-outcome`、`region-industry-outcome` 等其它 outcome path 禁止混抄预期。

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| comp.policy-outcome.main | GET | /comp/v1/comp/region-policy-outcome | API-00669～00673 | catalog `unavailable`；§0 **未试调**；本批 **金样 5 条**；非 kind 套餐 |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L54 \| comp.policy-outcome.main \| region \| 算法输入-region区域标签 | catalog region | API-00669、00671 | 已覆盖 | 主路径占位 + 非法 region |
| L54 \| comp.policy-outcome.main \| year \| 算法输入-year年份 | catalog year | API-00669、00672 | 已覆盖 | 主路径占位 + 非法 year |
| L54 \| comp.policy-outcome.main \| index \| 算法输出-index政策创新成果指数 | catalog index | API-00673 | 部分覆盖 | unavailable 金样批仅写字段形态；live 成功数值语义待升档补 |
| L54 \| comp.policy-outcome.main \| _empty \| 政策成果评价无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定空态构造；§0 未试调 |
| L54 \| comp.policy-outcome.main \| _fail \| 政策成果评价查询失败 | 契约错误态 | API-00670、00671、00672 | 已覆盖 | 鉴权、非法 region、非法 year |
| L54 \| comp.policy-outcome.main \| etl_nlp_policy_standardize \| 政策专题库采集与文本结构化 | 需规（1）采集预处理 | — | 无对应功能点 | req_only |
| L54 \| comp.policy-outcome.main \| three_dim_indicators_threshold \| 三维政策指标体系与阈值 | 需规指标体系阈值 | — | 无对应功能点 | req_only |
| L54 \| comp.policy-outcome.main \| weight_threshold_synthesis \| 维度指标加权综合指数 | 需规加权综合 | — | 无对应功能点 | req_only |
| L54 \| comp.policy-outcome.main \| dimension_sub_eval_results \| 单维度分项评价结果 | 需规（2）分项评价 | — | 无对应功能点 | req_only |
| L54 \| comp.policy-outcome.main \| regional_rank_compare \| 区域排名与横向对比 | 需规区域对比排名 | — | 无对应功能点 | req_only |
| L54 \| comp.policy-outcome.main \| trend_viz_analysis_report \| 趋势分析与可视化报告 | 需规趋势可视化 | — | 无对应功能点 | req_only |
| L54 \| comp.policy-outcome.main \| historical_time_series \| 历史对比与时间序列分析 | 需规历史时序 | — | 无对应功能点 | req_only |
| L54 \| comp.policy-outcome.main \| region_time_policy_category_scope \| 区域时间政策类别查询语义 | 需规（3）调用范围 | — | 无对应功能点 | req_only |
| L54 \| comp.policy-outcome.main \| online_monitor_refresh \| 在线监测与结果刷新 | 需规（3）监测展示 | — | 无对应功能点 | req_only |
| L54 \| comp.policy-outcome.main \| index_sub_rank_advice_outputs \| 指数分项排名建议四类输出 | 需规（2）四类输出 | — | 无对应功能点 | req_only |
| L54 \| comp.policy-outcome.main \| api_sdk_decision_platform \| API SDK 与决策分析系统对接 | 需规（3）系统对接 | — | 无对应功能点 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖（可测 API field / 哨兵） | 4（region、year、_fail；index 形态部分） |
| 未覆盖（契约 field / _empty） | 2（index live 语义、_empty） |
| 无对应功能点（req_only） | 11 |
| API 用例条数 | 5（00669～00673） |
| 金样 | API-00669 |

---

## 4. §I 计数

| 项 | 值 |
|----|-----|
| FUNC | 0 |
| API | 5 |
| 金样 | API-00669 |
| 试调 | **未试调**（§0；金样执行期复核信封） |
