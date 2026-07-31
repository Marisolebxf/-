# third-party-source

三方 / 外部**数据源结构**隔离落盘根目录。与加工（GDF Mapping）、自建库设计（`data-design/`）分离。

| 子目录 / 文件 | 说明 |
|---------------|------|
| [doc/](doc/) | **三方承诺要素库汇总表（xlsx）**；企业方向承诺表以本目录为准；Markdown 全量提取见 [doc/md-extract/](doc/md-extract/) |
| [gkx-mysql-raw/](gkx-mysql-raw/) | **运行时入站库结构沙箱**：MySQL `gkx`；加工文档在 `gkx-mysql-raw/加工/` |
| [SUPPLIER-LOAD-PROGRESS.md](SUPPLIER-LOAD-PROGRESS.md) | **供应方落库进度快照**（按反馈日期追加；≠ 本侧 ODS 已镜像） |

**承诺表（文档侧）** = `doc/`（及 `doc/md-extract/`）。  
**运行时入站真源** = 上总集采购输出库（见 `gkx-mysql-raw/CONNECTION.md`）。  
**工作面（live）** = 供应方 **`dwd_*` 表**（见 `gkx-mysql-raw/SOURCE-TABLES.md`，用于核验落库）。  
**加工映射** → `../GDF/Mapping/`；**自建库设计** → `../data-design/`。

> 已清理（2026-07-22）：`ODS源数据表结构清单(v2).md`、`gkx_szc_ods_表结构及行数报告.md`（历史对照清单，不再维护）。
