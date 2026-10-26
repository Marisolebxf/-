# POLICY-DDL-BASE-CODE-L07

- 任务：政策主表读列按交叉表改到 `dwd.md` 的 `policy_base_info` 目标列
- 状态：代码已推 `origin/dev`；registry 仍为 `in_progress`（本叶不改 `task-registry.yaml`，编排仓不提交）
- 监管人：human:淮政玮
- claimed_by：agent:algorithm-agent
- 协作：api-agent（`v_cms_pol` / `PolicyService`）
- ponytail: full

## 范围

两棵算法树里读 `policy_base_info` 的代码，以及 `lumen-svc-platform` 的 `v_cms_pol` 和 `PolicyService`，停止读取交叉表标为删除的列：`tenant_id`、`level`、`elements`、`factors`、`gis_location`、`attachment`、`sci_tech_attribute`、`application_conditions`、`execution_cycle`、`execution_entity`、`related_entities`、`ext1`–`ext5`。`create_time` / `update_time` 只在主表上改读 `created_time` / `updated_time`。

不 ALTER 现网库，不执行 `CREATE OR REPLACE VIEW`，不改 `schema_mysql.sql` / `schema_policy_ads.sql`，不改企业域 `org_id` 的 `general_ci`，不改 `policy_industry_rel` 的排序规则字面量，不改 CMS 表自身的排序规则。CODE-L05 已写上的 `COLLATE utf8mb4_0900_ai_ci` 保留。

## 读列对应

- 级别展示和筛选读 `rank` 原文。不把 `1/2/3/4` 映射成国家级/省级/市级/区县级。文字别名只保留「区级 / 区县 / 县级 → 区县级」。
- 类型读 `policy_type`。不把 `ext1` 改名为 `policy_type`。
- 省、市、区读 `province` / `city` / `district`。不把 `region` 拼串拆开。国内行政区不写入 `region`。`region` 只作国际实施区域。
- 深圳判定改为 `city` 以「深圳」开头。门户地域条件改为省/市/区/国家/地理区域/国际实施区域的或匹配。
- 有效性：状态非空、非纯数字、且不含「失效」，再看失效日。数字 `1` 不算有效，也不写成「有效」。失效列表只认 `status='失效'`。
- `source_plane` 不从 `ext1` / `level` / `region` 推断。ODS 没有该列时映射结果为空。Mock 自己生成的行才写字面量 `domestic` 或 `global`。
- 产业不读 `ext5` / `theme` / 主表 `related_entities`。补码写入 `policy_industry_rel`。`theme` 只作国际专题原文。
- ADS `policy_level_dist.level` 仍是整型列，本叶写入 `NULL`，原文级别放在 `ext` 的 `rank`。不改 ADS 表结构。

## 修改内容

- `demo-algo-ent-analysis` 与 `lumen-algo-py/vendor/entan-py`：`indicators`、`graph/ops`、`graph/entity`、`industry_enrich`、`search`（仅 lumen）、`timeseries_board`、`shenzhen_board`、`text/parse`、`text/match`、`eval`、`clause_job`、`mockgen/generate.py`、`mockgen/incr.py`、`api/policy_routes.py`、`db.py`。`db.py` 的本地 sqlite 列清单对齐目标列，并跳过对 `policy_base_info` 的补列，避免 `init_schema` 对现网 `ALTER`。
- `lumen_common`：产业补码不再 `UPDATE policy_base_info SET related_entities`；增量扫描改为关联表 `NOT EXISTS`。`theme` 不再回退 `ext5`。
- `lumen-svc-platform`：`v_cms_pol` 两支 `UNION` 改为 `t.\`rank\`` 与 `t.policy_type`。`PolicyService.expired` 改为 `status='失效'` 和 `updated_time`。只读门面的政策 `type` 改为 `policy_type`。详情说明改为 `status/rank/policy_type/source`。

## 测试结果

- `demo-algo-ent-analysis`：`python -m pytest tests/test_policy_ds_composite.py tests/test_policy_mock_rank.py tests/test_policy_portal_gaps.py tests/test_policy_clause_job.py tests/test_policy_industry_rel.py tests/test_policy_industry_enrich.py tests/test_policy_hang_industry.py -q` → 76 passed。
- `lumen-algo-py`：`python -m pytest tests/test_policy_industry_enrich.py tests/test_industry_vid_enrich.py tests/test_policy_search_filter.py tests/test_policy_portal_gaps.py tests/test_timeseries_board.py tests/test_policy_shenzhen_board.py tests/test_policy_job.py tests/test_policy_narrate.py -q` → 86 passed。
- 两棵树 `polan.graph.ops.self_check` 在 sqlite 上通过。demo 用 sqlite 生成 8 条主表行：状态只有空或「失效」，国内行的 `region` 为空，`rank` 不是数字码。
- `PolicyService` / 视图无对应单测，未跑 Maven。未对现网执行 `ALTER` 或重建视图。

## 提交

均已推 `origin/dev`。禁止 `main`，未 force。`lumen-svc-platform` 首次 push 被拒后 `git pull --no-rebase`，无冲突再推。

| 仓 | 内容提交 | 推送 tip |
| --- | --- | --- |
| demo-algo-ent-analysis | `8682260e7a3cae9f54394c4f9ae88b4f589311b5` | `8682260` |
| lumen-algo-py | `fc65914200404594a27b4b1e861d476c9e617348` | `fc65914` |
| lumen-svc-platform | `aecfd3df7f83a96437b4bc282eeb5c3a811334f8` | `dc5f373`（merge `d8fc1a4`） |

## 架构合规

- D1 调用链：前端仍走 Java REST；本叶只改 Python 读列和 CMS 视图 SQL。✅
- D2 算法只在 Python：Java 未做 NLP / 图谱 / 推理。✅
- D3 图谱：未改 Nebula 协议，未把产业 VID 写回主表。✅
- D8 / D9 / D10：无页面、无新指标口径、无交互改动。ADS 级别列暂写空，原文在 `ext.rank`。✅
- D12：demo 与 lumen 分仓改，未互相调用，未 merge。✅
- D14：未涉及对象存储。✅
- 未改库、未改 `schema_mysql.sql`、未改企业域 `org_id` 的 `general_ci`、未改 `policy_industry_rel` 排序规则字面量。✅

## cost

- actual_tokens: 未单列
- model_used: grok-4.7
- actual_cost: 0
- cost_warn: green

## 遗留

- 现网 `policy_base_info` 仍是旧列集。本叶代码按目标列读取，落库归 L08。在 L08 之前，对现网直接跑这些查询会因缺列失败。本叶不提前 `ALTER`。
- `source_plane` 在目标 DDL 中为 `NOT NULL`，但 ODS 没有该列时映射留空。L08 在加非空约束前必须补齐。Mock 自造行使用字面量，不从旧列推断。
- `v_cms_pol` 只改了脚本，现网视图未重建。
