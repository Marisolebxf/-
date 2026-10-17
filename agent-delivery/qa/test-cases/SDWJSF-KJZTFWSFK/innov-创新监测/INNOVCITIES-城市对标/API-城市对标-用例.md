# 智能服务集群-科技专题服务算法库测试用例（城市对标 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：创新监测 / 城市对标  
> **catalog**：`entry_id=innov.cities` · `catalog_page_id=innov.cities` · path `/innov/cities`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.cities`  
> **A 线对照**：`fp-split-by-api-run/work/` 内 **无** `innov.cities` 行（`_l6-to-catalog-map.yaml`：创新监测不在本轮 60 六级）；矩阵按 catalog + `_catalog-snapshot.md`  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`，常见前缀 `/api`） |
| 业务 path | Java REST：`GET /innov/v1/cities/rank` · `GET /innov/v1/cities/compare` · `GET /innov/v1/cities/{cityCode}/advice` · `GET /innov/v1/cities/index-method` |
| 鉴权头 | `Authorization: Bearer <access_token>`（50897 OAuth 密码模式，账号口径见 `lumen-ui-algo-apiview` LoginView）；`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-00799（金样）** 断言 **完整原始信封**（HTTP + `code` + 可解析 `data`）；同册其余用例在前置写「信封规则见 §0，金样见 API-00799」后，可只断言 `data` 载荷或失败态 |
| catalog 状态 | 本页 **4** 个 endpoint 均为 catalog `status=running`、`runtime=java_api`；**禁止**将 `sampleResponse` 中城市名称、indexScore、rankGlobal、子指数分值、雷达维度分值或政策 Markdown 示例正文作为通过条件 |
| scope 语义 | `innov.cities.rank` 的 `scope` 仅 `global` / `domestic`（catalog options） |
| 样例与契约差 | rank/compare 样例含 `period`、`subScores`、`radar` 等；契约 `responseFields` 对 rank/compare 仅声明 `list`，对 advice 仅 `title`、`contentMd`，对 method 仅 `weights`。断言 **只强制 responseFields** |
| 依赖链 | 政策建议合法 `cityCode` 默认 `440300`（catalog example）；对标 `cityCodes` 默认 `440300,110000`；执行期可先调 API-00799，若 `list` 非空则取首条 `cityCode` 替换 advice/compare，须在执行记录注明 |
| 试调 | **本会话未试调**（子任务约束禁止 curl）；执行期按 §0 鉴权与 catalog 复核，observed 仅记入执行记录 |
| 本页 endpoint 数 | **4** |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00799`～`00818`。`路由route` = catalog path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.cities`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00799 | 创新监测 | 城市对标 | 主流程-排行成功 | 城市排名 | 城市对标 | 城市排名 | 城市排名在 scope=global 下返回成功信封与 list 字段 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、断言对象为完整原始响应信封 | 1.GET /innov/v1/cities/rank，查询参数取组合 CIT-RNK-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.list 存在且为 array；5、禁止将 sample 中 indexScore 或 rankGlobal 具体值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M4 城市创新能力 | N/A-技术项 | N/A | /innov/v1/cities/rank | M_INNOV_CITY_INDEX | INTEG | | | endpoint_id=innov.cities.rank catalog_page_id=innov.cities 组合=CIT-RNK-01 金样 §0未试调 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00800 | 创新监测 | 城市对标 | 异常-鉴权 | 城市排名 | 城市对标 | 城市排名 | 城市排名缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.GET /innov/v1/cities/rank，查询参数取组合 CIT-RNK-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务 list 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M4 城市创新能力 | N/A-技术项 | N/A | /innov/v1/cities/rank | | INTEG | | | endpoint_id=innov.cities.rank catalog_page_id=innov.cities 组合=CIT-RNK-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00801 | 创新监测 | 城市对标 | 异常-非法scope | 城市排名 | 城市对标 | 城市排名 | 城市排名 scope 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00799 | 1.GET /innov/v1/cities/rank，查询参数取组合 CIT-RNK-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 list 的成功排行 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M4 城市创新能力 | N/A-技术项 | N/A | /innov/v1/cities/rank | | INTEG | | | endpoint_id=innov.cities.rank catalog_page_id=innov.cities 组合=CIT-RNK-02；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00802 | 创新监测 | 城市对标 | 异常-空scope | 城市排名 | 城市对标 | 城市排名 | 城市排名 scope 为空字符串时返回可识别失败或与省略 scope 可区分 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/cities/rank，查询参数取组合 CIT-RNK-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx），或可与 CIT-RNK-04 省略 scope 的成功语义明确区分；2、不得将空 scope 静默当作 global 并成功返回 sample 排名示例 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M4 城市创新能力 | N/A-技术项 | N/A | /innov/v1/cities/rank | | INTEG | | | endpoint_id=innov.cities.rank catalog_page_id=innov.cities 组合=CIT-RNK-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00803 | 创新监测 | 城市对标 | 备选-domestic | 城市排名 | 城市对标 | 城市排名 | 城市排名 scope=domestic 时响应可解析 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00799 | 1.GET /innov/v1/cities/rank，查询参数取组合 CIT-RNK-05 | 1、HTTP 状态为 200 或 4xx；2、响应体含可解析 code；3、若 code 属成功集合则 data.list 为 array；4、禁止将 sample 国内排名名次作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M4 城市创新能力 | N/A-技术项 | N/A | /innov/v1/cities/rank | M_INNOV_CITY_INDEX | INTEG | | | endpoint_id=innov.cities.rank catalog_page_id=innov.cities 组合=CIT-RNK-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00804 | 创新监测 | 城市对标 | 主流程-对标成功 | 城市对标 | 城市对标 | 城市对标 | 城市对标在合法 cityCodes 下返回 list 契约字段 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00799 | 1.GET /innov/v1/cities/compare，查询参数取组合 CIT-CMP-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.list 存在且为 array | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M4 城市创新能力 | N/A-技术项 | N/A | /innov/v1/cities/compare | | INTEG | | | endpoint_id=innov.cities.compare catalog_page_id=innov.cities 组合=CIT-CMP-01 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00805 | 创新监测 | 城市对标 | 异常-鉴权 | 城市对标 | 城市对标 | 城市对标 | 城市对标缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.GET /innov/v1/cities/compare，查询参数取组合 CIT-CMP-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务 list 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M4 城市创新能力 | N/A-技术项 | N/A | /innov/v1/cities/compare | | INTEG | | | endpoint_id=innov.cities.compare catalog_page_id=innov.cities 组合=CIT-CMP-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00806 | 创新监测 | 城市对标 | 异常-缺必填cityCodes | 城市对标 | 城市对标 | 城市对标 | 城市对标缺少 cityCodes 时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/cities/compare，查询参数取组合 CIT-CMP-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作空 list 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M4 城市创新能力 | N/A-技术项 | N/A | /innov/v1/cities/compare | | INTEG | | | endpoint_id=innov.cities.compare catalog_page_id=innov.cities 组合=CIT-CMP-02；矩阵挂 cityCodes、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00807 | 创新监测 | 城市对标 | 异常-空cityCodes | 城市对标 | 城市对标 | 城市对标 | 城市对标 cityCodes 为空字符串时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/cities/compare，查询参数取组合 CIT-CMP-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得与合法 CSV 主路径成功态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M4 城市创新能力 | N/A-技术项 | N/A | /innov/v1/cities/compare | | INTEG | | | endpoint_id=innov.cities.compare catalog_page_id=innov.cities 组合=CIT-CMP-03；矩阵挂 cityCodes、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00808 | 创新监测 | 城市对标 | 异常-非法cityCodes | 城市对标 | 城市对标 | 城市对标 | 城市对标 cityCodes 明显非法时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/cities/compare，查询参数取组合 CIT-CMP-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法编码当作含可信对标 list 的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M4 城市创新能力 | N/A-技术项 | N/A | /innov/v1/cities/compare | | INTEG | | | endpoint_id=innov.cities.compare catalog_page_id=innov.cities 组合=CIT-CMP-04；矩阵挂 cityCodes、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00809 | 创新监测 | 城市对标 | 主流程-建议成功 | 政策建议 | 城市对标 | 政策建议 | 政策建议在合法 cityCode 下返回 title 与 contentMd | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00799 | 1.GET /innov/v1/cities/440300/advice（path 取组合 CIT-ADV-01） | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.title 存在且为 string；5、data.contentMd 存在且为 string | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M4 城市创新能力 | N/A-技术项 | N/A | /innov/v1/cities/{cityCode}/advice | | INTEG | | | endpoint_id=innov.cities.advice catalog_page_id=innov.cities 组合=CIT-ADV-01 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00810 | 创新监测 | 城市对标 | 异常-鉴权 | 政策建议 | 城市对标 | 政策建议 | 政策建议缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.GET /innov/v1/cities/440300/advice，组合 CIT-ADV-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功 title/contentMd 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M4 城市创新能力 | N/A-技术项 | N/A | /innov/v1/cities/{cityCode}/advice | | INTEG | | | endpoint_id=innov.cities.advice catalog_page_id=innov.cities 组合=CIT-ADV-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00811 | 创新监测 | 城市对标 | 异常-非法cityCode | 政策建议 | 城市对标 | 政策建议 | 政策建议在非法 cityCode 时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/cities/__invalid__/advice（组合 CIT-ADV-02） | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 title/contentMd 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M4 城市创新能力 | N/A-技术项 | N/A | /innov/v1/cities/{cityCode}/advice | | INTEG | | | endpoint_id=innov.cities.advice catalog_page_id=innov.cities 组合=CIT-ADV-02；矩阵挂 cityCode、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00812 | 创新监测 | 城市对标 | 异常-空cityCode | 政策建议 | 城市对标 | 政策建议 | 政策建议 path 段 cityCode 为空占位时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/cities/%20/advice（组合 CIT-ADV-03，path 为空白编码） | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得与合法 440300 成功态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M4 城市创新能力 | N/A-技术项 | N/A | /innov/v1/cities/{cityCode}/advice | | INTEG | | | endpoint_id=innov.cities.advice catalog_page_id=innov.cities 组合=CIT-ADV-03；矩阵挂 cityCode、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00813 | 创新监测 | 城市对标 | 备选-依赖排行cityCode | 政策建议 | 城市对标 | 政策建议 | 政策建议使用排行接口取得的 cityCode 时契约字段可解析 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、已调用 API-00799 且 data.list 非空并记录首条 cityCode，或沿用 §0 默认 440300 | 1.GET /innov/v1/cities/{cityCode}/advice，path 取组合 CIT-ADV-04 | 1、HTTP 状态为 200 或 4xx；2、响应体含可解析 code；3、若 code 属成功集合则 data.title 为 string 且 data.contentMd 为 string | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M4 城市创新能力 | N/A-技术项 | N/A | /innov/v1/cities/{cityCode}/advice | | INTEG | | | endpoint_id=innov.cities.advice catalog_page_id=innov.cities 组合=CIT-ADV-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00814 | 创新监测 | 城市对标 | 主流程-方法成功 | 指数方法与权重 | 城市对标 | 指数方法与权重 | 城市指数方法接口在有效鉴权下返回 weights 契约字段 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00799 | 1.GET /innov/v1/cities/index-method（无查询参数，组合 CIT-METH-01） | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.weights 存在且为 array | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M4 城市创新能力 | N/A-技术项 | N/A | /innov/v1/cities/index-method | | INTEG | | | endpoint_id=innov.cities.method catalog_page_id=innov.cities 组合=CIT-METH-01 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00815 | 创新监测 | 城市对标 | 异常-鉴权 | 指数方法与权重 | 城市对标 | 指数方法与权重 | 城市指数方法接口缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.GET /innov/v1/cities/index-method，组合 CIT-METH-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功 weights 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M4 城市创新能力 | N/A-技术项 | N/A | /innov/v1/cities/index-method | | INTEG | | | endpoint_id=innov.cities.method catalog_page_id=innov.cities 组合=CIT-METH-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00816 | 创新监测 | 城市对标 | 异常-非法查询参数 | 指数方法与权重 | 城市对标 | 指数方法与权重 | 城市指数方法接口携带未登记查询参数时不得误判为契约失败以外的成功形态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/cities/index-method，查询参数取组合 CIT-METH-02 | 1、HTTP 状态为 200 或 4xx；2、响应体含可解析 code；3、若 code 非成功集合则为可识别失败；4、若 code 成功则仍须满足 data.weights 为 array（忽略未知查询键，不设权重数值断言） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M4 城市创新能力 | N/A-技术项 | N/A | /innov/v1/cities/index-method | | INTEG | | | endpoint_id=innov.cities.method catalog_page_id=innov.cities 组合=CIT-METH-02；矩阵挂 _fail（网关忽略或拒绝 observed） |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00817 | 创新监测 | 城市对标 | 备选-权重形态 | 指数方法与权重 | 城市对标 | 指数方法与权重 | 成功信封下 weights 元素形态可解析 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00799 | 1.GET /innov/v1/cities/index-method，组合 CIT-METH-01 | 1、若 code 属成功集合且 data.weights 非空，则首条元素为 object；2、禁止将 sample 中 w=0.28 等具体权重作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M4 城市创新能力 | N/A-技术项 | N/A | /innov/v1/cities/index-method | | INTEG | | | endpoint_id=innov.cities.method catalog_page_id=innov.cities 组合=CIT-METH-01；矩阵挂 weights |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00818 | 创新监测 | 城市对标 | 备选-重复请求 | 指数方法与权重 | 城市对标 | 指数方法与权重 | 连续两次无参请求城市指数方法接口响应均可解析 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00799 | 1.GET /innov/v1/cities/index-method，组合 CIT-METH-01；2.立即重复步骤 1 一次 | 1、两次响应均含可解析 code；2、若两次 code 均成功则 data.weights 均为 array；3、禁止要求两次 weights 内容完全一致 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M4 城市创新能力 | N/A-技术项 | N/A | /innov/v1/cities/index-method | | INTEG | | | endpoint_id=innov.cities.method catalog_page_id=innov.cities 组合=CIT-METH-01 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| CIT-RNK-01 | innov.cities.rank | `scope`: `global`（对齐 catalog example） | 排行主路径 |
| CIT-RNK-02 | innov.cities.rank | `scope`: `__invalid__` | 枚举外 scope |
| CIT-RNK-03 | innov.cities.rank | `scope`: `""`（空字符串） | 空 scope 边界 |
| CIT-RNK-04 | innov.cities.rank | 不传 `scope` | 省略可选 scope；**本轮无独立用例**，与 CIT-RNK-03 对照 observed |
| CIT-RNK-05 | innov.cities.rank | `scope`: `domestic` | 国内榜备选 |
| CIT-CMP-01 | innov.cities.compare | `cityCodes`: `440300,110000`（对齐 catalog example） | 对标主路径 |
| CIT-CMP-02 | innov.cities.compare | 不传 `cityCodes` | 缺必填 |
| CIT-CMP-03 | innov.cities.compare | `cityCodes`: `""` | 空 CSV |
| CIT-CMP-04 | innov.cities.compare | `cityCodes`: `__invalid__` | 非法编码 |
| CIT-CMP-05 | innov.cities.compare | `cityCodes`: `440300,110000,310000` | 三城对标；**本轮无独立用例**，多城边界待 live 试调后补 |
| CIT-ADV-01 | innov.cities.advice | path `cityCode`: `440300`（catalog example） | 政策建议主路径 |
| CIT-ADV-02 | innov.cities.advice | path `cityCode`: `__invalid__` | 非法编码 |
| CIT-ADV-03 | innov.cities.advice | path `cityCode`: 空白（URL 编码 `%20`） | 空占位编码 |
| CIT-ADV-04 | innov.cities.advice | path `cityCode`: 取自 API-00799 首条 `cityCode`，缺省 `440300` | 排行→建议依赖 |
| CIT-METH-01 | innov.cities.method | 无查询参数 | 方法主路径 |
| CIT-METH-02 | innov.cities.method | 未登记查询键 `debug`: `1` | 未知查询参数 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| innov.cities.rank | GET | /innov/v1/cities/rank | running | 无（scope 可选） |
| innov.cities.compare | GET | /innov/v1/cities/compare | running | cityCodes |
| innov.cities.advice | GET | /innov/v1/cities/{cityCode}/advice | running | path cityCode |
| innov.cities.method | GET | /innov/v1/cities/index-method | running | 无 |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.cities.rank | API-00799、00800、00801、00802、00803 |
| innov.cities.compare | API-00804、00805、00806、00807、00808 |
| innov.cities.advice | API-00809、00810、00811、00812、00813 |
| innov.cities.method | API-00814、00815、00816、00817、00818 |

---

## 3. 覆盖自检（§S1）

- [x] 4 个 running endpoint 各 1 条主路径（API-00799、00804、00809、00814），未写 sample 数值通过条件
- [x] 异常-鉴权 4 条（00800、00805、00810、00815）
- [x] rank scope 非法/空 + domestic 备选；compare 缺/空/非法 cityCodes；advice 非法/空 id + 依赖链；method 未知查询 + 形态/重复
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（§0 未试调）
- [x] 金样 1 条且断言完整信封（API-00799）
- [x] 本页 **0** 条 FUNC
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` / `run-log.md` 由父控回写（本子任务 **未改** registry / run-log）

**统计**：用例 **20** 条；编号 **API-00799**～**API-00818**。

---

## 4. §I 交卷自检计数

| 检查项 | 结果 |
|--------|------|
| FUNC 条数 | **0** |
| API 条数 | **20**（00799～00818） |
| 金样（完整信封） | **1**（00799） |
| live 主路径 | **4**（rank/compare/advice/method 各 1） |
| 异常-鉴权 | **4** |
| `_empty` 矩阵 | **4** 行 **未覆盖** |
| `_fail` 矩阵 | **4** 行 **已覆盖**（入参/鉴权哨兵） |
| 步骤以 GET+path 开头（抽检 00799、00806、00811） | **通过** |
| 预期无页面/图表表述（抽检 00800、00809、00817） | **通过** |
| 无一条同时覆盖成功+失败 | **通过** |
| A 线 `work` 检索 `innov.cities` | **0 命中** |
