# MySQL 建表规约

> **状态**：2026-10-26 `POLICY-DDL-CONV-L00` 补齐第 1–7 条。第 8 条保留。  
> **适用**：本批政策 ADS/DWD 在册表。其它域已有表不在本管线批量改。企业、产业在政策核对通过后按同一条执行。  
> **签收自检**：`.cursor/skills/gkx-gdf-ddl-signoff`

## 1. 结构真源

一张表只有一份带注释的 MySQL `CREATE`。真源在 `agent-delivery/data/data-design/storage/{域}/stores/mysql/` 的 `dwd.md`、`ads.md` 或同目录 `dwd-*.md`。文档里的库名写 `demo_gkxlumenx_*`。产线库只把库名换成 `gkxlumenx_*`，列、类型、空值、默认值、索引、注释、排序规则相同。

`AUTO_INCREMENT` 当前值不是结构，不写进 CREATE。

## 2. 字符集

表和全部字符列都是 `utf8mb4` / `utf8mb4_0900_ai_ci`。不留 `utf8mb4_unicode_ci`，不留 `utf8mb4_general_ci`。

## 3. 列从哪来

ADS 在册表的列、类型、空值、默认值、索引以现网 `demo_gkxlumenx_ads` 为准。不采用 PostgreSQL `schema_policy_ads.sql`，不把旧稿 v1 的 `smallint` / `decimal(6,2)` / 二级索引写回去。

`policy_base_info` 不走现网 37 列。目标列是派单包 `10` 的 CREATE，由 `POLICY-DDL-BASE-SPEC-L06` 写入 `dwd.md`。`ext1` 不是 `policy_type`，`level` 不是 `rank`，`region` 拼串不是省市区。

注释写在 CREATE 里。对得上的用现有中文用途。对不上的写「现网 demo 有此列，口径待补」，并在 handoff 列出。

## 4. 不再当作结构依据

- `schema_policy_ads.sql`（PostgreSQL）
- 政策旧稿 v1 §3 的类型
- `repos/lumen-algo-py/vendor/entan-py/scripts/mysql/schema_mysql.sql`

这三份禁止再执行，禁止当政策 ADS/DWD 的建表依据。

## 5. 本批不改的范围

企业域已有表上的 `utf8mb4_general_ci`（含 `org_id`）不在本管线批量改。不 DROP 有数据的表。不写 `gkxlumenx_ods` 和供应库 `gkx`。

## 8. GDF 派单包建表语句

GDF派单中有明确的建表语句和相关注释，派单包任务执行时，需要从dwd.md/ads.md copy相关的sql语句。

派单包签收时自动触发 skill `gkx-gdf-ddl-signoff`（按该任务的维度：政策 / 企业 / 产业 / 服务机构）。通过条件：

1. 当前最新版本的派单包中的 sql 建表语句包含了 dwd/ads 相关的建表语句，且建表语句和线上的 demo 数据库保持一致，也和 dwd.md 和 ads.md 中的建表语句一致
2. 线上的 lumen 库中已经创建了相关的表，并且和 1 中的建表语句一致

库名按所在库替换（`demo_gkxlumenx_*` 与 `gkxlumenx_*`），不把库名不同算作不一致。列、类型、空值、默认值、注释、索引、排序规则必须相同。
