# 企业产业链洞察 · 功能点覆盖（entan.chain-coverage）

> catalog `entan.chain-coverage` · path `/entan/chain-coverage`  
> A 线：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `entan.chain-coverage`（reason: 不扩六级）。不改 `work/`。  
> B 线用例：`API-企业产业链洞察-用例.md`（第二轮 **API-01143**～**01148**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| entan.chain-coverage.keypano | POST | /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute | API-01143、01144 | unavailable |
| entan.chain-coverage.diversification | POST | /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute | API-01145、01146 | unavailable |
| entan.chain-coverage.coverage-depth | POST | /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute | API-01147、01148 | unavailable |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。`enterprise_codes` 与 sampleResponse 嵌套字段、responseFields 都挂在同一接口的 2 条用例上。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| entan.chain-coverage.keypano \| 重点企业全景图（企业集合） | API-01143、01144 | 无对应功能点 | 01143 主流程断言 value.coverage_rate 及 sampleResponse 嵌套字段；01144 缺 enterprise_codes。备注注明文档未交付 |
| （无 Lxx） \| entan.chain-coverage.diversification \| 多元化指数（企业集合） | API-01145、01146 | 无对应功能点 | 01145 主流程断言 value.value（responseFields 多元化指数）及嵌套字段；01146 缺 enterprise_codes。备注注明文档未交付 |
| （无 Lxx） \| entan.chain-coverage.coverage-depth \| 领域覆盖深度（企业集合） | API-01147、01148 | 无对应功能点 | 01147 主流程断言 value.value（responseFields 领域覆盖深度）及嵌套字段；01148 缺 enterprise_codes。备注注明文档未交付 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 3 |
| title 数 | 3 |
| API 用例数 | 6 |
| 主流程 | 3（API-01143、01145、01147） |
| 反向 | 3（API-01144、01146、01148） |
| 编号 | API-01143～01148 |
| A 线 Lxx | 无 |
