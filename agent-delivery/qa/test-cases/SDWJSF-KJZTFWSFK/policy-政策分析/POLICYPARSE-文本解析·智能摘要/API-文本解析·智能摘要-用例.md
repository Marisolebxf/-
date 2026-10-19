# 智能服务集群-科技专题服务算法库测试用例（文本解析 · 智能摘要 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：政策分析 / 文本解析 · 智能摘要  
> **catalog**：`entry_id=policy.parse` · `catalog_page_id=policy.parse` · path `/policy/parse`  
> **A 线对照**：**无对应 Lxx**（`_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.parse`，原因：不扩六级；不改 `work/`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批11）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 文本解析 | policy.parse.main |
| 2 | 政策文本解析 | policy.parse.m_policy_text_parse |

两个接口的可选参数都是 `policy_id`、`limit`。`sampleRequest` 只含 `limit=20`，不含 `policy_id`。主流程对齐该 sample；备选各 1 条与 sample 相反（传入 `policy_id`、省略 `limit`）。传入 `policy_id` 的合法值取该接口 sampleResponse 示例 `P1`（`params.example` 为空）。第二接口 path 按 catalog 原文为 `/policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01465**～**API-01474**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.parse`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01465 | 政策分析 | 文本解析 · 智能摘要 | 主流程 | — | 文本解析 · 智能摘要 | 文本解析 | 文本解析按文档 sampleRequest 不传 policy_id、limit=20 查询并返回解析字段 | 1、不传 policy_id；limit=20（对齐 sampleRequest） | 1.GET /policy/v1/policy/text/parse，查询参数取组合 PAR-01 | 1、返回 body 的 data 为数组；2、元素含 policy_id（string，sampleResponse 示例 P1）、title（string，示例 示例政策）、summary（string，responseFields 摘要，示例 摘要）、metric_id（string，示例 M_POLICY_TEXT_PARSE）；3、结构与 sampleResponse 一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | M_POLICY_DS_11_POLICY_EVAL_012 | INTEG | | | endpoint_id=policy.parse.main catalog_page_id=policy.parse 组合=PAR-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01466 | 政策分析 | 文本解析 · 智能摘要 | 备选-参数组合 | 传入 policy_id | 文本解析 · 智能摘要 | 文本解析 | 文本解析传入可选 policy_id，limit 保持 sampleRequest 的 20 | 1、只将 policy_id 改为传入，其余保持 sampleRequest | 1.GET /policy/v1/policy/text/parse，查询参数取组合 PAR-02 | 1、返回 body 的 data 为数组；2、元素含 policy_id（string，sampleResponse 示例 P1）、title（string，示例 示例政策）、summary（string，responseFields 摘要，示例 摘要）、metric_id（string，示例 M_POLICY_TEXT_PARSE）；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | M_POLICY_DS_11_POLICY_EVAL_012 | INTEG | | | endpoint_id=policy.parse.main catalog_page_id=policy.parse 组合=PAR-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01467 | 政策分析 | 文本解析 · 智能摘要 | 备选-参数组合 | 省略 limit | 文本解析 · 智能摘要 | 文本解析 | 文本解析不传可选 limit，policy_id 保持 sample 不传 | 1、只将 limit 改为不传，其余保持 sampleRequest | 1.GET /policy/v1/policy/text/parse，查询参数取组合 PAR-03 | 1、返回 body 的 data 为数组；2、元素含 policy_id（string，sampleResponse 示例 P1）、title（string，示例 示例政策）、summary（string，responseFields 摘要，示例 摘要）、metric_id（string，示例 M_POLICY_TEXT_PARSE）；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | M_POLICY_DS_11_POLICY_EVAL_012 | INTEG | | | endpoint_id=policy.parse.main catalog_page_id=policy.parse 组合=PAR-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01468 | 政策分析 | 文本解析 · 智能摘要 | 异常-入参-非法policy_id | — | 文本解析 · 智能摘要 | 文本解析 | 文本解析 policy_id 非法，limit 保持文档合法值 | 1、只将 policy_id 改为非法值，其余保持 sampleRequest | 1.GET /policy/v1/policy/text/parse，查询参数取组合 PAR-04 | 1、返回 body 的 message 或 msg 指出 policy_id 非法；2、不返回含 summary 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | | INTEG | | | endpoint_id=policy.parse.main catalog_page_id=policy.parse 组合=PAR-04 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01469 | 政策分析 | 文本解析 · 智能摘要 | 异常-入参-非法limit | — | 文本解析 · 智能摘要 | 文本解析 | 文本解析 limit 非法，policy_id 保持 sample 不传 | 1、只将 limit 改为非法值，其余保持 sampleRequest | 1.GET /policy/v1/policy/text/parse，查询参数取组合 PAR-05 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 summary 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | | INTEG | | | endpoint_id=policy.parse.main catalog_page_id=policy.parse 组合=PAR-05 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01470 | 政策分析 | 文本解析 · 智能摘要 | 主流程 | — | 文本解析 · 智能摘要 | 政策文本解析 | 政策文本解析按文档 sampleRequest 提交 limit=20、不传 policy_id 并返回解析字段 | 1、请求体不传 policy_id；limit=20（对齐 sampleRequest） | 1.POST /policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute，请求体取组合 MTP-01 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，示例 M_POLICY_TEXT_PARSE）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 同层另列 summary（string，摘要），sampleResponse 未给该字段的示例值 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute | M_POLICY_TEXT_PARSE | INTEG | | | endpoint_id=policy.parse.m_policy_text_parse catalog_page_id=policy.parse 组合=MTP-01 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01471 | 政策分析 | 文本解析 · 智能摘要 | 备选-参数组合 | 传入 policy_id | 文本解析 · 智能摘要 | 政策文本解析 | 政策文本解析传入可选 policy_id，limit 保持 sampleRequest 的 20 | 1、只将 policy_id 改为传入，其余保持 sampleRequest | 1.POST /policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute，请求体取组合 MTP-02 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，示例 M_POLICY_TEXT_PARSE）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 同层另列 summary（string，摘要），sampleResponse 未给该字段的示例值 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute | M_POLICY_TEXT_PARSE | INTEG | | | endpoint_id=policy.parse.m_policy_text_parse catalog_page_id=policy.parse 组合=MTP-02 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01472 | 政策分析 | 文本解析 · 智能摘要 | 备选-参数组合 | 省略 limit | 文本解析 · 智能摘要 | 政策文本解析 | 政策文本解析不传可选 limit，policy_id 保持 sample 不传 | 1、只将 limit 改为不传，其余保持 sampleRequest | 1.POST /policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute，请求体取组合 MTP-03 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，示例 M_POLICY_TEXT_PARSE）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 同层另列 summary（string，摘要），sampleResponse 未给该字段的示例值 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute | M_POLICY_TEXT_PARSE | INTEG | | | endpoint_id=policy.parse.m_policy_text_parse catalog_page_id=policy.parse 组合=MTP-03 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01473 | 政策分析 | 文本解析 · 智能摘要 | 异常-入参-非法policy_id | — | 文本解析 · 智能摘要 | 政策文本解析 | 政策文本解析 policy_id 非法，limit 保持文档合法值 | 1、只将 policy_id 改为非法值，其余保持 sampleRequest | 1.POST /policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute，请求体取组合 MTP-04 | 1、返回 body 的 message 或 msg 指出 policy_id 非法；2、不返回含 summary 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute | | INTEG | | | endpoint_id=policy.parse.m_policy_text_parse catalog_page_id=policy.parse 组合=MTP-04 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01474 | 政策分析 | 文本解析 · 智能摘要 | 异常-入参-非法limit | — | 文本解析 · 智能摘要 | 政策文本解析 | 政策文本解析 limit 非法，policy_id 保持 sample 不传 | 1、只将 limit 改为非法值，其余保持 sampleRequest | 1.POST /policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute，请求体取组合 MTP-05 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 summary 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute | | INTEG | | | endpoint_id=policy.parse.m_policy_text_parse catalog_page_id=policy.parse 组合=MTP-05 catalog_status=available |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| PAR-01 | policy.parse.main | 不传 policy_id；limit=20 | 主路径（sampleRequest） |
| PAR-02 | policy.parse.main | policy_id=P1；limit=20 | 与 sample 相反：传入可选 policy_id |
| PAR-03 | policy.parse.main | 不传 policy_id；不传 limit | 与 sample 相反：省略可选 limit |
| PAR-04 | policy.parse.main | policy_id=__invalid__；limit=20 | 只破坏 policy_id |
| PAR-05 | policy.parse.main | 不传 policy_id；limit=-1 | 只破坏 limit |
| MTP-01 | policy.parse.m_policy_text_parse | 不传 policy_id；limit=20 | 主路径（sampleRequest） |
| MTP-02 | policy.parse.m_policy_text_parse | policy_id=P1；limit=20 | 与 sample 相反：传入可选 policy_id |
| MTP-03 | policy.parse.m_policy_text_parse | 不传 policy_id；不传 limit | 与 sample 相反：省略可选 limit |
| MTP-04 | policy.parse.m_policy_text_parse | policy_id=__invalid__；limit=20 | 只破坏 policy_id |
| MTP-05 | policy.parse.m_policy_text_parse | 不传 policy_id；limit=-1 | 只破坏 limit |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 文本解析 | policy.parse.main | GET | /policy/v1/policy/text/parse | policy_id?；limit? | unavailable |
| 政策文本解析 | policy.parse.m_policy_text_parse | POST | /policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute | policy_id?；limit? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.parse.main | API-01465、01466、01467、01468、01469 |
| policy.parse.m_policy_text_parse | API-01470、01471、01472、01473、01474 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title「文本解析」「政策文本解析」均在功能点列出现，且各有 1 条主流程（API-01465、API-01470）
- [x] 每个接口：sample 主流程 1 条；与 sample 相反的传/不传各 1 条备选（传入 policy_id、省略 limit）；每个参数 1 条非法反向
- [x] unavailable（文本解析）仍按 catalog 返回体写主流程，备注注明未交付
- [x] 反向预期写 message 或 msg 指出该参数非法
- [x] `coverage-fp.md` 已同步 API-01465～01474；A 线写无对应 Lxx

**统计**：用例 **10** 条（主流程 2、备选 4、反向 4）；编号闭区间 **API-01465**～**API-01474**（父控 R2-批11 分配）。
