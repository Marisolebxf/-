# DATA-ENT-STORAGE-S3-L01 · 派单说明

> **日期**：2026-08-12  
> **阶段**：企业维存储 **S3**（`stores/*` 从项目侧 as-built 灌入）  
> **前置**：`ARCH-ENT-STORAGE-FLOW-SIGNOFF-L01` + `DATA-ENT-STORAGE-S2-L01` = **done**  
> **Task ID**：`DATA-ENT-STORAGE-S3-L01`  
> **执行**：`human:淮政玮`（pull · 自监管）  
> **强度**：ponytail **lite**（文档指针与表清单；不粘贴整份 DDL、不改业务代码）

---

## 1. 目标

把 **项目侧** MySQL DWD/ADS/DIM、ES、Nebula 的 **as-built** 写入 `storage/ENT/stores/**`，使 Demo/正式共用结构入口可读；**不**把流图会签当成细表 approved。

**明确排除**：三方 ODS 结构仍认 `third-party-source/doc/`（优先读 `md-extract/`）；不灌 `gkx-mysql-raw`。

---

## 2. 必读

| 序 | 路径 |
|---:|---|
| 1 | `data-design/storage/README.md` §5 / §8 |
| 2 | `storage/ENT/01-data-flow.md`（S3 放行条款） |
| 3 | 工商 v3.1 / 指标汇总 v3.1 / 模块 MySQL-v3.0 |
| 4 | `企业搜索-ES索引设计.md` · `demo-algo-ent-analysis/docs/nebula-space-schema.md` |

---

## 3. DoD

- [x] mysql：entity / risk / aggregate / ads / dim  
- [x] elasticsearch：index + sync 指针  
- [x] nebula：graph-enterprise  
- [x] 细表 `status=draft`  
- [x] handoff + 开放项（结构评审、DIM 行政区划核验、ADS 列名 MySQL 核验）

---

## 4. 禁止

整份 DDL 粘贴进 stores；细表直接 `approved`；以三方 live 倒逼项目 DWD。
