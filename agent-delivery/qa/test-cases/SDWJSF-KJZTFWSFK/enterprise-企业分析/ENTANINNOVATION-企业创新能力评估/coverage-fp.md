# 企业创新能力评估 · 功能点覆盖（entan.innovation）

> catalog `entan.innovation` · path `/entan/innovation`  
> A 线：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `entan.innovation`（与 L31 相邻但不扩六级）。不改 `work/`。  
> B 线用例：`API-企业创新能力评估-用例.md`（第二轮 **API-01141**～**01142**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| entan.innovation.rank | POST | /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute | API-01141、01142 | unavailable |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。`enterprise_codes` 与 sampleResponse / responseFields 字段都挂在同一接口的 2 条用例上。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| entan.innovation.rank \| 创新能力指数（企业集合） | API-01141、01142 | 无对应功能点 | 与 L31 相邻但不扩六级。01141 主流程全参；01142 缺 enterprise_codes。备注注明文档未交付 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 1 |
| title 数 | 1（创新能力指数（企业集合）） |
| API 用例数 | 2 |
| 主流程 | 1（API-01141） |
| 备选-参数组合 | 0 |
| 反向 | 1（API-01142） |
| 编号 | API-01141～01142 |
| A 线 Lxx | 无 |
