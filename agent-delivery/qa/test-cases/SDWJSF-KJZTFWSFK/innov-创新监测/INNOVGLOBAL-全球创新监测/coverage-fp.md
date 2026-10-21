# 全球创新监测 · A 线功能点覆盖（innov.global-monitoring）

> **catalog_page_id**：`innov.global-monitoring` · path `/innov/global-monitoring`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`FUNC-全球创新监测-用例.md`（第三轮 **FUNC-01344**～**01399**，共 56 条：接口 54 + 清单 2；旧 API-02064～02117 作废）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.global-monitoring`  
> **联调台**：https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.global-monitoring.metrics | GET | /innov/v1/innov/metrics | FUNC-01344、01345、01346 | unavailable |
| innov.global-monitoring.m_innov_achieve_value | POST | /innov/v1/innov/metric/M_INNOV_ACHIEVE_VALUE/compute | FUNC-01347～01349 | available |
| innov.global-monitoring.m_innov_carrier_index_global | POST | /innov/v1/innov/metric/M_INNOV_CARRIER_INDEX_GLOBAL/compute | FUNC-01350～01352 | available |
| innov.global-monitoring.m_innov_impact_forecast | POST | /innov/v1/innov/metric/M_INNOV_IMPACT_FORECAST/compute | FUNC-01353～01355 | available |
| innov.global-monitoring.m_innov_impact_score | POST | /innov/v1/innov/metric/M_INNOV_IMPACT_SCORE/compute | FUNC-01356～01358 | available |
| innov.global-monitoring.m_innov_point_discovery | POST | /innov/v1/innov/metric/M_INNOV_POINT_DISCOVERY/compute | FUNC-01359～01361 | available |
| innov.global-monitoring.m_innov_point_value | POST | /innov/v1/innov/metric/M_INNOV_POINT_VALUE/compute | FUNC-01362～01364 | available |
| innov.global-monitoring.m_innov_ds_04_achieve_overview_001 | POST | /innov/v1/innov/metric/M_INNOV_DS_04_ACHIEVE_OVERVIEW_001/compute | FUNC-01365～01367 | available |
| innov.global-monitoring.m_innov_ds_04_carrier_rank_001 | POST | /innov/v1/innov/metric/M_INNOV_DS_04_CARRIER_RANK_001/compute | FUNC-01368～01370 | available |
| innov.global-monitoring.m_innov_ds_04_monitor_001 | POST | /innov/v1/innov/metric/M_INNOV_DS_04_MONITOR_001/compute | FUNC-01371～01373 | available |
| innov.global-monitoring.m_innov_ds_04_monitor_002 | POST | /innov/v1/innov/metric/M_INNOV_DS_04_MONITOR_002/compute | FUNC-01374～01376 | available |
| innov.global-monitoring.m_innov_ds_04_realtime_004 | POST | /innov/v1/innov/metric/M_INNOV_DS_04_REALTIME_004/compute | FUNC-01377～01379 | available |
| innov.global-monitoring.m_innov_ds_04_realtime_005 | POST | /innov/v1/innov/metric/M_INNOV_DS_04_REALTIME_005/compute | FUNC-01380～01382 | available |
| innov.global-monitoring.m_innov_carrier_rank_global | POST | /innov/v1/innov/metric/M_INNOV_CARRIER_RANK_GLOBAL/compute | FUNC-01383～01385 | available |
| innov.global-monitoring.m_innov_city_benchmark_global | POST | /innov/v1/innov/metric/M_INNOV_CITY_BENCHMARK_GLOBAL/compute | FUNC-01386～01388 | available |
| innov.global-monitoring.m_innov_city_factor_global | POST | /innov/v1/innov/metric/M_INNOV_CITY_FACTOR_GLOBAL/compute | FUNC-01389～01391 | available |
| innov.global-monitoring.m_innov_city_rank_global | POST | /innov/v1/innov/metric/M_INNOV_CITY_RANK_GLOBAL/compute | FUNC-01392～01394 | available |
| innov.global-monitoring.m_innov_ds_04_carrier_rank_002 | POST | /innov/v1/innov/metric/M_INNOV_DS_04_CARRIER_RANK_002/compute | FUNC-01395～01397 | available |

页面清单：**FUNC-01398**（接口信息）、**FUNC-01399**（算法测试）。

---

## 功能点 → 用例矩阵

本页不在六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行。每个 title 各 3 条（主流程 module=global-monitoring、不传 module、非法 module），预期字段与旧 API 册一致，步骤改为 algovwz 联调台操作。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） · innov.global-monitoring.metrics · 全球创新监测指标清单 | FUNC-01344、01345、01346 | 无对应功能点 | 01344 主流程 MET-01（金样）；01345 不传 module；01346 非法 module；catalog unavailable |
| （无 Lxx） · innov.global-monitoring.m_innov_achieve_value · 创新价值 | FUNC-01347～01349 | 无对应功能点 | AV1-01/02/03 |
| （无 Lxx） · innov.global-monitoring.m_innov_carrier_index_global · 创新载体创新能力指数 | FUNC-01350～01352 | 无对应功能点 | CIG-01/02/03 |
| （无 Lxx） · innov.global-monitoring.m_innov_impact_forecast · 创新影响预测 | FUNC-01353～01355 | 无对应功能点 | IF1-01/02/03 |
| （无 Lxx） · innov.global-monitoring.m_innov_impact_score · 创新影响分数 | FUNC-01356～01358 | 无对应功能点 | IS1-01/02/03 |
| （无 Lxx） · innov.global-monitoring.m_innov_point_discovery · 创新点发现 | FUNC-01359～01361 | 无对应功能点 | PD1-01/02/03 |
| （无 Lxx） · innov.global-monitoring.m_innov_point_value · 创新点价值评估 | FUNC-01362～01364 | 无对应功能点 | PV1-01/02/03 |
| （无 Lxx） · innov.global-monitoring.m_innov_ds_04_achieve_overview_001 · 创新价值 | FUNC-01365～01367 | 无对应功能点 | AO1-01/02/03 |
| （无 Lxx） · innov.global-monitoring.m_innov_ds_04_carrier_rank_001 · 创新能力指数 | FUNC-01368～01370 | 无对应功能点 | CR1-01/02/03 |
| （无 Lxx） · innov.global-monitoring.m_innov_ds_04_monitor_001 · 创新点发现 | FUNC-01371～01373 | 无对应功能点 | MO1-01/02/03 |
| （无 Lxx） · innov.global-monitoring.m_innov_ds_04_monitor_002 · 创新价值评估 | FUNC-01374～01376 | 无对应功能点 | MO2-01/02/03 |
| （无 Lxx） · innov.global-monitoring.m_innov_ds_04_realtime_004 · 创新影响分数 | FUNC-01377～01379 | 无对应功能点 | RT4-01/02/03 |
| （无 Lxx） · innov.global-monitoring.m_innov_ds_04_realtime_005 · 创新影响预测 | FUNC-01380～01382 | 无对应功能点 | RT5-01/02/03 |
| （无 Lxx） · innov.global-monitoring.m_innov_carrier_rank_global · 创新载体多维度排名 | FUNC-01383～01385 | 无对应功能点 | CRG-01/02/03 |
| （无 Lxx） · innov.global-monitoring.m_innov_city_benchmark_global · 城市对标分析 | FUNC-01386～01388 | 无对应功能点 | CBG-01/02/03 |
| （无 Lxx） · innov.global-monitoring.m_innov_city_factor_global · 城市创新能力要素表现 | FUNC-01389～01391 | 无对应功能点 | CFG-01/02/03 |
| （无 Lxx） · innov.global-monitoring.m_innov_city_rank_global · 城市创新能力排名 | FUNC-01392～01394 | 无对应功能点 | CRK-01/02/03 |
| （无 Lxx） · innov.global-monitoring.m_innov_ds_04_carrier_rank_002 · 多维度排名展示 | FUNC-01395～01397 | 无对应功能点 | CR2-01/02/03 |
| （页面清单） | FUNC-01398、01399 | 无对应功能点 | 十八接口页接口信息 / 算法测试 tab 清单 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 18 |
| title 数 | 18（同名不合并） |
| FUNC 用例数 | 56 |
| 主流程 | 18 |
| 备选-参数组合 | 18 |
| 反向 | 18 |
| 清单 | 2 |
| 编号 | FUNC-01344～01399 连续 |
| A 线 Lxx | 无 |
| 金样 | FUNC-01344 |
| 同名 title 主流程 | 创新价值 01347 / 01365；创新影响预测 01353 / 01380；创新影响分数 01356 / 01377；创新点发现 01359 / 01371 |
