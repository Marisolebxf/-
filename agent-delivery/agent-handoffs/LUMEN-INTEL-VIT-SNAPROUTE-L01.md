# Handoff — LUMEN-INTEL-VIT-SNAPROUTE-L01（E1 C1 修单：活力快照读端点 + CI 止血）

- **执行**：agent:algorithm-agent（本会话）
- **监管人**：human:徐滕强（supervised_by；claimed_by=agent:algorithm-agent）
- **时间**：2026-11-06 00:20 – 00:50（UTC+8）
- **仓**：`lumen-algo-py`（分支 `dev`；commit `501f8fc`，**按派单不 push**）
- **ponytail**: full（只补路由层 + 挂载 + CI 一行；装包 `pack.py` 未动；elements/collab 两叶未动）

## 0. 结论速览

红项 1（E1 冒烟 #1/#2 根因）已修：`/internal/v1/synth/vitality/*` 两读端点挂载完成，自检 21 断言全绿，邻叶回归无损；`e2e:chain-gold` 悬空 trigger 一行止血（`allow_failure: true`）。待 deploy 绿后由 qa 只复测 #1/#2（E1 handoff §11.5.2）。

## 1. 复现 → 修复对照（E1 缺陷包 §3.1）

| E1 复现 | 修后行为 |
|---|---|
| `GET /internal/v1/synth/vitality/batch-snapshot?region=深圳市&compare=全国重点城市&window=最近3年` → **404 Not Found**；`/openapi.json` 98 条路由无 vitality 读端点 | **200** `{code:0, data:{snapshotId, cache_key, computedAt, methodVersion, weight_profile, calc_batch_id, batch_reason, result}}`；openapi 新增 2 条路由 |
| Java `RemoteSynthPythonClient` L27/L35 两 Feign 契约悬空 → `SNAPSHOT_NOT_FOUND` → FE no_batch | 路由名/参数/包络与 Feign 已签契约逐项对齐（见 §2） |

## 2. 实现说明（文件边界）

1. **新增 `vendor/entan-py/api/synth_vitality_routes.py`**（路由层自含，装包口径仍在 `entan.synth_vitality.pack`，不重写公式）：
   - `GET /internal/v1/synth/vitality/batch-snapshot`：参数 `region/compare/window[/weight_profile][/calc_batch_id][/snapshotId]`（`snapshotId` 与 `calc_batch_id` 同义合同参数，`snap:` 前缀剥除）。缺省 `weight_profile` 归一 `INDEX_MAIN`；非法档/窗/区域 → 400（复用 `VitalityJobRejected`）。读路径：`synth_vit_*` 五表同批同 profile 只读（`calc_batch_created_at` 排序禁字符串比大小；缺行 null+confidence 禁常量回填，L2-VIT §1）；无 ADS 批 → 走既有 compute 中间态兜底（`calc_batch_id=mock_vit_latest` + `batch_reason=batch_not_published`）；**显式批号无行 → 200 空壳 + `batch_reason`，不回落最新批/compute**（collab 同语义）。`snapshotId=snap:{calc_batch_id}` 不可变；`cache_key=region|compare|window|profile` 回显。
   - `GET /internal/v1/synth/vitality/latest-batch`：按 Java Feign 期望返回 `code=0 + data={calc_batch_id, computed_at}`（该条件最新 succeeded 批）；无批返回中间态兜底批号 `mock_vit_latest` + `reason=batch_not_published`（**不 404**——Feign 侧 catch 异常→null→`SNAPSHOT_NOT_FOUND`，会整链落空态而 FE 默认三元组应有数；兜底让链路走到 compute 快照）。
2. **`api/main.py` 挂载**：+8 行，对齐 elements/collab try/except 先例，失败不影响企业主路由。
3. **CI 止血**：`.gitlab-ci.yml` `e2e:chain-gold` 加 `allow_failure: true` + 注释（恢复条件：ui-topic 恢复 CHAIN_GOLD_ONLY 可执行 job 后总控撤销）。
4. **自检**：新增 `vendor/entan-py/scripts/check_synth_vitality.py`（`--check` 式无 pytest 依赖；不要求 DB 可达）。

## 3. 自检证据（本机实跑，2026-11-06 00:40）

`python3 scripts/check_synth_vitality.py`（`SYNTH_VIT_REPRO_DIR` 指向编排仓 repro/out）→ **`{"ok": true, "passes": "all"}`，21/21 PASS**：

- 端点 200：默认三元组 `深圳市|全国重点城市|最近3年` → 200，`snapshotId=snap:mock_vit_latest`、`cache_key=深圳市|全国重点城市|最近3年|INDEX_MAIN`、外壳七字段齐、`result.vitalityIndex/dimScores` 出数（compute 中间态；`batch_reason=batch_not_published` 显式标记）
- 入参拒绝 400：`weight_profile=index_main`（大小写敏感）→ 400；`window=10y` → 400；`region=火星` → 400；latest-batch 非法档 → 400
- 不回落语义：`calc_batch_id=check_never_batch`（无行）→ 200 + `snapshotId=snap:check_never_batch` + `batch_reason=batch_not_published` + 指数 null
- latest-batch：200 + `data.calc_batch_id`（无 ADS 批时 `mock_vit_latest`+reason）
- 邻叶回归：elements/collab 快照 200、`region=火星`/`window=10y` 400、jobs execute vitality 202 —— 全部无损
- 自检期间抓到并修掉 1 个真 bug（`_read_batch_result` cond 解包 3/4 元不一致），其余首跑即绿

## 4. 偏离说明

1. **无 ADS 批时 latest-batch 返回兜底批号而非「无批 404」**：派单允许二选一（「看 RemoteSynthPythonClient 怎么签的就怎么给」）。Java Feign 对非 0 包络/catch 异常统一归 null → `SNAPSHOT_NOT_FOUND`；若返回无批信号会让默认三元组（E1 判定应有数）落到 no_batch 空态。故按 Feign 的 `code=0 + data.calc_batch_id` 形状返回中间态兜底批号，装包自然走既有 compute 真算（D18 合规：非写死 mock）。`batch_reason`/`reason` 显式标记，seed 落地后自动退位。
2. **五表读路径暂放路由文件而非 `pack.py`**：`synth_vit_*` DDL/seed 尚未在仓内（归「装包读表改造」并行线），不动 `pack.py` 符合「只补路由」边界；并行线落地后读路径可并入 pack，接口不变。
3. **列名按 `synth_elem_*` 惯例**（`weight_value/dim_code/indicator_code/rank_city_code/value_num/rank_no`）：VIT DDL 未落，按 L2-VIT §2 与 elem 已落表惯例对齐；表未建时读路径按无批降级（`ponytail:` 注释标注天花板与升级路径=并行线落地后区分缺表与真故障）。
4. CI 止血用 `allow_failure: true` 而非 `when: never`：保留 trigger 链，ui-topic 侧恢复后无需改回 algo-py 配置。

## 5. 架构合规自检（公约 §2 摘要）

| 铁律 | 结论 |
|---|---|
| 算法只在 Python | ✅ 全在本仓路由/装包层 |
| 调用链 FE→Java→Python `/internal/*` | ✅ 本单就是补 Python internal 层；参数/包络与 Java Feign 已签契约对齐 |
| 数据策略（ADS 先行/不写死 mock） | ✅ 只读 `synth_vit_*`；无批走既有 compute 真算兜底；显式批号无行诚实空壳不回落 |
| D9 缺行语义 | ✅ 缺行 null+confidence+`batch_reason`；权重缺行禁常量回填 |
| 边界（不动 elements/collab/pack.py） | ✅ 邻叶回归无损 |
| commit 标注 | ✅ `[agent:algorithm]`；未 push（派单要求） |

## 6. 待办移交（coordinator）

1. push `501f8fc` → CI deploy 绿（E0）→ qa **只复测 #1/#2**（活力快照 + 任务链）。
2. 红项 2 依赖的本端点现已就绪：#2 的 live 202 受理 + succeeded + fp/legacy_unknown 断言可随复测执行。
3. `e2e:chain-gold`：金路径修好后按 `.gitlab-ci.yml` 注释恢复（撤销 `allow_failure` 由总控决定）。
4. 提醒并行线：`synth_vit_*` DDL/seed + 装包读表改造落地后，本路由读路径并入 pack、中间态兜底自动退位。

## 7. registry / cost

```yaml
ponytail: full
model_used: glm-5.3-Flash
estimated_tokens: 170000
actual_cost: 0.42
cost_warn: false
```

- registry 回填经 `task-update-fields`（evidence=本 handoff）；状态流转/AV-0 推进由 coordinator 执行。
- 多会话保护：`git status` 两个他人 `??` 文件（`scripts/mock_stage_health_scores.py`、`scripts/seed_supply_chain_relations.py`）未触碰；本单 4 文件单独 `git add` 提交。
