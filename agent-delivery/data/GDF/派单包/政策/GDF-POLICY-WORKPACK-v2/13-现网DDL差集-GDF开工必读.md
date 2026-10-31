# 13 — 现网 DDL 差集（GDF 开工必读）

> **工作包**：GDF-POLICY-WORKPACK-v2.0  
> **核验**：本叶 **未连库**。下面是开工前要跑的核对，不是 2026-10-26 的 as-built 快照。空表是否已建，看 `SYSINT-06-03-DDL-L01`，不在本叶宣称已完成。  
> **GDF 作业库**：只认 `gkxlumenx_ods`（贴源）+ `gkxlumenx_dwd`（洗主表）。业务 MySQL `10.50.11.76:3306`（见 `03`）。旧外网 `111.198.38.90:34306` 停用。  
> **demo**：`demo_gkxlumenx_*` 本侧对照。GDF **不连、不改、不验收**。  
> **对照真源**：本包 `10-DWD-MySQL-DDL/` + `sources/ods-ddl.md`。  
> **铁律**：缺列只 `ADD`；现网多出来的列 **禁止 DROP**；**已有列禁止改类型**。禁止新建 `gkxlumenx_dws`。禁止按旧稿 37 列重建主表。

## 1. 开工前对正式库跑 `information_schema`

已存在则跳过，禁止重复 ADD，禁止为了对齐去连 demo。

| 对象 | 库 | 没有时 |
|------|----|--------|
| `dwd_policy_base` | `gkxlumenx_ods` | 按源 `SHOW CREATE TABLE` 建空表，库名改为 `gkxlumenx_ods`。缺表停工交我方，不在 demo 建 |
| `dwd_global_policy_base` | `gkxlumenx_ods` | 同上 |
| `policy_base_info` | `gkxlumenx_dwd` | 按 `10/policy_base_info-MySQL.md` 建空表 |
| `policy_base_info.is_history` | `gkxlumenx_dwd` | 表已在、列不在：只 `ADD` `is_history int NULL`。列已在则跳过，不改类型 |
| `policy_industry_rel` | `gkxlumenx_dwd` | 按 `10/policy_industry_rel-MySQL.md` 建空表。Wave B **不要洗**这张表 |
| `policy_industry_rel` | `gkxlumenx_ads` | 同结构空表。由本侧建。GDF 不在 ADS 上配 Mapping |
| `script_state` | `gkxlumenx_dwd` | 执行 `sql/update_round1.sql`（含建表、清重、索引）。缺表时 C1/C2 退出码 4。不要在作业里建表，不要 `DROP` |

ADS `policy_text_parse`：C2 合并条款用。没有冻结的产线 DDL 时，本包不猜列、不新建。缺表记缺口，不在 GDF 里造一张。

## 2. 源表

| 承诺名 | 优先级 | GDF 处置 |
|--------|--------|----------|
| `gkx.dwd_policy_base` | P0 | 贴源。无表则阻塞 |
| `gkx.dwd_global_policy_base` | P0 | 贴源。无表则阻塞 |
| `dwd_zck_*` | — | 不贴 |
| 供应方 `ods_*` | — | 不读 |

## 3. 开工顺序

1. 按 §1 核 ODS 两表和 DWD 主表。缺列只 ADD。  
2. Wave A：`gkx` → `gkxlumenx_ods` 同名镜像，勾 `05`。行数不要滤掉删除行和历史行。  
3. Wave B：按 `09` 洗入 **`gkxlumenx_dwd.policy_base_info`**。UK `(source_plane, policy_id)`。  
4. **该表当日 Wave B `success` 之后**，按 `15` 触发 C1 / C2。禁止只贴源就触发。禁止 GDF 直写 ADS、ES、Nebula。  
5. 关联表键只有 `policy_id`。两平面 `policy_id` 若撞车，C1 先停，本包不改表来绕。

## 4. 本包不包含

- CDC 预填 Excel（另派；`parse_workpack.py` 仍读不出政策字段行）  
- Java 对外触发与 callback（见 `15` §6）  
- `OPEN-POLICY-FLOW-01` 正式 DAG 名  
- 连库后的真实差集回填（开工时把 `SHOW CREATE` 差异附回执，不要把本节当成已经核对过的现网）
