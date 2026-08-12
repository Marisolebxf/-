# GDF 派单包（人类可读）

> GDF 数据中台团队**不使用 Cursor**。对外沟通用本目录工作包 + 飞书/例会，不用智能体派单话术。

| 工作包 | 范围 | 版本 |
|--------|------|------|
| [企业/GDF-ENT-WORKPACK-v2](企业/GDF-ENT-WORKPACK-v2/) | 企业维贴源（40 表）+ **MySQL DWD DDL（`10/`）** + **Mapping v4（`09`）** → `gkxlumenx_dwd` | **v2.0**（2026-08-13）· **现行** |
| [企业/GDF-ENT-WORKPACK-v1](企业/GDF-ENT-WORKPACK-v1/) | 同上历史包；DWD 指针误指旧 PG 稿 | v1.3 · **建表已作废** |

建表 / ALTER：**只认 v2 包内 `10-DWD-MySQL-DDL/`**。  
Mapping 施工真源：v2 工作包内 **`09` v4**；目录指针见 [`../Mapping/企业/`](../Mapping/企业/)。历史 v1 / Mapping v2/v3 **勿直接施工**。
