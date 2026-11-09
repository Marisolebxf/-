# SYSINT-04-01-L01 · 专题一张图后台接口

ponytail: full

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 本叶已在 2026-11-06 由孔东认领并处于 in_progress。本次只补路径修正，不改认领。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只改控制器映射一行，对齐网关已有剥前缀。未改对外 URL、未改网关、未加依赖。 |

## 问题清单

- 调试页 `POST /api/topic/v1/portal/one-map/industry-stats` 返回 404，响应 `path` 为 `/v1/portal/one-map/industry-stats`。
- 网关 `GkxlumenRequestGlobalFilter` 剥掉第一段 `topic`。控制器原来写在 `/topic/v1/portal/one-map`，对不上。
- 2026-11-06 流水线 4076 的 `helm:deploy` 在 `deploy:topic` 之后把镜像打回 `:latest`，节点 `IfNotPresent` 仍是旧包。本 handoff 不处理发布。

## 修改内容

- `OneMapPortalController` 的 `@RequestMapping` 改为 `/v1/portal/one-map`。
- 六个 POST 相对路径不变：`industry-stats`、`enterprise-stats`、`policy-stats`、`district-stats`、`key-enterprises/search`、`thematic-map`。
- 对外地址不变：`{gateway}/topic/v1/portal/one-map/*`，别名 `/api/open/topic/v1/portal/one-map/*`。

## 测试结果

- 未跑单测。改动是映射字符串，没有业务分支。
- 线上仍 404，要等 `TOPIC_RELEASE=true` 把本提交的镜像钉上。不要接着跑 `helm:deploy`。

## 遗留风险

- 当前 Pod 不是含本映射的镜像。未点名发布前，调试页继续 404。
- 同模块 `TopicHealthController` / `TopicElementController` / `SynthSnapshotController` 仍映射 `/topic/v1/**`，和网关剥前缀同样不一致。本叶不改。

## CI/CD（必填）

- 分支：`lumen-svc-platform` `dev`
- commit：`80d67b4`（本地 `dev`，未 push）
- pipeline URL / ID：未触发。发布须 `TOPIC_RELEASE=true`
- 部署 namespace / 镜像 tag：未部署
- K8s rollout：未做
- dev 测试 URL：`POST /api/topic/v1/portal/one-map/industry-stats`，发布后预期不再是 `path=/v1/...` 的 404

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkxlumen-topic`
- traceId（dev 抽样）：发布前抽样 `d833623d`（404，旧路径）
- Tempo / Loki：未再查

## 涉及文件

- `repos/lumen-svc-platform/gkxlumen-topic/src/main/java/com/topcomm/gkxlumen/topic/controller/onemap/OneMapPortalController.java`

## 范围与实现

联调通过：六个 one-map 接口已在 `gkxlumen-topic` 完成编排并部署；政策趋势、区政策、政策地图和重点企业搜索的后续适配缺陷已由 `SYSINT-04-01-API-GAP-L01` 修复。未把久新技术/人才/科研指标塞入智树接口。

## 偏离

- 对外契约保持不变；只修正既有实现和发布链路。
- 调试数据由 DATA-EMP 批次构造，不声称是正式业务来源。

## 产物清单

- Java one-map 门面与政策/企业适配修复。
- Python 企业搜索兼容路由。
- `/one-map-debug` 联调页免 SSO 路由修复。
- Helm/Nacos 初始化及部署诊断修复。
- API、UI、边界和发布证据。

## 验收证据

- Java `OneMapFacadeServiceTest`：10/10 通过。
- Python `pytest`：7/7 通过。
- 前端 type-check/build 通过，Pipeline `4227` 全绿。
- Java 正确服务 Pipeline `4219` 的 `deploy:topic` 成功；最终 Helm Pipeline `4233` 的 build/lint/chart 全部成功。
- 线上 12/12 产业、9/9 行政区、三类地图和 API-5 搜索全部通过；`/open/topic` 与 `/topic` 均 HTTP 200。
- UI 截图：`agent-delivery/agent-handoffs/系统集成-SYSINT/SYSINT-04-01-DATA-EMP-L01-evidence/one-map-ui-qa.jpg`。
- 结构化 QA：`agent-delivery/agent-handoffs/系统集成-SYSINT/SYSINT-04-01-DATA-EMP-L01-evidence/qa-regression.json`。

## 架构合规自检

- ✅ 前端只经网关调用，Java 不直连数据库写库。
- ✅ 计算只走 lumen 目标服务，不调用 demo-*。
- ✅ API 查询只读，未在接口请求中灌数。
- ✅ 无 DDL、无新 ES mapping。
- ✅ 对外六个 URL、请求与核心响应字段保持稳定。
- ✅ 缺数保持 null，参数错误使用稳定错误码。
- ✅ 发布、提交、测试、线上回归均有证据。

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | `not_measured` |
| model_used | `codex` |
| actual_cost | `not_measured` |
| cost_warn | `green` |
