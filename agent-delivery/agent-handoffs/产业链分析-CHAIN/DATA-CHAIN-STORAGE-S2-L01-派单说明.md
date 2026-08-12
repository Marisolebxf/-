# DATA-CHAIN-STORAGE-S2-L01 · 派单说明

> **日期**：2026-08-12  
> **Task ID**：`DATA-CHAIN-STORAGE-S2-L01`（registry · **backlog** · 依赖 S1）  
> **派单人**：`human:淮政玮`  
> **监管**：`human:李伟`  
> **执行 Agent**：`data-agent` · 协作 `architect-agent`  
> **前置**：`ARCH-CHAIN-STORAGE-FLOW-SIGNOFF-L01` = **done** 后升 **ready**  
> **阶段**：产业链存储 **S2**  
> **强度**：ponytail **lite**

---

## 1. 目标

流图会签后，落地 **sources / etl / seeds** 清单与 Demo Mock 口径，放行 S3。

主路径（与规范一致，不得改拓扑）：

```text
LLM/离线 → demo_* ODS（约定=doc/md-extract 产业链）→ ETL 模拟 GDF → demo_* DWD → ADS/ES/Nebula/MinIO
```

---

## 2. 必读

| 序 | 路径 |
|---:|---|
| 1 | `storage/CHAIN/01-data-flow.md`（会签版） |
| 2 | `storage/ENT/etl/pipeline-demo-mock.md`（写法模板） |
| 3 | `third-party-source/doc/md-extract/…产业链要素库…`（及 xlsx 权威） |
| 4 | GDF Mapping：`data/GDF/Mapping/产业链/`（若有） |
| 5 | S1 handoff |

---

## 3. DoD

- [ ] `sources/inventory.md`：ODS 表级清单 + 真源入口  
- [ ] `etl/`：demo-mock + ods→dwd / dwd→ads / es / nebula / minio 指针  
- [ ] `seeds/README.md`：覆盖矩阵骨架  
- [ ] 开放项推进或登记；CHANGELOG  
- [ ] handoff：`…/DATA-CHAIN-STORAGE-S2-L01.md` · 李伟确认 · 放行 S3  

---

## 4. 禁止

- 现网 as-built 当 Demo ODS 真源  
- 本单灌 stores 细表 as-built（属 S3）  
- 密钥入库  

---

## 5. 认领话术（S1 done 后）

```text
认领 DATA-CHAIN-STORAGE-S2-L01
claimed_by=agent:data-agent（或 human:李伟）
supervised_by=human:李伟
claim_type=pull
强度：ponytail lite
```

---

**汇总**：[`CHAIN-STORAGE-S1-S4-DISPATCH-2026-08-12.md`](./CHAIN-STORAGE-S1-S4-DISPATCH-2026-08-12.md)
