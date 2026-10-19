# 智能服务集群-科技专题服务算法库测试用例（人力资源服务机构技术力评估 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业服务分析 / 人力资源服务机构技术力评估  
> **catalog**：`entry_id=svc.tech-hr` · `catalog_page_id=svc.tech-hr` · path `/industry-service/tech-hr`  
> **A 线对照**：`fp-split-by-api-run/work/L45.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：联调台 `http://111.198.38.90:50897/`（接口文档真源 `svc.json` 页 `svc.tech-hr`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批14）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 人力资源技术力 | svc.tech-hr.models |
| 2 | 人力资源服务机构技术力评价模型 | svc.tech-hr.m_svc_deep_176_1 |

**kind 试调取值**：两个接口都只有可选 `kind`。主流程对齐各自 `sampleRequest`：`kind=tech`。省略 `kind` 为备选。非法值 `kind=__invalid__` 单独作反向。`人力资源技术力` 的 catalog `status=unavailable`，仍按该接口文档返回体编写。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01680**～**API-01685**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=svc.tech-hr`、组合 id。旧号 API-00609～00613 作废，不复用。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01680 | 产业服务分析 | 人力资源服务机构技术力评估 | 主流程 | — | 人力资源服务机构技术力评估 | 人力资源技术力 | 人力资源技术力按文档 sampleRequest kind=tech 查询返回技术力名单字段 | 1、kind 使用文档示例 tech | 1.GET /entan/v1/svc/models，查询参数取组合 HRM-01 | 1、返回 body 顶层含 tech（array，responseFields 技术力名单）；2、元素含 org_id（string，示例 svc:hr_ft）、service_type（string，示例 HR）、score（number，示例 77.5）；3、ext 含 name（string，示例 福田人才服务港）、rank_no（number，示例 1）；4、dimension_scores 含 patents（number，示例 52）、rdInvestment（number，示例 60）、experts（number，示例 88）、cases（number，示例 81）、standards（number，示例 48）；5、结构与 sampleResponse 一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_ORG_TECH_SCORE | INTEG | | | endpoint_id=svc.tech-hr.models catalog_page_id=svc.tech-hr 组合=HRM-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01681 | 产业服务分析 | 人力资源服务机构技术力评估 | 备选-参数组合 | 省略 kind | 人力资源服务机构技术力评估 | 人力资源技术力 | 人力资源技术力不传可选 kind（与 sampleRequest 相反） | 1、不传 kind | 1.GET /entan/v1/svc/models，查询参数取组合 HRM-02 | 1、返回 body 顶层仍含 tech（array，responseFields 技术力名单）；2、元素仍含 org_id（string）、service_type（string）、score（number）；3、ext 仍含 name（string）、rank_no（number）；4、dimension_scores 仍含 patents、rdInvestment、experts、cases、standards（number）；5、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_ORG_TECH_SCORE | INTEG | | | endpoint_id=svc.tech-hr.models catalog_page_id=svc.tech-hr 组合=HRM-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01682 | 产业服务分析 | 人力资源服务机构技术力评估 | 异常-入参-非法kind | — | 人力资源服务机构技术力评估 | 人力资源技术力 | 人力资源技术力 kind 非法 | 1、kind 取文档枚举外的值 | 1.GET /entan/v1/svc/models，查询参数取组合 HRM-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 tech 技术力名单数组的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | | INTEG | | | endpoint_id=svc.tech-hr.models catalog_page_id=svc.tech-hr 组合=HRM-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01683 | 产业服务分析 | 人力资源服务机构技术力评估 | 主流程 | — | 人力资源服务机构技术力评估 | 人力资源服务机构技术力评价模型 | 人力资源服务机构技术力评价模型按文档 sampleRequest kind=tech 计算 | 1、kind 使用文档示例 tech | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_176_1/compute，请求体取组合 HRC-01 | 1、返回 body 与 sampleResponse 同层含 metric_id（string，示例 M_SVC_DEEP_176_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 声明 tech 为 array（技术力名单）；3、sampleResponse 未给出 tech 示例元素，返回中应出现 responseFields 所列 tech | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_176_1/compute | M_SVC_DEEP_176_1 | INTEG | | | endpoint_id=svc.tech-hr.m_svc_deep_176_1 catalog_page_id=svc.tech-hr 组合=HRC-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01684 | 产业服务分析 | 人力资源服务机构技术力评估 | 备选-参数组合 | 省略 kind | 人力资源服务机构技术力评估 | 人力资源服务机构技术力评价模型 | 人力资源服务机构技术力评价模型不传可选 kind（与 sampleRequest 相反） | 1、不传 kind | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_176_1/compute，请求体取组合 HRC-02 | 1、返回 body 仍含 metric_id（string，示例 M_SVC_DEEP_176_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 所列 tech（array，技术力名单）仍应出现；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_176_1/compute | M_SVC_DEEP_176_1 | INTEG | | | endpoint_id=svc.tech-hr.m_svc_deep_176_1 catalog_page_id=svc.tech-hr 组合=HRC-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01685 | 产业服务分析 | 人力资源服务机构技术力评估 | 异常-入参-非法kind | — | 人力资源服务机构技术力评估 | 人力资源服务机构技术力评价模型 | 人力资源服务机构技术力评价模型 kind 非法 | 1、kind 取文档枚举外的值 | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_176_1/compute，请求体取组合 HRC-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 metric_id 为 M_SVC_DEEP_176_1 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_176_1/compute | | INTEG | | | endpoint_id=svc.tech-hr.m_svc_deep_176_1 catalog_page_id=svc.tech-hr 组合=HRC-03 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| HRM-01 | svc.tech-hr.models | kind=tech | 主路径（sampleRequest） |
| HRM-02 | svc.tech-hr.models | 不传 kind | 省略可选 kind |
| HRM-03 | svc.tech-hr.models | kind=__invalid__ | 只破坏 kind |
| HRC-01 | svc.tech-hr.m_svc_deep_176_1 | kind=tech | 主路径（sampleRequest） |
| HRC-02 | svc.tech-hr.m_svc_deep_176_1 | 不传 kind | 省略可选 kind |
| HRC-03 | svc.tech-hr.m_svc_deep_176_1 | kind=__invalid__ | 只破坏 kind |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 人力资源技术力 | svc.tech-hr.models | GET | /entan/v1/svc/models | kind? | unavailable |
| 人力资源服务机构技术力评价模型 | svc.tech-hr.m_svc_deep_176_1 | POST | /entan/v1/svc-metric/metric/M_SVC_DEEP_176_1/compute | kind? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| svc.tech-hr.models | API-01680、01681、01682 |
| svc.tech-hr.m_svc_deep_176_1 | API-01683、01684、01685 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title 均在功能点列出现，且各有 1 条主流程（01680、01683）
- [x] 各接口仅可选 kind：sampleRequest 主流程 1 条 + 省略 kind 备选 1 条 + 非法 kind 反向 1 条
- [x] unavailable（人力资源技术力）仍按 catalog 返回体写主流程，备注注明未交付
- [x] 正向预期逐字段写 sampleResponse；反向预期写 message 或 msg 指出 kind 非法
- [x] `coverage-fp.md` 已同步 API-01680～01685

**统计**：接口 **2**；用例 **6** 条（主流程 2、备选 2、反向 2）；编号闭区间 **API-01680**～**API-01685**（父控 R2-批14 分配，连续用满）。
