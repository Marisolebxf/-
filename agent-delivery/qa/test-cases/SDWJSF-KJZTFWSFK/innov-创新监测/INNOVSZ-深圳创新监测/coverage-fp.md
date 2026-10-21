# 深圳创新监测 · A 线功能点覆盖（innov.sz-monitoring）

> **catalog_page_id**：`innov.sz-monitoring` · path `/innov/sz-monitoring`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`FUNC-深圳创新监测-用例.md`（第三轮 **FUNC-01400**～**01425**，共 26 条：接口 24 + 清单 2）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.sz-monitoring`  
> **联调台**：https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.sz-monitoring.metrics | GET | /innov/v1/innov/metrics | FUNC-01400、FUNC-01401、FUNC-01402 | running |
| innov.sz-monitoring.m_innov_carrier_value_rank_sz | POST | /innov/v1/innov/metric/M_INNOV_CARRIER_VALUE_RANK_SZ/compute | FUNC-01403、FUNC-01404、FUNC-01405 | available |
| innov.sz-monitoring.m_innov_ds_06_carrier_003 | POST | /innov/v1/innov/metric/M_INNOV_DS_06_CARRIER_003/compute | FUNC-01406、FUNC-01407、FUNC-01408 | available |
| innov.sz-monitoring.m_innov_city_compare_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_COMPARE_SZ/compute | FUNC-01409、FUNC-01410、FUNC-01411 | available |
| innov.sz-monitoring.m_innov_city_compete_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_COMPETE_SZ/compute | FUNC-01412、FUNC-01413、FUNC-01414 | available |
| innov.sz-monitoring.m_innov_city_index_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_INDEX_SZ/compute | FUNC-01415、FUNC-01416、FUNC-01417 | available |
| innov.sz-monitoring.m_innov_city_rank_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_RANK_SZ/compute | FUNC-01418、FUNC-01419、FUNC-01420 | available |
| innov.sz-monitoring.m_innov_city_trend_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_TREND_SZ/compute | FUNC-01421、FUNC-01422、FUNC-01423 | available |
| （页面清单） | — | — | FUNC-01424、FUNC-01425 | — |

---

## 功能点 → 用例矩阵

本页不在六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个接口的 sampleResponse 与 responseFields 都挂在该接口主流程上；与 sample 相反的不传可选 `module` 挂备选；`module` 恰好 1 条非法反向。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| innov.sz-monitoring.metrics \| 深圳创新监测指标清单 | FUNC-01400、FUNC-01401、FUNC-01402 | 无对应功能点 | 01400 主流程 sampleRequest module=sz-monitoring，断言 data.metrics（元素 metric_id、name、algorithm_type、formula_status、pending_ref 共 7 行）与 total=7；01401 不传 module，结构同类；01402 非法 module=__invalid__ |
| （无 Lxx） \| innov.sz-monitoring.m_innov_carrier_value_rank_sz \| 深圳创新载体创新价值排名 | FUNC-01403、FUNC-01404、FUNC-01405 | 无对应功能点 | 01403 主流程 sampleRequest module=sz-monitoring，断言 metric_id=M_INNOV_CARRIER_VALUE_RANK_SZ、hint，以及 responseFields 声明的 metrics、total；01404 不传 module；01405 非法 module=__invalid__ |
| （无 Lxx） \| innov.sz-monitoring.m_innov_ds_06_carrier_003 \| 创新价值排名 | FUNC-01406、FUNC-01407、FUNC-01408 | 无对应功能点 | 01406 主流程 sampleRequest module=sz-monitoring，断言 metric_id=M_INNOV_DS_06_CARRIER_003、hint，以及 responseFields 声明的 metrics、total；01407 不传 module；01408 非法 module=__invalid__ |
| （无 Lxx） \| innov.sz-monitoring.m_innov_city_compare_sz \| 深圳科技发展指标对比 | FUNC-01409、FUNC-01410、FUNC-01411 | 无对应功能点 | 01409 主流程 sampleRequest module=sz-monitoring，断言 metric_id=M_INNOV_CITY_COMPARE_SZ、hint，以及 responseFields 声明的 metrics、total；01410 不传 module；01411 非法 module=__invalid__ |
| （无 Lxx） \| innov.sz-monitoring.m_innov_city_compete_sz \| 深圳科技竞争力 | FUNC-01412、FUNC-01413、FUNC-01414 | 无对应功能点 | 01412 主流程 sampleRequest module=sz-monitoring，断言 metric_id=M_INNOV_CITY_COMPETE_SZ、hint，以及 responseFields 声明的 metrics、total；01413 不传 module；01414 非法 module=__invalid__ |
| （无 Lxx） \| innov.sz-monitoring.m_innov_city_index_sz \| 深圳创新能力指数 | FUNC-01415、FUNC-01416、FUNC-01417 | 无对应功能点 | 01415 主流程 sampleRequest module=sz-monitoring，断言 metric_id=M_INNOV_CITY_INDEX_SZ、hint，以及 responseFields 声明的 metrics、total；01416 不传 module；01417 非法 module=__invalid__ |
| （无 Lxx） \| innov.sz-monitoring.m_innov_city_rank_sz \| 深圳城市科技发展排名 | FUNC-01418、FUNC-01419、FUNC-01420 | 无对应功能点 | 01418 主流程 sampleRequest module=sz-monitoring，断言 metric_id=M_INNOV_CITY_RANK_SZ、hint，以及 responseFields 声明的 metrics、total；01419 不传 module；01420 非法 module=__invalid__ |
| （无 Lxx） \| innov.sz-monitoring.m_innov_city_trend_sz \| 深圳与对标城市趋势 | FUNC-01421、FUNC-01422、FUNC-01423 | 无对应功能点 | 01421 主流程 sampleRequest module=sz-monitoring，断言 metric_id=M_INNOV_CITY_TREND_SZ、hint，以及 responseFields 声明的 metrics、total；01422 不传 module；01423 非法 module=__invalid__ |
| （页面清单） \| 接口信息 / 算法测试 | FUNC-01424、FUNC-01425 | 无对应功能点 | §6.1 清单：8 接口下拉与 method/path 切换刷新 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 8 |
| title 数 | 8 |
| FUNC 用例数 | 26 |
| 主流程 | 8（FUNC-01400、01403、01406、01409、01412、01415、01418、01421） |
| 备选-参数组合 | 8（FUNC-01401、01404、01407、01410、01413、01416、01419、01422） |
| 反向 | 8（FUNC-01402、01405、01408、01411、01414、01417、01420、01423） |
| 清单 | 2（FUNC-01424、01425） |
| 编号 | FUNC-01400～01425 连续 |
| A 线 Lxx | 无 |
| 作废 API 号 | API-02118～02141 不复用 |
