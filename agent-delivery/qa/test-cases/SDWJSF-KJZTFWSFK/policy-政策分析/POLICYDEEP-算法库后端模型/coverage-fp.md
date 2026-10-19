# 算法库后端模型 · A 线功能点覆盖（policy.deep）

> **catalog_page_id**：`policy.deep` · path `/policy/deep`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.deep`（原因：不扩六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-算法库后端模型-用例.md`（第二轮 **API-01513**～**01517**，共 5 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.deep`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.deep.models | GET | /policy/v1/policy/analysis/focus | API-01513、API-01514、API-01515、API-01516、API-01517 | unavailable |

---

## 功能点 → 用例矩阵

本页不在六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。title「后端模型」的 sampleResponse（`rows` 及行内 `model`、`model_name`、`metric_id`、`index`）与 responseFields 的 `rows` 都挂在主流程上；与 sample 相反的传/不传挂备选；每个参数恰好 1 条非法反向。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| policy.deep.models \| 后端模型 | API-01513、API-01514、API-01515、API-01516、API-01517 | 无对应功能点 | 01513 主流程 sampleRequest（scope_code=440300、limit=50），断言 rows 及六行 model/model_name/metric_id/index；01514 省略 scope_code；01515 省略 limit；01516 非法 scope_code；01517 非法 limit。文档标记未交付 |

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
| 编号 | API-01513～01517 连续 |
| A 线 Lxx | 无 |
