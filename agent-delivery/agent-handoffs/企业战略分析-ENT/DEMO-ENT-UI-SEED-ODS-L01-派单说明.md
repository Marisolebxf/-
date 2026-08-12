# DEMO-ENT-UI-SEED-ODS-L01 · 派单说明

> **日期**：2026-08-12  
> **Task ID**：`DEMO-ENT-UI-SEED-ODS-L01`（registry · **ready**）  
> **派单人**：`human:淮政玮`  
> **监管 / 落地 Owner**：`human:徐滕强`（认领时 `supervised_by=human:徐滕强`）  
> **执行 Agent**：`algorithm-agent`（主）· 协作 `frontend-agent` / `data-agent`  
> **仓**：`demo-ui-system-test`（UI 灌数入口）+ `demo-algo-ent-analysis`（流水线真实现）  
> **前置**：`DEMO-ENT-LLM-ODS-L01` = **done**；**Demo 库四件套已齐**（`DEMO-ENT-DEMO-DB-TRIPLE-L01` 库侧已落地：`demo_gkxlumenx_ods/dwd/ads/dim` + 授权 + settings 默认已切）  
> **强度**：ponytail **full**

---

## 0. 2026-08-13 口径补丁（必读）

| 项 | 值 |
|---|---|
| 开发默认库 | **仅** `demo_gkxlumenx_ods` / `_dwd` / `_ads` / `_dim` |
| ODS 真源 | `doc/` xlsx；**优先读** `md-extract/`（国内机构要素库已灌 33 表结构） |
| 禁止 | mockgen/run_all 默写 `gkxlumenx_dwd` 等正式库；不为其它平台库再建 demo |
| CFG | 继续共享 `gkxlumenx_cfg` |
---

## 1. 目标（一句话）

把企业 Demo **「灌数据」**从「mockgen 直写 DWD」改造成批准主路径：

```text
LLM/离线样例 → demo_gkxlumenx_ods（约定表 · md-extract）
            → ETL 模拟 GDF → demo_gkxlumenx_dwd
            → demo_gkxlumenx_ads /（既有）图谱·评估
```

（码表读 `demo_gkxlumenx_dim`；禁止落正式四库。）
并在 **`demo-ui-system-test` 企业页「灌数据」按钮**上反映真实步骤（不能只改文案不改后端）。

---

## 2. 现状（as-is）

| 层 | 现状 |
|---|---|
| UI | `demo-ui-system-test` · `src/views/entan/pages/BasicPage.vue` → `POST /entan/internal/run-pipeline` |
| API 封装 | `src/api/entan/index.ts` · `runPipeline` / `fetchEntanStatus` |
| 后端流水线 | `demo-algo-ent-analysis` · `scripts/run_all.py` · `STEPS`；其中 Mock 步 ≈ `entan/mockgen` **直写 `gkxlumenx_dwd`** |
| 已交付脚本（未接入灌数） | `entan/llm_ods/` · `scripts/run_llm_ods.py`（`--offline` / `--llm` / `--sql-out`）|
| 口径真源 | `storage/ENT/etl/pipeline-demo-mock.md`（approved）；ODS = `doc/` + **优先读** `md-extract/` |

---

## 3. 必读（按序）

| 序 | 路径 |
|---:|---|
| 1 | `agent-delivery/data/data-design/storage/ENT/etl/pipeline-demo-mock.md` |
| 2 | `agent-delivery/data/data-design/storage/ENT/seeds/README.md` |
| 3 | `repos/demo-algo-ent-analysis/entan/llm_ods/README.md` |
| 4 | `repos/demo-ui-system-test/src/views/entan/pages/BasicPage.vue`（seedFlow / seedNotes） |
| 5 | `repos/demo-algo-ent-analysis/scripts/run_all.py`（STEPS / Mock 步） |
| 6 | handoff：`DEMO-ENT-LLM-ODS-L01.md` |

---

## 4. 交付清单（DoD）

### A. 后端流水线（demo-algo-ent-analysis）— 必做

- [ ] 在 `run_all.py`（或等价 STEPS）中，**在原 mockgen 之前或替换 Mock 贴源步**：
  1. 调用 `entan.llm_ods`（默认 `--offline`）写入 **`demo_gkxlumenx_ods`**
  2. 增加「模拟 GDF」步：约定 ODS → 项目 DWD（至少覆盖已灌 P0：`dwd_org_base_info` / executive / news / annual_financial / shareholder → `enterprise_*`）；Mapping 对齐 GDF `09-…Mapping-v3`
- [ ] **明确**：`entan/mockgen` 降为旁路/兼容开关（如 `ENTAN_SEED_LEGACY_MOCKGEN=1`），默认主路径不得只跑 mockgen
- [ ] `/entan/internal/run-pipeline` 与 `/entan/internal/status` 能反映新步骤（running / last_error / 可选阶段名）
- [ ] 幂等可重跑；失败不静默半成功

### B. 前端灌数体验（demo-ui-system-test）— 必做

- [ ] 更新 `BasicPage.vue`（及若共用的其他 entan 页）`seedFlow` / `seedNotes`：
  - 写明：约定 ODS（md-extract）→ 模拟 GDF → DWD → 原有 A/B/C/D
  - 目标库文案含 `demo_gkxlumenx_ods`（或过渡说明）
- [ ] 状态标签：未灌数 / 灌数中 / 已就绪；若可区分「ODS 已有 / DWD 已有」更好（非强制）
- [ ] **不**改业务分析 Tab 算法语义；只改灌数入口与说明

### C. 验收证据

- [ ] 从 UI 点「灌数据」或等价 API 跑通一遍；附 status 截图或日志摘要
- [ ] handoff：`agent-handoffs/企业战略分析-ENT/DEMO-ENT-UI-SEED-ODS-L01.md`
- [ ] `supervised_by=human:徐滕强` 确认后推进签收

---

## 5. 禁止

- 以 `gkx-mysql-raw` live 作 ODS 建表真源  
- 只改 UI 文案、后端仍只 mockgen 直写 DWD 却宣称主路径达标  
- 另起第二套 ADS/DWD 表结构  
- 把 root 密码写入仓内配置（建库已完成；日常用 `gkxlumenx`）

---

## 6. 认领话术（给徐滕强 / 执行 agent）

```text
认领 DEMO-ENT-UI-SEED-ODS-L01
claimed_by=agent:algorithm-agent（或 human:徐滕强 亲自执行）
supervised_by=human:徐滕强
claim_type=pull
强度：ponytail full
目标：system-test 企业「灌数据」接入 llm_ods→约定 ODS→模拟 GDF→DWD
```

---

## 7. 开放项（本单可不关，须登记）

| 项 | 说明 |
|---|---|
| ODS→DWD Mapping 全量表 | 本单可先 P0 五表；招投标/产业链/风险扩表可另开 |
| `demo_gkxlumenx_dwd` 实例 | 若未建齐，过渡写 `gkxlumenx_dwd` 须在 UI/status 标明过渡 |
| OPEN-ENT-FLOW-01 | DAG/cron 名仍开；本单手工/API 灌数即可 |

---

**派单完成条件**：本说明入仓 + registry `ready` + 飞书/口头知会徐滕强。  
**本协调会话不执行改造代码**（仅派单）。
