# DATA-SVC-STORAGE-S3-L01 · 派单说明

> **日期**：2026-08-14  
> **Task ID**：`DATA-SVC-STORAGE-S3-L01`（registry · **ready（本地）** · 依赖 S2 本地签收）  
> **派单人**：`human:淮政玮` / **本地放行**：`human:侯佳伟`（2026-08-14）  
> **监管**：`human:侯佳伟`  
> **执行 Agent**：`data-agent` · 协作 `architect-agent`  
> **前置**：`DATA-SVC-STORAGE-S2-L01` Owner **本地签收**（会签通过 · **未 push**）→ 本单放行  
> **强度**：ponytail **lite**  
> **汇总**：[`SVC-STORAGE-S1-S4-DISPATCH-2026-08-14.md`](./SVC-STORAGE-S1-S4-DISPATCH-2026-08-14.md)

---

## 1. 目标

向 `storage/SVC/stores/*` 灌入 **项目侧结构清单**（MySQL 含 **ADS 必含** · ES · Nebula），细表保持 **draft**，放行 S4。

对齐 E7 叶子读模型：机构画像 / 服务链生态 / 招引培育 / 门户统计。缺口进开放项或后续 gap catalog，**不编造已批准契约**。

---

## 2. 必读

| 序 | 路径 |
|---:|---|
| 1 | `storage/SVC/01-data-flow.md`（流图会签 ≠ 细表 approved） |
| 2 | `storage/ENT/stores/` · `storage/CHAIN/stores/`（目录模板） |
| 3 | E7 四叶子五件套（ADS 应对哪些页面） |
| 4 | `data-design/服务机构/服务机构域数据库设计(v1).md`（**输入对照**，冲突以本树为准） |
| 5 | S2 handoff + `sources/inventory.md` |

---

## 3. DoD

- [ ] `stores/mysql/{dwd-*,ads,dim}.md` + README 状态列；**ADS 必有**  
- [ ] `stores/elasticsearch/*` · `stores/nebula/*`  
- [ ] 写清与 ENT 共用实体（机构主数据）vs 本域表（圈定标签、关系、本域指标切片）  
- [ ] 真源外链清晰；冲突以 `storage/SVC` 叙述为准  
- [ ] 若 Demo 联调需要：在 **`demo_gkxlumenx_dwd` / `_ads`** 补齐本域缺表（结构对齐本树 stores；**不是**用正式库 as-built 覆盖在线 ODS 约定）  
- [ ] **禁止**仅因 S1 会签把细表改 `approved`  
- [ ] Q-SVC-010 未决策前，圈定结果表标 draft + 待核验，不标 live 契约  
- [ ] handoff · Owner 确认 · 放行 S4  

---

## 4. 禁止

- 以 L01 / 现网探库覆盖 md-extract ODS 约定  
- 复制一整套 ENT 工商细表到 SVC stores  
- 伪闭合技术力 / 招引模型口径（Q-SVCCHAIN-01～05 走 METRIC-OPEN）  

---

## 5. 认领话术（S2 本地签收后 · 可开）

```text
认领 DATA-SVC-STORAGE-S3-L01
claimed_by=agent:data-agent
supervised_by=human:侯佳伟
claim_type=coordinator_dispatch
强度：ponytail lite
说明：S2 本地签收放行；六类/Q-SVC-010 另轨；细表 draft；不 push 除非 Owner 另行指示
```
