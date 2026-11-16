# POL-L2-PC3-PC4-API-L01 · 展示对比记录只读

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 开工时已是 in_progress。本叶不重新认领，不改 task-registry。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 加在已有 display 政策对比控制器上。POST 复用已有 entan Feign。GET 只读已有 ADS 表。不新开服务，不改 Nacos，不拼句子，不回退种子。 |

## 修改内容

浏览器只打这三个路径（网关 `Path=/display/**` 已转到 `gkxlumen-display`，StripPrefix 后为本服务 `/v1/policy/compare/runs`）：

| 方法 | 路径 | 行为 |
|------|------|------|
| POST | `/display/v1/policy/compare/runs` | 请求原样委托 Python `POST /internal/policy/compare-report`，返回那一行。Java 不写表、不拼句子、不返回写死 mock。算法服务连不上则失败，不造行。 |
| GET | `/display/v1/policy/compare/runs` | 只读 `gkxlumenx_ads.ads_policy_compare_report`，给分析对比记录。没有行则 `records` 为空。 |
| GET | `/display/v1/policy/compare/runs/{runId}` | 只读这一行，给对比结果和研报。没有这一行则空对象。 |

连不上库时 GET 返回失败，不编一个成功的空结果。旧的 `POST /display/v1/policy/compare/jobs` 未改。未改 Nacos，未设 `FORCE_NACOS_REPUBLISH`。未改前端，未改 Python 写入。

## 测试结果

本地编译已按监管人 `human:淮政玮` 指示跳过。编译交给 push 后的 CI。

未连库，因此没有对活行 `run_id=5ad8bcba9fae419e835ae2f3fed6a662` 打真实 HTTP。

## 遗留风险

- 展示服务读库口令沿用已有 `DISPLAY_ADS_PASSWORD` / `ELEMENT_MYSQL_PASSWORD`。缺口令时列表和单行是失败，不是空成功。
- 列表最多 100 行，按 `created_at` 倒序。
- Python 调用沿用政策算法 Feign 读超时 190 秒。

## CI/CD（必填）

- 分支：`origin/dev`
- lumen-svc-platform commit：`4707fd257e2e776892d820ea3bbd1a9edb508b00`
- pipeline：push 后由 CI 编译，本叶未在本地跑 Maven
- 未改 Nacos，未改 task-registry

## 涉及文件

- `repos/lumen-svc-platform/gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/controller/PolicyCompareController.java`
- `repos/lumen-svc-platform/gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/service/PolicyCompareService.java`
- `repos/lumen-svc-platform/gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/feign/RemotePolicySyncClient.java`
- `repos/lumen-svc-platform/gkxlumen-display/src/test/java/com/topcomm/gkxlumen/display/service/PolicyCompareServiceTest.java`
