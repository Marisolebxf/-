# DATA-CHAIN-STORAGE-S4-L01 · 旧路径 stub 指向 storage/CHAIN

> **日期**：2026-08-13  
> **前置**：`DATA-CHAIN-STORAGE-S3-L01` 经 `human:李伟` 确认放行  
> **强度**：ponytail **lite**

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:李伟` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `lite` |
| 说明 | chore/文档 stub；未删 DDL / 设计正文 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |

## 修改内容

1. 新增 `data-design/产业链/README.md` → 强制导航 `storage/CHAIN`  
2. **本目录全部 md** 文首 S4 横幅（含补漏）：  
   - DWD v5 / ADS v2 / ADS v1 对照 / 旧域设计 v1  
   - Step1、ODS→DWD v3、Step2、灌数对照、国内机构库映射  
   - `CHAIN-INST-DATA-ANALYSIS-L01.md`、`DEC-CHAIN-Q053-…`  
   - handoff 旧稿 `DATA-CHAIN-db-design.md`（PG/`chain_*`，标明勿当真源）  
3. 更新 `storage/CHAIN/{README,CHANGELOG}.md`

**未做**：删除旧 DDL / 映射报告正文；不开 stores 细表 approved 评审。

## DoD 自检

| DoD | 结果 |
|---|---|
| README + 强制导航 storage/CHAIN | ✅ |
| 主要旧稿文首横幅；冲突以 storage/CHAIN 为准 | ✅ |
| 不删旧 DDL 正文 | ✅ |
| CHANGELOG + handoff | ✅ |
| human:李伟 确认可签收 | ✅ 随「S3 确认，放行 S4」一并授权；registry=`done`（chore） |

## 架构合规

| 项 | 结果 |
|---|---|
| 冲突以 storage/CHAIN 为准 | ✅ |
| 功能设计不进 storage | ✅（本目录决议/说明仍留本地） |
| MySQL only / 三方 ODS≠live | ✅ 未改口径 |

## CI/CD

- 分支：`dev` · 纯文档 · N/A K8s

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~25k（估） |
| model_used | Cursor Grok 4.5 |
| actual_cost | <$1 |
| cost_warn | false |

## 下游

- 产业链存储 S1–S4 文档闭环（S1/S3 仍待淮政玮签收 → done）  
- 并行：Demo DWD/ADS DDL、Java 只读 ADS v2、细表 approved 另开  
