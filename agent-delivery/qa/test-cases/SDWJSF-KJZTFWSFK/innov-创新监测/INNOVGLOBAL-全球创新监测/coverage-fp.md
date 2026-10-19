# 全球创新监测 · A 线功能点覆盖（innov.global-monitoring）

> **catalog_page_id**：`innov.global-monitoring` · path `/innov/global-monitoring`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-全球创新监测-用例.md`（第二轮 **API-02064**～**02117**，共 54 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.global-monitoring`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.global-monitoring.metrics | GET | /innov/v1/innov/metrics | API-02064、API-02065、API-02066 | unavailable |
| innov.global-monitoring.m_innov_achieve_value | POST | /innov/v1/innov/metric/M_INNOV_ACHIEVE_VALUE/compute | API-02067、API-02068、API-02069 | available |
| innov.global-monitoring.m_innov_carrier_index_global | POST | /innov/v1/innov/metric/M_INNOV_CARRIER_INDEX_GLOBAL/compute | API-02070、API-02071、API-02072 | available |
| innov.global-monitoring.m_innov_impact_forecast | POST | /innov/v1/innov/metric/M_INNOV_IMPACT_FORECAST/compute | API-02073、API-02074、API-02075 | available |
| innov.global-monitoring.m_innov_impact_score | POST | /innov/v1/innov/metric/M_INNOV_IMPACT_SCORE/compute | API-02076、API-02077、API-02078 | available |
| innov.global-monitoring.m_innov_point_discovery | POST | /innov/v1/innov/metric/M_INNOV_POINT_DISCOVERY/compute | API-02079、API-02080、API-02081 | available |
| innov.global-monitoring.m_innov_point_value | POST | /innov/v1/innov/metric/M_INNOV_POINT_VALUE/compute | API-02082、API-02083、API-02084 | available |
| innov.global-monitoring.m_innov_ds_04_achieve_overview_001 | POST | /innov/v1/innov/metric/M_INNOV_DS_04_ACHIEVE_OVERVIEW_001/compute | API-02085、API-02086、API-02087 | available |
| innov.global-monitoring.m_innov_ds_04_carrier_rank_001 | POST | /innov/v1/innov/metric/M_INNOV_DS_04_CARRIER_RANK_001/compute | API-02088、API-02089、API-02090 | available |
| innov.global-monitoring.m_innov_ds_04_monitor_001 | POST | /innov/v1/innov/metric/M_INNOV_DS_04_MONITOR_001/compute | API-02091、API-02092、API-02093 | available |
| innov.global-monitoring.m_innov_ds_04_monitor_002 | POST | /innov/v1/innov/metric/M_INNOV_DS_04_MONITOR_002/compute | API-02094、API-02095、API-02096 | available |
| innov.global-monitoring.m_innov_ds_04_realtime_004 | POST | /innov/v1/innov/metric/M_INNOV_DS_04_REALTIME_004/compute | API-02097、API-02098、API-02099 | available |
| innov.global-monitoring.m_innov_ds_04_realtime_005 | POST | /innov/v1/innov/metric/M_INNOV_DS_04_REALTIME_005/compute | API-02100、API-02101、API-02102 | available |
| innov.global-monitoring.m_innov_carrier_rank_global | POST | /innov/v1/innov/metric/M_INNOV_CARRIER_RANK_GLOBAL/compute | API-02103、API-02104、API-02105 | available |
| innov.global-monitoring.m_innov_city_benchmark_global | POST | /innov/v1/innov/metric/M_INNOV_CITY_BENCHMARK_GLOBAL/compute | API-02106、API-02107、API-02108 | available |
| innov.global-monitoring.m_innov_city_factor_global | POST | /innov/v1/innov/metric/M_INNOV_CITY_FACTOR_GLOBAL/compute | API-02109、API-02110、API-02111 | available |
| innov.global-monitoring.m_innov_city_rank_global | POST | /innov/v1/innov/metric/M_INNOV_CITY_RANK_GLOBAL/compute | API-02112、API-02113、API-02114 | available |
| innov.global-monitoring.m_innov_ds_04_carrier_rank_002 | POST | /innov/v1/innov/metric/M_INNOV_DS_04_CARRIER_RANK_002/compute | API-02115、API-02116、API-02117 | available |

---

## 功能点 → 用例矩阵

本页不在六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。同名 title 按 endpoint 分列，不合并。每个接口的 sampleResponse 与 responseFields 都挂在该接口主流程上；与 sample 相反的不传可选 `module` 挂备选；`module` 恰好 1 条非法反向。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） · innov.global-monitoring.metrics · 全球创新监测指标清单 | API-02064、API-02065、API-02066 | 无对应功能点 | API-02064 主流程 sampleRequest module=global-monitoring，断言 data.metrics（元素 metric_id、name、algorithm_type、formula_status、pending_ref 共 17 行）与 total=17；API-02065 不传 module，结构同类；API-02066 非法 module=__invalid__。catalog status=unavailable，备注未交付。path 与其它创新监测页共用，本页以 module=global-monitoring 区分 |
| （无 Lxx） · innov.global-monitoring.m_innov_achieve_value · 创新价值 | API-02067、API-02068、API-02069 | 无对应功能点 | API-02067 主流程 sampleRequest module=global-monitoring，断言 metric_id=M_INNOV_ACHIEVE_VALUE、hint，以及 responseFields 声明的 metrics、total；API-02068 不传 module；API-02069 非法 module=__invalid__ |
| （无 Lxx） · innov.global-monitoring.m_innov_carrier_index_global · 创新载体创新能力指数 | API-02070、API-02071、API-02072 | 无对应功能点 | API-02070 主流程 sampleRequest module=global-monitoring，断言 metric_id=M_INNOV_CARRIER_INDEX_GLOBAL、hint，以及 responseFields 声明的 metrics、total；API-02071 不传 module；API-02072 非法 module=__invalid__ |
| （无 Lxx） · innov.global-monitoring.m_innov_impact_forecast · 创新影响预测 | API-02073、API-02074、API-02075 | 无对应功能点 | API-02073 主流程 sampleRequest module=global-monitoring，断言 metric_id=M_INNOV_IMPACT_FORECAST、hint，以及 responseFields 声明的 metrics、total；API-02074 不传 module；API-02075 非法 module=__invalid__ |
| （无 Lxx） · innov.global-monitoring.m_innov_impact_score · 创新影响分数 | API-02076、API-02077、API-02078 | 无对应功能点 | API-02076 主流程 sampleRequest module=global-monitoring，断言 metric_id=M_INNOV_IMPACT_SCORE、hint，以及 responseFields 声明的 metrics、total；API-02077 不传 module；API-02078 非法 module=__invalid__ |
| （无 Lxx） · innov.global-monitoring.m_innov_point_discovery · 创新点发现 | API-02079、API-02080、API-02081 | 无对应功能点 | API-02079 主流程 sampleRequest module=global-monitoring，断言 metric_id=M_INNOV_POINT_DISCOVERY、hint，以及 responseFields 声明的 metrics、total；API-02080 不传 module；API-02081 非法 module=__invalid__ |
| （无 Lxx） · innov.global-monitoring.m_innov_point_value · 创新点价值评估 | API-02082、API-02083、API-02084 | 无对应功能点 | API-02082 主流程 sampleRequest module=global-monitoring，断言 metric_id=M_INNOV_POINT_VALUE、hint，以及 responseFields 声明的 metrics、total；API-02083 不传 module；API-02084 非法 module=__invalid__ |
| （无 Lxx） · innov.global-monitoring.m_innov_ds_04_achieve_overview_001 · 创新价值 | API-02085、API-02086、API-02087 | 无对应功能点 | API-02085 主流程 sampleRequest module=global-monitoring，断言 metric_id=M_INNOV_DS_04_ACHIEVE_OVERVIEW_001、hint，以及 responseFields 声明的 metrics、total；API-02086 不传 module；API-02087 非法 module=__invalid__ |
| （无 Lxx） · innov.global-monitoring.m_innov_ds_04_carrier_rank_001 · 创新能力指数 | API-02088、API-02089、API-02090 | 无对应功能点 | API-02088 主流程 sampleRequest module=global-monitoring，断言 metric_id=M_INNOV_DS_04_CARRIER_RANK_001、hint，以及 responseFields 声明的 metrics、total；API-02089 不传 module；API-02090 非法 module=__invalid__ |
| （无 Lxx） · innov.global-monitoring.m_innov_ds_04_monitor_001 · 创新点发现 | API-02091、API-02092、API-02093 | 无对应功能点 | API-02091 主流程 sampleRequest module=global-monitoring，断言 metric_id=M_INNOV_DS_04_MONITOR_001、hint，以及 responseFields 声明的 metrics、total；API-02092 不传 module；API-02093 非法 module=__invalid__ |
| （无 Lxx） · innov.global-monitoring.m_innov_ds_04_monitor_002 · 创新价值评估 | API-02094、API-02095、API-02096 | 无对应功能点 | API-02094 主流程 sampleRequest module=global-monitoring，断言 metric_id=M_INNOV_DS_04_MONITOR_002、hint，以及 responseFields 声明的 metrics、total；API-02095 不传 module；API-02096 非法 module=__invalid__ |
| （无 Lxx） · innov.global-monitoring.m_innov_ds_04_realtime_004 · 创新影响分数 | API-02097、API-02098、API-02099 | 无对应功能点 | API-02097 主流程 sampleRequest module=global-monitoring，断言 metric_id=M_INNOV_DS_04_REALTIME_004、hint，以及 responseFields 声明的 metrics、total；API-02098 不传 module；API-02099 非法 module=__invalid__ |
| （无 Lxx） · innov.global-monitoring.m_innov_ds_04_realtime_005 · 创新影响预测 | API-02100、API-02101、API-02102 | 无对应功能点 | API-02100 主流程 sampleRequest module=global-monitoring，断言 metric_id=M_INNOV_DS_04_REALTIME_005、hint，以及 responseFields 声明的 metrics、total；API-02101 不传 module；API-02102 非法 module=__invalid__ |
| （无 Lxx） · innov.global-monitoring.m_innov_carrier_rank_global · 创新载体多维度排名 | API-02103、API-02104、API-02105 | 无对应功能点 | API-02103 主流程 sampleRequest module=global-monitoring，断言 metric_id=M_INNOV_CARRIER_RANK_GLOBAL、hint，以及 responseFields 声明的 metrics、total；API-02104 不传 module；API-02105 非法 module=__invalid__ |
| （无 Lxx） · innov.global-monitoring.m_innov_city_benchmark_global · 城市对标分析 | API-02106、API-02107、API-02108 | 无对应功能点 | API-02106 主流程 sampleRequest module=global-monitoring，断言 metric_id=M_INNOV_CITY_BENCHMARK_GLOBAL、hint，以及 responseFields 声明的 metrics、total；API-02107 不传 module；API-02108 非法 module=__invalid__ |
| （无 Lxx） · innov.global-monitoring.m_innov_city_factor_global · 城市创新能力要素表现 | API-02109、API-02110、API-02111 | 无对应功能点 | API-02109 主流程 sampleRequest module=global-monitoring，断言 metric_id=M_INNOV_CITY_FACTOR_GLOBAL、hint，以及 responseFields 声明的 metrics、total；API-02110 不传 module；API-02111 非法 module=__invalid__ |
| （无 Lxx） · innov.global-monitoring.m_innov_city_rank_global · 城市创新能力排名 | API-02112、API-02113、API-02114 | 无对应功能点 | API-02112 主流程 sampleRequest module=global-monitoring，断言 metric_id=M_INNOV_CITY_RANK_GLOBAL、hint，以及 responseFields 声明的 metrics、total；API-02113 不传 module；API-02114 非法 module=__invalid__ |
| （无 Lxx） · innov.global-monitoring.m_innov_ds_04_carrier_rank_002 · 多维度排名展示 | API-02115、API-02116、API-02117 | 无对应功能点 | API-02115 主流程 sampleRequest module=global-monitoring，断言 metric_id=M_INNOV_DS_04_CARRIER_RANK_002、hint，以及 responseFields 声明的 metrics、total；API-02116 不传 module；API-02117 非法 module=__invalid__ |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 18 |
| title 数 | 18（同名不合并） |
| API 用例数 | 54 |
| 主流程 | 18（API-02064、API-02067、API-02070、API-02073、API-02076、API-02079、API-02082、API-02085、API-02088、API-02091、API-02094、API-02097、API-02100、API-02103、API-02106、API-02109、API-02112、API-02115） |
| 备选-参数组合 | 18（API-02065、API-02068、API-02071、API-02074、API-02077、API-02080、API-02083、API-02086、API-02089、API-02092、API-02095、API-02098、API-02101、API-02104、API-02107、API-02110、API-02113、API-02116） |
| 反向 | 18（API-02066、API-02069、API-02072、API-02075、API-02078、API-02081、API-02084、API-02087、API-02090、API-02093、API-02096、API-02099、API-02102、API-02105、API-02108、API-02111、API-02114、API-02117） |
| 编号 | API-02064～02117 连续用满 |
| A 线 Lxx | 无 |
| 同名 title 主流程 | 创新价值 API-02067 / API-02085；创新影响预测 API-02073 / API-02100；创新影响分数 API-02076 / API-02097；创新点发现 API-02079 / API-02091 |
