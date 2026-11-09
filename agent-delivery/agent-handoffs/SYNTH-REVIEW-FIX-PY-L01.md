# SYNTH-REVIEW-FIX-PY-L01 · SYNTH 六 commit 评审修复（Python 侧）

> 评审结论「需修后放行」：4 项 Important（P1–P4）+ 3 条顺手 Minor（M5/M7/M10）。
> 评审对象：`e8565a9 / 6bab0ed / b778c07 / 429f516 / 2744c46 / c8fbd1e`（SYNTH 六 commit）。
> 本单只修评审点名项，不扩范围；M6/M8/M9/M11/M12 **不修（登记）**，见 §6。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm` |
| supervised_by | 当前会话用户（父会话 `/goal` 直接派单；registry 无本单条目，task-registry 查无 `SYNTH-REVIEW-FIX-PY-L01`，**登记缺口**：建议 coordinator 后补建单挂账，本 handoff 即交付凭证） |
| claim_type | `coordinator_dispatch`（父会话派单） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只修点名项，最短 diff；未用 YAGNI 跳过任何公约交付物（空态 reason/自检断言按诚实性铁律补齐） |

## 问题清单（评审原点名 → 修法）

### P1（Important）elements snapshot_id 契约缺口（快照回溯失效）

- **评审点**：`api/synth_elements_routes.py:31-38` 路由不声明 `snapshot_id`；`entan/synth_elements/pack.py:537-544` `build_elements_snapshot` 不接受。Java 已签契约传 `snapshot_id`（`RemoteSynthPythonClient.elementsBatchSnapshot` javadoc「snapshotId 入参直读该批」；`SynthElementsSnapshotService.batchSnapshot` 已在 query 放 `snapshot_id`），只读该批。
- **修法**：
  1. 路由加 `snapshot_id: str = ""`，透传 `build_elements_snapshot(..., snapshot_id=snapshot_id or None)`；
  2. `build_elements_snapshot` / `build_elements_result` 加 `snapshot_id` 参数；
  3. 批号解析：`snapshot_id.strip().rsplit("|", 1)[-1]`（`batch:…|{calc_batch_id}` 尾段），再剥 `snap:` 前缀（`snap:{calc_batch_id}`）——两形式都按批读；
  4. 读行豁免条件过滤：`_read_batch` 及 8 个读 helper（`_index_cell/_type_scores/_level_scores/_domain_scores/_lens_weights/_indicators/_contributions/_ranks`）加 `by_batch` 参数——批号全局唯一，回溯只按 `calc_batch_id(+metric_id/weight_profile 业务列)`，不按条件 4 列（**首跑实库自检抓到此缺口：SQL 仍带条件 4 列时非默认条件批读回空，已修并复跑全绿**，与 P2 vitality 同款语义）；
  5. 该批无行 → `compositeIndex=null` 全空态 + 新增 `batchReason=batch_not_published`（外壳同名字段 `batch_reason`），**不回落最新批**（对齐 collab `snapshot_id` 无映射不回落 / vitality 显式批号无行不回落语义）。
- **出参新增**：`result.batchReason` + 外壳 `batch_reason`（`None` 或 `"batch_not_published"`）；Java/FE 忽略多余键不破坏既有契约。

### P2（Important）vitality 按批装包用缺省条件过滤（非默认批必空壳）

- **评审点**：`api/synth_vitality_routes.py:227-244` `_ads_read`：requested 批号存在时仍按（深圳,全国重点城市,最近3年）条件过滤，非默认条件批按批读必空壳。
- **修法**：`_read_rows` 加 `by_batch` 参数；`_read_batch_result` 透传；`_ads_read` 中 `by_batch=bool(requested)`——requested 存在时 WHERE 收窄为 `calc_batch_id=%s AND weight_profile=%s AND calc_status='succeeded'`（批号全局唯一，不按条件过滤）；无 requested（最新批路由）行为不变。模块 docstring 同步该语义。

### P3（Important）`_publish_batch_meta` 幂等承诺与实现不符

- **评审点**：`entan/synth_collab/pack.py:247` docstring 说「snapshot_id 已存在 → 幂等跳过」，259-266 裸 INSERT——同 task 重试必撞 `uk(snapshot_id)` → rollback → 400（首次成功重试必败）。
- **修法**：插入前 `_meta_by_snapshot(conn, snapshot_id)` 命中即跳 INSERT（幂等跳过落地）；**保留后两条 UPDATE**（`is_latest=1` 指向本行 + 同 cache_key 旧行翻 0）——重试发布后改指必须正确；commit 语义不变；写失败仍 rollback 返回 None（拒绝 202）。

### P4（Important）seed 失败仍 commit

- **评审点**：`scripts/seed/seed_synth_elem.py:339-373` 与 `seed_synth_collab.py:151-184` 验证 `bad` 非空仍 commit。
- **修法**：两文件 apply() 验证段 `bad` 非空 → `conn.rollback()` + 输出 `rolled_back: true` + 返回 1；仅全绿才 commit。docstring 补「验证 bad 非空 → 整批回滚不发布（AR-6）」与行为对齐。

### M5（Minor）明文缺省库密码进 git

- **评审点**：seed 两文件 + check 两文件 `"GKX@Lumen2026"` 缺省。
- **修法**：四处改 `os.environ.get("<ENV>", "")` 缺省空串 + 无密码时打印原因 JSON 后 `sys.exit(2)`（seed）/ `sys.exit(2)`（check `_probe_conn`）。环境变量名按各文件既有约定：seed 用 `LUMEN_ALGO_MYSQL_PASSWORD`、`check_synth_collab` 用 `ENTAN_MYSQL_PASSWORD`、`check_synth_elements`/`check_synth_vitality` 用 `LUMEN_ALGO_MYSQL_PASSWORD`。
- **范围说明**：`conf/settings.yaml`、`conf/deploy/k8s/*.yaml`、`entan/institute/queries.py`、`polan/common/config.py` 等同密码出现点**不在评审点名清单内，不动**（扩范围；建议另开 chore 治理单统一收敛）。

### M7（Minor）`_read_batch_result` 判空含 ind_rows 但 created 兜底链漏 ind_rows

- **修法**：`(idx_rows or dim_rows or rank_rows)` → `(idx_rows or dim_rows or rank_rows or ind_rows)`；indicator-only 批不再 IndexError，created 正确兜底。

### M10（Minor）死代码

- `entan/synth_elements/pack.py:474` `computed_at` 赋值未用 → 删（`batchComputedAt` 用 `batch_created`，确认无人读）。
- `scripts/seed/seed_synth_elem.py:177-179` `_tail_city` → 评审判「残留」不准：实有 4 处调用（indicator/weight/contrib/rank 行构造）。**删包装函数、4 个调用点改直调 `_tail`**（行为逐字相同），效果等同消灭死代码且 diff 最小。

## 修改内容（文件清单）

| 文件 | 改动 |
|------|------|
| `vendor/entan-py/api/synth_elements_routes.py` | P1：路由加 `snapshot_id` 参数+透传；docstring 补契约 |
| `vendor/entan-py/entan/synth_elements/pack.py` | P1：`build_elements_snapshot/build_elements_result` 接 snapshot_id，尾段解析，`by_batch` 读行链（`_read_batch`+8 helper），无行空态 `batchReason`；M10：删 `computed_at` |
| `vendor/entan-py/api/synth_vitality_routes.py` | P2：`_read_rows/_read_batch_result/_ads_read` 加 `by_batch`，requested 收窄 WHERE；M7：created 兜底链补 `ind_rows`；docstring 同步 |
| `vendor/entan-py/entan/synth_collab/pack.py` | P3：`_publish_batch_meta` 插入前幂等命中跳 INSERT，保留两条 UPDATE |
| `scripts/seed/seed_synth_elem.py` | P4：bad 非空 rollback；M5：密码环境变量化+无密码退出；M10：删 `_tail_city`（4 调用点改 `_tail`）；docstring 对齐 |
| `scripts/seed/seed_synth_collab.py` | P4 + M5 同上 |
| `vendor/entan-py/scripts/check_synth_elements.py` | M5 + 新增 [8] 组 P1 断言（7 项） |
| `vendor/entan-py/scripts/check_synth_collab.py` | M5 + [4] 组追加 P3 幂等断言（3 项） |
| `vendor/entan-py/scripts/check_synth_vitality.py` | 新增 [5] 组 P2 门控探针断言（表可写才执行，缺密码/缺表 SKIP 不 FAIL；finally 保证清理） |

commit：`0bcfb71 fix(synth): 评审修复——elements快照回溯/按批读/批量发布幂等/seed回滚+密码治理 [agent:algorithm]`（9 files，+347/-95；**未 push**）

## 测试结果

> 环境：demo 库 10.50.11.76 可达（conf/settings.yaml host）。执行时间 2026-11-06 11:16–11:29。

1. **`python3 scripts/check_synth_elements.py`（`LUMEN_ALGO_MYSQL_PASSWORD` 注入）→ `{"ok": true, "passes": "all"}`，39 断言全绿**
   - 原 [1]–[7] 组 32 断言无回归（同构/四维空态/panorama 189116/running 批不读/202 包/入参 400/邻叶回归）；
   - 新 [8] 组 7 断言（实库探针批 `check_elem_snap_probe`=广州×最近1年×42.4242，自检后即清）：`batch:…|尾段` 按批读出数 42.4242 ✅、`snap:{batch}` 同批可读 ✅、无行批原样回显批号+指数 null+`batch_reason=batch_not_published` 不回落 ✅；
   - 首跑抓到「读行仍带条件过滤」缺口（见 P1 修法第 4 点）→ 修后复跑全绿。
2. **`python3 scripts/check_synth_collab.py`（`ENTAN_MYSQL_PASSWORD` 注入）→ `{"ok": true, "passes": "all"}`**：原全部断言无回归；新增 P3 幂等 3 断言实库验证：同 `task:check-tA` 二次发布 `status=succeeded` 不撞 uk ✅、`snapshot_id` 仍只 1 行 ✅、`is_latest` 仍 =1 ✅。
3. **`python3 scripts/check_synth_vitality.py` → `{"ok": true, "passes": "all"}`**：原 21 断言全绿（不回落/400/中间态语义无回归）；新增 [5] P2 探针因 `synth_vit_index` 表未建（VIT DDL 归数据侧，未落地）**优雅 SKIP**——断言本体已就位，VIT DDL 落地后即自动实跑。
4. **本地逻辑 harness（fake conn，17 断言全 PASS）**：P1 尾段解析/snap 前缀/无行不回落；P2 收窄 SQL（5 条读 SQL 均无 `region_code` 条件位）+snapshotId 同读+无行仍空壳；M7 indicator-only 批不 IndexError 且 created 兜底；P3 首/pub/重试 INSERT 恰 1 次、0 回滚、2 次 commit、`is_latest=1`。
5. **seed `--check`**：`seed_synth_elem.py` `{"ok": true, "tables": 8, 行数对齐}`；`seed_synth_collab.py` `{"ok": true, "seeded": 3, "empty": 7}`（删 `_tail_city` 后行构造逐字不变，行数断言佐证）。
6. **探针零残留**：自检后实查 `synth_elem_index/type_score/weight` `calc_batch_id LIKE 'check_%'` = 0；`synth_collab_batch_meta` `snapshot_id LIKE 'task:check%'` = 0。

## 不修清单（评审登记，后续 chore 单）

| 项 | 内容 | 原因 |
|----|------|------|
| M6 | relation_input 内存过滤 | 评审归类顺手不阻塞 |
| M8 | 同秒排序次级键 | 同上 |
| M9 | is_latest 唯一约束 | 同上 |
| M11 | 自检覆盖缺口 | 同上 |
| M12 | 条件归一三份重复 | 同上 |
| （新增登记） | 明文密码其余出现点（conf/settings*.yaml、conf/deploy/k8s/*.yaml、entan/institute/queries.py、polan/common/config.py） | 评审点名仅 seed/check 四文件；其余扩范围，建议另开 chore 统一收敛 |

## 架构合规自检（公约 §2 摘要）

| 铁律 | 结论 |
|------|------|
| 算法只在 Python | ✅ 全部改动在本仓 vendor/entan-py + scripts/seed |
| 调用链 FE→Java→Python `/internal/*` | ✅ P1 即补齐 Python internal 层对 Java 已签契约的承接，未越层 |
| 只读 ADS、缺行 null+reason 不补 0 | ✅ 回溯空态诚实 `batch_not_published`，无回落无编造 |
| snapshotId 不可变 | ✅ 回溯按批读强化该语义（elements 线补齐 collab/vitality 同款） |
| demo/lumen 隔离（D12） | ✅ 只写 demo_gkxlumenx_ads 探针行且自检后即清；不触碰正式库 |
| 密码不进 git | ✅ M5 后 seed/check 无明文缺省密码 |

## CI/CD（必填）

- 分支：`dev`（origin/dev 直推策略）
- commit：`0bcfb71`（**未 push**——按 2026-11-05 人工确认闸门，后端仓本单亦停本地待确认）
- pipeline URL / ID：未 push，无
- 部署 namespace / 镜像 tag：无（未 push）
- K8s rollout：未触发
- dev 测试 URL / 命令与结果：本机直跑三自检（见 §测试结果）

## 遗留风险

1. **registry 缺本单条目**：`task-query` 查无 `SYNTH-REVIEW-FIX-PY-L01`；建议 coordinator 补建单挂账（handoff 即凭证）。
2. **P2 实库断言待 VIT DDL**：`synth_vit_*` 表未建（数据侧并行线），`check_synth_vitality` [5] 现态优雅 SKIP；DDL 落地后建议跑一次全量自检确认 5 项探针断言实绿。
3. **P1 出参新增字段**：`result.batchReason`/外壳 `batch_reason` 为增量字段，Java `SynthElementsSnapshotService` 未消费（忽略多余键，不破坏）；若后续 Java 要把「回溯无行」映射为 404 语义，需在 Java 侧加判定（另单）。
4. **无行批 `_index_cell` 空 → `batchComputedAt=None`**：回溯无行时外壳 `computedAt=null`（诚实空态），FE 若直用该字段渲染时间需容 null（现有 FE 空态已容，风险低）。

## 涉及文件

- `vendor/entan-py/api/synth_elements_routes.py`
- `vendor/entan-py/api/synth_vitality_routes.py`
- `vendor/entan-py/entan/synth_elements/pack.py`
- `vendor/entan-py/entan/synth_collab/pack.py`
- `vendor/entan-py/scripts/check_synth_elements.py`
- `vendor/entan-py/scripts/check_synth_collab.py`
- `vendor/entan-py/scripts/check_synth_vitality.py`
- `scripts/seed/seed_synth_elem.py`
- `scripts/seed/seed_synth_collab.py`
