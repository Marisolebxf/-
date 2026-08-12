# GDF-ENT-WORKPACK-v2 投递说明

> **日期**：2026-08-13  
> **作者**：agent:data-agent（编排仓）  
> **对象**：GDF 产线（飞书投递）+ 本侧 `human:辜少彬` / PM  
> **工作包**：`agent-delivery/data/GDF/派单包/企业/GDF-ENT-WORKPACK-v2/` · **v2.0**  
> **ponytail:** off（文档投递，无业务代码）

## 1. 为什么发 v2

GDF 若仍按 WORKPACK-v1 指向的旧「企业模块」稿，或 `_公共/三方参考-DWD标准表结构清单.md`（PG `demo_gdf_data`、宽表 `enterprise`）建/改 DWD，会与现网 MySQL as-built 冲突。v2 **纠正建表真源**，并作废 v1 的建表用途。

## 2. Zip / 云盘清单（对外）

打包目录整包（建议 zip 名：`GDF-ENT-WORKPACK-v2.0-20260813.zip`）：

- `README.md` / `00`～`09` / `11` / `CHANGELOG.md`
- **`10-DWD-MySQL-DDL/`**（含 README + 三份 MySQL 设计稿冻结快照）

**不要**再单独发 v1 zip 当现行包；若历史链接仍在，在消息里声明作废。

## 3. 飞书话术（可直接粘贴）

```text
【企业维 GDF 工作包更新】GDF-ENT-WORKPACK-v2.0（2026-08-13）

请停用 WORKPACK-v1，以及任何「三方参考 DWD 标准表结构清单」/ PostgreSQL demo_gdf_data / 宽表 enterprise 的建表材料。

现行包：GDF-ENT-WORKPACK-v2
- 建表/ALTER 只认包内 10-DWD-MySQL-DDL/（MySQL · gkxlumenx_dwd）
- 企业主数据表是 enterprise_base（org_id），不是宽表 enterprise
- Mapping 只认 09 v4
- Wave A 贴源 40 表清单与 v1.3 相同，不重开范围

请回签：
1）已收到 v2.0，已停用旧 DDL；
2）将输出现网 gkxlumenx_dwd 相对 10/ 的差集（建/改/废）与迁移说明。
```

## 4. 本侧已同步（防再误导）

| 路径 | 动作 |
|------|------|
| `GDF/派单包/README.md` | 现行包改为 v2 |
| `GDF-ENT-WORKPACK-v1/README` + `00` | 顶部作废横幅 |
| `storage/ENT/etl/pipeline-ods-to-dwd.md` | 指针 → v2 / Mapping v4 |
| `_公共/三方参考-DWD标准表结构清单.md` | 顶部禁止施工横幅 |
| `GDF/Mapping/企业/…(v3).md` | 改为指向 v4 |

## 5. 回签检查项（GDF）

- [ ] 确认目标库 = MySQL `gkxlumenx_dwd`（非 PG / 非 demo_gdf_data）  
- [ ] 确认未再建宽表 `enterprise`  
- [ ] 差集清单已回传本侧  
- [ ] Mapping 作业可追溯到 `09` v4  

## 6. 不做

- 本仓不代执行正式库 DDL  
- 不要求 GDF 写 `demo_gkxlumenx_*`  
- 本次未新建 task-registry 条目（跟踪用本 handoff）
