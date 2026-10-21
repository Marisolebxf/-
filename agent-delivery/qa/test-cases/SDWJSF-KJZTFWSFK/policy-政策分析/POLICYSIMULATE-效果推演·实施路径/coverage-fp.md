# 效果推演 · 实施路径 · A 线功能点覆盖（policy.simulate）

> **catalog_page_id**：`policy.simulate` · path `#/policy/simulate`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.simulate`（原因：不扩六级）。不改 `work/`。  
> **B 线用例**：`FUNC-效果推演·实施路径-用例.md`（第三轮 **FUNC-00709**～**FUNC-00724**）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.simulate`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.simulate.main | GET | /policy/v1/policy/simulate | FUNC-00709～00715 | unavailable |
| policy.simulate.m_policy_simulate | POST | /policy/v1/polan/metric/M_POLICY_SIMULATE/compute | FUNC-00716～00722 | available |

---

## 功能点 → 用例矩阵

本页不在六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse 与 responseFields 都挂在该接口主流程上；可选参数与 sample 相反的传/不传挂备选；每个参数恰好 1 条非法反向。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| policy.simulate.main \| 效果推演 | FUNC-00709、00710、00711、00712、00713、00714、00715 | 无对应功能点 | 00709 主流程 sampleRequest（limit=20、不传 scope_code、不传 scenario_id），断言 data 元素 scope_code、scenario_id、baseline_value、simulated_value、metric_id；00710 传入 scope_code；00711 传入 scenario_id；00712 省略 limit；00713～00715 分别非法 scope_code、scenario_id、limit。文档标记未交付 |
| （无 Lxx） \| policy.simulate.m_policy_simulate \| 政策效果推演 | FUNC-00716、00717、00718、00719、00720、00721、00722 | 无对应功能点 | 00716 主流程 sampleRequest，断言 metric_id、hint 与 responseFields 的 simulated_value；00717 传入 scope_code；00718 传入 scenario_id；00719 省略 limit；00720～00722 分别非法 scope_code、scenario_id、limit |
| （页面清单） \| policy.simulate \| 接口信息 / 算法测试 | FUNC-00723、00724 | 已覆盖 | 双接口页清单 2 条 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| FUNC 用例数 | 16 |
| 主流程 | 2 |
| 备选-参数组合 | 6 |
| 反向 | 6 |
| 清单 | 2 |
| 编号 | FUNC-00709～00724 |
| A 线 Lxx | 无 |
| 旧 API 册 | API-01489～01502 作废，见 FUNC 册 §4 |
