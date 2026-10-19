# 智能服务集群-科技专题服务算法库测试用例（市场热度评级 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业服务分析 / 市场热度评级  
> **catalog**：`entry_id=svc.market-heat` · `catalog_page_id=svc.market-heat` · path `/industry-service/market-heat`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `svc.market-heat`，原因：不扩六级；不改 `work/`）  
> **环境**：联调台 `http://111.198.38.90:50897/`（接口文档真源 `svc.json` 页 `svc.market-heat`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批16）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 市场热度 | svc.market-heat.main |
| 2 | 市场热度评级 | svc.market-heat.m_svc_org_market_heat |

**industry 取值**：两个接口都只有可选 `industry`。主流程对齐各自 `sampleRequest`：`industry=人工智能`。省略 `industry` 为备选（与 sample 相反的不传）。非法值 `industry=__invalid__` 单独作反向。`市场热度` 的 catalog `status=unavailable`，仍按该接口文档返回体编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01716**～**API-01721**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=svc.market-heat`、组合 id。旧号 API-000639～000643 作废，不复用。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01716 | 产业服务分析 | 市场热度评级 | 主流程 | — | 市场热度评级 | 市场热度 | 市场热度按文档 sampleRequest industry=人工智能 查询返回热度与序列字段 | 1、industry 使用文档示例 人工智能 | 1.GET /entan/v1/svc/market-heat，查询参数取组合 MH-01 | 1、返回 body 含 market_heat_level（string，responseFields 市场热度等级，sampleResponse 示例「高」）；2、trend_slope（number，sampleResponse 示例 0.18）；3、volatility（number，sampleResponse 示例 0.24）；4、series 为数组（responseFields 新增机构时间序列）；5、series 元素含 year（number，示例 2022、2023、2024）与 new_org_count（number，示例 24、31、40）；6、结构与 sampleResponse 一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/market-heat | M_SVC_ORG_MARKET_HEAT | INTEG | | | endpoint_id=svc.market-heat.main catalog_page_id=svc.market-heat 组合=MH-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01717 | 产业服务分析 | 市场热度评级 | 备选-参数组合 | 省略 industry | 市场热度评级 | 市场热度 | 市场热度不传可选 industry（与 sampleRequest 相反） | 1、不传 industry | 1.GET /entan/v1/svc/market-heat，查询参数取组合 MH-02 | 1、返回 body 仍含 market_heat_level（string）、trend_slope（number）、volatility（number）；2、series 仍为数组，元素含 year（number）、new_org_count（number）；3、responseFields 所列 market_heat_level、series 仍应出现；4、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/market-heat | M_SVC_ORG_MARKET_HEAT | INTEG | | | endpoint_id=svc.market-heat.main catalog_page_id=svc.market-heat 组合=MH-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01718 | 产业服务分析 | 市场热度评级 | 异常-入参-非法industry | — | 市场热度评级 | 市场热度 | 市场热度 industry 非法 | 1、industry 取文档示例外的值 | 1.GET /entan/v1/svc/market-heat，查询参数取组合 MH-03 | 1、返回 body 的 message 或 msg 指出 industry 非法；2、不返回含 market_heat_level 或 series 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/market-heat | | INTEG | | | endpoint_id=svc.market-heat.main catalog_page_id=svc.market-heat 组合=MH-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01719 | 产业服务分析 | 市场热度评级 | 主流程 | — | 市场热度评级 | 市场热度评级 | 市场热度评级按文档 sampleRequest industry=人工智能 计算 | 1、industry 使用文档示例 人工智能 | 1.POST /entan/v1/svc-metric/metric/M_SVC_ORG_MARKET_HEAT/compute，请求体取组合 MHR-01 | 1、返回 body 与 sampleResponse 同层含 metric_id（string，示例 M_SVC_ORG_MARKET_HEAT）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 声明 market_heat_level（string，市场热度等级）、series（array，新增机构时间序列），返回中应有这些字段 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_ORG_MARKET_HEAT/compute | M_SVC_ORG_MARKET_HEAT | INTEG | | | endpoint_id=svc.market-heat.m_svc_org_market_heat catalog_page_id=svc.market-heat 组合=MHR-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01720 | 产业服务分析 | 市场热度评级 | 备选-参数组合 | 省略 industry | 市场热度评级 | 市场热度评级 | 市场热度评级不传可选 industry（与 sampleRequest 相反） | 1、不传 industry | 1.POST /entan/v1/svc-metric/metric/M_SVC_ORG_MARKET_HEAT/compute，请求体取组合 MHR-02 | 1、返回 body 仍含 metric_id（string）、hint（string）；2、responseFields 所列 market_heat_level（string，市场热度等级）、series（array，新增机构时间序列）仍应出现；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_ORG_MARKET_HEAT/compute | M_SVC_ORG_MARKET_HEAT | INTEG | | | endpoint_id=svc.market-heat.m_svc_org_market_heat catalog_page_id=svc.market-heat 组合=MHR-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01721 | 产业服务分析 | 市场热度评级 | 异常-入参-非法industry | — | 市场热度评级 | 市场热度评级 | 市场热度评级 industry 非法 | 1、industry 取文档示例外的值 | 1.POST /entan/v1/svc-metric/metric/M_SVC_ORG_MARKET_HEAT/compute，请求体取组合 MHR-03 | 1、返回 body 的 message 或 msg 指出 industry 非法；2、不返回含 metric_id 为 M_SVC_ORG_MARKET_HEAT 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_ORG_MARKET_HEAT/compute | | INTEG | | | endpoint_id=svc.market-heat.m_svc_org_market_heat catalog_page_id=svc.market-heat 组合=MHR-03 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| MH-01 | svc.market-heat.main | industry=人工智能 | 主路径（sampleRequest） |
| MH-02 | svc.market-heat.main | 不传 industry | 省略可选 industry |
| MH-03 | svc.market-heat.main | industry=__invalid__ | 只破坏 industry |
| MHR-01 | svc.market-heat.m_svc_org_market_heat | industry=人工智能 | 主路径（sampleRequest） |
| MHR-02 | svc.market-heat.m_svc_org_market_heat | 不传 industry | 省略可选 industry |
| MHR-03 | svc.market-heat.m_svc_org_market_heat | industry=__invalid__ | 只破坏 industry |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 市场热度 | svc.market-heat.main | GET | /entan/v1/svc/market-heat | industry? | unavailable |
| 市场热度评级 | svc.market-heat.m_svc_org_market_heat | POST | /entan/v1/svc-metric/metric/M_SVC_ORG_MARKET_HEAT/compute | industry? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| svc.market-heat.main | API-01716、01717、01718 |
| svc.market-heat.m_svc_org_market_heat | API-01719、01720、01721 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title 均在功能点列出现，且各有 1 条主流程（01716、01719）
- [x] 各接口仅可选 industry：sampleRequest 主流程 1 条 + 省略 industry 备选 1 条 + 非法 industry 反向 1 条
- [x] unavailable（市场热度）仍按 catalog 返回体写主流程，备注注明未交付
- [x] 正向预期逐字段写 sampleResponse；反向预期写 message 或 msg 指出 industry 非法
- [x] `coverage-fp.md` 已同步 API-01716～01721，写无对应 Lxx

**统计**：接口 **2**；用例 **6** 条（主流程 2、备选 2、反向 2）；编号闭区间 **API-01716**～**API-01721**（父控 R2-批16 分配，连续用满）。
