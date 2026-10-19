# 智能服务集群-科技专题服务算法库测试用例（载体分析 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：创新监测 / 载体分析  
> **catalog**：`entry_id=innov.carriers` · `catalog_page_id=innov.carriers` · path `/innov/carriers`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.carriers`  
> **A 线对照**：无对应 Lxx。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（创新监测不在本轮 60 六级）。不改 `work/`  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批20）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 载体排行 | innov.carriers.rank |
| 2 | 载体详情 | innov.carriers.detail |
| 3 | 指数方法与权重 | innov.carriers.method |

**参数口径**：载体排行两个参数均可选；主流程对齐 `sampleRequest`（`pageNum=1`、`pageSize=20`）；与 sample 相反为不传 `pageNum`、不传 `pageSize`；每个参数另 1 条非法。载体详情仅必填 path `carrierId`；主流程对齐 `sampleRequest`（`carrierId=CAR-01`）；必填反向为省略 `carrierId`。指数方法与权重无参，仅 1 条主流程。三接口 catalog `status=running`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01867**～**API-01874**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.carriers`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01867 | 创新监测 | 载体分析 | 主流程 | — | 载体分析 | 载体排行 | 载体排行按文档 sampleRequest pageNum=1、pageSize=20 查询 | 1、pageNum=1；pageSize=20 | 1.GET /innov/v1/carriers/rank，查询参数取组合 RNK-01 | 1、返回 body 的 data 含 total（number，示例 3）、period（string，示例 2025）、list（array，responseFields 排行）；2、list 元素含 carrierId（string）、name（string）、carrierType（string）、indexScore（number）、rankTotal（number）、subScores（object）；3、subScores 含 output、quality、activity、performance（number）；4、示例三行：carrierId=CAR-01、name=清华大学、carrierType=university、indexScore=91.2、rankTotal=1、subScores output=88/quality=93/activity=86/performance=90；carrierId=CAR-02、name=中科院计算所、carrierType=research、indexScore=87.4、rankTotal=2、subScores output=84/quality=90/activity=82/performance=86；carrierId=CAR-03、name=南山孵化器、carrierType=incubator、indexScore=72.8、rankTotal=3、subScores output=70/quality=68/activity=80/performance=74 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/carriers/rank | M_INNOV_CARRIER_INDEX | INTEG | | | endpoint_id=innov.carriers.rank catalog_page_id=innov.carriers 组合=RNK-01 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01868 | 创新监测 | 载体分析 | 备选-参数组合 | 省略 pageNum | 载体分析 | 载体排行 | 载体排行不传可选 pageNum（与 sampleRequest 相反） | 1、pageSize=20 | 1.GET /innov/v1/carriers/rank，查询参数取组合 RNK-02 | 1、返回 body 的 data 仍含 total（number）、period（string）、list（array）；2、list 元素仍含 carrierId、name、carrierType、indexScore、rankTotal、subScores；3、subScores 仍含 output、quality、activity、performance；4、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/carriers/rank | M_INNOV_CARRIER_INDEX | INTEG | | | endpoint_id=innov.carriers.rank catalog_page_id=innov.carriers 组合=RNK-02 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01869 | 创新监测 | 载体分析 | 备选-参数组合 | 省略 pageSize | 载体分析 | 载体排行 | 载体排行不传可选 pageSize（与 sampleRequest 相反） | 1、pageNum=1 | 1.GET /innov/v1/carriers/rank，查询参数取组合 RNK-03 | 1、返回 body 的 data 仍含 total（number）、period（string）、list（array）；2、list 元素仍含 carrierId、name、carrierType、indexScore、rankTotal、subScores；3、subScores 仍含 output、quality、activity、performance；4、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/carriers/rank | M_INNOV_CARRIER_INDEX | INTEG | | | endpoint_id=innov.carriers.rank catalog_page_id=innov.carriers 组合=RNK-03 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01870 | 创新监测 | 载体分析 | 异常-入参-非法pageNum | — | 载体分析 | 载体排行 | 载体排行 pageNum 非法 | 1、pageSize=20 保持合法 | 1.GET /innov/v1/carriers/rank，查询参数取组合 RNK-04 | 1、返回 body 的 message 或 msg 指出 pageNum 非法；2、不返回含 list 排行的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/carriers/rank | | INTEG | | | endpoint_id=innov.carriers.rank catalog_page_id=innov.carriers 组合=RNK-04 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01871 | 创新监测 | 载体分析 | 异常-入参-非法pageSize | — | 载体分析 | 载体排行 | 载体排行 pageSize 非法 | 1、pageNum=1 保持合法 | 1.GET /innov/v1/carriers/rank，查询参数取组合 RNK-05 | 1、返回 body 的 message 或 msg 指出 pageSize 非法；2、不返回含 list 排行的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/carriers/rank | | INTEG | | | endpoint_id=innov.carriers.rank catalog_page_id=innov.carriers 组合=RNK-05 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01872 | 创新监测 | 载体分析 | 主流程 | — | 载体分析 | 载体详情 | 载体详情按文档 sampleRequest 传 path carrierId=CAR-01 | 1、carrierId 使用文档示例 CAR-01 | 1.GET /innov/v1/carriers/{carrierId}，path 取组合 DET-01 | 1、返回 body 的 data 含 info（object，responseFields 基本信息）、trend（array，responseFields 多期指数）、radar（array，sampleResponse 多出字段）；2、info 含 carrierId（string，示例 CAR-01）、name（string，示例 清华大学）、carrierType（string，示例 university）；3、trend 元素含 statPeriod（string）、indexScore（number）、rankTotal（number）；示例三期：statPeriod=2023、indexScore=86.1、rankTotal=2；statPeriod=2024、indexScore=88.7、rankTotal=1；statPeriod=2025、indexScore=91.2、rankTotal=1；4、radar 元素含 成果产出、成果质量、创新活跃、转化绩效（number）；示例 成果产出=88、成果质量=93、创新活跃=86、转化绩效=90 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/carriers/{carrierId} | | INTEG | | | endpoint_id=innov.carriers.detail catalog_page_id=innov.carriers 组合=DET-01 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01873 | 创新监测 | 载体分析 | 异常-入参-缺carrierId | — | 载体分析 | 载体详情 | 载体详情不传必填 carrierId | 1、path 不传 carrierId | 1.GET /innov/v1/carriers/{carrierId}，path 取组合 DET-02 | 1、返回 body 的 message 或 msg 指出 carrierId 缺失；2、不返回含 info、trend 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/carriers/{carrierId} | | INTEG | | | endpoint_id=innov.carriers.detail catalog_page_id=innov.carriers 组合=DET-02 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01874 | 创新监测 | 载体分析 | 主流程 | — | 载体分析 | 指数方法与权重 | 指数方法与权重无参查询返回文档示例中的方法与权重字段 | 1、无业务前置 | 1.GET /innov/v1/carriers/index-method（无查询参数） | 1、返回 body 的 data 含 weightVersion（string，示例 carrier-v1，sampleResponse 多出字段）、methodDesc（string，responseFields 方法说明，示例 AHP 先验 × 熵权客观权重。）、weights（array，responseFields 权重）；2、weights 元素含 k（string）、desc（string）、w（number）；3、示例四行：k=成果产出、desc=论文/专利数量、w=0.28；k=成果质量、desc=高被引与授权、w=0.27；k=创新活跃、desc=近三年增量、w=0.22；k=转化绩效、desc=成果落地、w=0.23 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/carriers/index-method | | INTEG | | | endpoint_id=innov.carriers.method catalog_page_id=innov.carriers 组合=— catalog_status=running |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| RNK-01 | innov.carriers.rank | pageNum=1；pageSize=20 | 主路径全参（sampleRequest） |
| RNK-02 | innov.carriers.rank | 不传 pageNum；pageSize=20 | 省略可选 pageNum（与 sample 相反） |
| RNK-03 | innov.carriers.rank | pageNum=1；不传 pageSize | 省略可选 pageSize（与 sample 相反） |
| RNK-04 | innov.carriers.rank | pageNum=not-a-page；pageSize=20 | 只破坏 pageNum |
| RNK-05 | innov.carriers.rank | pageNum=1；pageSize=not-a-size | 只破坏 pageSize |
| DET-01 | innov.carriers.detail | path carrierId=CAR-01 | 主路径（sampleRequest） |
| DET-02 | innov.carriers.detail | 不传 path carrierId（请求 `/innov/v1/carriers/`，path 段为空） | 缺必填 carrierId |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 载体排行 | innov.carriers.rank | GET | /innov/v1/carriers/rank | pageNum?；pageSize? | running |
| 载体详情 | innov.carriers.detail | GET | /innov/v1/carriers/{carrierId} | carrierId* | running |
| 指数方法与权重 | innov.carriers.method | GET | /innov/v1/carriers/index-method | — | running |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.carriers.rank | API-01867、01868、01869、01870、01871 |
| innov.carriers.detail | API-01872、01873 |
| innov.carriers.method | API-01874 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 3 个 title 均在功能点列出现，且各有 1 条主流程（01867 载体排行、01872 载体详情、01874 指数方法与权重）
- [x] 载体排行 1 主流程 + 省略 pageNum 1 条 + 省略 pageSize 1 条 + 非法 pageNum 1 条 + 非法 pageSize 1 条；载体详情 1 主流程 + 省略 carrierId 1 条；指数方法与权重仅 1 条主流程
- [x] 正向预期逐字段写 sampleResponse；反向预期写 message 或 msg 指出该参数缺失或非法
- [x] 无登录 / Token / 401 / 424
- [x] `coverage-fp.md` 已同步 API-01867～01874；A 线写无对应 Lxx
- [ ] `code-registry.yaml` 由父控回写（本子任务未改 registry）

**统计**：用例 **8** 条；主流程 **3**、备选 **2**、反向 **3**；编号闭区间 **API-01867**～**API-01874**（父控 R2-批20 分配）。
