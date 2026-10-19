# 智能服务集群-科技专题服务算法库测试用例（区域产业创新人才综合评价 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业综合分析 / 区域产业创新人才综合评价  
> **catalog**：`entry_id=comp.talent-outcome` · `catalog_page_id=comp.talent-outcome` · path `/industry-comp/talent-outcome`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.talent-outcome`  
> **A 线对照**：`fp-split-by-api-run/work/L53.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：联调台 `http://111.198.38.90:50897/`（本册只读 catalog，不打开该地址）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批17 重派）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | status |
|---|------------------------|-------------|--------|--------|
| 1 | 人才成果评价 | comp.talent-outcome.main | GET | unavailable |
| 2 | 区域产业创新人才综合评价模型 | comp.talent-outcome.m_synth_184_1 | POST | available |

两个接口的可选参数都是 `region`（区域编码，string，example `440300`）、`year`（年份，integer，example `2025`）。`sampleRequest` 均含 `region=440300`、`year=2025`。主流程跟 sampleRequest。备选与 sample 相反：不传 `region`（`year` 保持 2025）、不传 `year`（`region` 保持 440300）。每个参数恰好 1 条非法反向（`region=__invalid__` 或 `year=not-a-year`），另一参数保持文档合法值。`人才成果评价` 的 catalog `status=unavailable`，备注注明未交付，仍按该接口 sampleResponse 编写。

`GET /comp/v1/comp/region-talent-outcome` 只挂 title「人才成果评价」。`POST /entan/v1/synth-metric/metric/M_SYNTH_184_1/compute` 只挂 title「区域产业创新人才综合评价模型」。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01782**～**API-01791**，连续用满；禁止复用 00001～00888）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=comp.talent-outcome`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01782 | 产业综合分析 | 区域产业创新人才综合评价 | 主流程 | — | 区域产业创新人才综合评价 | 人才成果评价 | 人才成果评价按文档 sampleRequest 传 region=440300、year=2025 | 1、region 使用文档示例 440300；year 使用文档示例 2025 | 1.GET /comp/v1/comp/region-talent-outcome，查询参数取组合 TAL-01 | 1、返回 body 与 sampleResponse 同层逐字段：index（number，人才指数，示例 66.3）、rank（number，示例 4）、yoy（string，示例 +8.0%）、adv（number，示例 1）；2、radar 为数组，元素含人才规模（number，示例 62）、人才结构（number，示例 71）、人才成果（number，示例 66）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76、苏州 74；4、pie_items 为数组，元素含 name（string）、value（number），示例人才规模 33、人才结构 34、人才成果 33；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例深圳 92/1/领先/综合优势突出、北京 90/2/领先/科研密度高、上海 88/3/领先/产业化强、杭州 79/4/跟进/数字经济拉动 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-talent-outcome | M_SYNTH_184_1 | INTEG | | | endpoint_id=comp.talent-outcome.main catalog_page_id=comp.talent-outcome 组合=TAL-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01783 | 产业综合分析 | 区域产业创新人才综合评价 | 备选-参数组合 | 省略 region | 区域产业创新人才综合评价 | 人才成果评价 | 人才成果评价不传可选 region、year 保持 2025（与 sample 相反） | 1、不传 region；year=2025 | 1.GET /comp/v1/comp/region-talent-outcome，查询参数取组合 TAL-02 | 1、返回 body 与 sampleResponse 逐字段同类：index（number，人才指数，示例 66.3）、rank（number，示例 4）、yoy（string，示例 +8.0%）、adv（number，示例 1）；2、radar 为数组，元素含人才规模、人才结构、人才成果（number，示例 62、71、66）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76、苏州 74；4、pie_items 为数组，元素含 name（string）、value（number），示例人才规模 33、人才结构 34、人才成果 33；5、rows 为数组，元素含 name、score、rank、tag、note，示例深圳 92/1/领先/综合优势突出、北京 90/2/领先/科研密度高、上海 88/3/领先/产业化强、杭州 79/4/跟进/数字经济拉动 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-talent-outcome | M_SYNTH_184_1 | INTEG | | | endpoint_id=comp.talent-outcome.main catalog_page_id=comp.talent-outcome 组合=TAL-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01784 | 产业综合分析 | 区域产业创新人才综合评价 | 备选-参数组合 | 省略 year | 区域产业创新人才综合评价 | 人才成果评价 | 人才成果评价不传可选 year、region 保持 440300（与 sample 相反） | 1、region=440300；不传 year | 1.GET /comp/v1/comp/region-talent-outcome，查询参数取组合 TAL-03 | 1、返回 body 与 sampleResponse 逐字段同类：index（number，人才指数，示例 66.3）、rank（number，示例 4）、yoy（string，示例 +8.0%）、adv（number，示例 1）；2、radar 为数组，元素含人才规模、人才结构、人才成果（number，示例 62、71、66）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76、苏州 74；4、pie_items 为数组，元素含 name（string）、value（number），示例人才规模 33、人才结构 34、人才成果 33；5、rows 为数组，元素含 name、score、rank、tag、note，示例深圳 92/1/领先/综合优势突出、北京 90/2/领先/科研密度高、上海 88/3/领先/产业化强、杭州 79/4/跟进/数字经济拉动 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-talent-outcome | M_SYNTH_184_1 | INTEG | | | endpoint_id=comp.talent-outcome.main catalog_page_id=comp.talent-outcome 组合=TAL-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01785 | 产业综合分析 | 区域产业创新人才综合评价 | 异常-入参-非法region | — | 区域产业创新人才综合评价 | 人才成果评价 | 人才成果评价 region 非法，year 保持文档示例 2025 | 1、year 保持文档示例 2025 | 1.GET /comp/v1/comp/region-talent-outcome，查询参数取组合 TAL-04 | 1、返回 body 的 message 或 msg 指出 region 非法；2、不返回含 index 或 rows 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-talent-outcome | | INTEG | | | endpoint_id=comp.talent-outcome.main catalog_page_id=comp.talent-outcome 组合=TAL-04 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01786 | 产业综合分析 | 区域产业创新人才综合评价 | 异常-入参-非法year | — | 区域产业创新人才综合评价 | 人才成果评价 | 人才成果评价 year 非法，region 保持文档示例 440300 | 1、region 保持文档示例 440300 | 1.GET /comp/v1/comp/region-talent-outcome，查询参数取组合 TAL-05 | 1、返回 body 的 message 或 msg 指出 year 非法；2、不返回含 index 或 rows 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-talent-outcome | | INTEG | | | endpoint_id=comp.talent-outcome.main catalog_page_id=comp.talent-outcome 组合=TAL-05 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01787 | 产业综合分析 | 区域产业创新人才综合评价 | 主流程 | — | 区域产业创新人才综合评价 | 区域产业创新人才综合评价模型 | 区域产业创新人才综合评价模型按文档 sampleRequest 传 region=440300、year=2025 计算 | 1、region 使用文档示例 440300；year 使用文档示例 2025 | 1.POST /entan/v1/synth-metric/metric/M_SYNTH_184_1/compute，请求体取组合 M184-01 | 1、返回 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_SYNTH_184_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 声明 index（number，人才指数），返回中应有该字段；3、结构与 sampleResponse 一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_184_1/compute | M_SYNTH_184_1 | INTEG | | | endpoint_id=comp.talent-outcome.m_synth_184_1 catalog_page_id=comp.talent-outcome 组合=M184-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01788 | 产业综合分析 | 区域产业创新人才综合评价 | 备选-参数组合 | 省略 region | 区域产业创新人才综合评价 | 区域产业创新人才综合评价模型 | 区域产业创新人才综合评价模型不传可选 region、year 保持 2025（与 sample 相反） | 1、不传 region；year=2025 | 1.POST /entan/v1/synth-metric/metric/M_SYNTH_184_1/compute，请求体取组合 M184-02 | 1、返回 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_SYNTH_184_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 所列 index（number，人才指数）仍应出现 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_184_1/compute | M_SYNTH_184_1 | INTEG | | | endpoint_id=comp.talent-outcome.m_synth_184_1 catalog_page_id=comp.talent-outcome 组合=M184-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01789 | 产业综合分析 | 区域产业创新人才综合评价 | 备选-参数组合 | 省略 year | 区域产业创新人才综合评价 | 区域产业创新人才综合评价模型 | 区域产业创新人才综合评价模型不传可选 year、region 保持 440300（与 sample 相反） | 1、region=440300；不传 year | 1.POST /entan/v1/synth-metric/metric/M_SYNTH_184_1/compute，请求体取组合 M184-03 | 1、返回 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_SYNTH_184_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 所列 index（number，人才指数）仍应出现 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_184_1/compute | M_SYNTH_184_1 | INTEG | | | endpoint_id=comp.talent-outcome.m_synth_184_1 catalog_page_id=comp.talent-outcome 组合=M184-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01790 | 产业综合分析 | 区域产业创新人才综合评价 | 异常-入参-非法region | — | 区域产业创新人才综合评价 | 区域产业创新人才综合评价模型 | 区域产业创新人才综合评价模型 region 非法，year 保持文档示例 2025 | 1、year 保持文档示例 2025 | 1.POST /entan/v1/synth-metric/metric/M_SYNTH_184_1/compute，请求体取组合 M184-04 | 1、返回 body 的 message 或 msg 指出 region 非法；2、不返回含 index 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_184_1/compute | | INTEG | | | endpoint_id=comp.talent-outcome.m_synth_184_1 catalog_page_id=comp.talent-outcome 组合=M184-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01791 | 产业综合分析 | 区域产业创新人才综合评价 | 异常-入参-非法year | — | 区域产业创新人才综合评价 | 区域产业创新人才综合评价模型 | 区域产业创新人才综合评价模型 year 非法，region 保持文档示例 440300 | 1、region 保持文档示例 440300 | 1.POST /entan/v1/synth-metric/metric/M_SYNTH_184_1/compute，请求体取组合 M184-05 | 1、返回 body 的 message 或 msg 指出 year 非法；2、不返回含 index 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_184_1/compute | | INTEG | | | endpoint_id=comp.talent-outcome.m_synth_184_1 catalog_page_id=comp.talent-outcome 组合=M184-05 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| TAL-01 | comp.talent-outcome.main | region=440300；year=2025 | 主路径（sampleRequest） |
| TAL-02 | comp.talent-outcome.main | 不传 region；year=2025 | 省略可选 region（与 sample 相反） |
| TAL-03 | comp.talent-outcome.main | region=440300；不传 year | 省略可选 year（与 sample 相反） |
| TAL-04 | comp.talent-outcome.main | region=__invalid__；year=2025 | 只破坏 region |
| TAL-05 | comp.talent-outcome.main | region=440300；year=not-a-year | 只破坏 year（catalog 类型 integer） |
| M184-01 | comp.talent-outcome.m_synth_184_1 | region=440300；year=2025 | 主路径（sampleRequest） |
| M184-02 | comp.talent-outcome.m_synth_184_1 | 不传 region；year=2025 | 省略可选 region（与 sample 相反） |
| M184-03 | comp.talent-outcome.m_synth_184_1 | region=440300；不传 year | 省略可选 year（与 sample 相反） |
| M184-04 | comp.talent-outcome.m_synth_184_1 | region=__invalid__；year=2025 | 只破坏 region |
| M184-05 | comp.talent-outcome.m_synth_184_1 | region=440300；year=not-a-year | 只破坏 year（catalog 类型 integer） |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 人才成果评价 | comp.talent-outcome.main | GET | /comp/v1/comp/region-talent-outcome | region?；year? | unavailable |
| 区域产业创新人才综合评价模型 | comp.talent-outcome.m_synth_184_1 | POST | /entan/v1/synth-metric/metric/M_SYNTH_184_1/compute | region?；year? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| comp.talent-outcome.main | API-01782、01783、01784、01785、01786 |
| comp.talent-outcome.m_synth_184_1 | API-01787、01788、01789、01790、01791 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title 均在功能点列出现，且各有 1 条主流程（01782 人才成果评价、01787 区域产业创新人才综合评价模型）
- [x] 各接口：sampleRequest 主流程 1 条 + 与 sample 相反的不传 region、不传 year 各 1 条备选 + region、year 各 1 条非法反向，各恰好 5 条
- [x] unavailable（人才成果评价）仍按 sampleResponse 逐字段写主流程与备选，备注注明文档标记未交付
- [x] 正向预期逐字段写 sampleResponse；反向预期写 message 或 msg 指出该参数非法
- [x] 无登录 / Token / 401 / 424
- [x] `coverage-fp.md` 已同步 API-01782～01791；field_key 挂到本页 API 号，未一字段一条用例
- [ ] `code-registry.yaml` 由父控回写（本子任务禁改）

**统计**：接口 **2**；用例 **10** 条（主流程 2、备选 4、反向 4）；编号闭区间 **API-01782**～**API-01791**（父控 R2-批17 分配，连续用满）。
