# 智能服务集群-科技专题服务算法库测试用例（风险洞察（异步） API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：创新监测 / 风险洞察（异步）  
> **catalog**：`entry_id=innov.risk` · `catalog_page_id=innov.risk` · path `/innov/risk`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.risk`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`，原因：创新监测不在本轮 60 六级；不改 work）  
> **环境**：联调台 50897（本册不写登录、不试调）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批20）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | path | 参数 | 条数 |
|---|------------------------|-------------|--------|------|------|------|
| 1 | 供应链风险图谱契约 | innov.risk.supply | POST | （空） | sub_type* | 2 |
| 2 | 发展痛难点契约 | innov.risk.pain | POST | （空） | sub_type* | 2 |

两个 title 的 catalog `status=unavailable`，`path` 均为空字符串。步骤只写「path 为空」，不臆造 URL。`路由route` 记 `—`。

每个接口只有必填 `sub_type`（string），无其它参数。主流程跟 `sampleRequest`：供应链 `sub_type=supply_chain`，痛难点 `sub_type=pain_points`。反向恰好 1 条：省略 `sub_type`（请求体 `{}`）。不另写非法值，不写备选。备注注明文档标记未交付，正向预期仍按该接口 sampleResponse 逐字段写。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01894`～`01897`（闭区间用满，不复用 00001～00888）。`路由route` = path（本页为空，记 `—`）；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.risk`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01894 | 创新监测 | 风险洞察（异步） | 主流程 | — | 风险洞察（异步） | 供应链风险图谱契约 | 供应链风险图谱契约按文档 sampleRequest 传 sub_type=supply_chain | 1、sub_type 使用文档示例 supply_chain | 1.POST（path 为空），请求体取组合 SUP-01 | 1、返回 body 与 sampleResponse 同层逐字段：summary.display_mode（string，示例 graph）、summary.data_time（string，示例 2026-07-30）、summary.enterprises（string 数组，示例 智芯科技、绿能装备）；2、nodes 为数组，元素含 id（string）、name（string）、relation_type（string）、influence_score（number）、is_key（boolean），示例 N1/智芯科技/core/86/true、N2/关键芯片供应商/supply/74/true；3、edges 为数组，元素含 src（string）、dst（string）、relation_type（string），示例 src=N2、dst=N1、relation_type=supply；4、key_nodes 为数组（responseFields 关键节点），元素含 name（string）、relation_type（string）、influence_score（number）、is_key（boolean）、suggestion（string），示例 关键芯片供应商/supply/74/true/备选供应商不足；5、break_risks 为数组（responseFields 断链风险），元素含 name（string）、risk_level（string）、impact（string）、suggestion（string），示例 关键芯片供应商/高/核心器件断供/引入第二货源 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.risk.supply catalog_page_id=innov.risk 组合=SUP-01 金样 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01895 | 创新监测 | 风险洞察（异步） | 异常-入参-缺sub_type | — | 风险洞察（异步） | 供应链风险图谱契约 | 供应链风险图谱契约不传必填 sub_type | 1、请求体不传 sub_type | 1.POST（path 为空），请求体取组合 SUP-02 | 1、返回 body 的 message 或 msg 指出 sub_type 缺失或非法；2、不返回含 key_nodes 或 break_risks 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.risk.supply catalog_page_id=innov.risk 组合=SUP-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01896 | 创新监测 | 风险洞察（异步） | 主流程 | — | 风险洞察（异步） | 发展痛难点契约 | 发展痛难点契约按文档 sampleRequest 传 sub_type=pain_points | 1、sub_type 使用文档示例 pain_points | 1.POST（path 为空），请求体取组合 PAIN-01 | 1、返回 body 与 sampleResponse 同层逐字段：summary.diagnosis_method（string，示例 四维共性）、summary.data_time（string，示例 2026-07-30）；2、dimension_cards 为数组，元素含 dimension（string）、priority（string）、issue_count（number）、affected_enterprise_count（number），示例 tech_rd/高/3/4、financing/中/2/3；3、issues 为数组（responseFields 共性问题），元素含 title（string）、priority（string）、dimension（string）、affected_enterprise_count（number）、evidence（string），示例 高端人才招聘难/高/tech_rd/4/研发岗位空缺率高、融资渠道单一/中/financing/3/银行贷款占比过高 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.risk.pain catalog_page_id=innov.risk 组合=PAIN-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01897 | 创新监测 | 风险洞察（异步） | 异常-入参-缺sub_type | — | 风险洞察（异步） | 发展痛难点契约 | 发展痛难点契约不传必填 sub_type | 1、请求体不传 sub_type | 1.POST（path 为空），请求体取组合 PAIN-02 | 1、返回 body 的 message 或 msg 指出 sub_type 缺失或非法；2、不返回含 issues 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.risk.pain catalog_page_id=innov.risk 组合=PAIN-02 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| SUP-01 | innov.risk.supply | sub_type=supply_chain | 主路径（sampleRequest） |
| SUP-02 | innov.risk.supply | 不传 sub_type（请求体 {}） | 缺必填 sub_type |
| PAIN-01 | innov.risk.pain | sub_type=pain_points | 主路径（sampleRequest） |
| PAIN-02 | innov.risk.pain | 不传 sub_type（请求体 {}） | 缺必填 sub_type |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 供应链风险图谱契约 | innov.risk.supply | POST | （空） | sub_type* | unavailable |
| 发展痛难点契约 | innov.risk.pain | POST | （空） | sub_type* | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.risk.supply | API-01894、01895 |
| innov.risk.pain | API-01896、01897 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title（供应链风险图谱契约、发展痛难点契约）均在功能点列出现，且各有 1 条主流程
- [x] 主流程跟 sampleRequest：supply_chain、pain_points
- [x] 无其它参数，无备选；每个接口反向恰好 1 条，只省略 sub_type，不另写非法值
- [x] 正向预期逐字段写出 sampleResponse（含 responseFields 未单列、但示例里出现的 summary、nodes、edges、dimension_cards）；反向预期为 message 或 msg 指出 sub_type 缺失或非法
- [x] path 为空，步骤未臆造 URL；unavailable 备注注明文档标记未交付
- [x] 无登录 / Token / 401 / 424 / 只写 HTTP 4xx 的预期
- [x] A 线无对应 Lxx；未改 work
- [x] `coverage-fp.md` 已同步 API-01894～01897
- [ ] `code-registry.yaml` 由父控回写（本子任务不改注册表）

**统计**：用例 **4** 条；主流程 **2**、备选 **0**、反向 **2**；编号闭区间 **API-01894**～**API-01897**（父控 R2-批20 分配）。
