# 智能服务集群-科技专题服务算法库测试用例（服务链短板分析 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业服务分析 / 服务链短板分析  
> **catalog**：`entry_id=svc.gap` · `catalog_page_id=svc.gap` · path `/industry-service/gap`  
> **A 线对照**：`fp-split-by-api-run/work/L41.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：联调台 `http://111.198.38.90:50897/`（接口文档真源 `svc.json` 页 `svc.gap`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批13）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 服务链短板 | svc.gap.models |
| 2 | 服务机构产业领域覆盖评分 | svc.gap.m_svc_org_coverage_depth |
| 3 | 服务链短板分析模型 | svc.gap.m_svc_deep_172_1 |

**kind 试调取值**：三个接口都只有可选 `kind`。主流程对齐各自 `sampleRequest`：`kind=gap`。省略 `kind` 为备选。非法值 `kind=__invalid__` 单独作反向。`服务链短板` 的 catalog `status=unavailable`，仍按该接口文档返回体编写。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01647**～**API-01655**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=svc.gap`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01647 | 产业服务分析 | 服务链短板分析 | 主流程 | — | 服务链短板分析 | 服务链短板 | 服务链短板按文档 sampleRequest kind=gap 查询返回短板环节字段 | 1、kind 使用文档示例 gap | 1.GET /entan/v1/svc/models，查询参数取组合 GAPM-01 | 1、返回 body 顶层含 gap（array，responseFields 短板环节）；2、元素含 stage_name（string）、stage_code（string）、org_count_in_stage（number）、avg_depth（number）、runtime_flag（string）、q061_score（number）；3、结构与 sampleResponse 一致（示例三条：概念验证/POC/机构数 0/均深 0/标记 blank/q061_score 12；中试放大/PILOT/1/48/weak/36；产业化/IND/18/71/标记空串/68） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_CHAIN_BOTTLENECK | INTEG | | | endpoint_id=svc.gap.models catalog_page_id=svc.gap 组合=GAPM-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01648 | 产业服务分析 | 服务链短板分析 | 备选-参数组合 | 省略 kind | 服务链短板分析 | 服务链短板 | 服务链短板不传可选 kind（与 sampleRequest 相反） | 1、不传 kind | 1.GET /entan/v1/svc/models，查询参数取组合 GAPM-02 | 1、返回 body 顶层仍含 gap（array，responseFields 短板环节）；2、元素仍含 stage_name（string）、stage_code（string）、org_count_in_stage（number）、avg_depth（number）、runtime_flag（string）、q061_score（number）；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_CHAIN_BOTTLENECK | INTEG | | | endpoint_id=svc.gap.models catalog_page_id=svc.gap 组合=GAPM-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01649 | 产业服务分析 | 服务链短板分析 | 异常-入参-非法kind | — | 服务链短板分析 | 服务链短板 | 服务链短板 kind 非法 | 1、kind 取文档枚举外的值 | 1.GET /entan/v1/svc/models，查询参数取组合 GAPM-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 gap 短板环节数组的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | | INTEG | | | endpoint_id=svc.gap.models catalog_page_id=svc.gap 组合=GAPM-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01650 | 产业服务分析 | 服务链短板分析 | 主流程 | — | 服务链短板分析 | 服务机构产业领域覆盖评分 | 服务机构产业领域覆盖评分按文档 sampleRequest kind=gap 计算 | 1、kind 使用文档示例 gap | 1.POST /entan/v1/svc-metric/metric/M_SVC_ORG_COVERAGE_DEPTH/compute，请求体取组合 GAPC-01 | 1、返回 body 与 sampleResponse 同层含 metric_id（string，示例 M_SVC_ORG_COVERAGE_DEPTH）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 声明 gap 为 array（短板环节）；3、sampleResponse 未给出 gap 示例元素，返回中应出现 responseFields 所列 gap | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_ORG_COVERAGE_DEPTH/compute | M_SVC_ORG_COVERAGE_DEPTH | INTEG | | | endpoint_id=svc.gap.m_svc_org_coverage_depth catalog_page_id=svc.gap 组合=GAPC-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01651 | 产业服务分析 | 服务链短板分析 | 备选-参数组合 | 省略 kind | 服务链短板分析 | 服务机构产业领域覆盖评分 | 服务机构产业领域覆盖评分不传可选 kind（与 sampleRequest 相反） | 1、不传 kind | 1.POST /entan/v1/svc-metric/metric/M_SVC_ORG_COVERAGE_DEPTH/compute，请求体取组合 GAPC-02 | 1、返回 body 仍含 metric_id（string）、hint（string）；2、responseFields 所列 gap（array，短板环节）仍应出现；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_ORG_COVERAGE_DEPTH/compute | M_SVC_ORG_COVERAGE_DEPTH | INTEG | | | endpoint_id=svc.gap.m_svc_org_coverage_depth catalog_page_id=svc.gap 组合=GAPC-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01652 | 产业服务分析 | 服务链短板分析 | 异常-入参-非法kind | — | 服务链短板分析 | 服务机构产业领域覆盖评分 | 服务机构产业领域覆盖评分 kind 非法 | 1、kind 取文档枚举外的值 | 1.POST /entan/v1/svc-metric/metric/M_SVC_ORG_COVERAGE_DEPTH/compute，请求体取组合 GAPC-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 metric_id 为 M_SVC_ORG_COVERAGE_DEPTH 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_ORG_COVERAGE_DEPTH/compute | | INTEG | | | endpoint_id=svc.gap.m_svc_org_coverage_depth catalog_page_id=svc.gap 组合=GAPC-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01653 | 产业服务分析 | 服务链短板分析 | 主流程 | — | 服务链短板分析 | 服务链短板分析模型 | 服务链短板分析模型按文档 sampleRequest kind=gap 计算 | 1、kind 使用 sampleRequest 取值 gap | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_172_1/compute，请求体取组合 GAPD-01 | 1、返回 body 与 sampleResponse 同层含 metric_id（string，responseFields 指标 ID，示例 M_SVC_DEEP_172_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、结构与 sampleResponse 一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_172_1/compute | M_SVC_DEEP_172_1 | INTEG | | | endpoint_id=svc.gap.m_svc_deep_172_1 catalog_page_id=svc.gap 组合=GAPD-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01654 | 产业服务分析 | 服务链短板分析 | 备选-参数组合 | 省略 kind | 服务链短板分析 | 服务链短板分析模型 | 服务链短板分析模型不传可选 kind（与 sampleRequest 相反） | 1、不传 kind | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_172_1/compute，请求体取组合 GAPD-02 | 1、返回 body 仍含 metric_id（string，responseFields 指标 ID）、hint（string）；2、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_172_1/compute | M_SVC_DEEP_172_1 | INTEG | | | endpoint_id=svc.gap.m_svc_deep_172_1 catalog_page_id=svc.gap 组合=GAPD-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01655 | 产业服务分析 | 服务链短板分析 | 异常-入参-非法kind | — | 服务链短板分析 | 服务链短板分析模型 | 服务链短板分析模型 kind 非法 | 1、kind 取文档枚举外的值 | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_172_1/compute，请求体取组合 GAPD-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 metric_id 为 M_SVC_DEEP_172_1 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_172_1/compute | | INTEG | | | endpoint_id=svc.gap.m_svc_deep_172_1 catalog_page_id=svc.gap 组合=GAPD-03 |

---

## 附录 A · 入参组合

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
| svc.gap.models | API-01647、01648、01649 |
| svc.gap.m_svc_org_coverage_depth | API-01650、01651、01652 |
| svc.gap.m_svc_deep_172_1 | API-01653、01654、01655 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 3 个 title 均在功能点列出现，且各有 1 条主流程（01647、01650、01653）
- [x] 各接口仅可选 kind：sampleRequest 主流程 1 条 + 省略 kind 备选 1 条 + 非法 kind 反向 1 条
- [x] unavailable（服务链短板）仍按 catalog 返回体写主流程，备注注明未交付
- [x] 正向预期逐字段写 sampleResponse；反向预期写 message 或 msg 指出 kind 非法
- [x] 反向预期均写 message 或 msg 指出 kind 非法，未把传输层状态码当作预期主体
- [x] `coverage-fp.md` 已同步 API-01647～01655

**统计**：接口 **3**；用例 **9** 条（主流程 3、备选 3、反向 3）；编号闭区间 **API-01647**～**API-01655**（父控 R2-批13 分配，连续用满）。
