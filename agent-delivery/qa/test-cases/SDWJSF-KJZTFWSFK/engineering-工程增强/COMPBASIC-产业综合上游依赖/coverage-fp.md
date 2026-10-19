# 产业综合上游依赖 · A 线功能点覆盖（comp.basic）

> **catalog_page_id**：`comp.basic` · path `/industry-comp/basic`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `comp.basic`（原因：上游依赖页，非 60 六级模型）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-产业综合上游依赖-用例.md`（第二轮 **API-01728**～**01730**，共 3 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.basic`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| comp.basic.upstream | GET | /comp/v1/comp/upstream-deps | API-01728、API-01729、API-01730 | unavailable |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。title「上游依赖与综合研判」的 sampleResponse（`kpis.vitality` / `element` / `synergy`，`upstream` 行内 `dimension`、`name`、`bidSection`、`menuLabel`、`ready`、`ready_label`，以及 sampleResponse 多出的 `bar_items`、`pie_items`）与 responseFields 的 `upstream`、`kpis` 都挂在主流程上；与 sample 相反的不传 `region` 挂备选；`region` 恰好 1 条非法反向。catalog `status=unavailable`，备注注明未交付。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| comp.basic.upstream \| 上游依赖与综合研判 | API-01728、API-01729、API-01730 | 无对应功能点 | 01728 主流程 sampleRequest（region=440300），断言 kpis、upstream 七维及 bar_items、pie_items；01729 不传 region；01730 非法 region。文档标记未交付 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 1 |
| title 数 | 1 |
| API 用例数 | 3 |
| 主流程 | 1 |
| 备选-参数组合 | 1 |
| 反向 | 1 |
| 编号 | API-01728～01730 连续 |
| A 线 Lxx | 无 |
