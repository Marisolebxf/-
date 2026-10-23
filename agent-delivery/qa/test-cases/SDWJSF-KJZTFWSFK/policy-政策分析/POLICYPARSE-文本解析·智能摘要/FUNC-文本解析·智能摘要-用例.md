# 智能服务集群-科技专题服务算法库测试用例（文本解析 · 智能摘要 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=policy.parse` · `catalog_page_id=policy.parse` · path `#/policy/parse`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/policy.json` · 页 `policy.parse`  
> **A 线对照**：**无对应 Lxx**（`_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.parse`，原因：不扩六级；不改 `work/`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批11）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 文本解析 | policy.parse.main | unavailable |
| 2 | 政策文本解析 | policy.parse.m_policy_text_parse | available |

两个接口的可选参数都是 `policy_id`、`limit`。`sampleRequest` 只含 `limit=20`，不含 `policy_id`。主流程对齐该 sample；备选各 1 条与 sample 相反（传入 `policy_id=P1`、省略 `limit`）。传入 `policy_id` 的合法值取该接口 sampleResponse 示例 `P1`。第二接口 path 按 catalog 原文为 `/policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute`。`文本解析` 为 unavailable，仍按文档返回体编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00681**～**FUNC-00692**，共 **12** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.parse`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00681 | 算法工具库 | 科技专题服务算法库 | 政策文本解析与智能摘要 | 智能摘要 | 文本解析 · 智能摘要 | 文本解析 | 验证文本解析功能，检查填写 sampleRequest 所示参数 不传 policy_id、limit=20 查询后返回解析字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 policy_id；limit=20（对齐 sampleRequest） | 1.侧栏进入「政策分析」→「文本解析 · 智能摘要」；2.切换至「算法测试」tab；3.接口下拉选择「文本解析」；4.不传 policy_id，填写 limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 policy_id（string，sampleResponse 示例 P1）、title（string，示例 示例政策）、summary（string，responseFields 摘要，示例 摘要）、metric_id（string，示例 M_POLICY_TEXT_PARSE）；3、结构与 sampleResponse 一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | M_POLICY_DS_11_POLICY_EVAL_012 | INTEG |  | FUNC-00681 | endpoint_id=policy.parse.main catalog_page_id=policy.parse 组合=PAR-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00682 | 算法工具库 | 科技专题服务算法库 | 政策文本解析与智能摘要 | 智能摘要 | 文本解析 · 智能摘要 | 文本解析 | 验证文本解析功能，检查传入可选 policy_id、limit 保持 sampleRequest 的 20 时仍返回解析字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、policy_id=P1；limit=20 | 1.侧栏进入「政策分析」→「文本解析 · 智能摘要」；2.切换至「算法测试」tab；3.接口下拉选择「文本解析」；4.填写 policy_id=P1、limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 policy_id（string，sampleResponse 示例 P1）、title（string，示例 示例政策）、summary（string，responseFields 摘要，示例 摘要）、metric_id（string，示例 M_POLICY_TEXT_PARSE）；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | M_POLICY_DS_11_POLICY_EVAL_012 | INTEG |  | FUNC-00682 | endpoint_id=policy.parse.main catalog_page_id=policy.parse 组合=PAR-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00683 | 算法工具库 | 科技专题服务算法库 | 政策文本解析与智能摘要 | 智能摘要 | 文本解析 · 智能摘要 | 文本解析 | 验证文本解析功能，检查不传可选 limit、policy_id 保持 sample 不传时仍返回解析字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 policy_id；不传 limit | 1.侧栏进入「政策分析」→「文本解析 · 智能摘要」；2.切换至「算法测试」tab；3.接口下拉选择「文本解析」；4.不传 policy_id、不传 limit，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 policy_id（string，sampleResponse 示例 P1）、title（string，示例 示例政策）、summary（string，responseFields 摘要，示例 摘要）、metric_id（string，示例 M_POLICY_TEXT_PARSE）；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | M_POLICY_DS_11_POLICY_EVAL_012 | INTEG |  | FUNC-00683 | endpoint_id=policy.parse.main catalog_page_id=policy.parse 组合=PAR-03 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00684 | 算法工具库 | 科技专题服务算法库 | 政策文本解析与智能摘要 | 智能摘要 | 文本解析 · 智能摘要 | 文本解析 | 验证文本解析功能，检查 policy_id 非法、limit 保持文档合法值时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit=20 | 1.侧栏进入「政策分析」→「文本解析 · 智能摘要」；2.切换至「算法测试」tab；3.接口下拉选择「文本解析」；4.填写 policy_id=__invalid__、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 policy_id 非法；2、不返回含 summary 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse |  | INTEG |  | FUNC-00684 | endpoint_id=policy.parse.main catalog_page_id=policy.parse 组合=PAR-04 场景=异常-入参-非法policy_id catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00685 | 算法工具库 | 科技专题服务算法库 | 政策文本解析与智能摘要 | 智能摘要 | 文本解析 · 智能摘要 | 文本解析 | 验证文本解析功能，检查 limit 非法、policy_id 保持 sample 不传时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 policy_id | 1.侧栏进入「政策分析」→「文本解析 · 智能摘要」；2.切换至「算法测试」tab；3.接口下拉选择「文本解析」；4.不传 policy_id，填写 limit=-1，点击调用 | 1、返回面板的 message 或 msg 指出 limit 非法；2、不返回含 summary 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse |  | INTEG |  | FUNC-00685 | endpoint_id=policy.parse.main catalog_page_id=policy.parse 组合=PAR-05 场景=异常-入参-非法limit catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00686 | 算法工具库 | 科技专题服务算法库 | 政策文本解析与智能摘要 | 智能摘要 | 文本解析 · 智能摘要 | 政策文本解析 | 验证政策文本解析功能，检查填写 sampleRequest 所示参数 提交 limit=20、不传 policy_id 后返回解析字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 policy_id；limit=20（对齐 sampleRequest） | 1.侧栏进入「政策分析」→「文本解析 · 智能摘要」；2.切换至「算法测试」tab；3.接口下拉选择「政策文本解析」；4.不传 policy_id，填写 limit=20，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，示例 M_POLICY_TEXT_PARSE）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 同层另列 summary（string，摘要），sampleResponse 未给该字段的示例值 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute | M_POLICY_TEXT_PARSE | INTEG |  | FUNC-00686 | endpoint_id=policy.parse.m_policy_text_parse catalog_page_id=policy.parse 组合=MTP-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00687 | 算法工具库 | 科技专题服务算法库 | 政策文本解析与智能摘要 | 智能摘要 | 文本解析 · 智能摘要 | 政策文本解析 | 验证政策文本解析功能，检查传入可选 policy_id、limit 保持 sampleRequest 的 20 时仍返回解析字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、policy_id=P1；limit=20 | 1.侧栏进入「政策分析」→「文本解析 · 智能摘要」；2.切换至「算法测试」tab；3.接口下拉选择「政策文本解析」；4.填写 policy_id=P1、limit=20，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，示例 M_POLICY_TEXT_PARSE）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 同层另列 summary（string，摘要），sampleResponse 未给该字段的示例值 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute | M_POLICY_TEXT_PARSE | INTEG |  | FUNC-00687 | endpoint_id=policy.parse.m_policy_text_parse catalog_page_id=policy.parse 组合=MTP-02 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00688 | 算法工具库 | 科技专题服务算法库 | 政策文本解析与智能摘要 | 智能摘要 | 文本解析 · 智能摘要 | 政策文本解析 | 验证政策文本解析功能，检查不传可选 limit、policy_id 保持 sample 不传时仍返回解析字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 policy_id；不传 limit | 1.侧栏进入「政策分析」→「文本解析 · 智能摘要」；2.切换至「算法测试」tab；3.接口下拉选择「政策文本解析」；4.不传 policy_id、不传 limit，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，示例 M_POLICY_TEXT_PARSE）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 同层另列 summary（string，摘要），sampleResponse 未给该字段的示例值 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute | M_POLICY_TEXT_PARSE | INTEG |  | FUNC-00688 | endpoint_id=policy.parse.m_policy_text_parse catalog_page_id=policy.parse 组合=MTP-03 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00689 | 算法工具库 | 科技专题服务算法库 | 政策文本解析与智能摘要 | 智能摘要 | 文本解析 · 智能摘要 | 政策文本解析 | 验证政策文本解析功能，检查 policy_id 非法、limit 保持文档合法值时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit=20 | 1.侧栏进入「政策分析」→「文本解析 · 智能摘要」；2.切换至「算法测试」tab；3.接口下拉选择「政策文本解析」；4.填写 policy_id=__invalid__、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 policy_id 非法；2、不返回含 summary 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute |  | INTEG |  | FUNC-00689 | endpoint_id=policy.parse.m_policy_text_parse catalog_page_id=policy.parse 组合=MTP-04 场景=异常-入参-非法policy_id catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00690 | 算法工具库 | 科技专题服务算法库 | 政策文本解析与智能摘要 | 智能摘要 | 文本解析 · 智能摘要 | 政策文本解析 | 验证政策文本解析功能，检查 limit 非法、policy_id 保持 sample 不传时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 policy_id | 1.侧栏进入「政策分析」→「文本解析 · 智能摘要」；2.切换至「算法测试」tab；3.接口下拉选择「政策文本解析」；4.不传 policy_id，填写 limit=-1，点击调用 | 1、返回面板的 message 或 msg 指出 limit 非法；2、不返回含 summary 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute |  | INTEG |  | FUNC-00690 | endpoint_id=policy.parse.m_policy_text_parse catalog_page_id=policy.parse 组合=MTP-05 场景=异常-入参-非法limit catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00691 | 算法工具库 | 科技专题服务算法库 | 政策文本解析与智能摘要 | 智能摘要 | 文本解析 · 智能摘要 | 接口信息 | 验证文本解析 · 智能摘要的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「政策分析」→「文本解析 · 智能摘要」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 2；2、下拉名称与 §0 各 title 一致（文本解析、政策文本解析）；3、默认项概览 method=GET、path=/policy/v1/policy/text/parse；4、切换后概览对应政策文本解析 POST /policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00691 | catalog_page_id=policy.parse 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00692 | 算法工具库 | 科技专题服务算法库 | 政策文本解析与智能摘要 | 智能摘要 | 文本解析 · 智能摘要 | 算法测试 | 验证文本解析 · 智能摘要的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「政策分析」→「文本解析 · 智能摘要」；2.切换到「算法测试」tab；3.下拉切换到「政策文本解析」 | 1、算法测试 tab 下拉共 2 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「政策文本解析」；3、调用区 method 为 POST、path 为 /policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute；4、请求区已随所选接口刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00692 | catalog_page_id=policy.parse 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

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
| policy.parse.main | FUNC-00681、00682、00683、00684、00685 |
| policy.parse.m_policy_text_parse | FUNC-00686、00687、00688、00689、00690 |
| （页面清单） | FUNC-00691、00692 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 2 个 title「文本解析」「政策文本解析」均在功能点列出现，且各有 1 条 `场景=主流程`（FUNC-00681、FUNC-00686）
- [x] 每个接口：sample 主流程 1 条；与 sample 相反的传/不传各 1 条备选（传入 policy_id、省略 limit）；每个参数 1 条非法反向
- [x] unavailable（文本解析）仍按 catalog 返回体写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条裸 GET/POST 步骤
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 双接口页清单用例 2 条：预期写明下拉共 2 项且可切换；`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00681～00692
- [x] A 线写无对应 Lxx（catalog_skip）

**统计**：catalog endpoint **2**；title **2**；FUNC 用例 **12** 条；主流程 **2**、备选 **4**、反向 **4**、清单 **2**；编号闭区间 **FUNC-00681**～**FUNC-00692**（R3-批11 policy.parse）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **12** |
| 编号闭区间 | **FUNC-00681**～**FUNC-00692** |
| 接口向（不含清单） | **10** |
| 主流程 | **2** |
| 备选-参数组合 | **4** |
| 反向 | **4** |
| 清单 | **2** |
| 已删 API 册 | `API-文本解析·智能摘要-用例.md`（API-01465～01474 作废，不复用；B 线只保留本 FUNC 册） |
| 鉴权用例 | **0** |
