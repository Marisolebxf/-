# 政策 ADS/DWD 建表真源对齐 · 长任务总控

> **日期**：2026-10-26  
> **授权**：未授权。待 `human:淮政玮` 在聊天写明「后续认领不必再问」后，本文件才成为一次授权。现在禁止升 ready、禁止认领、禁止改库。  
> **监管人（授权后）**：`human:淮政玮`  
> **升级人**：改列集、改主键、DROP、写 ODS / 供应库 `gkx` → `human:李伟`。  
> **锁**：`lock_hours=24`  
> **目标**：`ads.md` 与 `dwd.md` 里每张在册表有一份带注释的 MySQL `CREATE`；`demo_gkxlumenx_*` 与 `gkxlumenx_*` 同表同结构，只换库名；字符集 `utf8mb4`、排序规则 `utf8mb4_0900_ai_ci` 写成规约并在本批表上落地。  
> **模式**：长任务。规约：[`长任务执行规约.md`](../../长任务执行规约.md)。不套前端 A–E，无段 E 金路径。同仓同时只派一张 coding 单。  
> **厚包**：本文件。薄条 = 各叶 registry DoD。`/goal` 必抄本路径。强度：文档叶不压完整性；改库叶 `ponytail full`。

| 作业 | 仓 | 分支 | 任务 | 状态门 |
|------|-----|------|------|--------|
| 规约 | `gkx-orchestration` | `origin/dev` | `POLICY-DDL-CONV-L00` | 授权句之后才 ready |
| 文档 CREATE | 同上 | 同上 | `POLICY-DDL-DOC-L01` | CONV 联调闸门 |
| 影响扫描 | 同上 | 同上 | `POLICY-DDL-IMPACT-L02` | 授权后可与 DOC 并行（只读代码和库） |
| 两库对齐 | 同上（改的是 MySQL，不改算法仓） | 同上 | `POLICY-DDL-ALIGN-L03` | DOC 与 IMPACT 都到联调闸门，且 IMPACT 写明拟 ALTER 清单 |
| 核对 | 同上 | 同上 | `POLICY-DDL-CHECK-L04` | ALIGN 联调闸门 |

废作、不建单、不派：把 `policy_base_info` 的 demo 37 列或产线 44 列互相覆盖；用 PostgreSQL `schema_policy_ads.sql` 或旧稿 v1 §3 的类型当结构；用 `schema_mysql.sql` 再执行一遍；DROP 有数据的表；写 `gkxlumenx_ods` / 供应库 `gkx`。

---

## 1. 目标（已拍板，授权后禁止回问）

1. **在册范围**：只处理这两份文档里已经点名的表。  
   - [`ads.md`](../../data/data-design/storage/POLICY/stores/mysql/ads.md)：指标 9 张、图镜像 2 张、`policy_entity`、文本 3 张。`policy_industry_rel` 不在这里再写一份 CREATE。  
   - [`dwd.md`](../../data/data-design/storage/POLICY/stores/mysql/dwd.md)：`policy_industry_rel` 已有 CREATE，本管线只补齐注释与列级排序规则，不另起列集。  
2. **结构以现网 demo 的列、类型、空值、默认值、索引为准**（2026-10-26 对 `10.50.11.76` 的 `demo_gkxlumenx_ads`）。不采用 PostgreSQL 脚本，也不把旧稿 v1 的 `smallint` / `decimal(6,2)` / 二级索引写回去。  
3. **排序规则单独拍板，覆盖 demo 现状**：表和全部字符列都是 `utf8mb4` / `utf8mb4_0900_ai_ci`。demo 上的 `utf8mb4_unicode_ci`、`policy_industry_rel.policy_id` 上的 `utf8mb4_general_ci` 都要改到这一套。  
4. **两库一致**：同一张表在 `demo_gkxlumenx_ads` 与 `gkxlumenx_ads`（关联表再加两个 DWD 库）列集、类型、空值、默认值、索引、注释、排序规则相同，只换库名。文档里的 CREATE 写 `demo_gkxlumenx_*`。  
5. **注释写在 CREATE 里**。列注释取自现有中文用途（`ads.md` 用途列、旧稿里仍对得上的 COMMENT、`policy_industry_rel` 已有注释）。对不上的列不编口径，注释写「现网 demo 有此列，口径待补」，并在 handoff 列出。  
6. **规约**：上述 2–4 写成 `agent-delivery/data/data-design/storage/mysql-ddl-convention.md`，并在 `architecture-baseline.md` 加一条指针。从本批表执行。其它域已有表不在本管线批量改。  
7. **不改** `policy_base_info` 的列集。demo 是 37 列 `utf8mb4_general_ci`，产线是 44 列 `utf8mb4_0900_ai_ci`（旧 37 列空壳已改名 `policy_base_info_retired_20261026`）。上一轮已定 37 列不作产线依据。本轮「与 demo 一致」不套到这张主表，直到另一次人拍板。

## 2. 干法

```text
CONV-L00 规约落盘
    ├─闸门─► DOC-L01  把 demo 列结构写成带注释的 CREATE，收进 ads.md；
    │         dwd.md 的 policy_industry_rel 只补注释/排序规则
    └─并行─► IMPACT-L02  只读：谁 INSERT/SELECT 这些表，拟 ALTER 清单
                │
DOC + IMPACT 都到联调闸门
                │
                └─► ALIGN-L03  先 demo 后产线。只 CONVERT 排序规则、补缺列、补注释。
                      不 DROP，不改列类型，不改主键。
                      │
                      └─► CHECK-L04  information_schema 与两份 md 逐表对上
```

改库前 IMPACT 必须交出清单。清单以外的语句 ALIGN 不得执行。两库都先留 `information_schema` 快照在 handoff，再改。

拟改动（IMPACT 可收窄，不可扩大）：

| 库 | 表 | 动作 |
|----|----|------|
| `demo_gkxlumenx_ads` | 指标 9 + 图 2 + `policy_entity` + 文本 3，共 15 张 | `CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci`；按文档补列注释。列类型不动 |
| `gkxlumenx_ads` | 同上 12 张（已是 `utf8mb4_0900_ai_ci`，列数与 demo 相同） | 只补注释，使与文档一致 |
| `gkxlumenx_ads` | `policy_text_parse` | 补 `metric_id`、`update_time`（demo 有、产线没有），再补注释 |
| `gkxlumenx_ads` | `policy_match`、`policy_simulate` | 补 `metric_id`，再补注释 |
| `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads` / 两个产线库 | `policy_industry_rel` | 列已齐、表级已是 `0900_ai_ci`。把 `policy_id` 列上的 `utf8mb4_general_ci` 收到表级排序规则；注释与 `dwd.md` 对齐 |

`AUTO_INCREMENT` 当前值不是结构，不写进真源 CREATE。

## 3. 影响（开工前已看到的，IMPACT 叶要核实）

- demo 的 `policy_text_parse` 约有两万行，`policy_match`、`policy_simulate`、`policy_level_dist` 也有行。`CONVERT` 会重建表。这些表只有主键 `id`，没有字符列上的唯一索引，排序规则变化不会撞唯一键。`ORDER BY` 中文列的次序可能变。  
- 产线缺的列都是可空 `longtext` 或带默认值的 `update_time`。按列名写入的 INSERT 不受影响；按位置写入的 INSERT 会坏。IMPACT 要在 `lumen-algo-py`、`demo-algo-ent-analysis`、`lumen-svc-platform` 里把这种写法找出来。找到则 ALIGN 停，升级李伟，不在本叶改算法。  
- Java 现网读的是 `demo_gkxlumenx_ads`。本管线不改 Java 契约。多出来的可空列，具名 SELECT 可以忽略。  
- `repos/lumen-algo-py/vendor/entan-py/scripts/mysql/schema_mysql.sql` 贴近产线缺列后的样子，不是 demo，也不是真源。`schema_policy_ads.sql` 是 PostgreSQL。两份都禁止再执行。本管线不改这两个文件，只在规约里声明作废为结构依据。  
- DWD 里其余 `policy_*`（`policy_favorite`、`policy_effect_eval` 等）列数两边已经相同，且已是 `utf8mb4_0900_ai_ci`。不写进 `dwd.md`，本管线不 ALTER。  
- `policy_base_info` 见 §1.7。动它会碰到 CMS 读 demo 37 列、产线 UK `(source_plane, policy_id)` 和已改名的空壳表。

## 4. 开工顺序

1. 人写授权句。  
2. coordinator 只升 `POLICY-DDL-CONV-L00`。  
3. CONV 到联调闸门后，升 DOC 与 IMPACT。DOC 不改库。IMPACT 只读。  
4. 两叶都到联调闸门，且 IMPACT 的拟 ALTER 没有超出 §2 的表，才升 ALIGN。  
5. ALIGN 的 handoff 有改前改后 `information_schema` 后，升 CHECK。  
6. 签收可积压。`ready_to_sign` 不标 `done`。

卡住只允许：连不上 `10.50.11.76`、拟 ALTER 超出 §2、发现按位置 INSERT、有人要求改 `policy_base_info` 列集、单叶 cost > $10。
