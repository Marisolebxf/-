# 智能服务集群-科技专题服务算法库测试用例（焦点识别(单个政策) API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：政策分析 / 焦点识别(单个政策)  
> **catalog**：`entry_id=policy.focus-one` · `catalog_page_id=policy.focus-one` · path `/policy/focus-one`  
> **A 线对照**：`fp-split-by-api-run/work/L35.md`（挂接表 `catalog_skip`：本页为 L35 单政策变体，按 path 去重；不把 `policy.focus` 的 field 灌成新用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批9）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 单条焦点识别 | policy.focus-one.main |

参数：`mode?` `title?` `text!` `execution?` `aux?`。`sampleRequest` 五字段都传。正向只写 1 条全参主流程，再对 4 个可选参数各写 1 条「不传」（与 sample 相反），不做全组合。反向 5 条：`text` 缺省，`mode` / `title` / `execution` / `aux` 各 1 条非法。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01409**～**API-01418**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.focus-one`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01409 | 政策分析 | 焦点识别(单个政策) | 主流程 | — | 焦点识别(单个政策) | 单条焦点识别 | 单条焦点识别按文档 sampleRequest 提交 mode、title、text、execution、aux 并返回焦点、堵点与建议字段 | 1、请求体使用文档 sampleRequest（mode=rule，title、text、execution、aux 取示例原文） | 1.POST /policy/v1/policy/analysis/focus-one，请求体取组合 FO1-01 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：mode（string，sampleResponse 多出字段，示例 rule）；focus_list（array，responseFields 焦点词 Tag；第1条 term=集成电路（string）、score=1（number）、evidence=rule（string））；bottleneck_list（array，responseFields 堵点清单；第1条 item=流片补贴兑付率低（string）、evidence=文本/执行措辞（string））；suggestions（array，responseFields 优化建议；第1条 item=补充实施进度（string）、reason=缺执行数据（string））；persisted（boolean，sampleResponse 多出字段，示例 false） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one | M_POLICY_DEEP_166_1 | INTEG | | | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FO1-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01410 | 政策分析 | 焦点识别(单个政策) | 备选-参数组合 | 省略 mode | 焦点识别(单个政策) | 单条焦点识别 | 单条焦点识别省略可选 mode，其余保持 sampleRequest | 1、不传 mode，title、text、execution、aux 保持文档示例 | 1.POST /policy/v1/policy/analysis/focus-one，请求体取组合 FO1-02 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：mode（string，sampleResponse 多出字段，示例 rule）；focus_list（array，responseFields 焦点词 Tag；第1条 term=集成电路（string）、score=1（number）、evidence=rule（string））；bottleneck_list（array，responseFields 堵点清单；第1条 item=流片补贴兑付率低（string）、evidence=文本/执行措辞（string））；suggestions（array，responseFields 优化建议；第1条 item=补充实施进度（string）、reason=缺执行数据（string））；persisted（boolean，sampleResponse 多出字段，示例 false） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one | M_POLICY_DEEP_166_1 | INTEG | | | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FO1-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01411 | 政策分析 | 焦点识别(单个政策) | 备选-参数组合 | 省略 title | 焦点识别(单个政策) | 单条焦点识别 | 单条焦点识别省略可选 title，其余保持 sampleRequest | 1、不传 title，mode、text、execution、aux 保持文档示例 | 1.POST /policy/v1/policy/analysis/focus-one，请求体取组合 FO1-03 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：mode（string，sampleResponse 多出字段，示例 rule）；focus_list（array，responseFields 焦点词 Tag；第1条 term=集成电路（string）、score=1（number）、evidence=rule（string））；bottleneck_list（array，responseFields 堵点清单；第1条 item=流片补贴兑付率低（string）、evidence=文本/执行措辞（string））；suggestions（array，responseFields 优化建议；第1条 item=补充实施进度（string）、reason=缺执行数据（string））；persisted（boolean，sampleResponse 多出字段，示例 false） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one | M_POLICY_DEEP_166_1 | INTEG | | | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FO1-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01412 | 政策分析 | 焦点识别(单个政策) | 备选-参数组合 | 省略 execution | 焦点识别(单个政策) | 单条焦点识别 | 单条焦点识别省略可选 execution，其余保持 sampleRequest | 1、不传 execution，mode、title、text、aux 保持文档示例 | 1.POST /policy/v1/policy/analysis/focus-one，请求体取组合 FO1-04 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：mode（string，sampleResponse 多出字段，示例 rule）；focus_list（array，responseFields 焦点词 Tag；第1条 term=集成电路（string）、score=1（number）、evidence=rule（string））；bottleneck_list（array，responseFields 堵点清单；第1条 item=流片补贴兑付率低（string）、evidence=文本/执行措辞（string））；suggestions（array，responseFields 优化建议；第1条 item=补充实施进度（string）、reason=缺执行数据（string））；persisted（boolean，sampleResponse 多出字段，示例 false） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one | M_POLICY_DEEP_166_1 | INTEG | | | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FO1-04 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01413 | 政策分析 | 焦点识别(单个政策) | 备选-参数组合 | 省略 aux | 焦点识别(单个政策) | 单条焦点识别 | 单条焦点识别省略可选 aux，其余保持 sampleRequest | 1、不传 aux，mode、title、text、execution 保持文档示例 | 1.POST /policy/v1/policy/analysis/focus-one，请求体取组合 FO1-05 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：mode（string，sampleResponse 多出字段，示例 rule）；focus_list（array，responseFields 焦点词 Tag；第1条 term=集成电路（string）、score=1（number）、evidence=rule（string））；bottleneck_list（array，responseFields 堵点清单；第1条 item=流片补贴兑付率低（string）、evidence=文本/执行措辞（string））；suggestions（array，responseFields 优化建议；第1条 item=补充实施进度（string）、reason=缺执行数据（string））；persisted（boolean，sampleResponse 多出字段，示例 false） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one | M_POLICY_DEEP_166_1 | INTEG | | | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FO1-05 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01414 | 政策分析 | 焦点识别(单个政策) | 异常-入参-缺text | — | 焦点识别(单个政策) | 单条焦点识别 | 单条焦点识别不传必填 text | 1、不传 text，mode、title、execution、aux 保持文档示例 | 1.POST /policy/v1/policy/analysis/focus-one，请求体取组合 FO1-06 | 1、返回 body 的 message 或 msg 指出缺少 text；2、不返回含 focus_list 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one | | INTEG | | | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FO1-06 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01415 | 政策分析 | 焦点识别(单个政策) | 异常-入参-非法mode | — | 焦点识别(单个政策) | 单条焦点识别 | 单条焦点识别 mode 取非法值 | 1、仅 mode 取非法值，其余保持 sampleRequest | 1.POST /policy/v1/policy/analysis/focus-one，请求体取组合 FO1-07 | 1、返回 body 的 message 或 msg 指出 mode 非法；2、不返回含 focus_list 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one | | INTEG | | | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FO1-07 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01416 | 政策分析 | 焦点识别(单个政策) | 异常-入参-非法title | — | 焦点识别(单个政策) | 单条焦点识别 | 单条焦点识别 title 取非法类型 | 1、仅 title 取非 string，其余保持 sampleRequest | 1.POST /policy/v1/policy/analysis/focus-one，请求体取组合 FO1-08 | 1、返回 body 的 message 或 msg 指出 title 非法；2、不返回含 focus_list 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one | | INTEG | | | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FO1-08 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01417 | 政策分析 | 焦点识别(单个政策) | 异常-入参-非法execution | — | 焦点识别(单个政策) | 单条焦点识别 | 单条焦点识别 execution 取非法类型 | 1、仅 execution 取非 string，其余保持 sampleRequest | 1.POST /policy/v1/policy/analysis/focus-one，请求体取组合 FO1-09 | 1、返回 body 的 message 或 msg 指出 execution 非法；2、不返回含 focus_list 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one | | INTEG | | | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FO1-09 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01418 | 政策分析 | 焦点识别(单个政策) | 异常-入参-非法aux | — | 焦点识别(单个政策) | 单条焦点识别 | 单条焦点识别 aux 取非法类型 | 1、仅 aux 取非 string，其余保持 sampleRequest | 1.POST /policy/v1/policy/analysis/focus-one，请求体取组合 FO1-10 | 1、返回 body 的 message 或 msg 指出 aux 非法；2、不返回含 focus_list 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one | | INTEG | | | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FO1-10 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| FO1-01 | policy.focus-one.main | mode=rule；title=深圳市加快集成电路产业发展若干措施；text=推进先进封装产业化，支持科技型中小企业流片补贴。；execution=流片补贴兑付率低，仅完成计划40%。；aux=行业解读认为先进封装是下一阶段焦点。 | 主路径全参（sampleRequest） |
| FO1-02 | policy.focus-one.main | 不传 mode；title、text、execution、aux 同 FO1-01 | 省略可选 mode（sample 含 mode） |
| FO1-03 | policy.focus-one.main | 不传 title；mode、text、execution、aux 同 FO1-01 | 省略可选 title（sample 含 title） |
| FO1-04 | policy.focus-one.main | 不传 execution；mode、title、text、aux 同 FO1-01 | 省略可选 execution（sample 含 execution） |
| FO1-05 | policy.focus-one.main | 不传 aux；mode、title、text、execution 同 FO1-01 | 省略可选 aux（sample 含 aux） |
| FO1-06 | policy.focus-one.main | 不传 text；mode、title、execution、aux 同 FO1-01 | 缺必填 text |
| FO1-07 | policy.focus-one.main | mode=__invalid__（不在 rule、llm）；title、text、execution、aux 同 FO1-01 | 只破坏 mode |
| FO1-08 | policy.focus-one.main | title=0（number，非 string）；mode、text、execution、aux 同 FO1-01 | 只破坏 title |
| FO1-09 | policy.focus-one.main | execution=0（number，非 string）；mode、title、text、aux 同 FO1-01 | 只破坏 execution |
| FO1-10 | policy.focus-one.main | aux=0（number，非 string）；mode、title、text、execution 同 FO1-01 | 只破坏 aux |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 单条焦点识别 | policy.focus-one.main | POST | /policy/v1/policy/analysis/focus-one | mode?；title?；text*；execution?；aux? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.focus-one.main | API-01409、01410、01411、01412、01413、01414、01415、01416、01417、01418 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 1 个 title「单条焦点识别」在功能点列出现，且有 1 条主流程（API-01409）
- [x] 可选 mode / title / execution / aux 各 1 条与 sample 相反的不传（API-01410～01413）；未做全组合，未另写 mode=llm
- [x] 反向恰好 5 条：缺 text（01414），非法 mode / title / execution / aux（01415～01418）；预期写 message 或 msg 指出该参数
- [x] unavailable 仍按 sampleResponse 写主流程与备选返回字段，备注注明文档标记未交付
- [x] 功能项只用主流程、备选-参数组合、异常-入参-*；预期主体是返回字段或该参数的 message/msg
- [x] 未把 L35 中 GET `/policy/v1/policy/analysis/focus` 的 field 写成用例
- [x] `coverage-fp.md` 已同步 API-01409～01418

**统计**：接口 **1**；用例 **10** 条（主流程 1、备选 4、反向 5）；编号闭区间 **API-01409**～**API-01418**（父控 R2-批9 分配）。
