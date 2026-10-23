# 智能服务集群-科技专题服务算法库测试用例（服务机构管理 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=innov.service-org` · `catalog_page_id=innov.service-org` · path `/innov/service-org`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/innov.json` · 页 `innov.service-org`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3 返工；金样主流程 MET-01）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | path | 参数 | 条数 |
|---|------------------------|-------------|--------|------|------|------|
| 1 | 服务机构管理指标清单 | innov.service-org.metrics | GET | /innov/v1/innov/metrics | module? | 3 |
| 2 | 影响力评价 | innov.service-org.m_innov_ds_29_incubator_006 | POST | /innov/v1/innov/metric/M_INNOV_DS_29_INCUBATOR_006/compute | module? | 3 |

2 个 title 各 3 条，合计 **6** 条接口调用 + §6.1 清单 **2** 条 = **8** 条。每个接口只有可选 `module`：1 条主流程（跟 `sampleRequest`，`module=service-org`）+ 1 条与 sample 相反的不传 `module` + 1 条非法 `module=__invalid__`。GET 的 `module` 为查询参数；POST 的 `module` 为请求体。

`服务机构管理指标清单` 为 catalog `status=running`。`影响力评价` 为 `status=available`。GET metrics 与其它创新监测指标页共用 path `/innov/v1/innov/metrics`，本页以 `module=service-org` 与 `endpoint_id` 区分。POST 的 `sampleResponse` 为 `metric_id`、`hint`；同接口 `responseFields` 另声明 `metrics`（array）、`total`（number），正向预期两处都写。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01493`～`01500`（闭区间 **8** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.service-org`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01493 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 服务机构管理 | 服务机构管理指标清单 | 验证服务机构管理指标清单功能，检查填写 module=service-org 传 module=service-org 后返回 metrics 清单与 total 及元素字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=service-org | 1.侧栏进入「创新监测算法库」→「服务机构管理」；2.切换至「算法测试」tab；3.接口下拉选择「服务机构管理指标清单」；4.填写 module=service-org，点击调用 | 1、返回面板 body 的 data 与 sampleResponse 同层逐字段：metrics 为数组（responseFields 指标元数据清单），共 1 条，元素含 metric_id（string，示例 M_INNOV_DS_29_INCUBATOR_006）、name（string，示例 影响力评价）、algorithm_type（string，示例 MODEL）、formula_status（string，示例 mock）、pending_ref（string，示例 GAP-ALGO-TYPE-UNSIGNED）；2、total 为 number（responseFields 指标数，示例 1） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metrics |  | INTEG |  | FUNC-01493 | endpoint_id=innov.service-org.metrics catalog_page_id=innov.service-org 组合=MET-01 场景=主流程 金样 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01494 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 服务机构管理 | 服务机构管理指标清单 | 验证服务机构管理指标清单功能，检查不传可选 module 不传 module 后仍返回与 sampleResponse 同类结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 module | 1.侧栏进入「创新监测算法库」→「服务机构管理」；2.切换至「算法测试」tab；3.接口下拉选择「服务机构管理指标清单」；4.不传 module，点击调用 | 1、返回面板 body 的 data 与 sampleResponse 逐字段同类：metrics 为数组（responseFields 指标元数据清单），元素含 metric_id（string）、name（string）、algorithm_type（string）、formula_status（string）、pending_ref（string）；2、total 为 number（responseFields 指标数，示例 1）；3、字段结构与主流程及 sampleResponse 一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metrics |  | INTEG |  | FUNC-01494 | endpoint_id=innov.service-org.metrics catalog_page_id=innov.service-org 组合=MET-02 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01495 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 服务机构管理 | 服务机构管理指标清单 | 验证服务机构管理指标清单功能，检查 module 非法填写 module=__invalid__ 后返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=__invalid__ | 1.侧栏进入「创新监测算法库」→「服务机构管理」；2.切换至「算法测试」tab；3.接口下拉选择「服务机构管理指标清单」；4.填写 module=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 module 非法；2、不返回含 metrics 与 total 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metrics |  | INTEG |  | FUNC-01495 | endpoint_id=innov.service-org.metrics catalog_page_id=innov.service-org 组合=MET-03 场景=异常-入参-非法module catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01496 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 服务机构管理 | 影响力评价 | 验证影响力评价功能，检查填写 module=service-org 传 module=service-org 后返回 metric_id、hint 及 metrics、total 字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=service-org | 1.侧栏进入「创新监测算法库」→「服务机构管理」；2.切换至「算法测试」tab；3.接口下拉选择「影响力评价」；4.填写 module=service-org，点击调用 | 1、返回面板 body 的 data 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_DS_29_INCUBATOR_006）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_29_INCUBATOR_006/compute | M_INNOV_DS_29_INCUBATOR_006 | INTEG |  | FUNC-01496 | endpoint_id=innov.service-org.m_innov_ds_29_incubator_006 catalog_page_id=innov.service-org 组合=INC-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01497 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 服务机构管理 | 影响力评价 | 验证影响力评价功能，检查不传可选 module 不传 module 后仍返回与 sampleResponse 同类结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 module | 1.侧栏进入「创新监测算法库」→「服务机构管理」；2.切换至「算法测试」tab；3.接口下拉选择「影响力评价」；4.不传 module，点击调用 | 1、返回面板 body 的 data 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_DS_29_INCUBATOR_006）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_29_INCUBATOR_006/compute | M_INNOV_DS_29_INCUBATOR_006 | INTEG |  | FUNC-01497 | endpoint_id=innov.service-org.m_innov_ds_29_incubator_006 catalog_page_id=innov.service-org 组合=INC-02 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01498 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 服务机构管理 | 影响力评价 | 验证影响力评价功能，检查 module 非法填写 module=__invalid__ 后返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=__invalid__ | 1.侧栏进入「创新监测算法库」→「服务机构管理」；2.切换至「算法测试」tab；3.接口下拉选择「影响力评价」；4.填写 module=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id 为 M_INNOV_DS_29_INCUBATOR_006 且含 hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_29_INCUBATOR_006/compute |  | INTEG |  | FUNC-01498 | endpoint_id=innov.service-org.m_innov_ds_29_incubator_006 catalog_page_id=innov.service-org 组合=INC-03 场景=异常-入参-非法module catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01499 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 服务机构管理 | 接口信息 | 验证服务机构管理的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「服务机构管理」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 2；2、下拉名称与 §0 各 title 一致（服务机构管理指标清单、影响力评价）；3、默认项概览 method=GET、path=/innov/v1/innov/metrics；4、切换后概览对应影响力评价 POST /innov/v1/innov/metric/M_INNOV_DS_29_INCUBATOR_006/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-01499 | catalog_page_id=innov.service-org 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01500 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 服务机构管理 | 算法测试 | 验证服务机构管理的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「服务机构管理」；2.切换至「算法测试」tab；3.接口下拉切换到「影响力评价」 | 1、算法测试 tab 下拉共 2 项，名称与接口信息 tab、catalog 一致；2、切换后调用区 method 为 POST、path 为 /innov/v1/innov/metric/M_INNOV_DS_29_INCUBATOR_006/compute；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对接口下拉共 2 项且名称与 §0 一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-01500 | catalog_page_id=innov.service-org 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

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
| 服务机构管理指标清单 | innov.service-org.metrics | GET | /innov/v1/innov/metrics | module? | running |
| 影响力评价 | innov.service-org.m_innov_ds_29_incubator_006 | POST | /innov/v1/innov/metric/M_INNOV_DS_29_INCUBATOR_006/compute | module? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.service-org.metrics | FUNC-01493、01494、01495 |
| innov.service-org.m_innov_ds_29_incubator_006 | FUNC-01496、01497、01498 |
| （页面清单） | FUNC-01499、01500 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 2 个 title 均在功能点列出现且各有 1 条主流程（步骤为联调台侧栏/下拉/填参/点击调用）
- [x] 每个接口恰好 3 条：sampleRequest 主流程 + 与 sample 相反的不传 module + 非法 module
- [x] 正向预期逐字段写 sampleResponse；POST 另写 responseFields 的 metrics、total
- [x] 反向预期为 message 或 msg 指出 module 非法
- [x] 无登录 / Token / 401 / 424；0 条裸 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 待挂需规 / 待挂需规
- [x] 双接口页清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（01499、01500）
- [x] A 线无对应 Lxx；未改 work
- [x] `coverage-fp.md` 已同步 FUNC-01493～01500；旧 API-02205～02210 作废

**统计**：合计 **8** 条（主流程 2、备选 2、反向 2、清单 2）；编号闭区间 **FUNC-01493**～**FUNC-01500**（R3 · innov.service-org）。金样 **FUNC-01493**（MET-01）。
