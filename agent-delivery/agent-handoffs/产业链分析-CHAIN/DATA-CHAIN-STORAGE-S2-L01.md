# DATA-CHAIN-STORAGE-S2-L01 · 产业链存储 S2 — sources/etl/seeds + Demo ODS 建表

> **日期**：2026-08-13  
> **确认**：`human:李伟`（监管/建表 Owner）· 实质完成并放行进入会签/签收路径  
> **淮政玮口径**：主责 = `demo_gkxlumenx_ods` 按在线约定建表；副产品 = 在线 md vs 三方真实四表差异 md

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:李伟` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full`（建表/脚本）+ 文档侧按派单 `lite` |
| 说明 | 未用 YAGNI 跳过真源铁律 / handoff；管道下游仅指针、细表留给 S3 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机 MCP 面板未稳定挂载；用 `scripts/task-mcp-cli.mjs` |

## 问题清单

- Demo 默认内网 `192.168.88.43` 超时 → 改用可达入口 `111.198.38.90:34306` 完成 `--apply`
- 三方 live 资讯编码 `IC*` 与链表 `INB*` 不一致（开放项 DIFF-03，不挡 S2 建表）
- 仓内 `gkx_schema_ddl.sql` 产业链旧片段滞后（DIFF-04）

## 修改内容

### A. 文档（orchestration · `storage/CHAIN`）

- `sources/inventory.md`：四表字段摘要 + 建表入口
- `sources/md-extract-vs-live-ods-diff.md`：**副产品**；2026-08-13 live DESCRIBE `@183.240.141.251:3318/gkx`
- `etl/`：`pipeline-demo-mock` + ods/dwd/ads/es/nebula/minio/mock-ads 指针齐套；DDL 快照
- `seeds/README.md`：覆盖矩阵骨架
- README / CHANGELOG 回填

### B. 建表（demo-algo-ent-analysis）

- `scripts/run_chain_ods.py`：md-extract「产业链要素库」→ `demo_gkxlumenx_ods`
- `entan/llm_ods/schema.py` / `load.py`：按表头解析主键；TEXT 前缀索引
- 已 `--apply` 四表；拒写正式 `gkxlumenx_ods`

### C. 三方探测证据

- `gkx-mysql-raw/加工/_chain_four_tables_live_2026-08-13.json`（结构；密码仅本机 `.env.local`）

## 测试结果

| 检查 | 结果 |
|---|---|
| `run_chain_ods.py --self-check` | OK（四表 + 业务键断言） |
| `run_llm_ods.py --self-check` | OK（ENT 回归） |
| `--apply` → `demo_gkxlumenx_ods` | OK · 四表 present（经 `111.198.38.90:34306`） |
| Live DESCRIBE 三方四表 | OK · 行数 1273 / 20000 / 20000 / 476 |

### Demo 四表

- `dwd_industry_chain_info`
- `dwd_org_industry_tags`
- `dwd_org_industry_product_tags`
- `dwd_industry_chain_news_info`

DDL 仓内：`storage/CHAIN/etl/demo_gkxlumenx_ods_chain_tables.sql`  
`SHOW CREATE` 本机旁路：`repos/demo-algo-ent-analysis/out/chain_demo_ods_show_create.sql`（`out/` gitignore）

## 遗留风险 / 开放项

| ID | 说明 | 是否挡 S3 |
|---|---|---|
| OPEN-CHAIN-DIFF-03 | 资讯 `IC*`↔`INB*` | 否（灌数/挂链时处理） |
| OPEN-CHAIN-DIFF-04 | 刷新沙箱 DDL 旧片段 | 否 |
| OPEN-CHAIN-S2-02 | 产品表 `id` live=bigint（在线标「数字」）已对齐；样例形态持续观察 | 否 |
| seeds 样例值 | 矩阵骨架已有，具体 INSERT 属 S3/灌数 | 否 |

**放行 S3**：`DATA-CHAIN-STORAGE-S3-L01`（stores mysql/es/nebula 细表）— `human:李伟` 确认可开。

## CI/CD

- 分支：`gkx-orchestration` → `dev`；`demo-algo-ent-analysis` → `dev`
- commit：algo `5c0f575`；orchestration `f9b98e8`（文档）+ `3cb3ced`（registry）
- pipeline：文档/脚本为主；无强制 K8s rollout
- 建表验证：直连 MySQL `--apply`（见上）

## 可观测性

- N/A（存储定义 + Demo DDL；无新服务）

## 架构合规自检

| # | 铁律 | |
|---|---|---|
| 1 | 算法只在 Python | ✅ 建表脚本在 Python |
| 2 | 调用链 | ✅ 未越层 |
| 3 | Nebula | ✅ 未引入 Neo4j |
| 4 | 可观测 | N/A 本单 |
| 5 | CI/CD | ✅ push 后随仓流水线 |
| 6 | demo→lumen | ✅ 仅 demo ODS |
| 7 | 共享核心 | N/A |
| 8 | ADS 先行 | ✅ S3 再灌 stores |
| 9 | D8 Design | N/A 无 UI |
| 10 | D9 血缘 | N/A 本单无指标页 |
| 11 | D10 交互 | N/A |

## 涉及文件

- `agent-delivery/data/data-design/storage/CHAIN/**`
- `agent-delivery/data/third-party-source/gkx-mysql-raw/加工/_chain_four_tables_live_2026-08-13.json`
- `repos/demo-algo-ent-analysis/scripts/run_chain_ods.py`
- `repos/demo-algo-ent-analysis/entan/llm_ods/{schema,load}.py`
- 本 handoff

## Cost（估）

| 字段 | 值 |
|---|---|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~8–12 万（多轮） |
| actual_cost | 估 <$5 |
| cost_warn | false |
