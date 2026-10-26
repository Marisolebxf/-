# POLICY-DDL-CODE-L05

- 任务：政策代码的排序规则改为 utf8mb4_0900_ai_ci
- 状态：代码已推 `origin/dev`；registry 仍为 `in_progress`（本叶不改 `task-registry.yaml`，编排仓不提交）
- 监管人：human:淮政玮
- claimed_by：agent:algorithm-agent
- ponytail: full

## 范围

只改政策 `policy_id` 比较和运行时对齐用的排序规则字面量。不 ALTER 现网库，不改 `policy_base_info` 列集，不改企业域 `org_id` 的 `utf8mb4_general_ci`，不改 `schema_mysql.sql`，不改 CMS 表自身的排序规则。

## 修改内容

- `demo-algo-ent-analysis` 与 `lumen-algo-py/vendor/entan-py` 的 `clause_job.py`、`industry_job.py`：`policy_id` 等值改为 `COLLATE utf8mb4_0900_ai_ci`，不再写死 `utf8mb4_unicode_ci` 或 `utf8mb4_general_ci`。
- 两仓 `industry_enrich.py`：关联表 `policy_id` 运行时只收到 `utf8mb4_0900_ai_ci`。`ALTER` 使用 `information_schema.COLUMN_TYPE` 的原类型和长度，不再写死 `varchar(128)`。已是该排序规则则不执行。
- `lumen-svc-platform`：`v_cms_pol` 的 `source_id = policy_id`，以及视图 `id` 的两条 `UNION`（否则建视图会 1271），加上 `PolicyService` 里失效列表的同一等值、审计里 `v.id` / `p.policy_id` 对 `business_id` 的等值，都显式 `COLLATE utf8mb4_0900_ai_ci`。`cms_entity_overlay.source_id = cms_op_audit.business_id` 两边都是 CMS `general_ci`，未改。

## 测试结果

- `demo-algo-ent-analysis`：`python -m pytest tests/test_policy_clause_job.py tests/test_policy_industry_rel.py -q` → 22 passed。
- `lumen-algo-py` vendor 无同名 pytest。
- `PolicyService` / 视图无对应单测，未跑 Maven。未对现网执行 `ALTER` 或重建视图。

## 提交

均已 `git pull --no-rebase` 后推 `origin/dev`。禁止 `main`，未 force。

| 仓 | 内容提交 | 推送 tip（merge） |
| --- | --- | --- |
| demo-algo-ent-analysis | `83a0fdf8914cf173a203959abfa629a30067df95` | `ef57e4a` |
| lumen-algo-py | `472b144913b841d413f4d9d83159d74431f30733` | `802eda8` |
| lumen-svc-platform | `8f194b04629419152472ddd6679c5911a7648e7d` | `feae0bf` |

远端领先导致首次 push 被拒，merge 后已推上。`PolicyService.java` 与远端自动合并，`COLLATE` 仍在。流水线未在本叶等待结果。

## 架构合规

- D1 调用链：前端仍走 Java REST；本叶只改 SQL 谓词与 Python 比较字面量。✅
- D2 算法只在 Python：Java 未做 NLP / 图谱 / 推理。✅
- D3 图谱：未涉及 Nebula。✅
- D8 / D9 / D10：无页面、无新指标、无交互改动。✅
- D12：demo 与 lumen 分仓改，未互相调用，未 merge。✅
- D14：未涉及对象存储。✅
- 未改库、未改 `schema_mysql.sql`、未改企业域 `org_id` 的 `general_ci`。✅

## cost

- actual_tokens: 未单列（随会话）
- model_used: grok-4.7
- actual_cost: 0
- cost_warn: green

## 遗留

- 现网 `policy_base_info` 改成 `utf8mb4_0900_ai_ci` 仍归后续 ALIGN / BASE-ALIGN。本叶只让比较在改列之后不报 1267。
- 关联表运行时 `MODIFY` 不带回列注释，与改前一样，执行时可能清掉该列注释。升级路径：把 `COLUMN_COMMENT` 原样写回。
- `v_cms_pol` 里 `title` / `body` 等 `COALESCE(JSON, 主表字符列)` 未加 `COLLATE`。整表改为 `0900_ai_ci` 后若再报 1271，不在本叶。
