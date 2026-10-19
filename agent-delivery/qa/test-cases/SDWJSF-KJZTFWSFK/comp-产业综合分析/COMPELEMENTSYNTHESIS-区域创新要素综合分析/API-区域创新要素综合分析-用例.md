# 智能服务集群-科技专题服务算法库测试用例（区域创新要素综合分析 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业综合分析 / 区域创新要素综合分析  
> **catalog**：`entry_id=comp.element-synthesis` · `catalog_page_id=comp.element-synthesis` · path `/industry-comp/element-synthesis`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.element-synthesis`  
> **A 线对照**：`fp-split-by-api-run/work/L59.md`（覆盖矩阵用，禁止 field 一行一用例；未改 work）  
> **环境**：联调台 `http://111.198.38.90:50897/`（接口文档真源 `comp.json` 页 `comp.element-synthesis`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批19）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | status |
|---|------------------------|-------------|--------|--------|
| 1 | 要素综合 | comp.element-synthesis.main | GET | unavailable |
| 2 | 要素贡献度与影响路径 | comp.element-synthesis.m_synth_elem_contrib | POST | available |

两个接口各只有可选参数 `region`（区域编码，string，required=false，example `440300`）。`sampleRequest` 均传 `region=440300`。主流程跟 sampleRequest。备选与 sample 相反：不传 `region`，各 1 条。反向每个参数 1 条非法：`region=__invalid__`。不把省略写成反向。各恰好 3 条，合计 6。

- 要素综合：`GET /comp/v1/comp/element-synthesis`（查询参数）。catalog `status=unavailable`，备注注明文档标记未交付。与同模块其它 `element-*` path 分开验收。
- 要素贡献度与影响路径：`POST /entan/v1/synth-metric/metric/M_SYNTH_ELEM_CONTRIB/compute`（请求体）。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01814**～**API-01819**，连续用满；禁止复用 00001～00888）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=comp.element-synthesis`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01814 | 产业综合分析 | 区域创新要素综合分析 | 主流程 | — | 区域创新要素综合分析 | 要素综合 | 要素综合按文档 sampleRequest 传 region=440300 | 1、region 使用文档示例 440300 | 1.GET /comp/v1/comp/element-synthesis，查询参数取组合 ESYN-01 | 1、返回 body 与 sampleResponse 同层逐字段：index（number，responseFields 要素综合指数，示例 71.5）、type（number，示例 73.5）、layer（number，示例 69.8）、domain（number，示例 71.2）；2、radar 为数组，元素含类型（number，示例 73.5）、层次（number，示例 69.8）、领域（number，示例 71.2）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 88、北京 86、上海 84、杭州 76、广州 73；4、pie_items 为数组，元素含 name（string）、value（number），示例类型 34、层次 33、领域 33；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例类型维度 score 73.5 rank 1 tag 良好 note 企业/政策强、领域维度 score 71.2 rank 2 tag 良好 note 重点赛道密、层次维度 score 69.8 rank 3 tag 一般 note 应用层偏弱 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/element-synthesis | M_SYNTH_ELEM_INDEX | INTEG | | | endpoint_id=comp.element-synthesis.main catalog_page_id=comp.element-synthesis 组合=ESYN-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01815 | 产业综合分析 | 区域创新要素综合分析 | 备选-参数组合 | 省略 region | 区域创新要素综合分析 | 要素综合 | 要素综合不传可选 region（与 sample 相反） | 1、不传 region | 1.GET /comp/v1/comp/element-synthesis，查询参数取组合 ESYN-02 | 1、返回 body 与 sampleResponse 逐字段同类：index（number，responseFields 要素综合指数，示例 71.5）、type（number，示例 73.5）、layer（number，示例 69.8）、domain（number，示例 71.2）；2、radar 为数组，元素含类型（number，示例 73.5）、层次（number，示例 69.8）、领域（number，示例 71.2）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 88、北京 86、上海 84、杭州 76、广州 73；4、pie_items 为数组，元素含 name（string）、value（number），示例类型 34、层次 33、领域 33；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），三条示例与主流程相同 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/element-synthesis | M_SYNTH_ELEM_INDEX | INTEG | | | endpoint_id=comp.element-synthesis.main catalog_page_id=comp.element-synthesis 组合=ESYN-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01816 | 产业综合分析 | 区域创新要素综合分析 | 异常-入参-非法region | — | 区域创新要素综合分析 | 要素综合 | 要素综合的 region 非法 | 1、region 取非法值 | 1.GET /comp/v1/comp/element-synthesis，查询参数取组合 ESYN-03 | 1、返回 body 的 message 或 msg 指出 region 非法；2、不返回含 index 或 rows 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/element-synthesis | | INTEG | | | endpoint_id=comp.element-synthesis.main catalog_page_id=comp.element-synthesis 组合=ESYN-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01817 | 产业综合分析 | 区域创新要素综合分析 | 主流程 | — | 区域创新要素综合分析 | 要素贡献度与影响路径 | 要素贡献度与影响路径按文档 sampleRequest 传 region=440300 | 1、region 使用文档示例 440300 | 1.POST /entan/v1/synth-metric/metric/M_SYNTH_ELEM_CONTRIB/compute，请求体取组合 ECON-01 | 1、返回 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_SYNTH_ELEM_CONTRIB）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 index（number，要素综合指数），sampleResponse 未给出 index 示例值，返回中应含 index 且类型为 number | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_ELEM_CONTRIB/compute | M_SYNTH_ELEM_CONTRIB | INTEG | | | endpoint_id=comp.element-synthesis.m_synth_elem_contrib catalog_page_id=comp.element-synthesis 组合=ECON-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01818 | 产业综合分析 | 区域创新要素综合分析 | 备选-参数组合 | 省略 region | 区域创新要素综合分析 | 要素贡献度与影响路径 | 要素贡献度与影响路径不传可选 region（与 sample 相反） | 1、不传 region | 1.POST /entan/v1/synth-metric/metric/M_SYNTH_ELEM_CONTRIB/compute，请求体取组合 ECON-02 | 1、返回 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_SYNTH_ELEM_CONTRIB）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 index（number，要素综合指数）仍应出现，类型与主流程一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_ELEM_CONTRIB/compute | M_SYNTH_ELEM_CONTRIB | INTEG | | | endpoint_id=comp.element-synthesis.m_synth_elem_contrib catalog_page_id=comp.element-synthesis 组合=ECON-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01819 | 产业综合分析 | 区域创新要素综合分析 | 异常-入参-非法region | — | 区域创新要素综合分析 | 要素贡献度与影响路径 | 要素贡献度与影响路径的 region 非法 | 1、region 取非法值 | 1.POST /entan/v1/synth-metric/metric/M_SYNTH_ELEM_CONTRIB/compute，请求体取组合 ECON-03 | 1、返回 body 的 message 或 msg 指出 region 非法；2、不返回含 metric_id 或 index 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_ELEM_CONTRIB/compute | | INTEG | | | endpoint_id=comp.element-synthesis.m_synth_elem_contrib catalog_page_id=comp.element-synthesis 组合=ECON-03 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| ESYN-01 | comp.element-synthesis.main | region=440300 | 主路径（sampleRequest） |
| ESYN-02 | comp.element-synthesis.main | 不传 region | 省略可选 region（与 sample 相反） |
| ESYN-03 | comp.element-synthesis.main | region=__invalid__ | 只破坏 region |
| ECON-01 | comp.element-synthesis.m_synth_elem_contrib | region=440300 | 主路径（sampleRequest，请求体） |
| ECON-02 | comp.element-synthesis.m_synth_elem_contrib | 不传 region | 省略可选 region（与 sample 相反） |
| ECON-03 | comp.element-synthesis.m_synth_elem_contrib | region=__invalid__ | 只破坏 region |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 要素综合 | comp.element-synthesis.main | GET | /comp/v1/comp/element-synthesis | region? | unavailable |
| 要素贡献度与影响路径 | comp.element-synthesis.m_synth_elem_contrib | POST | /entan/v1/synth-metric/metric/M_SYNTH_ELEM_CONTRIB/compute | region? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| comp.element-synthesis.main | API-01814、01815、01816 |
| comp.element-synthesis.m_synth_elem_contrib | API-01817、01818、01819 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title 均在功能点列出现，且各有 1 条主流程（01814 要素综合、01817 要素贡献度与影响路径）
- [x] 每个接口：sampleRequest 主流程 + 与 sample 相反的不传 region 备选 + region 1 条非法反向
- [x] 正向预期逐字段写 sampleResponse；反向预期写 message 或 msg 指出 region 非法
- [x] unavailable（要素综合）仍按 sampleResponse 写主流程与备选，备注注明文档标记未交付
- [x] 无登录 / Token / 401 / 424
- [x] `coverage-fp.md` 已同步 API-01814～01819；field_key 挂到本页 API 号，未一字段一条用例；未改 A 线 work

**步骤字数**：GET 步骤为 METHOD + path + 组合 id，53 字。POST 步骤保留同样句式后为 80 字：path `/entan/v1/synth-metric/metric/M_SYNTH_ELEM_CONTRIB/compute` 单独已 58 字，加上 `1.POST ` 与组合 id 即超过 60。按金样保留完整 path 与组合 id。

**统计**：接口 **2**；用例 **6** 条（主流程 2、备选 2、反向 2）；编号闭区间 **API-01814**～**API-01819**（父控 R2-批19，连续用满）。
