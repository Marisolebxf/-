# 智能服务集群-科技专题服务算法库测试用例（区域科技创新成果综合评价 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业综合分析 / 区域科技创新成果综合评价  
> **catalog**：`entry_id=comp.tech-outcome` · `catalog_page_id=comp.tech-outcome` · path `/industry-comp/tech-outcome`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.tech-outcome`  
> **A 线对照**：`fp-split-by-api-run/work/L51.md`（覆盖矩阵用，禁止 field 一行一用例；未改 work）  
> **环境**：联调台 `http://111.198.38.90:50897/`（接口文档真源 `comp.json` 页 `comp.tech-outcome`；本册不访问）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批17 重派）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | status |
|---|------------------------|-------------|--------|--------|
| 1 | 科技成果评价 | comp.tech-outcome.main | GET | unavailable |
| 2 | 区域科技创新成果综合评价模型 | comp.tech-outcome.m_synth_182_1 | POST | available |

两个接口的可选参数都是 `region`（区域编码，example `440300`）、`year`（年份，example `2025`）。`sampleRequest` 均含 `region=440300`、`year=2025`。主流程跟 sampleRequest。备选与 sample 相反：不传 `region`（`year` 保持 2025）、不传 `year`（`region` 保持 440300）。每个参数恰好 1 条非法反向（`region=__invalid__` 或 `year=-1`），另一参数保持文档合法值。`科技成果评价` 的 catalog `status=unavailable`，备注注明未交付，仍按该接口 sampleResponse 编写。path 为 `GET /comp/v1/comp/region-tech-outcome`，与同模块其它 `region-*-outcome` 分开验收。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01767**～**API-01776**，连续用满；禁止复用 00001～00888）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=comp.tech-outcome`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01767 | 产业综合分析 | 区域科技创新成果综合评价 | 主流程 | — | 区域科技创新成果综合评价 | 科技成果评价 | 科技成果评价按文档 sampleRequest 传 region=440300、year=2025 | 1、region 使用文档示例 440300；year 使用文档示例 2025 | 1.GET /comp/v1/comp/region-tech-outcome，查询参数取组合 TEC-01 | 1、返回 body 与 sampleResponse 同层逐字段：index（number，responseFields 科技成果指数，示例 66.3）、rank（number，示例 2）、yoy（string，示例 +6.0%）、adv（number，示例 1）；2、radar 为数组，元素含基础科学（number，示例 62）、应用科技（number，示例 71）、科研机构（number，示例 66）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76、苏州 74；4、pie_items 为数组，元素含 name（string）、value（number），示例基础科学 33、应用科技 34、科研机构 33；5、rows 为数组（responseFields 区域明细），元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例深圳/92/1/领先/综合优势突出、北京/90/2/领先/科研密度高、上海/88/3/领先/产业化强、杭州/79/4/跟进/数字经济拉动 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-tech-outcome | M_SYNTH_182_1 | INTEG | | | endpoint_id=comp.tech-outcome.main catalog_page_id=comp.tech-outcome 组合=TEC-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01768 | 产业综合分析 | 区域科技创新成果综合评价 | 备选-参数组合 | 省略 region | 区域科技创新成果综合评价 | 科技成果评价 | 科技成果评价不传可选 region（与 sample 相反），year=2025 | 1、不传 region；year=2025 | 1.GET /comp/v1/comp/region-tech-outcome，查询参数取组合 TEC-02 | 1、返回 body 与 sampleResponse 逐字段同类：index（number，responseFields 科技成果指数，示例 66.3）、rank（number，示例 2）、yoy（string，示例 +6.0%）、adv（number，示例 1）；2、radar 为数组，元素含基础科学（number，示例 62）、应用科技（number，示例 71）、科研机构（number，示例 66）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76、苏州 74；4、pie_items 为数组，元素含 name（string）、value（number），示例基础科学 33、应用科技 34、科研机构 33；5、rows 为数组（responseFields 区域明细），元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例深圳/92/1/领先/综合优势突出、北京/90/2/领先/科研密度高、上海/88/3/领先/产业化强、杭州/79/4/跟进/数字经济拉动 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-tech-outcome | M_SYNTH_182_1 | INTEG | | | endpoint_id=comp.tech-outcome.main catalog_page_id=comp.tech-outcome 组合=TEC-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01769 | 产业综合分析 | 区域科技创新成果综合评价 | 备选-参数组合 | 省略 year | 区域科技创新成果综合评价 | 科技成果评价 | 科技成果评价不传可选 year（与 sample 相反），region=440300 | 1、region=440300；不传 year | 1.GET /comp/v1/comp/region-tech-outcome，查询参数取组合 TEC-03 | 1、返回 body 与 sampleResponse 逐字段同类：index（number，responseFields 科技成果指数，示例 66.3）、rank（number，示例 2）、yoy（string，示例 +6.0%）、adv（number，示例 1）；2、radar 为数组，元素含基础科学（number，示例 62）、应用科技（number，示例 71）、科研机构（number，示例 66）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76、苏州 74；4、pie_items 为数组，元素含 name（string）、value（number），示例基础科学 33、应用科技 34、科研机构 33；5、rows 为数组（responseFields 区域明细），元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例深圳/92/1/领先/综合优势突出、北京/90/2/领先/科研密度高、上海/88/3/领先/产业化强、杭州/79/4/跟进/数字经济拉动 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-tech-outcome | M_SYNTH_182_1 | INTEG | | | endpoint_id=comp.tech-outcome.main catalog_page_id=comp.tech-outcome 组合=TEC-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01770 | 产业综合分析 | 区域科技创新成果综合评价 | 异常-入参-非法region | — | 区域科技创新成果综合评价 | 科技成果评价 | 科技成果评价的 region 非法 | 1、region 取非法值；year=2025 保持合法 | 1.GET /comp/v1/comp/region-tech-outcome，查询参数取组合 TEC-04 | 1、返回 body 的 message 或 msg 指出 region 非法；2、不返回含 index 或 rows 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-tech-outcome | | INTEG | | | endpoint_id=comp.tech-outcome.main catalog_page_id=comp.tech-outcome 组合=TEC-04 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01771 | 产业综合分析 | 区域科技创新成果综合评价 | 异常-入参-非法year | — | 区域科技创新成果综合评价 | 科技成果评价 | 科技成果评价的 year 非法 | 1、year 取非法值；region=440300 保持合法 | 1.GET /comp/v1/comp/region-tech-outcome，查询参数取组合 TEC-05 | 1、返回 body 的 message 或 msg 指出 year 非法；2、不返回含 index 或 rows 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-tech-outcome | | INTEG | | | endpoint_id=comp.tech-outcome.main catalog_page_id=comp.tech-outcome 组合=TEC-05 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01772 | 产业综合分析 | 区域科技创新成果综合评价 | 主流程 | — | 区域科技创新成果综合评价 | 区域科技创新成果综合评价模型 | 区域科技创新成果综合评价模型按文档 sampleRequest 传 region=440300、year=2025 | 1、region 使用文档示例 440300；year 使用文档示例 2025 | 1.POST /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute，请求体取组合 SYN-01 | 1、返回 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_SYNTH_182_1）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 index（number，科技成果指数）、rows（array，区域明细），sampleResponse 未给出这两字段的示例值，返回中应含 index、rows 且类型与声明一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute | M_SYNTH_182_1 | INTEG | | | endpoint_id=comp.tech-outcome.m_synth_182_1 catalog_page_id=comp.tech-outcome 组合=SYN-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01773 | 产业综合分析 | 区域科技创新成果综合评价 | 备选-参数组合 | 省略 region | 区域科技创新成果综合评价 | 区域科技创新成果综合评价模型 | 区域科技创新成果综合评价模型不传可选 region（与 sample 相反），year=2025 | 1、不传 region；year=2025 | 1.POST /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute，请求体取组合 SYN-02 | 1、返回 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_SYNTH_182_1）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 index（number，科技成果指数）、rows（array，区域明细）仍应出现，类型与主流程一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute | M_SYNTH_182_1 | INTEG | | | endpoint_id=comp.tech-outcome.m_synth_182_1 catalog_page_id=comp.tech-outcome 组合=SYN-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01774 | 产业综合分析 | 区域科技创新成果综合评价 | 备选-参数组合 | 省略 year | 区域科技创新成果综合评价 | 区域科技创新成果综合评价模型 | 区域科技创新成果综合评价模型不传可选 year（与 sample 相反），region=440300 | 1、region=440300；不传 year | 1.POST /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute，请求体取组合 SYN-03 | 1、返回 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_SYNTH_182_1）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 index（number，科技成果指数）、rows（array，区域明细）仍应出现，类型与主流程一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute | M_SYNTH_182_1 | INTEG | | | endpoint_id=comp.tech-outcome.m_synth_182_1 catalog_page_id=comp.tech-outcome 组合=SYN-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01775 | 产业综合分析 | 区域科技创新成果综合评价 | 异常-入参-非法region | — | 区域科技创新成果综合评价 | 区域科技创新成果综合评价模型 | 区域科技创新成果综合评价模型的 region 非法 | 1、region 取非法值；year=2025 保持合法 | 1.POST /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute，请求体取组合 SYN-04 | 1、返回 body 的 message 或 msg 指出 region 非法；2、不返回含 metric_id 或 index 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute | | INTEG | | | endpoint_id=comp.tech-outcome.m_synth_182_1 catalog_page_id=comp.tech-outcome 组合=SYN-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01776 | 产业综合分析 | 区域科技创新成果综合评价 | 异常-入参-非法year | — | 区域科技创新成果综合评价 | 区域科技创新成果综合评价模型 | 区域科技创新成果综合评价模型的 year 非法 | 1、year 取非法值；region=440300 保持合法 | 1.POST /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute，请求体取组合 SYN-05 | 1、返回 body 的 message 或 msg 指出 year 非法；2、不返回含 metric_id 或 index 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute | | INTEG | | | endpoint_id=comp.tech-outcome.m_synth_182_1 catalog_page_id=comp.tech-outcome 组合=SYN-05 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| TEC-01 | comp.tech-outcome.main | region=440300；year=2025 | 主路径（sampleRequest） |
| TEC-02 | comp.tech-outcome.main | 不传 region；year=2025 | 省略可选 region（与 sample 相反） |
| TEC-03 | comp.tech-outcome.main | region=440300；不传 year | 省略可选 year（与 sample 相反） |
| TEC-04 | comp.tech-outcome.main | region=__invalid__；year=2025 | 只破坏 region |
| TEC-05 | comp.tech-outcome.main | region=440300；year=-1 | 只破坏 year |
| SYN-01 | comp.tech-outcome.m_synth_182_1 | region=440300；year=2025 | 主路径（sampleRequest，请求体） |
| SYN-02 | comp.tech-outcome.m_synth_182_1 | 不传 region；year=2025 | 省略可选 region（与 sample 相反） |
| SYN-03 | comp.tech-outcome.m_synth_182_1 | region=440300；不传 year | 省略可选 year（与 sample 相反） |
| SYN-04 | comp.tech-outcome.m_synth_182_1 | region=__invalid__；year=2025 | 只破坏 region |
| SYN-05 | comp.tech-outcome.m_synth_182_1 | region=440300；year=-1 | 只破坏 year |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 科技成果评价 | comp.tech-outcome.main | GET | /comp/v1/comp/region-tech-outcome | region?；year? | unavailable |
| 区域科技创新成果综合评价模型 | comp.tech-outcome.m_synth_182_1 | POST | /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute | region?；year? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| comp.tech-outcome.main | API-01767、01768、01769、01770、01771 |
| comp.tech-outcome.m_synth_182_1 | API-01772、01773、01774、01775、01776 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title 均在功能点列出现，且各有 1 条主流程（01767 科技成果评价、01772 区域科技创新成果综合评价模型）
- [x] 每个接口：sampleRequest 主流程 + 每个可选参数与 sample 相反的传/不传（省略 region、省略 year）+ 每参数 1 条非法反向
- [x] 正向预期逐字段写 sampleResponse；反向预期写 message 或 msg 指出该参数非法
- [x] unavailable（科技成果评价）仍按 sampleResponse 写主流程与备选，备注注明文档标记未交付
- [x] 无登录 / Token / 401 / 424
- [x] `coverage-fp.md` 已同步 API-01767～01776；field_key 挂到本页 API 号，未一字段一条用例；未改 A 线 work

**步骤字数**：GET 步骤为 METHOD + path + 组合 id，54 字。POST 步骤保留同样句式后为 72 字：path `/entan/v1/synth-metric/metric/M_SYNTH_182_1/compute` 单独已 51 字，加上 `1.POST ` 为 58 字，再写组合 id 即超过 60。按金样保留完整 path 与组合 id。

**预期字数**：正向按 sampleResponse 逐字段展开，单条超过 60 字（本页条数锁定 10，不再拆条）。反向各 2 点，指出该参数非法。

**统计**：接口 **2**；用例 **10** 条（主流程 2、备选 4、反向 4）；编号闭区间 **API-01767**～**API-01776**（父控 R2-批17 重派，连续用满）。
