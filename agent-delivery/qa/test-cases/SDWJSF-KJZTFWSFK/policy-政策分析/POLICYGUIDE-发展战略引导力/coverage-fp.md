# 发展战略引导力 · A 线功能点覆盖（policy.guide）

> **catalog_page_id**：`policy.guide` · path `#/policy/guide`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.guide`（原因：不扩六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **B 线用例**：`FUNC-发展战略引导力-用例.md`（第三轮 **FUNC-00725**～**FUNC-00731**）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.guide`  
> **联调台**：https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.guide.main | GET | /policy/v1/policy/analysis/guide | FUNC-00725～00729 | unavailable |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。title「引导力」的 sampleResponse（`model_id`、`count`、`rows` 及行内 `scope_name`、`effect_score`、`layout_rec_cnt`、`metric_id`）与 responseFields（仅 `rows`）都挂在该接口主流程上；与 sample 相反的传/不传挂备选；每个参数恰好 1 条非法反向。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| policy.guide.main \| 引导力 | FUNC-00725、00726、00727、00728、00729 | 无对应功能点 | 00725 主流程 sampleRequest（不传 scope_code、limit=20），断言 model_id、count、rows 及行内 scope_name、effect_score、layout_rec_cnt、metric_id；00726 补传 scope_code=440000；00727 省略 limit；00728 非法 scope_code；00729 非法 limit。文档标记未交付 |
| （页面清单） \| policy.guide \| 接口信息 / 算法测试 | FUNC-00730、00731 | 已覆盖 | 单接口页清单 2 条 |

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
| 编号 | FUNC-00725～00731 |
| A 线 Lxx | 无 |
| 旧 API 册 | API-01503～01507 作废，见 FUNC 册 §4 |
