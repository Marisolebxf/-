# POL-L2-DS10-TREND-IMPL-JAVA · 科创政策全景 · 政策动向跟踪 · Java 实现

- 任务：`POL-L2-DS10-TREND-IMPL-JAVA`
- 日期：2026-11-04
- 认领：`agent:api-agent`
- 监管：`human:淮政玮`
- 强度：ponytail full
- 上游：`sdd/l2/POL-L2-DS10-TREND-API.md`（签收版）、`POL-L2-DS10-TREND-ARCH.md`（2026-11-03 签收）、`POL-L2-DS10-TREND-DATA.md`
- 仓：`repos/lumen-svc-platform`（gkxlumen-display + gkxlumen-element 两模块）

## 任务认领表

| 项 | 值 |
|---|---|
| task-id | POL-L2-DS10-TREND-IMPL-JAVA |
| 认领 | agent:api-agent（2026-11-04 开工，MCP task-update-status → in_progress） |
| 监管 | human:淮政玮 |

## 范围与实现

四资源（SRS 203–206），全部落在既有 `PolicyPanoramaController`/`PolicyPanoramaService` 与 `PolicyGapfillController`，无新控制器、无新依赖、无新表。

| # | 公开资源 | 实现 |
|---|---|---|
| 203 | `GET /display/v1/policy/panorama/ingest` | display `PolicyPanoramaService.ingest` → Feign `RemoteElementClient.policyIngest` → element `PolicyGapfillController#ingest`（`@Inner`）只读 `{dwd}.policy_base_info`（`is_deleted=0`，最新在前，LIMIT 默认 20 硬顶 100）。列：id/policy_id/source_plane/title/issued_number/publish_organization/publish_date/policy_type/province/status/url/etl_batch_id/created_time。无行空列表，不发起抓取；详情复用既有 `{id}/detail` |
| 204 | `GET /display/v1/policy/panorama/subscriptions` | 已有 `PolicyPanoramaSubscriptionController`（委托 gkxlumen-topic-policy），本单核验无需改动 |
| 205/206 | `GET /display/v1/policy/panorama/stats` 扩展 | 时序（M_POLICY_TIMESERIES）、地域（M_POLICY_NATIONAL_DIST）沿用既有 stats 委托未动；新增 `theme_dist` 维：display `stats()` 内 `RemoteElementClient.policyThemeDist` → element `themeDist()` 只读 `{gapfill}.gapfill_policy_theme_dist`（theme_name/item_count/stat_year + D16 列）。无行空数组，主题失败只让该维空（`recordList` 容错），不清时序/地域/入库 |
| 205 | `POST /display/v1/policy/panorama/jobs` 三域 | body 带 `kind` ∈ {热点识别, 政策影响评估, 深度分析报告} 时同步分流（对齐 PolicyEvaluationService kind 先例）：display 按类读 element `/trend/hotspot`、`/trend/impact`、`/trend/report`（各只读对应缺项表，行按 `domain_name` 过滤，不传读全部，原样返回）。kind 与 sub_type 同传→空；kind 闭集外→空；不带 kind 走原有 sub_type（policy_effect/match/intensity）异步流程不变。不进 Python、不进 topic-async-service |

**参数名约定**（TREND-API §5 允许自定并在此写明）：

- 种类键：`kind`，取值即中文叶子名 `热点识别` / `政策影响评估` / `深度分析报告`（与评价链 jobs 的 `kind` 同风格）。
- 领域键：`domain`（兼容 `domain_name`、`领域`），值如「科创发展/人才引进/资金扶持」，透传 element 作 `domain_name` 过滤；不传读全部行。
- ingest 条数：`limit`（可选，默认 20，1–100 夹取）。

## 偏离说明

1. **ingest 读 DWD `policy_base_info` 而非 ADS 表**：TREND-API §2 写「读第 6 项已经落入 ADS 的入库列表」，但 GDF 派单包 v2 与 `ads.md` 均未点名「来源监控入库」ADS 表（TREND-DATA §2 明文「本单不编造 ADS 表名」）。政策唯一入库主表是 DWD `policy_base_info`（GDF-WORKPACK-V2 落库终点，demo 20,000 行）。选择：element 经 `{dwd}` 占位只读该表（配置 `ELEMENT_DWD_DB` 已存在，正是第 6 项入库结果），符合「读第 6 项已落库的入库列表」语义，未编造表名、未加字段。如后续 ADS 出专用入库表，只改 element 一处 SQL。
2. **kind 闭集外返回空而非回落 sub_type**：对齐评价链 `PolicyEvaluationService#syncKind` 先例语义（带 kind 即同步分支），避免同一请求双语义。
3. jobs 三域的 205 热点/影响/深度报告按契约不建任务、不返任务号，直接返回行（`records`）。

## 产物清单

- `gkxlumen-element/.../controller/PolicyGapfillController.java`：+5 端点（ingest/trend-hotspot/trend-impact/trend-report/theme-dist）+ trendRows 辅助
- `gkxlumen-display/.../feign/RemoteElementClient.java`：+5 `@NoToken` Feign 方法
- `gkxlumen-display/.../service/PolicyPanoramaService.java`：stats 加 theme_dist 维、ingest()、jobs kind 分流 + TREND_JOB_KINDS
- `gkxlumen-display/.../controller/PolicyPanoramaController.java`：+`GET /ingest`
- `gkxlumen-display/.../test/.../PolicyPanoramaServiceTest.java`：+4 测试（kind 三域读表不建任务、kind+sub_type 互斥空、stats 主题维挂接+失败隔离、ingest 透传+失败空列表）

## 验收证据

- **本地编译跳过（用户指令 2026-11-04：本机 Maven 3.6.0 环境限制，禁止本地 mvn/pnpm 编译验证），验证走 GitLab 流水线**
  - 首推 `530bd05`（merge `760885b`）→ 流水线 [3678](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/pipelines/3678) `backend:build` **failed**：单测 `statsAttachesThemeDistAndKeepsBlocksOnFailure` 断言失败——`recordMap` 误接 R 包装体（多解一层 `payload`）致 `theme_dist.records` 恒空。
  - 修复 `4fc4c35`（theme_dist 改 `recordList` 先解包再取数组直出）→ 流水线 [3680](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/pipelines/3680) **passed**：`backend:build` success（单测 48/48 过）→ 全部 `backend:image:*` success → `deploy:display` / `deploy:element` 等 deploy success，K8s dev 已发布；流水线终态 `manual` 仅剩 diag/diag:nacos 类手动诊断 job，为仓常态
- 单测：`PolicyPanoramaServiceTest` 48 用例（含本单 +4：kind 三域读表不建任务、kind+sub_type 互斥空、stats 主题维挂接+失败隔离、ingest 透传+失败空列表）随 CI `backend:build` 执行

curl 语义验证清单（dev 环境部署后）：

1. `GET /display/v1/policy/panorama/ingest` → 200，records 为 policy_base_info 最新行（camelCase）；`?limit=5` 生效
2. `GET /display/v1/policy/panorama/stats` → body 含 `theme_dist.records`（5 行：themeName/itemCount/statYear）；断掉 gapfill 库时其余块不空
3. `POST /display/v1/policy/panorama/jobs` `{"kind":"热点识别"}` → records 6 行（domainName/hotspotName/brief + D16 列）；`{"kind":"深度分析报告","domain":"科创发展"}` → 该域 1 行（title/body）
4. `GET /display/v1/policy/panorama/subscriptions` → 未登录/无订阅时空列表

## 架构合规自检

| 条 | 结论 |
|---|---|
| 调用链：前端→Java REST→（element Feign / topic-policy 委托），不越层不直连 Python/库 | ✅ display 只 Feign；element 只 JdbcTemplate 只读 |
| 对外路径不出现 /topic/v1/policy、/v1/policy、/topicAsync/** | ✅ 测试断言 Controller 映射 /v1/policy/panorama（网关 StripPrefix 后）；新增对外仅 /ingest |
| 空态=空列表/空数组，无 501 充当、无写死 mock、无行不造 0 | ✅ 全部 listOrEmpty/recordsBody 空列表；单测断言 |
| 读失败只让对应块空，不清其它块 | ✅ stats theme 失败单测；jobs 各域独立 |
| 不新造 metric_id、不改 D4、不改三分册 | ✅ 只透传行上 D16 列 |
| trace 沿既有展示链带 traceId，不新设计观测点 | ✅ 复用 Feign/网关既有 trace 透传，零新观测代码 |
| D12 lumen 不调 demo-* | ✅ element 数据源按既有 {dwd}/{gapfill} 配置占位，未改配置 |
| @NoToken + @Inner 配对（element 下游） | ✅ 五个新 Feign 方法全 @NoToken，element 端点全 @Inner |
| @Inner 读面不建表不插入不写死 | ✅ 全 SELECT，listOrEmpty 容错 |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | ~0.9M（含前段会话实现 + 本段提交/CI 轮询） |
| model_used | glm-5.3 |
| actual_cost | ~$4 |
| cost_warn | false（< $10） |

## CI-CD

- lumen-svc-platform push `origin/dev`（`530bd05` → merge `760885b` → fix `4fc4c35`）→ GitLab CI → K8s dev（仓规标准链，非 cicd:skip）
- 首推流水线 3678 红（单测断言），修复后流水线 [3680](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/pipelines/3680) **passed**（backend:build + 全部 image + deploy:display/deploy:element 全绿，K8s dev 已发布）

## 涉及文件

- repos/lumen-svc-platform：上述 5 个 Java 文件
- gkx-orchestration：本 handoff、task-registry 状态（MCP）
