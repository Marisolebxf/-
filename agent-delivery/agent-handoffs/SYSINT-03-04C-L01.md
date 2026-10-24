# SYSINT-03-04C-L01 · 政策扶持最新政策与深圳最新政策

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | `LUMEN-POLICY-C-SEARCH-FILTER-L01` 已 done。本叶按派单不调 Python。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只加一个只读时间线。主数据未接通，默认空列表。mock 开关默认关。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 按契约五个字段写，未用压缩代替契约。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SYSINT-SCHEME-03-SEQ` |
| 图 diff | 未改图。本叶浏览器到 Java 即返回，不画到 Python |
| 会签态 | 技术方案 §2.2 frontmatter 为 `draft` |
| 说明 | 派单写明本单不调 Python。 |

## 范围与实现

`GET /topic/v1/policy/timeline?scope=latest|shenzhen`

每条记录只有 `policy_id`、`title`、`publish_time`、`region_name`、`source_url`。`scope` 缺省为 `latest`。深圳范围只留地区为深圳市的记录。未知 `scope` 返回空列表。

`gkxlumen.topic.policy.timeline-mock` 默认 `false`（环境变量 `GKXLUMEN_TOPIC_POLICY_TIMELINE_MOCK`）。关：`items` 为空。开：返回两条示例，深圳范围只留深圳市那条。示例地址用 `example.invalid`，没有运营导语。

## 偏离

正式政策主数据未接通，本接口没有去查库。有主数据之后再把这五个字段从 ADS 读出来，mock 仍要能关。

## 产物清单

- `PolicyFacadeController` `/timeline`
- `PolicyFacadeService` / `PolicyFacadeServiceImpl`
- `PolicyPythonProperties.timelineMock`
- `application.yml`
- `PolicyFacadeServiceImplTest`、`PolicyFacadeControllerTest`

## 验收证据

单测写了空列表和 mock 开时的五字段记录。本机没有 `java` / `mvn`，测试没有跑起来。

## 架构合规自检

| 项 | 结果 |
|---|---|
| 本叶不调 Python，不写算法 | ✅ |
| 不调用 demo-* | ✅ |
| 不写 ADS，不新造导语 | ✅ |
| 可观测沿用服务已有 tracing 配置，未另接一套 | ✅ |

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 未单列计量 |
| model_used | 未单列 |
| actual_cost | 未单列 |
| cost_warn | green |
