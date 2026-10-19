# 智能服务集群-科技专题服务算法库测试用例（科技专题战略分析 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：创新监测 / 科技专题战略分析  
> **catalog**：`entry_id=innov.topic-strategy` · `catalog_page_id=innov.topic-strategy` · path `/innov/topic-strategy`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.topic-strategy`  
> **A 线对照**：无对应 Lxx。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（创新监测不在本轮 60 六级）。不改 `work/`  
> **环境**：联调台 50897（本册不试调）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批22）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | path | 参数 | 条数 |
|---|------------------------|-------------|--------|------|------|------|
| 1 | 科技专题战略分析指标清单 | innov.topic-strategy.metrics | GET | /innov/v1/innov/metrics | module? | 3 |
| 2 | 影响力评价与应用反馈 | innov.topic-strategy.m_innov_ds_25_softsci_012 | POST | /innov/v1/innov/metric/M_INNOV_DS_25_SOFTSCI_012/compute | module? | 3 |
| 3 | 协同绩效与影响力智能评估 | innov.topic-strategy.m_innov_ds_26_eco_012 | POST | /innov/v1/innov/metric/M_INNOV_DS_26_ECO_012/compute | module? | 3 |
| 4 | 热点区域自动识别与预警 | innov.topic-strategy.m_innov_ds_27_spatio_003 | POST | /innov/v1/innov/metric/M_INNOV_DS_27_SPATIO_003/compute | module? | 3 |

4 个 title 按 catalog `endpoints` 顺序各 3 条，合计 **12** 条。每个接口只有可选 `module`：1 条主流程（跟 `sampleRequest`，`module=topic-strategy`）+ 1 条与 sample 相反的不传 `module` + 1 条非法 `module=__invalid__`。GET 的 `module` 为查询参数；POST 的 `module` 为请求体。

第 1 个 `GET /innov/v1/innov/metrics` 为 catalog `status=unavailable`，三条备注注明文档标记未交付，主流程仍按 sampleResponse 写返回字段。其余 3 个 POST compute 为 `available`。本页 title 互不重复，每条步骤仍写 `endpoint_id`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02193`～`02204`（闭区间用满，不复用 00001～00888）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.topic-strategy`、组合 id。步骤含 `endpoint_id`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02193 | 创新监测 | 科技专题战略分析 | 主流程 | — | 科技专题战略分析 | 科技专题战略分析指标清单 | 科技专题战略分析指标清单按文档 sampleRequest 传 module=topic-strategy | 1、module 使用文档示例 topic-strategy | 1.GET /innov/v1/innov/metrics，endpoint_id=innov.topic-strategy.metrics，查询参数取组合 MET-01 | 1、返回 body 的 data 含 metrics（array，responseFields 指标元数据清单）、total（number，responseFields 指标数，sampleResponse 示例 3）；2、metrics 元素含 metric_id（string）、name（string）、algorithm_type（string）、formula_status（string）、pending_ref（string）；3、sampleResponse 三行：metric_id=M_INNOV_DS_25_SOFTSCI_012、name=影响力评价与应用反馈、algorithm_type=MODEL、formula_status=mock、pending_ref=GAP-ALGO-TYPE-UNSIGNED；metric_id=M_INNOV_DS_26_ECO_012、name=协同绩效与影响力智能评估、algorithm_type=MODEL、formula_status=mock、pending_ref=GAP-ALGO-TYPE-UNSIGNED；metric_id=M_INNOV_DS_27_SPATIO_003、name=热点区域自动识别与预警、algorithm_type=MODEL、formula_status=mock、pending_ref=GAP-ALGO-TYPE-UNSIGNED | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metrics |  | INTEG |  |  | endpoint_id=innov.topic-strategy.metrics catalog_page_id=innov.topic-strategy 组合=MET-01 金样 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02194 | 创新监测 | 科技专题战略分析 | 备选-参数组合 | 省略 module | 科技专题战略分析 | 科技专题战略分析指标清单 | 科技专题战略分析指标清单不传可选 module（与 sampleRequest 相反） | 1、不传 module | 1.GET /innov/v1/innov/metrics，endpoint_id=innov.topic-strategy.metrics，查询参数取组合 MET-02 | 1、返回 body 的 data 仍含 metrics（array）、total（number）；2、metrics 元素仍含 metric_id（string）、name（string）、algorithm_type（string）、formula_status（string）、pending_ref（string）；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metrics |  | INTEG |  |  | endpoint_id=innov.topic-strategy.metrics catalog_page_id=innov.topic-strategy 组合=MET-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02195 | 创新监测 | 科技专题战略分析 | 异常-入参-非法module | — | 科技专题战略分析 | 科技专题战略分析指标清单 | 科技专题战略分析指标清单 module 非法 | 1、module 取不可识别 slug | 1.GET /innov/v1/innov/metrics，endpoint_id=innov.topic-strategy.metrics，查询参数取组合 MET-03 | 1、返回 body 的 message 或 msg 指出 module 非法；2、不返回含 metrics、total 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metrics |  | INTEG |  |  | endpoint_id=innov.topic-strategy.metrics catalog_page_id=innov.topic-strategy 组合=MET-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02196 | 创新监测 | 科技专题战略分析 | 主流程 | — | 科技专题战略分析 | 影响力评价与应用反馈 | 影响力评价与应用反馈按文档 sampleRequest 传 module=topic-strategy | 1、module 使用文档示例 topic-strategy | 1.POST /innov/v1/innov/metric/M_INNOV_DS_25_SOFTSCI_012/compute，endpoint_id=innov.topic-strategy.m_innov_ds_25_softsci_012，请求体取组合 S25-01 | 1、返回 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_DS_25_SOFTSCI_012）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_25_SOFTSCI_012/compute | M_INNOV_DS_25_SOFTSCI_012 | INTEG |  |  | endpoint_id=innov.topic-strategy.m_innov_ds_25_softsci_012 catalog_page_id=innov.topic-strategy 组合=S25-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02197 | 创新监测 | 科技专题战略分析 | 备选-参数组合 | 省略 module | 科技专题战略分析 | 影响力评价与应用反馈 | 影响力评价与应用反馈不传可选 module（与 sampleRequest 相反） | 1、不传 module | 1.POST /innov/v1/innov/metric/M_INNOV_DS_25_SOFTSCI_012/compute，endpoint_id=innov.topic-strategy.m_innov_ds_25_softsci_012，请求体取组合 S25-02 | 1、返回 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_DS_25_SOFTSCI_012）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_25_SOFTSCI_012/compute | M_INNOV_DS_25_SOFTSCI_012 | INTEG |  |  | endpoint_id=innov.topic-strategy.m_innov_ds_25_softsci_012 catalog_page_id=innov.topic-strategy 组合=S25-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02198 | 创新监测 | 科技专题战略分析 | 异常-入参-非法module | — | 科技专题战略分析 | 影响力评价与应用反馈 | 影响力评价与应用反馈 module 非法 | 1、module 取不可识别 slug | 1.POST /innov/v1/innov/metric/M_INNOV_DS_25_SOFTSCI_012/compute，endpoint_id=innov.topic-strategy.m_innov_ds_25_softsci_012，请求体取组合 S25-03 | 1、返回 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id、hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_25_SOFTSCI_012/compute |  | INTEG |  |  | endpoint_id=innov.topic-strategy.m_innov_ds_25_softsci_012 catalog_page_id=innov.topic-strategy 组合=S25-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02199 | 创新监测 | 科技专题战略分析 | 主流程 | — | 科技专题战略分析 | 协同绩效与影响力智能评估 | 协同绩效与影响力智能评估按文档 sampleRequest 传 module=topic-strategy | 1、module 使用文档示例 topic-strategy | 1.POST /innov/v1/innov/metric/M_INNOV_DS_26_ECO_012/compute，endpoint_id=innov.topic-strategy.m_innov_ds_26_eco_012，请求体取组合 E26-01 | 1、返回 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_DS_26_ECO_012）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_26_ECO_012/compute | M_INNOV_DS_26_ECO_012 | INTEG |  |  | endpoint_id=innov.topic-strategy.m_innov_ds_26_eco_012 catalog_page_id=innov.topic-strategy 组合=E26-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02200 | 创新监测 | 科技专题战略分析 | 备选-参数组合 | 省略 module | 科技专题战略分析 | 协同绩效与影响力智能评估 | 协同绩效与影响力智能评估不传可选 module（与 sampleRequest 相反） | 1、不传 module | 1.POST /innov/v1/innov/metric/M_INNOV_DS_26_ECO_012/compute，endpoint_id=innov.topic-strategy.m_innov_ds_26_eco_012，请求体取组合 E26-02 | 1、返回 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_DS_26_ECO_012）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_26_ECO_012/compute | M_INNOV_DS_26_ECO_012 | INTEG |  |  | endpoint_id=innov.topic-strategy.m_innov_ds_26_eco_012 catalog_page_id=innov.topic-strategy 组合=E26-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02201 | 创新监测 | 科技专题战略分析 | 异常-入参-非法module | — | 科技专题战略分析 | 协同绩效与影响力智能评估 | 协同绩效与影响力智能评估 module 非法 | 1、module 取不可识别 slug | 1.POST /innov/v1/innov/metric/M_INNOV_DS_26_ECO_012/compute，endpoint_id=innov.topic-strategy.m_innov_ds_26_eco_012，请求体取组合 E26-03 | 1、返回 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id、hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_26_ECO_012/compute |  | INTEG |  |  | endpoint_id=innov.topic-strategy.m_innov_ds_26_eco_012 catalog_page_id=innov.topic-strategy 组合=E26-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02202 | 创新监测 | 科技专题战略分析 | 主流程 | — | 科技专题战略分析 | 热点区域自动识别与预警 | 热点区域自动识别与预警按文档 sampleRequest 传 module=topic-strategy | 1、module 使用文档示例 topic-strategy | 1.POST /innov/v1/innov/metric/M_INNOV_DS_27_SPATIO_003/compute，endpoint_id=innov.topic-strategy.m_innov_ds_27_spatio_003，请求体取组合 P27-01 | 1、返回 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_DS_27_SPATIO_003）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_27_SPATIO_003/compute | M_INNOV_DS_27_SPATIO_003 | INTEG |  |  | endpoint_id=innov.topic-strategy.m_innov_ds_27_spatio_003 catalog_page_id=innov.topic-strategy 组合=P27-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02203 | 创新监测 | 科技专题战略分析 | 备选-参数组合 | 省略 module | 科技专题战略分析 | 热点区域自动识别与预警 | 热点区域自动识别与预警不传可选 module（与 sampleRequest 相反） | 1、不传 module | 1.POST /innov/v1/innov/metric/M_INNOV_DS_27_SPATIO_003/compute，endpoint_id=innov.topic-strategy.m_innov_ds_27_spatio_003，请求体取组合 P27-02 | 1、返回 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_DS_27_SPATIO_003）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_27_SPATIO_003/compute | M_INNOV_DS_27_SPATIO_003 | INTEG |  |  | endpoint_id=innov.topic-strategy.m_innov_ds_27_spatio_003 catalog_page_id=innov.topic-strategy 组合=P27-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02204 | 创新监测 | 科技专题战略分析 | 异常-入参-非法module | — | 科技专题战略分析 | 热点区域自动识别与预警 | 热点区域自动识别与预警 module 非法 | 1、module 取不可识别 slug | 1.POST /innov/v1/innov/metric/M_INNOV_DS_27_SPATIO_003/compute，endpoint_id=innov.topic-strategy.m_innov_ds_27_spatio_003，请求体取组合 P27-03 | 1、返回 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id、hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_27_SPATIO_003/compute |  | INTEG |  |  | endpoint_id=innov.topic-strategy.m_innov_ds_27_spatio_003 catalog_page_id=innov.topic-strategy 组合=P27-03 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| MET-01 | innov.topic-strategy.metrics | module=topic-strategy（sampleRequest） | 主路径（sampleRequest 传 module） |
| MET-02 | innov.topic-strategy.metrics | 不传 module | 与 sampleRequest 相反：省略可选 module |
| MET-03 | innov.topic-strategy.metrics | module=__invalid__ | 只破坏 module 这一个参数 |
| S25-01 | innov.topic-strategy.m_innov_ds_25_softsci_012 | module=topic-strategy（sampleRequest） | 主路径（sampleRequest 传 module） |
| S25-02 | innov.topic-strategy.m_innov_ds_25_softsci_012 | 不传 module | 与 sampleRequest 相反：省略可选 module |
| S25-03 | innov.topic-strategy.m_innov_ds_25_softsci_012 | module=__invalid__ | 只破坏 module 这一个参数 |
| E26-01 | innov.topic-strategy.m_innov_ds_26_eco_012 | module=topic-strategy（sampleRequest） | 主路径（sampleRequest 传 module） |
| E26-02 | innov.topic-strategy.m_innov_ds_26_eco_012 | 不传 module | 与 sampleRequest 相反：省略可选 module |
| E26-03 | innov.topic-strategy.m_innov_ds_26_eco_012 | module=__invalid__ | 只破坏 module 这一个参数 |
| P27-01 | innov.topic-strategy.m_innov_ds_27_spatio_003 | module=topic-strategy（sampleRequest） | 主路径（sampleRequest 传 module） |
| P27-02 | innov.topic-strategy.m_innov_ds_27_spatio_003 | 不传 module | 与 sampleRequest 相反：省略可选 module |
| P27-03 | innov.topic-strategy.m_innov_ds_27_spatio_003 | module=__invalid__ | 只破坏 module 这一个参数 |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 科技专题战略分析指标清单 | innov.topic-strategy.metrics | GET | /innov/v1/innov/metrics | module? | unavailable |
| 影响力评价与应用反馈 | innov.topic-strategy.m_innov_ds_25_softsci_012 | POST | /innov/v1/innov/metric/M_INNOV_DS_25_SOFTSCI_012/compute | module? | available |
| 协同绩效与影响力智能评估 | innov.topic-strategy.m_innov_ds_26_eco_012 | POST | /innov/v1/innov/metric/M_INNOV_DS_26_ECO_012/compute | module? | available |
| 热点区域自动识别与预警 | innov.topic-strategy.m_innov_ds_27_spatio_003 | POST | /innov/v1/innov/metric/M_INNOV_DS_27_SPATIO_003/compute | module? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.topic-strategy.metrics | API-02193、API-02194、API-02195 |
| innov.topic-strategy.m_innov_ds_25_softsci_012 | API-02196、API-02197、API-02198 |
| innov.topic-strategy.m_innov_ds_26_eco_012 | API-02199、API-02200、API-02201 |
| innov.topic-strategy.m_innov_ds_27_spatio_003 | API-02202、API-02203、API-02204 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 4 个 title 均在功能点列出现且各有 1 条主流程（功能项=主流程）
- [x] 每个接口恰好 3 条：sampleRequest 主流程 + 与 sample 相反的不传 module + 非法 module
- [x] 每条步骤含 endpoint_id
- [x] unavailable（科技专题战略分析指标清单）仍按 sampleResponse 写主流程，备注注明未交付
- [x] 正向预期逐字段写 sampleResponse；反向预期为 message 或 msg 指出 module 非法
- [x] 反向预期写 message 或 msg，不写状态码
- [x] `coverage-fp.md` 已同步 API-02193～02204；A 线无对应 Lxx，未改 work

**统计**：用例 **12** 条；编号闭区间 **API-02193**～**API-02204**（父控 R2-批22 分配）。主流程 **4**（02193、02196、02199、02202）；备选 **4**；反向 **4**。
