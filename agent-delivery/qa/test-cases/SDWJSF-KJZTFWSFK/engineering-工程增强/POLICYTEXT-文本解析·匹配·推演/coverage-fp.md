# 文本解析 · 匹配 · 推演 · 功能点覆盖（policy.text）

> **catalog_page_id**：`policy.text` · path `/policy/text`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.text`（原因：parse/match/simulate 合页；60 条无独立六级）。不改 `work/`。  
> **用例册**：`API-文本解析·匹配·推演-用例.md`（第二轮 **API-01446**～**01464**，共 19 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.text`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.text.parse | GET | /policy/v1/policy/text/parse | API-01446、01447、01448、01449、01450 | unavailable |
| policy.text.match | GET | /policy/v1/policy/match | API-01451、01452、01453、01454、01455、01456、01457 | unavailable |
| policy.text.simulate | GET | /policy/v1/policy/simulate | API-01458、01459、01460、01461、01462、01463、01464 | unavailable |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse（含 `elements`、`curve.step` / `curve.value`）与 responseFields 都挂在该接口主流程上；可选参数与 sample 相反的传/不传挂备选；每个参数恰好 1 条反向。三个接口 catalog `status=unavailable`，备注注明未交付。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| policy.text.parse \| 文本解析 | API-01446、01447、01448、01449、01450 | 无对应功能点 | 01446 主流程 sampleRequest（limit=20，不传 policy_id）；01447 传入 policy_id；01448 省略 limit；01449 非法 policy_id；01450 非法 limit。sampleResponse 的 policy_id、title、elements 挂主流程 |
| （无 Lxx） \| policy.text.match \| 政策匹配 | API-01451、01452、01453、01454、01455、01456、01457 | 无对应功能点 | 01451 主流程 sampleRequest（subject_type=enterprise、limit=20，不传 subject_id）；01452 传入 subject_id；01453 省略 subject_type；01454 省略 limit；01455～01457 分别非法 subject_id、subject_type、limit。sampleResponse 的 rank_no、subject_name、policy_title、match_score、reason 挂主流程 |
| （无 Lxx） \| policy.text.simulate \| 效果推演 | API-01458、01459、01460、01461、01462、01463、01464 | 无对应功能点 | 01458 主流程 sampleRequest（scope_code=440000、limit=20，不传 scenario_id）；01459 省略 scope_code；01460 传入 scenario_id；01461 省略 limit；01462～01464 分别非法 scope_code、scenario_id、limit。sampleResponse 的 scope_code、scenario_id、baseline_value、simulated_value、curve.step、curve.value 挂主流程 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 3 |
| title 数 | 3 |
| API 用例数 | 19 |
| 主流程 | 3（API-01446、01451、01458） |
| 备选-参数组合 | 8（API-01447、01448、01452、01453、01454、01459、01460、01461） |
| 反向 | 8（API-01449、01450、01455、01456、01457、01462、01463、01464） |
| 编号 | API-01446～01464 连续 |
| A 线 Lxx | 无 |
