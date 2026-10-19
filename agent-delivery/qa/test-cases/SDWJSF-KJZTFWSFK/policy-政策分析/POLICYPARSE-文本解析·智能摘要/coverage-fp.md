# 文本解析 · 智能摘要 · A 线功能点覆盖（policy.parse）

> **catalog_page_id**：`policy.parse` · path `/policy/parse`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.parse`（原因：不扩六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-文本解析·智能摘要-用例.md`（第二轮 **API-01465**～**01474**，共 10 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.parse`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.parse.main | GET | /policy/v1/policy/text/parse | API-01465、API-01466、API-01467、API-01468、API-01469 | unavailable |
| policy.parse.m_policy_text_parse | POST | /policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute | API-01470、API-01471、API-01472、API-01473、API-01474 | available |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse 与 responseFields 都挂在该接口主流程上；与 sample 相反的传/不传挂备选；每个参数恰好 1 条非法反向。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| policy.parse.main \| 文本解析 | API-01465、API-01466、API-01467、API-01468、API-01469 | 无对应功能点 | 01465 主流程 sampleRequest（不传 policy_id、limit=20），断言 policy_id、title、summary、metric_id；01466 传入 policy_id；01467 省略 limit；01468 非法 policy_id；01469 非法 limit。文档标记未交付 |
| （无 Lxx） \| policy.parse.m_policy_text_parse \| 政策文本解析 | API-01470、API-01471、API-01472、API-01473、API-01474 | 无对应功能点 | 01470 主流程 sampleRequest（不传 policy_id、limit=20），断言 metric_id、hint 及 responseFields 的 summary；01471 传入 policy_id；01472 省略 limit；01473 非法 policy_id；01474 非法 limit |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| API 用例数 | 10 |
| 主流程 | 2 |
| 备选-参数组合 | 4 |
| 反向 | 4 |
| 编号 | API-01465～01474 连续 |
| A 线 Lxx | 无 |
