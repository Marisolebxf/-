# 政策短板识别 · 功能点覆盖（policy.gap / L38）

> catalog `policy.gap` · 50897 · path `/policy/gap`  
> 用例 `API-政策短板识别-用例.md`  
> A 线范围：**L38**（`fp-split-by-api-run/work/L38.md`）  
> 功能点键：`L38 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| policy.gap.shortboard | GET | /policy/v1/policy/analysis/gap | API-000469～API-000473 | catalog `status=unavailable`；不含 `policy.gap.opportunity`（属 `policy.opportunity` 页） |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L38 \| policy.gap.shortboard \| scope_code \| 算法输入-scope_code范围编码 | catalog scope_code | API-000469、API-000471 | 部分覆盖 | GAP-01 不传 scope；非法 scope 见 GAP-02 / API-000471 |
| L38 \| policy.gap.shortboard \| limit \| 算法输入-limit结果条数上限 | catalog limit | API-000469、API-000472 | 已覆盖 | 主路径 limit=20 + 非正整数失败 |
| L38 \| policy.gap.shortboard \| shortboard_cnt \| 算法输出-shortboard_cnt短板数 | catalog shortboard_cnt | API-000473 | 契约占位 | unavailable，禁止 sample 计数作通过条件 |
| L38 \| policy.gap.shortboard \| _empty \| 短板分析无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「合法入参必空」试调证据 |
| L38 \| policy.gap.shortboard \| _fail \| 短板分析查询失败 | 契约错误态 | API-000469、API-000470、API-000471、API-000472 | 已覆盖 | 含 catalog 不可用、鉴权失败与入参失败语义 |
| L38 \| \| etl_clean_standardize \| 多源政策与执行反馈数据标准化 | 需规（1） | — | 未覆盖 | req_only |
| L38 \| \| coverage_exec_goal_compliance_dims \| 覆盖执行目标合规四维指标体系 | 需规四维指标 | — | 未覆盖 | req_only |
| L38 \| \| indicator_weight_eval \| 维度指标计算与权重评估 | 需规权重评估 | — | 未覆盖 | req_only |
| L38 \| \| below_threshold_shortboard_id \| 低于阈值短板项识别 | 需规阈值识别 | — | 未覆盖 | req_only |
| L38 \| \| shortboard_list_structured \| 政策短板清单结构化输出 | 需规（2）短板清单 | — | 未覆盖 | req_only |
| L38 \| \| cause_analysis_association \| 短板成因与关联定位 | 需规（2）成因关联 | — | 未覆盖 | req_only |
| L38 \| \| improvement_strategy_suggest \| 改进策略建议输出 | 需规（2）改进建议 | — | 未覆盖 | req_only |
| L38 \| \| policy_tag_time_dimension_scope \| 政策标签时间区间与分析维度查询 | 需规（3）检索条件 | — | 未覆盖 | req_only |
| L38 \| \| monitoring_trend_push \| 在线监测趋势与策略推送 | 需规监测趋势推送 | — | 未覆盖 | req_only |
| L38 \| \| api_sdk_platform_gap \| API SDK 与政策管理平台对接 | 需规（3）平台对接 | — | 未覆盖 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`limit`、`_fail`） |
| 部分覆盖 | 1（`scope_code`） |
| 契约占位 | 1（`shortboard_cnt`） |
| 未覆盖 | 11（含 `_empty` 1 + req_only 10） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-000469～API-000473 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
