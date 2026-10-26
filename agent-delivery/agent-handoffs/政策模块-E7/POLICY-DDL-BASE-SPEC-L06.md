# POLICY-DDL-BASE-SPEC-L06

- 任务：把 `policy_base_info` 的结构真源改成派单包 10 的 CREATE，并写出交叉表、丢弃列和行回填
- 状态：文档已落盘（definition 叶，本叶不改 registry）
- claimed_by：`agent:data-agent`
- supervised_by：`human:淮政玮`
- ponytail: off（文档叶不压完整性）
- 厚包：`agent-delivery/agent-handoffs/政策模块-E7/POLICY-DDL-ALIGN-长任务总控.md`

## 范围

只改 `agent-delivery/data/data-design/storage/POLICY/stores/mysql/dwd.md` 里 `policy_base_info` 那一节，并新增本 handoff。没有改 `policy_industry_rel`、`policy_text_parse`，没有改 `ads.md`，没有改库，没有 DROP，没有把旧 37 列加到产线。未 commit、未 push。口令未写入任何文件。

目标 CREATE 取 `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/10-DWD-MySQL-DDL/policy_base_info-MySQL.md`。文档库名写 `demo_gkxlumenx_dwd`。表和全部字符列写 `utf8mb4` / `utf8mb4_0900_ai_ci`。列注释只沿用派单包里已有的注释。不写 `AUTO_INCREMENT` 当前值。

## 现网快照（只读，2026-10-26，10.50.11.76:3306）

只跑了 `information_schema` 和 `SELECT`。`COUNT(*)` 如下。

| 库.表 | 行数 | 列数 | 表级排序规则 | 索引 | 角色 |
|---|---:|---:|---|---|---|
| `demo_gkxlumenx_dwd.policy_base_info` | 20000 | 37 | `utf8mb4_general_ci` | 仅 `PRIMARY (id)` | 待对齐的现网 demo |
| `gkxlumenx_dwd.policy_base_info` | 0 | 44 | `utf8mb4_0900_ai_ci` | `PRIMARY (id)` + `uk_policy_plane_id (source_plane, policy_id)` | 产线。已是派单包列集去掉 `is_history`。不要改回 37 列 |
| `gkxlumenx_dwd.policy_base_info_retired_20261026` | 0 | 37 | `utf8mb4_general_ci` | 仅 `PRIMARY (id)` | 旧空壳。不是目标。demo 库没有这张表 |

demo 字符列都是 `utf8mb4` / `utf8mb4_general_ci`。产线字符列已是 `utf8mb4` / `utf8mb4_0900_ai_ci`，表注释已是「政策主表（国内+国际同表）」。产线没有 `is_history`。

demo 现网 37 列（类型按 `information_schema`，均可空，除 `id` 为 `bigint NOT NULL AUTO_INCREMENT` 主键）：`tenant_id bigint`，`policy_id longtext`，`title longtext`，`issued_number longtext`，`publish_organization longtext`，`publish_date date`，`implementation_date date`，`expire_date date`，`status bigint`，`publish_year bigint`，`level bigint`，`region longtext`，`abstract longtext`，`keywords longtext`，`content longtext`，`url longtext`，`pedigree longtext`，`elements longtext`，`keypoints longtext`，`factors longtext`，`source longtext`，`gis_location longtext`，`attachment longtext`，`sci_tech_attribute bigint`，`application_conditions longtext`，`execution_cycle longtext`，`execution_entity longtext`，`related_entities longtext`，`create_time datetime`（默认 `CURRENT_TIMESTAMP`），`update_time datetime`（默认 `CURRENT_TIMESTAMP`），`is_deleted bigint`，`ext1`–`ext5 longtext`。

## 交叉表

对照面是 demo 现网 37 列 → 派单包 10 的 45 列。产线已经在目标侧，见下一节，不把产线列算进「新增」。

### 新增

目标有、demo 现网无。这些列没有同名值可回填。

| 列 | 目标类型 | 备注 |
|---|---|---|
| `source_plane` | `varchar(16) NOT NULL` | 20,000 行没有来源列。不从 `ext1` / `level` / `region` 推导 |
| `rank` | `varchar(50) NULL` | 不是 `level` 的改名 |
| `policy_type` | `varchar(200) NULL` | 不是 `ext1` 的改名 |
| `topic` | `text NULL` | |
| `province` | `varchar(50) NULL` | 不是 `region` 拼串拆出来的 |
| `city` | `varchar(50) NULL` | 同上 |
| `district` | `varchar(50) NULL` | 同上 |
| `country` | `text NULL` | |
| `geo_region` | `text NULL` | |
| `disclosure_date` | `date NULL` | |
| `theme` | `text NULL` | |
| `policy_support` | `json NULL` | |
| `appendix_name` | `text NULL` | 不是 `attachment` 的改名 |
| `appendix_link` | `text NULL` | 同上 |
| `language` | `text NULL` | |
| `report_number` | `text NULL` | |
| `project_id` | `varchar(500) NULL` | |
| `security_class` | `text NULL` | |
| `version_type` | `text NULL` | |
| `volume_no` | `text NULL` | |
| `doc_type` | `varchar(64) NULL` | |
| `etl_batch_id` | `varchar(64) NULL` | |
| `ods_updated_time` | `datetime NULL` | |
| `is_history` | `int NULL` | 产线也没有这列。NULL 视为当前，取数不过滤 |
| `created_time` | `datetime NOT NULL DEFAULT CURRENT_TIMESTAMP` | 值可以从 demo `create_time` 拷贝，见回填 |
| `updated_time` | `datetime NULL` | 值可以从 demo `update_time` 拷贝，见回填 |

### 删除

demo 现网有、目标无。不进产线目标列。不 DROP 表；列集改动在 L08。有值的列是数据丢弃，不是改名。

| 列 | demo 类型 | 非空行数（20,000 行内） | 值 |
|---|---|---:|---|
| `tenant_id` | `bigint` | 20000 | 丢弃。全部为 1 |
| `level` | `bigint` | 19499 | 丢弃。禁止改名为 `rank` |
| `elements` | `longtext` | 0 | 丢弃。不进目标列 |
| `factors` | `longtext` | 0 | 丢弃。不进目标列 |
| `gis_location` | `longtext` | 17813 | 丢弃。不进目标列 |
| `attachment` | `longtext` | 3733 | 丢弃。不改名为 `appendix_*` |
| `sci_tech_attribute` | `bigint` | 20000 | 丢弃。全部为 1 |
| `application_conditions` | `longtext` | 0 | 丢弃 |
| `execution_cycle` | `longtext` | 0 | 丢弃 |
| `execution_entity` | `longtext` | 19989 | 丢弃 |
| `related_entities` | `longtext` | 20000 | 丢弃。不进目标列 |
| `create_time` | `datetime` | 20000 | 列名从目标删除。值拷贝到 `created_time` |
| `update_time` | `datetime` | 20000 | 列名从目标删除。值拷贝到 `updated_time` |
| `ext1` | `longtext` | 18138 | 丢弃。禁止改名为 `policy_type` |
| `ext2` | `longtext` | 17813 | 丢弃 |
| `ext3` | `longtext` | 1165 | 丢弃 |
| `ext4` | `longtext` | 10294 | 丢弃 |
| `ext5` | `longtext` | 2 | 丢弃 |

### 类型变化

同名列。排序规则另计：demo 这些字符列现在是 `utf8mb4_general_ci`，目标是 `utf8mb4_0900_ai_ci`。

| 列 | demo 现网 | 目标 | 现网值能否落入新类型 |
|---|---|---|---|
| `policy_id` | `longtext NULL` | `varchar(100) NOT NULL` | 能。20,000 个互异、无空、长度 ≤ 100 |
| `title` | `longtext NULL` | `text NOT NULL` | 能。无空，字节长度不超过 text |
| `issued_number` | `longtext NULL` | `varchar(200) NULL` | 能。7,460 行非空，长度都 ≤ 200 |
| `publish_organization` | `longtext NULL` | `text NULL` | 能。19,989 行非空，字节长度不超过 text |
| `publish_year` | `bigint NULL` | `varchar(32) NULL` | 能。全部有值，是 1981–2026 的年份整数，写成十进制字符串 |
| `status` | `bigint NULL` | `varchar(20) NULL` | 不能按现网值回填。20,000 行全是 `1`，不是「有效/失效原文」 |
| `region` | `longtext NULL` | `text NULL`，注释「国际实施区域」 | 类型放得下（最长 13 字）。值不能回填，见禁止改名 |
| `abstract` | `longtext NULL` | `text NULL` | 能。12,159 行非空，字节长度不超过 text |
| `keywords` | `longtext NULL` | `text NULL` | 能。现网全空 |
| `url` | `longtext NULL` | `text NULL` | 能。20,000 行非空，字节长度不超过 text |
| `pedigree` | `longtext NULL` | `text NULL` | 能。2 行非空，字节长度不超过 text |
| `keypoints` | `longtext NULL` | `varchar(1000) NULL` | 能。现网全空 |
| `source` | `longtext NULL` | `text NULL` | 能。20,000 行非空，字节长度不超过 text |
| `is_deleted` | `bigint NULL` | `smallint NOT NULL DEFAULT 0` | 能。20,000 行全是 0 |

同名且 SQL 类型不变：`id bigint NOT NULL AUTO_INCREMENT`，`publish_date date`，`implementation_date date`，`expire_date date`，`content longtext`。`content` 只改排序规则。`publish_date` / `implementation_date` 各有 3 行为空，目标仍可空。`expire_date` 现网全空。

### 主键或唯一键变化

| 项 | demo 现网 | 目标 | 产线现网 |
|---|---|---|---|
| 主键 | `PRIMARY (id)` | `PRIMARY (id)` | `PRIMARY (id)` |
| 唯一键 | 无 | `UNIQUE uk_policy_plane_id (source_plane, policy_id)` | 已有这把唯一键 |
| 业务键 | 旧文档把 `policy_id` 写成主键。现网 `policy_id` 是 `longtext`，不在索引里 | `policy_id` 是唯一键的第二列，不是主键 | 已按目标 |

主键列没有变，仍是 `id`。变化是加上 `(source_plane, policy_id)` 这把唯一键。demo 的 `policy_id` 已经 20,000 行互异，所以不会因为 `policy_id` 重复撞这把唯一键。空 `policy_id` 为 0。

## 禁止直接改名

这三组不是同一列的换名，L08 不得把左边的值写入右边。

1. `ext1` 不是 `policy_type`。`ext1` 有 18,138 行非空，样例是「其他通知」「公示公告」「政策文件-管理办法/实施方案」「申报通知」。`policy_type` 作为新列留空，不接收这些值。
2. `level` 不是 `rank`。`level` 是 `bigint`：`1` 共 2,174，`2` 共 9,922，`3` 共 6,149，`4` 共 1,254，空 501。`rank` 的注释是「国家级/省级/市级/区县级原文」。不把 1/2/3/4 写进 `rank`。
3. `region` 拼串不是 `province` / `city` / `district`。非空 17,813 行，无分隔符，最长 13 字，样例是「上海市」「北京市」「广东省深圳市」「河南省」。这三个新列留空。demo 的 `region` 也不是目标列 `region`（注释「国际实施区域」）的回填来源，这 17,813 个值不写入目标 `region`。

`gis_location`、`related_entities`、`factors`、`elements`、`ext1`–`ext5` 不写进产线目标列。

## 行回填与丢弃

不 DROP 表。下面说的是 L08 改 demo 列集时，现有 20,000 行哪些值留得下。产线是 0 行，没有行要回填。

能回填：

- `id`、`policy_id`、`title`、`issued_number`、`publish_organization`、`publish_date`、`implementation_date`、`expire_date`、`abstract`、`keywords`、`content`、`url`、`pedigree`、`keypoints`、`source`：同名，现网值落得进目标类型。
- `publish_year`：年份整数写成十进制字符串，放入 `varchar(32)`。
- `is_deleted`：全是 0，写入 `smallint NOT NULL`。
- `create_time` → `created_time`，`update_time` → `updated_time`：20,000 行都有值，按时间值拷贝。这是审计时间列的列名对应，不是上面三组改名。

不能回填，值丢弃：

- `status` 的 `1`。不写成「有效」，也不把数字塞进「有效/失效原文」。
- `region` 的国内行政区拼串。不拆省市区，不写入目标 `region`。
- 删除表里除 `create_time` / `update_time` 以外的列，包括有值的 `tenant_id`、`level`、`sci_tech_attribute`、`gis_location`、`attachment`、`execution_entity`、`related_entities`、`ext1`–`ext5`。

新增列里，除了两个审计时间列的拷贝，都没有 demo 值。`source_plane` 是 `NOT NULL`，20,000 行必须在改成目标列时有一个填充值。本叶不指定 `domestic` 或 `global`，也不从 `ext1`、`level`、`region` 推导。现网 `region` 样例是国内行政区地名，`source` 样例是国内机构名、`demo-mock` 和 `[]`，只作为 L08 的现场事实，不在本叶写成 UPDATE。

## 产线对照

`gkxlumenx_dwd.policy_base_info` 的 44 列与派单包 10 的同名列在类型、空值、默认值、注释和 `utf8mb4_0900_ai_ci` 上一致，唯一键已在，0 行。与目标 CREATE 的差别只有缺 `is_history`。不要把 demo 的 37 列加回去，不要改回 37 列。

`policy_base_info_retired_20261026` 只记这一笔：产线库里的 37 列空壳，0 行，`utf8mb4_general_ci`，主键只有 `id`。不是目标，本管线不动它。

## 偏离

派单包 10 正文写过「若仅有 Demo as-built，按差集加列，不要按旧 37 列重建后丢新列」。本叶以同文件的 CREATE 为列集真源：CREATE 里的新列要有，CREATE 里没有的旧列不进入目标，也不加到产线。这与总控 §1.7 一致。没有用 PostgreSQL 脚本或旧稿 v1 的类型。

## 执行边界

改列集、改类型、改主键或唯一键的执行在 `POLICY-DDL-BASE-ALIGN-L08`。按总控职务表：`policy_base_info` 改列集由 `human:淮政玮` 直接改，不升级 `human:李伟`。DROP、写 ODS 或供应库 `gkx` 才升级 `human:李伟`。本叶不 ALTER，不 DROP。

## 产物清单

- `agent-delivery/data/data-design/storage/POLICY/stores/mysql/dwd.md` 的 `policy_base_info` 节：换成上面的目标 CREATE。
- 本 handoff。

## 架构合规

1. 算法只在 Python：本叶只有文档，没有算法。✅
2. 调用链前端 → Java → Python：没有改调用链。✅
3. 图谱 NebulaGraph：没有改图库。✅
4. 可观测性：文档叶，没有运行时代码。✅
5. CI/CD：未 commit、未 push，没有业务流水线。✅
6. demo 不 merge 进 lumen：只改编排仓文档。✅
7. 共享聚合、Java 只读 ADS：没有改 Java。✅
8. 标准表先行：目标 CREATE 写入 `dwd.md`。没有改库，没有写 ODS 或供应库 `gkx`，没有 DROP。✅
9. D8 前端规范：不涉及页面。✅
10. D9 血缘：没有改指标口径，没有把 `ext1` 写成 `policy_type`。✅
11. D10 交互规范：不涉及交互。✅
12. D12 demo / lumen 隔离：文档库名是 `demo_gkxlumenx_dwd`，产线只换库名，没有把 demo 服务写进 lumen。✅
13. D14 对象存储：不涉及。✅

## cost

- actual_tokens: 未单列
- model_used: grok-4.7
- actual_cost: 0
- cost_warn: green

## 联调

会签通过。
