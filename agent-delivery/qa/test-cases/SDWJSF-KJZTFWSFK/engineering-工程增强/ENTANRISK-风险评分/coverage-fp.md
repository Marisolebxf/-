# 风险评分 · 功能点覆盖（entan.risk）

> catalog `entan.risk` · path `/entan/risk`  
> A 线：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `entan.risk`（工程增强，非 60 六级）。不改 `work/`。  
> B 线用例：`API-风险评分-用例.md`（第二轮 **API-01134**～**01138**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| entan.risk.list | GET | /entan/v1/risk | API-01134～01138 | unavailable |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。`level`、`limit` 与 `rows` 及 sampleResponse 行内字段都挂在同一接口的 5 条用例上。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| entan.risk.list \| 风险评分 | API-01134～01138 | 无对应功能点 | 工程增强页。01134 主流程全参；01135 省略 level；01136 省略 limit；01137 非法 level；01138 非法 limit。备注注明文档未交付 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 1 |
| title 数 | 1（风险评分） |
| API 用例数 | 5 |
| 主流程 | 1（API-01134） |
| 备选-参数组合 | 2（API-01135、01136） |
| 反向 | 2（API-01137、01138） |
| 编号 | API-01134～01138 |
| A 线 Lxx | 无 |
