# 智能服务集群-科技专题服务算法库测试用例（政策文本处理 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：政策分析 / 政策文本处理（catalog `policy.text`；侧栏在「工程增强」）  
> **catalog**：`entry_id=policy.text` · `catalog_page_id=policy.text` · path `#/policy/text`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/policy.json` · 页 `policy.text`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` catalog_skip `policy.text`，原因：parse/match/simulate 合页；60 条无独立六级；不改 work）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批11）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 文本解析 | policy.text.parse | unavailable |
| 2 | 政策匹配 | policy.text.match | unavailable |
| 3 | 效果推演 | policy.text.simulate | unavailable |

三个接口 `status=unavailable`，仍按 catalog 的 `sampleRequest` / `sampleResponse` 编写。主路径取 `sampleRequest`；每个可选参数再写 1 条与 sample 相反的传或不传；每个参数再写 1 条非法反向。不做全组合。

**文本解析** sampleRequest 仅 `limit=20`（不传 `policy_id`）。`policy_id` 文档 example 为 `POL_SZ_IC`。

**政策匹配** sampleRequest 为 `subject_type=enterprise`、`limit=20`（不传 `subject_id`）。`subject_id` 的 example 为空串，描述示例为 `E0001`；与 sample 相反的「传」取 `E0001`。`subject_type` 合法选项含空串、`enterprise`、`user`。

**效果推演** sampleRequest 为 `scope_code=440000`、`limit=20`（不传 `scenario_id`）。`scenario_id` 的 example 为空串（全部情景）；与 sample 相反的「传」取选项值 `sc_support_up_20`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00660**～**FUNC-00680**，共 **21** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.text`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00660 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 文本解析 | 文本解析 · 匹配 · 推演 | 文本解析 | 验证文本解析功能，检查填写 chainId=INB1701只传 limit=20、不传 policy_id 时返回解析列表字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit=20；不传 policy_id | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.切换至「算法测试」tab；3.接口下拉选择「文本解析」；4.不传 policy_id，填写 limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 title（string，responseFields 政策标题）；3、sampleResponse 还含 policy_id（string）、elements（string 数组）；4、示例首条 policy_id=POL_SZ_IC、title=深圳市加快集成电路产业发展若干措施、elements 为补贴、流片、人才；5、次条 policy_id=POL_GD_AI、title=广东省推动人工智能产业发展行动方案、elements 为算力、模型 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | M_POLICY_DS_11_POLICY_EVAL_012 | INTEG |  | FUNC-00660 | endpoint_id=policy.text.parse catalog_page_id=policy.text 组合=PARSE-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00661 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 文本解析 | 文本解析 · 匹配 · 推演 | 文本解析 | 验证文本解析功能，检查传入可选 policy_id=POL_SZ_IC、并传 limit=20 时仍返回解析字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、policy_id=POL_SZ_IC；limit=20 | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.切换至「算法测试」tab；3.接口下拉选择「文本解析」；4.填写 policy_id=POL_SZ_IC、limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 title（string，responseFields 政策标题）、policy_id（string）、elements（string 数组）；3、结构与 sampleResponse 同类：示例含 policy_id=POL_SZ_IC、title=深圳市加快集成电路产业发展若干措施、elements 为补贴、流片、人才，以及 policy_id=POL_GD_AI、title=广东省推动人工智能产业发展行动方案、elements 为算力、模型 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | M_POLICY_DS_11_POLICY_EVAL_012 | INTEG |  | FUNC-00661 | endpoint_id=policy.text.parse catalog_page_id=policy.text 组合=PARSE-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00662 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 文本解析 | 文本解析 · 匹配 · 推演 | 文本解析 | 验证文本解析功能，检查省略可选 limit、不传 policy_id 时仍返回解析列表字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 limit；不传 policy_id | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.切换至「算法测试」tab；3.接口下拉选择「文本解析」；4.不传 policy_id、不传 limit，点击调用 | 1、返回面板 body 的 data 为数组；2、元素仍含 title（string，responseFields 政策标题）、policy_id（string）、elements（string 数组）；3、结构与 sampleResponse 同类：示例含 policy_id=POL_SZ_IC、title=深圳市加快集成电路产业发展若干措施、elements 为补贴、流片、人才，以及 policy_id=POL_GD_AI、title=广东省推动人工智能产业发展行动方案、elements 为算力、模型 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | M_POLICY_DS_11_POLICY_EVAL_012 | INTEG |  | FUNC-00662 | endpoint_id=policy.text.parse catalog_page_id=policy.text 组合=PARSE-03 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00663 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 文本解析 | 文本解析 · 匹配 · 推演 | 文本解析 | 验证文本解析功能，检查 policy_id 非法、limit 保持文档合法值 20 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit=20 | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.切换至「算法测试」tab；3.接口下拉选择「文本解析」；4.填写 policy_id=__invalid__、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 policy_id 非法；2、不返回含 title、policy_id 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse |  | INTEG |  | FUNC-00663 | endpoint_id=policy.text.parse catalog_page_id=policy.text 组合=PARSE-04 场景=异常-入参-非法policy_id catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00664 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 文本解析 | 文本解析 · 匹配 · 推演 | 文本解析 | 验证文本解析功能，检查 limit 非法、不传 policy_id 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 policy_id | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.切换至「算法测试」tab；3.接口下拉选择「文本解析」；4.不传 policy_id，填写 limit=not_a_number，点击调用 | 1、返回面板的 message 或 msg 指出 limit 非法；2、不返回含 title 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse |  | INTEG |  | FUNC-00664 | endpoint_id=policy.text.parse catalog_page_id=policy.text 组合=PARSE-05 场景=异常-入参-非法limit catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00665 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 政策匹配 | 文本解析 · 匹配 · 推演 | 政策匹配 | 验证政策匹配功能，检查填写 sampleRequest 所示参数 传 subject_type=enterprise、limit=20、不传 subject_id 时返回匹配字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、subject_type=enterprise；limit=20；不传 subject_id | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配」；4.不传 subject_id，填写 subject_type=enterprise、limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 match_score（number，responseFields 匹配度）；3、sampleResponse 还含 rank_no（number）、subject_name（string）、policy_title（string）、reason（string）；4、示例首条 rank_no=1、subject_name=华为技术有限公司、policy_title=深圳市加快集成电路产业发展若干措施、match_score=0.86、reason=产业关键词命中；5、次条 rank_no=2、subject_name=鹏城实验室、policy_title=广东省推动人工智能产业发展行动方案、match_score=0.79、reason=算力与模型条款 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match |  | INTEG |  | FUNC-00665 | endpoint_id=policy.text.match catalog_page_id=policy.text 组合=MATCH-01 场景=主流程 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00666 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 政策匹配 | 文本解析 · 匹配 · 推演 | 政策匹配 | 验证政策匹配功能，检查传入可选 subject_id=E0001，subject_type 与 limit 保持 sampleRequest 时仍返回匹配字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、subject_id=E0001；subject_type=enterprise；limit=20 | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配」；4.填写 subject_id=E0001、subject_type=enterprise、limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 match_score（number，responseFields 匹配度）、rank_no（number）、subject_name（string）、policy_title（string）、reason（string）；3、结构与 sampleResponse 同类：示例含 rank_no=1、subject_name=华为技术有限公司、policy_title=深圳市加快集成电路产业发展若干措施、match_score=0.86、reason=产业关键词命中，以及 rank_no=2、subject_name=鹏城实验室、policy_title=广东省推动人工智能产业发展行动方案、match_score=0.79、reason=算力与模型条款 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match |  | INTEG |  | FUNC-00666 | endpoint_id=policy.text.match catalog_page_id=policy.text 组合=MATCH-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00667 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 政策匹配 | 文本解析 · 匹配 · 推演 | 政策匹配 | 验证政策匹配功能，检查省略可选 subject_type、保留 limit=20、不传 subject_id 时仍返回匹配字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit=20；不传 subject_type；不传 subject_id | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配」；4.不传 subject_id、不传 subject_type，填写 limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素仍含 match_score（number，responseFields 匹配度）、rank_no（number）、subject_name（string）、policy_title（string）、reason（string）；3、结构与 sampleResponse 同类：示例含 rank_no=1、subject_name=华为技术有限公司、policy_title=深圳市加快集成电路产业发展若干措施、match_score=0.86、reason=产业关键词命中，以及 rank_no=2、subject_name=鹏城实验室、policy_title=广东省推动人工智能产业发展行动方案、match_score=0.79、reason=算力与模型条款 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match |  | INTEG |  | FUNC-00667 | endpoint_id=policy.text.match catalog_page_id=policy.text 组合=MATCH-03 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00668 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 政策匹配 | 文本解析 · 匹配 · 推演 | 政策匹配 | 验证政策匹配功能，检查省略可选 limit、保留 subject_type=enterprise、不传 subject_id 时仍返回匹配字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、subject_type=enterprise；不传 limit；不传 subject_id | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配」；4.不传 subject_id、不传 limit，填写 subject_type=enterprise，点击调用 | 1、返回面板 body 的 data 为数组；2、元素仍含 match_score（number，responseFields 匹配度）、rank_no（number）、subject_name（string）、policy_title（string）、reason（string）；3、结构与 sampleResponse 同类：示例含 rank_no=1、subject_name=华为技术有限公司、policy_title=深圳市加快集成电路产业发展若干措施、match_score=0.86、reason=产业关键词命中，以及 rank_no=2、subject_name=鹏城实验室、policy_title=广东省推动人工智能产业发展行动方案、match_score=0.79、reason=算力与模型条款 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match |  | INTEG |  | FUNC-00668 | endpoint_id=policy.text.match catalog_page_id=policy.text 组合=MATCH-04 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00669 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 政策匹配 | 文本解析 · 匹配 · 推演 | 政策匹配 | 验证政策匹配功能，检查 subject_id 非法、subject_type 与 limit 保持合法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、subject_type=enterprise；limit=20 | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配」；4.填写 subject_id=__invalid__、subject_type=enterprise、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 subject_id 非法；2、不返回含 match_score 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match |  | INTEG |  | FUNC-00669 | endpoint_id=policy.text.match catalog_page_id=policy.text 组合=MATCH-05 场景=异常-入参-非法subject_id catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00670 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 政策匹配 | 文本解析 · 匹配 · 推演 | 政策匹配 | 验证政策匹配功能，检查 subject_type 枚举外非法、limit 保持合法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit=20；不传 subject_id | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配」；4.不传 subject_id，填写 subject_type=__invalid_type__、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 subject_type 非法；2、不返回含 match_score 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match |  | INTEG |  | FUNC-00670 | endpoint_id=policy.text.match catalog_page_id=policy.text 组合=MATCH-06 场景=异常-入参-非法subject_type catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00671 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 政策匹配 | 文本解析 · 匹配 · 推演 | 政策匹配 | 验证政策匹配功能，检查 limit 非法、subject_type 保持文档合法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、subject_type=enterprise；不传 subject_id | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配」；4.不传 subject_id，填写 subject_type=enterprise、limit=not_a_number，点击调用 | 1、返回面板的 message 或 msg 指出 limit 非法；2、不返回含 match_score 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match |  | INTEG |  | FUNC-00671 | endpoint_id=policy.text.match catalog_page_id=policy.text 组合=MATCH-07 场景=异常-入参-非法limit catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00672 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 效果推演 | 文本解析 · 匹配 · 推演 | 效果推演 | 验证效果推演功能，检查填写 sampleRequest 所示参数 传 scope_code=440000、limit=20、不传 scenario_id 时返回推演字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、scope_code=440000；limit=20；不传 scenario_id | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.切换至「算法测试」tab；3.接口下拉选择「效果推演」；4.不传 scenario_id，填写 scope_code=440000、limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 simulated_value（number，responseFields 推演值）；3、sampleResponse 还含 scope_code（string）、scenario_id（string）、baseline_value（number）、curve（数组）；4、curve 元素含 step（string）、value（number）；5、示例首条 scope_code=440300、scenario_id=补贴上调、baseline_value=72、simulated_value=81.4，curve 为 step=基线且 value=72、step=推演且 value=81.4；6、次条 scope_code=440000、scenario_id=人才安居、baseline_value=68.2、simulated_value=74.1，curve 为 step=基线且 value=68.2、step=推演且 value=74.1 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | M_POLICY_DS_11_POLICY_EVAL_015 | INTEG |  | FUNC-00672 | endpoint_id=policy.text.simulate catalog_page_id=policy.text 组合=SIM-01 场景=主流程 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00673 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 效果推演 | 文本解析 · 匹配 · 推演 | 效果推演 | 验证效果推演功能，检查省略可选 scope_code、保留 limit=20、不传 scenario_id 时仍返回推演字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit=20；不传 scope_code；不传 scenario_id | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.切换至「算法测试」tab；3.接口下拉选择「效果推演」；4.不传 scope_code、不传 scenario_id，填写 limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素仍含 simulated_value（number，responseFields 推演值）、scope_code（string）、scenario_id（string）、baseline_value（number）、curve（数组，元素含 step string、value number）；3、结构与 sampleResponse 同类：示例含 scope_code=440300、scenario_id=补贴上调、baseline_value=72、simulated_value=81.4、curve step=基线/value=72 与 step=推演/value=81.4，以及 scope_code=440000、scenario_id=人才安居、baseline_value=68.2、simulated_value=74.1、curve step=基线/value=68.2 与 step=推演/value=74.1 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | M_POLICY_DS_11_POLICY_EVAL_015 | INTEG |  | FUNC-00673 | endpoint_id=policy.text.simulate catalog_page_id=policy.text 组合=SIM-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00674 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 效果推演 | 文本解析 · 匹配 · 推演 | 效果推演 | 验证效果推演功能，检查传入可选 scenario_id=sc_support_up_20，scope_code 与 limit 保持 sampleRequest 时仍返回推演字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、scenario_id=sc_support_up_20；scope_code=440000；limit=20 | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.切换至「算法测试」tab；3.接口下拉选择「效果推演」；4.填写 scope_code=440000、scenario_id=sc_support_up_20、limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素仍含 simulated_value（number，responseFields 推演值）、scope_code（string）、scenario_id（string）、baseline_value（number）、curve（数组，元素含 step string、value number）；3、结构与 sampleResponse 同类：示例含 scope_code=440300、scenario_id=补贴上调、baseline_value=72、simulated_value=81.4、curve step=基线/value=72 与 step=推演/value=81.4，以及 scope_code=440000、scenario_id=人才安居、baseline_value=68.2、simulated_value=74.1、curve step=基线/value=68.2 与 step=推演/value=74.1 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | M_POLICY_DS_11_POLICY_EVAL_015 | INTEG |  | FUNC-00674 | endpoint_id=policy.text.simulate catalog_page_id=policy.text 组合=SIM-03 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00675 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 效果推演 | 文本解析 · 匹配 · 推演 | 效果推演 | 验证效果推演功能，检查省略可选 limit、保留 scope_code=440000、不传 scenario_id 时仍返回推演字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、scope_code=440000；不传 limit；不传 scenario_id | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.切换至「算法测试」tab；3.接口下拉选择「效果推演」；4.不传 scenario_id、不传 limit，填写 scope_code=440000，点击调用 | 1、返回面板 body 的 data 为数组；2、元素仍含 simulated_value（number，responseFields 推演值）、scope_code（string）、scenario_id（string）、baseline_value（number）、curve（数组，元素含 step string、value number）；3、结构与 sampleResponse 同类：示例含 scope_code=440300、scenario_id=补贴上调、baseline_value=72、simulated_value=81.4、curve step=基线/value=72 与 step=推演/value=81.4，以及 scope_code=440000、scenario_id=人才安居、baseline_value=68.2、simulated_value=74.1、curve step=基线/value=68.2 与 step=推演/value=74.1 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | M_POLICY_DS_11_POLICY_EVAL_015 | INTEG |  | FUNC-00675 | endpoint_id=policy.text.simulate catalog_page_id=policy.text 组合=SIM-04 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00676 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 效果推演 | 文本解析 · 匹配 · 推演 | 效果推演 | 验证效果推演功能，检查 scope_code 非法、limit 保持文档合法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit=20；不传 scenario_id | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.切换至「算法测试」tab；3.接口下拉选择「效果推演」；4.不传 scenario_id，填写 scope_code=__invalid__、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 scope_code 非法；2、不返回含 simulated_value 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate |  | INTEG |  | FUNC-00676 | endpoint_id=policy.text.simulate catalog_page_id=policy.text 组合=SIM-05 场景=异常-入参-非法scope_code catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00677 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 效果推演 | 文本解析 · 匹配 · 推演 | 效果推演 | 验证效果推演功能，检查 scenario_id 枚举外非法、scope_code 与 limit 保持合法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、scope_code=440000；limit=20 | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.切换至「算法测试」tab；3.接口下拉选择「效果推演」；4.填写 scope_code=440000、scenario_id=__invalid_scenario__、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 scenario_id 非法；2、不返回含 simulated_value 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate |  | INTEG |  | FUNC-00677 | endpoint_id=policy.text.simulate catalog_page_id=policy.text 组合=SIM-06 场景=异常-入参-非法scenario_id catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00678 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 效果推演 | 文本解析 · 匹配 · 推演 | 效果推演 | 验证效果推演功能，检查 limit 非法、scope_code 保持文档合法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、scope_code=440000；不传 scenario_id | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.切换至「算法测试」tab；3.接口下拉选择「效果推演」；4.不传 scenario_id，填写 scope_code=440000、limit=not_a_number，点击调用 | 1、返回面板的 message 或 msg 指出 limit 非法；2、不返回含 simulated_value 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate |  | INTEG |  | FUNC-00678 | endpoint_id=policy.text.simulate catalog_page_id=policy.text 组合=SIM-07 场景=异常-入参-非法limit catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00679 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 政策文本处理 | 文本解析 · 匹配 · 推演 | 接口信息 | 验证政策文本处理的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 3；2、下拉名称与 §0 各 title 一致；3、默认项概览 method、path 对应文本解析 GET /policy/v1/policy/text/parse；4、切换后概览对应政策匹配 GET /policy/v1/policy/match、效果推演 GET /policy/v1/policy/simulate，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00679 | catalog_page_id=policy.text 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00680 | 算法工具库 | 科技专题服务算法库 | 政策文本处理 | 政策文本处理 | 文本解析 · 匹配 · 推演 | 算法测试 | 验证政策文本处理的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「工程增强」→「文本解析 · 匹配 · 推演」；2.切换到「算法测试」tab；3.下拉切换到「效果推演」 | 1、算法测试 tab 下拉共 3 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「效果推演」；3、调用区 method 为 GET、path 为 /policy/v1/policy/simulate；4、请求区已随所选接口刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00680 | catalog_page_id=policy.text 场景=算法测试-清单 |
---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| PARSE-01 | policy.text.parse | 不传 policy_id；limit=20 | 主路径（sampleRequest） |
| PARSE-02 | policy.text.parse | policy_id=POL_SZ_IC；limit=20 | 传入 sample 未带的可选 policy_id |
| PARSE-03 | policy.text.parse | 不传 policy_id；不传 limit | 省略 sample 已带的可选 limit |
| PARSE-04 | policy.text.parse | policy_id=__invalid__；limit=20 | 只破坏 policy_id |
| PARSE-05 | policy.text.parse | 不传 policy_id；limit=not_a_number | 只破坏 limit |
| MATCH-01 | policy.text.match | 不传 subject_id；subject_type=enterprise；limit=20 | 主路径（sampleRequest） |
| MATCH-02 | policy.text.match | subject_id=E0001；subject_type=enterprise；limit=20 | 传入 sample 未带的可选 subject_id |
| MATCH-03 | policy.text.match | 不传 subject_id；不传 subject_type；limit=20 | 省略 sample 已带的可选 subject_type |
| MATCH-04 | policy.text.match | 不传 subject_id；subject_type=enterprise；不传 limit | 省略 sample 已带的可选 limit |
| MATCH-05 | policy.text.match | subject_id=__invalid__；subject_type=enterprise；limit=20 | 只破坏 subject_id |
| MATCH-06 | policy.text.match | 不传 subject_id；subject_type=__invalid_type__；limit=20 | 只破坏 subject_type |
| MATCH-07 | policy.text.match | 不传 subject_id；subject_type=enterprise；limit=not_a_number | 只破坏 limit |
| SIM-01 | policy.text.simulate | scope_code=440000；不传 scenario_id；limit=20 | 主路径（sampleRequest） |
| SIM-02 | policy.text.simulate | 不传 scope_code；不传 scenario_id；limit=20 | 省略 sample 已带的可选 scope_code |
| SIM-03 | policy.text.simulate | scope_code=440000；scenario_id=sc_support_up_20；limit=20 | 传入 sample 未带的可选 scenario_id |
| SIM-04 | policy.text.simulate | scope_code=440000；不传 scenario_id；不传 limit | 省略 sample 已带的可选 limit |
| SIM-05 | policy.text.simulate | scope_code=__invalid__；不传 scenario_id；limit=20 | 只破坏 scope_code |
| SIM-06 | policy.text.simulate | scope_code=440000；scenario_id=__invalid_scenario__；limit=20 | 只破坏 scenario_id |
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
| policy.text.parse | FUNC-00660、00661、00662、00663、00664 |
| policy.text.match | FUNC-00665、00666、00667、00668、00669、00670、00671 |
| policy.text.simulate | FUNC-00672、00673、00674、00675、00676、00677、00678 |
| （页面清单） | FUNC-00679、00680 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 3 个 title（文本解析、政策匹配、效果推演）均在功能点列出现，且各有 1 条 `场景=主流程`（FUNC-00660、00665、00672）
- [x] 有参接口：sampleRequest 主路径 + 每个可选参数与 sample 相反的传/不传 1 条；每个参数恰好 1 条非法反向；无全组合
- [x] unavailable 三接口仍按 catalog sampleResponse 写正向预期，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条裸 GET/POST 步骤
- [x] 无对应 Lxx：五级/六级按 catalog 页「政策文本处理」与 title 填写
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 多接口页清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（含切换步骤）
- [x] `coverage-fp.md` 已同步 FUNC-00660～00680

**统计**：catalog endpoint **3**；title **3**；FUNC 用例 **21** 条；主流程 **3**、备选 **8**、反向 **8**、清单 **2**；编号闭区间 **FUNC-00660**～**FUNC-00680**（R3-批11 policy.text）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **21** |
| 编号闭区间 | **FUNC-00660**～**FUNC-00680** |
| 接口向（不含清单） | **19** |
| 主流程 | **3** |
| 备选-参数组合 | **8** |
| 反向 | **8** |
| 清单 | **2** |
| 对照 API 册 | `engineering-工程增强/POLICYTEXT-文本解析·匹配·推演/API-文本解析·匹配·推演-用例.md`（API-01446～01464；B 线以本 FUNC 册为准） |
| 鉴权用例 | **0** |
