# 产业周期分析 · A 线功能点覆盖（chain.cycle / L19）

> **catalog_page_id**：`chain.cycle` · path `/chain/cycle`  
> **A 线真源**：`fp-split-by-api-run/work/L19.md`  
> **用例册**：`API-产业周期分析-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00055`～`00058`，共 4 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/chain.json` 页 `chain.cycle`  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | catalog status | 用例编号 |
|-------------|--------|------|----------------|----------|
| chain.cycle.main | GET | /innov/v1/industry/{chainId}/cycle | unavailable | 00055、00056、00057、00058 |

---

## 2. 功能点 → 用例矩阵（L19 · catalog 可测行）

键：`L19 | endpoint_id | field_key | 功能点（A 线）`

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L19 \| chain.cycle.main \| chainId \| 算法输入-chainId产业标识 | catalog chainId | 00055、00057、00058 | 已覆盖 | 合法 example 契约请求 + 非法 id + 空 path 段 |
| L19 \| chain.cycle.main \| cycle.cycle_stage \| 算法输出-cycle.cycle_stage产业周期阶段 | catalog cycle.cycle_stage | 00055 | 契约占位 | endpoint unavailable；不得用 sample「成长期」作通过条件；Java 接通后改主流程断言 |
| L19 \| chain.cycle.main \| stage.sub_stage \| 算法输出-stage.sub_stage周期子阶段 | catalog stage.sub_stage | 00055 | 契约占位 | 同上 |
| L19 \| chain.cycle.main \| _empty \| 周期分析无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定可构造「合法 chainId 且无周期数据」条件；试调未获有效鉴权主路径，禁止编造必空参数 |
| L19 \| chain.cycle.main \| _fail \| 周期分析查询失败 | 契约错误态 | 00057、00058 | 已覆盖 | 非法 chainId 与空 path 占位触发可识别失败态 |

---

## 3. req_only 行（A 线 · 不拆 API 用例）

| 功能点键（field_key） | A 线功能点摘要 | 状态 | 说明 |
|----------------------|----------------|------|------|
| L19 \| — \| etl_clean_standardize | 历史与实时产业数据清洗 | 不投影 | 无 catalog endpoint 字段；模型侧验收 |
| L19 \| — \| cycle_stage_framework | 四阶段划分框架 | 不投影 | req_only |
| L19 \| — \| cycle_indicator_threshold | 阶段评价指标与阈值 | 不投影 | req_only |
| L19 \| — \| cycle_prediction_model | 预测模型训练与阶段识别 | 不投影 | req_only |
| L19 \| — \| future_trend_forecast | 未来趋势变化预测 | 不投影 | catalog 未列独立趋势 responseFields |
| L19 \| — \| multi_industry_cycle_compare | 多产业周期位置对比 | 不投影 | 单 chainId 查询，不发明对比 endpoint |
| L19 \| — \| dynamic_cycle_refresh | 周期判定动态更新 | 不投影 | req_only |
| L19 \| — \| cycle_visualization | 可视化趋势展示支撑 | 不投影 | viz 不进 API 断言 |
| L19 \| — \| trend_prediction_report | 趋势预测分析报告 | 不投影 | 无独立报告 path |
| L19 \| — \| api_sdk_export | API/SDK 与报告导出 | 不投影 | req_only |

---

## 4. 计数

| 项 | 值 |
|----|-----|
| API 用例条数 | 4 |
| 用例编号起止 | API-00055～API-00058 |
| `_empty` 未覆盖 | 1 行（见矩阵） |
| 试调 | 2026-10-17 主路径 1 次无 Bearer → HTTP 424，§0 已记；有效鉴权主路径未重试 |
| 产物路径 | `agent-delivery/qa/test-cases/SDWJSF-KJZTFWSFK/chain-产业链分析/CHAINCYCLE-产业周期分析/` |
