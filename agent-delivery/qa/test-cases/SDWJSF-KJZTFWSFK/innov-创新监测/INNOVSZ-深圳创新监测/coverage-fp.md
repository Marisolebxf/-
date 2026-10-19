# 深圳创新监测 · A 线功能点覆盖（innov.sz-monitoring）

> **catalog_page_id**：`innov.sz-monitoring` · path `/innov/sz-monitoring`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-深圳创新监测-用例.md`（第二轮 **API-02118**～**02141**，共 24 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.sz-monitoring`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.sz-monitoring.metrics | GET | /innov/v1/innov/metrics | API-02118、API-02119、API-02120 | unavailable |
| innov.sz-monitoring.m_innov_carrier_value_rank_sz | POST | /innov/v1/innov/metric/M_INNOV_CARRIER_VALUE_RANK_SZ/compute | API-02121、API-02122、API-02123 | available |
| innov.sz-monitoring.m_innov_ds_06_carrier_003 | POST | /innov/v1/innov/metric/M_INNOV_DS_06_CARRIER_003/compute | API-02124、API-02125、API-02126 | available |
| innov.sz-monitoring.m_innov_city_compare_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_COMPARE_SZ/compute | API-02127、API-02128、API-02129 | available |
| innov.sz-monitoring.m_innov_city_compete_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_COMPETE_SZ/compute | API-02130、API-02131、API-02132 | available |
| innov.sz-monitoring.m_innov_city_index_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_INDEX_SZ/compute | API-02133、API-02134、API-02135 | available |
| innov.sz-monitoring.m_innov_city_rank_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_RANK_SZ/compute | API-02136、API-02137、API-02138 | available |
| innov.sz-monitoring.m_innov_city_trend_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_TREND_SZ/compute | API-02139、API-02140、API-02141 | available |

---

## 功能点 → 用例矩阵

本页不在六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个接口的 sampleResponse 与 responseFields 都挂在该接口主流程上；与 sample 相反的不传可选 `module` 挂备选；`module` 恰好 1 条非法反向。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） · innov.sz-monitoring.metrics · 深圳创新监测指标清单 | API-02118、API-02119、API-02120 | 无对应功能点 | API-02118 主流程 sampleRequest module=sz-monitoring，断言 data.metrics（元素 metric_id、name、algorithm_type、formula_status、pending_ref 共 7 行）与 total=7；API-02119 不传 module，结构同类；API-02120 非法 module=__invalid__。catalog status=unavailable，备注未交付 |
| （无 Lxx） · innov.sz-monitoring.m_innov_carrier_value_rank_sz · 深圳创新载体创新价值排名 | API-02121、API-02122、API-02123 | 无对应功能点 | API-02121 主流程 sampleRequest module=sz-monitoring，断言 metric_id=M_INNOV_CARRIER_VALUE_RANK_SZ、hint，以及 responseFields 声明的 metrics、total；API-02122 不传 module；API-02123 非法 module=__invalid__ |
| （无 Lxx） · innov.sz-monitoring.m_innov_ds_06_carrier_003 · 创新价值排名 | API-02124、API-02125、API-02126 | 无对应功能点 | API-02124 主流程 sampleRequest module=sz-monitoring，断言 metric_id=M_INNOV_DS_06_CARRIER_003、hint，以及 responseFields 声明的 metrics、total；API-02125 不传 module；API-02126 非法 module=__invalid__ |
| （无 Lxx） · innov.sz-monitoring.m_innov_city_compare_sz · 深圳科技发展指标对比 | API-02127、API-02128、API-02129 | 无对应功能点 | API-02127 主流程 sampleRequest module=sz-monitoring，断言 metric_id=M_INNOV_CITY_COMPARE_SZ、hint，以及 responseFields 声明的 metrics、total；API-02128 不传 module；API-02129 非法 module=__invalid__ |
| （无 Lxx） · innov.sz-monitoring.m_innov_city_compete_sz · 深圳科技竞争力 | API-02130、API-02131、API-02132 | 无对应功能点 | API-02130 主流程 sampleRequest module=sz-monitoring，断言 metric_id=M_INNOV_CITY_COMPETE_SZ、hint，以及 responseFields 声明的 metrics、total；API-02131 不传 module；API-02132 非法 module=__invalid__ |
| （无 Lxx） · innov.sz-monitoring.m_innov_city_index_sz · 深圳创新能力指数 | API-02133、API-02134、API-02135 | 无对应功能点 | API-02133 主流程 sampleRequest module=sz-monitoring，断言 metric_id=M_INNOV_CITY_INDEX_SZ、hint，以及 responseFields 声明的 metrics、total；API-02134 不传 module；API-02135 非法 module=__invalid__ |
| （无 Lxx） · innov.sz-monitoring.m_innov_city_rank_sz · 深圳城市科技发展排名 | API-02136、API-02137、API-02138 | 无对应功能点 | API-02136 主流程 sampleRequest module=sz-monitoring，断言 metric_id=M_INNOV_CITY_RANK_SZ、hint，以及 responseFields 声明的 metrics、total；API-02137 不传 module；API-02138 非法 module=__invalid__ |
| （无 Lxx） · innov.sz-monitoring.m_innov_city_trend_sz · 深圳与对标城市趋势 | API-02139、API-02140、API-02141 | 无对应功能点 | API-02139 主流程 sampleRequest module=sz-monitoring，断言 metric_id=M_INNOV_CITY_TREND_SZ、hint，以及 responseFields 声明的 metrics、total；API-02140 不传 module；API-02141 非法 module=__invalid__ |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 8 |
| title 数 | 8 |
| API 用例数 | 24 |
| 主流程 | 8（API-02118、API-02121、API-02124、API-02127、API-02130、API-02133、API-02136、API-02139） |
| 备选-参数组合 | 8（API-02119、API-02122、API-02125、API-02128、API-02131、API-02134、API-02137、API-02140） |
| 反向 | 8（API-02120、API-02123、API-02126、API-02129、API-02132、API-02135、API-02138、API-02141） |
| 编号 | API-02118～02141 连续用满 |
| A 线 Lxx | 无 |
