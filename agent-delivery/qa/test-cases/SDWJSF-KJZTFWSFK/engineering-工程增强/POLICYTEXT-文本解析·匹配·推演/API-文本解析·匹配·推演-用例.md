# 智能服务集群-科技专题服务算法库测试用例（文本解析 · 匹配 · 推演 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：工程增强 / 文本解析 · 匹配 · 推演  
> **catalog**：`entry_id=policy.text` · `catalog_page_id=policy.text` · path `/policy/text`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/policy.json` · 页 `policy.text`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` catalog_skip `policy.text`，原因：parse/match/simulate 合页；60 条无独立六级；不改 work）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批11）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 文本解析 | policy.text.parse |
| 2 | 政策匹配 | policy.text.match |
| 3 | 效果推演 | policy.text.simulate |

三个接口 `status=unavailable`，仍按 catalog 的 `sampleRequest` / `sampleResponse` 编写。主路径取 `sampleRequest`；每个可选参数再写 1 条与 sample 相反的传或不传；每个参数再写 1 条非法反向。不做全组合。

**文本解析** sampleRequest 仅 `limit=20`（不传 `policy_id`）。`policy_id` 文档 example 为 `POL_SZ_IC`。

**政策匹配** sampleRequest 为 `subject_type=enterprise`、`limit=20`（不传 `subject_id`）。`subject_id` 的 example 为空串，描述示例为 `E0001`；与 sample 相反的「传」取 `E0001`。`subject_type` 合法选项含空串、`enterprise`、`user`。

**效果推演** sampleRequest 为 `scope_code=440000`、`limit=20`（不传 `scenario_id`）。`scenario_id` 的 example 为空串（全部情景）；与 sample 相反的「传」取选项值 `sc_support_up_20`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01446**～**API-01464**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.text`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01446 | 工程增强 | 文本解析 · 匹配 · 推演 | 主流程 | — | 文本解析 · 匹配 · 推演 | 文本解析 | 文本解析按文档 sampleRequest 仅传 limit=20、不传 policy_id 返回解析列表字段 | 1、limit 使用文档示例 20；不传 policy_id | 1.GET /policy/v1/policy/text/parse，查询参数取组合 PARSE-01 | 1、返回 body 的 data 为数组；2、元素含 title（string，responseFields 政策标题）；3、sampleResponse 还含 policy_id（string）、elements（string 数组）；4、示例首条 policy_id=POL_SZ_IC、title=深圳市加快集成电路产业发展若干措施、elements 为补贴、流片、人才；5、次条 policy_id=POL_GD_AI、title=广东省推动人工智能产业发展行动方案、elements 为算力、模型 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | M_POLICY_DS_11_POLICY_EVAL_012 | INTEG | | | endpoint_id=policy.text.parse catalog_page_id=policy.text 组合=PARSE-01 金样 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01447 | 工程增强 | 文本解析 · 匹配 · 推演 | 备选-参数组合 | 传入 policy_id | 文本解析 · 匹配 · 推演 | 文本解析 | 文本解析传入可选 policy_id=POL_SZ_IC、并传 limit=20 返回解析字段 | 1、policy_id 使用文档示例 POL_SZ_IC；limit=20 | 1.GET /policy/v1/policy/text/parse，查询参数取组合 PARSE-02 | 1、返回 body 的 data 为数组；2、元素含 title（string，responseFields 政策标题）、policy_id（string）、elements（string 数组）；3、结构与 sampleResponse 同类：示例含 policy_id=POL_SZ_IC、title=深圳市加快集成电路产业发展若干措施、elements 为补贴、流片、人才，以及 policy_id=POL_GD_AI、title=广东省推动人工智能产业发展行动方案、elements 为算力、模型 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | M_POLICY_DS_11_POLICY_EVAL_012 | INTEG | | | endpoint_id=policy.text.parse catalog_page_id=policy.text 组合=PARSE-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01448 | 工程增强 | 文本解析 · 匹配 · 推演 | 备选-参数组合 | 省略 limit | 文本解析 · 匹配 · 推演 | 文本解析 | 文本解析省略可选 limit、不传 policy_id 返回解析列表字段 | 1、不传 limit；不传 policy_id | 1.GET /policy/v1/policy/text/parse，查询参数取组合 PARSE-03 | 1、返回 body 的 data 为数组；2、元素仍含 title（string，responseFields 政策标题）、policy_id（string）、elements（string 数组）；3、结构与 sampleResponse 同类：示例含 policy_id=POL_SZ_IC、title=深圳市加快集成电路产业发展若干措施、elements 为补贴、流片、人才，以及 policy_id=POL_GD_AI、title=广东省推动人工智能产业发展行动方案、elements 为算力、模型 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | M_POLICY_DS_11_POLICY_EVAL_012 | INTEG | | | endpoint_id=policy.text.parse catalog_page_id=policy.text 组合=PARSE-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01449 | 工程增强 | 文本解析 · 匹配 · 推演 | 异常-入参-非法policy_id | — | 文本解析 · 匹配 · 推演 | 文本解析 | 文本解析 policy_id 取非法值、limit 保持文档合法 | 1、limit=20 保持文档合法值 | 1.GET /policy/v1/policy/text/parse，查询参数取组合 PARSE-04 | 1、返回 body 的 message 或 msg 指出 policy_id 非法；2、不返回含 title、policy_id 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | | INTEG | | | endpoint_id=policy.text.parse catalog_page_id=policy.text 组合=PARSE-04 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01450 | 工程增强 | 文本解析 · 匹配 · 推演 | 异常-入参-非法limit | — | 文本解析 · 匹配 · 推演 | 文本解析 | 文本解析 limit 取非整数非法值、不传 policy_id | 1、不传 policy_id | 1.GET /policy/v1/policy/text/parse，查询参数取组合 PARSE-05 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 title 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | | INTEG | | | endpoint_id=policy.text.parse catalog_page_id=policy.text 组合=PARSE-05 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01451 | 工程增强 | 文本解析 · 匹配 · 推演 | 主流程 | — | 文本解析 · 匹配 · 推演 | 政策匹配 | 政策匹配按文档 sampleRequest 传 subject_type=enterprise、limit=20、不传 subject_id 返回匹配字段 | 1、subject_type 使用文档示例 enterprise；limit=20；不传 subject_id | 1.GET /policy/v1/policy/match，查询参数取组合 MATCH-01 | 1、返回 body 的 data 为数组；2、元素含 match_score（number，responseFields 匹配度）；3、sampleResponse 还含 rank_no（number）、subject_name（string）、policy_title（string）、reason（string）；4、示例首条 rank_no=1、subject_name=华为技术有限公司、policy_title=深圳市加快集成电路产业发展若干措施、match_score=0.86、reason=产业关键词命中；5、次条 rank_no=2、subject_name=鹏城实验室、policy_title=广东省推动人工智能产业发展行动方案、match_score=0.79、reason=算力与模型条款 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | | INTEG | | | endpoint_id=policy.text.match catalog_page_id=policy.text 组合=MATCH-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01452 | 工程增强 | 文本解析 · 匹配 · 推演 | 备选-参数组合 | 传入 subject_id | 文本解析 · 匹配 · 推演 | 政策匹配 | 政策匹配传入可选 subject_id=E0001，subject_type 与 limit 保持 sampleRequest | 1、subject_id 取描述示例 E0001；subject_type=enterprise；limit=20 | 1.GET /policy/v1/policy/match，查询参数取组合 MATCH-02 | 1、返回 body 的 data 为数组；2、元素含 match_score（number，responseFields 匹配度）、rank_no（number）、subject_name（string）、policy_title（string）、reason（string）；3、结构与 sampleResponse 同类：示例含 rank_no=1、subject_name=华为技术有限公司、policy_title=深圳市加快集成电路产业发展若干措施、match_score=0.86、reason=产业关键词命中，以及 rank_no=2、subject_name=鹏城实验室、policy_title=广东省推动人工智能产业发展行动方案、match_score=0.79、reason=算力与模型条款 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | | INTEG | | | endpoint_id=policy.text.match catalog_page_id=policy.text 组合=MATCH-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01453 | 工程增强 | 文本解析 · 匹配 · 推演 | 备选-参数组合 | 省略 subject_type | 文本解析 · 匹配 · 推演 | 政策匹配 | 政策匹配省略可选 subject_type、保留 limit=20、不传 subject_id | 1、limit=20；不传 subject_type；不传 subject_id | 1.GET /policy/v1/policy/match，查询参数取组合 MATCH-03 | 1、返回 body 的 data 为数组；2、元素仍含 match_score（number，responseFields 匹配度）、rank_no（number）、subject_name（string）、policy_title（string）、reason（string）；3、结构与 sampleResponse 同类：示例含 rank_no=1、subject_name=华为技术有限公司、policy_title=深圳市加快集成电路产业发展若干措施、match_score=0.86、reason=产业关键词命中，以及 rank_no=2、subject_name=鹏城实验室、policy_title=广东省推动人工智能产业发展行动方案、match_score=0.79、reason=算力与模型条款 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | | INTEG | | | endpoint_id=policy.text.match catalog_page_id=policy.text 组合=MATCH-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01454 | 工程增强 | 文本解析 · 匹配 · 推演 | 备选-参数组合 | 省略 limit | 文本解析 · 匹配 · 推演 | 政策匹配 | 政策匹配省略可选 limit、保留 subject_type=enterprise、不传 subject_id | 1、subject_type=enterprise；不传 limit；不传 subject_id | 1.GET /policy/v1/policy/match，查询参数取组合 MATCH-04 | 1、返回 body 的 data 为数组；2、元素仍含 match_score（number，responseFields 匹配度）、rank_no（number）、subject_name（string）、policy_title（string）、reason（string）；3、结构与 sampleResponse 同类：示例含 rank_no=1、subject_name=华为技术有限公司、policy_title=深圳市加快集成电路产业发展若干措施、match_score=0.86、reason=产业关键词命中，以及 rank_no=2、subject_name=鹏城实验室、policy_title=广东省推动人工智能产业发展行动方案、match_score=0.79、reason=算力与模型条款 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | | INTEG | | | endpoint_id=policy.text.match catalog_page_id=policy.text 组合=MATCH-04 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01455 | 工程增强 | 文本解析 · 匹配 · 推演 | 异常-入参-非法subject_id | — | 文本解析 · 匹配 · 推演 | 政策匹配 | 政策匹配 subject_id 取非法值，subject_type 与 limit 保持合法 | 1、subject_type=enterprise；limit=20 | 1.GET /policy/v1/policy/match，查询参数取组合 MATCH-05 | 1、返回 body 的 message 或 msg 指出 subject_id 非法；2、不返回含 match_score 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | | INTEG | | | endpoint_id=policy.text.match catalog_page_id=policy.text 组合=MATCH-05 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01456 | 工程增强 | 文本解析 · 匹配 · 推演 | 异常-入参-非法subject_type | — | 文本解析 · 匹配 · 推演 | 政策匹配 | 政策匹配 subject_type 取枚举外非法值，limit 保持合法 | 1、limit=20；不传 subject_id | 1.GET /policy/v1/policy/match，查询参数取组合 MATCH-06 | 1、返回 body 的 message 或 msg 指出 subject_type 非法；2、不返回含 match_score 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | | INTEG | | | endpoint_id=policy.text.match catalog_page_id=policy.text 组合=MATCH-06 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01457 | 工程增强 | 文本解析 · 匹配 · 推演 | 异常-入参-非法limit | — | 文本解析 · 匹配 · 推演 | 政策匹配 | 政策匹配 limit 取非整数非法值，subject_type 保持文档合法 | 1、subject_type=enterprise；不传 subject_id | 1.GET /policy/v1/policy/match，查询参数取组合 MATCH-07 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 match_score 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | | INTEG | | | endpoint_id=policy.text.match catalog_page_id=policy.text 组合=MATCH-07 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01458 | 工程增强 | 文本解析 · 匹配 · 推演 | 主流程 | — | 文本解析 · 匹配 · 推演 | 效果推演 | 效果推演按文档 sampleRequest 传 scope_code=440000、limit=20、不传 scenario_id 返回推演字段 | 1、scope_code 使用文档示例 440000；limit=20；不传 scenario_id | 1.GET /policy/v1/policy/simulate，查询参数取组合 SIM-01 | 1、返回 body 的 data 为数组；2、元素含 simulated_value（number，responseFields 推演值）；3、sampleResponse 还含 scope_code（string）、scenario_id（string）、baseline_value（number）、curve（数组）；4、curve 元素含 step（string）、value（number）；5、示例首条 scope_code=440300、scenario_id=补贴上调、baseline_value=72、simulated_value=81.4，curve 为 step=基线且 value=72、step=推演且 value=81.4；6、次条 scope_code=440000、scenario_id=人才安居、baseline_value=68.2、simulated_value=74.1，curve 为 step=基线且 value=68.2、step=推演且 value=74.1 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | M_POLICY_DS_11_POLICY_EVAL_015 | INTEG | | | endpoint_id=policy.text.simulate catalog_page_id=policy.text 组合=SIM-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01459 | 工程增强 | 文本解析 · 匹配 · 推演 | 备选-参数组合 | 省略 scope_code | 文本解析 · 匹配 · 推演 | 效果推演 | 效果推演省略可选 scope_code、保留 limit=20、不传 scenario_id | 1、limit=20；不传 scope_code；不传 scenario_id | 1.GET /policy/v1/policy/simulate，查询参数取组合 SIM-02 | 1、返回 body 的 data 为数组；2、元素仍含 simulated_value（number，responseFields 推演值）、scope_code（string）、scenario_id（string）、baseline_value（number）、curve（数组，元素含 step string、value number）；3、结构与 sampleResponse 同类：示例含 scope_code=440300、scenario_id=补贴上调、baseline_value=72、simulated_value=81.4、curve step=基线/value=72 与 step=推演/value=81.4，以及 scope_code=440000、scenario_id=人才安居、baseline_value=68.2、simulated_value=74.1、curve step=基线/value=68.2 与 step=推演/value=74.1 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | M_POLICY_DS_11_POLICY_EVAL_015 | INTEG | | | endpoint_id=policy.text.simulate catalog_page_id=policy.text 组合=SIM-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01460 | 工程增强 | 文本解析 · 匹配 · 推演 | 备选-参数组合 | 传入 scenario_id | 文本解析 · 匹配 · 推演 | 效果推演 | 效果推演传入可选 scenario_id=sc_support_up_20，scope_code 与 limit 保持 sampleRequest | 1、scenario_id 取选项 sc_support_up_20；scope_code=440000；limit=20 | 1.GET /policy/v1/policy/simulate，查询参数取组合 SIM-03 | 1、返回 body 的 data 为数组；2、元素仍含 simulated_value（number，responseFields 推演值）、scope_code（string）、scenario_id（string）、baseline_value（number）、curve（数组，元素含 step string、value number）；3、结构与 sampleResponse 同类：示例含 scope_code=440300、scenario_id=补贴上调、baseline_value=72、simulated_value=81.4、curve step=基线/value=72 与 step=推演/value=81.4，以及 scope_code=440000、scenario_id=人才安居、baseline_value=68.2、simulated_value=74.1、curve step=基线/value=68.2 与 step=推演/value=74.1 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | M_POLICY_DS_11_POLICY_EVAL_015 | INTEG | | | endpoint_id=policy.text.simulate catalog_page_id=policy.text 组合=SIM-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01461 | 工程增强 | 文本解析 · 匹配 · 推演 | 备选-参数组合 | 省略 limit | 文本解析 · 匹配 · 推演 | 效果推演 | 效果推演省略可选 limit、保留 scope_code=440000、不传 scenario_id | 1、scope_code=440000；不传 limit；不传 scenario_id | 1.GET /policy/v1/policy/simulate，查询参数取组合 SIM-04 | 1、返回 body 的 data 为数组；2、元素仍含 simulated_value（number，responseFields 推演值）、scope_code（string）、scenario_id（string）、baseline_value（number）、curve（数组，元素含 step string、value number）；3、结构与 sampleResponse 同类：示例含 scope_code=440300、scenario_id=补贴上调、baseline_value=72、simulated_value=81.4、curve step=基线/value=72 与 step=推演/value=81.4，以及 scope_code=440000、scenario_id=人才安居、baseline_value=68.2、simulated_value=74.1、curve step=基线/value=68.2 与 step=推演/value=74.1 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | M_POLICY_DS_11_POLICY_EVAL_015 | INTEG | | | endpoint_id=policy.text.simulate catalog_page_id=policy.text 组合=SIM-04 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01462 | 工程增强 | 文本解析 · 匹配 · 推演 | 异常-入参-非法scope_code | — | 文本解析 · 匹配 · 推演 | 效果推演 | 效果推演 scope_code 取非法值，limit 保持文档合法 | 1、limit=20；不传 scenario_id | 1.GET /policy/v1/policy/simulate，查询参数取组合 SIM-05 | 1、返回 body 的 message 或 msg 指出 scope_code 非法；2、不返回含 simulated_value 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | | INTEG | | | endpoint_id=policy.text.simulate catalog_page_id=policy.text 组合=SIM-05 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01463 | 工程增强 | 文本解析 · 匹配 · 推演 | 异常-入参-非法scenario_id | — | 文本解析 · 匹配 · 推演 | 效果推演 | 效果推演 scenario_id 取枚举外非法值，scope_code 与 limit 保持合法 | 1、scope_code=440000；limit=20 | 1.GET /policy/v1/policy/simulate，查询参数取组合 SIM-06 | 1、返回 body 的 message 或 msg 指出 scenario_id 非法；2、不返回含 simulated_value 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | | INTEG | | | endpoint_id=policy.text.simulate catalog_page_id=policy.text 组合=SIM-06 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01464 | 工程增强 | 文本解析 · 匹配 · 推演 | 异常-入参-非法limit | — | 文本解析 · 匹配 · 推演 | 效果推演 | 效果推演 limit 取非整数非法值，scope_code 保持文档合法 | 1、scope_code=440000；不传 scenario_id | 1.GET /policy/v1/policy/simulate，查询参数取组合 SIM-07 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 simulated_value 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | | INTEG | | | endpoint_id=policy.text.simulate catalog_page_id=policy.text 组合=SIM-07 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| PARSE-01 | policy.text.parse | 不传 policy_id；limit=20 | 主路径（sampleRequest） |
| PARSE-02 | policy.text.parse | policy_id=POL_SZ_IC；limit=20 | 传入 sample 未带的可选 policy_id |
| PARSE-03 | policy.text.parse | 不传 policy_id；不传 limit | 省略 sample 已带的可选 limit |
| PARSE-04 | policy.text.parse | policy_id=__invalid__；limit=20 | 只破坏 policy_id |
| PARSE-05 | policy.text.parse | 不传 policy_id；limit=not_a_number | 只破坏 limit |
| MATCH-01 | policy.text.match | 不传 subject_id；subject_type=enterprise；limit=20 | 主路径（sampleRequest） |
| MATCH-02 | policy.text.match | subject_id=E0001；subject_type=enterprise；limit=20 | 传入 sample 未带的可选 subject_id（example 为空串，取描述示例 E0001） |
| MATCH-03 | policy.text.match | 不传 subject_id；不传 subject_type；limit=20 | 省略 sample 已带的可选 subject_type |
| MATCH-04 | policy.text.match | 不传 subject_id；subject_type=enterprise；不传 limit | 省略 sample 已带的可选 limit |
| MATCH-05 | policy.text.match | subject_id=__invalid__；subject_type=enterprise；limit=20 | 只破坏 subject_id |
| MATCH-06 | policy.text.match | 不传 subject_id；subject_type=__invalid_type__；limit=20 | 只破坏 subject_type（枚举外） |
| MATCH-07 | policy.text.match | 不传 subject_id；subject_type=enterprise；limit=not_a_number | 只破坏 limit |
| SIM-01 | policy.text.simulate | scope_code=440000；不传 scenario_id；limit=20 | 主路径（sampleRequest） |
| SIM-02 | policy.text.simulate | 不传 scope_code；不传 scenario_id；limit=20 | 省略 sample 已带的可选 scope_code |
| SIM-03 | policy.text.simulate | scope_code=440000；scenario_id=sc_support_up_20；limit=20 | 传入 sample 未带的可选 scenario_id（example 为空串，取选项 sc_support_up_20） |
| SIM-04 | policy.text.simulate | scope_code=440000；不传 scenario_id；不传 limit | 省略 sample 已带的可选 limit |
| SIM-05 | policy.text.simulate | scope_code=__invalid__；不传 scenario_id；limit=20 | 只破坏 scope_code |
| SIM-06 | policy.text.simulate | scope_code=440000；scenario_id=__invalid_scenario__；limit=20 | 只破坏 scenario_id（枚举外） |
| SIM-07 | policy.text.simulate | scope_code=440000；不传 scenario_id；limit=not_a_number | 只破坏 limit |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 文本解析 | policy.text.parse | GET | /policy/v1/policy/text/parse | policy_id?；limit? | unavailable |
| 政策匹配 | policy.text.match | GET | /policy/v1/policy/match | subject_id?；subject_type?；limit? | unavailable |
| 效果推演 | policy.text.simulate | GET | /policy/v1/policy/simulate | scope_code?；scenario_id?；limit? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.text.parse | API-01446、01447、01448、01449、01450 |
| policy.text.match | API-01451、01452、01453、01454、01455、01456、01457 |
| policy.text.simulate | API-01458、01459、01460、01461、01462、01463、01464 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 3 个 title（文本解析、政策匹配、效果推演）均在功能点列出现，且各有 1 条主流程（功能项=主流程）
- [x] 有参接口：sampleRequest 主路径 + 每个可选参数与 sample 相反的传/不传 1 条；每个参数恰好 1 条非法反向；无全组合
- [x] unavailable 三个接口仍按 catalog sampleResponse 逐字段写正向预期，备注注明未交付
- [x] 反向预期写 message 或 msg 指出该参数非法，并写明不返回成功业务字段
- [x] 无鉴权 / Token / 401 / 424 / 契约占位 / 纯 HTTP 4xx 预期
- [x] 无对应 Lxx，不按 field_key 拆用例；`coverage-fp.md` 已同步 API-01446～01464
- [x] 编号使用父控闭区间 API-01446～01464，未复用 00001～00888；本子任务不改 code-registry

**统计**：用例 **19** 条（主流程 3、备选 8、反向 8）；编号闭区间 **API-01446**～**API-01464**（父控 R2-批11 分配）。
