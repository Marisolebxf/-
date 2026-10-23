# 智能服务集群-科技专题服务算法库测试用例（产业瓶颈堵点识别 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=chain.bottleneck` · `catalog_page_id=chain.bottleneck` · path `#/chain/bottleneck`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/chain.json` · 页 `chain.bottleneck`  
> **A 线对照**：`fp-split-by-api-run/work/L22.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批7；父控自 chain.json 转正）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 瓶颈堵点 | chain.bottleneck.main | unavailable |
| 2 | 产业瓶颈堵点识别模型 | chain.bottleneck.m_chain_deep_125_1 | available |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00467**～**FUNC-00472**，共 **6** 条）。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00467 | 算法工具库 | 科技专题服务算法库 | 产业瓶颈堵点识别模型 | 瓶颈堵点 | 产业瓶颈堵点识别 | 瓶颈堵点 | 验证瓶颈堵点功能，检查 chainId=INB170101 时返回面板含严重度、综合得分、五维得分与建议 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB170101 | 1.侧栏进入「产业链分析」→「产业瓶颈堵点识别」；2.切换至「算法测试」tab；3.接口下拉选择「瓶颈堵点」；4.填写 chainId=INB170101，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：severity（string，responseFields 综合严重度，示例 中等）、overall_score（number，responseFields 综合得分，示例 62.4）；2、sampleResponse 还含 tech_score（number，示例 48）、talent_score（number，示例 55）、market_score（number，示例 71）、capital_score（number，示例 64）、policy_score（number，示例 74）；3、suggestions 为数组，元素含 name（string）、advice（string）；示例第 1 条 name=关键设备、advice=加快刻蚀、薄膜沉积与量检测设备的国产替代验证。；示例第 2 条 name=半导体材料、advice=加强高端光刻材料与电子特气的本地化供给。 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/bottlenecks | M_CHAIN_BOTTLENECK_SEVERITY | INTEG |  | FUNC-00467 | endpoint_id=chain.bottleneck.main catalog_page_id=chain.bottleneck 组合=BOT-01 场景=主流程 金样 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00468 | 算法工具库 | 科技专题服务算法库 | 产业瓶颈堵点识别模型 | 瓶颈堵点 | 产业瓶颈堵点识别 | 瓶颈堵点 | 验证瓶颈堵点功能，检查不传 chainId 时返回面板指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「产业瓶颈堵点识别」；2.切换至「算法测试」tab；3.接口下拉选择「瓶颈堵点」；4.不传 chainId，点击调用（不传 chainId），点击调用 | 1、返回面板的 message 或 msg 指出缺少 chainId；2、不返回含 severity 或 overall_score 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/bottlenecks |  | INTEG |  | FUNC-00468 | endpoint_id=chain.bottleneck.main catalog_page_id=chain.bottleneck 组合=BOT-02 场景=异常-入参-缺chainId catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00469 | 算法工具库 | 科技专题服务算法库 | 产业瓶颈堵点识别模型 | 产业瓶颈堵点识别模型 | 产业瓶颈堵点识别 | 产业瓶颈堵点识别模型 | 验证产业瓶颈堵点识别模型功能，检查填写 sampleRequest 所示参数 传 chain_id=INB1701 后返回 metric_id 与 hint | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「产业瓶颈堵点识别」；2.切换至「算法测试」tab；3.接口下拉选择「产业瓶颈堵点识别模型」；4.填写 请求体按sampleRequest：chain_id=INB1701（params.name=chainId，example=INB170101，键名与取值均与sampleRequest不一致，本组合以sampleRequest为准），点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，responseFields 指标 ID，示例 M_CHAIN_DEEP_125_1）、hint（string，sampleResponse 多出字段，示例 真实 compute 响应,以实际调用为准） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_125_1/compute | M_CHAIN_DEEP_125_1 | INTEG |  | FUNC-00469 | endpoint_id=chain.bottleneck.m_chain_deep_125_1 catalog_page_id=chain.bottleneck 组合=BTM-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00470 | 算法工具库 | 科技专题服务算法库 | 产业瓶颈堵点识别模型 | 产业瓶颈堵点识别模型 | 产业瓶颈堵点识别 | 产业瓶颈堵点识别模型 | 验证产业瓶颈堵点识别模型功能，检查不传 chainId/chain_id 时返回面板指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「产业瓶颈堵点识别」；2.切换至「算法测试」tab；3.接口下拉选择「产业瓶颈堵点识别模型」；4.不传 chainId，请求体也不含 chain_id，点击调用（不传 chainId），点击调用 | 1、返回面板的 message 或 msg 指出缺少 chainId；2、不返回含 metric_id 为 M_CHAIN_DEEP_125_1 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_125_1/compute |  | INTEG |  | FUNC-00470 | endpoint_id=chain.bottleneck.m_chain_deep_125_1 catalog_page_id=chain.bottleneck 组合=BTM-02 场景=异常-入参-缺chainId catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00471 | 算法工具库 | 科技专题服务算法库 | 产业瓶颈堵点识别模型 | 瓶颈堵点 | 产业瓶颈堵点识别 | 接口信息 | 验证产业瓶颈堵点识别的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「产业瓶颈堵点识别」；2.停留在「接口信息」tab；3.接口下拉切换到「产业瓶颈堵点识别模型」 | 1、页头数量、下拉项数均为 2；2、下拉名称与 endpoints 各 title 一致；3、默认项概览 method、path 对应瓶颈堵点 GET /innov/v1/industry/{chainId}/bottlenecks；4、切换后概览对应产业瓶颈堵点识别模型 POST /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_125_1/compute，参数表与示例区已刷新；1、确认页头接口数量为 2；2、查看默认选中接口的概览 title、method、path 与 endpoints 清单第一项一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00471 | catalog_page_id=chain.bottleneck 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00472 | 算法工具库 | 科技专题服务算法库 | 产业瓶颈堵点识别模型 | 瓶颈堵点 | 产业瓶颈堵点识别 | 算法测试 | 验证产业瓶颈堵点识别的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「产业瓶颈堵点识别」；2.切换到「算法测试」tab；3.下拉切换到「产业瓶颈堵点识别模型」 | 1、算法测试 tab 下拉共 2 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「产业瓶颈堵点识别模型」；3、调用区 method 为 POST、path 为 /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_125_1/compute；4、请求区已随所选接口刷新；1、确认调用区下拉项数量与名称与 endpoints 清单一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00472 | catalog_page_id=chain.bottleneck 场景=算法测试-清单 |
---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| BOT-01 | chain.bottleneck.main | chainId=INB170101 | 主路径（sampleRequest / params.example） |
| BOT-02 | chain.bottleneck.main | 不传 chainId | 缺必填 chainId |
| BTM-01 | chain.bottleneck.m_chain_deep_125_1 | 请求体按 sampleRequest：chain_id=INB1701（params.name=chainId，example=INB170101，键名与取值均与 sampleRequest 不一致，本组合以 sampleRequest 为准） | 主路径（sampleRequest） |
| BTM-02 | chain.bottleneck.m_chain_deep_125_1 | 不传 chainId，请求体也不含 chain_id | 缺必填 chainId |

---

**统计**：合计 **6** 条；编号闭区间 **FUNC-00467**～**FUNC-00472**（R3-批7）。
