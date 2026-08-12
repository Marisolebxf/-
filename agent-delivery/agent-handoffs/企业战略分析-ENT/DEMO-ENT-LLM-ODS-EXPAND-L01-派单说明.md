# DEMO-ENT-LLM-ODS-EXPAND-L01 · 派单说明

> **日期**：2026-08-12  
> **Task ID**：`DEMO-ENT-LLM-ODS-EXPAND-L01`（registry · **ready**）  
> **派单人**：`human:淮政玮`  
> **监管 / 落地 Owner**：`human:徐滕强`（认领时 `supervised_by=human:徐滕强`）  
> **执行 Agent**：`algorithm-agent`（主）· 协作 `data-agent` / `devops-agent`  
> **仓**：`demo-algo-ent-analysis`（实现）+ `gkx-orchestration`（seeds / pipeline 回写）  
> **合包逻辑**：最粗③ — seeds「待扩展」+ MinIO 样例 + Nebula demo space 定名  
> **硬依赖**：`DEMO-ENT-LLM-ODS-L01` = **done**  
> **软依赖**：`DEMO-ENT-UI-SEED-ODS-L01`（灌数 UI 主路径；**不硬挡 ready**，全链路强验收建议等其合入）  
> **强度**：ponytail **full**

---

## 1. 目标（一句话）

把 Demo 样本从「P0 五表骨架」扩到 seeds 矩阵缺的场景，并补齐对象桶样例与图谱 demo space 命名/灌边，仍遵守：

```text
LLM/离线 → demo_gkxlumenx_ods（doc/md-extract）→（模拟 GDF）→ 下游
```

---

## 2. 覆盖范围

| 块 | 内容 | 最低验收 |
|---|---|---|
| **A. llm_ods 扩表** | 招投标 `dwd_bid_*`；产业链 tags/chain；风险 abnormal/punish/judicial 等 ≥3 类 | offline 矩阵对应行「脚本/入口」可跑 |
| **B. 可选** | `stock_*`、special_* 字段加厚 | 做不到则 handoff 写延期，不挡关单 |
| **C. MinIO 样例** | 1× PDF/HTML + 元数据路径；桶名对齐 `demo-*` / 过渡说明 | 不替代业务表 |
| **D. Nebula** | `demo_entan` vs `demo_gkx_enterprise` **二选一拍板**；≥1 供应链或投资边 | 回写 `pipeline-demo-mock.md` 命名表 |

回写：`storage/ENT/seeds/README.md`；必要时 `pipeline-demo-mock.md`。

---

## 3. 必读

| 序 | 路径 |
|---:|---|
| 1 | `storage/ENT/seeds/README.md`（待扩展行） |
| 2 | `storage/ENT/etl/pipeline-demo-mock.md` |
| 3 | `repos/demo-algo-ent-analysis/entan/llm_ods/README.md` |
| 4 | `doc/md-extract/` 与 `sources/inventory.md`（表名口径） |
| 5 | 合包① MinIO 若未关：可用过渡桶，须标明 |

---

## 4. DoD

- [ ] A 三类场景可 `--offline`（或 `--llm`）灌入约定 ODS；自检/日志可复现  
- [ ] C + D 达标或明确阻塞（跟 OPEN-02）  
- [ ] seeds 矩阵脚本列更新  
- [ ] handoff：`…/DEMO-ENT-LLM-ODS-EXPAND-L01.md`  
- [ ] `supervised_by=human:徐滕强` 确认  

---

## 5. 禁止

- 以 `gkx-mysql-raw` as-built 当 ODS 真源  
- 另起第二套表结构  
- 用扩表冒充灌数 UI 主路径改造（那是 `DEMO-ENT-UI-SEED-ODS-L01`）  
- 密钥入库  

---

## 6. 认领话术

```text
认领 DEMO-ENT-LLM-ODS-EXPAND-L01
claimed_by=agent:algorithm-agent（或 human:徐滕强）
supervised_by=human:徐滕强
claim_type=pull
强度：ponytail full
目标：llm_ods 招投标/产业链/风险扩覆盖 + MinIO 样例 + Nebula demo space
```

---

**合包汇总**：[`ENT-STORAGE-COARSE-DISPATCH-2026-08-12.md`](./ENT-STORAGE-COARSE-DISPATCH-2026-08-12.md)
