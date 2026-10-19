# 智能服务集群-科技专题服务算法库测试用例（企业评估（异步） API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：工程增强 / 企业评估（异步）  
> **catalog**：`entry_id=entan.eval-async` · `catalog_page_id=entan.eval-async` · path `/entan/eval-async`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/entan.json` · 页 `entan.eval-async`  
> **A 线对照**：无对应 Lxx（工程增强，非 60 六级；`_l6-to-catalog-map.yaml` catalog_skip `entan.eval-async`；不改 work）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批4）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 异步评估契约 | entan.eval-async.mock |

必填参数仅 `mode`（string，枚举 technology / business / competitiveness）。主路径取 `sampleRequest`：`mode=technology`。catalog `path` 为空字符串，`status=unavailable`（文档标记未交付）。本页按父控闭区间只写 1 条主流程 + 1 条缺 mode。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01139**～**API-01140**）。`路由route` = catalog `path`（本 endpoint 为空则填（空））；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.eval-async`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01139 | 工程增强 | 企业评估（异步） | 主流程 | — | 企业评估（异步） | 异步评估契约 | 异步评估契约按文档 sampleRequest 传 mode=technology 返回契约示例字段 | 1、mode 使用文档示例 technology | 1.POST （path 为空），请求体取组合 EVAL-01 | 1、返回 body 为对象，含 technology、business、competitiveness 三个对象（与 sampleResponse 一致）；responseFields 的 task_id（string，任务标识）出现在三个对象内；2、technology 含 task_id（string，示例 EVAL-20260730-001）、sub_type（string，technology）、report_status（string，not_created）；enterprises 为数组，元素含 enterprise_code（string）、enterprise_name（string），示例 ORG00000050/智芯科技（深圳）有限公司、ORG00000054/绿能装备制造有限公司；3、technology.summary 含 max_score（number，88.6）、enterprise_count（number，5）、avg_score（number，72.3）、high_risk_count（number，1）；4、technology.result.radar_dimensions 为 string 数组（技术创新、技术人才、技术投入、技术合作、技术转化）；radar_series 为数组，元素含 enterprise_name（string）、values（number 数组），示例智芯 92/88/85/78/90、绿能 55/48/42/50/38；5、technology.result.ranking 为数组，元素含 enterprise_name（string）、score（number）、rank（number），示例智芯 score=88.6 rank=1、绿能 score=46.6 rank=5；6、technology.result.diagnosis_rows 为数组，元素含 enterprise_name（string）、total_score（number）、confidence（string）、gap_text（string），示例智芯 total_score=88.6 confidence=high gap_text=建议加强产业链协同、绿能 total_score=46.6 confidence=low gap_text=研发投入强度偏低；7、business 含 task_id（string，EVAL-20260730-002）、sub_type（string，business）、report_status（string，not_created）；enterprises 元素含 enterprise_code（string，ORG00000050）、enterprise_name（string，智芯科技（深圳）有限公司）；summary 含 max_score（number，85.2）、enterprise_count（number，5）、benchmark_avg_score（number，68.5）；8、business.result.operating_indicators 为数组，元素含 enterprise_name（string）与 indicators 对象（市场 88、产品 90、品牌 82、技术合作 78、产业链覆盖 85、关键环节参与 80，均为 number）；ranking 含 enterprise_name、score（number，85.2）、rank（number，1）；diagnosis_rows 含 enterprise_name、total_score（number，85.2）、confidence（string，high）、gap_text（string，市场与产品表现突出）；9、competitiveness 含 task_id（string，EVAL-20260730-003）、sub_type（string，competitiveness）、report_status（string，not_created）；enterprises 元素含 enterprise_code（ORG00000050）、enterprise_name（智芯科技（深圳）有限公司）；summary 含 max_score（number，85.9）、enterprise_count（number，5）、avg_score（number，66.8）；10、competitiveness.result.radar_dimensions 为 string 数组（创新能力、经营能力、成长能力）；radar_series 元素含 enterprise_name（string）、values（number 数组，智芯 92/88/86，集合均值 75.6/67.0/66.4）；ranking 含 enterprise_name、score（number，88.7）、rank（number，1）；diagnosis_rows 含 enterprise_name、total_score（number，88.7）、confidence（string，high）、gap_text（string，集合龙头） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | （空） | | INTEG | | | endpoint_id=entan.eval-async.mock catalog_page_id=entan.eval-async 组合=EVAL-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01140 | 工程增强 | 企业评估（异步） | 异常-入参-缺mode | — | 企业评估（异步） | 异步评估契约 | 异步评估契约不传必填 mode | 1、请求体不含 mode | 1.POST （path 为空），请求体取组合 EVAL-02 | 1、返回 body 的 message 或 msg 指出缺少 mode；2、不返回含 task_id 的成功契约对象（technology、business、competitiveness） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | （空） | | INTEG | | | endpoint_id=entan.eval-async.mock catalog_page_id=entan.eval-async 组合=EVAL-02 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| EVAL-01 | entan.eval-async.mock | mode=technology（sampleRequest） | 主路径全参 |
| EVAL-02 | entan.eval-async.mock | 请求体不含 mode | 缺必填 mode |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 异步评估契约 | entan.eval-async.mock | POST | （空） | mode* | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.eval-async.mock | API-01139、01140 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 1 个 title「异步评估契约」在功能点列出现，且有 1 条主流程（功能项=主流程）
- [x] 必填 mode：sampleRequest 正向 1 条 + 缺 mode 反向 1 条（父控闭区间恰好 2 条）
- [x] unavailable 仍按 catalog sampleResponse 与 responseFields 逐字段写主流程，备注注明未交付
- [x] 反向预期写 message 或 msg 指出缺 mode
- [x] 无对应 Lxx，不按 field_key 拆用例；`coverage-fp.md` 已同步 API-01139～01140
- [x] 编号使用父控闭区间 API-01139～01140；本子任务不改 code-registry

**统计**：用例 **2** 条（主流程 1、反向 1）；编号闭区间 **API-01139**～**API-01140**（父控 R2-批4 分配）。
