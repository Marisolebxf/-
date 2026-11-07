# SYSINT-04-01-API-GAP-L01 · 专题一张图灌数读取与搜索适配修复

ponytail: full

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:徐滕强` |
| supervised_by | `human:徐滕强` |
| claim_type | `coordinator_dispatch` |
| 说明 | 用户在本会话明确要求继续推进调试页数据与代码，不改表结构。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只修已经由线上响应证明的三个适配缺陷：政策字段名、政策查询 kind/区筛选、缺失的企业搜索兼容路由。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SYSINT-04-01-L01` |
| 图 diff | 未新增服务边；沿用 `gkxlumen-topic -> entan-py/search-py`。 |
| 会签态 | 源方案 `draft`，本单只修既有调用实现，不改契约。 |
| 说明 | 对外六个 URL、请求字段和返回字段未变。 |

## 问题清单

- API-3 的政策趋势读取了不存在的 `policy_count`，Python 实际返回 `publish_count`。
- API-4/API-6 用 `kind=sz` 却按 `data.sz` 解析；Python 在该 kind 下返回 `data.items`，导致区政策数和政策地图为空。
- API-5 Java 调用 `/internal/gkx-search/search/query`，但检索服务没有该路由，接口稳定返回 0。
- `/topic/**` 路由到 `gkxlumen-topic`，早先部署成功的 `gkxlumen-topic-svc` 不是承载一张图门面的正确服务。
- 调试政策关联曾使用裸 `INB*`，现有查询要求 `chain:INB*`；外部数据刷新还曾覆盖本批调试行。

## 修改内容

- Java `OneMapFacadeService`：政策趋势改读 `publish_count`；API-4/API-6 改用 `kind=all` 的 `data.sz` 后按行政区名筛选。
- Python `enterprise_search`：新增 `/internal/gkx-search/search/query` 兼容路由，复用通用企业检索，把 `keyword/district/industry_chain_code/page/page_size` 转成现有 query_tree，并返回一张图所需的 `records` 契约。
- 调试数据重灌到原表：共 1302 行仍完整；540 条政策关联修正为 `chain:INB*`；72 个产业名和 9 个区名恢复标准显示值，避免 Java 精确匹配失效。
- 未创建或修改表、字段、索引、mapping；未写 ES 调试文档，因为 `gkx_enterprise_v1` 已有关键词命中数据。

## 测试结果

- Java：临时 Maven 3.9.9 执行 `OneMapFacadeServiceTest`，`10` 项通过，`0` 失败、`0` 错误。
- Python：`pytest -q tests/test_one_map_search_query.py tests/test_one_map_gap_fill.py`，`7` 项通过。
- 数据：当前批次行数为 `141 + 72 + 9 + 540 + 540 = 1302`，全部来自既有表。
- ES 只读核查：`gkx_enterprise_v1` 有 19 家“腾讯”，`INB1309` 命中 7 家。
- 全量线上回归：
  - 12/12 产业的 API-1/2/3 有数，规模趋势均为 5 点，政策趋势均有非空值。
  - 9/9 行政区的 API-4 发展指数、企业数、政策数均有值。
  - API-6 `development=9/9`、`enterprise=9/9`、`policy=10/10`（九区+市本级）非空。
  - API-5 `腾讯 + INB1309` 返回 7 条，首条为“腾讯科技（深圳）有限公司”，区为南山区。
- 回归摘要：`/private/tmp/one-map-final-regression.json`（执行机本地证据，不提交明细）。
- 未保留有效 traceId，不虚构链路证据。

## 遗留风险

- 调试行位于现有业务表，后续上游刷新可能再次覆盖；当前已重新校验 1302 行存在。完整行计划和备份只留执行机，不提交 Git。
- 本次没有新增正式数据口径，也没有改 ES mapping。页面验收仍由 QA/授权人完成。
- Java 完整流水线还包含其他服务部署，但其未影响本次已成功的 `deploy:topic`；本单结论只依赖对应 Job 和线上回归。

## CI/CD（必填）

- Java 分支：`lumen-svc-platform/dev`
- Java 修复提交：`7a37b7386c778a33fce659d764b37b16663fbe5e`（已包含在部署 SHA `1921744916713b960784379a3d45c1f7f6ae4202`）
- Java 错误部署对照：Pipeline `4197` 的 `deploy:topic-svc` 成功，但该服务不承载 `/topic/**`。
- Java 正确部署：[Pipeline 4219](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/pipelines/4219)，`deploy:topic` Job `29687` success，rolling image digest `sha256:97a51d95c30de868a1f82c44061fc779e3fb7ad1e4d358bc128439d58fdaf018`。
- Python 分支：`lumen-topic-py/dev`
- Python 提交：`67c7bd0de2e8eb11366946ec0f6ae67627212ad3`（兼容路由）、`6ae85c8b598021e4d8be6cc042bc350ff367e866`（过滤操作符修正）
- Python 最终部署：[Pipeline 4223](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-topic-py/-/pipelines/4223)，`py:smoke` Job `29742`、重试镜像 Job `29769`、`deploy:search-py` Job `29747` 均 success。
- K8s namespace：`zhipu-tts`；`gkxlumen-platform-topic`、`gkxlumen-platform-search-py` 已滚更。
- dev 回归：`http://10.50.69.111:30895/topic/v1/portal/one-map/**`，六类内容全部为 HTTP 200、`code=0`。

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkxlumen-topic` / `gkx-search-service`
- traceId（dev 抽样）：未保留
- Tempo / Loki：本次未取证

## 涉及文件

- `repos/lumen-svc-platform/gkxlumen-topic/src/main/java/com/topcomm/gkxlumen/topic/service/onemap/OneMapFacadeService.java`
- `repos/lumen-svc-platform/gkxlumen-topic/src/test/java/com/topcomm/gkxlumen/topic/service/onemap/OneMapFacadeServiceTest.java`
- `repos/lumen-topic-py/gkx_search_service/views/enterprise_search.py`
- `repos/lumen-topic-py/tests/test_one_map_search_query.py`
- `agent-delivery/agent-handoffs/系统集成-SYSINT/SYSINT-04-01-DATA-EMP-L01.md`
- `agent-delivery/agent-handoffs/系统集成-SYSINT/SYSINT-04-01-DATA-EMP-L01-evidence/debug-batch-summary.json`
