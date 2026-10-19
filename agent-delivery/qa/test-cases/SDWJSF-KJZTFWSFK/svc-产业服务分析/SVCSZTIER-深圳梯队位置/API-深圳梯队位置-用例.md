# 智能服务集群-科技专题服务算法库测试用例（深圳梯队位置 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业服务分析 / 深圳梯队位置  
> **catalog**：`entry_id=svc.sz-tier` · `catalog_page_id=svc.sz-tier` · path `/industry-service/sz-tier`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/svc.json` 页 `svc.sz-tier`  
> **A 线对照**：无对应 Lxx。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `svc.sz-tier`（不扩六级）。不改 `work/`  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批16）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 深圳梯队 | svc.sz-tier.main |
| 2 | 深圳梯队位置 | svc.sz-tier.m_svc_sz_tier |

**industry 文档取值**：两个接口都只有可选 `industry`。主流程对齐各自 `sampleRequest`：`industry=人工智能`。省略 `industry` 为备选。非法值 `industry=__invalid__` 单独作反向。`深圳梯队` 的 catalog `status=unavailable`，仍按该接口文档返回体编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01722**～**API-01727**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=svc.sz-tier`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01722 | 产业服务分析 | 深圳梯队位置 | 主流程 | — | 深圳梯队位置 | 深圳梯队 | 深圳梯队按文档 sampleRequest industry=人工智能 查询返回三维度梯队字段 | 1、industry 使用文档示例 人工智能 | 1.GET /entan/v1/svc/sz-tier，查询参数取组合 SZT-01 | 1、返回 body 含 dims（array，responseFields 三维度梯队位置）；2、元素含 dim（string）、dim_key（string）、tier（string）；3、sampleResponse 示例三行：dim=机构数量、dim_key=org_count、tier=T1；dim=技术力得分、dim_key=tech_score、tier=T2；dim=服务链完整度、dim_key=chain_coverage、tier=T1；4、结构与 sampleResponse 一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/sz-tier | | INTEG | | | endpoint_id=svc.sz-tier.main catalog_page_id=svc.sz-tier 组合=SZT-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01723 | 产业服务分析 | 深圳梯队位置 | 备选-参数组合 | 省略 industry | 深圳梯队位置 | 深圳梯队 | 深圳梯队不传可选 industry（与 sampleRequest 相反） | 1、不传 industry | 1.GET /entan/v1/svc/sz-tier，查询参数取组合 SZT-02 | 1、返回 body 仍含 dims（array，responseFields 三维度梯队位置）；2、元素仍含 dim（string）、dim_key（string）、tier（string）；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/sz-tier | | INTEG | | | endpoint_id=svc.sz-tier.main catalog_page_id=svc.sz-tier 组合=SZT-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01724 | 产业服务分析 | 深圳梯队位置 | 异常-入参-非法industry | — | 深圳梯队位置 | 深圳梯队 | 深圳梯队 industry 非法 | 1、industry 取文档示例外的值 | 1.GET /entan/v1/svc/sz-tier，查询参数取组合 SZT-03 | 1、返回 body 的 message 或 msg 指出 industry 非法；2、不返回含 dims 三维度梯队的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/sz-tier | | INTEG | | | endpoint_id=svc.sz-tier.main catalog_page_id=svc.sz-tier 组合=SZT-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01725 | 产业服务分析 | 深圳梯队位置 | 主流程 | — | 深圳梯队位置 | 深圳梯队位置 | 深圳梯队位置按文档 sampleRequest industry=人工智能 计算 | 1、industry 使用文档示例 人工智能 | 1.POST /entan/v1/svc-metric/metric/M_SVC_SZ_TIER/compute，请求体取组合 SZC-01 | 1、返回 body 与 sampleResponse 同层含 metric_id（string，示例 M_SVC_SZ_TIER）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 声明 dims 为 array（三维度梯队位置）；3、sampleResponse 未给出 dims 示例元素，返回中应出现 responseFields 所列 dims；4、结构与 sampleResponse 一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_SZ_TIER/compute | M_SVC_SZ_TIER | INTEG | | | endpoint_id=svc.sz-tier.m_svc_sz_tier catalog_page_id=svc.sz-tier 组合=SZC-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01726 | 产业服务分析 | 深圳梯队位置 | 备选-参数组合 | 省略 industry | 深圳梯队位置 | 深圳梯队位置 | 深圳梯队位置不传可选 industry（与 sampleRequest 相反） | 1、不传 industry | 1.POST /entan/v1/svc-metric/metric/M_SVC_SZ_TIER/compute，请求体取组合 SZC-02 | 1、返回 body 仍含 metric_id（string）、hint（string）；2、responseFields 所列 dims（array，三维度梯队位置）仍应出现；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_SZ_TIER/compute | M_SVC_SZ_TIER | INTEG | | | endpoint_id=svc.sz-tier.m_svc_sz_tier catalog_page_id=svc.sz-tier 组合=SZC-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01727 | 产业服务分析 | 深圳梯队位置 | 异常-入参-非法industry | — | 深圳梯队位置 | 深圳梯队位置 | 深圳梯队位置 industry 非法 | 1、industry 取文档示例外的值 | 1.POST /entan/v1/svc-metric/metric/M_SVC_SZ_TIER/compute，请求体取组合 SZC-03 | 1、返回 body 的 message 或 msg 指出 industry 非法；2、不返回含 metric_id 为 M_SVC_SZ_TIER 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_SZ_TIER/compute | | INTEG | | | endpoint_id=svc.sz-tier.m_svc_sz_tier catalog_page_id=svc.sz-tier 组合=SZC-03 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| SZT-01 | svc.sz-tier.main | industry=人工智能 | 主路径（sampleRequest） |
| SZT-02 | svc.sz-tier.main | 不传 industry | 省略可选 industry |
| SZT-03 | svc.sz-tier.main | industry=__invalid__ | 只破坏 industry |
| SZC-01 | svc.sz-tier.m_svc_sz_tier | industry=人工智能 | 主路径（sampleRequest） |
| SZC-02 | svc.sz-tier.m_svc_sz_tier | 不传 industry | 省略可选 industry |
| SZC-03 | svc.sz-tier.m_svc_sz_tier | industry=__invalid__ | 只破坏 industry |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 深圳梯队 | svc.sz-tier.main | GET | /entan/v1/svc/sz-tier | industry? | unavailable |
| 深圳梯队位置 | svc.sz-tier.m_svc_sz_tier | POST | /entan/v1/svc-metric/metric/M_SVC_SZ_TIER/compute | industry? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| svc.sz-tier.main | API-01722、01723、01724 |
| svc.sz-tier.m_svc_sz_tier | API-01725、01726、01727 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title 均在功能点列出现，且各有 1 条主流程（01722、01725）
- [x] 各接口仅可选 industry：sampleRequest 主流程 1 条 + 省略 industry 备选 1 条 + 非法 industry 反向 1 条
- [x] unavailable（深圳梯队）仍按 catalog 返回体写主流程，备注注明未交付
- [x] 正向预期逐字段写 sampleResponse；反向预期写 message 或 msg 指出 industry 非法
- [x] 无登录 / Token / 401 / 424
- [x] `coverage-fp.md` 已同步 API-01722～01727；A 线写无对应 Lxx
- [ ] `code-registry.yaml` 由父控回写（本子任务未改 registry）

**统计**：用例 **6** 条；主流程 **2**、备选 **2**、反向 **2**；编号闭区间 **API-01722**～**API-01727**（父控 R2-批16 分配）。
