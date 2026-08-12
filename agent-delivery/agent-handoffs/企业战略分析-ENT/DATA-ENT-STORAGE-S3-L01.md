# DATA-ENT-STORAGE-S3-L01 · 企业维存储 S3 stores as-built 灌入

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 流图+S2 已 done；S3 文档灌入 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `lite` |
| 说明 | 定义/文档类；指针+表清单，未跳过架构铁律 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载；纯文档灌入 |

## 范围与实现

- 对照：`storage/README.md` S3；流图 §6 S3 放行。  
- 产物：`storage/ENT/stores/mysql/*`、`elasticsearch/*`、`nebula/graph-enterprise.md`。  
- 真源：工商 v3.1、指标汇总 v3.1、模块 v3.0、ES 索引设计、Nebula space schema、算法 ADS 表清单。  
- **未**将细表标 `approved`；**未**改三方 ODS 口径（仍 doc + md-extract）。

## 偏离说明

- ADS 部分表清单来自算法仓/历史 schema（含 PG 方言遗留）；**现网 MySQL 列名核验**留 OPEN-ENT-STORE-01。  
- DIM 行政区划码表路径待核验：OPEN-ENT-STORE-02。  
- ES/Nebula 以指针+摘要为主，全 mapping/ngql 不内嵌（防双源）。

## 产物清单

| 路径 | 说明 |
|---|---|
| `stores/mysql/dwd-entity.md` 等 5 文件 | DWD/ADS/DIM |
| `stores/elasticsearch/*` | 索引+同步 |
| `stores/nebula/graph-enterprise.md` | 子图 |
| `…/DATA-ENT-STORAGE-S3-L01-派单说明.md` | 本派单 |

## 开放项

| ID | 内容 | Owner |
|---|---|---|
| OPEN-ENT-STORE-01 | ADS 表现网 MySQL 列名 vs schema_ent_score 对齐核验 | 数据/算法 |
| OPEN-ENT-STORE-02 | DIM 行政区划表现网路径核验 | 数据 |
| OPEN-ENT-STORE-03 | 各 stores 细表结构评审 → approved | 数据 Lead + 会签人 |
| （承接）OPEN-ENT-FLOW-01/04/06 | DAG 名、ES/Nebula SLA、LLM→ODS 脚本 | 见 S2 handoff |

## 下游

- **S4**：旧 `data-design/企业/*` stub 可排（stores 已有实质内容）。  
- Demo 工程：按 stores 结构建 `demo_*`；LLM→ODS 仍开。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本单无 Java 算法 |
| 调用链 / Java 只读 ADS | ✅ ads.md 写明 |
| Nebula only | ✅ |
| 可观测 | N/A 文档 |
| MySQL only（RDB） | ✅ |
| D9 指标不替代 | ✅ 指向 metrics |
| 三方 ODS≠live | ✅ 未灌 gkx-mysql-raw |

## CI/CD

- 分支：`dev`（编排仓文档）  
- commit：待 push  
- pipeline / K8s：N/A（纯文档）

## Cost（四字段）

| 字段 | 值 |
|------|-----|
| actual_tokens | ~80k（估） |
| model_used | Cursor Grok 4.5 |
| actual_cost | <$2（估） |
| cost_warn | false |

## 联调 / 会签确认

S3 文档灌入完成；细表仍 draft，**结构评审另单**。联调确认：文档闭环可支撑 S4 与 Demo 对表。
