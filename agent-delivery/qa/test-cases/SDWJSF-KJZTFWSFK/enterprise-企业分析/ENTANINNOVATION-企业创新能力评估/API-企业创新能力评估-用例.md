# 智能服务集群-科技专题服务算法库测试用例（企业创新能力评估 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 企业创新能力评估  
> **catalog**：`entry_id=entan.innovation` · `catalog_page_id=entan.innovation` · path `/entan/innovation`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/entan.json` · 页 `entan.innovation`  
> **A 线对照**：无对应 Lxx（与 L31 相邻但不扩六级；`_l6-to-catalog-map.yaml` catalog_skip `entan.innovation`；不改 work）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批4）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 创新能力指数（企业集合） | entan.innovation.rank |

仅必填 `enterprise_codes`（array）。主路径取 `sampleRequest` 四元组。无其它参数，不写备选。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01141**～**API-01142**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.innovation`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01141 | 企业分析 | 企业创新能力评估 | 主流程 | — | 企业创新能力评估 | 创新能力指数（企业集合） | 创新能力指数（企业集合）按文档 sampleRequest 传 enterprise_codes 四元组，返回该接口示例字段 | 1、enterprise_codes 取 sampleRequest 四元组 | 1.POST /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute，请求体取组合 INNO-01 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，sampleResponse 多出字段，示例 M_ENT_INNOVATION_INDEX）；metric_name_zh（string，sampleResponse 多出字段，示例 企业创新能力指数）；value（object，sampleResponse 多出字段）；data_source（string，sampleResponse 多出字段，示例 real）；confidence（string，sampleResponse 多出字段，示例 high）；calc_process（object，sampleResponse 多出字段）；2、value.enterprises（array，responseFields 企业创新能力指数明细，嵌套于 value）元素含 org_id（string）、enterprise_name（string）、innovation_index（number）；第1条 org_id=0218337e44ca794fee9850cf1627b03b、enterprise_name=云启智元科技股份有限公司、innovation_index=92.5；第2条 org_id=05dc8024336db695425572625773381b、enterprise_name=星辰半导体香港有限公司、innovation_index=84.1；3、calc_process 含 definition（string，示例 企业创新能力指数）、formula（string，示例 创新投入/产出/可持续三维加权）、source_tables（array，示例 ads.enterprise_score）、model_version（string，示例 entan-v1.0） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute | M_ENT_INNOVATION_INDEX | INTEG | | | endpoint_id=entan.innovation.rank catalog_page_id=entan.innovation 组合=INNO-01 金样 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01142 | 企业分析 | 企业创新能力评估 | 异常-入参-缺enterprise_codes | — | 企业创新能力评估 | 创新能力指数（企业集合） | 创新能力指数（企业集合）不传必填参数 enterprise_codes | 1、请求体不含 enterprise_codes | 1.POST /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute，请求体取组合 INNO-02 | 1、返回 body 的 message 或 msg 指出缺少 enterprise_codes；2、不返回含 innovation_index 的成功业务 body | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute | | INTEG | | | endpoint_id=entan.innovation.rank catalog_page_id=entan.innovation 组合=INNO-02 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| INNO-01 | entan.innovation.rank | enterprise_codes=["0218337e44ca794fee9850cf1627b03b","05dc8024336db695425572625773381b","0551ccfde6aa2b3c52e647e283204040","05ff69620c962ce3bbb852351f077299"] | 主路径全参（sampleRequest） |
| INNO-02 | entan.innovation.rank | 请求体不含 enterprise_codes | 缺必填 enterprise_codes |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 创新能力指数（企业集合） | entan.innovation.rank | POST | /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute | enterprise_codes* | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.innovation.rank | API-01141、01142 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 1 个 title「创新能力指数（企业集合）」在功能点列出现，且有 1 条主流程（功能项=主流程）
- [x] 有参接口：sampleRequest 全参 1 条；必填参数 1 条缺省反向（无其它参数，不写备选）
- [x] unavailable 仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 无鉴权 / Token / 401 / 424 / 契约占位 / 纯 HTTP 4xx 预期
- [x] 无对应 Lxx，不按 field_key 拆用例；`coverage-fp.md` 已同步 API-01141～01142
- [x] 编号使用父控闭区间 API-01141～01142；本子任务不改 code-registry

**统计**：用例 **2** 条（主流程 1、反向 1）；编号闭区间 **API-01141**～**API-01142**（父控 R2-批4 分配）。
