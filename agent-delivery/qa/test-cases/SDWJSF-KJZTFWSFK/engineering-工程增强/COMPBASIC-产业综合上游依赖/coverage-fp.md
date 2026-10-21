# 产业综合上游依赖 · 功能点覆盖（comp.basic）

> catalog `comp.basic` · path `/industry-comp/basic`  
> A 线：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `comp.basic`（上游依赖页，非 60 六级）。不改 `work/`。  
> B 线用例：`FUNC-产业综合上游依赖-用例.md`（第三轮 **FUNC-00964**～**00968**；旧 API-01728～01730、旧 FUNC-00649～00653 作废）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| comp.basic.upstream | GET | /comp/v1/comp/upstream-deps | FUNC-00964～00966 | unavailable |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。title「上游依赖与综合研判」的 sampleResponse（`kpis`、`upstream` 七维、`bar_items`、`pie_items`）与 responseFields 的 `upstream`、`kpis` 都挂在同一接口的 3 条调用用例上；另 2 条为页面清单（接口信息、算法测试）。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| comp.basic.upstream \| 上游依赖与综合研判 | FUNC-00964～00966 | 无对应功能点 | 工程增强页。00964 主流程 sampleRequest（region=440300），断言 kpis、upstream 七维及 bar_items、pie_items；00965 不传 region；00966 非法 region。备注注明文档未交付 |
| （页面清单） \| comp.basic \| 接口信息 / 算法测试 | FUNC-00967、00968 | 无对应功能点 | 单接口页清单 2 条，不点击调用 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 1 |
| title 数 | 1（上游依赖与综合研判） |
| FUNC 用例数 | 5 |
| 主流程 | 1（FUNC-00964） |
| 备选-参数组合 | 1（FUNC-00965） |
| 反向 | 1（FUNC-00966） |
| 清单 | 2（FUNC-00967、00968） |
| 编号 | FUNC-00964～00968 |
| A 线 Lxx | 无 |
