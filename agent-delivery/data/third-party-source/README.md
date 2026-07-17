# third-party-source

三方原始数据源隔离落盘根目录。各批次独立子目录，互不影响。

| 子目录 | 说明 |
|--------|------|
| [gkx-mysql-raw/](gkx-mysql-raw/) | **当前入站贴源**：MySQL `gkx` @ `183.240.141.251:3318`（只读，可互联网直连）；含 DDL 沙箱 + [CONNECTION.md](gkx-mysql-raw/CONNECTION.md) + [SUPPLIER-WORK-CONSTRAINTS.md](gkx-mysql-raw/SUPPLIER-WORK-CONSTRAINTS.md) |

**运行时入站真源** = 上总集采购输出库（见 `gkx-mysql-raw/CONNECTION.md`）。  
**工作面** = 供应方 **`dwd_*` 表**（`ods_*` 不对项目正式暴露，见工作约束）。  
**不是**算法 demo 的 `innov` / `demo_gdf_data`。

详见各子目录 README.md。
