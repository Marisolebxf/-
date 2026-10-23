# 智能服务集群-科技专题服务算法库测试用例（服务链短板分析 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=svc.gap` · `catalog_page_id=svc.gap` · path `#/industry-service/gap`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/svc.json` · 页 `svc.gap`  
> **A 线对照**：`fp-split-by-api-run/work/L41.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批13）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 服务链短板 | svc.gap.models | unavailable |
| 2 | 服务机构产业领域覆盖评分 | svc.gap.m_svc_org_coverage_depth | available |
| 3 | 服务链短板分析模型 | svc.gap.m_svc_deep_172_1 | available |

三个接口均仅有可选 `kind`。主流程对齐各自 `sampleRequest`：`kind=gap`。省略 `kind` 为备选；`kind=__invalid__` 作反向。`服务链短板` 的 catalog `status=unavailable`，仍按该接口文档返回体编写。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00859**～**FUNC-00869**，共 **11** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=svc.gap`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00859 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务链短板分析模型 | 服务链短板分析 | 服务链短板 | 验证服务链短板功能，检查填写 kind=gap调用后返回短板环节字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind=gap | 1.侧栏进入「产业服务分析」→「服务链短板分析」；2.切换至「算法测试」tab；3.接口下拉选择「服务链短板」；4.填写 kind=gap，点击调用 | 1、返回面板 body 顶层含 gap（array，responseFields 短板环节）；2、元素含 stage_name（string）、stage_code（string）、org_count_in_stage（number）、avg_depth（number）、runtime_flag（string）、q061_score（number）；3、结构与 sampleResponse 一致（示例三条：概念验证/POC/机构数 0/均深 0/标记 blank/q061_score 12；中试放大/PILOT/1/48/weak/36；产业化/IND/18/71/标记空串/68） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_CHAIN_BOTTLENECK | INTEG |  | FUNC-00859 | endpoint_id=svc.gap.models catalog_page_id=svc.gap 组合=GAPM-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00860 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务链短板分析模型 | 服务链短板分析 | 服务链短板 | 验证服务链短板功能，检查不传 kind 后仍返回短板环节结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「产业服务分析」→「服务链短板分析」；2.切换至「算法测试」tab；3.接口下拉选择「服务链短板」；4.不传 kind，点击调用（不传 kind），点击调用 | 1、返回面板 body 顶层仍含 gap（array，responseFields 短板环节）；2、元素仍含 stage_name（string）、stage_code（string）、org_count_in_stage（number）、avg_depth（number）、runtime_flag（string）、q061_score（number）；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_CHAIN_BOTTLENECK | INTEG |  | FUNC-00860 | endpoint_id=svc.gap.models catalog_page_id=svc.gap 组合=GAPM-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00861 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务链短板分析模型 | 服务链短板分析 | 服务链短板 | 验证服务链短板功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「产业服务分析」→「服务链短板分析」；2.切换至「算法测试」tab；3.接口下拉选择「服务链短板」；4.填写 kind=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 kind 非法；2、不返回含 gap 短板环节数组的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models |  | INTEG |  | FUNC-00861 | endpoint_id=svc.gap.models catalog_page_id=svc.gap 组合=GAPM-03 场景=异常-入参-非法kind catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00862 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务链短板分析模型 | 服务链短板分析 | 服务机构产业领域覆盖评分 | 验证服务机构产业领域覆盖评分功能，检查填写 kind=gap调用后返回 metric_id 与 gap 字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind=gap | 1.侧栏进入「产业服务分析」→「服务链短板分析」；2.切换至「算法测试」tab；3.接口下拉选择「服务机构产业领域覆盖评分」；4.填写 kind=gap，点击调用 | 1、返回面板 body 与 sampleResponse 同层含 metric_id（string，示例 M_SVC_ORG_COVERAGE_DEPTH）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 声明 gap 为 array（短板环节）；3、sampleResponse 未给出 gap 示例元素，返回中应出现 responseFields 所列 gap | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_ORG_COVERAGE_DEPTH/compute | M_SVC_ORG_COVERAGE_DEPTH | INTEG |  | FUNC-00862 | endpoint_id=svc.gap.m_svc_org_coverage_depth catalog_page_id=svc.gap 组合=GAPC-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00863 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务链短板分析模型 | 服务链短板分析 | 服务机构产业领域覆盖评分 | 验证服务机构产业领域覆盖评分功能，检查不传 kind 后仍返回计算结果结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「产业服务分析」→「服务链短板分析」；2.切换至「算法测试」tab；3.接口下拉选择「服务机构产业领域覆盖评分」；4.不传 kind，点击调用（不传 kind），点击调用 | 1、返回面板 body 仍含 metric_id（string）、hint（string）；2、responseFields 所列 gap（array，短板环节）仍应出现；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_ORG_COVERAGE_DEPTH/compute | M_SVC_ORG_COVERAGE_DEPTH | INTEG |  | FUNC-00863 | endpoint_id=svc.gap.m_svc_org_coverage_depth catalog_page_id=svc.gap 组合=GAPC-02 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00864 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务链短板分析模型 | 服务链短板分析 | 服务机构产业领域覆盖评分 | 验证服务机构产业领域覆盖评分功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「产业服务分析」→「服务链短板分析」；2.切换至「算法测试」tab；3.接口下拉选择「服务机构产业领域覆盖评分」；4.填写 kind=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 kind 非法；2、不返回含 metric_id 为 M_SVC_ORG_COVERAGE_DEPTH 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_ORG_COVERAGE_DEPTH/compute |  | INTEG |  | FUNC-00864 | endpoint_id=svc.gap.m_svc_org_coverage_depth catalog_page_id=svc.gap 组合=GAPC-03 场景=异常-入参-非法kind catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00865 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务链短板分析模型 | 服务链短板分析 | 服务链短板分析模型 | 验证服务链短板分析模型功能，检查填写 kind=gap调用后返回 metric_id 与 hint | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 使用 sampleRequest 取值 gap | 1.侧栏进入「产业服务分析」→「服务链短板分析」；2.切换至「算法测试」tab；3.接口下拉选择「服务链短板分析模型」；4.填写 kind=gap，点击调用 | 1、返回面板 body 与 sampleResponse 同层含 metric_id（string，responseFields 指标 ID，示例 M_SVC_DEEP_172_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、结构与 sampleResponse 一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_172_1/compute | M_SVC_DEEP_172_1 | INTEG |  | FUNC-00865 | endpoint_id=svc.gap.m_svc_deep_172_1 catalog_page_id=svc.gap 组合=GAPD-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00866 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务链短板分析模型 | 服务链短板分析 | 服务链短板分析模型 | 验证服务链短板分析模型功能，检查不传 kind 后仍返回计算结果结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「产业服务分析」→「服务链短板分析」；2.切换至「算法测试」tab；3.接口下拉选择「服务链短板分析模型」；4.不传 kind，点击调用（不传 kind），点击调用 | 1、返回面板 body 仍含 metric_id（string，responseFields 指标 ID）、hint（string）；2、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_172_1/compute | M_SVC_DEEP_172_1 | INTEG |  | FUNC-00866 | endpoint_id=svc.gap.m_svc_deep_172_1 catalog_page_id=svc.gap 组合=GAPD-02 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00867 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务链短板分析模型 | 服务链短板分析 | 服务链短板分析模型 | 验证服务链短板分析模型功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「产业服务分析」→「服务链短板分析」；2.切换至「算法测试」tab；3.接口下拉选择「服务链短板分析模型」；4.填写 kind=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 kind 非法；2、不返回含 metric_id 为 M_SVC_DEEP_172_1 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_172_1/compute |  | INTEG |  | FUNC-00867 | endpoint_id=svc.gap.m_svc_deep_172_1 catalog_page_id=svc.gap 组合=GAPD-03 场景=异常-入参-非法kind catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00868 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务链短板分析模型 | 服务链短板分析 | 接口信息 | 验证服务链短板分析的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业服务分析」→「服务链短板分析」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 3；2、下拉名称与 §0 各 title 一致（服务链短板、服务机构产业领域覆盖评分、服务链短板分析模型）；3、默认项概览 method=GET、path=/entan/v1/svc/models；4、切换后概览对应服务机构产业领域覆盖评分 POST /entan/v1/svc-metric/metric/M_SVC_ORG_COVERAGE_DEPTH/compute、服务链短板分析模型 POST /entan/v1/svc-metric/metric/M_SVC_DEEP_172_1/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00868 | catalog_page_id=svc.gap 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00869 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务链短板分析模型 | 服务链短板分析 | 算法测试 | 验证服务链短板分析的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业服务分析」→「服务链短板分析」；2.切换到「算法测试」tab；3.下拉切换到「服务机构产业领域覆盖评分」 | 1、算法测试 tab 下拉共 3 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「服务机构产业领域覆盖评分」；3、调用区 method 为 POST、path 为 /entan/v1/svc-metric/metric/M_SVC_ORG_COVERAGE_DEPTH/compute；4、请求参数区已随所选接口刷新；5、未点击调用时不校验返回字段 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00869 | catalog_page_id=svc.gap 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| GAPM-01 | svc.gap.models | kind=gap | 主路径（sampleRequest） |
| GAPM-02 | svc.gap.models | 不传 kind | 省略可选 kind |
| GAPM-03 | svc.gap.models | kind=__invalid__ | 只破坏 kind |
| GAPC-01 | svc.gap.m_svc_org_coverage_depth | kind=gap | 主路径（sampleRequest） |
| GAPC-02 | svc.gap.m_svc_org_coverage_depth | 不传 kind | 省略可选 kind |
| GAPC-03 | svc.gap.m_svc_org_coverage_depth | kind=__invalid__ | 只破坏 kind |
| GAPD-01 | svc.gap.m_svc_deep_172_1 | kind=gap | 主路径（sampleRequest；params.example 为 tech，本组合不改用 tech） |
| GAPD-02 | svc.gap.m_svc_deep_172_1 | 不传 kind | 省略可选 kind |
| GAPD-03 | svc.gap.m_svc_deep_172_1 | kind=__invalid__ | 只破坏 kind |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 服务链短板 | svc.gap.models | GET | /entan/v1/svc/models | kind? | unavailable |
| 服务机构产业领域覆盖评分 | svc.gap.m_svc_org_coverage_depth | POST | /entan/v1/svc-metric/metric/M_SVC_ORG_COVERAGE_DEPTH/compute | kind? | available |
| 服务链短板分析模型 | svc.gap.m_svc_deep_172_1 | POST | /entan/v1/svc-metric/metric/M_SVC_DEEP_172_1/compute | kind? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| svc.gap.models | FUNC-00859、00860、00861 |
| svc.gap.m_svc_org_coverage_depth | FUNC-00862、00863、00864 |
| svc.gap.m_svc_deep_172_1 | FUNC-00865、00866、00867 |
| （页面清单） | FUNC-00868、00869 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 3 个 title 均在功能点列出现且各有 ≥1 条 `场景=主流程`（FUNC-00859、00862、00865）
- [x] 仅可选 kind 的接口各 3 条（sampleRequest 主流程 + 省略 kind 备选 + 非法 kind 反向）
- [x] unavailable 仍按 catalog sampleResponse 写主流程与备选，备注注明未交付
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 五级/六级按 L41（产业服务深度分析模型构建 / 服务链短板分析模型）
- [x] 测试内容均含「验证」与「检查」；登录仅在前置条件
- [x] 多接口页清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（含切换步骤）
- [x] `coverage-fp.md` 已同步 FUNC-00859～00869

**统计**：catalog endpoint **3**；title **3**；FUNC 用例 **11** 条；主流程 **3**、备选 **3**、反向 **3**、清单 **2**；编号闭区间 **FUNC-00859**～**FUNC-00869**（R3-批13 svc.gap）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **11** |
| 编号闭区间 | **FUNC-00859**～**FUNC-00869** |
| 接口向（不含清单） | **9** |
| 主流程 | **3** |
| 备选-参数组合 | **3** |
| 反向 | **3** |
| 清单 | **2** |
| 已删 API 册 | `API-服务链短板分析-用例.md`（API-01647～01655 作废，不复用；B 线只保留本 FUNC 册） |
| 鉴权用例 | **0** |
