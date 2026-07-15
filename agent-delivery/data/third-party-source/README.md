# third-party-source

三方原始数据源隔离落盘根目录。各批次独立子目录，互不影响。

| 子目录 | 说明 |
|--------|------|
| [gkx-mysql-raw/](gkx-mysql-raw/) | **当前 ODS 贴源**：MySQL `gkx` @ `183.240.141.251:3318`（只读）；含 DDL 沙箱 + [CONNECTION.md](gkx-mysql-raw/CONNECTION.md) |

**运行时 ODS 真源** = 上总集采购输出库（见 `gkx-mysql-raw/CONNECTION.md`）。  
**不是**算法 demo 的 `innov` / `demo_gdf_data`。

详见各子目录 README.md。
