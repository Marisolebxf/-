# 加工侧文档（非源表真源）

> 本目录存放**加工 / 映射 / 全量盘点 / 工具**相关文件。  
> **已确认入站源表结构**请看上一级：[`../SOURCE-TABLES.md`](../SOURCE-TABLES.md)、[`../gkx_schema_ddl.sql`](../gkx_schema_ddl.sql)。

| 文件 | 说明 |
|------|------|
| [SUPPLIER-WORK-CONSTRAINTS.md](SUPPLIER-WORK-CONSTRAINTS.md) | 供应方工作约束（入站只消费 `dwd_*`、技术字段、缺表核验等）— **做 Mapping 前必读** |
| [ANALYSIS.md](ANALYSIS.md) | 相对旧「要素库」DDL 差异 + 对映射任务含义 |
| [table_inventory.md](table_inventory.md) | 全量结构盘点（含 `ods_*` / bak，对照用） |
| [table_list.txt](table_list.txt) | 全量表名列表（含非工作面） |
| `_extract_ddl.py` | 从 transcript 再提取 DDL 的辅助脚本 |

## 加工产物应落在哪里

| 内容 | 路径 |
|------|------|
| 各垂向 ODS→DWD 字段映射报告 | `agent-delivery/data/GDF/Mapping/{企业,产业链,政策,服务机构}/` |
| 各垂向自建库设计 | `agent-delivery/data/data-design/{垂向}/` |

勿把 Mapping 结论回写进上一级「源表」目录冒充数据源说明。
