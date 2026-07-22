# third-party-source

三方 / 外部**数据源结构**隔离落盘根目录。与加工（GDF Mapping）、自建库设计（`data-design/`）分离。

| 子目录 / 文件 | 说明 |
|---------------|------|
| [gkx-mysql-raw/](gkx-mysql-raw/) | **当前入站贴源**：MySQL `gkx`；根目录只描述已确认源表；加工文档在 `gkx-mysql-raw/加工/` |

**运行时入站真源** = 上总集采购输出库（见 `gkx-mysql-raw/CONNECTION.md`）。  
**工作面** = 供应方 **`dwd_*` 表**（见 `gkx-mysql-raw/SOURCE-TABLES.md`）。  
**加工映射** → `../GDF/Mapping/`；**自建库设计** → `../data-design/`。

> 已清理（2026-07-22）：`ODS源数据表结构清单(v2).md`、`gkx_szc_ods_表结构及行数报告.md`（历史对照清单，不再维护）。
