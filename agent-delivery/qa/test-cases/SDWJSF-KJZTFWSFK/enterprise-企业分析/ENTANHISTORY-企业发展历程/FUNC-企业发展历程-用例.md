# 智能服务集群-科技专题服务算法库测试用例（企业发展历程 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=entan.history` · `catalog_page_id=entan.history` · path `#/entan/history`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **A 线对照**：`fp-split-by-api-run/work/L28.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批2）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 企业搜索 | entan.history.enterprises | unavailable |
| 2 | 发展历程 | entan.history.timeline | unavailable |

**org_id 试调取值**：文档示例 `0218337e44ca794fee9850cf1627b03b`（`发展历程` params example，执行期可替换）。

本页 2 个接口在 catalog 均为 `status=unavailable`；用例仍按各接口 `sampleRequest` / `sampleResponse` / `responseFields` 编写返回 body 预期，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00108**～**FUNC-00116**，共 **9** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.history`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00108 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业发展历程模型 | 企业发展历程 | 企业搜索 | 验证企业搜索功能，检查填写 chainId=INB1701 keyword 空、limit=1 查询后返回企业列表字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业发展历程」；2.切换至「算法测试」tab；3.接口下拉选择「企业搜索」；4.填写 keyword=（空字符串）、limit=1（catalogsampleRequest），点击调用 | 1、返回面板业务载荷为数组（常见为 data 数组，与网关 envelope 一致）；2、元素含 org_id（string）、enterprise_name（string）；3、sampleResponse 示例 org_id=0218337e44ca794fee9850cf1627b03b、enterprise_name=云启智元科技股份有限公司 说明命中元素形态；4、允许空数组表示无匹配企业 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises |  | INTEG |  | FUNC-00108 | endpoint_id=entan.history.enterprises catalog_page_id=entan.history 组合=ENT-01 场景=主流程 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00109 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业发展历程模型 | 企业发展历程 | 企业搜索 | 验证企业搜索功能，检查 keyword=云启、limit=5 时返回文档列表字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业发展历程」；2.切换至「算法测试」tab；3.接口下拉选择「企业搜索」；4.填写 keyword=云启、limit=5，点击调用 | 1、返回面板业务载荷为数组；2、非空元素含 org_id（string）、enterprise_name（string）；3、字段形态与 sampleResponse 一致；4、空数组仍表示无匹配，不得与入参错误失败态混淆 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises |  | INTEG |  | FUNC-00109 | endpoint_id=entan.history.enterprises catalog_page_id=entan.history 组合=ENT-02 场景=备选-参数组合 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00110 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业发展历程模型 | 企业发展历程 | 企业搜索 | 验证企业搜索功能，检查 limit 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业发展历程」；2.切换至「算法测试」tab；3.接口下拉选择「企业搜索」；4.填写 keyword=测试、limit=-1，点击调用 | 1、返回面板的 message 或 msg 说明 limit 非法、越界或不可解析；2、不返回含可信 org_id/enterprise_name 命中列表的成功业务载荷 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises |  | INTEG |  | FUNC-00110 | endpoint_id=entan.history.enterprises catalog_page_id=entan.history 组合=ENT-03 场景=异常-入参-非法limit catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00111 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业发展历程模型 | 企业发展历程 | 企业搜索 | 验证企业搜索功能，检查 keyword 明显非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业发展历程」；2.切换至「算法测试」tab；3.接口下拉选择「企业搜索」；4.填写 keyword=__invalid__、limit=10，点击调用 | 1、返回面板的 message 或 msg 说明 keyword 非法或不可接受；2、不返回将失败冒充为含 org_id 的成功命中列表 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises |  | INTEG |  | FUNC-00111 | endpoint_id=entan.history.enterprises catalog_page_id=entan.history 组合=ENT-04 场景=异常-入参-非法keyword catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00112 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业发展历程模型 | 企业发展历程 | 发展历程 | 验证发展历程功能，检查填写 chainId=INB1701 org_id 查询后返回时间线字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、org_id 使用 §0 文档示例或环境有效值 | 1.侧栏进入「企业分析」→「企业发展历程」；2.切换至「算法测试」tab；3.接口下拉选择「发展历程」；4.填写 org_id=0218337e44ca794fee9850cf1627b03b（catalogparamsexample，可替换），点击调用 | 1、返回面板业务载荷为对象（常见为 data 对象）；2、含 enterprise_name（string），sampleResponse 示例「云启智元科技股份有限公司」说明形态；3、含 timeline（array，responseFields 事件时间线）；4、timeline 元素含 year（number）、type（string）、title（string）、detail（object），sampleResponse 示例含 type=finance/patent/news 及 detail 内 revenue、patent_apply_count、finance_round 等键说明节点结构；5、timeline 可为空数组（无重大事件空态），与缺 org_id 失败态区分 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/history |  | INTEG |  | FUNC-00112 | endpoint_id=entan.history.timeline catalog_page_id=entan.history 组合=HIS-01 场景=主流程 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00113 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业发展历程模型 | 企业发展历程 | 发展历程 | 验证发展历程功能，检查不传 org_id 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业发展历程」；2.切换至「算法测试」tab；3.接口下拉选择「发展历程」；4.不传 org_id 查询参数，点击调用 | 1、返回面板的 message 或 msg 指出 org_id 缺失或必填；2、不返回含 timeline 数组的成功业务载荷 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/history |  | INTEG |  | FUNC-00113 | endpoint_id=entan.history.timeline catalog_page_id=entan.history 组合=HIS-02 场景=异常-入参-缺org_id catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00114 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业发展历程模型 | 企业发展历程 | 发展历程 | 验证发展历程功能，检查 org_id 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业发展历程」；2.切换至「算法测试」tab；3.接口下拉选择「发展历程」；4.填写 org_id=__invalid__，点击调用 | 1、返回面板的 message 或 msg 说明 org_id 非法或企业不存在；2、不返回将失败冒充为合法 org_id 下空 timeline 成功态 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/history |  | INTEG |  | FUNC-00114 | endpoint_id=entan.history.timeline catalog_page_id=entan.history 组合=HIS-03 场景=异常-入参-非法org_id catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00115 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业发展历程模型 | 企业发展历程 | 接口信息 | 验证企业发展历程的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业发展历程」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 2；2、下拉名称与 §0 各 title 一致（企业搜索、发展历程）；3、默认项概览 method、path 对应企业搜索 GET /entan/v1/enterprises；4、切换后概览对应发展历程 GET /entan/v1/history，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00115 | catalog_page_id=entan.history 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00116 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业发展历程模型 | 企业发展历程 | 算法测试 | 验证企业发展历程的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业发展历程」；2.切换到「算法测试」tab；3.下拉切换到「发展历程」 | 1、算法测试 tab 下拉共 2 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「发展历程」；3、调用区 method 为 GET、path 为 /entan/v1/history；4、请求区已随所选接口刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00116 | catalog_page_id=entan.history 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| ENT-01 | entan.history.enterprises | keyword=（空字符串）；limit=1（catalog sampleRequest） | 主路径全参 |
| ENT-02 | entan.history.enterprises | keyword=云启；limit=5 | keyword+limit 合法组合 |
| ENT-03 | entan.history.enterprises | keyword=测试；limit=-1 | 只破坏 limit |
| ENT-04 | entan.history.enterprises | keyword=__invalid__；limit=10 | 只破坏 keyword |
| HIS-01 | entan.history.timeline | org_id=0218337e44ca794fee9850cf1627b03b（catalog params example，可替换） | 主路径全参 |
| HIS-02 | entan.history.timeline | 不传 org_id 查询参数 | 缺必填 org_id |
| HIS-03 | entan.history.timeline | org_id=__invalid__ | 非法 org_id |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 企业搜索 | entan.history.enterprises | GET | /entan/v1/enterprises | keyword?；limit? | unavailable |
| 发展历程 | entan.history.timeline | GET | /entan/v1/history | org_id* | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.history.enterprises | FUNC-00108、00109、00110、00111 |
| entan.history.timeline | FUNC-00112、00113、00114 |
| （页面清单） | FUNC-00115、00116 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 2 个 title 均在功能点列出现且各有 ≥1 条 `场景=主流程`
- [x] 企业搜索：文档 sampleRequest 正向 + keyword/limit 合法组合 + 每参数 1 条反向（limit、keyword）
- [x] 发展历程：文档 org_id 正向 + 缺/非法 org_id 各 1 条反向
- [x] unavailable 两接口仍按 catalog 返回体写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 企业深度分析模型构建 / 企业发展历程模型
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00108～00116

**统计**：接口 **2**；主流程 **2**；备选 **1**；反向 **4**；清单 **2**；合计 **9** 条；编号闭区间 **FUNC-00108**～**FUNC-00116**（父控 R3-批2 分配）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **9** |
| 编号闭区间 | **FUNC-00108**～**FUNC-00116** |
| 接口向（不含清单） | **7** |
| 清单 | **2** |
| 已删 API 册 | `API-企业发展历程-用例.md`（API-00949～00955 作废，不复用） |
| 鉴权用例 | **0** |
