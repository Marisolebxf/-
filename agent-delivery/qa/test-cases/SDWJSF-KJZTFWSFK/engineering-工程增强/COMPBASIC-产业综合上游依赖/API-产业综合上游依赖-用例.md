# 智能服务集群-科技专题服务算法库测试用例（产业综合上游依赖 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：工程增强 / 产业综合上游依赖  
> **catalog**：`entry_id=comp.basic` · `catalog_page_id=comp.basic` · path `/industry-comp/basic`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.basic`  
> **A 线对照**：无对应 Lxx。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `comp.basic`（上游依赖页，非 60 六级模型）。不改 `work/`  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批16）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | status |
|---|------------------------|-------------|--------|--------|
| 1 | 上游依赖与综合研判 | comp.basic.upstream | GET | unavailable |

可选参数 1 个：`region`（区域编码，example `440300`）。`sampleRequest` 含 `region=440300`。备选与 sample 相反：不传 `region`。反向恰好 1 条非法 `region`，不把省略写成反向。path 为 `/comp/v1/comp/upstream-deps`。catalog `status=unavailable`，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01728**～**API-01730**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=comp.basic`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01728 | 工程增强 | 产业综合上游依赖 | 主流程 | — | 产业综合上游依赖 | 上游依赖与综合研判 | 上游依赖与综合研判按文档 sampleRequest 传 region=440300 | 1、region 使用文档示例 440300 | 1.GET /comp/v1/comp/upstream-deps，查询参数取组合 UPD-01 | 1、返回 body 与 sampleResponse 同层逐字段：kpis 为 object（responseFields 活力/要素/协同演示指数），含 vitality（number，示例 76.4）、element（number，示例 71.5）、synergy（number，示例 68.5）；2、upstream 为数组（responseFields 上游七维依赖），元素含 dimension（string）、name（string）、bidSection（string）、menuLabel（string）、ready（boolean）、ready_label（string）；sampleResponse 七条为产业链/产业链基础指标输出/§4.1.1/产业链分析算法库 · 基础指标/true/可消费，技术链/技术基础指标输出/§4.1.2/未挂载算法库/false/待接入，企业/企业基础指标输出/§4.1.3/企业分析算法库 · 基础指标/true/可消费，人才/人才基础指标输出/§4.1.4/未挂载算法库/false/待接入，科研机构/科研机构基础指标输出/§4.1.5/未挂载算法库/false/待接入，政策/政策基础指标输出/§4.1.6/政策分析算法库 · 基础指标/true/可消费，服务机构/服务机构基础指标输出/§4.1.7/产业服务算法库 · 基础指标/true/可消费；3、bar_items 为数组（sampleResponse 多出字段），元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76、苏州 74；4、pie_items 为数组（sampleResponse 多出字段），元素含 name（string）、value（number），示例活力 40、要素 32、协同 28 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/upstream-deps | M_SYNTH_VIT_INDEX | INTEG | | | endpoint_id=comp.basic.upstream catalog_page_id=comp.basic 组合=UPD-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01729 | 工程增强 | 产业综合上游依赖 | 备选-参数组合 | 省略 region | 产业综合上游依赖 | 上游依赖与综合研判 | 上游依赖与综合研判不传可选 region（与 sample 相反） | 1、不传 region | 1.GET /comp/v1/comp/upstream-deps，查询参数取组合 UPD-02 | 1、返回 body 为对象，与 sampleResponse 逐字段同类：kpis 为 object，含 vitality（number，示例 76.4）、element（number，示例 71.5）、synergy（number，示例 68.5）；2、upstream 为数组，元素含 dimension、name、bidSection、menuLabel（string）、ready（boolean）、ready_label（string），七条示例与主流程相同（产业链至服务机构，§4.1.1～§4.1.7）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76、苏州 74；4、pie_items 为数组，元素含 name（string）、value（number），示例活力 40、要素 32、协同 28 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/upstream-deps | M_SYNTH_VIT_INDEX | INTEG | | | endpoint_id=comp.basic.upstream catalog_page_id=comp.basic 组合=UPD-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01730 | 工程增强 | 产业综合上游依赖 | 异常-入参-非法region | — | 产业综合上游依赖 | 上游依赖与综合研判 | 上游依赖与综合研判 region 非法 | 1、无其它查询参数 | 1.GET /comp/v1/comp/upstream-deps，查询参数取组合 UPD-03 | 1、返回 body 的 message 或 msg 指出 region 非法；2、不返回含 kpis.vitality 或 upstream 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/upstream-deps | | INTEG | | | endpoint_id=comp.basic.upstream catalog_page_id=comp.basic 组合=UPD-03 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| UPD-01 | comp.basic.upstream | region=440300 | 主路径（sampleRequest） |
| UPD-02 | comp.basic.upstream | 不传 region | 省略可选 region（与 sample 相反） |
| UPD-03 | comp.basic.upstream | region=__invalid__ | 只破坏 region |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 上游依赖与综合研判 | comp.basic.upstream | GET | /comp/v1/comp/upstream-deps | region? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| comp.basic.upstream | API-01728、01729、01730 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 1 个 title「上游依赖与综合研判」在功能点列出现，且有 1 条主流程（API-01728）
- [x] 与 sample 相反的传/不传 1 条备选：不传 region（01729）
- [x] 参数 region 恰好 1 条非法反向（01730）；省略未写成反向
- [x] unavailable 仍按 sampleResponse 逐字段写主流程与备选，备注注明文档标记未交付
- [x] 反向预期写 message 或 msg 指出 region 非法
- [x] `coverage-fp.md` 已同步 API-01728～01730；A 线写无对应 Lxx

**统计**：接口 **1**；用例 **3** 条（主流程 1、备选 1、反向 1）；编号闭区间 **API-01728**～**API-01730**（父控 R2-批16 分配，连续用满）。
