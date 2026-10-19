# 匹配推送 · A 线功能点覆盖（policy.match）

> **catalog_page_id**：`policy.match` · path `/policy/match`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.match`（原因：不扩六级）。不改 `work/`。  
> **用例册**：`API-政策匹配推送-用例.md`（第二轮 **API-01475**～**01488**，共 14 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.match`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.match.main | GET | /policy/v1/policy/match | API-01475、API-01476、API-01477、API-01478、API-01479、API-01480、API-01481 | unavailable |
| policy.match.m_policy_match | POST | /policy/v1/polan/metric/M_POLICY_MATCH/compute | API-01482、API-01483、API-01484、API-01485、API-01486、API-01487、API-01488 | available |

---

## 功能点 → 用例矩阵

本页不在六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse 与 responseFields 都挂在该接口主流程上；可选参数与 sample 相反的传/不传挂备选；每个参数恰好 1 条非法反向。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| policy.match.main \| 政策匹配 | API-01475、API-01476、API-01477、API-01478、API-01479、API-01480、API-01481 | 无对应功能点 | 01475 主流程 sampleRequest（subject_type=enterprise、limit=20、不传 subject_id），断言 data 元素 rank_no、subject_name、policy_title、match_score、metric_id；01476 传入 subject_id；01477 省略 subject_type；01478 省略 limit；01479～01481 分别非法 subject_id、subject_type、limit。文档标记未交付 |
| （无 Lxx） \| policy.match.m_policy_match \| 政策匹配推送 | API-01482、API-01483、API-01484、API-01485、API-01486、API-01487、API-01488 | 无对应功能点 | 01482 主流程 sampleRequest，断言 metric_id、hint 与 responseFields 的 match_score；01483 传入 subject_id；01484 省略 subject_type；01485 省略 limit；01486～01488 分别非法 subject_id、subject_type、limit |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| API 用例数 | 14 |
| 主流程 | 2 |
| 备选-参数组合 | 6 |
| 反向 | 6 |
| 编号 | API-01475～01488 连续 |
| A 线 Lxx | 无 |
