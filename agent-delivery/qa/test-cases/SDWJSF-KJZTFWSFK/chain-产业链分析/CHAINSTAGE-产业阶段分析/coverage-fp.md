# 产业阶段分析 · 功能点覆盖（chain.stage / L20）

> catalog `chain.stage` · path `#/chain/stage`  
> A 线真源：`fp-split-by-api-run/work/L20.md`  
> B 线用例：`API-产业阶段分析-用例.md`（第二轮 **API-01262**～**01265**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| chain.stage.main | GET | /innov/v1/industry/{chainId}/cycle | API-01262、01263 | unavailable |
| chain.stage.m_chain_deep_123_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_123_1/compute | API-01264、01265 | available |

---

## 功能点 → 用例矩阵（挂 L20.md）

多条 field 挂同一用例。不按 field 另开用例。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L20 \| chain.stage.main \| chainId \| 算法输入-chainId产业标识 | API-01262、01263 | 已覆盖 | 合法 path chainId=INB1701 + 缺 chainId；规则来源 catalog chainId |
| L20 \| chain.stage.main \| cycle.cycle_stage \| 算法输出-cycle.cycle_stage产业主阶段 | API-01262 | 已覆盖 | 主流程断言 cycle.cycle_stage（string）；规则来源 catalog cycle.cycle_stage |
| L20 \| chain.stage.main \| stage.sub_stage \| 算法输出-stage.sub_stage产业子阶段 | API-01262 | 已覆盖 | 同条主流程断言 stage.sub_stage（string）；规则来源 catalog stage.sub_stage |
| L20 \| chain.stage.main \| _empty \| 产业阶段判定无数据空态 | — | 未覆盖 | 无稳定「合法 chainId 且无阶段数据」构造条件；规则来源 契约空结果 |
| L20 \| chain.stage.main \| _fail \| 产业阶段查询失败 | API-01263 | 部分覆盖 | 仅缺 chainId 反向（message/msg）；规则来源 契约错误态 |

---

## req_only 行（无 endpoint 挂接）

L20.md 中下列 field 的 endpoint_id 为空、`catalog_status=req_only`，catalog 无对应入参或 responseFields。B 线记 **无对应功能点**，不单独开 API 用例：

`etl_clean_standardize`（多源权威数据标准化整合）、`stage_indicator_system`（阶段判定关键指标体系）、`indicator_weight_params`（指标权重参数分配）、`cycle_model_stage_map`（周期模型阶段映射计算）、`model_historical_calibration`（历史数据验证与模型优化）、`scheduled_stage_refresh`（阶段结果周期性自动更新）、`stage_analysis_report`（阶段分析报告）、`trend_prediction_chart_data`（趋势变化预测图表数据）、`api_result_sync`（API 结果服务化同步）、`sdk_invocation`（SDK 调用支持）、`report_chart_export`（分析报告与数据导出）。

---

## B 线独有（catalog 有、L20 未挂 endpoint）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L20 \| chain.stage.m_chain_deep_123_1 \| — \| 产业阶段分析模型 | API-01264、01265 | 无对应功能点 | 下拉 title 仍写主流程（metric_id、hint）与缺 chainId；L20 未给该 endpoint 挂 field 行 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| API 用例数 | 4 |
| 主流程 | 2（API-01262 产业阶段分析、API-01264 产业阶段分析模型） |
| 反向 | 2（API-01263、01265，均为缺 chainId） |
| 编号 | API-01262～01265 |
| L20 挂接行 | 5（已覆盖 3、部分覆盖 1、未覆盖 1） |
| L20 req_only | 11（无对应功能点） |
