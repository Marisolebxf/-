# 风险评分 · 功能点覆盖（entan.risk）

> catalog `entan.risk` · path `#/entan/risk`  
> A 线：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `entan.risk`（工程增强，非 60 六级）。不改 `work/`。  
> B 线用例：`FUNC-风险评分-用例.md`（第三轮 **FUNC-00309**～**FUNC-00315**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| entan.risk.list | GET | /entan/v1/risk | FUNC-00309～00313 | unavailable |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。`level`、`limit` 与 `rows` 及 sampleResponse 行内字段都挂在同一接口的 5 条接口向用例上。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| entan.risk.list \| 风险评分 | FUNC-00309～00313 | 无对应功能点 | 工程增强页。00309 主流程全参；00310 省略 level；00311 省略 limit；00312 非法 level；00313 非法 limit。备注注明文档未交付 |
| （页面清单） \| entan.risk \| 接口信息 / 算法测试 | FUNC-00314、00315 | 无对应功能点 | 单接口页清单 2 条 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 1 |
| title 数 | 1（风险评分） |
| FUNC 用例数 | 7 |
| 主流程 | 1（FUNC-00309） |
| 备选-参数组合 | 2（FUNC-00310、00311） |
| 反向 | 2（FUNC-00312、00313） |
| 清单 | 2（FUNC-00314、00315） |
| 编号 | FUNC-00309～00315 |
| A 线 Lxx | 无 |
| 旧 API 册 | API-01134～01138 作废 |
