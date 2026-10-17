# ENT-RISK-INGEST-BTN-L01 · 风险域（risk_*）灌数按钮

- **执行**：agent:algorithm-agent（监管/签收：human:徐滕强）
- **仓**：demo-algo-ent-analysis（后端）+ demo-ui-system-test（前端按钮）
- ** ponytail:** full（复用 gdf_sim 既有模式，最短差异；映射函数均为纯转换）

## 范围与实现

企业灌数（gdf_sim）之外，为风险域新增独立小样灌数入口，与 `run-pipeline`/`rewrite-es` 互斥共用 `_state` 异步模式：

- `entan/llm_ods/risk_ingest.py`（新增）：9 张 ODS 源表 → 8 张 DWD 目标表映射；每表 `RISK_INGEST_LIMIT`（默认 10000）LIMIT 取样 → `dedup_by` 按各表 DDL 唯一键去重 → 删旧插新（幂等可重跑）
- `api/main.py`：`POST /internal/ingest-risk`（启动）+ status 的 `dwd` 段新增 6 张 risk 表行数采样
- demo-ui-system-test `BasicPage.vue`：重写 ES 旁「风险灌数」按钮（确认弹窗 + waitJob 轮询），`api/entan/index.ts` 加 `ingestRisk()`

## 源 → 目标映射与落库对账（2026-10-15 17:57 实测）

| ODS 源表（总量） | DWD 目标（uk） | 小样落库 |
|---|---|---|
| dwd_org_opt_judicial_case（339 万） | risk_judicial_case（org_id+case_id） | 9,997 |
| dwd_org_risk_shixin（7.6 万） | risk_dishonest（dishonest_id） | 8,517 |
| dwd_org_risk_zhixing（55 万） | risk_executed（org+case_no+person） | 10,000 |
| dwd_org_company_abnormal（5,862） | risk_abnormal（case_id） | 5,862（全量=源上限） |
| dwd_org_company_punish（6.6 万） | risk_punishment（case_id+org_id） | 10,000 |
| dwd_org_risk_tax_punish（528） | risk_tax_punish（case_id） | 528（全量=源上限） |
| dwd_org_bankruptcy_public_cases（3.6 万） | risk_bankruptcy（case_id） | 10,000 |
| dwd_org_company_illegal（247） | risk_illegal（case_id=sv_id） | 247（全量=源上限） |

无源表（ODS 无对应贴源，跳过并在日志说明）：limit_high / equity_freeze / equity_pledge / zhongben / chattel_mortgage；party 侧 5 张（无独立当事人源）。

## 开发中修复（连库实测驱动）

| 提交 | 问题 → 修复 |
|---|---|
| `05be799` | 初版：接口 + 8 表映射 + status 采样 |
| `fdb32d8` | 1364 Field 'case_id' doesn't have default：abnormal/punishment/tax/bankruptcy DDL 业务键是 case_id，映射补齐并按 uk 去重 |
| `25715f5` | 1366 Incorrect decimal ''：源 fine_amount 是 varchar（3.4 万空串+3.1 万文本）。根修在 `db.insert` 按 SHOW COLUMNS 识别 DECIMAL 列统一 `''`/文本→NULL（全模块受益），punishment 金额 `_num` 化 |
| `fee1285` | risk_bankruptcy 0 落库：它是案件详情表（无 org 列），admin_org_id 当 org_id 被 `_insert_filtered` 过滤；改案件映射 + 守卫放行 case_id/dishonest_id 主键表 |
| `b14b82f` | risk_illegal 0 落库：源键是 `sv_id` 非 illegal_id；列结构对齐 risk_abnormal |

## 验证证据

- 触发方式：k8s exec → `POST /internal/ingest-risk`（公网经 50100 转发偶发超时，集群内稳定）
- Pod 日志 8 表逐条 `[risk] X 源行 → N 落库`，无 Traceback；status `running=false, last_error=none`
- 连库 COUNT 与日志一致；重复执行幂等（删旧插新）， judicial 339 万全量放开待小样观察后另议

## 架构合规自检

- ✅ 调用链：前端 → Java 网关 → Python `/internal/*`（无越层）；只写 demo_gkxlumenx_dwd（`assert_demo_mysql_targets` 闸门保留）
- ✅ 无新依赖；复用 gdf_sim 的 `_fetch_all/_insert_filtered/dedup_by/_delete_by_org` 与 `_state` 异步模式
- ✅ 可观测：status 采样 + 结构化日志；失败写 `last_error` 不伪装成功
- ✅ demo/lumen 隔离：仅 demo 仓、仅 demo_* 库
- ✅ commit 全部 `[agent:algorithm-agent]`，push origin/dev（demo-algo 05be799→fdb32d8→25715f5→fee1285→b14b82f；demo-ui cf8f165）

## cost

- actual_tokens: ~85k（含连库对账与 5 轮线上验证）
- model_used: glm-5.3-Flash
- actual_cost: ~$3.5
- cost_warn: no
