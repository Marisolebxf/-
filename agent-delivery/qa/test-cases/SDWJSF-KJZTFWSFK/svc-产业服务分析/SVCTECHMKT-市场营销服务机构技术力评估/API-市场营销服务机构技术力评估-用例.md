# 智能服务集群-科技专题服务算法库测试用例（市场营销服务机构技术力评估 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业服务分析 / 市场营销服务机构技术力评估  
> **catalog**：`entry_id=svc.tech-mkt` · `catalog_page_id=svc.tech-mkt` · path `/industry-service/tech-mkt`  
> **A 线对照**：`fp-split-by-api-run/work/L46.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：联调台 `http://111.198.38.90:50897/`（接口文档真源 `svc.json` 页 `svc.tech-mkt`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批14）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 市场营销技术力 | svc.tech-mkt.models |
| 2 | 市场营销服务机构技术力评价模型 | svc.tech-mkt.m_svc_deep_177_1 |

**kind 试调取值**：两个接口都只有可选 `kind`。主流程对齐各自 `sampleRequest`：`kind=tech`。省略 `kind` 为备选。非法值 `kind=__invalid__` 单独作反向。`市场营销技术力` 的 catalog `status=unavailable`，仍按该接口文档返回体编写。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01686**～**API-01691**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=svc.tech-mkt`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01686 | 产业服务分析 | 市场营销服务机构技术力评估 | 主流程 | — | 市场营销服务机构技术力评估 | 市场营销技术力 | 市场营销技术力按文档 sampleRequest kind=tech 查询返回技术力名单字段 | 1、kind 使用文档示例 tech | 1.GET /entan/v1/svc/models，查询参数取组合 TMKT-01 | 1、返回 body 顶层含 tech（array，responseFields 技术力名单）；2、元素含 org_id（string，示例 svc:mkt_lg）、service_type（string，示例 MKT）、score（number，示例 73.8）；3、元素含 ext.name（string，示例 龙岗产业推广中心）、ext.rank_no（number，示例 1）；4、元素含 dimension_scores.patents（number，示例 40）、rdInvestment（number，示例 55）、experts（number，示例 62）、cases（number，示例 84）、standards（number，示例 44）；5、结构与 sampleResponse 一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_ORG_TECH_SCORE | INTEG | | | endpoint_id=svc.tech-mkt.models catalog_page_id=svc.tech-mkt 组合=TMKT-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01687 | 产业服务分析 | 市场营销服务机构技术力评估 | 备选-参数组合 | 省略 kind | 市场营销服务机构技术力评估 | 市场营销技术力 | 市场营销技术力不传可选 kind（与 sampleRequest 相反） | 1、不传 kind | 1.GET /entan/v1/svc/models，查询参数取组合 TMKT-02 | 1、返回 body 顶层仍含 tech（array，responseFields 技术力名单）；2、元素仍含 org_id（string）、service_type（string）、score（number）；3、元素仍含 ext.name（string）、ext.rank_no（number）；4、元素仍含 dimension_scores.patents、rdInvestment、experts、cases、standards（number）；5、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_ORG_TECH_SCORE | INTEG | | | endpoint_id=svc.tech-mkt.models catalog_page_id=svc.tech-mkt 组合=TMKT-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01688 | 产业服务分析 | 市场营销服务机构技术力评估 | 异常-入参-非法kind | — | 市场营销服务机构技术力评估 | 市场营销技术力 | 市场营销技术力 kind 非法 | 1、kind 取文档枚举外的值 | 1.GET /entan/v1/svc/models，查询参数取组合 TMKT-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 tech 技术力名单的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | | INTEG | | | endpoint_id=svc.tech-mkt.models catalog_page_id=svc.tech-mkt 组合=TMKT-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01689 | 产业服务分析 | 市场营销服务机构技术力评估 | 主流程 | — | 市场营销服务机构技术力评估 | 市场营销服务机构技术力评价模型 | 市场营销服务机构技术力评价模型按文档 sampleRequest kind=tech 计算 | 1、kind 使用文档示例 tech | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_177_1/compute，请求体取组合 M177-01 | 1、返回 body 与 sampleResponse 同层含 metric_id（string，示例 M_SVC_DEEP_177_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 声明 tech 为 array（技术力名单）；3、sampleResponse 未给出 tech 示例元素，返回中应出现 responseFields 所列 tech | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_177_1/compute | M_SVC_DEEP_177_1 | INTEG | | | endpoint_id=svc.tech-mkt.m_svc_deep_177_1 catalog_page_id=svc.tech-mkt 组合=M177-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01690 | 产业服务分析 | 市场营销服务机构技术力评估 | 备选-参数组合 | 省略 kind | 市场营销服务机构技术力评估 | 市场营销服务机构技术力评价模型 | 市场营销服务机构技术力评价模型不传可选 kind（与 sampleRequest 相反） | 1、不传 kind | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_177_1/compute，请求体取组合 M177-02 | 1、返回 body 仍含 metric_id（string）、hint（string）；2、responseFields 所列 tech（array，技术力名单）仍应出现；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_177_1/compute | M_SVC_DEEP_177_1 | INTEG | | | endpoint_id=svc.tech-mkt.m_svc_deep_177_1 catalog_page_id=svc.tech-mkt 组合=M177-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01691 | 产业服务分析 | 市场营销服务机构技术力评估 | 异常-入参-非法kind | — | 市场营销服务机构技术力评估 | 市场营销服务机构技术力评价模型 | 市场营销服务机构技术力评价模型 kind 非法 | 1、kind 取文档枚举外的值 | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_177_1/compute，请求体取组合 M177-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 metric_id 为 M_SVC_DEEP_177_1 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_177_1/compute | | INTEG | | | endpoint_id=svc.tech-mkt.m_svc_deep_177_1 catalog_page_id=svc.tech-mkt 组合=M177-03 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| TMKT-01 | svc.tech-mkt.models | kind=tech | 主路径（sampleRequest） |
| TMKT-02 | svc.tech-mkt.models | 不传 kind | 省略可选 kind |
| TMKT-03 | svc.tech-mkt.models | kind=__invalid__ | 只破坏 kind |
| M177-01 | svc.tech-mkt.m_svc_deep_177_1 | kind=tech | 主路径（sampleRequest） |
| M177-02 | svc.tech-mkt.m_svc_deep_177_1 | 不传 kind | 省略可选 kind |
| M177-03 | svc.tech-mkt.m_svc_deep_177_1 | kind=__invalid__ | 只破坏 kind |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 市场营销技术力 | svc.tech-mkt.models | GET | /entan/v1/svc/models | kind? | unavailable |
| 市场营销服务机构技术力评价模型 | svc.tech-mkt.m_svc_deep_177_1 | POST | /entan/v1/svc-metric/metric/M_SVC_DEEP_177_1/compute | kind? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| svc.tech-mkt.models | API-01686、01687、01688 |
| svc.tech-mkt.m_svc_deep_177_1 | API-01689、01690、01691 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title 均在功能点列出现，且各有 1 条主流程（01686、01689）
- [x] 各接口仅可选 kind：sampleRequest 主流程 1 条 + 省略 kind 备选 1 条 + 非法 kind 反向 1 条
- [x] unavailable（市场营销技术力）仍按 catalog 返回体写主流程，备注注明未交付
- [x] 正向预期逐字段写 sampleResponse；反向预期写 message 或 msg 指出 kind 非法
- [x] 无登录 / Token / 401 / 424 用例
- [x] `coverage-fp.md` 已同步 API-01686～01691

**统计**：接口 **2**；用例 **6** 条（主流程 2、备选 2、反向 2）；编号闭区间 **API-01686**～**API-01691**（父控 R2-批14 分配，连续用满）。
