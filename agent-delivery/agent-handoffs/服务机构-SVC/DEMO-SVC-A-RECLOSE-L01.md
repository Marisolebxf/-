# DEMO-SVC-A-RECLOSE-L01 · 产业服务链 A — Demo 库可测闭环重跑

> 日期：2026-08-18  
> Task：`DEMO-SVC-A-RECLOSE-L01`  
> 总控：`DEMO-SVC-ABCD-长任务总控.md`（已授权 · human:侯佳伟；本叶监管人本会话 `human:淮政玮` 令重跑）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| lock | 24h |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用已有三脚本，不新写第二套主表/灌数器；未用 YAGNI 跳过零写正式库、Q-SVC-010 待核验、handoff |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶连库+短 JSON，未 compress |

## 问题清单

- 旧 `DEMO-SVC-SEED-ODS/MOCK/ENRICH` 标过 `integration`，但 `out/` 证据未入库、`pipeline-demo-mock.md` 仍写「S2 待回填」→ **不能当 C 闸门**
- 内网 `10.50.11.76:3306` 本机不可达 → 沿用 NAT `111.198.38.90:34306`
- ADS 全表 `pending_client_confirm` 曾 >24（含非 MOCK 残留）；**MOCK 码 24 户 pending=24**
- OPEN-SVC-FLOW-01/03/04（DAG / MinIO / ES·Nebula SLA）仍开放，**不挡**「Demo MySQL 可测」
- 正式 schema `gkxlumenx_{ods,dwd,ads}` 存在；本叶 **零写入**

## 修改内容

### 重跑（`demo-algo-ent-analysis`，未改脚本逻辑）

| 命令 | 结果 |
|---|---|
| `run_svc_ods_reconcile.py --self-check` | OK |
| `--check --json-out out/svc_a_reclose_ods.json` | `aligned=true` · 33 表 · 缺表/缺列空 |
| `apply_svc_demo_ddl.py`（无 `--rebuild-mismatch`） | DWD 五表 + ADS 骨架 live |
| `seed_svc_demo_mock.py` | batch `svc-mock-20260818` · 24 户 |

live 抽检：`dwd_org_base_info` 100 行 · `industry*` 9 列 · DWD/ADS MOCK 各 24 · ranking 8+8。

### 文档（orchestration）

- `storage/SVC/etl/pipeline-demo-mock.md` → **as-built**（脚本入口、命名表、决策 #7、live 表、禁止旧 SEED 单独开 C）
- `DEMO-SVC-A-总派单.md` / `DEMO-SVC-ABCD-长任务总控.md`：C 只认本叶
- `seeds/README.md` · `etl/README.md` · `SVC/README.md` · `CHANGELOG.md`

## 测试结果

| 检查 | 结果 |
|---|---|
| ODS aligned | ✅ |
| MOCK ≥20 + pending | ✅ 24 |
| 零写正式库 | ✅（脚本拒非 `demo_`；未对 `gkxlumenx_*` 发 DDL/DML） |
| `pipeline-demo-mock` 可复跑 | ✅ |

## 遗留风险

- 模拟 GDF DAG 名未登记（OPEN-SVC-FLOW-01）
- ES / Nebula / MinIO 本叶未重灌（不挡 MySQL 退出门）
- 旧 SEED 三叶仍 `needs-revision`，勿 AV 回 `integration`

## CI/CD

- 分支：`gkx-orchestration` / `demo-algo-ent-analysis` 工作区 `dev`
- commit：文档本叶；脚本无 diff；`out/` gitignore
- pipeline / K8s：N/A（Demo 库作业）

## 可观测性

- N/A（无新服务）

## 涉及文件

- `agent-delivery/data/data-design/storage/SVC/etl/pipeline-demo-mock.md`
- `agent-delivery/data/data-design/storage/SVC/etl/README.md`
- `agent-delivery/data/data-design/storage/SVC/seeds/README.md`
- `agent-delivery/data/data-design/storage/SVC/README.md`
- `agent-delivery/data/data-design/storage/SVC/CHANGELOG.md`
- `agent-delivery/agent-handoffs/服务机构-SVC/DEMO-SVC-A-总派单.md`
- `agent-delivery/agent-handoffs/服务机构-SVC/DEMO-SVC-ABCD-长任务总控.md`
- 本 handoff

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 脚本在 Python |
| 2 | 调用链 | ✅ 未越层 |
| 3 | Nebula | ✅ 未引入 Neo4j；space 仍决策 #7 |
| 6 | demo 不污染 lumen/正式 | ✅ 仅 demo_* |
| 8 | ADS | ✅ Demo ADS 可读 |
| D9 | 待核验不伪闭合 | ✅ pending + Q-SVC-010 |
| D12 | 不写正式 ODS 当真源 | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.6 |
| actual_tokens | 估 ~9 万 |
| actual_cost | 估 <$6 |
| cost_warn | false |

## 联调确认

联调通过：Demo ODS 对齐 + 本域表可连 + MOCK 24 户待核验可读。**段 A 退出门已关。** C 下一张仍是 `LUMEN-SVC-JAVA-API-SEARCH-ORGS-L01`，须等本叶 ≥ `integration` 后再升 ready。
