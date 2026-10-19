# 效果推演 · 实施路径 · A 线功能点覆盖（policy.simulate）

> **catalog_page_id**：`policy.simulate` · path `/policy/simulate`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.simulate`（原因：不扩六级）。不改 `work/`。  
> **用例册**：`API-效果推演·实施路径-用例.md`（第二轮 **API-01489**～**01502**，共 14 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.simulate`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.simulate.main | GET | /policy/v1/policy/simulate | API-01489、API-01490、API-01491、API-01492、API-01493、API-01494、API-01495 | unavailable |
| policy.simulate.m_policy_simulate | POST | /policy/v1/polan/metric/M_POLICY_SIMULATE/compute | API-01496、API-01497、API-01498、API-01499、API-01500、API-01501、API-01502 | available |

---

## 功能点 → 用例矩阵

本页不在六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse 与 responseFields 都挂在该接口主流程上；可选参数与 sample 相反的传/不传挂备选；每个参数恰好 1 条非法反向。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| policy.simulate.main \| 效果推演 | API-01489、API-01490、API-01491、API-01492、API-01493、API-01494、API-01495 | 无对应功能点 | 01489 主流程 sampleRequest（limit=20、不传 scope_code、不传 scenario_id），断言 data 元素 scope_code、scenario_id、baseline_value、simulated_value、metric_id；01490 传入 scope_code；01491 传入 scenario_id；01492 省略 limit；01493～01495 分别非法 scope_code、scenario_id、limit。文档标记未交付 |
| （无 Lxx） \| policy.simulate.m_policy_simulate \| 政策效果推演 | API-01496、API-01497、API-01498、API-01499、API-01500、API-01501、API-01502 | 无对应功能点 | 01496 主流程 sampleRequest，断言 metric_id、hint 与 responseFields 的 simulated_value；01497 传入 scope_code；01498 传入 scenario_id；01499 省略 limit；01500～01502 分别非法 scope_code、scenario_id、limit |

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
| 编号 | API-01489～01502 连续 |
| A 线 Lxx | 无 |
