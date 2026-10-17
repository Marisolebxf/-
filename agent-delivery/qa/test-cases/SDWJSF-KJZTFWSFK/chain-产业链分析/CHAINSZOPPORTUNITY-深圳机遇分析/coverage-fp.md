# 深圳机遇分析 · A 线功能点覆盖（chain.sz-opportunity / L25）

> **catalog_page_id**：`chain.sz-opportunity` · path `/chain/sz-opportunity`  
> **A 线真源**：`fp-split-by-api-run/work/L25.md`（矩阵键来自 L25 grep + catalog；本子任务未读 work 全文）  
> **用例册**：`API-深圳机遇分析-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00384`～`00388`，共 5 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/chain.json` 页 `chain.sz-opportunity`  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | catalog status | 用例编号 |
|-------------|--------|------|----------------|----------|
| chain.sz-opportunity.main | GET | /innov/v1/industry/{chainId}/shenzhen | unavailable | 00384、00385、00386、00387、00388 |

> **同 path 说明**：`chain.shenzhen.main`、`chain.sz-problem.main` 与 `chain.sz-opportunity.main` 共用 path；B 线以 `catalog_page_id` + `endpoint_id` 区分矩阵，禁止与 L18/L24 用例混抄预期。

---

## 2. 功能点 → 用例矩阵（L25 · catalog 可测行）

键：`L25 | endpoint_id | field_key | 功能点（A 线）`

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L25 \| chain.sz-opportunity.main \| chainId \| 算法输入-chainId产业标识 | catalog chainId | 00384、00386 | 已覆盖 | 合法 example 契约请求 + 非法 id |
| L25 \| chain.sz-opportunity.main \| panorama.enterprise_count \| 算法输出-panorama.enterprise_count深圳企业数 | catalog panorama.enterprise_count | 00384、00387 | 契约占位 | endpoint unavailable；不得用 sample 企业数作通过条件；接通后改主流程断言 |
| L25 \| chain.sz-opportunity.main \| panorama.nodes \| 算法输出-panorama.nodes深圳机遇环节节点 | catalog panorama.nodes | 00384、00388 | 契约占位 | 同上；空数组与 _fail 执行期区分 |
| L25 \| chain.sz-opportunity.main \| _empty \| 深圳机遇分析无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定可构造「合法 chainId 且无机遇推荐」条件；§0 未试调，禁止编造必空参数 |
| L25 \| chain.sz-opportunity.main \| _fail \| 深圳机遇分析查询失败 | 契约错误态 | 00386 | 已覆盖 | 非法 chainId；鉴权失败见 00385 |

---

## 3. req_only 行（A 线 · 不拆 API 用例）

| 功能点键（field_key） | A 线功能点摘要 | 状态 | 说明 |
|----------------------|----------------|------|------|
| L25 \| — \| etl_clean_standardize | 多维区域数据清洗一致化 | 不投影 | 无 catalog endpoint 字段 |
| L25 \| — \| mining_advantage_constraints | 优势产业与制约因素识别 | 不投影 | req_only |
| L25 \| — \| advantage_problem_fusion | 优势与问题结果融合 | 不投影 | req_only |
| L25 \| — \| expert_strategy_config | 专家策略配置驱动 | 不投影 | req_only |
| L25 \| — \| ml_opportunity_predict | 机器学习机遇预测推荐 | 不投影 | req_only |
| L25 \| — \| strategy_plan_resource_talent | 发展规划与资源人才策略 | 不投影 | req_only |
| L25 \| — \| opportunity_policy_innovation_outputs | 机遇清单与方向政策创新输出 | 不投影 | 与 panorama.nodes 契约协同，不重复拆 endpoint |
| L25 \| — \| dynamic_monitor_refresh | 动态监测与策略更新 | 不投影 | req_only |
| L25 \| — \| industry_tag_report_export | 产业标签与报告导出 | 不投影 | catalog 无 export path |

---

## 4. 计数

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 用例编号起止 | API-00384～API-00388 |
| `_empty` 未覆盖 | 1 行（见矩阵） |
| 试调 | **未试调**（§0）；父控禁止 curl |
| 产物路径 | `agent-delivery/qa/test-cases/SDWJSF-KJZTFWSFK/chain-产业链分析/CHAINSZOPPORTUNITY-深圳机遇分析/` |
| code-registry | **未回写**（父控约束） |
