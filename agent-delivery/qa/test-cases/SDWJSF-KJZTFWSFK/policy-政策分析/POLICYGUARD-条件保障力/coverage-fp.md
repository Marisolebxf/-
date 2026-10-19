# 条件保障力 · A 线功能点覆盖（policy.guard）

> **catalog_page_id**：`policy.guard` · path `/policy/guard`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.guard`（原因：不扩六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-条件保障力-用例.md`（第二轮 **API-01508**～**01512**，共 5 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.guard`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.guard.main | GET | /policy/v1/policy/analysis/guard | API-01508、API-01509、API-01510、API-01511、API-01512 | unavailable |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。title「保障力」的 sampleResponse（`model_id`、`count`、`rows` 及行内 `scope_name`、`effect_score`、`metric_id`）与 responseFields 的 `rows` 都挂在主流程上；与 sample 相反的传/不传挂备选；每个参数恰好 1 条非法反向。catalog `status=unavailable`，备注注明未交付。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| policy.guard.main \| 保障力 | API-01508、API-01509、API-01510、API-01511、API-01512 | 无对应功能点 | 01508 主流程 sampleRequest（limit=20、不传 scope_code），断言 model_id、count、rows 及行内 scope_name、effect_score、metric_id；01509 传入 scope_code=440000；01510 省略 limit；01511、01512 分别非法 scope_code、limit。文档标记未交付 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 1 |
| title 数 | 1 |
| API 用例数 | 5 |
| 主流程 | 1 |
| 备选-参数组合 | 2 |
| 反向 | 2 |
| 编号 | API-01508～01512 连续 |
| A 线 Lxx | 无 |
