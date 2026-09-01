# ALGO-LIB-ODS-MOCK-ENT-L01 · 企业分析算法库 — 企业 Mock ODS 主表 CRUD+搜索+翻译

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 用户授权连跑并行；本叶不重复认领。registry 监管人按会话为淮政玮（派单包默认徐滕强未改现场授权）。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最短 diff：新路由 + 一页 Element Plus；复用 `connect`/`is_live`/`assert_demo_mysql_targets`/`request`/`dataPlane`。未用 YAGNI 跳过 live 写守卫、服务端搜索、X-Trace-Id、handoff。未做 LLM 填表（SPEC 未要）。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未走 Headroom；实现面小、对照 SPEC 与政策 Mock 页即可。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A（本叶不改存储流图拓扑） |
| 图 diff | 写库方仍 = Demo ODS `demo_gkxlumenx_ods.dwd_org_base_info`；禁止写 DWD/ADS/正式 `gkxlumenx_*`。 |
| 会签态 | 抄 ENT `01-data-flow.md` 已 `approved`。 |

## 范围与实现

对照 SPEC `ALGO-LIB-ODS-MOCK-SPEC-L01.md` §企业：

1. 新页 `/entan/mock`，侧栏底部「企业 Mock」。
2. 主表 `demo_gkxlumenx_ods.dwd_org_base_info`，主键 `org_id`；信用代码列 `external_id`（无 `credit_code`）。
3. 列表列：org_id / name_cn / city / area / industry / org_type / reg_status / org_size；列头中文。
4. 搜索服务端 AND：`q_name_cn` `q_org_id` `q_external_id` `q_city` `q_industry`（参数化 LIKE）。
5. 码值：`org_size` 微型/小型/中型/大型/未知；`reg_status`/`org_type` 原文。
6. CRUD 只写 Demo ODS；`is_live("ent")` 禁止写；不入 DWD/ADS；无 fixture。
7. API 挂本仓 FastAPI `/v1/entan/mock`；前端 `/entan/v1/entan/mock/...`。
8. UI 对齐 `PolicyMockPage.vue`（Element Plus），无 Arco。

## 偏离说明

- 列表加了 `limit`/`offset` 分页：现网表约 5 万行，不用分页会一次拉爆；搜索仍在 SQL。
- 未做政策页那种 LLM 填表 / 待追加差集：SPEC 企业叶未要求。
- 并行 CHAIN 叶同仓作业；本 commit **不**带 `chain_mock*` / `PolicyMock*` / `svc_*`。

## 产物清单

| 产物 | 路径 |
|------|------|
| Python CRUD | `demo-algo-ent-analysis/entan/mock/org_ods.py` |
| FastAPI | `demo-algo-ent-analysis/api/entan_mock_routes.py` 前缀 `/v1/entan/mock` |
| include | `api/main.py` 文末 `# ALGO-LIB-ODS-MOCK-ENT-L01` try/include |
| 单测 | `tests/test_entan_mock_org.py`（6 passed） |
| 前端 API | `demo-ui-system-test/src/api/entan/index.ts` |
| 页 | `src/views/entan/pages/EntanMockPage.vue` |
| 菜单 | `entanMenuConfig.ts` 底部「企业 Mock」 |
| 路由 | `src/router/index.ts` entan children `path: 'mock'` |
| 本 handoff | `agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/ALGO-LIB-ODS-MOCK-ENT-L01.md` |

## API 路径

| 方法 | Python | 前端（经 `/entan` 网关） |
|------|--------|--------------------------|
| GET | `/v1/entan/mock/orgs` | `/entan/v1/entan/mock/orgs` |
| GET | `/v1/entan/mock/orgs/{org_id}` | `/entan/v1/entan/mock/orgs/{org_id}` |
| POST | `/v1/entan/mock/orgs` | `/entan/v1/entan/mock/orgs` |
| PUT | `/v1/entan/mock/orgs/{org_id}` | `/entan/v1/entan/mock/orgs/{org_id}` |
| DELETE | `/v1/entan/mock/orgs/{org_id}` | `/entan/v1/entan/mock/orgs/{org_id}` |

查询参数：`limit` `offset` `q_name_cn` `q_org_id` `q_external_id` `q_city` `q_industry`。包络 `{code,msg,data}`；`data.list=[]` + HTTP 200 诚实空态。

## 测试结果

- `python -m pytest tests/test_entan_mock_org.py -q` → **6 passed**（WHERE AND、五字段、空搜、禁 `credit_code`、org_size 字典、live 拒写）。
- 未在 50100 / K8s 点验（并行叶同仓，镜像未滚）。**本地验证、K8s 待滚**。

## 遗留风险

- 与产业服务 Mock 共用 `dwd_org_base_info`：两页可改同一 `org_id` 的圈定列（SPEC 已提示）。
- 删除不限 `MOCKENT*`：Demo ODS 全表可删，确认框已提示。
- 表缺失时列表诚实空态；现网 5 万行，默认 50/页。

## CI/CD（必填）

- 分支：`dev`（两业务仓 + 编排仓）
- commit：见收尾 git（`[agent:algorithm-agent]`）
- pipeline URL / ID：push 后由 GitLab 触发，本会话未等绿
- 部署 namespace / 镜像 tag：K8s 待滚
- K8s rollout：待滚
- dev 测试 URL：50100 `/entan/mock`（滚完后点验）

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用 `ent-analysis-demo` / 现网 entan
- 新路由走已有 `TraceHeaderMiddleware`；前端 `request.ts` 已带 `X-Trace-Id`
- Tempo / Loki：未抽样

## 涉及文件

- `demo-algo-ent-analysis/entan/mock/__init__.py`
- `demo-algo-ent-analysis/entan/mock/org_ods.py`
- `demo-algo-ent-analysis/api/entan_mock_routes.py`
- `demo-algo-ent-analysis/api/main.py`（仅文末 include）
- `demo-algo-ent-analysis/tests/test_entan_mock_org.py`
- `demo-ui-system-test/src/api/entan/index.ts`（仅追加 mock 方法）
- `demo-ui-system-test/src/views/entan/entanMenuConfig.ts`（底部一条）
- `demo-ui-system-test/src/router/index.ts`（entan children 末一条）
- `demo-ui-system-test/src/views/entan/pages/EntanMockPage.vue`

## 架构合规自检

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法只在 Python | ✅ CRUD 在 Python；Java 不写 ODS |
| 2 | 调用链 前端→网关→Python | ✅ 50100 → `/entan/**` → `/v1/entan/mock` |
| 3 | 图谱 NebulaGraph | ✅ 本叶不写图 |
| 4 | 可观测性 | ✅ 沿用 Trace 中间件 + `observability.ts` |
| 5 | CI/CD | ✅ push `origin/dev`；未 force |
| 6 | demo 不污染 lumen | ✅ 只改 demo 仓 |
| 7 | 方案 A | ✅ Java 不直连 ODS |
| 8 | 数据走 ADS | ✅ Mock 只写 Demo ODS；不写 DWD/ADS |
| 9 | D8 | ✅ 50100 Element Plus，对齐政策 Mock；非 Arco |
| 10 | D9/D10 | ✅ 联调台工作台，无指标卡 |
| 12 | D12 lumen 不调 demo | ✅ 未改 lumen-ui-* |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 88000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.55 |
| cost_warn | green |

## 明确未做

- 未开工 POLICY / CHAIN / SVC / COMP / INNOV
- 未改 `policy_routes.py` / `polan/mockgen/incr.py` / `PolicyMockPage.vue` / `src/api/policy/**`
- 未改 `svc_routes.py` / `svc_mock_routes.py` / `chain_mock_routes.py`
- 未把 SPEC / xlsx 快照写入本 commit
- 未在 50100 现网点验（K8s 待滚）
