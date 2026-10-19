# 智能服务集群-科技专题服务算法库测试用例（城市对标 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：创新监测 / 城市对标  
> **catalog**：`entry_id=innov.cities` · `catalog_page_id=innov.cities` · path `/innov/cities` · 页标题 M4 城市创新能力  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.cities`  
> **A 线对照**：无对应 Lxx。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（创新监测不在本轮 60 六级）。不改 `work/`  
> **环境**：联调台 50897（本册不写登录、不试调）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批20）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | path | 参数 | 条数 |
|---|------------------------|-------------|--------|------|------|------|
| 1 | 城市排名 | innov.cities.rank | GET | /innov/v1/cities/rank | scope? | 3 |
| 2 | 城市对标 | innov.cities.compare | GET | /innov/v1/cities/compare | cityCodes* | 2 |
| 3 | 政策建议 | innov.cities.advice | GET | /innov/v1/cities/{cityCode}/advice | cityCode* | 2 |
| 4 | 指数方法与权重 | innov.cities.method | GET | /innov/v1/cities/index-method | 无 | 1 |

四个 title 均为 catalog `status=running`。合计 **8** 条：无参 1 条主流程；有参为 1 条主流程（跟 `sampleRequest`）+ 每个可选参数与 sample 相反的传/不传 1 条 + 每个参数 1 条反向。必填反向只省略该参数。

`城市排名` 的 `scope` 可选，`sampleRequest` 传 `scope=global`；与 sample 相反为不传 `scope`；反向为枚举外非法值。`城市对标` 必填 `cityCodes`，主流程用 `sampleRequest` 的 `440300,110000`（params.example 三城不单列）。`政策建议` 必填 path `cityCode`，主流程 `440300`，反向省略 path 段。`指数方法与权重` 无参，仅 1 条主流程。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01875`～`01882`（闭区间用满，不复用 00001～00888）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.cities`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01875 | 创新监测 | 城市对标 | 主流程 | — | 城市对标 | 城市排名 | 城市排名按文档 sampleRequest scope=global 查询 | 1、scope 使用文档示例 global | 1.GET /innov/v1/cities/rank，查询参数取组合 RNK-01 | 1、返回 body 的 data 含 period（string，示例 2025）、list（array，responseFields 城市排名）；2、list 元素含 cityCode（string）、nameZh（string）、indexScore（number）、rankGlobal（number）、rankDomestic（number）、isBenchmark（number）、subScores（object，含 resource、institution、output、environment，均为 number）；3、示例三行：cityCode=US-BOS、nameZh=波士顿、indexScore=94.1、rankGlobal=1、rankDomestic=99、isBenchmark=1、subScores resource=95/institution=92/output=94/environment=90；cityCode=440300、nameZh=深圳、indexScore=88.6、rankGlobal=6、rankDomestic=1、isBenchmark=0、subScores resource=86/institution=84/output=92/environment=88；cityCode=110000、nameZh=北京、indexScore=87.2、rankGlobal=7、rankDomestic=2、isBenchmark=0、subScores resource=90/institution=88/output=85/environment=82 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/cities/rank | M_INNOV_CITY_INDEX | INTEG | | | endpoint_id=innov.cities.rank catalog_page_id=innov.cities 组合=RNK-01 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01876 | 创新监测 | 城市对标 | 备选-参数组合 | 省略 scope | 城市对标 | 城市排名 | 城市排名不传可选 scope（与 sampleRequest 相反） | 1、不传 scope | 1.GET /innov/v1/cities/rank，查询参数取组合 RNK-02 | 1、返回 body 的 data 仍含 period（string）、list（array）；2、list 元素仍含 cityCode、nameZh、indexScore、rankGlobal、rankDomestic、isBenchmark、subScores（resource、institution、output、environment）；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/cities/rank | M_INNOV_CITY_INDEX | INTEG | | | endpoint_id=innov.cities.rank catalog_page_id=innov.cities 组合=RNK-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01877 | 创新监测 | 城市对标 | 异常-入参-非法scope | — | 城市对标 | 城市排名 | 城市排名 scope 非法 | 1、scope 取枚举外值 | 1.GET /innov/v1/cities/rank，查询参数取组合 RNK-03 | 1、返回 body 的 message 或 msg 指出 scope 非法；2、不返回含 list 城市排名的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/cities/rank | | INTEG | | | endpoint_id=innov.cities.rank catalog_page_id=innov.cities 组合=RNK-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01878 | 创新监测 | 城市对标 | 主流程 | — | 城市对标 | 城市对标 | 城市对标按文档 sampleRequest cityCodes=440300,110000 查询 | 1、cityCodes 使用 sampleRequest 440300,110000 | 1.GET /innov/v1/cities/compare，查询参数取组合 CMP-01 | 1、返回 body 的 data 含 list（array，responseFields 对标城市）、radar（array，sampleResponse 多出）；2、list 元素含 cityCode（string）、nameZh（string）、indexScore（number）、rankGlobal（number）、resource（number）、institution（number）、output（number）、environment（number）；3、示例两行：cityCode=440300、nameZh=深圳、indexScore=88.6、rankGlobal=6、resource=86、institution=84、output=92、environment=88；cityCode=110000、nameZh=北京、indexScore=87.2、rankGlobal=7、resource=90、institution=88、output=85、environment=82；4、radar 元素含创新资源、制度环境、创新产出、产业环境（number）；5、示例两行：创新资源=86、制度环境=84、创新产出=92、产业环境=88；创新资源=90、制度环境=88、创新产出=85、产业环境=82 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/cities/compare | | INTEG | | | endpoint_id=innov.cities.compare catalog_page_id=innov.cities 组合=CMP-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01879 | 创新监测 | 城市对标 | 异常-入参-缺cityCodes | — | 城市对标 | 城市对标 | 城市对标不传必填 cityCodes | 1、不传 cityCodes | 1.GET /innov/v1/cities/compare，查询参数取组合 CMP-02 | 1、返回 body 的 message 或 msg 指出 cityCodes 缺失；2、不返回含 list、radar 的成功对标 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/cities/compare | | INTEG | | | endpoint_id=innov.cities.compare catalog_page_id=innov.cities 组合=CMP-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01880 | 创新监测 | 城市对标 | 主流程 | — | 城市对标 | 政策建议 | 政策建议按文档 sampleRequest path cityCode=440300 查询 | 1、path cityCode 使用文档示例 440300 | 1.GET /innov/v1/cities/440300/advice，path 取组合 ADV-01 | 1、返回 body 的 data 含 title（string，responseFields 标题）、contentMd（string，responseFields Markdown 正文）；2、sampleResponse 还含 reportId（string）、generateMode（string）；3、示例 reportId=RPT-SZ-01、title=深圳城市创新能力政策建议、generateMode=rule、contentMd 为「## 建议」及两条「加强基础研究投入」「补齐制度环境短板」 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/cities/{cityCode}/advice | | INTEG | | | endpoint_id=innov.cities.advice catalog_page_id=innov.cities 组合=ADV-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01881 | 创新监测 | 城市对标 | 异常-入参-缺cityCode | — | 城市对标 | 政策建议 | 政策建议不传必填 cityCode | 1、path 不传 cityCode | 1.GET /innov/v1/cities/{cityCode}/advice，path 取组合 ADV-02 | 1、返回 body 的 message 或 msg 指出 cityCode 缺失；2、不返回含 title、contentMd 的成功建议 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/cities/{cityCode}/advice | | INTEG | | | endpoint_id=innov.cities.advice catalog_page_id=innov.cities 组合=ADV-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01882 | 创新监测 | 城市对标 | 主流程 | — | 城市对标 | 指数方法与权重 | 指数方法与权重无参查询返回文档示例中的权重字段 | 1、无业务前置 | 1.GET /innov/v1/cities/index-method（无查询参数） | 1、返回 body 的 data 含 weightVersion（string，示例 city-v1）、methodDesc（string，示例 四要素加权合成。）、weights（array，responseFields 权重展平）；2、weights 元素含 k（string）、desc（string）、w（number）；3、示例四行：k=创新资源、desc=人才与资金、w=0.28；k=制度环境、desc=政策与治理、w=0.22；k=创新产出、desc=论文专利、w=0.3；k=产业环境、desc=产业配套、w=0.2 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/cities/index-method | | INTEG | | | endpoint_id=innov.cities.method catalog_page_id=innov.cities 组合=— 金样 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| RNK-01 | innov.cities.rank | scope=global | 主路径（sampleRequest） |
| RNK-02 | innov.cities.rank | 不传 scope | 省略可选 scope（与 sample 相反） |
| RNK-03 | innov.cities.rank | scope=__invalid__ | 只破坏 scope |
| CMP-01 | innov.cities.compare | cityCodes=440300,110000 | 主路径（sampleRequest） |
| CMP-02 | innov.cities.compare | 不传 cityCodes | 缺必填 cityCodes |
| ADV-01 | innov.cities.advice | path cityCode=440300 | 主路径（sampleRequest） |
| ADV-02 | innov.cities.advice | 不传 path cityCode（请求 `/innov/v1/cities//advice`，path 段为空） | 缺必填 cityCode |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 城市排名 | innov.cities.rank | GET | /innov/v1/cities/rank | scope? | running |
| 城市对标 | innov.cities.compare | GET | /innov/v1/cities/compare | cityCodes* | running |
| 政策建议 | innov.cities.advice | GET | /innov/v1/cities/{cityCode}/advice | cityCode* | running |
| 指数方法与权重 | innov.cities.method | GET | /innov/v1/cities/index-method | — | running |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.cities.rank | API-01875、01876、01877 |
| innov.cities.compare | API-01878、01879 |
| innov.cities.advice | API-01880、01881 |
| innov.cities.method | API-01882 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 4 个 title 均在功能点列出现，且各有 1 条主流程（01875 城市排名、01878 城市对标、01880 政策建议、01882 指数方法与权重）
- [x] 无参指数方法与权重仅 1 条主流程；城市排名 1 主流程 + 省略 scope 1 条 + 非法 scope 1 条；城市对标、政策建议各 1 主流程 + 省略必填 1 条
- [x] 正向预期逐字段写 sampleResponse；反向预期写 message 或 msg 指出该参数缺失或非法
- [x] 无登录 / Token / 401 / 424
- [x] `coverage-fp.md` 已同步 API-01875～01882；A 线写无对应 Lxx
- [ ] `code-registry.yaml` 由父控回写（本子任务未改 registry）

**统计**：用例 **8** 条；主流程 **4**、备选 **1**、反向 **3**；编号闭区间 **API-01875**～**API-01882**（父控 R2-批20 分配）。
