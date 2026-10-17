# 产业阶段分析 · A 线功能点覆盖（chain.stage / L20）

> **catalog_page_id**：`chain.stage` · path `/chain/stage`  
> **A 线真源**：`fp-split-by-api-run/work/L20.md`（矩阵键来自 L20 grep + catalog；本子任务未读 work 全文）  
> **用例册**：`API-产业阶段分析-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00340`～`00349`，共 10 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/chain.json` 页 `chain.stage`  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | catalog status | 用例编号 |
|-------------|--------|------|----------------|----------|
| chain.stage.main | GET | /innov/v1/industry/{chainId}/cycle | unavailable | 00340、00341、00342、00343、00344、00345、00346、00347、00348、00349 |

> **同 path 说明**：`chain.cycle.main` 与 `chain.stage.main` 共用 path；B 线以 `catalog_page_id` + `endpoint_id` 区分矩阵，禁止与 L19 用例混抄预期。

---

## 2. 功能点 → 用例矩阵（L20 · catalog 可测行）

键：`L20 | endpoint_id | field_key | 功能点（A 线）`

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L20 \| chain.stage.main \| chainId \| 算法输入-chainId产业标识 | catalog chainId | 00340、00344、00345、00346 | 已覆盖 | 合法 example 契约请求 + 非法 id + 空 path + 空白 id |
| L20 \| chain.stage.main \| cycle.cycle_stage \| 算法输出-cycle.cycle_stage产业主阶段 | catalog cycle.cycle_stage | 00340、00347 | 契约占位 | endpoint unavailable；不得用 sample「成长期」作通过条件；接通后改主流程断言 |
| L20 \| chain.stage.main \| stage.sub_stage \| 算法输出-stage.sub_stage产业子阶段 | catalog stage.sub_stage | 00340、00348 | 契约占位 | 同上 |
| L20 \| chain.stage.main \| _empty \| 产业阶段判定无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定可构造「合法 chainId 且指标不足无法判定」条件；§0 未试调，禁止编造必空参数 |
| L20 \| chain.stage.main \| _fail \| 产业阶段查询失败 | 契约错误态 | 00344、00345、00346、00349 | 已覆盖 | 非法 chainId、空 path、错误 HTTP 方法 |

---

## 3. req_only 行（A 线 · 不拆 API 用例）

| 功能点键（field_key） | A 线功能点摘要 | 状态 | 说明 |
|----------------------|----------------|------|------|
| L20 \| — \| etl_clean_standardize | 多源权威数据标准化整合 | 不投影 | 无 catalog endpoint 字段 |
| L20 \| — \| stage_indicator_system | 阶段判定关键指标体系 | 不投影 | req_only |
| L20 \| — \| indicator_weight_params | 指标权重参数分配 | 不投影 | req_only |
| L20 \| — \| cycle_model_stage_map | 周期模型阶段映射计算 | 不投影 | req_only |
| L20 \| — \| model_historical_calibration | 历史数据验证与模型优化 | 不投影 | req_only |
| L20 \| — \| scheduled_stage_refresh | 阶段结果周期性自动更新 | 不投影 | req_only |
| L20 \| — \| stage_analysis_report | 阶段分析报告 | 不投影 | 无独立报告 path |
| L20 \| — \| trend_prediction_chart_data | 趋势变化预测图表数据 | 不投影 | viz 不进 API 断言 |
| L20 \| — \| api_result_sync | API 结果服务化同步 | 不投影 | 与本 GET 重合，不重复拆行 |
| L20 \| — \| sdk_invocation | SDK 调用支持 | 不投影 | req_only |
| L20 \| — \| report_chart_export | 分析报告与数据导出 | 不投影 | req_only |

---

## 4. 计数

| 项 | 值 |
|----|-----|
| API 用例条数 | 10 |
| 用例编号起止 | API-00340～API-00349 |
| `_empty` 未覆盖 | 1 行（见矩阵） |
| 试调 | **未试调**（§0）；父控禁止 curl |
| 产物路径 | `agent-delivery/qa/test-cases/SDWJSF-KJZTFWSFK/chain-产业链分析/CHAINSTAGE-产业阶段分析/` |
| code-registry | **未回写**（父控约束） |
