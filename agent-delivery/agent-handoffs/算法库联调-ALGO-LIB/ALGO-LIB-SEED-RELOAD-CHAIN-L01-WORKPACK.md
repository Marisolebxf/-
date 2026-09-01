# 派单厚包 · 产业链灌数据补「重灌」(对照政策)

```yaml
---
doc_id: ALGO-LIB-SEED-RELOAD-CHAIN-L01-WORKPACK
task_id: ALGO-LIB-SEED-RELOAD-CHAIN-L01
dispatcher: agent:coordinator-agent
supervised_by: human:李伟
date: 2026-09-01
claim_type: coordinator_dispatch
status: claimed
---
```

> 调度者只建单、写厚包、给 `/goal`。**不写业务代码。**  
> 执行真源=本厚包 + registry DoD。政策页是金标准，禁止另发明第四档。  
> 企业叶 `ALGO-LIB-SEED-RELOAD-ENT-L01`（徐滕强）并行、不同仓，不挡本叶。

## 1. 为什么派

政策基础指标页「灌数据」已是三档：追加 / **重灌** / 重建。  
产业链基础指标页（`#/chain/basic`）现只有追加 + 重建。重建会 **TRUNCATE 约定四表 ODS**，三方或 Mock 贴源进 ODS 之后无法「留树、只重算 DWD/ADS」。

本叶只做 **产业链**。企业已另派。产业服务另开叶。

**本叶不含** 政策页右侧「数据同步」（三方 `gkx` → Demo ODS）。

## 2. 金标准（政策 as-built）

| 档 | mode | 语义 |
|---|---|---|
| 追加 | `append` | 读 ODS 增量，不清贴源 |
| **重灌** | `reload` | **保留 ODS，只清 DWD，再全量 ODS→DWD 并重算 ADS** |
| 重建 | `replace` | 清 ODS+DWD，再造底树 |

政策对照只读：`policy/pages/BasicPage.vue`、`polan/mockgen/incr.py#reload_from_ods`。  
灌数剥离图谱：`COORD-GRAPH-TRIPLE-UI-DISPATCH-20260831.md` §0.1。

## 3. 产业链现网缺口（必须改）

| 文件 | 现状 | 本叶 |
|---|---|---|
| `chainan/llm_ods/seed.py` | 只认 `append\|replace`；replace 会 TRUNCATE 四表 ODS 再造树 | 增 `reload`：不清 ODS、不 `build_offline_rows` 造数；只清映射 DWD 后 `apply_ods_to_dwd` 全量映入，再 `recalc_ads` |
| `scripts/run_all.py` `run_chain()` | `mode = "replace" if mode == "replace" else "append"` | 三档原样下传；CLI `--mode` 接受 `reload` |
| `api/main.py` `/internal/run-chain-pipeline` | `payload.mode in ("append", "replace")` | 接受 `reload` |
| `demo-ui-system-test/.../chain/pages/BasicPage.vue` | 下拉两项 + 两卡对照 | 中间加「重灌」项 + 第三张对照卡 + 确认框 |

网关路径现网：`POST /innov/v1/industry/internal/run-chain-pipeline`。只写 Demo。

## 4. 硬闸

1. **只写 Demo**：`demo_gkxlumenx_ods / _dwd / _ads`。正式 `gkxlumenx_*` 禁止。顶栏「产业链」= live 时禁用（现网已有）。
2. **重灌不清 ODS**：约定四表（含 `dwd_industry_chain_info` / `dwd_org_industry_tags` 等）行数重灌前后必须一致。禁止整表 TRUNCATE ODS。
3. **重灌不造底树**：禁止走 `build_offline_rows` / `write_rows(..., truncate=True)`。
4. **图谱剥离**：`run_chain` / `run-chain-pipeline` / 本页灌数 **grep 不到** graph / nebula / hang-to-graph。图只走全景 / 深圳产业链菜单。
5. **追加 / 重建语义不得被改坏**：append 仍只补缺失节点 + 延伸链；replace 仍清四表 ODS+映射 DWD 再灌 10+5 全树。
6. **企业上链**：上链是另一步。重灌若 TRUNCATE 映射 DWD，挂接可能作废——handoff 必须写明 as-built，禁止文案写成「挂接仍在」却实际被清。
7. **禁止** 本叶做三方「数据同步」、禁止改 lumen 正式仓、禁止 merge demo→lumen。  
   lumen-algo-py `vendor/innov-py` 仅当本仓与 vendor 必须同文时才碰，默认只改 `demo-algo-science`。

## 5. UI 文案（照政策句式，换产业链词）

下拉顺序固定：

1. 【追加】保留已有产业树，只补新节点/延伸链（默认）
2. **【重灌】保留 ODS，只清 DWD 并按现有产业树重算指标**
3. 【重建】清空贴源与明细后再灌完整 3.0 底树 ← 保持 `divided`

确认框：

> 将保留 ODS 约定四表（产业树贴源），只清空产业链映射 DWD，再把现有 ODS 全量映入 DWD 并重算 ADS 全景切面。不写 Nebula、不建图。企业上链若挂在映射 DWD 上，重灌后需重跑上链。是否继续？

对照卡补第三张「重灌」：不清 ODS、不造树、不建图。

## 6. 验收

1. Demo 产业链基础指标页下拉可见三档；正式面禁用。
2. 对已有 ODS 点「重灌」：ODS 四表行数不变；DWD `industry_chain` 按现有 ODS 重映；ADS fact/全景可刷新。
3. 「追加」在无新节点时行为与现网一致（不误走 reload）。
4. 「重建」仍会清 ODS（与重灌可区分）。
5. handoff 附：三档对照 + 重灌前后 ODS/DWD/ADS 行数 + 上链挂接 as-built + `grep` 灌数路径无 nebula/graph。

## 7. 并行叶

| ID | 监管人 | 仓 |
|---|---|---|
| `ALGO-LIB-SEED-RELOAD-ENT-L01` | 徐滕强 | `demo-algo-ent-analysis` |
| `ALGO-LIB-SEED-RELOAD-CHAIN-L01` | 李伟 | `demo-algo-science` |
| `ALGO-LIB-SEED-RELOAD-SVC-L01` | 未建 | — |

## 8. /goal 监管人

已确认 `supervised_by: human:李伟`。`claimed_by: agent:algorithm-agent`，`claim_type: coordinator_dispatch`。
