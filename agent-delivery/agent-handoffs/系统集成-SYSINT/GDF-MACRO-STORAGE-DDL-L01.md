# GDF-MACRO-STORAGE-DDL-L01 · 宏观行业：storage/MACRO dwd.md+ads.md 入仓（OPEN-MACRO-05）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:architect-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 名词与流程见 [`task-claiming-guide.md`](../../task-claiming-guide.md) |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·文档类，无业务代码） |
| 说明 | 用脚本逐字提取派单包 SQL 生成 md，没有手抄列。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶文件小，无需压缩。 |

## 图即契约

N/A（未动架构图 / 存储流图）。

## 问题清单

- 2026-11-09 DDL 签收自检红：`GDF-MACRO-WORKPACK-v1` 有 CREATE TABLE，`storage/MACRO` 无 md（见 `工程过程/04-系统集成/06-GDF数据治理集成/自检报告-MACRO-FIN-DDL-20261109.md`）。

## 修改内容

新建 `agent-delivery/data/data-design/storage/MACRO/stores/mysql/`：

| 文件 | 内容 |
|---|---|
| `dwd.md` | 六张 DWD：`macro_index_data` / `macro_admin_area` / `macro_index_attribute` / `macro_index_cal` / `macro_index_dur` / `macro_source_code` |
| `ads.md` | 一张 ADS：`macro_city_section` |
| `README.md` | 目录索引与同步规则 |

- CREATE 来源：DWD 六张 ← 派单包 `10-DWD-MySQL-DDL/macro-dwd.md`；ADS ← 派单包 `12-...附录.md` §2。由脚本按 ```sql 块提取，列、索引、注释、排序规则不改。
- 唯一差异：库名。按 `mysql-ddl-convention.md` §1 md 写 `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads`；派单包仍是 `gkxlumenx_*`（自检脚本比较列/索引/注释/字符集/排序规则，不比库名）。
- 未改派单包任何业务口径。12 §3 灌数 SQL、§4 血缘占位不复制进 `ads.md`。

## 测试结果

命令：`python .cursor/skills/gkx-gdf-ddl-signoff/scripts/check_gdf_ddl.py --task GDF-MACRO-WORKPACK-L01`

退出码：**1**（不通过）。原文：

```
文件一致 macro_admin_area
文件一致 macro_city_section
文件一致 macro_index_attribute
文件一致 macro_index_cal
文件一致 macro_index_data
文件一致 macro_index_dur
文件一致 macro_source_code
派单包 agent-delivery\data\GDF\派单包\宏观行业\GDF-MACRO-WORKPACK-v1
结构真源 agent-delivery\data\data-design\storage\MACRO\stores\mysql
不通过
- 未设置 GKX_LUMEN_MYSQL_PASSWORD，库未核对
```

- 文件一致：7/7 绿（修复前 7 张均报「md 没有」）。
- 库一致：**未核**。本机未设 `GKX_LUMEN_MYSQL_PASSWORD`，不造假通过。唯一失败项即此。

## 遗留风险

- demo / lumen 库是否已建这 7 张表、列是否一致，未核（`OPEN-MACRO-06`）。需有口令的人设环境变量后重跑同一命令。
- 派单包 `10/README.md` 写「Demo 库不是本包目标」，而 `mysql-ddl-convention.md` §8 要求 demo 与 lumen 两库都与 md 一致。库核对时 demo 库未建表会红，需人裁定：补建 demo 表，或签收口径对 MACRO 豁免 demo。本叶不拍板。
- `macro_city_section` 未灌数，D4 不得宣称 live（沿用派单包 12 §4）。

## CI/CD

- 分支：`origin/dev`（编排仓）
- commit：见 git log（`[agent:architect-agent]`）
- pipeline / K8s：不适用（编排仓无业务 CI；`cicd: skip` 类设计产物）

## 涉及文件

- `agent-delivery/data/data-design/storage/MACRO/stores/mysql/dwd.md`
- `agent-delivery/data/data-design/storage/MACRO/stores/mysql/ads.md`
- `agent-delivery/data/data-design/storage/MACRO/stores/mysql/README.md`
- `agent-delivery/agent-handoffs/系统集成-SYSINT/GDF-MACRO-STORAGE-DDL-L01.md`
- `agent-delivery/data/GDF/派单包/宏观行业/GDF-MACRO-WORKPACK-v1/10-DWD-MySQL-DDL/README.md`（仅进度行）
