# QA-TOPIC-BUGFIX-API-DICT-L01 · A 类编码泄漏根因（接口 VO / 字典）

## 任务认领

| 字段 | 值 |
|------|-----|
| task-id | `QA-TOPIC-BUGFIX-API-DICT-L01`（bugfix，P0，lumen-topic-py） |
| claimed_by / supervised_by | `agent:api-agent` / `human:徐滕强` |
| claim_type | `pull`（2026-10-29 22:14 认领，MCP task-claim 落 supervised_by；**claim_type 字段为 MCP 工具缺口未落 registry，以此行为准**） |
| ponytail | `full` |
| 业务仓 commit | `lumen-topic-py 40eb2e7`（**本地未 push**，按 2026-10-20 人工验收闸门待走查） |

前置：与 `QA-TOPIC-BUGFIX-FE-L01` 字段对齐；前端兜底已落地，本单修根因后可评估删兜底。

## 问题清单与修复实现

| BUG-ID | 接口/场景 | 根因 | 修复（lumen-topic-py） |
|--------|-----------|------|------------------------|
| 027-002 | `POST /internal/gkx-search/key-analysis/region-insight` → `type_structure[].tag_name` | 聚合 key（编码）直接填 tag_name | 新增 `_TAG_ZH` + `_tag_name()`（key_analysis.py）；7 白名单码出中文，`foreign`/`sme` 旧码别名兼容，缺项回落原码 |
| 027-007 | `POST .../sz-status/city-benchmark` → `rows[].object_name` | DWD 缺行时回落城市码 | 新增 `_CITY_NAME_FALLBACK`（深圳/北京/上海/苏州/广州/全国）+ `_city_name()`（sz_status.py）；指标仍诚实 `None`/无数据，仅名称回显 |
| 028-004 | `sz-status/enterprise-list` + `profile/basic` | **契约两端字段已齐**（Python `name_cn`、Java `nameCn` 均在） | 无需代码改动；残留案例疑为 ES 文档缺 `name_cn`，待联调复现后按 D16 登记数据缺口，不伪闭合 |
| 028-006/008 | 招引/培育推荐结果契约 | 无可读回显，前端拼 raw key | `_enrich_recommend_result`（recommend.py）新增 `weights_readable`（中文名+权重降序）与 `submitted_filters_readable`（键名+值译中文，INB 码走 DWD chain 码表，去重）；原 snake 键全部保留 |

Java 门面（gkxlumen-topic-enterprise）DTO 字段齐备、`Map` 透传，**无 Java 改动**；调用链 前端→Java REST→Python `/internal` 未越层。

中文名对齐源：前端 `COMPARE_BASKET_TYPE_TAG_FALLBACK`（lumen-ui-topic `src/config/enterpriseTypeContext.ts`）、`WEIGHT_DIMENSIONS`（useRecruit.ts）、`recruitResultMap` 维度标签；`little_giant=专精特新`、`specialized_new=专精特新企业`（避免饼图双扇区同名）。

## 验证

- 新增自检 `tests/test_qa_topic_bugfix_api_dict.py`：**7/7 通过**（中文名、城市兜底、权重回显排序、筛选回显+去重+HTTP 打桩、无参数不误出键、字典单源守卫、HTTP 契约守卫）。
- 全量回归 `pytest tests/`：**305 passed** / 2 skipped；**3 个存量失败与本单无关**（`test_meta_chains_fallback_when_db_empty` 等，stash 验证改动前即失败：meta 兜底用例与 `_CHAIN_FALLBACK` 断言不匹配，属 DATA-INDUSTRY-NODE-DICT-L02 遗留，建议另行派修）。
- 测试还抓出并修掉一个实现 bug：地理筛选键（region_ids 等）漏出回显。

## 评审修正轮（2026-10-29 深度 review 后，commit `4945207`）

深度评审（[记录](708f21c8-bd6f-4408-8f03-dee1ad983953)）抓出 1 Critical + 2 Important，处置如下：

| 级别 | 问题 | 处置 |
|------|------|------|
| Critical | `Dockerfile.ai` 仅 COPY `gkx_common/gkx_ai_service/gkx_ai_worker`，跨包 import `gkx_search_service.views.meta` 线上必 ModuleNotFoundError，INB 翻译静默降级原码（本地测试因 repo 在 sys.path 全绿遮蔽） | `_chain_names()` 改走 search 服务 HTTP `POST /internal/gkx-search/meta/chains`（对齐 `search_client.fetch_by_codes` 既有模式，同 `GKX_SEARCH_BASE_URL`）；测试加源码守卫断言防跨包 import 复活 |
| Important | city-insight（`sz_status.py`）同函数同数据源的城市编码回落未一并修 | 3 处（advantages/shortboards comment + sz/compare_city_name）统一 `_city_name()` |
| Important | enrich 只覆盖 live 查询路径；回调/Kafka 存量结果无可读键 | 已核实 Java `TalentRecommendAnalysisAdapterImpl.queryResult` 走 live `/tasks/result`（主链路覆盖）；存量路径登记为跟进项，不阻塞 |
| Minor | detail 字典与 key_analysis 字典漂移（detail 缺 specialized_new/listed/chain_leader/foreign_invested/small_micro，detail 页今天就在漏编码） | 三处字典收敛 `gkx_common/dicts.py::tag_name` 单源；守卫测试锁定同源；detail 4 码缺口顺带闭合 |
| Minor | city-benchmark 有行分支 `r["city_name"]` 为 NULL 时 object_name=null | 统一 `_city_name(city_code, r)` |

遗留跟进（登记不阻塞）：① 存量 resultData 消费路径缺可读键（评估 Java 是否有缓存/导出读存量）；② `_tasks` 进程内回读 best-effort（单副本部署命中率高，CI 滚动重启丢失；后续单可改从 lumen-algo `GET /gdf/tasks/{id}` 回读 params）；③ `enterprise-list items[].tags` 仍透白名单码（前端 COMPARE_BASKET 有兜底，属 027-002 票面范围外）；④ meta 产业链兜底 3 个存量红测试另派修。

## 联调闸门（待走查通过后执行）

1. 监管人走查本 commit → push → CI → K8s dev rollout（search/ai 两服务）。
2. `USE_MOCK=false` 30892 复测上表 4 组 BUG + source_case（FUNC-00385/02120/01414/02195）。
3. 与孔东确认 FE 兜底（`TypeRegionPanel`/`CityBenchmarkPanel`/`recruitDisplay`）保留或删除。
4. 通过后 note 写「联调通过」+ trace_id 回填 bug-registry，本单推进 pending_test。

## 遗留与开放项

- `test_meta_dimension_endpoints` 2 例 + `test_query_tree_dsl` 1 例存量红（见验证节）。
- 028-004 若复现仍显示编号 → D16 gapfill 登记（ES 文档缺 name_cn 灌数）。
- MCP task-claim 不写 `claim_type`、`depends_on` 无写入口：registry 以 note 声明（见任务 QA-TOPIC-BUGFIX-API-L01 note v2）。

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~96000 |
| model_used | glm-5.3-Flash |
| actual_cost | 0.19 |
| cost_warn | green |
