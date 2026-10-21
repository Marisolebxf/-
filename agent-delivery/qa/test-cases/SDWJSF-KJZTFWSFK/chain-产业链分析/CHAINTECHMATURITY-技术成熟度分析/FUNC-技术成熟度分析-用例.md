# 智能服务集群-科技专题服务算法库测试用例（技术成熟度分析 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=chain.tech-maturity` · `catalog_page_id=chain.tech-maturity` · path `#/chain/tech-maturity`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/chain.json` · 页 `chain.tech-maturity`  
> **A 线对照**：无对应 Lxx（`_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `chain.tech-maturity`，原因：60 条无对应六级；覆盖矩阵见 `coverage-fp.md`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批9）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 技术成熟度 | chain.tech-maturity.main | unavailable |
| 2 | 技术成熟度评分 | chain.tech-maturity.m_chain_tech_maturity_score | available |

两个 title 均只有必填 `chainId`。各 1 条主流程 + 1 条缺 `chainId` 反向，不写备选，不按 field 拆条。

**chainId 取值**：`技术成熟度` 的 params.example 与 sampleRequest 均为 `INB170101`。`技术成熟度评分` 的 sampleRequest 为 `chain_id=INB1701`，params.example 为 `INB170101`，键名与取值不一致，主路径以 sampleRequest 为准（见附录 A）。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00521**～**FUNC-00526**，共 **6** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.tech-maturity`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00521 | 算法工具库 | 科技专题服务算法库 | 技术成熟度分析 | 技术成熟度分析 | 技术成熟度分析 | 技术成熟度 | 验证技术成熟度功能，检查 chainId=INB170101 时返回面板中的成熟度评分、阶段与年度专利趋势 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB170101 | 1.侧栏进入「产业链分析」→「技术成熟度分析」；2.切换至「算法测试」tab；3.接口下拉选择「技术成熟度」；4.填写 chainId=INB170101，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：tech_maturity_score（number，responseFields 技术成熟度评分，示例 70）、stage（string，sampleResponse 多出字段，示例 趋于成熟）；2、trend 为数组（responseFields 年度公开专利量），元素含 year（number）、patent_count（number）；示例第 1 条 year=2023、patent_count=86；示例第 2 条 year=2024、patent_count=102；示例第 3 条 year=2025、patent_count=118 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/tech-maturity | M_CHAIN_TECH_MATURITY_SCORE | INTEG |  |  | endpoint_id=chain.tech-maturity.main catalog_page_id=chain.tech-maturity 组合=TMA-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00522 | 算法工具库 | 科技专题服务算法库 | 技术成熟度分析 | 技术成熟度分析 | 技术成熟度分析 | 技术成熟度 | 验证技术成熟度功能，检查不传 chainId 时返回面板指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「技术成熟度分析」；2.切换至「算法测试」tab；3.接口下拉选择「技术成熟度」；4.不传 chainId，点击调用（不传 chainId），点击调用 | 1、返回面板的 message 或 msg 指出缺少 chainId；2、不返回含 tech_maturity_score 或 trend 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/tech-maturity |  | INTEG |  |  | endpoint_id=chain.tech-maturity.main catalog_page_id=chain.tech-maturity 组合=TMA-02 场景=异常-入参-缺chainId catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00523 | 算法工具库 | 科技专题服务算法库 | 技术成熟度分析 | 技术成熟度评分 | 技术成熟度分析 | 技术成熟度评分 | 验证技术成熟度评分功能，检查填写 sampleRequest 所示参数 传 chain_id=INB1701 后返回 metric_id 与 hint | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「技术成熟度分析」；2.切换至「算法测试」tab；3.接口下拉选择「技术成熟度评分」；4.填写 请求体按sampleRequest：chain_id=INB1701（params.name=chainId，example=INB170101，键名与取值均与sampleRequest不一致，本组合以sampleRequest为准），点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，responseFields 指标 ID，示例 M_CHAIN_TECH_MATURITY_SCORE）、hint（string，sampleResponse 多出字段，示例 真实 compute 响应,以实际调用为准） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_TECH_MATURITY_SCORE/compute | M_CHAIN_TECH_MATURITY_SCORE | INTEG |  |  | endpoint_id=chain.tech-maturity.m_chain_tech_maturity_score catalog_page_id=chain.tech-maturity 组合=TMS-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00524 | 算法工具库 | 科技专题服务算法库 | 技术成熟度分析 | 技术成熟度评分 | 技术成熟度分析 | 技术成熟度评分 | 验证技术成熟度评分功能，检查不传 chainId/chain_id 时返回面板指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「技术成熟度分析」；2.切换至「算法测试」tab；3.接口下拉选择「技术成熟度评分」；4.不传 chainId，请求体也不含 chain_id，点击调用（不传 chainId），点击调用 | 1、返回面板的 message 或 msg 指出缺少 chainId；2、不返回含 metric_id 为 M_CHAIN_TECH_MATURITY_SCORE 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_TECH_MATURITY_SCORE/compute |  | INTEG |  |  | endpoint_id=chain.tech-maturity.m_chain_tech_maturity_score catalog_page_id=chain.tech-maturity 组合=TMS-02 场景=异常-入参-缺chainId catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00525 | 算法工具库 | 科技专题服务算法库 | 技术成熟度分析 | 技术成熟度分析 | 技术成熟度分析 | 接口信息 | 验证技术成熟度分析的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「技术成熟度分析」；2.停留在「接口信息」tab；3.接口下拉切换到「技术成熟度评分」 | 1、页头数量、下拉项数均为 2；2、下拉名称与 §0 各 title 一致；3、默认项概览 method、path 对应技术成熟度 GET /innov/v1/industry/{chainId}/tech-maturity；4、切换后概览对应技术成熟度评分 POST /innov/v1/industry/chainan/metric/M_CHAIN_TECH_MATURITY_SCORE/compute，参数表与示例区已刷新；1、确认页头接口数量为 2；2、查看默认选中接口的概览 title、method、path 与 §0 清单第一项一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=chain.tech-maturity 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00526 | 算法工具库 | 科技专题服务算法库 | 技术成熟度分析 | 技术成熟度分析 | 技术成熟度分析 | 算法测试 | 验证技术成熟度分析的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「技术成熟度分析」；2.切换到「算法测试」tab；3.下拉切换到「技术成熟度评分」 | 1、算法测试 tab 下拉共 2 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「技术成熟度评分」；3、调用区 method 为 POST、path 为 /innov/v1/industry/chainan/metric/M_CHAIN_TECH_MATURITY_SCORE/compute；4、请求区已随所选接口刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=chain.tech-maturity 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| TMA-01 | chain.tech-maturity.main | chainId=INB170101 | 主路径（sampleRequest / params.example） |
| TMA-02 | chain.tech-maturity.main | 不传 chainId | 缺必填 chainId |
| TMS-01 | chain.tech-maturity.m_chain_tech_maturity_score | 请求体按 sampleRequest：chain_id=INB1701（params.name=chainId，example=INB170101，键名与取值均与 sampleRequest 不一致，本组合以 sampleRequest 为准） | 主路径（sampleRequest） |
| TMS-02 | chain.tech-maturity.m_chain_tech_maturity_score | 不传 chainId，请求体也不含 chain_id | 缺必填 chainId |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 技术成熟度 | chain.tech-maturity.main | GET | /innov/v1/industry/{chainId}/tech-maturity | chainId* | unavailable |
| 技术成熟度评分 | chain.tech-maturity.m_chain_tech_maturity_score | POST | /innov/v1/industry/chainan/metric/M_CHAIN_TECH_MATURITY_SCORE/compute | chainId* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.tech-maturity.main | FUNC-00521、00522 |
| chain.tech-maturity.m_chain_tech_maturity_score | FUNC-00523、00524 |
| （页面清单） | FUNC-00525、00526 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 2 个 title（技术成熟度、技术成熟度评分）均在功能点列出现，且各有 1 条 `场景=主流程`（FUNC-00521、00523）
- [x] 有参接口：文档示例正向各 1 条；必填 chainId 各 1 条反向；无可选参数，无备选-参数组合
- [x] unavailable（技术成熟度）仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条 GET/POST 步骤
- [x] 无对应 Lxx：五级/六级按 catalog 页名与 title 填写
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（2 接口页含切换步骤）
- [x] `coverage-fp.md` 已同步 FUNC-00521～00526

**统计**：catalog endpoint **2**；title **2**；FUNC 用例 **6** 条；主流程 **2**、反向 **2**、清单 **2**；编号闭区间 **FUNC-00521**～**FUNC-00526**（R3-批9 chain.tech-maturity）。
