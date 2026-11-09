# GDF-FIN-STORAGE-DDL-L01 · 金融数据：storage/FIN dwd.md+ads.md 入仓（OPEN-FIN-01）

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
| ponytail | `N/A`（定义·文档类；仅微调一处生成脚本） |
| 说明 | 脚本逐字提取派单包 SQL 生成 md，没有手抄列。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 文件小。 |

## 图即契约

N/A（未动架构图 / 存储流图）。

## 问题清单

- 2026-11-09 DDL 签收自检红：`GDF-FIN-WORKPACK-v1` 有 CREATE TABLE，`storage/FIN` 无 md（见 `工程过程/04-系统集成/06-GDF数据治理集成/自检报告-MACRO-FIN-DDL-20261109.md`）。
- 自检脚本每个 ```sql 围栏只解析第一条 CREATE。原草稿把 11 张 DWD 放在同一围栏，只会比到第 1 张（首次跑只有 2 张「文件一致」）。因此新 md 与派单包两份 draft 都改成**每表一个围栏**，否则 15 张里 13 张不会被真正比对。

## 修改内容

新建 `agent-delivery/data/data-design/storage/FIN/stores/mysql/`：

| 文件 | 内容 |
|---|---|
| `dwd.md` | 11 张 DWD：`fin_corp_basic` / `fin_security` / `fin_industrial_fund` / `fin_industrial_fund_gp` / `fin_industrial_fund_lp` / `fin_industrial_fund_strategy` / `fin_industrial_fund_inv_summary` / `fin_bond` / `fin_industry_class_his` / `fin_main_biz_composition` / `fin_valuation_daily` |
| `ads.md` | 4 张 ADS：`ads_fin_industrial_fund_summary` / `ads_fin_bond_issue_summary` / `ads_fin_listed_company_snapshot` / `ads_fin_main_biz_latest` |

- 来源：派单包 `10-DWD-MySQL-DDL/fin-dwd-draft.md`、`fin-ads-draft.md`，列、类型、索引、注释、排序规则一字未改。
- 唯一差异：库名。md 按 `mysql-ddl-convention.md` §1 写 `demo_gkxlumenx_*`；派单包仍是 `gkxlumenx_*`（GDF 只写正式库）。自检不比库名。
- 同时改动：
  - 派单包 `10/fin-dwd-draft.md`、`fin-ads-draft.md`：改为每表一围栏；ads 草稿头注改为「同步副本」。
  - `10/README.md`：状态改为「真源已入仓」。
  - `script/gen_fin_pack.py` `gen_ddl()`：与上同步（每表一围栏、头注指向 storage），避免下次重生成回退。
- 未改任何业务口径，未碰 `12-ADS后加工-金融.md`。

## 测试结果

命令：`python .cursor/skills/gkx-gdf-ddl-signoff/scripts/check_gdf_ddl.py --task GDF-FIN-WORKPACK-L01`

退出码：**1**（不通过）。原文：

```
文件一致 ads_fin_bond_issue_summary
文件一致 ads_fin_industrial_fund_summary
文件一致 ads_fin_listed_company_snapshot
文件一致 ads_fin_main_biz_latest
文件一致 fin_bond
文件一致 fin_corp_basic
文件一致 fin_industrial_fund
文件一致 fin_industrial_fund_gp
文件一致 fin_industrial_fund_inv_summary
文件一致 fin_industrial_fund_lp
文件一致 fin_industrial_fund_strategy
文件一致 fin_industry_class_his
文件一致 fin_main_biz_composition
文件一致 fin_security
文件一致 fin_valuation_daily
派单包 agent-delivery\data\GDF\派单包\金融数据\GDF-FIN-WORKPACK-v1
结构真源 agent-delivery\data\data-design\storage\FIN\stores\mysql
不通过
- 未设置 GKX_LUMEN_MYSQL_PASSWORD，库未核对
```

- 文件一致：**15/15 绿**（修复前 15 张均报「md 没有」）。
- 库一致：**未核**。本机未设 `GKX_LUMEN_MYSQL_PASSWORD`；且 `10/README.md` 记载 demo / lumen 库均未建这 15 张表。唯一失败项即此，不造假通过。

## 遗留风险

- 库核对仍红：需 GDF 在 `gkxlumenx_dwd`/`gkxlumenx_ads` 建表；`mysql-ddl-convention.md` §8 还要求 demo 库一致，而派单包「禁止在 demo 库建这些表」，二者冲突需人裁定（补建 demo，或对 FIN 豁免 demo）。本叶不拍板。
- 4 张 ADS 未灌数，D4 不得宣称 live。
- 依赖 OPEN-FIN-03（金额单位）、OPEN-FIN-04（报告期格式）等口径未闭合，列注释原样保留。

## CI/CD

- 分支：`origin/dev`（编排仓）
- commit：见 git log（`[agent:architect-agent]`）
- pipeline / K8s：不适用（编排仓无业务 CI；`cicd: skip` 类设计产物）

## 涉及文件

- `agent-delivery/data/data-design/storage/FIN/stores/mysql/dwd.md`
- `agent-delivery/data/data-design/storage/FIN/stores/mysql/ads.md`
- `agent-delivery/data/GDF/派单包/金融数据/GDF-FIN-WORKPACK-v1/10-DWD-MySQL-DDL/fin-dwd-draft.md`
- `agent-delivery/data/GDF/派单包/金融数据/GDF-FIN-WORKPACK-v1/10-DWD-MySQL-DDL/fin-ads-draft.md`
- `agent-delivery/data/GDF/派单包/金融数据/GDF-FIN-WORKPACK-v1/10-DWD-MySQL-DDL/README.md`
- `agent-delivery/data/GDF/派单包/金融数据/GDF-FIN-WORKPACK-v1/script/gen_fin_pack.py`
- `agent-delivery/agent-handoffs/系统集成-SYSINT/GDF-FIN-STORAGE-DDL-L01.md`
