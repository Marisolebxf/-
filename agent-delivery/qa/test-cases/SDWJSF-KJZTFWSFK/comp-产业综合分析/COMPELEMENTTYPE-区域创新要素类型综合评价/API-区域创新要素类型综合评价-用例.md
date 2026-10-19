# 智能服务集群-科技专题服务算法库测试用例（区域创新要素类型综合评价 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业综合分析 / 区域创新要素类型综合评价  
> **catalog**：`entry_id=comp.element-type` · `catalog_page_id=comp.element-type` · path `/industry-comp/element-type`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.element-type`  
> **A 线对照**：`fp-split-by-api-run/work/L56.md`（覆盖矩阵用，禁止 field 一行一用例；未改 work）  
> **环境**：联调台 `http://111.198.38.90:50897/`（接口文档真源 `comp.json` 页 `comp.element-type`；本册不访问）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批18）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | status |
|---|------------------------|-------------|--------|--------|
| 1 | 要素类型 | comp.element-type.main | GET | unavailable |

可选参数只有 `region`（区域编码，string，example `440300`，`required=false`）。`sampleRequest` 含 `region=440300`。主流程跟 sampleRequest。备选与 sample 相反：不传 `region`。反向恰好 1 条：`region=__invalid__`。catalog `status=unavailable`，备注注明未交付，仍按该接口 sampleResponse 编写。path 为 `GET /comp/v1/comp/element-type`，与同模块其它 `element-*` / `region-*` path 分开验收。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01805**～**API-01807**，连续用满；禁止复用 00001～00888）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=comp.element-type`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01805 | 产业综合分析 | 区域创新要素类型综合评价 | 主流程 | — | 区域创新要素类型综合评价 | 要素类型 | 要素类型按文档 sampleRequest 传 region=440300 | 1、region 使用文档示例 440300 | 1.GET /comp/v1/comp/element-type，查询参数取组合 ELEM-01 | 1、返回 body 与 sampleResponse 同层逐字段：index（number，responseFields 类型综合分，示例 73.5）、cov（string，示例 6/7）、weak（number，示例 2）、rank（number，示例 4）；2、radar 为数组，元素含人才（number，示例 79）、企业（number，示例 84）、政策（number，示例 81）、服务机构（number，示例 70）、科研机构（number，示例 66）、资金（number，示例 73）、空间（number，示例 61）；3、bar_items 为数组，元素含 name（string）、value（number），示例企业 84、政策 81、人才 79、资金 73、服务 70、科研 66、空间 61；4、pie_items 为数组，元素含 name（string）、value（number），示例强 3、中 2、弱 2；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例企业/84/1/强/链主与专精特新密集、政策/81/2/强/工具箱完善、空间/61/7/弱/载体饱和度偏高 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/element-type | M_SYNTH_ELEM_TYPE_INDEX | INTEG | | | endpoint_id=comp.element-type.main catalog_page_id=comp.element-type 组合=ELEM-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01806 | 产业综合分析 | 区域创新要素类型综合评价 | 备选-参数组合 | 省略 region | 区域创新要素类型综合评价 | 要素类型 | 要素类型不传可选 region（与 sample 相反） | 1、不传 region | 1.GET /comp/v1/comp/element-type，查询参数取组合 ELEM-02 | 1、返回 body 与 sampleResponse 逐字段同类：index（number，responseFields 类型综合分，示例 73.5）、cov（string，示例 6/7）、weak（number，示例 2）、rank（number，示例 4）；2、radar 为数组，元素含人才（number，示例 79）、企业（number，示例 84）、政策（number，示例 81）、服务机构（number，示例 70）、科研机构（number，示例 66）、资金（number，示例 73）、空间（number，示例 61）；3、bar_items 为数组，元素含 name（string）、value（number），示例企业 84、政策 81、人才 79、资金 73、服务 70、科研 66、空间 61；4、pie_items 为数组，元素含 name（string）、value（number），示例强 3、中 2、弱 2；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例企业/84/1/强/链主与专精特新密集、政策/81/2/强/工具箱完善、空间/61/7/弱/载体饱和度偏高 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/element-type | M_SYNTH_ELEM_TYPE_INDEX | INTEG | | | endpoint_id=comp.element-type.main catalog_page_id=comp.element-type 组合=ELEM-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01807 | 产业综合分析 | 区域创新要素类型综合评价 | 异常-入参-非法region | — | 区域创新要素类型综合评价 | 要素类型 | 要素类型的 region 非法 | 1、region 取非法值 | 1.GET /comp/v1/comp/element-type，查询参数取组合 ELEM-03 | 1、返回 body 的 message 或 msg 指出 region 非法；2、不返回含 index 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/element-type | | INTEG | | | endpoint_id=comp.element-type.main catalog_page_id=comp.element-type 组合=ELEM-03 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| ELEM-01 | comp.element-type.main | region=440300 | 主路径（sampleRequest） |
| ELEM-02 | comp.element-type.main | 不传 region | 省略可选 region（与 sample 相反） |
| ELEM-03 | comp.element-type.main | region=__invalid__ | 只破坏 region |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 要素类型 | comp.element-type.main | GET | /comp/v1/comp/element-type | region? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| comp.element-type.main | API-01805、01806、01807 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 1 个 title「要素类型」在功能点列出现，且有 1 条主流程（API-01805）
- [x] sampleRequest 主流程 + 与 sample 相反的不传 region（API-01806）+ 非法 region 1 条（API-01807）
- [x] 正向预期逐字段写 sampleResponse（index、cov、weak、rank、radar、bar_items、pie_items、rows）；反向预期写 message 或 msg 指出 region 非法
- [x] unavailable 仍按 sampleResponse 写主流程与备选，备注注明文档标记未交付
- [x] 无登录 / Token / 401 / 424
- [x] `coverage-fp.md` 已同步 API-01805～01807；field_key 挂到本页 API 号，未一字段一条用例；未改 A 线 work

**步骤字数**：`1.GET /comp/v1/comp/element-type，查询参数取组合 ELEM-01` 为 49 字。

**预期字数**：正向按 sampleResponse 逐字段展开，单条超过 60 字（本页条数锁定 3，不再拆条）。反向 2 点，指出 region 非法。

**统计**：接口 **1**；用例 **3** 条（主流程 1、备选 1、反向 1）；编号闭区间 **API-01805**～**API-01807**（父控 R2-批18 分配，连续用满）。
