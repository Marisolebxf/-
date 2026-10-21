# 条件保障力 · A 线功能点覆盖（policy.guard）

> **catalog_page_id**：`policy.guard` · path `#/policy/guard`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.guard`（原因：不扩六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **B 线用例**：`FUNC-条件保障力-用例.md`（第三轮 **FUNC-00732**～**FUNC-00738**）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.guard`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.guard.main | GET | /policy/v1/policy/analysis/guard | FUNC-00732～00736 | unavailable |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。title「保障力」的 sampleResponse（`model_id`、`count`、`rows` 及行内 `scope_name`、`effect_score`、`metric_id`）与 responseFields 的 `rows` 都挂在主流程上；与 sample 相反的传/不传挂备选；每个参数恰好 1 条非法反向。catalog `status=unavailable`，备注注明未交付。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| policy.guard.main \| 保障力 | FUNC-00732、00733、00734、00735、00736 | 无对应功能点 | 00732 主流程 sampleRequest（limit=20、不传 scope_code），断言 model_id、count、rows 及行内 scope_name、effect_score、metric_id；00733 传入 scope_code=440000；00734 省略 limit；00735、00736 分别非法 scope_code、limit。文档标记未交付 |
| （页面清单） \| policy.guard \| 接口信息 / 算法测试 | FUNC-00737、00738 | 已覆盖 | 单接口页清单 2 条 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 1 |
| title 数 | 1 |
| FUNC 用例数 | 7 |
| 主流程 | 1 |
| 备选-参数组合 | 2 |
| 反向 | 2 |
| 清单 | 2 |
| 编号 | FUNC-00732～00738 |
| A 线 Lxx | 无 |
| 旧 API 册 | API-01508～01512 作废，见 FUNC 册 §4 |
