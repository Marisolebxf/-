# DATA-CHAIN-STORAGE-S3-L01 · 产业链存储 S3 — stores as-built 清单灌入

> **日期**：2026-08-13  
> **监管**：`human:李伟`  
> **强度**：ponytail **lite**  
> **收口**：ADS 真源切换为 **v2**（团队认定 DWD+ADS 已定）

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
| 说明 | 定义/文档类；指针+表清单；未跳过架构铁律；细表保持 draft |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机 MCP 面板未稳定；用 task-mcp-cli |

## 范围与实现

- 对照：`storage/ENT/stores/` 同构；流图 `01-data-flow`（会签 ≠ 细表 approved）。  
- 产物：`storage/CHAIN/stores/mysql/*`、`elasticsearch/*`、`nebula/*`。  
- DWD 真源：**v5** `industry_chain_*` 十四表（`dwd-chain.md`）。  
- ADS 真源：**v2** `产业链-ADS表设计-原型与Handoff驱动(v2).md`（**10 物理表**）；`stores/mysql/ads.md` 已改指针；**v1 仅对照**。  
- **未**标 stores 细表 `approved`；**未**用供应方 ODS 四表冒充项目 DWD。  
- Demo `demo_dwd/ads` 物理建表：本单未强制（OPEN-CHAIN-STORE-04 / OPEN-CHAIN-ADS-V2-06）。

## 偏离说明

- 旧 `DATA-CHAIN-db-design` 为 PG/8 表稿；本树 DWD **以 v5 为准**。  
- S3 首灌曾指 ADS v1；收口按团队「DWD+ADS 已定」切换至 **v2**（相对 v1 增 `metric_dist` / `region_dist`）。  
- ADS / Nebula 仍多指针摘要，全 DDL/ngql 不内嵌（防双源）。  
- ES mapping 设计文档尚未单独立项，索引名为建议稿。

## 产物清单

| 路径 | 说明 |
|---|---|
| `stores/README.md` | 索引 |
| `stores/mysql/{README,dwd-chain,ads,dim}.md` | DWD=v5；**ADS=v2**；DIM |
| `stores/elasticsearch/{README,index-chain,sync}.md` | ES |
| `stores/nebula/{README,graph-chain}.md` | Nebula |
| `storage/CHAIN/CHANGELOG.md` | S3 收口行 |
| 本 handoff | — |

## DoD 自检

| DoD | 结果 |
|---|---|
| stores/mysql（含 ads）/es/nebula 灌入 draft 清单 | ✅ |
| 细表 frontmatter 保持 draft | ✅ |
| README + CHANGELOG 更新 | ✅ |
| handoff 经 human:李伟 确认；放行 S4 | ✅ **2026-08-13 ·「S3 确认，放行 S4」** |

## 开放项

| ID | 内容 | Owner | 挡 S4？ |
|---|---|---|---|
| OPEN-CHAIN-ADS-V2-01 | v2 纸面多签（李伟 + 架构 + 数据 Lead） | 监管人 | **否**（指针已切；可补签） |
| OPEN-CHAIN-ADS-V2-06 | Demo `demo_gkxlumenx_ads` DDL + seeds | data | 否 |
| OPEN-CHAIN-STORE-02 | ES 正式 mapping 文档补链 | data | 否 |
| OPEN-CHAIN-STORE-03 | Nebula Tag/Edge 与 v5 `*_rel` 命名对齐 | data / architect | 否 |
| OPEN-CHAIN-STORE-04 | Demo `demo_gkxlumenx_dwd/_ads` 按需补表 | data | 否 |
| OPEN-CHAIN-STORE-05 | 各细表结构评审 → approved | 数据 Lead | 否（另开） |
| （承接）OPEN-CHAIN-DIFF-03 | 资讯 IC*↔INB* | 见 S2 | 否 |

> ~~OPEN-CHAIN-ADS-01（v1 会签）~~：真源已迁 v2，关闭。  
> ~~OPEN-CHAIN-STORE-01~~：旧十一表对齐废止，关闭。

## 下游

- **放行 S4**：`DATA-CHAIN-STORAGE-S4-L01`（旧 `data-design/产业链/*` stub）— 监管确认本 handoff 后升 ready / 开工。  
- 并行：Demo ADS DDL、Java 同步读路径按 v2 映射。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ |
| 调用链 / Java 只读 ADS | ✅ ads.md |
| Nebula only | ✅ |
| MySQL only（RDB） | ✅ |
| 三方 ODS≠项目 DWD | ✅ |
| 细表 draft | ✅ |
| ADS 先行（契约面有文档） | ✅ v2 |

## CI/CD

- 分支：`gkx-orchestration` `dev`  
- commit：（监管人确认后提交）  
- pipeline / K8s：N/A（纯文档）

## Cost（估 · 含收口）

| 字段 | 值 |
|---|---|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~6–8 万（含 ADS v2 指针收口） |
| actual_cost | 估 <$4 |
| cost_warn | false |

## 监管确认栏（李伟）

**已确认**（2026-08-13 会话原文：「S3 确认，放行 S4」）：

- [x] `ads.md` 现行真源 = ADS **v2**（10 表）；v1 仅对照  
- [x] `dwd-chain.md` 现行真源 = DWD **v5**  
- [x] stores 细表保持 draft；**已放行 S4 stub**  

> Registry：`ready_to_sign`（待 `human:淮政玮` 签收 → done）。S4 已按监管放行开工。  
