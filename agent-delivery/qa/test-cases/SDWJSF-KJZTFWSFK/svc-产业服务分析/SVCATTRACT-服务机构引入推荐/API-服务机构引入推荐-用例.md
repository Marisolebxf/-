# 智能服务集群-科技专题服务算法库测试用例（服务机构引入推荐 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业服务分析 / 服务机构引入推荐  
> **catalog**：`entry_id=svc.attract` · `catalog_page_id=svc.attract` · path `/industry-service/attract`  
> **A 线对照**：`fp-split-by-api-run/work/L49.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：联调台 `http://111.198.38.90:50897/`（接口文档真源 `svc.json` 页 `svc.attract`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批15）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 引入推荐 | svc.attract.models |
| 2 | 服务机构引入推荐模型 | svc.attract.m_svc_deep_180_1 |

**kind 试调取值**：两个接口都只有可选 `kind`。主流程对齐各自 `sampleRequest`：`kind=attract`。省略 `kind` 为备选。非法值 `kind=__invalid__` 单独作反向。`引入推荐` 的 catalog `status=unavailable`，仍按该接口文档返回体编写。`服务机构引入推荐模型` 的 params.example 与 options 为 `tech`，与 sampleRequest `attract` 不一致，主流程以 sampleRequest 为准。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01704**～**API-01709**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=svc.attract`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01704 | 产业服务分析 | 服务机构引入推荐 | 主流程 | — | 服务机构引入推荐 | 引入推荐 | 引入推荐按文档 sampleRequest kind=attract 查询返回引入名单字段 | 1、kind 使用文档示例 attract | 1.GET /entan/v1/svc/models，查询参数取组合 ATTR-01 | 1、返回 body 顶层含 attract（array，responseFields 引入名单）；2、元素含 org_id（string，示例 svc:sh_fin、svc:bj_ip）、attraction_index（number，示例 88.4、76.2）、priority_level（string，示例 high、mid）、rank_no（number，示例 1、2）、recommend_reason（string，示例 产业匹配高、知产服务互补）；3、元素含 ext.name（string，示例 上海科技金融集团、北京知产运营中心）；4、元素含 dimension_scores.industryFit（number，示例 90、72）、techLead（number，示例 84、78）、potential（number，示例 80、74）、willingness（number，示例 70、66）；5、结构与 sampleResponse 一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_REC_ATTRACT_SCORE | INTEG | | | endpoint_id=svc.attract.models catalog_page_id=svc.attract 组合=ATTR-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01705 | 产业服务分析 | 服务机构引入推荐 | 备选-参数组合 | 省略 kind | 服务机构引入推荐 | 引入推荐 | 引入推荐不传可选 kind（与 sampleRequest 相反） | 1、不传 kind | 1.GET /entan/v1/svc/models，查询参数取组合 ATTR-02 | 1、返回 body 顶层仍含 attract（array，responseFields 引入名单）；2、元素仍含 org_id（string）、attraction_index（number）、priority_level（string）、rank_no（number）、recommend_reason（string）；3、元素仍含 ext.name（string）；4、元素仍含 dimension_scores.industryFit、techLead、potential、willingness（number）；5、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_REC_ATTRACT_SCORE | INTEG | | | endpoint_id=svc.attract.models catalog_page_id=svc.attract 组合=ATTR-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01706 | 产业服务分析 | 服务机构引入推荐 | 异常-入参-非法kind | — | 服务机构引入推荐 | 引入推荐 | 引入推荐 kind 非法 | 1、kind 取文档枚举外的值 | 1.GET /entan/v1/svc/models，查询参数取组合 ATTR-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 attract 引入名单的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | | INTEG | | | endpoint_id=svc.attract.models catalog_page_id=svc.attract 组合=ATTR-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01707 | 产业服务分析 | 服务机构引入推荐 | 主流程 | — | 服务机构引入推荐 | 服务机构引入推荐模型 | 服务机构引入推荐模型按文档 sampleRequest kind=attract 计算 | 1、kind 使用文档 sampleRequest attract | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_180_1/compute，请求体取组合 M180-01 | 1、返回 body 与 sampleResponse 同层含 metric_id（string，示例 M_SVC_DEEP_180_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 声明 metric_id（string，指标 ID）；3、结构与 sampleResponse 一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_180_1/compute | M_SVC_DEEP_180_1 | INTEG | | | endpoint_id=svc.attract.m_svc_deep_180_1 catalog_page_id=svc.attract 组合=M180-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01708 | 产业服务分析 | 服务机构引入推荐 | 备选-参数组合 | 省略 kind | 服务机构引入推荐 | 服务机构引入推荐模型 | 服务机构引入推荐模型不传可选 kind（与 sampleRequest 相反） | 1、不传 kind | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_180_1/compute，请求体取组合 M180-02 | 1、返回 body 仍含 metric_id（string）、hint（string）；2、responseFields 所列 metric_id（string，指标 ID）仍应出现；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_180_1/compute | M_SVC_DEEP_180_1 | INTEG | | | endpoint_id=svc.attract.m_svc_deep_180_1 catalog_page_id=svc.attract 组合=M180-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01709 | 产业服务分析 | 服务机构引入推荐 | 异常-入参-非法kind | — | 服务机构引入推荐 | 服务机构引入推荐模型 | 服务机构引入推荐模型 kind 非法 | 1、kind 取文档枚举外的值 | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_180_1/compute，请求体取组合 M180-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 metric_id 为 M_SVC_DEEP_180_1 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_180_1/compute | | INTEG | | | endpoint_id=svc.attract.m_svc_deep_180_1 catalog_page_id=svc.attract 组合=M180-03 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| ATTR-01 | svc.attract.models | kind=attract | 主路径（sampleRequest） |
| ATTR-02 | svc.attract.models | 不传 kind | 省略可选 kind |
| ATTR-03 | svc.attract.models | kind=__invalid__ | 只破坏 kind |
| M180-01 | svc.attract.m_svc_deep_180_1 | kind=attract | 主路径（sampleRequest） |
| M180-02 | svc.attract.m_svc_deep_180_1 | 不传 kind | 省略可选 kind |
| M180-03 | svc.attract.m_svc_deep_180_1 | kind=__invalid__ | 只破坏 kind |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 引入推荐 | svc.attract.models | GET | /entan/v1/svc/models | kind? | unavailable |
| 服务机构引入推荐模型 | svc.attract.m_svc_deep_180_1 | POST | /entan/v1/svc-metric/metric/M_SVC_DEEP_180_1/compute | kind? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| svc.attract.models | API-01704、01705、01706 |
| svc.attract.m_svc_deep_180_1 | API-01707、01708、01709 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title 均在功能点列出现，且各有 1 条主流程（01704、01707）
- [x] 各接口仅可选 kind：sampleRequest 主流程 1 条 + 省略 kind 备选 1 条 + 非法 kind 反向 1 条
- [x] unavailable（引入推荐）仍按 catalog 返回体写主流程，备注注明未交付
- [x] 正向预期逐字段写 sampleResponse；反向预期写 message 或 msg 指出 kind 非法
- [x] 无登录 / Token / 401 / 424 用例
- [x] `coverage-fp.md` 已同步 API-01704～01709

**统计**：接口 **2**；用例 **6** 条（主流程 2、备选 2、反向 2）；编号闭区间 **API-01704**～**API-01709**（父控 R2-批15 分配，连续用满）。
