# 技术成熟度分析 · A 线功能点覆盖（chain.tech-maturity）

> **catalog_page_id**：`chain.tech-maturity` · path `/chain/tech-maturity`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `chain.tech-maturity`（原因：60 条无对应六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-技术成熟度分析-用例.md`（第二轮 **API-01308**～**01311**，共 4 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/chain.json` 页 `chain.tech-maturity`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| chain.tech-maturity.main | GET | /innov/v1/industry/{chainId}/tech-maturity | API-01308、API-01309 | unavailable |
| chain.tech-maturity.m_chain_tech_maturity_score | POST | /innov/v1/industry/chainan/metric/M_CHAIN_TECH_MATURITY_SCORE/compute | API-01310、API-01311 | available |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse（含嵌套 `trend.year` / `trend.patent_count`，以及 sampleResponse 多出的 `stage`、`hint`）与 responseFields 都挂在该接口主流程上；缺 `chainId` 挂在同接口的反向用例上。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| chain.tech-maturity.main \| 技术成熟度 | API-01308、API-01309 | 无对应功能点 | 01308 主流程 path chainId=INB170101，断言 tech_maturity_score、stage、trend 及元素 year、patent_count；01309 缺 chainId。文档标记未交付 |
| （无 Lxx） \| chain.tech-maturity.m_chain_tech_maturity_score \| 技术成熟度评分 | API-01310、API-01311 | 无对应功能点 | 01310 主流程按 sampleRequest 的 chain_id=INB1701，断言 metric_id、hint；01311 缺 chainId |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| API 用例数 | 4 |
| 主流程 | 2 |
| 备选-参数组合 | 0 |
| 反向 | 2 |
| 编号 | API-01308～01311 连续 |
| A 线 Lxx | 无 |
