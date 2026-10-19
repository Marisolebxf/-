# 智能服务集群-科技专题服务算法库测试用例（风险评分 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：工程增强 / 风险评分  
> **catalog**：`entry_id=entan.risk` · `catalog_page_id=entan.risk` · path `/entan/risk`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/entan.json` · 页 `entan.risk`  
> **A 线对照**：无对应 Lxx（工程增强，非 60 六级；`_l6-to-catalog-map.yaml` catalog_skip `entan.risk`；不改 work）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批3）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 风险评分 | entan.risk.list |

`level`、`limit` 均为可选。主路径取 `sampleRequest`：`level` 空串（选项「全部」）、`limit`=200。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01134**～**API-01138**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.risk`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01134 | 工程增强 | 风险评分 | 主流程 | — | 风险评分 | 风险评分 | 风险评分按文档 sampleRequest 传 level 空串、limit=200 返回风险列表字段 | 1、level 使用文档示例空串；limit=200 | 1.GET /entan/v1/risk，查询参数取组合 RISK-01 | 1、返回 body 含 rows（array，responseFields 风险列表）；2、元素含 enterprise_name（string）、risk_score（number）、risk_level（string）、shixin_count（number）、abnormal_count（number）、punish_count（number）；3、与 sampleResponse 一致：南山智造有限公司 enterprise_name、risk_score=68、risk_level=高、shixin_count=1、abnormal_count=2、punish_count=3；深湾算法有限公司 risk_score=41、risk_level=中、shixin_count=0、abnormal_count=1、punish_count=1；云启智元科技股份有限公司 risk_score=18、risk_level=低、shixin_count=0、abnormal_count=0、punish_count=0 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/risk | | INTEG | | | endpoint_id=entan.risk.list catalog_page_id=entan.risk 组合=RISK-01 金样 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01135 | 工程增强 | 风险评分 | 备选-参数组合 | 省略 level | 风险评分 | 风险评分 | 风险评分省略可选 level、仅传 limit=200 返回风险列表字段 | 1、limit=200；不传 level | 1.GET /entan/v1/risk，查询参数取组合 RISK-02 | 1、返回 body 含 rows（array，responseFields 风险列表）；2、元素仍含 enterprise_name（string）、risk_score（number）、risk_level（string）、shixin_count（number）、abnormal_count（number）、punish_count（number）；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/risk | | INTEG | | | endpoint_id=entan.risk.list catalog_page_id=entan.risk 组合=RISK-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01136 | 工程增强 | 风险评分 | 备选-参数组合 | 省略 limit | 风险评分 | 风险评分 | 风险评分传 level 空串、省略可选 limit 返回风险列表字段 | 1、level 使用文档示例空串；不传 limit | 1.GET /entan/v1/risk，查询参数取组合 RISK-03 | 1、返回 body 含 rows（array，responseFields 风险列表）；2、元素仍含 enterprise_name（string）、risk_score（number）、risk_level（string）、shixin_count（number）、abnormal_count（number）、punish_count（number）；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/risk | | INTEG | | | endpoint_id=entan.risk.list catalog_page_id=entan.risk 组合=RISK-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01137 | 工程增强 | 风险评分 | 异常-入参-非法level | — | 风险评分 | 风险评分 | 风险评分 level 取枚举外非法值 | 1、limit=200 保持文档合法值 | 1.GET /entan/v1/risk，查询参数取组合 RISK-04 | 1、返回 body 的 message 或 msg 指出 level 非法；2、不返回含 risk_score、risk_level 的成功业务 rows | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/risk | | INTEG | | | endpoint_id=entan.risk.list catalog_page_id=entan.risk 组合=RISK-04 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01138 | 工程增强 | 风险评分 | 异常-入参-非法limit | — | 风险评分 | 风险评分 | 风险评分 limit 取非整数非法值 | 1、level 使用文档示例空串 | 1.GET /entan/v1/risk，查询参数取组合 RISK-05 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 risk_score 的成功业务 rows | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/risk | | INTEG | | | endpoint_id=entan.risk.list catalog_page_id=entan.risk 组合=RISK-05 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| RISK-01 | entan.risk.list | level=""（sampleRequest 空串，选项全部）；limit=200 | 主路径全参（sampleRequest） |
| RISK-02 | entan.risk.list | 不传 level；limit=200 | 省略可选 level |
| RISK-03 | entan.risk.list | level=""；不传 limit | 省略可选 limit |
| RISK-04 | entan.risk.list | level=__invalid_level__；limit=200 | 只破坏 level |
| RISK-05 | entan.risk.list | level=""；limit=not_a_number | 只破坏 limit |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 风险评分 | entan.risk.list | GET | /entan/v1/risk | level?；limit? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.risk.list | API-01134、01135、01136、01137、01138 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 1 个 title「风险评分」在功能点列出现，且有 1 条主流程（功能项=主流程）
- [x] 有参接口：sampleRequest 全参 + 省略 level + 省略 limit；每参数 1 条非法反向（不写缺省反向）
- [x] unavailable 仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 无鉴权 / Token / 401 / 424 / 契约占位 / 纯 HTTP 4xx 预期
- [x] 无对应 Lxx，不按 field_key 拆用例；`coverage-fp.md` 已同步 API-01134～01138
- [x] 编号使用父控闭区间 API-01134～01138；本子任务不改 code-registry

**统计**：用例 **5** 条（主流程 1、备选 2、反向 2）；编号闭区间 **API-01134**～**API-01138**（父控 R2-批3 分配）。
