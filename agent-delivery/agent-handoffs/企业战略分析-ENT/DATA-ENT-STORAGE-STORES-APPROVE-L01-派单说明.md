# DATA-ENT-STORAGE-STORES-APPROVE-L01 · 派单说明

> **日期**：2026-08-12  
> **Task ID**：`DATA-ENT-STORAGE-STORES-APPROVE-L01`（registry · **ready**）  
> **派单人**：`human:淮政玮`  
> **监管 / 结构签 Owner**：`human:徐滕强`（认领时 `supervised_by=human:徐滕强`）  
> **执行 Agent**：`data-agent`（主）· 协作 `architect-agent`  
> **仓**：`gkx-orchestration`（`storage/ENT/stores/**`）  
> **合包逻辑**：最粗② — S3 清单已灌入后的 **细表结构评审 → approved**  
> **前置**：`DATA-ENT-STORAGE-S3-L01` = **done**（清单 draft 已存在）  
> **强度**：ponytail **off**（定义/评审）

---

## 1. 目标（一句话）

对 ENT `stores/*` 细表做**单独结构评审**，可批准者升 `approved`；不可批准者保留 `draft` 并写清缺口。  
**流图会签不算细表 approved。**

---

## 2. 覆盖范围

| 路径 | 说明 |
|---|---|
| `stores/mysql/dwd-entity.md` | 工商/实体 DWD |
| `stores/mysql/dwd-risk.md` | 风险 DWD |
| `stores/mysql/dwd-aggregate.md` | 预聚合 |
| `stores/mysql/ads.md` | ADS 契约面 |
| `stores/mysql/dim.md` | 码表（含行政区划核验或记 OPEN） |
| `stores/elasticsearch/*` | 索引与 sync |
| `stores/nebula/*` | 企业图谱 |

输出：评审纪要 / 差异清单 + `CHANGELOG`；`stores/mysql/README.md` 状态列更新。

---

## 3. 必读

| 序 | 路径 |
|---:|---|
| 1 | `storage/ENT/01-data-flow.md` §6（细表不得仅因流图升格） |
| 2 | `storage/ENT/stores/mysql/README.md` |
| 3 | `storage/README.md`（stores 规范） |
| 4 | 外链 as-built / 旧 `data-design/企业/` DDL（冲突以 storage/ENT 为准） |

---

## 4. DoD

- [ ] 逐文件评审；可升则 frontmatter `status: approved` + 签收人/日期
- [ ] 不可升：保留 draft + 缺口列表（禁止「为干净而改绿」）
- [ ] dim 码表路径核验或新 OPEN
- [ ] handoff：`…/DATA-ENT-STORAGE-STORES-APPROVE-L01.md`
- [ ] 徐滕强结构确认后再进签收链

---

## 5. 禁止

- 仅因 S1 流图 / S3 清单灌入就把细表标 approved  
- 手改前端/算法把 D2「改绿」冒充结构批准  
- 本单不做 llm_ods 扩表（见合包③）

---

## 6. 认领话术

```text
认领 DATA-ENT-STORAGE-STORES-APPROVE-L01
claimed_by=agent:data-agent（或 human:徐滕强）
supervised_by=human:徐滕强
claim_type=pull
强度：ponytail off
目标：ENT stores 细表结构评审升 approved
```

---

**合包汇总**：[`ENT-STORAGE-COARSE-DISPATCH-2026-08-12.md`](./ENT-STORAGE-COARSE-DISPATCH-2026-08-12.md)
