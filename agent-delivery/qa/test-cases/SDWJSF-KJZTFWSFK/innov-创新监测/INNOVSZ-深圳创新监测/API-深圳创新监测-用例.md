# 智能服务集群-科技专题服务算法库测试用例（深圳创新监测 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：创新监测 / 深圳创新监测  
> **catalog**：`entry_id=innov.sz-monitoring` · `catalog_page_id=innov.sz-monitoring` · path `/innov/sz-monitoring`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.sz-monitoring`  
> **A 线对照**：无对应 Lxx。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（创新监测不在本轮 60 六级）。不改 `work/`  
> **环境**：联调台 50897（本册不试调）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批22）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | path | 参数 | 条数 |
|---|------------------------|-------------|--------|------|------|------|
| 1 | 深圳创新监测指标清单 | innov.sz-monitoring.metrics | GET | /innov/v1/innov/metrics | module? | 3 |
| 2 | 深圳创新载体创新价值排名 | innov.sz-monitoring.m_innov_carrier_value_rank_sz | POST | /innov/v1/innov/metric/M_INNOV_CARRIER_VALUE_RANK_SZ/compute | module? | 3 |
| 3 | 创新价值排名 | innov.sz-monitoring.m_innov_ds_06_carrier_003 | POST | /innov/v1/innov/metric/M_INNOV_DS_06_CARRIER_003/compute | module? | 3 |
| 4 | 深圳科技发展指标对比 | innov.sz-monitoring.m_innov_city_compare_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_COMPARE_SZ/compute | module? | 3 |
| 5 | 深圳科技竞争力 | innov.sz-monitoring.m_innov_city_compete_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_COMPETE_SZ/compute | module? | 3 |
| 6 | 深圳创新能力指数 | innov.sz-monitoring.m_innov_city_index_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_INDEX_SZ/compute | module? | 3 |
| 7 | 深圳城市科技发展排名 | innov.sz-monitoring.m_innov_city_rank_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_RANK_SZ/compute | module? | 3 |
| 8 | 深圳与对标城市趋势 | innov.sz-monitoring.m_innov_city_trend_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_TREND_SZ/compute | module? | 3 |

8 个 title 按 catalog `endpoints` 顺序各 3 条，合计 **24** 条。每个接口只有可选 `module`：1 条主流程（跟 `sampleRequest`，`module=sz-monitoring`）+ 1 条与 sample 相反的不传 `module` + 1 条非法 `module=__invalid__`。GET 的 `module` 为查询参数；POST 的 `module` 为请求体。

第 1 个 `GET /innov/v1/innov/metrics` 为 catalog `status=unavailable`，三条备注注明文档标记未交付，主流程仍按 sampleResponse 写返回字段。其余 7 个 POST compute 为 `available`。本页 title 互不重复，每条步骤仍写 `endpoint_id`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02118`～`02141`（闭区间用满，不复用 00001～00888）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.sz-monitoring`、组合 id。步骤含 `endpoint_id`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02118 | 创新监测 | 深圳创新监测 | 主流程 | — | 深圳创新监测 | 深圳创新监测指标清单 | 深圳创新监测指标清单按文档 sampleRequest 传 module=sz-monitoring | 1、module 使用文档示例 sz-monitoring | 1.GET /innov/v1/innov/metrics，endpoint_id=innov.sz-monitoring.metrics，查询参数取组合 MET-01 | 1、返回 body 的 data 含 metrics（array，responseFields 指标元数据清单）、total（number，responseFields 指标数，sampleResponse 示例 7）；2、metrics 元素含 metric_id（string）、name（string）、algorithm_type（string）、formula_status（string）、pending_ref（string）；3、sampleResponse 七行：metric_id=M_INNOV_CARRIER_VALUE_RANK_SZ、name=深圳创新载体创新价值排名、algorithm_type=MODEL、formula_status=mock、pending_ref=GAP-ALGO-TYPE-UNSIGNED；metric_id=M_INNOV_DS_06_CARRIER_003、name=创新价值排名、algorithm_type=MODEL、formula_status=mock、pending_ref=GAP-ALGO-TYPE-UNSIGNED；metric_id=M_INNOV_CITY_COMPARE_SZ、name=深圳科技发展指标对比、algorithm_type=MIXED、formula_status=mock、pending_ref=Q-MO-DS06-01；metric_id=M_INNOV_CITY_COMPETE_SZ、name=深圳科技竞争力、algorithm_type=MIXED、formula_status=mock、pending_ref=Q-MO-DS06-03；metric_id=M_INNOV_CITY_INDEX_SZ、name=深圳创新能力指数、algorithm_type=MIXED、formula_status=mock、pending_ref=GAP-ALGO-TYPE-UNSIGNED；metric_id=M_INNOV_CITY_RANK_SZ、name=深圳城市科技发展排名、algorithm_type=MIXED、formula_status=mock、pending_ref=GAP-ALGO-TYPE-UNSIGNED；metric_id=M_INNOV_CITY_TREND_SZ、name=深圳与对标城市趋势、algorithm_type=MIXED、formula_status=mock、pending_ref=GAP-ALGO-TYPE-UNSIGNED | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metrics |  | INTEG |  |  | endpoint_id=innov.sz-monitoring.metrics catalog_page_id=innov.sz-monitoring 组合=MET-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02119 | 创新监测 | 深圳创新监测 | 备选-参数组合 | 省略 module | 深圳创新监测 | 深圳创新监测指标清单 | 深圳创新监测指标清单不传可选 module（与 sampleRequest 相反） | 1、不传 module | 1.GET /innov/v1/innov/metrics，endpoint_id=innov.sz-monitoring.metrics，查询参数取组合 MET-02 | 1、返回 body 的 data 仍含 metrics（array）、total（number）；2、metrics 元素仍含 metric_id（string）、name（string）、algorithm_type（string）、formula_status（string）、pending_ref（string）；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metrics |  | INTEG |  |  | endpoint_id=innov.sz-monitoring.metrics catalog_page_id=innov.sz-monitoring 组合=MET-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02120 | 创新监测 | 深圳创新监测 | 异常-入参-非法module | — | 深圳创新监测 | 深圳创新监测指标清单 | 深圳创新监测指标清单 module 非法 | 1、module 取不可识别 slug | 1.GET /innov/v1/innov/metrics，endpoint_id=innov.sz-monitoring.metrics，查询参数取组合 MET-03 | 1、返回 body 的 message 或 msg 指出 module 非法；2、不返回含 metrics、total 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metrics |  | INTEG |  |  | endpoint_id=innov.sz-monitoring.metrics catalog_page_id=innov.sz-monitoring 组合=MET-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02121 | 创新监测 | 深圳创新监测 | 主流程 | — | 深圳创新监测 | 深圳创新载体创新价值排名 | 深圳创新载体创新价值排名按文档 sampleRequest 传 module=sz-monitoring | 1、module 使用文档示例 sz-monitoring | 1.POST /innov/v1/innov/metric/M_INNOV_CARRIER_VALUE_RANK_SZ/compute，endpoint_id=innov.sz-monitoring.m_innov_carrier_value_rank_sz，请求体取组合 CVR-01 | 1、返回 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_CARRIER_VALUE_RANK_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CARRIER_VALUE_RANK_SZ/compute | M_INNOV_CARRIER_VALUE_RANK_SZ | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_carrier_value_rank_sz catalog_page_id=innov.sz-monitoring 组合=CVR-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02122 | 创新监测 | 深圳创新监测 | 备选-参数组合 | 省略 module | 深圳创新监测 | 深圳创新载体创新价值排名 | 深圳创新载体创新价值排名不传可选 module（与 sampleRequest 相反） | 1、不传 module | 1.POST /innov/v1/innov/metric/M_INNOV_CARRIER_VALUE_RANK_SZ/compute，endpoint_id=innov.sz-monitoring.m_innov_carrier_value_rank_sz，请求体取组合 CVR-02 | 1、返回 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_CARRIER_VALUE_RANK_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CARRIER_VALUE_RANK_SZ/compute | M_INNOV_CARRIER_VALUE_RANK_SZ | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_carrier_value_rank_sz catalog_page_id=innov.sz-monitoring 组合=CVR-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02123 | 创新监测 | 深圳创新监测 | 异常-入参-非法module | — | 深圳创新监测 | 深圳创新载体创新价值排名 | 深圳创新载体创新价值排名 module 非法 | 1、module 取不可识别 slug | 1.POST /innov/v1/innov/metric/M_INNOV_CARRIER_VALUE_RANK_SZ/compute，endpoint_id=innov.sz-monitoring.m_innov_carrier_value_rank_sz，请求体取组合 CVR-03 | 1、返回 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id、hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CARRIER_VALUE_RANK_SZ/compute |  | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_carrier_value_rank_sz catalog_page_id=innov.sz-monitoring 组合=CVR-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02124 | 创新监测 | 深圳创新监测 | 主流程 | — | 深圳创新监测 | 创新价值排名 | 创新价值排名按文档 sampleRequest 传 module=sz-monitoring | 1、module 使用文档示例 sz-monitoring | 1.POST /innov/v1/innov/metric/M_INNOV_DS_06_CARRIER_003/compute，endpoint_id=innov.sz-monitoring.m_innov_ds_06_carrier_003，请求体取组合 C03-01 | 1、返回 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_DS_06_CARRIER_003）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_06_CARRIER_003/compute | M_INNOV_DS_06_CARRIER_003 | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_ds_06_carrier_003 catalog_page_id=innov.sz-monitoring 组合=C03-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02125 | 创新监测 | 深圳创新监测 | 备选-参数组合 | 省略 module | 深圳创新监测 | 创新价值排名 | 创新价值排名不传可选 module（与 sampleRequest 相反） | 1、不传 module | 1.POST /innov/v1/innov/metric/M_INNOV_DS_06_CARRIER_003/compute，endpoint_id=innov.sz-monitoring.m_innov_ds_06_carrier_003，请求体取组合 C03-02 | 1、返回 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_DS_06_CARRIER_003）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_06_CARRIER_003/compute | M_INNOV_DS_06_CARRIER_003 | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_ds_06_carrier_003 catalog_page_id=innov.sz-monitoring 组合=C03-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02126 | 创新监测 | 深圳创新监测 | 异常-入参-非法module | — | 深圳创新监测 | 创新价值排名 | 创新价值排名 module 非法 | 1、module 取不可识别 slug | 1.POST /innov/v1/innov/metric/M_INNOV_DS_06_CARRIER_003/compute，endpoint_id=innov.sz-monitoring.m_innov_ds_06_carrier_003，请求体取组合 C03-03 | 1、返回 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id、hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_06_CARRIER_003/compute |  | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_ds_06_carrier_003 catalog_page_id=innov.sz-monitoring 组合=C03-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02127 | 创新监测 | 深圳创新监测 | 主流程 | — | 深圳创新监测 | 深圳科技发展指标对比 | 深圳科技发展指标对比按文档 sampleRequest 传 module=sz-monitoring | 1、module 使用文档示例 sz-monitoring | 1.POST /innov/v1/innov/metric/M_INNOV_CITY_COMPARE_SZ/compute，endpoint_id=innov.sz-monitoring.m_innov_city_compare_sz，请求体取组合 CMP-01 | 1、返回 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_CITY_COMPARE_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_COMPARE_SZ/compute | M_INNOV_CITY_COMPARE_SZ | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_city_compare_sz catalog_page_id=innov.sz-monitoring 组合=CMP-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02128 | 创新监测 | 深圳创新监测 | 备选-参数组合 | 省略 module | 深圳创新监测 | 深圳科技发展指标对比 | 深圳科技发展指标对比不传可选 module（与 sampleRequest 相反） | 1、不传 module | 1.POST /innov/v1/innov/metric/M_INNOV_CITY_COMPARE_SZ/compute，endpoint_id=innov.sz-monitoring.m_innov_city_compare_sz，请求体取组合 CMP-02 | 1、返回 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_CITY_COMPARE_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_COMPARE_SZ/compute | M_INNOV_CITY_COMPARE_SZ | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_city_compare_sz catalog_page_id=innov.sz-monitoring 组合=CMP-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02129 | 创新监测 | 深圳创新监测 | 异常-入参-非法module | — | 深圳创新监测 | 深圳科技发展指标对比 | 深圳科技发展指标对比 module 非法 | 1、module 取不可识别 slug | 1.POST /innov/v1/innov/metric/M_INNOV_CITY_COMPARE_SZ/compute，endpoint_id=innov.sz-monitoring.m_innov_city_compare_sz，请求体取组合 CMP-03 | 1、返回 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id、hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_COMPARE_SZ/compute |  | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_city_compare_sz catalog_page_id=innov.sz-monitoring 组合=CMP-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02130 | 创新监测 | 深圳创新监测 | 主流程 | — | 深圳创新监测 | 深圳科技竞争力 | 深圳科技竞争力按文档 sampleRequest 传 module=sz-monitoring | 1、module 使用文档示例 sz-monitoring | 1.POST /innov/v1/innov/metric/M_INNOV_CITY_COMPETE_SZ/compute，endpoint_id=innov.sz-monitoring.m_innov_city_compete_sz，请求体取组合 CPT-01 | 1、返回 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_CITY_COMPETE_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_COMPETE_SZ/compute | M_INNOV_CITY_COMPETE_SZ | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_city_compete_sz catalog_page_id=innov.sz-monitoring 组合=CPT-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02131 | 创新监测 | 深圳创新监测 | 备选-参数组合 | 省略 module | 深圳创新监测 | 深圳科技竞争力 | 深圳科技竞争力不传可选 module（与 sampleRequest 相反） | 1、不传 module | 1.POST /innov/v1/innov/metric/M_INNOV_CITY_COMPETE_SZ/compute，endpoint_id=innov.sz-monitoring.m_innov_city_compete_sz，请求体取组合 CPT-02 | 1、返回 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_CITY_COMPETE_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_COMPETE_SZ/compute | M_INNOV_CITY_COMPETE_SZ | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_city_compete_sz catalog_page_id=innov.sz-monitoring 组合=CPT-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02132 | 创新监测 | 深圳创新监测 | 异常-入参-非法module | — | 深圳创新监测 | 深圳科技竞争力 | 深圳科技竞争力 module 非法 | 1、module 取不可识别 slug | 1.POST /innov/v1/innov/metric/M_INNOV_CITY_COMPETE_SZ/compute，endpoint_id=innov.sz-monitoring.m_innov_city_compete_sz，请求体取组合 CPT-03 | 1、返回 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id、hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_COMPETE_SZ/compute |  | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_city_compete_sz catalog_page_id=innov.sz-monitoring 组合=CPT-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02133 | 创新监测 | 深圳创新监测 | 主流程 | — | 深圳创新监测 | 深圳创新能力指数 | 深圳创新能力指数按文档 sampleRequest 传 module=sz-monitoring | 1、module 使用文档示例 sz-monitoring | 1.POST /innov/v1/innov/metric/M_INNOV_CITY_INDEX_SZ/compute，endpoint_id=innov.sz-monitoring.m_innov_city_index_sz，请求体取组合 IDX-01 | 1、返回 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_CITY_INDEX_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_INDEX_SZ/compute | M_INNOV_CITY_INDEX_SZ | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_city_index_sz catalog_page_id=innov.sz-monitoring 组合=IDX-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02134 | 创新监测 | 深圳创新监测 | 备选-参数组合 | 省略 module | 深圳创新监测 | 深圳创新能力指数 | 深圳创新能力指数不传可选 module（与 sampleRequest 相反） | 1、不传 module | 1.POST /innov/v1/innov/metric/M_INNOV_CITY_INDEX_SZ/compute，endpoint_id=innov.sz-monitoring.m_innov_city_index_sz，请求体取组合 IDX-02 | 1、返回 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_CITY_INDEX_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_INDEX_SZ/compute | M_INNOV_CITY_INDEX_SZ | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_city_index_sz catalog_page_id=innov.sz-monitoring 组合=IDX-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02135 | 创新监测 | 深圳创新监测 | 异常-入参-非法module | — | 深圳创新监测 | 深圳创新能力指数 | 深圳创新能力指数 module 非法 | 1、module 取不可识别 slug | 1.POST /innov/v1/innov/metric/M_INNOV_CITY_INDEX_SZ/compute，endpoint_id=innov.sz-monitoring.m_innov_city_index_sz，请求体取组合 IDX-03 | 1、返回 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id、hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_INDEX_SZ/compute |  | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_city_index_sz catalog_page_id=innov.sz-monitoring 组合=IDX-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02136 | 创新监测 | 深圳创新监测 | 主流程 | — | 深圳创新监测 | 深圳城市科技发展排名 | 深圳城市科技发展排名按文档 sampleRequest 传 module=sz-monitoring | 1、module 使用文档示例 sz-monitoring | 1.POST /innov/v1/innov/metric/M_INNOV_CITY_RANK_SZ/compute，endpoint_id=innov.sz-monitoring.m_innov_city_rank_sz，请求体取组合 RNK-01 | 1、返回 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_CITY_RANK_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_RANK_SZ/compute | M_INNOV_CITY_RANK_SZ | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_city_rank_sz catalog_page_id=innov.sz-monitoring 组合=RNK-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02137 | 创新监测 | 深圳创新监测 | 备选-参数组合 | 省略 module | 深圳创新监测 | 深圳城市科技发展排名 | 深圳城市科技发展排名不传可选 module（与 sampleRequest 相反） | 1、不传 module | 1.POST /innov/v1/innov/metric/M_INNOV_CITY_RANK_SZ/compute，endpoint_id=innov.sz-monitoring.m_innov_city_rank_sz，请求体取组合 RNK-02 | 1、返回 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_CITY_RANK_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_RANK_SZ/compute | M_INNOV_CITY_RANK_SZ | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_city_rank_sz catalog_page_id=innov.sz-monitoring 组合=RNK-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02138 | 创新监测 | 深圳创新监测 | 异常-入参-非法module | — | 深圳创新监测 | 深圳城市科技发展排名 | 深圳城市科技发展排名 module 非法 | 1、module 取不可识别 slug | 1.POST /innov/v1/innov/metric/M_INNOV_CITY_RANK_SZ/compute，endpoint_id=innov.sz-monitoring.m_innov_city_rank_sz，请求体取组合 RNK-03 | 1、返回 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id、hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_RANK_SZ/compute |  | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_city_rank_sz catalog_page_id=innov.sz-monitoring 组合=RNK-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02139 | 创新监测 | 深圳创新监测 | 主流程 | — | 深圳创新监测 | 深圳与对标城市趋势 | 深圳与对标城市趋势按文档 sampleRequest 传 module=sz-monitoring | 1、module 使用文档示例 sz-monitoring | 1.POST /innov/v1/innov/metric/M_INNOV_CITY_TREND_SZ/compute，endpoint_id=innov.sz-monitoring.m_innov_city_trend_sz，请求体取组合 TRD-01 | 1、返回 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_CITY_TREND_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_TREND_SZ/compute | M_INNOV_CITY_TREND_SZ | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_city_trend_sz catalog_page_id=innov.sz-monitoring 组合=TRD-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02140 | 创新监测 | 深圳创新监测 | 备选-参数组合 | 省略 module | 深圳创新监测 | 深圳与对标城市趋势 | 深圳与对标城市趋势不传可选 module（与 sampleRequest 相反） | 1、不传 module | 1.POST /innov/v1/innov/metric/M_INNOV_CITY_TREND_SZ/compute，endpoint_id=innov.sz-monitoring.m_innov_city_trend_sz，请求体取组合 TRD-02 | 1、返回 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_CITY_TREND_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_TREND_SZ/compute | M_INNOV_CITY_TREND_SZ | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_city_trend_sz catalog_page_id=innov.sz-monitoring 组合=TRD-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02141 | 创新监测 | 深圳创新监测 | 异常-入参-非法module | — | 深圳创新监测 | 深圳与对标城市趋势 | 深圳与对标城市趋势 module 非法 | 1、module 取不可识别 slug | 1.POST /innov/v1/innov/metric/M_INNOV_CITY_TREND_SZ/compute，endpoint_id=innov.sz-monitoring.m_innov_city_trend_sz，请求体取组合 TRD-03 | 1、返回 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id、hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_TREND_SZ/compute |  | INTEG |  |  | endpoint_id=innov.sz-monitoring.m_innov_city_trend_sz catalog_page_id=innov.sz-monitoring 组合=TRD-03 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| MET-01 | innov.sz-monitoring.metrics | module=sz-monitoring（sampleRequest） | 主路径（sampleRequest 传 module） |
| MET-02 | innov.sz-monitoring.metrics | 不传 module | 与 sampleRequest 相反：省略可选 module |
| MET-03 | innov.sz-monitoring.metrics | module=__invalid__ | 只破坏 module 这一个参数 |
| CVR-01 | innov.sz-monitoring.m_innov_carrier_value_rank_sz | module=sz-monitoring（sampleRequest） | 主路径（sampleRequest 传 module） |
| CVR-02 | innov.sz-monitoring.m_innov_carrier_value_rank_sz | 不传 module | 与 sampleRequest 相反：省略可选 module |
| CVR-03 | innov.sz-monitoring.m_innov_carrier_value_rank_sz | module=__invalid__ | 只破坏 module 这一个参数 |
| C03-01 | innov.sz-monitoring.m_innov_ds_06_carrier_003 | module=sz-monitoring（sampleRequest） | 主路径（sampleRequest 传 module） |
| C03-02 | innov.sz-monitoring.m_innov_ds_06_carrier_003 | 不传 module | 与 sampleRequest 相反：省略可选 module |
| C03-03 | innov.sz-monitoring.m_innov_ds_06_carrier_003 | module=__invalid__ | 只破坏 module 这一个参数 |
| CMP-01 | innov.sz-monitoring.m_innov_city_compare_sz | module=sz-monitoring（sampleRequest） | 主路径（sampleRequest 传 module） |
| CMP-02 | innov.sz-monitoring.m_innov_city_compare_sz | 不传 module | 与 sampleRequest 相反：省略可选 module |
| CMP-03 | innov.sz-monitoring.m_innov_city_compare_sz | module=__invalid__ | 只破坏 module 这一个参数 |
| CPT-01 | innov.sz-monitoring.m_innov_city_compete_sz | module=sz-monitoring（sampleRequest） | 主路径（sampleRequest 传 module） |
| CPT-02 | innov.sz-monitoring.m_innov_city_compete_sz | 不传 module | 与 sampleRequest 相反：省略可选 module |
| CPT-03 | innov.sz-monitoring.m_innov_city_compete_sz | module=__invalid__ | 只破坏 module 这一个参数 |
| IDX-01 | innov.sz-monitoring.m_innov_city_index_sz | module=sz-monitoring（sampleRequest） | 主路径（sampleRequest 传 module） |
| IDX-02 | innov.sz-monitoring.m_innov_city_index_sz | 不传 module | 与 sampleRequest 相反：省略可选 module |
| IDX-03 | innov.sz-monitoring.m_innov_city_index_sz | module=__invalid__ | 只破坏 module 这一个参数 |
| RNK-01 | innov.sz-monitoring.m_innov_city_rank_sz | module=sz-monitoring（sampleRequest） | 主路径（sampleRequest 传 module） |
| RNK-02 | innov.sz-monitoring.m_innov_city_rank_sz | 不传 module | 与 sampleRequest 相反：省略可选 module |
| RNK-03 | innov.sz-monitoring.m_innov_city_rank_sz | module=__invalid__ | 只破坏 module 这一个参数 |
| TRD-01 | innov.sz-monitoring.m_innov_city_trend_sz | module=sz-monitoring（sampleRequest） | 主路径（sampleRequest 传 module） |
| TRD-02 | innov.sz-monitoring.m_innov_city_trend_sz | 不传 module | 与 sampleRequest 相反：省略可选 module |
| TRD-03 | innov.sz-monitoring.m_innov_city_trend_sz | module=__invalid__ | 只破坏 module 这一个参数 |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 深圳创新监测指标清单 | innov.sz-monitoring.metrics | GET | /innov/v1/innov/metrics | module? | unavailable |
| 深圳创新载体创新价值排名 | innov.sz-monitoring.m_innov_carrier_value_rank_sz | POST | /innov/v1/innov/metric/M_INNOV_CARRIER_VALUE_RANK_SZ/compute | module? | available |
| 创新价值排名 | innov.sz-monitoring.m_innov_ds_06_carrier_003 | POST | /innov/v1/innov/metric/M_INNOV_DS_06_CARRIER_003/compute | module? | available |
| 深圳科技发展指标对比 | innov.sz-monitoring.m_innov_city_compare_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_COMPARE_SZ/compute | module? | available |
| 深圳科技竞争力 | innov.sz-monitoring.m_innov_city_compete_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_COMPETE_SZ/compute | module? | available |
| 深圳创新能力指数 | innov.sz-monitoring.m_innov_city_index_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_INDEX_SZ/compute | module? | available |
| 深圳城市科技发展排名 | innov.sz-monitoring.m_innov_city_rank_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_RANK_SZ/compute | module? | available |
| 深圳与对标城市趋势 | innov.sz-monitoring.m_innov_city_trend_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_TREND_SZ/compute | module? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.sz-monitoring.metrics | API-02118、API-02119、API-02120 |
| innov.sz-monitoring.m_innov_carrier_value_rank_sz | API-02121、API-02122、API-02123 |
| innov.sz-monitoring.m_innov_ds_06_carrier_003 | API-02124、API-02125、API-02126 |
| innov.sz-monitoring.m_innov_city_compare_sz | API-02127、API-02128、API-02129 |
| innov.sz-monitoring.m_innov_city_compete_sz | API-02130、API-02131、API-02132 |
| innov.sz-monitoring.m_innov_city_index_sz | API-02133、API-02134、API-02135 |
| innov.sz-monitoring.m_innov_city_rank_sz | API-02136、API-02137、API-02138 |
| innov.sz-monitoring.m_innov_city_trend_sz | API-02139、API-02140、API-02141 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 8 个 title 均在功能点列出现且各有 1 条主流程（功能项=主流程）
- [x] 每个接口恰好 3 条：sampleRequest 主流程 + 与 sample 相反的不传 module + 非法 module
- [x] 每条步骤含 endpoint_id
- [x] unavailable（深圳创新监测指标清单）仍按 sampleResponse 写主流程，备注注明未交付
- [x] 正向预期逐字段写 sampleResponse；反向预期为 message 或 msg 指出 module 非法
- [x] 反向预期写 message 或 msg，不写状态码
- [x] `coverage-fp.md` 已同步 API-02118～02141；A 线无对应 Lxx，未改 work

**统计**：用例 **24** 条；编号闭区间 **API-02118**～**API-02141**（父控 R2-批22 分配）。主流程 **8**（02118、02121、02124、02127、02130、02133、02136、02139）；备选 **8**（02119、02122、02125、02128、02131、02134、02137、02140）；反向 **8**（02120、02123、02126、02129、02132、02135、02138、02141）。
