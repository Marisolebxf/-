# 智能服务集群-科技专题服务算法库测试用例（产业阶段分析 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=chain.stage` · `catalog_page_id=chain.stage` · path `#/chain/stage`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/chain.json` · 页 `chain.stage`  
> **A 线对照**：`fp-split-by-api-run/work/L20.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批6）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 产业阶段分析 | chain.stage.main | unavailable |
| 2 | 产业阶段分析模型 | chain.stage.m_chain_deep_123_1 | available |

**chainId 取值**：`产业阶段分析` 的 params.example 与 sampleRequest 均为 `INB1701`。`产业阶段分析模型` 的 sampleRequest 为 `chain_id=INB1701`（params.name=chainId，example=INB170101，主路径以 sampleRequest 为准）。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00455**～**FUNC-00460**，共 **6** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.stage`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00455 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 产业阶段分析模型 | 产业阶段分析 | 产业阶段分析 | 验证产业阶段分析功能，检查 chainId=INB1701 后返回面板含 cycle、stage 及文档示例字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB1701 | 1.侧栏进入「产业链分析」→「产业阶段分析」；2.切换至「算法测试」tab；3.接口下拉选择「产业阶段分析」；4.填写 chainId=INB1701，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层含 cycle（object）、stage（object）；2、cycle.cycle_stage（string，responseFields 周期阶段，示例 成长期）、cycle.growth_rate（number，示例 14.9）、cycle.investment_trend（string，示例 up）、cycle.enterprise_trend（string，示例 up）、cycle.trend（array）；3、trend 元素含 year（number）、revenue（number）、growth_rate（number），示例三条为 2023/12800/8.2、2024/14640/14.4、2025/16820/14.9；4、stage.cycle_stage（string，示例 成长期）、stage.sub_stage（string，responseFields 细分阶段，示例 加速扩张）、stage.high_tech_ratio（number，示例 46.2）、stage.investment_intensity（number，示例 7.8）、stage.growth_rate（number，示例 14.9） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/cycle | M_CHAIN_CYCLE_STAGE | INTEG |  | FUNC-00455 | endpoint_id=chain.stage.main catalog_page_id=chain.stage 组合=STG-01 场景=主流程 金样 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00456 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 产业阶段分析模型 | 产业阶段分析 | 产业阶段分析 | 验证产业阶段分析功能，检查不传 chainId 时返回面板指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「产业阶段分析」；2.切换至「算法测试」tab；3.接口下拉选择「产业阶段分析」；4.不传 chainId，点击调用（不传 chainId），点击调用 | 1、返回面板的 message 或 msg 指出 chainId 缺失；2、不返回含 cycle.cycle_stage 或 stage.sub_stage 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/cycle |  | INTEG |  | FUNC-00456 | endpoint_id=chain.stage.main catalog_page_id=chain.stage 组合=STG-02 场景=异常-入参-缺chainId catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00457 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 产业阶段分析模型 | 产业阶段分析 | 产业阶段分析模型 | 验证产业阶段分析模型功能，检查填写 sampleRequest 所示参数 传 chain_id=INB1701 后返回 metric_id 与 hint | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「产业阶段分析」；2.切换至「算法测试」tab；3.接口下拉选择「产业阶段分析模型」；4.填写 请求体按sampleRequest：chain_id=INB1701，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，responseFields 指标 ID，示例 M_CHAIN_DEEP_123_1）、hint（string，示例 真实 compute 响应,以实际调用为准） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_123_1/compute | M_CHAIN_DEEP_123_1 | INTEG |  | FUNC-00457 | endpoint_id=chain.stage.m_chain_deep_123_1 catalog_page_id=chain.stage 组合=STM-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00458 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 产业阶段分析模型 | 产业阶段分析 | 产业阶段分析模型 | 验证产业阶段分析模型功能，检查不传 chainId/chain_id 时返回面板指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「产业阶段分析」；2.切换至「算法测试」tab；3.接口下拉选择「产业阶段分析模型」；4.填写 请求体为空，不传 chainId/chain_id，点击调用（不传 chainId），点击调用 | 1、返回面板的 message 或 msg 指出 chainId 缺失；2、不返回含 metric_id 为 M_CHAIN_DEEP_123_1 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_123_1/compute |  | INTEG |  | FUNC-00458 | endpoint_id=chain.stage.m_chain_deep_123_1 catalog_page_id=chain.stage 组合=STM-02 场景=异常-入参-缺chainId catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00459 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 产业阶段分析模型 | 产业阶段分析 | 接口信息 | 验证产业阶段分析的接口信息功能，检查接口数量、名称和 method/path 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「产业阶段分析」；2.停留在「接口信息」tab；3.接口下拉切换到「产业阶段分析模型」 | 1、页头数量、下拉项数均为 2；2、下拉名称与 §0 各 title 一致；3、默认项概览 method、path 对应产业阶段分析 GET /innov/v1/industry/{chainId}/cycle；4、切换后概览对应产业阶段分析模型 POST /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_123_1/compute，参数表与示例区已刷新；1、确认页头接口数量为 2；2、查看默认选中接口的概览 title、method、path 与 §0 清单第一项一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00459 | catalog_page_id=chain.stage 场景=接口信息-清单 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00460 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 产业阶段分析模型 | 产业阶段分析 | 算法测试 | 验证产业阶段分析的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「产业阶段分析」；2.切换到「算法测试」tab；3.下拉切换到「产业阶段分析模型」 | 1、算法测试 tab 下拉共 2 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「产业阶段分析模型」；3、调用区 method 为 POST、path 为 /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_123_1/compute；4、请求区已随所选接口刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00460 | catalog_page_id=chain.stage 场景=算法测试-清单 金样 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| STG-01 | chain.stage.main | chainId=INB1701 | 主路径（sampleRequest / params.example） |
| STG-02 | chain.stage.main | 不传 chainId | 缺必填 chainId |
| STM-01 | chain.stage.m_chain_deep_123_1 | 请求体按 sampleRequest：chain_id=INB1701 | 主路径（sampleRequest；params.example=INB170101 与键名不一致，本组合以 sampleRequest 为准） |
| STM-02 | chain.stage.m_chain_deep_123_1 | 请求体为空，不传 chainId/chain_id | 缺必填 chainId |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 产业阶段分析 | chain.stage.main | GET | /innov/v1/industry/{chainId}/cycle | chainId* | unavailable |
| 产业阶段分析模型 | chain.stage.m_chain_deep_123_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_123_1/compute | chainId* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.stage.main | FUNC-00455、00456 |
| chain.stage.m_chain_deep_123_1 | FUNC-00457、00458 |
| （页面清单） | FUNC-00459、00460 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 2 个 title 均在功能点列出现且各有 1 条 `场景=主流程`（FUNC-00455、00457）
- [x] 仅有必填 chainId：各接口 1 条主流程 + 1 条缺 chainId 反向；无其它参数，不写备选、不写非法 chainId
- [x] unavailable（产业阶段分析）仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条 GET/POST 步骤
- [x] 五级/六级按 L20（产业链深度分析模型构建 / 产业阶段分析模型）
- [x] 清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00455～00460

**统计**：catalog endpoint **2**；FUNC 用例 **6** 条；主流程 **2**、反向 **2**、清单 **2**；编号闭区间 **FUNC-00455**～**FUNC-00460**（父控 R3-批6 · chain.stage）。
