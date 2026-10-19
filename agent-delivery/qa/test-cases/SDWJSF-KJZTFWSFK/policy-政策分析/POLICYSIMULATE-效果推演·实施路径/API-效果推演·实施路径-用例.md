# 智能服务集群-科技专题服务算法库测试用例（效果推演 · 实施路径 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：政策分析 / 效果推演 · 实施路径  
> **catalog**：`entry_id=policy.simulate` · `catalog_page_id=policy.simulate` · path `/policy/simulate`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.simulate`  
> **A 线对照**：无对应 Lxx。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.simulate`（不扩六级）。不改 `work/`  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批12）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | status |
|---|------------------------|-------------|--------|--------|
| 1 | 效果推演 | policy.simulate.main | GET | unavailable |
| 2 | 政策效果推演 | policy.simulate.m_policy_simulate | POST | available |

两个接口的可选参数相同：`scope_code`、`scenario_id`、`limit`。`sampleRequest` 均为 `limit=20`，不含 `scope_code`、`scenario_id`。备选各动一个参数，与 sample 相反：传入 `scope_code=440000`（参数说明「如 440000」，亦为 sampleResponse 示例）、传入 `scenario_id=sc_support_up_20`（枚举非空项，亦为 sampleResponse 示例）、不传 `limit`。反向各 1 条非法，不把省略写成反向。GET 走查询参数；POST 走 JSON 请求体。`效果推演` 的 path 为 `/policy/v1/policy/simulate`；`政策效果推演` 的 path 按 catalog 原文为 `/policy/v1/polan/metric/M_POLICY_SIMULATE/compute`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01489**～**API-01502**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.simulate`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01489 | 政策分析 | 效果推演 · 实施路径 | 主流程 | — | 效果推演 · 实施路径 | 效果推演 | 效果推演按文档 sampleRequest 传 limit=20、不传 scope_code 与 scenario_id | 1、limit=20；不传 scope_code；不传 scenario_id | 1.GET /policy/v1/policy/simulate，查询参数取组合 SIM-01 | 1、返回 body 的 data 为数组；2、元素含 scope_code（string）、scenario_id（string）、baseline_value（number）、simulated_value（number，responseFields 推演值）、metric_id（string）；3、与 sampleResponse 逐字段一致，示例第1条 scope_code=440000、scenario_id=sc_support_up_20、baseline_value=70、simulated_value=78.4、metric_id=M_POLICY_SIMULATE | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | M_POLICY_DS_11_POLICY_EVAL_015 | INTEG | | | endpoint_id=policy.simulate.main catalog_page_id=policy.simulate 组合=SIM-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01490 | 政策分析 | 效果推演 · 实施路径 | 备选-参数组合 | 传入 scope_code | 效果推演 · 实施路径 | 效果推演 | 效果推演传入可选 scope_code=440000，limit 保持 sample 的 20、不传 scenario_id | 1、scope_code=440000；不传 scenario_id；limit=20 | 1.GET /policy/v1/policy/simulate，查询参数取组合 SIM-02 | 1、返回 body 的 data 为数组；2、元素仍含 scope_code（string）、scenario_id（string）、baseline_value（number）、simulated_value（number，responseFields 推演值）、metric_id（string）；3、字段与 sampleResponse 逐字段同类，示例值（scope_code=440000、scenario_id=sc_support_up_20、baseline_value=70、simulated_value=78.4、metric_id=M_POLICY_SIMULATE）说明形态 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | M_POLICY_DS_11_POLICY_EVAL_015 | INTEG | | | endpoint_id=policy.simulate.main catalog_page_id=policy.simulate 组合=SIM-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01491 | 政策分析 | 效果推演 · 实施路径 | 备选-参数组合 | 传入 scenario_id | 效果推演 · 实施路径 | 效果推演 | 效果推演传入可选 scenario_id=sc_support_up_20，limit 保持 sample 的 20、不传 scope_code | 1、不传 scope_code；scenario_id=sc_support_up_20；limit=20 | 1.GET /policy/v1/policy/simulate，查询参数取组合 SIM-03 | 1、返回 body 的 data 为数组；2、元素仍含 scope_code（string）、scenario_id（string）、baseline_value（number）、simulated_value（number，responseFields 推演值）、metric_id（string）；3、字段与 sampleResponse 逐字段同类，示例值（scope_code=440000、scenario_id=sc_support_up_20、baseline_value=70、simulated_value=78.4、metric_id=M_POLICY_SIMULATE）说明形态 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | M_POLICY_DS_11_POLICY_EVAL_015 | INTEG | | | endpoint_id=policy.simulate.main catalog_page_id=policy.simulate 组合=SIM-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01492 | 政策分析 | 效果推演 · 实施路径 | 备选-参数组合 | 省略 limit | 效果推演 · 实施路径 | 效果推演 | 效果推演不传可选 limit，亦不传 scope_code 与 scenario_id | 1、不传 scope_code；不传 scenario_id；不传 limit | 1.GET /policy/v1/policy/simulate，查询参数取组合 SIM-04 | 1、返回 body 的 data 为数组；2、元素仍含 scope_code（string）、scenario_id（string）、baseline_value（number）、simulated_value（number，responseFields 推演值）、metric_id（string）；3、字段与 sampleResponse 逐字段同类，示例值（baseline_value=70、simulated_value=78.4、metric_id=M_POLICY_SIMULATE）说明形态 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | M_POLICY_DS_11_POLICY_EVAL_015 | INTEG | | | endpoint_id=policy.simulate.main catalog_page_id=policy.simulate 组合=SIM-04 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01493 | 政策分析 | 效果推演 · 实施路径 | 异常-入参-非法scope_code | — | 效果推演 · 实施路径 | 效果推演 | 效果推演 scope_code 非法，其余保持 sample | 1、不传 scenario_id；limit=20 | 1.GET /policy/v1/policy/simulate，查询参数取组合 SIM-05 | 1、返回 body 的 message 或 msg 指出 scope_code 非法；2、不返回含 simulated_value 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | | INTEG | | | endpoint_id=policy.simulate.main catalog_page_id=policy.simulate 组合=SIM-05 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01494 | 政策分析 | 效果推演 · 实施路径 | 异常-入参-非法scenario_id | — | 效果推演 · 实施路径 | 效果推演 | 效果推演 scenario_id 非法，其余保持 sample | 1、不传 scope_code；limit=20 | 1.GET /policy/v1/policy/simulate，查询参数取组合 SIM-06 | 1、返回 body 的 message 或 msg 指出 scenario_id 非法；2、不返回含 simulated_value 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | | INTEG | | | endpoint_id=policy.simulate.main catalog_page_id=policy.simulate 组合=SIM-06 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01495 | 政策分析 | 效果推演 · 实施路径 | 异常-入参-非法limit | — | 效果推演 · 实施路径 | 效果推演 | 效果推演 limit 非法，其余保持 sample | 1、不传 scope_code；不传 scenario_id | 1.GET /policy/v1/policy/simulate，查询参数取组合 SIM-07 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 simulated_value 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | | INTEG | | | endpoint_id=policy.simulate.main catalog_page_id=policy.simulate 组合=SIM-07 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01496 | 政策分析 | 效果推演 · 实施路径 | 主流程 | — | 效果推演 · 实施路径 | 政策效果推演 | 政策效果推演按文档 sampleRequest 传 limit=20、不传 scope_code 与 scenario_id | 1、请求体 limit=20；不传 scope_code；不传 scenario_id | 1.POST /policy/v1/polan/metric/M_POLICY_SIMULATE/compute，请求体取组合 CMP-01 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，示例 M_POLICY_SIMULATE）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 另含 simulated_value（number，推演值） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_SIMULATE/compute | M_POLICY_SIMULATE | INTEG | | | endpoint_id=policy.simulate.m_policy_simulate catalog_page_id=policy.simulate 组合=CMP-01 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01497 | 政策分析 | 效果推演 · 实施路径 | 备选-参数组合 | 传入 scope_code | 效果推演 · 实施路径 | 政策效果推演 | 政策效果推演传入可选 scope_code=440000，limit 保持 sample 的 20、不传 scenario_id | 1、请求体 scope_code=440000；不传 scenario_id；limit=20 | 1.POST /policy/v1/polan/metric/M_POLICY_SIMULATE/compute，请求体取组合 CMP-02 | 1、返回 body 为对象；2、仍含 metric_id（string，示例 M_POLICY_SIMULATE）、hint（string，示例 真实 compute 响应,以实际调用为准）；3、responseFields 的 simulated_value 为 number（推演值） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_SIMULATE/compute | M_POLICY_SIMULATE | INTEG | | | endpoint_id=policy.simulate.m_policy_simulate catalog_page_id=policy.simulate 组合=CMP-02 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01498 | 政策分析 | 效果推演 · 实施路径 | 备选-参数组合 | 传入 scenario_id | 效果推演 · 实施路径 | 政策效果推演 | 政策效果推演传入可选 scenario_id=sc_support_up_20，limit 保持 sample 的 20、不传 scope_code | 1、请求体不传 scope_code；scenario_id=sc_support_up_20；limit=20 | 1.POST /policy/v1/polan/metric/M_POLICY_SIMULATE/compute，请求体取组合 CMP-03 | 1、返回 body 为对象；2、仍含 metric_id（string，示例 M_POLICY_SIMULATE）、hint（string，示例 真实 compute 响应,以实际调用为准）；3、responseFields 的 simulated_value 为 number（推演值） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_SIMULATE/compute | M_POLICY_SIMULATE | INTEG | | | endpoint_id=policy.simulate.m_policy_simulate catalog_page_id=policy.simulate 组合=CMP-03 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01499 | 政策分析 | 效果推演 · 实施路径 | 备选-参数组合 | 省略 limit | 效果推演 · 实施路径 | 政策效果推演 | 政策效果推演不传可选 limit，亦不传 scope_code 与 scenario_id | 1、请求体不传 scope_code；不传 scenario_id；不传 limit | 1.POST /policy/v1/polan/metric/M_POLICY_SIMULATE/compute，请求体取组合 CMP-04 | 1、返回 body 为对象；2、仍含 metric_id（string，示例 M_POLICY_SIMULATE）、hint（string，示例 真实 compute 响应,以实际调用为准）；3、responseFields 的 simulated_value 为 number（推演值） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_SIMULATE/compute | M_POLICY_SIMULATE | INTEG | | | endpoint_id=policy.simulate.m_policy_simulate catalog_page_id=policy.simulate 组合=CMP-04 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01500 | 政策分析 | 效果推演 · 实施路径 | 异常-入参-非法scope_code | — | 效果推演 · 实施路径 | 政策效果推演 | 政策效果推演 scope_code 非法，其余保持 sample | 1、请求体不传 scenario_id；limit=20 | 1.POST /policy/v1/polan/metric/M_POLICY_SIMULATE/compute，请求体取组合 CMP-05 | 1、返回 body 的 message 或 msg 指出 scope_code 非法；2、不返回含 metric_id 或 simulated_value 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_SIMULATE/compute | | INTEG | | | endpoint_id=policy.simulate.m_policy_simulate catalog_page_id=policy.simulate 组合=CMP-05 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01501 | 政策分析 | 效果推演 · 实施路径 | 异常-入参-非法scenario_id | — | 效果推演 · 实施路径 | 政策效果推演 | 政策效果推演 scenario_id 非法，其余保持 sample | 1、请求体不传 scope_code；limit=20 | 1.POST /policy/v1/polan/metric/M_POLICY_SIMULATE/compute，请求体取组合 CMP-06 | 1、返回 body 的 message 或 msg 指出 scenario_id 非法；2、不返回含 metric_id 或 simulated_value 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_SIMULATE/compute | | INTEG | | | endpoint_id=policy.simulate.m_policy_simulate catalog_page_id=policy.simulate 组合=CMP-06 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01502 | 政策分析 | 效果推演 · 实施路径 | 异常-入参-非法limit | — | 效果推演 · 实施路径 | 政策效果推演 | 政策效果推演 limit 非法，其余保持 sample | 1、请求体不传 scope_code；不传 scenario_id | 1.POST /policy/v1/polan/metric/M_POLICY_SIMULATE/compute，请求体取组合 CMP-07 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 metric_id 或 simulated_value 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_SIMULATE/compute | | INTEG | | | endpoint_id=policy.simulate.m_policy_simulate catalog_page_id=policy.simulate 组合=CMP-07 catalog_status=available |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| SIM-01 | policy.simulate.main | 不传 scope_code；不传 scenario_id；limit=20 | 主路径（sampleRequest）；查询参数 |
| SIM-02 | policy.simulate.main | scope_code=440000；不传 scenario_id；limit=20 | 传入可选 scope_code（sample 不含 scope_code；440000 取参数说明示例） |
| SIM-03 | policy.simulate.main | 不传 scope_code；scenario_id=sc_support_up_20；limit=20 | 传入可选 scenario_id（sample 不含 scenario_id；枚举非空项） |
| SIM-04 | policy.simulate.main | 不传 scope_code；不传 scenario_id；不传 limit | 省略可选 limit（sample 含 limit） |
| SIM-05 | policy.simulate.main | scope_code=__invalid__；不传 scenario_id；limit=20 | 只破坏 scope_code |
| SIM-06 | policy.simulate.main | 不传 scope_code；scenario_id=__invalid__（不在空、sc_support_up_20、sc_support_up_40、sc_coverage_expand）；limit=20 | 只破坏 scenario_id |
| SIM-07 | policy.simulate.main | 不传 scope_code；不传 scenario_id；limit=-1 | 只破坏 limit |
| CMP-01 | policy.simulate.m_policy_simulate | 不传 scope_code；不传 scenario_id；limit=20 | 主路径（sampleRequest）；JSON 请求体 |
| CMP-02 | policy.simulate.m_policy_simulate | scope_code=440000；不传 scenario_id；limit=20 | 传入可选 scope_code（sample 不含 scope_code；440000 取参数说明示例） |
| CMP-03 | policy.simulate.m_policy_simulate | 不传 scope_code；scenario_id=sc_support_up_20；limit=20 | 传入可选 scenario_id（sample 不含 scenario_id；枚举非空项） |
| CMP-04 | policy.simulate.m_policy_simulate | 不传 scope_code；不传 scenario_id；不传 limit | 省略可选 limit（sample 含 limit） |
| CMP-05 | policy.simulate.m_policy_simulate | scope_code=__invalid__；不传 scenario_id；limit=20 | 只破坏 scope_code |
| CMP-06 | policy.simulate.m_policy_simulate | 不传 scope_code；scenario_id=__invalid__（不在空、sc_support_up_20、sc_support_up_40、sc_coverage_expand）；limit=20 | 只破坏 scenario_id |
| CMP-07 | policy.simulate.m_policy_simulate | 不传 scope_code；不传 scenario_id；limit=-1 | 只破坏 limit |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 效果推演 | policy.simulate.main | GET | /policy/v1/policy/simulate | scope_code?；scenario_id?；limit? | unavailable |
| 政策效果推演 | policy.simulate.m_policy_simulate | POST | /policy/v1/polan/metric/M_POLICY_SIMULATE/compute | scope_code?；scenario_id?；limit? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.simulate.main | API-01489、01490、01491、01492、01493、01494、01495 |
| policy.simulate.m_policy_simulate | API-01496、01497、01498、01499、01500、01501、01502 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title「效果推演」「政策效果推演」均在功能点列出现，且各有 1 条主流程（API-01489、API-01496）
- [x] 与 sample 相反的传/不传各 1 条备选：传入 scope_code（01490、01497）、传入 scenario_id（01491、01498）、省略 limit（01492、01499）
- [x] 每个参数恰好 1 条非法反向（01493～01495、01500～01502）；省略未写成反向
- [x] unavailable 的「效果推演」仍按 sampleResponse 写主流程与备选返回字段，备注注明文档标记未交付
- [x] 反向预期写 message 或 msg 指出该参数非法
- [x] `coverage-fp.md` 已同步 API-01489～01502；A 线写无对应 Lxx

**统计**：接口 **2**；用例 **14** 条（主流程 2、备选 6、反向 6）；编号闭区间 **API-01489**～**API-01502**（父控 R2-批12 分配，连续用满）。
