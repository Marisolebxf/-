# 智能服务集群-科技专题服务算法库测试用例（政策匹配推送 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：政策分析 / 匹配推送  
> **catalog**：`entry_id=policy.match` · `catalog_page_id=policy.match` · path `/policy/match`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.match`  
> **A 线对照**：无对应 Lxx。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.match`（不扩六级）。不改 `work/`  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批11）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | status |
|---|------------------------|-------------|--------|--------|
| 1 | 政策匹配 | policy.match.main | GET | unavailable |
| 2 | 政策匹配推送 | policy.match.m_policy_match | POST | available |

两个接口的可选参数相同：`subject_id`、`subject_type`、`limit`。`sampleRequest` 均为 `subject_type=enterprise`、`limit=20`，不含 `subject_id`。备选各动一个参数，与 sample 相反：传入 `subject_id=E0001`（参数说明示例）、不传 `subject_type`、不传 `limit`。反向各 1 条非法，不把省略写成反向。GET 走查询参数；POST 走 JSON 请求体。`政策匹配` 的 path 为 `/policy/v1/policy/match`；`政策匹配推送` 的 path 按 catalog 原文为 `/policy/v1/polan/metric/M_POLICY_MATCH/compute`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01475**～**API-01488**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.match`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01475 | 政策分析 | 匹配推送 | 主流程 | — | 匹配推送 | 政策匹配 | 政策匹配按文档 sampleRequest 传 subject_type=enterprise、limit=20、不传 subject_id | 1、subject_type=enterprise；limit=20；不传 subject_id | 1.GET /policy/v1/policy/match，查询参数取组合 MAT-01 | 1、返回 body 的 data 为数组；2、元素含 rank_no（number）、subject_name（string）、policy_title（string）、match_score（number，responseFields 匹配分）、metric_id（string）；3、与 sampleResponse 逐字段一致，示例第1条 rank_no=1、subject_name=示例企业、policy_title=示例政策、match_score=75、metric_id=M_POLICY_MATCH | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | M_POLICY_MATCH | INTEG | | | endpoint_id=policy.match.main catalog_page_id=policy.match 组合=MAT-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01476 | 政策分析 | 匹配推送 | 备选-参数组合 | 传入 subject_id | 匹配推送 | 政策匹配 | 政策匹配传入可选 subject_id=E0001，subject_type 与 limit 保持 sample | 1、subject_id=E0001；subject_type=enterprise；limit=20 | 1.GET /policy/v1/policy/match，查询参数取组合 MAT-02 | 1、返回 body 的 data 为数组；2、元素仍含 rank_no（number）、subject_name（string）、policy_title（string）、match_score（number，responseFields 匹配分）、metric_id（string）；3、字段与 sampleResponse 逐字段同类，示例值（如 rank_no=1、subject_name=示例企业、policy_title=示例政策、match_score=75、metric_id=M_POLICY_MATCH）说明形态 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | M_POLICY_MATCH | INTEG | | | endpoint_id=policy.match.main catalog_page_id=policy.match 组合=MAT-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01477 | 政策分析 | 匹配推送 | 备选-参数组合 | 省略 subject_type | 匹配推送 | 政策匹配 | 政策匹配不传可选 subject_type，limit 保持 sample 的 20、不传 subject_id | 1、不传 subject_id；不传 subject_type；limit=20 | 1.GET /policy/v1/policy/match，查询参数取组合 MAT-03 | 1、返回 body 的 data 为数组；2、元素仍含 rank_no（number）、subject_name（string）、policy_title（string）、match_score（number，responseFields 匹配分）、metric_id（string）；3、字段与 sampleResponse 逐字段同类，示例值（如 match_score=75、subject_name=示例企业、policy_title=示例政策）说明形态 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | M_POLICY_MATCH | INTEG | | | endpoint_id=policy.match.main catalog_page_id=policy.match 组合=MAT-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01478 | 政策分析 | 匹配推送 | 备选-参数组合 | 省略 limit | 匹配推送 | 政策匹配 | 政策匹配不传可选 limit，subject_type 保持 sample 的 enterprise、不传 subject_id | 1、不传 subject_id；subject_type=enterprise；不传 limit | 1.GET /policy/v1/policy/match，查询参数取组合 MAT-04 | 1、返回 body 的 data 为数组；2、元素仍含 rank_no（number）、subject_name（string）、policy_title（string）、match_score（number，responseFields 匹配分）、metric_id（string）；3、字段与 sampleResponse 逐字段同类，示例值（如 match_score=75、rank_no=1、metric_id=M_POLICY_MATCH）说明形态 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | M_POLICY_MATCH | INTEG | | | endpoint_id=policy.match.main catalog_page_id=policy.match 组合=MAT-04 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01479 | 政策分析 | 匹配推送 | 异常-入参-非法subject_id | — | 匹配推送 | 政策匹配 | 政策匹配 subject_id 非法，其余保持 sample | 1、subject_type=enterprise；limit=20 | 1.GET /policy/v1/policy/match，查询参数取组合 MAT-05 | 1、返回 body 的 message 或 msg 指出 subject_id 非法；2、不返回含 match_score 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | | INTEG | | | endpoint_id=policy.match.main catalog_page_id=policy.match 组合=MAT-05 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01480 | 政策分析 | 匹配推送 | 异常-入参-非法subject_type | — | 匹配推送 | 政策匹配 | 政策匹配 subject_type 非法，其余保持 sample | 1、不传 subject_id；limit=20 | 1.GET /policy/v1/policy/match，查询参数取组合 MAT-06 | 1、返回 body 的 message 或 msg 指出 subject_type 非法；2、不返回含 match_score 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | | INTEG | | | endpoint_id=policy.match.main catalog_page_id=policy.match 组合=MAT-06 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01481 | 政策分析 | 匹配推送 | 异常-入参-非法limit | — | 匹配推送 | 政策匹配 | 政策匹配 limit 非法，其余保持 sample | 1、不传 subject_id；subject_type=enterprise | 1.GET /policy/v1/policy/match，查询参数取组合 MAT-07 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 match_score 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | | INTEG | | | endpoint_id=policy.match.main catalog_page_id=policy.match 组合=MAT-07 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01482 | 政策分析 | 匹配推送 | 主流程 | — | 匹配推送 | 政策匹配推送 | 政策匹配推送按文档 sampleRequest 传 subject_type=enterprise、limit=20、不传 subject_id | 1、请求体 subject_type=enterprise；limit=20；不传 subject_id | 1.POST /policy/v1/polan/metric/M_POLICY_MATCH/compute，请求体取组合 PSH-01 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，示例 M_POLICY_MATCH）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 另含 match_score（number，匹配分） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_MATCH/compute | M_POLICY_MATCH | INTEG | | | endpoint_id=policy.match.m_policy_match catalog_page_id=policy.match 组合=PSH-01 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01483 | 政策分析 | 匹配推送 | 备选-参数组合 | 传入 subject_id | 匹配推送 | 政策匹配推送 | 政策匹配推送传入可选 subject_id=E0001，subject_type 与 limit 保持 sample | 1、请求体 subject_id=E0001；subject_type=enterprise；limit=20 | 1.POST /policy/v1/polan/metric/M_POLICY_MATCH/compute，请求体取组合 PSH-02 | 1、返回 body 为对象；2、仍含 metric_id（string，示例 M_POLICY_MATCH）、hint（string，示例 真实 compute 响应,以实际调用为准）；3、responseFields 的 match_score 为 number（匹配分） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_MATCH/compute | M_POLICY_MATCH | INTEG | | | endpoint_id=policy.match.m_policy_match catalog_page_id=policy.match 组合=PSH-02 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01484 | 政策分析 | 匹配推送 | 备选-参数组合 | 省略 subject_type | 匹配推送 | 政策匹配推送 | 政策匹配推送不传可选 subject_type，limit 保持 sample 的 20、不传 subject_id | 1、请求体不传 subject_id；不传 subject_type；limit=20 | 1.POST /policy/v1/polan/metric/M_POLICY_MATCH/compute，请求体取组合 PSH-03 | 1、返回 body 为对象；2、仍含 metric_id（string，示例 M_POLICY_MATCH）、hint（string，示例 真实 compute 响应,以实际调用为准）；3、responseFields 的 match_score 为 number（匹配分） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_MATCH/compute | M_POLICY_MATCH | INTEG | | | endpoint_id=policy.match.m_policy_match catalog_page_id=policy.match 组合=PSH-03 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01485 | 政策分析 | 匹配推送 | 备选-参数组合 | 省略 limit | 匹配推送 | 政策匹配推送 | 政策匹配推送不传可选 limit，subject_type 保持 sample 的 enterprise、不传 subject_id | 1、请求体不传 subject_id；subject_type=enterprise；不传 limit | 1.POST /policy/v1/polan/metric/M_POLICY_MATCH/compute，请求体取组合 PSH-04 | 1、返回 body 为对象；2、仍含 metric_id（string，示例 M_POLICY_MATCH）、hint（string，示例 真实 compute 响应,以实际调用为准）；3、responseFields 的 match_score 为 number（匹配分） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_MATCH/compute | M_POLICY_MATCH | INTEG | | | endpoint_id=policy.match.m_policy_match catalog_page_id=policy.match 组合=PSH-04 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01486 | 政策分析 | 匹配推送 | 异常-入参-非法subject_id | — | 匹配推送 | 政策匹配推送 | 政策匹配推送 subject_id 非法，其余保持 sample | 1、请求体 subject_type=enterprise；limit=20 | 1.POST /policy/v1/polan/metric/M_POLICY_MATCH/compute，请求体取组合 PSH-05 | 1、返回 body 的 message 或 msg 指出 subject_id 非法；2、不返回含 metric_id 或 match_score 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_MATCH/compute | | INTEG | | | endpoint_id=policy.match.m_policy_match catalog_page_id=policy.match 组合=PSH-05 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01487 | 政策分析 | 匹配推送 | 异常-入参-非法subject_type | — | 匹配推送 | 政策匹配推送 | 政策匹配推送 subject_type 非法，其余保持 sample | 1、请求体不传 subject_id；limit=20 | 1.POST /policy/v1/polan/metric/M_POLICY_MATCH/compute，请求体取组合 PSH-06 | 1、返回 body 的 message 或 msg 指出 subject_type 非法；2、不返回含 metric_id 或 match_score 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_MATCH/compute | | INTEG | | | endpoint_id=policy.match.m_policy_match catalog_page_id=policy.match 组合=PSH-06 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01488 | 政策分析 | 匹配推送 | 异常-入参-非法limit | — | 匹配推送 | 政策匹配推送 | 政策匹配推送 limit 非法，其余保持 sample | 1、请求体不传 subject_id；subject_type=enterprise | 1.POST /policy/v1/polan/metric/M_POLICY_MATCH/compute，请求体取组合 PSH-07 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 metric_id 或 match_score 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_MATCH/compute | | INTEG | | | endpoint_id=policy.match.m_policy_match catalog_page_id=policy.match 组合=PSH-07 catalog_status=available |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| MAT-01 | policy.match.main | subject_type=enterprise；不传 subject_id；limit=20 | 主路径（sampleRequest）；查询参数 |
| MAT-02 | policy.match.main | subject_id=E0001；subject_type=enterprise；limit=20 | 传入可选 subject_id（sample 不含 subject_id；E0001 取参数说明示例） |
| MAT-03 | policy.match.main | 不传 subject_id；不传 subject_type；limit=20 | 省略可选 subject_type（sample 含 subject_type） |
| MAT-04 | policy.match.main | 不传 subject_id；subject_type=enterprise；不传 limit | 省略可选 limit（sample 含 limit） |
| MAT-05 | policy.match.main | subject_id=__invalid__；subject_type=enterprise；limit=20 | 只破坏 subject_id |
| MAT-06 | policy.match.main | 不传 subject_id；subject_type=__invalid__（不在空、enterprise、user）；limit=20 | 只破坏 subject_type |
| MAT-07 | policy.match.main | 不传 subject_id；subject_type=enterprise；limit=-1 | 只破坏 limit |
| PSH-01 | policy.match.m_policy_match | subject_type=enterprise；不传 subject_id；limit=20 | 主路径（sampleRequest）；JSON 请求体 |
| PSH-02 | policy.match.m_policy_match | subject_id=E0001；subject_type=enterprise；limit=20 | 传入可选 subject_id（sample 不含 subject_id；E0001 取参数说明示例） |
| PSH-03 | policy.match.m_policy_match | 不传 subject_id；不传 subject_type；limit=20 | 省略可选 subject_type（sample 含 subject_type） |
| PSH-04 | policy.match.m_policy_match | 不传 subject_id；subject_type=enterprise；不传 limit | 省略可选 limit（sample 含 limit） |
| PSH-05 | policy.match.m_policy_match | subject_id=__invalid__；subject_type=enterprise；limit=20 | 只破坏 subject_id |
| PSH-06 | policy.match.m_policy_match | 不传 subject_id；subject_type=__invalid__（不在空、enterprise、user）；limit=20 | 只破坏 subject_type |
| PSH-07 | policy.match.m_policy_match | 不传 subject_id；subject_type=enterprise；limit=-1 | 只破坏 limit |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 政策匹配 | policy.match.main | GET | /policy/v1/policy/match | subject_id?；subject_type?；limit? | unavailable |
| 政策匹配推送 | policy.match.m_policy_match | POST | /policy/v1/polan/metric/M_POLICY_MATCH/compute | subject_id?；subject_type?；limit? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.match.main | API-01475、01476、01477、01478、01479、01480、01481 |
| policy.match.m_policy_match | API-01482、01483、01484、01485、01486、01487、01488 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title「政策匹配」「政策匹配推送」均在功能点列出现，且各有 1 条主流程（API-01475、API-01482）
- [x] 与 sample 相反的传/不传各 1 条备选：传入 subject_id（01476、01483）、省略 subject_type（01477、01484）、省略 limit（01478、01485）
- [x] 每个参数恰好 1 条非法反向（01479～01481、01486～01488）；省略未写成反向
- [x] unavailable 的「政策匹配」仍按 sampleResponse 写主流程与备选返回字段，备注注明文档标记未交付
- [x] 反向预期写 message 或 msg 指出该参数非法
- [x] `coverage-fp.md` 已同步 API-01475～01488；A 线写无对应 Lxx

**统计**：接口 **2**；用例 **14** 条（主流程 2、备选 6、反向 6）；编号闭区间 **API-01475**～**API-01488**（父控 R2-批11 分配，连续用满）。
