# 智能服务集群-科技专题服务算法库测试用例（区域产业创新成果综合评价 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业综合分析 / 区域产业创新成果综合评价  
> **catalog**：`entry_id=comp.industry-outcome` · `catalog_page_id=comp.industry-outcome` · path `/industry-comp/industry-outcome`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.industry-outcome`  
> **A 线对照**：`fp-split-by-api-run/work/L52.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：联调台 `http://111.198.38.90:50897/`（接口文档真源 `comp.json` 页 `comp.industry-outcome`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批17）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | status |
|---|------------------------|-------------|--------|--------|
| 1 | 产业成果评价 | comp.industry-outcome.main | GET | unavailable |

可选参数 2 个：`region`（区域编码，example `440300`）、`year`（年份，example `2025`），catalog 均为 `required=false`。`sampleRequest` 同时传 `region=440300`、`year=2025`。备选 2 条与 sample 相反：不传 `region`（`year` 保持 2025）、不传 `year`（`region` 保持 440300）。反向恰好 2 条：只非法 `region`、只非法 `year`。path 为 `GET /comp/v1/comp/region-industry-outcome`。catalog `status=unavailable`，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01777**～**API-01781**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=comp.industry-outcome`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01777 | 产业综合分析 | 区域产业创新成果综合评价 | 主流程 | — | 区域产业创新成果综合评价 | 产业成果评价 | 产业成果评价按文档 sampleRequest 传 region=440300、year=2025 返回产业成果字段 | 1、region 使用文档示例 440300；year 使用文档示例 2025 | 1.GET /comp/v1/comp/region-industry-outcome，查询参数取组合 RIO-01 | 1、返回 body 与 sampleResponse 同层逐字段：index（number，responseFields 产业成果指数，示例 66.3）、rank（number，示例 2）、yoy（string，示例 +5.0%）、adv（number，示例 1）；2、radar 为数组，元素含产品服务（number，示例 62）、企业创新（number，示例 71）、服务机构（number，示例 66）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76、苏州 74；4、pie_items 为数组，元素含 name（string）、value（number），示例产品服务 33、企业创新 34、服务机构 33；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例深圳/92/1/领先/综合优势突出、北京/90/2/领先/科研密度高、上海/88/3/领先/产业化强、杭州/79/4/跟进/数字经济拉动 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-industry-outcome | M_SYNTH_183_1 | INTEG | | | endpoint_id=comp.industry-outcome.main catalog_page_id=comp.industry-outcome 组合=RIO-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01778 | 产业综合分析 | 区域产业创新成果综合评价 | 备选-参数组合 | 省略 region | 区域产业创新成果综合评价 | 产业成果评价 | 产业成果评价不传可选 region、year 保持 2025（与 sample 相反） | 1、不传 region；year=2025 | 1.GET /comp/v1/comp/region-industry-outcome，查询参数取组合 RIO-02 | 1、返回 body 仍与 sampleResponse 同层：index（number，示例 66.3）、rank（number，示例 2）、yoy（string，示例 +5.0%）、adv（number，示例 1）；2、radar 为数组，元素含产品服务（number，示例 62）、企业创新（number，示例 71）、服务机构（number，示例 66）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76、苏州 74；4、pie_items 为数组，元素含 name（string）、value（number），示例产品服务 33、企业创新 34、服务机构 33；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例深圳/92/1/领先/综合优势突出、北京/90/2/领先/科研密度高、上海/88/3/领先/产业化强、杭州/79/4/跟进/数字经济拉动 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-industry-outcome | M_SYNTH_183_1 | INTEG | | | endpoint_id=comp.industry-outcome.main catalog_page_id=comp.industry-outcome 组合=RIO-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01779 | 产业综合分析 | 区域产业创新成果综合评价 | 备选-参数组合 | 省略 year | 区域产业创新成果综合评价 | 产业成果评价 | 产业成果评价不传可选 year、region 保持 440300（与 sample 相反） | 1、region=440300；不传 year | 1.GET /comp/v1/comp/region-industry-outcome，查询参数取组合 RIO-03 | 1、返回 body 仍与 sampleResponse 同层：index（number，示例 66.3）、rank（number，示例 2）、yoy（string，示例 +5.0%）、adv（number，示例 1）；2、radar 为数组，元素含产品服务（number，示例 62）、企业创新（number，示例 71）、服务机构（number，示例 66）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76、苏州 74；4、pie_items 为数组，元素含 name（string）、value（number），示例产品服务 33、企业创新 34、服务机构 33；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例深圳/92/1/领先/综合优势突出、北京/90/2/领先/科研密度高、上海/88/3/领先/产业化强、杭州/79/4/跟进/数字经济拉动 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-industry-outcome | M_SYNTH_183_1 | INTEG | | | endpoint_id=comp.industry-outcome.main catalog_page_id=comp.industry-outcome 组合=RIO-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01780 | 产业综合分析 | 区域产业创新成果综合评价 | 异常-入参-非法region | — | 区域产业创新成果综合评价 | 产业成果评价 | 产业成果评价 region 非法 | 1、year=2025 | 1.GET /comp/v1/comp/region-industry-outcome，查询参数取组合 RIO-04 | 1、返回 body 的 message 或 msg 指出 region 非法；2、不返回含 index 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-industry-outcome | | INTEG | | | endpoint_id=comp.industry-outcome.main catalog_page_id=comp.industry-outcome 组合=RIO-04 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01781 | 产业综合分析 | 区域产业创新成果综合评价 | 异常-入参-非法year | — | 区域产业创新成果综合评价 | 产业成果评价 | 产业成果评价 year 非法 | 1、region=440300 | 1.GET /comp/v1/comp/region-industry-outcome，查询参数取组合 RIO-05 | 1、返回 body 的 message 或 msg 指出 year 非法；2、不返回含 index 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-industry-outcome | | INTEG | | | endpoint_id=comp.industry-outcome.main catalog_page_id=comp.industry-outcome 组合=RIO-05 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| RIO-01 | comp.industry-outcome.main | region=440300；year=2025 | 主路径全参（sampleRequest） |
| RIO-02 | comp.industry-outcome.main | 不传 region；year=2025 | 省略可选 region（与 sample 相反） |
| RIO-03 | comp.industry-outcome.main | region=440300；不传 year | 省略可选 year（与 sample 相反） |
| RIO-04 | comp.industry-outcome.main | region=__invalid__；year=2025 | 只破坏 region |
| RIO-05 | comp.industry-outcome.main | region=440300；year=0 | 只破坏 year |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 产业成果评价 | comp.industry-outcome.main | GET | /comp/v1/comp/region-industry-outcome | region?；year? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| comp.industry-outcome.main | API-01777、01778、01779、01780、01781 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 1 个 title「产业成果评价」在功能点列出现，且有 1 条主流程（API-01777）
- [x] 与 sample 相反的传/不传 2 条备选：不传 region（01778）、不传 year（01779）
- [x] 参数 region、year 各恰好 1 条非法反向（01780、01781）；省略未写成反向
- [x] unavailable 仍按 sampleResponse 逐字段写主流程与备选，备注注明文档标记未交付
- [x] 反向预期写 message 或 msg 指出该参数非法
- [x] 无登录 / Token / 401 / 424 用例
- [x] `coverage-fp.md` 已同步 API-01777～01781；A 线 field_key 挂本页 API 号，未改 `work/L52.md`

**统计**：接口 **1**；用例 **5** 条（主流程 1、备选 2、反向 2）；编号闭区间 **API-01777**～**API-01781**（父控 R2-批17 分配，连续用满）。
