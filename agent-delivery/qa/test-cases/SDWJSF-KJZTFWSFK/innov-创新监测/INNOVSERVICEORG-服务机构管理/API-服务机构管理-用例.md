# 智能服务集群-科技专题服务算法库测试用例（服务机构管理 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：创新监测 / 服务机构管理  
> **catalog**：`entry_id=innov.service-org` · `catalog_page_id=innov.service-org` · path `/innov/service-org`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.service-org`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`，原因：创新监测不在本轮 60 六级；不改 work）  
> **环境**：联调台 50897（本册不试调）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批23）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

每个接口只有可选 `module`（string，example `service-org`）。各恰好 3 条：主流程跟 `sampleRequest`（`module=service-org`）；1 条与 sample 相反的不传 `module`；1 条非法 `module=__invalid__`。本页 2 个 title 互不重复，步骤仍写 `endpoint_id`。

| # | title（功能点列原文） | endpoint_id | METHOD | path | 参数 | status | 条数 |
|---|------------------------|-------------|--------|------|------|--------|------|
| 1 | 服务机构管理指标清单 | innov.service-org.metrics | GET | /innov/v1/innov/metrics | module? | unavailable | 3 |
| 2 | 影响力评价 | innov.service-org.m_innov_ds_29_incubator_006 | POST | /innov/v1/innov/metric/M_INNOV_DS_29_INCUBATOR_006/compute | module? | available | 3 |

GET `innov.service-org.metrics` 与其它创新监测指标页共用 path `/innov/v1/innov/metrics`，本页以 `module=service-org` 与 `endpoint_id` 区分。该接口 catalog `status=unavailable`，备注注明文档标记未交付；正向预期仍按该接口 sampleResponse 逐字段写。

POST 的 `sampleResponse` 为 `metric_id`、`hint`；同接口 `responseFields` 另声明 `metrics`（array）、`total`（number）。正向预期两处都写。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02205`～`02210`（闭区间用满，不复用 00001～00888）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.service-org`、组合 id。步骤含 `endpoint_id`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02205 | 创新监测 | 服务机构管理 | 主流程 | — | 服务机构管理 | 服务机构管理指标清单 | 服务机构管理指标清单按文档 sampleRequest 传 module=service-org | 1、module 使用文档示例 service-org | 1.GET /innov/v1/innov/metrics，查询参数取组合 MET-01（endpoint_id=innov.service-org.metrics） | 1、返回 body 与 sampleResponse 同层逐字段：metrics 为数组（responseFields 指标元数据清单），共 1 条，元素含 metric_id（string，示例 M_INNOV_DS_29_INCUBATOR_006）、name（string，示例 影响力评价）、algorithm_type（string，示例 MODEL）、formula_status（string，示例 mock）、pending_ref（string，示例 GAP-ALGO-TYPE-UNSIGNED）；2、total 为 number（responseFields 指标数，示例 1） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metrics | | INTEG | | | endpoint_id=innov.service-org.metrics catalog_page_id=innov.service-org 组合=MET-01 金样 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02206 | 创新监测 | 服务机构管理 | 备选-参数组合 | 省略 module | 服务机构管理 | 服务机构管理指标清单 | 服务机构管理指标清单不传可选 module（与 sample 相反） | 1、不传 module | 1.GET /innov/v1/innov/metrics，查询参数取组合 MET-02（endpoint_id=innov.service-org.metrics） | 1、返回 body 与 sampleResponse 逐字段同类：metrics 为数组（responseFields 指标元数据清单），元素含 metric_id（string）、name（string）、algorithm_type（string）、formula_status（string）、pending_ref（string）；2、total 为 number（responseFields 指标数，示例 1）；3、字段结构与主流程及 sampleResponse 一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metrics | | INTEG | | | endpoint_id=innov.service-org.metrics catalog_page_id=innov.service-org 组合=MET-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02207 | 创新监测 | 服务机构管理 | 异常-入参-非法module | — | 服务机构管理 | 服务机构管理指标清单 | 服务机构管理指标清单传非法 module | 1、module=__invalid__ | 1.GET /innov/v1/innov/metrics，查询参数取组合 MET-03（endpoint_id=innov.service-org.metrics） | 1、返回 body 的 message 或 msg 指出 module 非法；2、不返回含 metrics 与 total 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metrics | | INTEG | | | endpoint_id=innov.service-org.metrics catalog_page_id=innov.service-org 组合=MET-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02208 | 创新监测 | 服务机构管理 | 主流程 | — | 服务机构管理 | 影响力评价 | 影响力评价按文档 sampleRequest 传 module=service-org | 1、module 使用文档示例 service-org | 1.POST /innov/v1/innov/metric/M_INNOV_DS_29_INCUBATOR_006/compute，请求体取组合 INC-01（endpoint_id=innov.service-org.m_innov_ds_29_incubator_006） | 1、返回 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_DS_29_INCUBATOR_006）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_29_INCUBATOR_006/compute | M_INNOV_DS_29_INCUBATOR_006 | INTEG | | | endpoint_id=innov.service-org.m_innov_ds_29_incubator_006 catalog_page_id=innov.service-org 组合=INC-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02209 | 创新监测 | 服务机构管理 | 备选-参数组合 | 省略 module | 服务机构管理 | 影响力评价 | 影响力评价不传可选 module（与 sample 相反） | 1、不传 module | 1.POST /innov/v1/innov/metric/M_INNOV_DS_29_INCUBATOR_006/compute，请求体取组合 INC-02（endpoint_id=innov.service-org.m_innov_ds_29_incubator_006） | 1、返回 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_DS_29_INCUBATOR_006）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_29_INCUBATOR_006/compute | M_INNOV_DS_29_INCUBATOR_006 | INTEG | | | endpoint_id=innov.service-org.m_innov_ds_29_incubator_006 catalog_page_id=innov.service-org 组合=INC-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-02210 | 创新监测 | 服务机构管理 | 异常-入参-非法module | — | 服务机构管理 | 影响力评价 | 影响力评价传非法 module | 1、module=__invalid__ | 1.POST /innov/v1/innov/metric/M_INNOV_DS_29_INCUBATOR_006/compute，请求体取组合 INC-03（endpoint_id=innov.service-org.m_innov_ds_29_incubator_006） | 1、返回 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id 为 M_INNOV_DS_29_INCUBATOR_006 且含 hint 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_29_INCUBATOR_006/compute | | INTEG | | | endpoint_id=innov.service-org.m_innov_ds_29_incubator_006 catalog_page_id=innov.service-org 组合=INC-03 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| MET-01 | innov.service-org.metrics | module=service-org | 主路径（sampleRequest） |
| MET-02 | innov.service-org.metrics | 不传 module | 与 sample 相反：省略可选 module |
| MET-03 | innov.service-org.metrics | module=__invalid__ | 只破坏 module |
| INC-01 | innov.service-org.m_innov_ds_29_incubator_006 | module=service-org | 主路径（sampleRequest） |
| INC-02 | innov.service-org.m_innov_ds_29_incubator_006 | 不传 module | 与 sample 相反：省略可选 module |
| INC-03 | innov.service-org.m_innov_ds_29_incubator_006 | module=__invalid__ | 只破坏 module |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 服务机构管理指标清单 | innov.service-org.metrics | GET | /innov/v1/innov/metrics | module? | unavailable |
| 影响力评价 | innov.service-org.m_innov_ds_29_incubator_006 | POST | /innov/v1/innov/metric/M_INNOV_DS_29_INCUBATOR_006/compute | module? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.service-org.metrics | API-02205、02206、02207 |
| innov.service-org.m_innov_ds_29_incubator_006 | API-02208、02209、02210 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title 均在功能点列出现且各有 1 条主流程（步骤含 endpoint_id）
- [x] 每个接口：sampleRequest 主流程 + 与 sample 相反的不传 module + 恰好 1 条非法 module
- [x] GET metrics 为 unavailable，仍按 sampleResponse 写主流程，备注注明未交付
- [x] 反向预期写 message 或 msg 指出参数非法，不单写状态码
- [x] `coverage-fp.md` 已同步 API-02205～02210；A 线无对应 Lxx，未改 work

**统计**：用例 **6** 条（主流程 2、备选-参数组合 2、异常-入参-非法module 2）；编号闭区间 **API-02205**～**API-02210**（父控 R2-批23 分配）。
