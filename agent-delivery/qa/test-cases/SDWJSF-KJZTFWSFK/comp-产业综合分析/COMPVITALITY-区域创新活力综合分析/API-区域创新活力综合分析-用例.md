# 智能服务集群-科技专题服务算法库测试用例（区域创新活力综合分析 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业综合分析 / 区域创新活力综合分析  
> **catalog**：`entry_id=comp.vitality` · `catalog_page_id=comp.vitality` · path `/industry-comp/vitality`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.vitality`  
> **A 线对照**：`fp-split-by-api-run/work/L55.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：联调台 `http://111.198.38.90:50897/`（接口文档真源 `comp.json` 页 `comp.vitality`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批18）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | status |
|---|------------------------|-------------|--------|--------|
| 1 | 创新活力 | comp.vitality.main | GET | unavailable |

可选参数 1 个：`region`（区域编码，example `440300`），catalog 为 `required=false`。`sampleRequest` 传 `region=440300`。备选 1 条与 sample 相反：不传 `region`。反向恰好 1 条：非法 `region`。path 为 `GET /comp/v1/comp/region-vitality`。catalog `status=unavailable`，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01802**～**API-01804**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=comp.vitality`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01802 | 产业综合分析 | 区域创新活力综合分析 | 主流程 | — | 区域创新活力综合分析 | 创新活力 | 创新活力按文档 sampleRequest 传 region=440300 返回创新活力字段 | 1、region 使用文档示例 440300 | 1.GET /comp/v1/comp/region-vitality，查询参数取组合 VIT-01 | 1、返回 body 与 sampleResponse 同层逐字段：index（number，responseFields 活力指数，示例 76.4）、rank（number，示例 3）、yoy（string，示例 +8.2%）、cov（number，示例 15）；2、radar 为数组，元素含科技活力（number，示例 81）、产业活力（number，示例 78）、人才活力（number，示例 72）、政策活力（number，示例 74）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76；4、pie_items 为数组，元素含 name（string）、value（number），示例科技 25、产业 25、人才 25、政策 25；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例深圳 score=92 rank=1 tag=领先 note=四维均衡、北京 score=90 rank=2 tag=领先 note=科技/人才强、上海 score=88 rank=3 tag=领先 note=产业/政策强 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-vitality | M_SYNTH_186_1 | INTEG | | | endpoint_id=comp.vitality.main catalog_page_id=comp.vitality 组合=VIT-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01803 | 产业综合分析 | 区域创新活力综合分析 | 备选-参数组合 | 省略 region | 区域创新活力综合分析 | 创新活力 | 创新活力不传可选 region（与 sample 相反） | 1、不传 region | 1.GET /comp/v1/comp/region-vitality，查询参数取组合 VIT-02 | 1、返回 body 仍与 sampleResponse 同层：index（number，示例 76.4）、rank（number，示例 3）、yoy（string，示例 +8.2%）、cov（number，示例 15）；2、radar 为数组，元素含科技活力（number，示例 81）、产业活力（number，示例 78）、人才活力（number，示例 72）、政策活力（number，示例 74）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76；4、pie_items 为数组，元素含 name（string）、value（number），示例科技 25、产业 25、人才 25、政策 25；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），三条示例与主流程相同（深圳四维均衡、北京科技/人才强、上海产业/政策强） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-vitality | M_SYNTH_186_1 | INTEG | | | endpoint_id=comp.vitality.main catalog_page_id=comp.vitality 组合=VIT-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01804 | 产业综合分析 | 区域创新活力综合分析 | 异常-入参-非法region | — | 区域创新活力综合分析 | 创新活力 | 创新活力的 region 非法 | 1、region 取非法值 | 1.GET /comp/v1/comp/region-vitality，查询参数取组合 VIT-03 | 1、返回 body 的 message 或 msg 指出 region 非法；2、不返回含 index 或 rows 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-vitality | | INTEG | | | endpoint_id=comp.vitality.main catalog_page_id=comp.vitality 组合=VIT-03 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| VIT-01 | comp.vitality.main | region=440300 | 主路径（sampleRequest） |
| VIT-02 | comp.vitality.main | 不传 region | 省略可选 region（与 sample 相反） |
| VIT-03 | comp.vitality.main | region=__invalid__ | 只破坏 region |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 创新活力 | comp.vitality.main | GET | /comp/v1/comp/region-vitality | region? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| comp.vitality.main | API-01802、01803、01804 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 1 个 title「创新活力」在功能点列出现，且有 1 条主流程（API-01802）
- [x] 与 sample 相反的传/不传 1 条备选：不传 region（01803）
- [x] 参数 region 恰好 1 条非法反向（01804）；省略未写成反向
- [x] unavailable 仍按 sampleResponse 逐字段写主流程与备选，备注注明文档标记未交付
- [x] 反向预期写 message 或 msg 指出 region 非法
- [x] 无登录 / Token / 401 / 424 用例
- [x] `coverage-fp.md` 已同步 API-01802～01804；A 线 field_key 挂本页 API 号，未改 `work/L55.md`

**统计**：接口 **1**；用例 **3** 条（主流程 1、备选 1、反向 1）；编号闭区间 **API-01802**～**API-01804**（父控 R2-批18 分配，连续用满）。
