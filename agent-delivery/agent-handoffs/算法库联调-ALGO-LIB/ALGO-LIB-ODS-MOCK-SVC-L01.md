# ALGO-LIB-ODS-MOCK-SVC-L01 · 产业服务 Mock ODS 圈定列 CRUD+搜索

> 对照 SPEC `ALGO-LIB-ODS-MOCK-SPEC-L01.md` §产业服务。新页 `/industry-service/mock`，与企业共用 `dwd_org_base_info`。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 用户授权连跑并行；本会话 algorithm-agent 独自完成，不问人。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 新文件 `svc_mock_routes.py`，不改 `svc_routes.py` / 政策 / ENT / CHAIN Mock。可写列仅圈定列+技术列。未用 YAGNI 跳过 live 写禁、X-Trace-Id、空表诚实空态、服务端搜索。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | SPEC 已锁表与列，无需压缩检索。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A（本叶不改存储流图拓扑） |
| 图 diff | 写库方仍 = Demo ODS `demo_gkxlumenx_ods.dwd_org_base_info`；禁止写 DWD/ADS/正式库。 |
| 会签态 | 抄源：SVC `01-data-flow.md` 已 `approved`。 |

## 范围与实现

对照 SPEC 已锁产业服务行：

1. 表：与企业共用 `demo_gkxlumenx_ods.dwd_org_base_info`，主键 `org_id`。
2. **新页** `/industry-service/mock`「产业服务 Mock」；菜单在 `industryServiceMenuConfig.ts` 底部。
3. 列表只圈定列：`org_id` / `name_cn` / `city` / `area` / `industry` / `industry_l1_name`（列头中文）。
4. 搜索走服务端 AND（查询参数可空）：`q_name_cn` / `q_org_id` / `q_city` / `q_industry` / `q_industry_l1_name`。
5. 可选 `circled_only=true`：SQL 粗滤 + `svc_rule_demo_kw_v1.1` `should_circle`；命中少就少行，无 fixture。
6. 编辑只写圈定列 + `table_data_source`/`operator_remarks`；拒绝 `org_type`/资本/法人/经纬度等工商全档。
7. 删除仅允许本页新增行（`SVC-MOCK-*` 或 `table_data_source=demo-svc-mock`），存量主档禁止删。
8. live / 非 `demo_` ODS：禁止写。空表 HTTP 200 + `list=[]`。
9. 码值：无服务类型 ODS 码；页面无「科技金融/知识产权」下拉。

未做：平行 `svc_org_base`；遗留 `dwd_service_org` 主表；改 `svc_routes.py` 灌数/十模型；不删 ODS 机构主档。

## 偏离说明（2026-09-01 淮政玮现场）

原 SPEC 锁 `dwd_org_base_info` 圈定列。用户要求列表改为 **加工后的服务机构表**，并按 **服务类型** 查询。

as-built：读 Demo ADS `svc_org_card`（现网 3525 行），写时同步 Demo DWD `svc_org_circle`；`q_service_type` 中英互认（FINANCE↔金融服务）。不读 5 万行机构主档，不用遗留 `dwd_service_org`（50 行）。live 仍禁写。

## 产物清单

| 产物 | 路径 |
|------|------|
| Python Mock CRUD | `demo-algo-ent-analysis/api/svc_mock_routes.py`（`/v1/svc/mock/orgs`） |
| include | `demo-algo-ent-analysis/api/main.py` |
| 单测 | `demo-algo-ent-analysis/tests/test_svc_mock.py` |
| 前端 API | `demo-ui-system-test/src/api/industry-service/index.ts`（`/entan/v1/svc/mock/...`） |
| 新页 | `demo-ui-system-test/src/views/industry-service/pages/SvcMockPage.vue` |
| 菜单 | `demo-ui-system-test/src/views/industry-service/industryServiceMenuConfig.ts` |
| 路由 | `demo-ui-system-test/src/router/index.ts`（industry-service `mock`） |
| 本 handoff | `agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/ALGO-LIB-ODS-MOCK-SVC-L01.md` |

## 测试结果

- 本地 `python -m pytest tests/test_svc_mock.py -q`：**7 passed**。覆盖圈定列、搜索 `%s`、拒绝工商全档、`should_circle`、仅 Mock 行可删。
- **50100 未点验**：本机未开联调台。K8s 现网进程在 push/rollout 前不会吃新路由。本地契约验证通过，待滚后再点 50100「产业服务 Mock」。

## 遗留风险

- 与企业 Mock 共用同一 ODS：两页可同时改同一 `org_id` 的圈定列（城市/行业）；本页不能改资本/法人/经纬度。
- `circled_only` 扫描封顶 2000 行后再 `should_circle`；全表圈定命中若超过窗口则 `scan_capped=true`，不补 fixture。
- 并行 ENT/CHAIN 同改 `main.py` / `router/index.ts`：本叶只追加 SVC include 与 industry-service `mock`。

## CI/CD（必填）

- 分支：`dev`（两业务仓 + 编排仓 handoff）
- commit：见 push 后 hash
- pipeline URL / ID：push 后由 GitLab 触发；本叶未等绿
- 部署 namespace / 镜像 tag：`dev` / `demo-platform-entan-py` + `demo-ui-system-test`
- K8s rollout：待 CI
- dev 测试 URL：50100 产业服务 → 产业服务 Mock（rollout 后）

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用 entan-py
- 新路由经现有 `TraceHeaderMiddleware` / 前端 `X-Trace-Id`
- Tempo / Loki：有（未抽样）

## 涉及文件

- `demo-algo-ent-analysis/api/svc_mock_routes.py`
- `demo-algo-ent-analysis/api/main.py`
- `demo-algo-ent-analysis/tests/test_svc_mock.py`
- `demo-ui-system-test/src/api/industry-service/index.ts`
- `demo-ui-system-test/src/views/industry-service/pages/SvcMockPage.vue`
- `demo-ui-system-test/src/views/industry-service/industryServiceMenuConfig.ts`
- `demo-ui-system-test/src/router/index.ts`

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ CRUD 在 Python；Java 不写 ODS |
| 2 | 调用链 前端→Java→Python | ✅ 50100 → gateway `/entan/v1/svc/mock` → `/v1/svc/mock` |
| 3 | 图谱 NebulaGraph | ✅ N/A |
| 4 | 可观测性 | ✅ 沿用 Trace 中间件 / request.ts |
| 5 | CI/CD | ✅ 将 push `origin/dev` |
| 6 | demo 不污染 lumen | ✅ 只改 demo 仓 |
| 7 | 方案 A | ✅ Java 不直连 ODS |
| 8 | 数据走 ADS | ✅ Mock 只写 Demo ODS；不写 DWD/ADS |
| 9 | D8 | ✅ 50100 Element Plus，对齐政策 Mock |
| 10 | D9/D10 | ✅ 联调台 Mock 工作台，非指标卡页 |
| 12 | D12 lumen 不调 demo | ✅ 未改 lumen-ui-* |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 98000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.15 |
| cost_warn | green |

## 明确未做

- 未改 `svc_routes.py` / `policy_*` / `entan_mock_routes.py` / `chain_mock_routes.py` / `IndanaCrudPage`
- 未写 DWD `svc_org_circle`
- 未在 50100 浏览器点验（诚实：等 CI rollout）
