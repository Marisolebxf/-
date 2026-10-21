# 产业周期分析 · 功能点覆盖（chain.cycle / L19）

> catalog `chain.cycle` · path `#/chain/cycle`  
> A 线真源：`fp-split-by-api-run/work/L19.md`  
> B 线用例：`FUNC-产业周期分析-用例.md`（第三轮 **FUNC-00449**～**00454**）  
> 历史 R2 API 册：`API-产业周期分析-用例.md`（**API-01258**～**01261**，第三轮不复用编号）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| chain.cycle.main | GET | /innov/v1/industry/{chainId}/cycle | FUNC-00449、00450 | unavailable |
| chain.cycle.m_chain_deep_122_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_122_1/compute | FUNC-00451、00452 | available |
| （页面清单） | — | — | FUNC-00453、00454 | — |

---

## 功能点 → 用例矩阵（挂 L19.md）

多条 field 挂同一用例。不按 field 另开用例。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L19 \| chain.cycle.main \| chainId \| 算法输入-chainId产业标识 | FUNC-00449、00450 | 已覆盖 | 合法 chainId=INB1701 + 缺 chainId；规则来源 catalog chainId |
| L19 \| chain.cycle.main \| cycle.cycle_stage \| 算法输出-cycle.cycle_stage产业周期阶段 | FUNC-00449 | 已覆盖 | 主流程断言 cycle.cycle_stage（string）；规则来源 catalog cycle.cycle_stage |
| L19 \| chain.cycle.main \| stage.sub_stage \| 算法输出-stage.sub_stage周期子阶段 | FUNC-00449 | 已覆盖 | 同条主流程断言 stage.sub_stage（string）；规则来源 catalog stage.sub_stage |
| L19 \| chain.cycle.main \| _empty \| 周期分析无数据空态 | — | 未覆盖 | 无稳定「合法 chainId 且无周期数据」构造条件；规则来源 契约空结果 |
| L19 \| chain.cycle.main \| _fail \| 周期分析查询失败 | FUNC-00450 | 部分覆盖 | 仅缺 chainId 反向（message/msg）；规则来源 契约错误态 |

---

## req_only 行（无 endpoint 挂接）

L19.md 中下列 field 的 endpoint_id 为空、`catalog_status=req_only`，catalog 无对应入参或 responseFields。B 线记 **无对应功能点**，不单独开 FUNC 用例：

`etl_clean_standardize`（历史与实时产业数据清洗）、`cycle_stage_framework`（四阶段划分框架）、`cycle_indicator_threshold`（阶段评价指标与阈值）、`cycle_prediction_model`（预测模型训练与阶段识别）、`future_trend_forecast`（未来趋势变化预测）、`multi_industry_cycle_compare`（多产业周期位置对比）、`dynamic_cycle_refresh`（周期判定动态更新）、`cycle_visualization`（可视化趋势展示支撑）、`trend_prediction_report`（趋势预测分析报告）、`api_sdk_export`（API/SDK 与报告导出）。

---

## B 线独有（catalog 有、L19 未挂 endpoint）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L19 \| chain.cycle.m_chain_deep_122_1 \| — \| 产业周期分析模型 | FUNC-00451、00452 | 无对应功能点 | 下拉 title 仍写主流程（metric_id、hint）与缺 chainId；L19 未给该 endpoint 挂 field 行 |
| （页面清单） \| 接口信息 / 算法测试 | FUNC-00453、00454 | 无对应功能点 | 2 接口下拉与 method/path 刷新 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| FUNC 用例数 | 6 |
| 主流程 | 2（FUNC-00449 产业周期分析、FUNC-00451 产业周期分析模型） |
| 反向 | 2（FUNC-00450、00452，均为缺 chainId） |
| 清单 | 2（FUNC-00453、00454） |
| 编号 | FUNC-00449～00454 |
| L19 挂接行 | 5（已覆盖 3、部分覆盖 1、未覆盖 1） |
| L19 req_only | 10（无对应功能点） |
