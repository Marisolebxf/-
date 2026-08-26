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
| `_probe_live_dwd_enterprise.py` | **仅企业 Wave A 40 表** live 行数探测 |
| `LIVE-DWD-ENTERPRISE-READINESS-*.md` | 企业维齐套日更（承诺 40 表） |

## 数据源表分析（全要素库，推荐）

对照 **20 个要素库 Excel** 与 live MySQL `gkx` 的行数 + 字段差异。覆盖机构 / 人才 / 政策 / 金融 / 宏观 / 产业链 / 专题 / 论文专利项目报告，**不是**只探企业维。

Agent 复跑流程：`.cursor/skills/gkx-yuansuku-live-snapshot/SKILL.md`（Codex 短指针：`.codex/skills/gkx-yuansuku-live-snapshot/`）。用户说「执行一次快照」即走该 Skill。

| 文件 | 说明 |
|------|------|
| [GKX数据源表差异分析摘要-20260826.md](GKX数据源表差异分析摘要-20260826.md) | **先读**：分要素库就绪度与缺口（跟最新快照） |
| [GKX数据源表及行数报告-20260826-1429.MD](GKX数据源表及行数报告-20260826-1429.MD) | **最新**全量报告（2026-08-26 14:29） |
| [GKX数据源表及行数报告-20260824-1542.MD](GKX数据源表及行数报告-20260824-1542.MD) | 08-24 15:42 快照（仓内环比基准） |
| [GKX数据源表及行数报告-20260821-1441.MD](GKX数据源表及行数报告-20260821-1441.MD) | 08-21 14:41 快照 |
| [GKX数据源表及行数报告-20260820-1827.MD](GKX数据源表及行数报告-20260820-1827.MD) | 08-20 18:27 快照 |
| [GKX数据源表及行数报告-20260820-1130.MD](GKX数据源表及行数报告-20260820-1130.MD) | 08-20 11:30 快照 |
| `要素库xlsx/` | 四份「数据汇总表」Excel（脚本输入） |
| `gen_gkx_report.py` | 只从 Excel 抽表/字段，不连库 |
| `update_row_counts.py` | Excel + 连库回填行数 |
| `gen_schema_diff_report.py` | **推荐日常执行**：行数 + Excel↔库字段差异 |
| `_yuansuku_paths.py` | Excel / `.env.local` / 报告输出路径 |

```powershell
cd agent-delivery/data/third-party-source/gkx-mysql-raw/加工
python gen_schema_diff_report.py
```

依赖 `pymysql`；密码只读 [`../.env.local`](../.env.local)。默认读本目录 `要素库xlsx/`，报告写回本目录。可用环境变量 `GKX_YUANSUKU_XLSX_DIR` 指向其它 Excel 目录。

## 加工产物应落在哪里

| 内容 | 路径 |
|------|------|
| 各垂向 ODS→DWD 字段映射 | `agent-delivery/data/GDF/派单包/{域}/GDF-*-WORKPACK-vN/` 内 `09-*Mapping*` |
| 各垂向自建库设计 | `agent-delivery/data/data-design/{垂向}/` |

勿把 Mapping 结论回写进上一级「源表」目录冒充数据源说明。
