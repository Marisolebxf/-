# DATA-CHAIN-STORAGE-S3-L01 · 产业链存储 S3 — stores as-built 清单灌入

> **日期**：2026-08-13  
> **监管**：`human:李伟`  
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
| 说明 | 定义/文档类；指针+表清单，未跳过架构铁律；细表保持 draft |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机 MCP 面板未稳定；用 task-mcp-cli |

## 范围与实现

- 对照：`storage/ENT/stores/` 同构；流图 `01-data-flow`（会签 ≠ 细表 approved）。  
- 产物：`storage/CHAIN/stores/mysql/*`、`elasticsearch/*`、`nebula/*`。  
- DWD 真源：v5 `industry_chain_*` 十四表。  
- ADS 清单：`chain_*` 十一表（DATA-CHAIN-db-design §5；须 MySQL 化核验）。  
- **未**标 `approved`；**未**用供应方 ODS 四表冒充项目 DWD。  
- Demo `demo_dwd/ads` 物理建表：本单未强制执行（联调需要时补，见开放项）。

## 偏离说明

- 旧 `DATA-CHAIN-db-design` 为 PG/8 表稿；本树 DWD **以 v5 为准**，冲突已在 `dwd-chain.md` 写明。  
- ADS / Nebula 仍多指针摘要，全 DDL/ngql 不内嵌（防双源）。  
- ES mapping 设计文档尚未单独立项，索引名为建议稿。

## 产物清单

| 路径 | 说明 |
|---|---|
| `stores/README.md` | 索引 |
| `stores/mysql/{README,dwd-chain,ads,dim}.md` | DWD/ADS/DIM |
| `stores/elasticsearch/{README,index-chain,sync}.md` | ES |
| `stores/nebula/{README,graph-chain}.md` | Nebula |
| 本 handoff | — |

## 开放项

| ID | 内容 | Owner |
|---|---|---|
| OPEN-CHAIN-STORE-01 | ADS `chain_*` 现网 MySQL 列名 vs 设计稿对齐 | data / algorithm |
| OPEN-CHAIN-STORE-02 | ES 正式 mapping 文档补链 | data |
| OPEN-CHAIN-STORE-03 | Nebula Tag/Edge 与 v5 `*_rel` 命名对齐 | data / architect |
| OPEN-CHAIN-STORE-04 | Demo `demo_gkxlumenx_dwd/_ads` 按需补表 | data（联调触发） |
| OPEN-CHAIN-STORE-05 | 各细表结构评审 → approved | 数据 Lead + 会签 |
| （承接）OPEN-CHAIN-DIFF-03 | 资讯 IC*↔INB* | 见 S2 |

## 下游

- **放行 S4**：旧 `data-design/产业链/*` stub 可排（stores 已有实质内容）。  
- 须 **human:李伟** 确认本 handoff 后推进签收。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ |
| 调用链 / Java 只读 ADS | ✅ ads.md |
| Nebula only | ✅ |
| MySQL only（RDB） | ✅ |
| 三方 ODS≠项目 DWD | ✅ |
| 细表 draft | ✅ |

## CI/CD

- 分支：`gkx-orchestration` `dev`  
- commit：（随后填）  
- pipeline / K8s：N/A（纯文档）

## Cost（估）

| 字段 | 值 |
|---|---|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~4–6 万 |
| actual_cost | 估 <$3 |
| cost_warn | false |
