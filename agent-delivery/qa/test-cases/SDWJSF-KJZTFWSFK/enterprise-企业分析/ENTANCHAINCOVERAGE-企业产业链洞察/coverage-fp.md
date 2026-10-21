# 企业产业链洞察 · 功能点覆盖（entan.chain-coverage）

> catalog `entan.chain-coverage` · path `/entan/chain-coverage`  
> A 线：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `entan.chain-coverage`（reason: 不扩六级）。不改 `work/`。  
> B 线用例：`FUNC-企业产业链洞察-用例.md`（第三轮 **FUNC-00324**～**00331**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| entan.chain-coverage.keypano | POST | /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute | FUNC-00324、00325 | unavailable |
| entan.chain-coverage.diversification | POST | /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute | FUNC-00326、00327 | unavailable |
| entan.chain-coverage.coverage-depth | POST | /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute | FUNC-00328、00329 | unavailable |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。`enterprise_codes` 与 sampleResponse 嵌套字段、responseFields 都挂在同一接口的 2 条用例上；另 2 条页面清单用例覆盖接口信息 / 算法测试 tab。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| entan.chain-coverage.keypano \| 重点企业全景图（企业集合） | FUNC-00324、00325 | 无对应功能点 | 00324 主流程断言 value.coverage_rate 及 sampleResponse 嵌套字段；00325 缺 enterprise_codes。备注注明文档未交付 |
| （无 Lxx） \| entan.chain-coverage.diversification \| 多元化指数（企业集合） | FUNC-00326、00327 | 无对应功能点 | 00326 主流程断言 value.value（responseFields 多元化指数）及嵌套字段；00327 缺 enterprise_codes。备注注明文档未交付 |
| （无 Lxx） \| entan.chain-coverage.coverage-depth \| 领域覆盖深度（企业集合） | FUNC-00328、00329 | 无对应功能点 | 00328 主流程断言 value.value（responseFields 领域覆盖深度）及嵌套字段；00329 缺 enterprise_codes。备注注明文档未交付 |
| （页面清单） \| 接口信息 / 算法测试 | FUNC-00330、00331 | 无对应功能点 | 下拉 3 项与 catalog title 一致；切换后概览/调用区刷新 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 3 |
| title 数 | 3 |
| FUNC 用例数 | 8 |
| 主流程 | 3（FUNC-00324、00326、00328） |
| 备选-参数组合 | 0 |
| 反向 | 3（FUNC-00325、00327、00329） |
| 清单 | 2（FUNC-00330、00331） |
| 编号 | FUNC-00324～00331 |
| A 线 Lxx | 无 |
