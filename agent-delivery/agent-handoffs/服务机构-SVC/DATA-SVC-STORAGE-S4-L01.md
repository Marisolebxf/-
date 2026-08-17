# DATA-SVC-STORAGE-S4-L01 · 旧路径 stub 指向 storage/SVC

> **日期**：2026-08-17  
> **前置**：S3 stores 清单已本地交付；Owner 指示「进行本地 S4」= **本地签收 S3 并放行 S4**  
> **强度**：ponytail **lite**  
> **Git**：**不 commit / 不 push**

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch`（本地） |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `lite` |
| 说明 | chore/文档 stub；未删旧正文；未开 stores approved |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 远端 registry 拉码后无本单；仅本地 handoff |

## 修改内容

1. 新增 `data-design/服务机构/README.md` → 强制导航 `storage/SVC`  
2. `服务机构域数据库设计(v1).md` 文首横幅：冲突以 `storage/SVC` 为准；勿作建表真源  
3. `SVC-DATA-ANALYSIS-L01-数据分析报告.md` 文首横幅：**legacy 分析纪要，非 ODS/stores 真源**；开放项仍指决策清单 §2.ae  
4. `storage/SVC/{README,CHANGELOG}.md` 回填 S3 本地签收 + S4  
5. `storage/README.md` 补回 SVC 同构登记 + 旧路径映射（拉码后远端丢失）  
6. 更新本派单说明头信息  

**未做**：删除旧报告 / v1 正文；不开字段级 DDL / stores approved；不伪闭合 Q-SVC-010。

## DoD 自检

| DoD | 结果 |
|---|---|
| README + 强制导航 storage/SVC | ✅ |
| v1 文首横幅 | ✅ |
| L01 文首横幅（legacy / 非真源 / §2.ae） | ✅ |
| CHANGELOG + handoff | ✅ |
| 不删旧正文 | ✅ |
| 本地 only（无 push） | ✅ |

## 架构合规

| 项 | 结果 |
|---|---|
| 冲突以 storage/SVC 为准 | ✅ |
| L01 不作建表真源 | ✅ |
| 未升 stores approved | ✅ |

## CI/CD

- 分支：本地工作区 · **未 push** · N/A K8s

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~20k（估） |
| model_used | Cursor Grok 4.5 |
| actual_cost | <$1 |
| cost_warn | false |

## 下游

- SVC 存储 S1–S4 **本地文档闭环**（registry 需另挂回远端时由 coordinator 处理）  
- 字段级 DDL / 对比篮键 / ADS 单轨 → **另开**结构补钉单（非 S4）  
- Q-SVC-010 另轨  
