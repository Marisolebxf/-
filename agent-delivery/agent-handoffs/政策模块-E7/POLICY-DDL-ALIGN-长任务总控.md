# 政策 ADS/DWD 建表真源对齐 · 长任务总控

> **日期**：2026-10-26
> **授权**：未授权。待 `human:淮政玮` 在聊天写明「后续认领不必再问」后，本文件才成为一次授权。现在禁止升 ready、禁止认领、禁止改库。
> **监管人（授权后）**：`human:淮政玮`
> **升级人**：DROP、写 ODS / 供应库 `gkx` → `human:李伟`。`policy_base_info` 改列集由 `human:淮政玮` 直接改。
> **锁**：`lock_hours=24`
> **目标**：`ads.md` 与 `dwd.md` 里每张在册表有一份带注释的 MySQL `CREATE`；`demo_gkxlumenx_`* 与 `gkxlumenx_`* 同表同结构，只换库名；字符集 `utf8mb4`、排序规则 `utf8mb4_0900_ai_ci` 写成规约并在本批表上落地。线上 demo 相关表（含 `policy_base_info`）的排序规则也是这一套，不留 `general_ci` / `unicode_ci`。
> **模式**：长任务。规约：`[长任务执行规约.md](../../长任务执行规约.md)`。不套前端 A–E，无段 E 金路径。同仓同时只派一张 coding 单。
> **厚包**：本文件。薄条 = 各叶 registry DoD。`/goal` 必抄本路径。强度：文档叶不压完整性；改库叶 `ponytail full`。


| 作业        | 仓                                                              | 分支           | 任务                          | 状态门                                                                |
| --------- | -------------------------------------------------------------- | ------------ | --------------------------- | ------------------------------------------------------------------ |
| 规约        | `gkx-orchestration`                                            | `origin/dev` | `POLICY-DDL-CONV-L00`       | 授权句之后才 ready                                                       |
| 文档 CREATE | 同上                                                             | 同上           | `POLICY-DDL-DOC-L01`        | CONV 联调闸门                                                          |
| 影响扫描      | 同上                                                             | 同上           | `POLICY-DDL-IMPACT-L02`     | 授权后可与 DOC 并行（只读代码和库）                                               |
| 排序规则代码    | `demo-algo-ent-analysis` 为主；同步 `lumen-algo-py` vendor 与 CMS 连接 | `origin/dev` | `POLICY-DDL-CODE-L05`       | 授权后可与 DOC 并行。只改排序规则字面量。BASE-ALIGN 改 `policy_base_info` 前，本叶须到联调闸门  |
| 主表列集规格    | `gkx-orchestration`                                            | `origin/dev` | `POLICY-DDL-BASE-SPEC-L06`  | DOC 联调闸门。只写交叉表和 `dwd.md`，不改库                                       |
| 主表读列代码    | `demo-algo-ent-analysis` 为主；同步 `lumen-algo-py` vendor 与 CMS    | `origin/dev` | `POLICY-DDL-BASE-CODE-L07`  | SPEC 与 CODE-L05 都到联调闸门。同仓串在 L05 之后。只改代码                            |
| 两库对齐      | 同上（改的是 MySQL，不改算法仓）                                            | 同上           | `POLICY-DDL-ALIGN-L03`      | DOC、IMPACT、CODE 都到联调闸门，且 IMPACT 写明拟 ALTER 清单。不碰 `policy_base_info` |
| 主表一次改库    | 同上（改的是 MySQL）                                                  | 同上           | `POLICY-DDL-BASE-ALIGN-L08` | SPEC、CODE-L07、ALIGN 都到联调闸门。改列集 / 改类型 / 改主键（不需要升级到李伟，淮政玮直接修改）       |
| 核对        | 同上                                                             | 同上           | `POLICY-DDL-CHECK-L04`      | ALIGN 与 BASE-ALIGN 都到联调闸门                                          |
| 派单包复制建表   | 同上                                                             | 同上           | `POLICY-DDL-GDF-SYNC-L09`   | CHECK 联调闸门。把 `dwd.md` / `ads.md` 的 CREATE 复制进现行派单包，再跑签收自检           |


废作、不建单、不派：把产线 `policy_base_info` 改回 demo 旧 37 列；在 BASE-SPEC 交叉表未到联调闸门时 ALTER demo 这张表；把 `ext1` 改名为 `policy_type`、把 `level` 改名为 `rank`、把 `region` 拼串拆成省市区；用 PostgreSQL `schema_policy_ads.sql` 或旧稿 v1 §3 的类型当结构；用 `schema_mysql.sql` 再执行一遍；DROP 有数据的表；写 `gkxlumenx_ods` / 供应库 `gkx`。

---



## 1. 目标（已拍板，授权后禁止回问）

1. **在册范围**：只处理这两份文档里已经点名的表。
  - `[ads.md](../../data/data-design/storage/POLICY/stores/mysql/ads.md)`：指标 9 张、图镜像 2 张、`policy_entity`、文本 3 张。`policy_industry_rel` 不在这里再写一份 CREATE。
  - `[dwd.md](../../data/data-design/storage/POLICY/stores/mysql/dwd.md)`：`policy_industry_rel` 已有 CREATE，DOC 只补齐注释与列级排序规则，不另起列集。`policy_text_parse` 也要在 `dwd.md` 有说明和建表语句。`policy_base_info` 的结构真源改为派单包 `10` [的 CREATE](../../data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/10-DWD-MySQL-DDL/policy_base_info-MySQL.md)，由 `POLICY-DDL-BASE-SPEC-L06` 写入这一节。
2. **ADS 这批表的结构以现网 demo 的列、类型、空值、默认值、索引为准**（2026-10-26 对 `10.50.11.76` 的 `demo_gkxlumenx_ads`）。不采用 PostgreSQL 脚本，也不把旧稿 v1 的 `smallint` / `decimal(6,2)` / 二级索引写回去。`policy_base_info` 不走这条，走第 7 条。
3. **排序规则单独拍板，覆盖 demo 现状**：表和全部字符列都是 `utf8mb4` / `utf8mb4_0900_ai_ci`。demo 上的 `utf8mb4_unicode_ci`、`policy_industry_rel.policy_id` 上的 `utf8mb4_general_ci` 都要改到这一套。
4. **两库一致**：同一张表在 `demo_gkxlumenx_ads` 与 `gkxlumenx_ads`（关联表再加两个 DWD 库）列集、类型、空值、默认值、索引、注释、排序规则相同，只换库名。文档里的 CREATE 写 `demo_gkxlumenx_`*。
5. **注释写在 CREATE 里**。列注释取自现有中文用途（`ads.md` 用途列、旧稿里仍对得上的 COMMENT、`policy_industry_rel` 已有注释）。对不上的列不编口径，注释写「现网 demo 有此列，口径待补」，并在 handoff 列出。
6. **规约**：上述 2–4 与第 8 条写成 `agent-delivery/data/data-design/storage/mysql-ddl-convention.md`，并在 `architecture-baseline.md` 加一条指针。从本批表执行。其它域已有表不在本管线批量改。第 8 条已经写入该文件，CONV 补齐时不要删。
7. `policy_base_info` **改为与产线同结构。** 目标列是派单包 `10` 的 CREATE。demo 现网 37 列不再作这张表的结构真源，也不写回产线（旧 37 列空壳 `policy_base_info_retired_20261026` 仍不动）。`ext1` 不是 `policy_type`，`level` 不是 `rank`，`region` 拼串不是省市区，禁止直接改名。交叉表、丢弃列和行回填写在 `POLICY-DDL-BASE-SPEC-L06`。读旧列的 demo 算法、`lumen-algo-py` vendor、CMS 由 `POLICY-DDL-BASE-CODE-L07` 改。改库只在 `POLICY-DDL-BASE-ALIGN-L08` 做一次：列集、类型、索引、注释和 `utf8mb4` / `utf8mb4_0900_ai_ci` 一起对齐。`POLICY-DDL-ALIGN-L03` 不碰这张表。改列集、改类型、改主键或唯一键、删列之前升级 `human:李伟`。写死 `utf8mb4_unicode_ci` 或 `utf8mb4_general_ci` 的比较仍归 `POLICY-DDL-CODE-L05`，且须在 BASE-ALIGN 之前到联调闸门。  
8. **GDF 派单包从 `dwd.md` / `ads.md` 复制建表语句。** GDF派单中有明确的建表语句和相关注释，派单包任务执行时，需要从dwd.md/ads.md copy相关的sql语句。签收时跑 skill `gkx-gdf-ddl-signoff`。通过条件：① 当前最新版本的派单包中的 sql 建表语句包含了 dwd/ads 相关的建表语句，且建表语句和线上的 demo 数据库保持一致，也和 dwd.md 和 ads.md 中的建表语句一致；② 线上的 lumen 库中已经创建了相关的表，并且和 1 中的建表语句一致。政策这一条在 `POLICY-DDL-GDF-SYNC-L09` 落地。已签收的 `GDF-POLICY-WORKPACK-V2-L01` 不改状态，按该 skill 复检，缺口由 L09 补。



## 2. 干法

```text
CONV-L00 规约落盘
    ├─闸门─► DOC-L01  ads.md 的 CREATE；dwd.md 只补 policy_industry_rel
    │         └─闸门─► BASE-SPEC-L06  policy_base_info 交叉表写入 dwd.md
    ├─并行─► IMPACT-L02  只读 ADS 这批表，拟 ALTER 清单（不含主表改列）
    └─并行─► CODE-L05  排序规则字面量
                │
DOC + IMPACT + CODE 都到联调闸门          SPEC + CODE 都到联调闸门
                │                                    │
                └─► ALIGN-L03                        └─► BASE-CODE-L07
                      不碰 policy_base_info                 改 demo / lumen Python / CMS 读列
                      │                                    │
                      └──────────────┬─────────────────────┘
                                     │
                                     └─► BASE-ALIGN-L08
                                           demo policy_base_info 一次对齐目标列 + 0900_ai_ci
                                           改列集由淮政玮直接改
                                           │
                                           └─► CHECK-L04  含这张主表
                                                 │
                                                 └─► GDF-SYNC-L09
                                                       从 dwd.md/ads.md 复制 CREATE 进派单包
                                                       再跑 gkx-gdf-ddl-signoff
```

改库前 IMPACT 必须交出清单。清单以外的语句 ALIGN 不得执行。两库都先留 `information_schema` 快照在 handoff，再改。

拟改动（IMPACT 可收窄，不可扩大）：


| 库                                                   | 表                                            | 动作                                                                                    |
| --------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------- |
| `demo_gkxlumenx_ads`                                | 指标 9 + 图 2 + `policy_entity` + 文本 3，共 15 张   | `CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci`；按文档补列注释。列类型不动           |
| `gkxlumenx_ads`                                     | 同上 12 张（已是 `utf8mb4_0900_ai_ci`，列数与 demo 相同） | 只补注释，使与文档一致                                                                           |
| `gkxlumenx_ads`                                     | `policy_text_parse`                          | 补 `metric_id`、`update_time`（demo 有、产线没有），再补注释                                         |
| `gkxlumenx_ads`                                     | `policy_match`、`policy_simulate`             | 补 `metric_id`，再补注释                                                                    |
| `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads` / 两个产线库 | `policy_industry_rel`                        | 列已齐、表级已是 `0900_ai_ci`。把 `policy_id` 列上的 `utf8mb4_general_ci` 收到表级排序规则；注释与 `dwd.md` 对齐 |


`demo_gkxlumenx_dwd.policy_base_info` 不在上表。ALIGN 不碰它。列集、类型、索引、注释和排序规则由 `POLICY-DDL-BASE-ALIGN-L08` 按 SPEC 一次改完。

`AUTO_INCREMENT` 当前值不是结构，不写进真源 CREATE。

## 3. 影响（开工前已看到的，IMPACT 叶要核实）

- demo 的 `policy_text_parse` 约有两万行，`policy_match`、`policy_simulate`、`policy_level_dist` 也有行。`CONVERT` 会重建表。这些表只有主键 `id`，没有字符列上的唯一索引，排序规则变化不会撞唯一键。`ORDER BY` 中文列的次序可能变。
- 产线缺的列都是可空 `longtext` 或带默认值的 `update_time`。按列名写入的 INSERT 不受影响；按位置写入的 INSERT 会坏。IMPACT 要在 `lumen-algo-py`、`demo-algo-ent-analysis`、`lumen-svc-platform` 里把这种写法找出来。找到则 ALIGN 停，升级李伟，不在本叶改算法。
- Java 现网读的是 `demo_gkxlumenx_ads`。ADS 这批多出来的可空列，本管线不改 Java 契约，具名 SELECT 可以忽略。读 `policy_base_info` 旧列的 CMS 语句归 `POLICY-DDL-BASE-CODE-L07`。
- `repos/lumen-algo-py/vendor/entan-py/scripts/mysql/schema_mysql.sql` 贴近产线缺列后的样子，不是 demo，也不是真源。`schema_policy_ads.sql` 是 PostgreSQL。两份都禁止再执行。本管线不改这两个文件，只在规约里声明作废为结构依据。
- DWD 里其余 `policy_*`（`policy_favorite`、`policy_effect_eval` 等）列数两边已经相同，且已是 `utf8mb4_0900_ai_ci`。不写进 `dwd.md`，本管线不 ALTER。
- `policy_base_info` 见 §1.7。demo 现网读者包括 `polan/basic/indicators.py`（`level`、`ext1`）、`polan/graph/ops.py`（`level`、`region`、`related_entities`、`ext1`、`ext5`）、`polan/industry_enrich.py`，以及 `lumen-algo-py/vendor/entan-py` 里同名模块和 `search.py`、`timeseries_board.py`、`shenzhen_board.py`。CMS 的 `v_cms_pol`、`PolicyService` 还用 `t.level`，并且 `source_id = policy_id` 在排序规则变成 `0900_ai_ci` 后会撞 1267。排序规则字面量归 `POLICY-DDL-CODE-L05`；旧列改读归 `POLICY-DDL-BASE-CODE-L07`。已改名空壳表 `policy_base_info_retired_20261026` 不动。产线不改回 37 列。



## 4. 开工顺序

1. 人写授权句。
2. coordinator 只升 `POLICY-DDL-CONV-L00`。
3. CONV 到联调闸门后，升 DOC、IMPACT、CODE。DOC 不改库，也不改 `dwd.md` 的 `policy_base_info` 节。IMPACT 只读，不扩大到主表改列。CODE 只改排序规则字面量，不 ALTER。
4. DOC 到联调闸门后升 BASE-SPEC。SPEC 只写交叉表和 `dwd.md`，不改库。
5. SPEC 与 CODE 都到联调闸门后，升 BASE-CODE。同仓串在 CODE 之后。只改代码，不 ALTER。
6. DOC、IMPACT、CODE 都到联调闸门，且 IMPACT 的拟 ALTER 没有超出 §2 的表，才升 ALIGN。ALIGN 不碰 `policy_base_info`。
7. SPEC、BASE-CODE、ALIGN 都到联调闸门后升 BASE-ALIGN。`policy_base_info` 改列集由 `human:淮政玮` 直接改。
8. ALIGN 与 BASE-ALIGN 的 handoff 都有改前改后 `information_schema` 后，升 CHECK。registry 里 CHECK 的 `depends_on` 仍只有 ALIGN，以本条为准。
9. CHECK 到联调闸门后升 GDF-SYNC。本叶把 `dwd.md` / `ads.md` 的 CREATE 原样复制进现行政策派单包，再跑 `gkx-gdf-ddl-signoff`，退出码 0 才算完成。不另写一套建表语句。
10. 签收可积压。`ready_to_sign` 不标 `done`。GDF 派单包签收前必须通过该 skill。

卡住只允许：连不上 `10.50.11.76`、拟 ALTER 超出 §2、发现按位置 INSERT、交叉表把 `ext1` 直接改名为 `policy_type` 或把 `level` 直接改名为 `rank`、李伟未确认就改 `policy_base_info` 列集或主键、有人要求把产线改回 37 列、单叶 cost > $10。