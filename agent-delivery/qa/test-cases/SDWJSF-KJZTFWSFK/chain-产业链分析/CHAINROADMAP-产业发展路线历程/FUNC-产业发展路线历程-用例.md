# 智能服务集群-科技专题服务算法库测试用例（产业发展路线历程 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=chain.roadmap` · `catalog_page_id=chain.roadmap` · path `#/chain/roadmap`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/chain.json` · 页 `chain.roadmap`  
> **A 线对照**：`fp-split-by-api-run/work/L16.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批8）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 产业发展路线历程 | chain.hotspot.roadmap | unavailable |
| 2 | 产业发展路线历程模型 | chain.roadmap.m_chain_deep_119_1 | available |

两个 title 均只有必填 `chainId`。各 1 条主流程 + 1 条缺 `chainId` 反向，不写备选，不按 field 拆条。

**chainId 取值**：`产业发展路线历程` 的 params.example 与 sampleRequest 均为 `chainId=INB1701`。`产业发展路线历程模型` 的 sampleRequest 为 `chain_id=INB1701`，params.example 为 `INB170101`，键名与取值不一致，主路径以 sampleRequest 为准（见附录 A）。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00509**～**FUNC-00514**，共 **6** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.roadmap`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00509 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 产业发展路线历程模型 | 产业发展路线历程 | 产业发展路线历程 | 验证产业发展路线历程功能，检查 chainId=INB1701 时返回面板中的 timeline 及嵌套 key_events 结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB1701 | 1.侧栏进入「产业链分析」→「产业发展路线历程」；2.切换至「算法测试」tab；3.接口下拉选择「产业发展路线历程」；4.填写 chainId=INB1701，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层：timeline 为数组（responseFields 历程事件（按年，含 key_events））；2、timeline 元素含 year（number）、key_events（array）；3、key_events 元素含 date（string）、type（string）、type_name（string）、title（string）、enterprise（string）；4、sampleResponse 示例 year=2024 两条：date=2024-06、type=policy、type_name=政策、title=产业专项规划发布、enterprise 空串；date=2024-11、type=financing、type_name=融资、title=头部企业完成新一轮融资、enterprise=深微制造；year=2025 两条：date=2025-04、type=breakthrough、type_name=突破、title=关键设备国产替代验证通过、enterprise=鹏城装备；date=2025-09、type=cooperation、type_name=合作、title=产学研联合实验室揭牌、enterprise 空串 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/roadmap |  | INTEG |  |  | endpoint_id=chain.hotspot.roadmap catalog_page_id=chain.roadmap 组合=RDP-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00510 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 产业发展路线历程模型 | 产业发展路线历程 | 产业发展路线历程 | 验证产业发展路线历程功能，检查不传 chainId 时返回面板指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「产业发展路线历程」；2.切换至「算法测试」tab；3.接口下拉选择「产业发展路线历程」；4.不传 chainId，点击调用（不传 chainId），点击调用 | 1、返回面板的 message 或 msg 指出缺少 chainId；2、不返回含 timeline 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/roadmap |  | INTEG |  |  | endpoint_id=chain.hotspot.roadmap catalog_page_id=chain.roadmap 组合=RDP-02 场景=异常-入参-缺chainId catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00511 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 产业发展路线历程模型 | 产业发展路线历程 | 产业发展路线历程模型 | 验证产业发展路线历程模型功能，检查填写 sampleRequest 所示参数 传 chain_id=INB1701 后返回 metric_id 与 hint | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「产业发展路线历程」；2.切换至「算法测试」tab；3.接口下拉选择「产业发展路线历程模型」；4.填写 请求体按sampleRequest：chain_id=INB1701，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，responseFields 指标 ID，示例 M_CHAIN_DEEP_119_1）、hint（string，sampleResponse 示例 真实 compute 响应,以实际调用为准） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_119_1/compute | M_CHAIN_DEEP_119_1 | INTEG |  |  | endpoint_id=chain.roadmap.m_chain_deep_119_1 catalog_page_id=chain.roadmap 组合=RMM-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00512 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 产业发展路线历程模型 | 产业发展路线历程 | 产业发展路线历程模型 | 验证产业发展路线历程模型功能，检查不传 chainId/chain_id 时返回面板指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「产业发展路线历程」；2.切换至「算法测试」tab；3.接口下拉选择「产业发展路线历程模型」；4.填写 请求体为空，不传 chainId/chain_id，点击调用（不传 chainId），点击调用 | 1、返回面板的 message 或 msg 指出缺少 chainId；2、不返回含 metric_id 为 M_CHAIN_DEEP_119_1 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_119_1/compute |  | INTEG |  |  | endpoint_id=chain.roadmap.m_chain_deep_119_1 catalog_page_id=chain.roadmap 组合=RMM-02 场景=异常-入参-缺chainId catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00513 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 产业发展路线历程模型 | 产业发展路线历程 | 接口信息 | 验证产业发展路线历程的接口信息功能，检查接口数量、名称和 method/path 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「产业发展路线历程」；2.停留在「接口信息」tab；3.接口下拉切换到「产业发展路线历程模型」 | 1、页头数量、下拉项数均为 2；2、下拉名称与 §0 各 title 一致；3、默认项概览 method、path 对应产业发展路线历程 GET /innov/v1/industry/{chainId}/roadmap；4、切换后概览对应产业发展路线历程模型 POST /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_119_1/compute，参数表与示例区已刷新；1、确认页头接口数量为 2；2、查看默认选中接口的概览 title、method、path 与 §0 清单第一项一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=chain.roadmap 场景=接口信息-清单 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00514 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 产业发展路线历程模型 | 产业发展路线历程 | 算法测试 | 验证产业发展路线历程的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「产业发展路线历程」；2.切换到「算法测试」tab；3.下拉切换到「产业发展路线历程模型」 | 1、算法测试 tab 下拉共 2 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「产业发展路线历程模型」；3、调用区 method 为 POST、path 为 /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_119_1/compute；4、请求区已随所选接口刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=chain.roadmap 场景=算法测试-清单 金样 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| RDP-01 | chain.hotspot.roadmap | chainId=INB1701 | 主路径（sampleRequest / params.example） |
| RDP-02 | chain.hotspot.roadmap | 不传 chainId | 缺必填 chainId |
| RMM-01 | chain.roadmap.m_chain_deep_119_1 | 请求体按 sampleRequest：chain_id=INB1701 | 主路径（sampleRequest；params.example=INB170101 与键名不一致，本组合以 sampleRequest 为准） |
| RMM-02 | chain.roadmap.m_chain_deep_119_1 | 请求体为空，不传 chainId/chain_id | 缺必填 chainId |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 产业发展路线历程 | chain.hotspot.roadmap | GET | /innov/v1/industry/{chainId}/roadmap | chainId* | unavailable |
| 产业发展路线历程模型 | chain.roadmap.m_chain_deep_119_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_119_1/compute | chainId* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.hotspot.roadmap | FUNC-00509、00510 |
| chain.roadmap.m_chain_deep_119_1 | FUNC-00511、00512 |
| （页面清单） | FUNC-00513、00514 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 2 个 title 均在功能点列出现且各有 1 条 `场景=主流程`（FUNC-00509、00511）
- [x] 仅有必填 chainId：各接口 1 条主流程 + 1 条缺 chainId 反向；无其它参数，不写备选
- [x] unavailable（产业发展路线历程）仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条 GET/POST 步骤
- [x] 五级/六级按 L16（产业链深度分析模型构建 / 产业发展路线历程模型）
- [x] 清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00509～00514

**统计**：catalog endpoint **2**；FUNC 用例 **6** 条；主流程 **2**、反向 **2**、清单 **2**；编号闭区间 **FUNC-00509**～**FUNC-00514**（R3-批8 · chain.roadmap）。
