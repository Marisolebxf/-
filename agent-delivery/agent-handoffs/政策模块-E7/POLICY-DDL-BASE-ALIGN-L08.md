# POLICY-DDL-BASE-ALIGN-L08

- 任务：demo `policy_base_info` 一次对齐到派单包 10 的 CREATE，产线只补缺的 `is_history`
- 状态：改库完成（本叶不改 registry）
- 执行：agent:data-agent
- 监管人：human:淮政玮
- 日期：2026-10-26
- ponytail: full
- 依据：`POLICY-DDL-BASE-SPEC-L06` 交叉表；`dwd.md` 的目标 CREATE

human:淮政玮 2026-10-26 选择方案 1：现网 20,000 行 `source_plane` 整批填 `domestic`。不从 `region`、`ext1`、`level` 推导。总控职务表：改列集由淮政玮直接改，不升级 human:李伟。口令未写入本文件。

联调通过。

## 做法

不 DROP 表。在 `demo_gkxlumenx_dwd` 建同结构新表，按交叉表拷入 20,000 行，核对行数和回填值之后再改名：

- `policy_base_info` → `policy_base_info_pre_20261026`（旧 37 列，20,000 行仍在，表级 `utf8mb4_general_ci`）
- 新表 → `policy_base_info`

产线 `gkxlumenx_dwd.policy_base_info` 原来已是目标列集去掉 `is_history`，0 行。只加了 `is_history int NULL`，位置在 `is_deleted` 之后。没有改回 37 列。`policy_base_info_retired_20261026` 未动。

`gkxlumenx_cms.v_cms_pol` 在改名后按 `db/9x_gkxlumenx_cms.sql` 重建。JSON 抽出的字符串与主表 `utf8mb4_0900_ai_ci` 混用会 1271，所以这些表达式加了 `COLLATE utf8mb4_0900_ai_ci`。同一处改动写回该 SQL 文件。未改 CMS 表自身的排序规则。

## 回填与丢弃

回填：`id`、`policy_id`、`title`、`issued_number`、`publish_organization`、`publish_date`、`implementation_date`、`expire_date`、`abstract`、`keywords`、`content`、`url`、`pedigree`、`keypoints`、`source`、`publish_year`（整数写成十进制字符串）、`is_deleted`、`create_time`→`created_time`、`update_time`→`updated_time`。

整批写入、不来自旧列：`source_plane='domestic'`（20,000 行）。

留空：`status`（旧值全是 `1`，不写成「有效」）、`rank`、`policy_type`、`topic`、`province`、`city`、`district`、`region`（旧行政区拼串不写入国际实施区域）、`country`、`geo_region`、`disclosure_date`、`theme`、`policy_support`、`appendix_name`、`appendix_link`、`language`、`report_number`、`project_id`、`security_class`、`version_type`、`volume_no`、`doc_type`、`etl_batch_id`、`ods_updated_time`、`is_history`。

不进新表、仍留在 `policy_base_info_pre_20261026`：`tenant_id`、`level`、`elements`、`factors`、`gis_location`、`attachment`、`sci_tech_attribute`、`application_conditions`、`execution_cycle`、`execution_entity`、`related_entities`、`ext1`–`ext5`。

禁止改名已遵守：`ext1` 没有写入 `policy_type`，`level` 没有写入 `rank`，`region` 拼串没有拆进省市区。

拷完、改名前，按 `utf8mb4_0900_ai_ci` 对过 20,000 行：`policy_id`、`title`、`content`、`create_time`、`update_time`、`is_deleted` 与旧表一致。

## 改后快照

2026-10-26。行数是 `COUNT(*)`。

| 库.表 | 行数 | 列数 | 表排序规则 | 非 0900 字符列 | 索引 |
| --- | ---: | ---: | --- | ---: | --- |
| `demo_gkxlumenx_dwd.policy_base_info` | 20000（全部 `domestic`） | 45 | `utf8mb4_0900_ai_ci` | 0 | `PRIMARY(id)`，`uk_policy_plane_id(source_plane, policy_id)` |
| `gkxlumenx_dwd.policy_base_info` | 0 | 45 | `utf8mb4_0900_ai_ci` | 0 | 同上 |
| `demo_gkxlumenx_dwd.policy_base_info_pre_20261026` | 20000 | 37 | `utf8mb4_general_ci` | 旧列 | 仅 `PRIMARY(id)` |

`is_history` 在两库都是第 43 列，`int NULL`，在 `is_deleted` 与 `created_time` 之间。`v_cms_pol` 改名后可查，返回 20,004 行（主表 20,000 加上 CMS 自建政策）。

## 架构合规

- D1–D4：未改算法、未改调用链、未改 Nebula。视图只按已提交的 CMS SQL 重建。✅
- D12：demo 与产线分库改，没有把 37 列写回产线。✅
- 未 DROP 表，未写 ODS 或供应库 `gkx`，未动 `policy_base_info_retired_20261026`。✅
- D8 / D9 / D10 / D14：未改页面、未改指标口径、未改对象存储。✅
- 口令未写入本文件。✅

## cost

- actual_tokens: 未单列
- model_used: grok-4.7
- actual_cost: 0
- cost_warn: green

## 遗留

旧 37 列表留在 `policy_base_info_pre_20261026`。确认不再需要这批丢弃列之后，由人决定是否 DROP。本叶不删。
