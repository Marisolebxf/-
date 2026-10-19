# 智能服务集群-科技专题服务算法库测试用例（服务机构培育推荐 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业服务分析 / 服务机构培育推荐  
> **catalog**：`entry_id=svc.cultivate` · `catalog_page_id=svc.cultivate` · path `/industry-service/cultivate`  
> **A 线对照**：`fp-split-by-api-run/work/L50.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：联调台 `http://111.198.38.90:50897/`（接口文档真源 `svc.json` 页 `svc.cultivate`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批15）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 培育推荐 | svc.cultivate.models |
| 2 | 服务机构培育推荐模型 | svc.cultivate.m_svc_deep_181_1 |

**kind 试调取值**：两个接口都只有可选 `kind`。主流程对齐各自 `sampleRequest`：`kind=cultivate`。省略 `kind` 为备选。非法值 `kind=__invalid__` 单独作反向。`培育推荐` 的 catalog `status=unavailable`，仍按该接口文档返回体编写。`服务机构培育推荐模型` 的 `params.example` / `options` 为 `tech`，`sampleRequest` 为 `kind=cultivate`，主流程取 `sampleRequest`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01710**～**API-01715**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=svc.cultivate`、组合 id。旧号 API-000634～000638 作废，不复用。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01710 | 产业服务分析 | 服务机构培育推荐 | 主流程 | — | 服务机构培育推荐 | 培育推荐 | 培育推荐按文档 sampleRequest kind=cultivate 查询返回培育名单字段 | 1、kind 使用文档示例 cultivate | 1.GET /entan/v1/svc/models，查询参数取组合 CULM-01 | 1、返回 body 顶层含 cultivate（array，responseFields 培育名单）；2、元素含 org_id（string，示例 svc:ns_fin、svc:ip_sz）、cultivation_index（number，示例 84.0、71.5）、priority_level（string，示例 high、mid）、growth_stage（string，示例 扩张、成长）、advice（string，示例 补强跨境服务、扩大海外布局）；3、ext 含 name（string，示例 南山科技金融站、知产服务中心）；4、dimension_scores 含 scale（number，示例 78、66）、innovation（number，示例 82、75）、effect（number，示例 80、70）、marketGap（number，示例 74、68）；5、结构与 sampleResponse 一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_REC_CULTIVATE_SCORE | INTEG | | | endpoint_id=svc.cultivate.models catalog_page_id=svc.cultivate 组合=CULM-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01711 | 产业服务分析 | 服务机构培育推荐 | 备选-参数组合 | 省略 kind | 服务机构培育推荐 | 培育推荐 | 培育推荐不传可选 kind（与 sampleRequest 相反） | 1、不传 kind | 1.GET /entan/v1/svc/models，查询参数取组合 CULM-02 | 1、返回 body 顶层仍含 cultivate（array，responseFields 培育名单）；2、元素仍含 org_id（string）、cultivation_index（number）、priority_level（string）、growth_stage（string）、advice（string）；3、ext 仍含 name（string）；4、dimension_scores 仍含 scale、innovation、effect、marketGap（number）；5、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_REC_CULTIVATE_SCORE | INTEG | | | endpoint_id=svc.cultivate.models catalog_page_id=svc.cultivate 组合=CULM-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01712 | 产业服务分析 | 服务机构培育推荐 | 异常-入参-非法kind | — | 服务机构培育推荐 | 培育推荐 | 培育推荐 kind 非法 | 1、kind 取文档枚举外的值 | 1.GET /entan/v1/svc/models，查询参数取组合 CULM-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 cultivate 培育名单数组的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | | INTEG | | | endpoint_id=svc.cultivate.models catalog_page_id=svc.cultivate 组合=CULM-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01713 | 产业服务分析 | 服务机构培育推荐 | 主流程 | — | 服务机构培育推荐 | 服务机构培育推荐模型 | 服务机构培育推荐模型按文档 sampleRequest kind=cultivate 计算 | 1、kind 使用文档示例 cultivate | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_181_1/compute，请求体取组合 CULC-01 | 1、返回 body 与 sampleResponse 同层含 metric_id（string，示例 M_SVC_DEEP_181_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 声明 metric_id 为 string（指标 ID） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_181_1/compute | M_SVC_DEEP_181_1 | INTEG | | | endpoint_id=svc.cultivate.m_svc_deep_181_1 catalog_page_id=svc.cultivate 组合=CULC-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01714 | 产业服务分析 | 服务机构培育推荐 | 备选-参数组合 | 省略 kind | 服务机构培育推荐 | 服务机构培育推荐模型 | 服务机构培育推荐模型不传可选 kind（与 sampleRequest 相反） | 1、不传 kind | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_181_1/compute，请求体取组合 CULC-02 | 1、返回 body 仍含 metric_id（string，示例 M_SVC_DEEP_181_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 所列 metric_id（string，指标 ID）仍应出现；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_181_1/compute | M_SVC_DEEP_181_1 | INTEG | | | endpoint_id=svc.cultivate.m_svc_deep_181_1 catalog_page_id=svc.cultivate 组合=CULC-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01715 | 产业服务分析 | 服务机构培育推荐 | 异常-入参-非法kind | — | 服务机构培育推荐 | 服务机构培育推荐模型 | 服务机构培育推荐模型 kind 非法 | 1、kind 取文档枚举外的值 | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_181_1/compute，请求体取组合 CULC-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 metric_id 为 M_SVC_DEEP_181_1 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_181_1/compute | | INTEG | | | endpoint_id=svc.cultivate.m_svc_deep_181_1 catalog_page_id=svc.cultivate 组合=CULC-03 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| CULM-01 | svc.cultivate.models | kind=cultivate | 主路径（sampleRequest） |
| CULM-02 | svc.cultivate.models | 不传 kind | 省略可选 kind |
| CULM-03 | svc.cultivate.models | kind=__invalid__ | 只破坏 kind |
| CULC-01 | svc.cultivate.m_svc_deep_181_1 | kind=cultivate | 主路径（sampleRequest） |
| CULC-02 | svc.cultivate.m_svc_deep_181_1 | 不传 kind | 省略可选 kind |
| CULC-03 | svc.cultivate.m_svc_deep_181_1 | kind=__invalid__ | 只破坏 kind |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 培育推荐 | svc.cultivate.models | GET | /entan/v1/svc/models | kind? | unavailable |
| 服务机构培育推荐模型 | svc.cultivate.m_svc_deep_181_1 | POST | /entan/v1/svc-metric/metric/M_SVC_DEEP_181_1/compute | kind? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| svc.cultivate.models | API-01710、01711、01712 |
| svc.cultivate.m_svc_deep_181_1 | API-01713、01714、01715 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title 均在功能点列出现，且各有 1 条主流程（01710、01713）
- [x] 各接口仅可选 kind：sampleRequest 主流程 1 条 + 省略 kind 备选 1 条 + 非法 kind 反向 1 条
- [x] unavailable（培育推荐）仍按 catalog 返回体写主流程，备注注明未交付
- [x] 正向预期逐字段写 sampleResponse；反向预期写 message 或 msg 指出 kind 非法
- [x] `coverage-fp.md` 已同步 API-01710～01715

**统计**：接口 **2**；用例 **6** 条（主流程 2、备选 2、反向 2）；编号闭区间 **API-01710**～**API-01715**（父控 R2-批15 分配，连续用满）。
