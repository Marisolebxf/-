# DEMO-CHAIN-UI-SEED-ODS-L01 · 派单说明

> **日期**：2026-08-14  
> **Task ID**：`DEMO-CHAIN-UI-SEED-ODS-L01`（registry · **ready**）  
> **派单人**：`human:淮政玮`  
> **监管**：`human:淮政玮`（认领时 `supervised_by=human:淮政玮`）  
> **结构歧义升级**：`human:李伟`（禁止执行 agent 自创表结构）  
> **参考实现（非监管）**：`human:徐滕强` 企业灌数主路径（见 §0）  
> **执行 Agent**：`algorithm-agent`（主）· 协作 `data-agent` / `frontend-agent`  
> **仓**：`demo-algo-science`（`CHAIN_STEPS` / `/internal/run-chain-pipeline`）+ `demo-ui-system-test`（产业链「灌数据」）  
> **复用**：`demo-algo-ent-analysis/entan/llm_ods`（`schema.py` / `load.py` / `assert_demo_mysql_targets`）；**禁止**第二套 DDL 解析  
> **前置**：S1–S4 **done**（ODS 四表已建、0 行；DWD/ADS 细表仍 draft，本单按 v5/v2 **在 demo_* 建表并灌数**）  
> **强度**：ponytail **full**  
> **Epic**：`E-CHAIN-PROTOTYPE`

---

## 0. 对标徐滕强企业灌数（必须同等，禁止另起交互）

真源 handoff：`agent-handoffs/企业战略分析-ENT/DEMO-ENT-UI-SEED-ODS-L01.md`

| 口径 / commit | 产业链本单必须同等落地 |
|---|---|
| 三条拍板：默认 `append`；两种 mode 都 **TRUNCATE ADS 后按当前 DWD 全量重算**；主按钮追加 + 下拉 `replace` | 产业链 `BasicPage` + `POST /internal/run-chain-pipeline` body `{mode}` |
| `643ac63` llm_ods → 模拟 GDF → demo DWD | `CHAIN_STEPS` **替换** `mock_chain` 直写旧 `chain_*` |
| `5c10eab` `assert_demo_mysql_targets()`，库名不以 `demo_` 开头直接拒绝 | 产业链同样闸门；禁止写 `gkxlumenx_*` |
| `605d4c6` K8s 不依赖 `GKX_ROOT`，包内 md-extract 快照 | 产业链四表 CSV 进 `chainan/llm_ods/vendor/`（或等价） |
| `4d32c31` 一批约 50 + **按正式口径铺关联表** | 样例按 DWD v5 / ADS v2 铺开，禁止瘦表导致 CP0/CP1 全空 |
| `d8b8d89` 必填关联键禁止 NULL | `credit_code` / `industry_link_code` / `chain_id` 不得空 |
| `b4b075f` 状态 `ODS n｜DWD n｜ADS…` | 产业链标签同样三层计数 |
| 禁止 `init_schema(reset=True)`（会 DROP 到正式库名） | 缺表用 **demo 库 `CREATE LIKE` 正式结构**（无正式表则按 v5/v2 DDL 在 **仅 demo_*** 建）；不拷数据、不 DROP 正式库 |
| mockgen 仅 `ENTAN_SEED_LEGACY_MOCKGEN=1` | `CHAIN_SEED_LEGACY_MOCKGEN=1` 才走旧 `mock_chain`；默认不算验收 |

```text
append（默认）：保留 ODS/DWD 明细 → 新批次写入 demo ODS → 模拟 GDF INSERT demo DWD → ADS 全量重算
replace：TRUNCATE 约定四表 ODS + 映射 DWD → 同路径 → ADS 全量重算
```

---

## 1. 目标（一句话）

把产业链 Demo **「灌数据」**从「`mock_chain` 直写 `gkxlumenx_*` / 旧 `chain_*`」改造成批准主路径，并 **模拟完成全部数据加工与数据开发准备**（Demo 库可测）：

```text
LLM / 离线样例（确定性种子 + 可选 LLM 补全）
  → demo_gkxlumenx_ods 约定四表（md-extract · 角色=ODS）
  → ETL 模拟 GDF → demo_gkxlumenx_dwd.industry_chain_*（v5 十四表）
  → demo_gkxlumenx_ads v2 十表（同步面）
  → ES / Nebula Demo 投影（失败不阻断，状态诚实）
```

并在 **`demo-ui-system-test` 产业链页「灌数据」**上反映真实步骤（不能只改文案不改后端）。

---

## 2. 架构裁决（冲突时执行 agent 不得自选）

| 主题 | 现行真源 | 废作真源（禁止当施工） |
|---|---|---|
| 存储入口 / 流图 | `storage/CHAIN/`；`01-data-flow.md` **approved** · `human:李伟` | 旧 `DATA-CHAIN-db-design.md`（PG / 8 表） |
| ODS 四表 | `sources/inventory.md` + md-extract「产业链要素库」 | `gkx-mysql-raw` as-built；不存在的 `dwd_org_industry_chain_dtl` |
| 项目 DWD | v5 `industry_chain_*` 十四表 | 旧 `dwd.chain_*` / Mock 七表 |
| ADS | v2 十表 | v1 八表；旧 `ads.chain_*` |
| `chain_id` / `node_id` / `industry_id` | **Q053** = 供应方 INB 原文 | 自造 `CH*` 编码 |
| 灌数 UX / 幂等 | §0 徐滕强三条口径 | 单按钮 + mock 直写 DWD |
| 产业介绍 / 发展历程 | **CMS**；本单不灌长文进 DWD | 用 ODS 资讯冒充历程正文 |
| Job 诊断结果 | 不得写入全景 `graph_snapshot` | 与发布快照混表 |

**四表 ODS 填不满十四张 DWD**：映射子集（链/节点/节点关系/实体关系/资讯）必须有行；无源表（投融资、外部市场观测）可 **合成并标 🧪**；`milestone_event` 正文不灌。平台默认市场规模走 ADS（企业营收加总），**禁止**灌进 `market_observation`。

---

## 3. 必读（按序；禁止用压缩摘要代替精读）

| 序 | 路径 |
|---:|---|
| 1 | `agent-delivery/data/data-design/storage/CHAIN/README.md` |
| 2 | `…/storage/CHAIN/00-context.md` |
| 3 | `…/storage/CHAIN/01-data-flow.md`（§7 Demo 全链路） |
| 4 | `…/storage/CHAIN/sources/inventory.md` |
| 5 | `…/storage/CHAIN/sources/md-extract-vs-live-ods-diff.md` |
| 6 | `agent-delivery/data/data-design/产业链/产业链-DWD表设计-业务需求驱动(v5).md` |
| 7 | `agent-delivery/data/data-design/产业链/产业链-ADS表设计-原型与Handoff驱动(v2).md` |
| 8 | `…/storage/CHAIN/etl/pipeline-demo-mock.md` 及 `pipeline-ods-to-dwd.md` / `pipeline-dwd-to-ads.md` / `pipeline-dwd-to-es.md` / `pipeline-to-nebula.md` / `pipeline-to-minio.md` |
| 9 | `…/storage/CHAIN/seeds/README.md` |
| 10 | `agent-delivery/architecture-baseline.md`（调用链 / Java 只读 ADS / Nebula / D7） |
| 11 | **参考实现**：`agent-handoffs/企业战略分析-ENT/DEMO-ENT-UI-SEED-ODS-L01.md` + §0 commit |
| 12 | as-is 旧灌数：`repos/demo-algo-science/scripts/run_all.py`（`CHAIN_STEPS`）· `demo-ui-system-test/src/views/chain/pages/BasicPage.vue` |

Headroom：上表 1–10 **禁止 compress 代替精读**。

---

## 4. 样例覆盖（可测完备，SEED-01～08）

| ID | 必须有 |
|---|---|
| SEED-01 | ≥2 条链（集成电路 + 对照链），多层 `parent_code` |
| SEED-02 | 同一节点多企业；深圳 / 外地都有 |
| SEED-03 | 一企多产品；`product_top5` 有空有非空 |
| SEED-04 | 资讯有/无日期、长短摘要 |
| SEED-05 | 同一 `industry_code` 贯穿四表 |
| SEED-06 | **空节点**（结构在、企业为 0）→ 空态 |
| SEED-07 | 一条链节点够做上下游边 → CP1 全景不是单点 |
| SEED-08 | 与企业域可对上的 `credit_code` 若干条 |

规模建议：节点 80–150、企业 80–120、产品 150+、资讯 80+。确定性种子可复跑；LLM 只补名称/摘要/产品词，不改主键。

---

## 5. 交付清单（DoD）

### A. 后端流水线（demo-algo-science）— 必做

- [ ] `CHAIN_STEPS` 主路径：`llm_ods`（默认 offline）→ `demo_gkxlumenx_ods` 四表 → 模拟 GDF → `demo_gkxlumenx_dwd.industry_chain_*` → 按当前 DWD **全量重算** `demo_gkxlumenx_ads` v2 同步面  
- [ ] `assert_demo_mysql_targets()`（或同构闸门）；拒绝非 `demo_` 库  
- [ ] `POST /internal/run-chain-pipeline` body `{ "mode": "append"|"replace" }`；`/internal/status` 含 ODS/DWD/ADS 计数、`running` / `last_error` / `current_step`  
- [ ] 旧 `mock_chain` 仅 `CHAIN_SEED_LEGACY_MOCKGEN=1`  
- [ ] `--self-check`：行数、跨表 join、SEED-01～08、拒绝正式库  
- [ ] ES / Nebula Demo 投影：失败不阻断全链路；status 诚实（未灌/失败/已投影）

### B. 前端灌数（demo-ui-system-test）— 必做

- [ ] `src/views/chain/pages/BasicPage.vue` 对齐企业：split-button、`seedFlow` / `seedNotes` 写 demo_* 与 v5/v2，**不再**写 `gkxlumenx_*` / `dwd.chain_*`  
- [ ] `src/api/chain/index.ts`：`runChainPipeline(mode)`  
- [ ] 状态标签：`ODS n｜DWD n｜ADS n`

### C. 文档回写（gkx-orchestration）— 必做

- [ ] `storage/CHAIN/etl/pipeline-demo-mock.md` 灌数入口 as-built  
- [ ] `storage/CHAIN/seeds/README.md` 矩阵从「待灌」改为脚本/入口  
- [ ] `pipeline-ods-to-dwd.md` / `pipeline-dwd-to-ads.md` 补 Demo 脚本指针

### D. 验收证据

- [ ] UI 或等价 API 跑通一遍 append；正式库行数未变  
- [ ] handoff：`agent-handoffs/产业链分析-CHAIN/DEMO-CHAIN-UI-SEED-ODS-L01.md`  
- [ ] `supervised_by=human:淮政玮` 确认后推进签收

---

## 6. 禁止

- 默认写 `gkxlumenx_ods` / `_dwd` / `_ads`  
- 只改 UI 文案、后端仍 `mock_chain` 直写旧表却宣称主路径达标  
- 以 `DATA-CHAIN-db-design.md` / 旧 `chain_*` 当 DWD/ADS 真源  
- CMS 历程/介绍长文灌进 DWD；QC07 假值；Job 结果写入 `graph_snapshot`  
- 本单做 PDR、GDF 正式包、`lumen-ui-topic` 页面、Java 新门面  
- 密钥 / root 密码入库；`init_schema` DROP 正式库

---

## 7. `/goal`（粘贴到执行会话开头）

```text
/goal algorithm-agent
身份：你是经验丰富、遵循最佳实践的资深算法/数据工程师；算法与模拟 GDF 只在 Python。
强度：ponytail full。禁止用 YAGNI 跳过调用链、只写 demo_*、handoff。
任务 ID：DEMO-CHAIN-UI-SEED-ODS-L01
监管：human:淮政玮
结构歧义：升级 human:李伟，禁止自创表结构。
仓库：${GKX_ROOT}/repos/demo-algo-science（主）
      ${GKX_ROOT}/repos/demo-ui-system-test（产业链灌数据 UI）
复用：demo-algo-ent-analysis 的 llm_ods schema/load 与 assert_demo_mysql_targets；禁止第二套 DDL 解析。
参考实现（必须对齐交互与闸门，勿另起）：DEMO-ENT-UI-SEED-ODS-L01
  commit 643ac63 5c10eab 605d4c6 4d32c31 d8b8d89（ent-analysis）
  commit b4b075f（system-test）
架构：只读 storage/CHAIN 现行树 + DWD v5 + ADS v2；冲突以本派单说明「§2 裁决表」为准。
  禁止把 DATA-CHAIN-db-design / 旧 chain_* 当施工真源。
  必读全文（禁止 compress 代替）：本说明 §3。
目标：LLM/离线→demo ODS 四表→模拟 GDF→DWD v5→ADS v2；system-test 按钮 append/replace；样例 SEED-01～08。
DoD：见本说明 §5。
Handoff：agent-handoffs/产业链分析-CHAIN/DEMO-CHAIN-UI-SEED-ODS-L01.md
不要问我；阻塞写 handoff。结构争议停工升级李伟。
```

---

## 8. 认领话术

```text
认领 DEMO-CHAIN-UI-SEED-ODS-L01
claimed_by=agent:algorithm-agent
supervised_by=human:淮政玮
claim_type=pull
强度：ponytail full
目标：system-test 产业链「灌数据」接入 llm_ods→约定 ODS→模拟 GDF→DWD v5→ADS v2
```

---

## 9. 开放项（本单可不关，须登记）

| 项 | 说明 |
|---|---|
| OPEN-CHAIN-FLOW-01 | 正式 GDF DAG/cron 仍开；本单手工/API 灌数即可 |
| Q054 投融资 ODS | 本单合成 🧪，不伪称供应方已到 |
| CMS 历程/介绍 | 本单不灌；门户后续 CMS 单 |
| Job Snapshot | 本单不把七键诊断当同步 GET 真源 |
| `DEMO-ENT-UI-SEED-ODS-L01` | 企业灌数仍 `ready`（代码已合入）；本单**不硬依赖**其 registry 状态 |

---

**派单完成条件**：本说明入仓 + registry `ready` + 监管人 `human:淮政玮`。  
**本协调会话不执行改造代码**（仅派单）。
