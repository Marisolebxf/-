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

## 已发布调试页与 QA 回归

- 前端提交 `03661ffe82470ea06c18de6e73572b049292b8a2`；Pipeline `4227` 全绿（build/image/trivy/deploy）。
- 根因：`requiresAuth=false` 只跳过登录判断，后续 `shouldLoadPortalPerms()` 仍触发 SSO。新增页面级 `skipAuthGuard=true`，仅 `/one-map-debug` 在登录/权限守卫前放行。
- `http://10.50.69.111:30892/one-map-debug` 已可直接打开，不再重定向统一用户中心。
- 页面内逐项点击 API-1～API-6，均 HTTP 200、`code=0`；API-6 抽样 traceId `cfc0e183`。
- 切换到页面“`/api/open/topic`（新别名）”后再发 API-6，HTTP 200；抽样 traceId `c1c0e183`。
- QA 截图与结构化结果：
  - `agent-delivery/agent-handoffs/系统集成-SYSINT/SYSINT-04-01-DATA-EMP-L01-evidence/one-map-ui-qa.jpg`
  - `agent-delivery/agent-handoffs/系统集成-SYSINT/SYSINT-04-01-DATA-EMP-L01-evidence/qa-regression.json`

## QA 边界结果

- `/open/topic` 新别名：HTTP 200、`code=0`。
- 政策 + 南山区：6 条，趋势非空 6 点。
- 搜索分页第 2 页、每页 2 条：total 7、records 2。
- 搜索 + 南山区：total 4，所有记录均在南山区。
- 不存在关键词：total 0、records 0。
- 缺 keyword、缺 district、非法 theme 分别稳定返回 `KEYWORD_REQUIRED`、`INDUSTRY_CODE_AND_DISTRICT_REQUIRED`、`THEME_INVALID`。

## Helm / Nacos 发布修复

- `8e5e8dd`：Nacos 初始化改用 Harbor 可用的 `python-algo-base:3.11`，用 Python 标准库发布配置，移除 Docker Hub `curlimages/curl` 依赖；异步服务 image tag 使用 `--set-string`，避免 Helm 把它解析成科学计数法。
- `96ac772`：部署诊断循环容忍 Pod 在滚动中已被删除的瞬时 NotFound，避免 Helm 已成功却被诊断命令误判失败。
- 已用 Helm 3.14 本地通过 `helm lint`、模板渲染、Shell/Python 语法检查及 fake Nacos 双命名空间发布测试。
- [Pipeline 4233](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/pipelines/4233)：`backend:build` Job `29832`、`helm:lint` Job `29833`、`helm:chart` Job `29844` 全部 success。


## 偏离

- 保留既有接口契约，只修正实现和三仓发布链路；未按早期过度扩张的批次改造/指标定义方案实施。

## 产物清单

- Java/Python/前端修复、Helm/Nacos 发布修复、测试与线上回归证据、QA 截图。

## 架构合规自检

- ✅ D9/D12：前端只经网关，Java/Python 只调 lumen 目标，不接 demo 服务。
- ✅ 只读：一张图接口不写业务库；调试数据另由 DATA-EMP 批次在既有表写入。
- ✅ 无 DDL：未新建/修改表、字段、索引或 ES mapping；已有索引无调试文档新增。
- ✅ 契约稳定：六个对外 URL、HTTP 方法、入参与核心返回字段未变。
- ✅ 容错：缺数保持 null，空搜索返回空列表，参数错误返回稳定错误码。
- ✅ 发布可追溯：Java、Python、前端、Helm/Nacos 均有 commit、pipeline 与线上回归。
- ✅ 边界隔离：免登录仅作用于 `/one-map-debug` 内部联调页，未放宽其他页面。

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | `not_measured` |
| model_used | `codex` |
| actual_cost | `not_measured` |
| cost_warn | `green` |
