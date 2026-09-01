# ENTAN-NO-CREATEDB-L01 · entan 启动不再 CREATE DATABASE，库由外部预建

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 用户口径：CREATE DATABASE 不进应用代码，库由外部保证；并授权缩容 CrashLoop + 提交推送 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 启动路径只跳过/删除 CREATE DATABASE；建库入口仍是已有 `create_demo_dbs.sql`。未改 health 时序、未重写 schema 库名映射 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶为 schema 启动路径 + K8s 缩容，未挂载 Headroom |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 不改调用链；建库从应用启动挪到 DBA 脚本 |
| 会签态 | N/A |

## 问题清单

- GitLab job 24831 / 24830：`deploy:entan-py-api` / `deploy:entan-py-worker` ProgressDeadlineExceeded。根因是 demo Pod CrashLoop 同步执行 `schema_mysql.sql` 头部 `CREATE DATABASE gkxlumenx_dwd`，MySQL MDL 排队。
- 应急已做：`demo-platform-entan-py` replicas=0；新 worker RS `86c5b6f94` 缩到 0；worker 钉回 `fb145d45`（旧 Pod Running）。未 KILL MySQL 会话。
- 推送后 CI 会给 API 换镜像，但 Deployment 仍是 0 副本，需显式 `scale --replicas=1` 才会拉起修复后的 API。
- `schema_mysql.sql` 表名仍硬编码 `gkxlumenx_*`；本叶只去掉建库，不改库名映射。

## 修改内容

- `init_schema` / `svcseed.ensure_schema` 跳过 `CREATE DATABASE`。
- `llm_ods.connect_ods` 只 `select_db`；离线 SQL 不再生成建库语句。
- 应用 DDL（`schema_mysql.sql`、`svc_ddl_demo_empty.sql`、编排仓 `ddl-demo-empty.sql`）去掉 `CREATE DATABASE`。
- 建库唯一入口：`scripts/mysql/create_demo_dbs.sql`（DBA / root）。
- lumen-algo-py `vendor/entan-py` 同步，避免正式 entan 再发 `CREATE DATABASE gkxlumenx_dwd`。
- `tests/test_no_create_database.py`；`py:smoke` 纳入该文件。

## 测试结果

- 本地 `python -m pytest tests/test_no_create_database.py tests/test_insert_existing.py -q`：6 passed。
- K8s `dev`（缩容后）：API `0/0`；worker `1/1` 镜像 `gkx-entan-py-worker:fb145d45`；崩溃 Pod 已无。未改 `gkxlumen-platform-entan-py*`。

## 遗留风险

- MySQL 上原 `CREATE DATABASE gkxlumenx_dwd` 长会话若仍在，后续 `CREATE TABLE` 仍可能等 MDL；本叶未 KILL。
- 推送会触发 demo CI deploy；API 保持 0 副本直到人为或后续 scale 1。
- lumen `vendor/innov-py` 的 schema 仍含 `CREATE DATABASE`（非本叶 entan 启动路径）。

## CI/CD（必填）

- 分支：`origin/dev`（demo-algo-ent-analysis / lumen-algo-py / gkx-orchestration）
- commit：见各仓 push 后 SHA
- pipeline URL / ID：push 后回填
- 部署 namespace：`dev`；镜像 tag：本叶推送短 SHA
- K8s rollout：应急缩容已完成；修复镜像 rollout 待 CI + scale API 1
- dev 测试 URL：Service `demo-platform-entan-py` NodePort 30800，Endpoints 在 API 0 副本期间为空

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A（启动 DDL，无新埋点）
- traceId：N/A
- Tempo / Loki：无

## 涉及文件

- `repos/demo-algo-ent-analysis/entan/common/db.py`
- `repos/demo-algo-ent-analysis/entan/svcseed.py`
- `repos/demo-algo-ent-analysis/entan/llm_ods/load.py`
- `repos/demo-algo-ent-analysis/scripts/mysql/schema_mysql.sql`
- `repos/demo-algo-ent-analysis/scripts/mysql/svc_ddl_demo_empty.sql`
- `repos/demo-algo-ent-analysis/scripts/mysql/create_demo_dbs.sql`
- `repos/demo-algo-ent-analysis/tests/test_no_create_database.py`
- `repos/demo-algo-ent-analysis/.gitlab-ci.yml`
- `repos/lumen-algo-py/vendor/entan-py/**`（同上策略）
- `agent-delivery/data/data-design/storage/SVC/stores/mysql/ddl-demo-empty.sql`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ |
| 调用链 前端→Java→Python `/internal/*` | ✅ 未越层 |
| 图谱 Nebula，禁止 Neo4j | ✅ 未改 |
| 可观测性 | ✅ 本叶无新服务 |
| CI/CD push → Pipeline | ✅ 推 `origin/dev` |
| demo2 不 merge 进 lumen | ✅ lumen 只改 vendor 副本 |
| 共享聚合 / Java 不写算法 | ✅ |
| 数据 ADS / Mock | ✅ 不建库，只建表 |
| D8 Design | N/A |
| D9 指标 8 件套 | ✅ 未改口径 |
| D10 交互规范 | N/A |
| D12 lumen 不调 demo-* | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 120000 |
| model_used | grok-4 |
| actual_cost | 0.60 |
| cost_warn | green |
| 说明 | 估算 in+out；algorithm 默认 75/25 × Sonnet 公开价折算；source: session_estimate |
