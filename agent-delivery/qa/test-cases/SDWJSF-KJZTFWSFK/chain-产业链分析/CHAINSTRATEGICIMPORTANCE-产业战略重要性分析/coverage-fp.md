# 产业战略重要性分析 · A 线功能点覆盖（chain.strategic-importance）

> **catalog_page_id**：`chain.strategic-importance` · path `/chain/strategic-importance`  
> **A 线真源**：`fp-split-by-api-run/_catalog-snapshot.md`（1 endpoint、unavailable×1）；`_l6-to-catalog-map.yaml` **无六级 work/Lxx**（60 条无对应六级）  
> **用例册**：`API-产业战略重要性分析-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000404`～`000408`，共 5 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/chain.json` 页 `chain.strategic-importance` · `chain.strategic-importance.main`  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | catalog status | 用例编号 |
|-------------|--------|------|----------------|----------|
| chain.strategic-importance.main | GET | /innov/v1/industry/{chainId}/strategic-importance | unavailable | 000404、000405、000406、000407、000408 |

---

## 2. 功能点 → 用例矩阵（catalog 可测行 · 待 A 线合表）

键：`Lxx | endpoint_id | field_key | 功能点（A 线）` — **Lxx 待六级合表后替换**；当前以 catalog + snapshot 对齐。

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| 待合表 \| chain.strategic-importance.main \| chainId \| 算法输入-chainId产业标识 | catalog chainId | 000404、000406、000407 | 已覆盖 | 合法 example 契约请求 + 非法 id + 空 path 段 |
| 待合表 \| chain.strategic-importance.main \| rows \| 算法输出-rows环节战略重要性 | catalog rows | 000404、000408 | 契约占位 / 形态 | endpoint unavailable；000404 禁止 sample 评分作通过条件；000408 仅断言 array 形态 |
| 待合表 \| chain.strategic-importance.main \| _empty \| 战略重要性无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定可构造「合法 chainId 且无环节评分」条件；§0 未试调，禁止编造必空参数 |
| 待合表 \| chain.strategic-importance.main \| _fail \| 战略重要性查询失败 | 契约错误态 | 000406、000407 | 已覆盖 | 非法 chainId 与空 path 占位触发可识别失败态 |

---

## 3. B 线独有 / 不投影

| 项 | 说明 |
|----|------|
| `viz` bar/table | 联调台图表配置，不进 API 断言 |
| `metricIds` M_CHAIN_STRATEGIC_IMPORTANCE | 指标追溯列扩展用，不进用例正文 |

---

## 4. 计数

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 用例编号起止 | API-000404～API-000408 |
| FUNC 条数 | 0 |
| `_empty` 未覆盖 | 1 行（见矩阵） |
| A 线六级 | **待 A 线合表核对** |
| 试调 | **未试调**（子任务 §0 约束） |
| 产物路径 | `agent-delivery/qa/test-cases/SDWJSF-KJZTFWSFK/chain-产业链分析/CHAINSTRATEGICIMPORTANCE-产业战略重要性分析/` |
