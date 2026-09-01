# 派单厚包 · 企业灌数据补「重灌」(对照政策)

```yaml
---
doc_id: ALGO-LIB-SEED-RELOAD-ENT-L01-WORKPACK
task_id: ALGO-LIB-SEED-RELOAD-ENT-L01
dispatcher: agent:coordinator-agent
supervised_by: human:徐滕强
date: 2026-09-01
claim_type: coordinator_dispatch
status: claimed
---
```

> 调度者只建单、写厚包、给 `/goal`。**不写业务代码。**  
> 执行真源=本厚包 + registry DoD。政策页是金标准，禁止另发明第四档。

## 1. 为什么派

政策基础指标页（`#/policy/basic`）「灌数据」已是三档：

| 档 | mode | 语义 |
|---|---|---|
| 追加 | `append` | 读 ODS 增量差集入 DWD，不清贴源 |
| **重灌** | `reload` | **保留 ODS，只清 DWD，再全量 ODS→DWD 并重算 ADS** |
| 重建 | `replace` | 清 ODS+DWD，再内存造底数 |

企业 / 产业链 / 产业服务基础指标页目前只有 **追加 + 重建**。三方贴源进 ODS 之后，没有「不动 ODS、只重算 DWD/ADS」的入口——政策圈出的就是这一档。

本叶只做 **企业**。产业链 / 产业服务另开叶。产业综合无独立贴源，不做。创新监测无同构基础指标灌数页，暂不做。

**本叶不含** 政策页右侧的「数据同步」（三方 `gkx` → Demo ODS）。那是另一条链路。

## 2. 金标准（政策 as-built，照抄语义）

| 层 | 政策现网 | 企业本叶应对齐 |
|---|---|---|
| UI | `demo-ui-system-test/src/views/policy/pages/BasicPage.vue` 下拉第二项 `command="reload"` | `src/views/entan/pages/BasicPage.vue` 同样位置加一项 |
| 确认框 | 「保留 ODS，只清 DWD，全量映入并重算；不写 Nebula」 | 同语义，换成企业表名 |
| API | `POST /policy/internal/policy/run-pipeline` `{mode: append\|reload\|replace}` | `POST /entan/internal/run-pipeline` 必须接受 `reload` |
| 贴源 | `polan/mockgen/incr.py#reload_from_ods`：TRUNCATE `policy_base_info`，再 `ingest_pending()` 全量差集（DWD 已空 → 等于全量） | `entan/llm_ods/seed.py`：不清 ODS、不 `write_rows` 造数；`apply_ods_to_dwd(..., replace=True)` 清企业 DWD 后按现有 ODS 全量映射 |
| 流水线 | `run_all_policy.build_steps(mode)` 三档都走 | `scripts/run_all.py` **现网把非 replace 一律折成 append**（`run()` L65），必须改掉 |
| 图 | 灌数零调用 NER/RE/Nebula | 同样：重灌后图空或保持旧图都合法；图只走企业图谱 A/B/C |

政策实现要点（只读对照，禁止复制政策表名到企业）：

```text
reload_from_ods:
  1. live 面禁止
  2. TRUNCATE demo DWD.policy_base_info
  3. ingest_pending() 把 ODS 现有行映入 DWD
  4. 不碰 Nebula
随后 run_all_policy 重算 A/C/D ADS（不含图谱）
```

## 3. 企业现网缺口（必须改）

| 文件 | 现状 | 本叶 |
|---|---|---|
| `entan/llm_ods/seed.py` | 只认 `append\|replace`；replace 会 `write_rows(..., truncate=True)` **清 ODS 再造数** | 增 `reload`：跳过造数，只 `apply_ods_to_dwd(replace=True)` |
| `scripts/run_all.py` `run()` | `mode = "replace" if mode == "replace" else "append"` | 三档原样下传；`build_steps` 标签加「重灌」 |
| `api/main.py` `/internal/run-pipeline` | `payload.mode in ("append", "replace")` | 接受 `reload` |
| `entan/pages/BasicPage.vue` | 下拉两项 | 中间加「重灌」+ 确认文案 + SeedHelpBadge 一句 |

`apply_ods_to_dwd(replace=True)` 已是「先 TRUNCATE 目标 DWD 再按 ODS 灌」。reload 应复用它，不要另写一套 TRUNCATE 列表。

## 4. 硬闸

1. **只写 Demo**：`demo_gkxlumenx_ods / _dwd / _ads`。正式 `gkxlumenx_*` 禁止。顶栏「企业」= live 时按钮禁用（现网已有）。
2. **重灌不清 ODS**：`dwd_org_*` 等 P0 贴源行数重灌前后必须一致（允许映射列补齐，禁止整表 TRUNCATE ODS）。
3. **重灌不内存造数**：禁止走 `orgs_for_batch` / `build_seed_rows` / `write_rows`。
4. **图谱剥离**：`run_all` / `run-pipeline` / 本页灌数 **grep 不到** graph / nebula / entity NER-RE 调用。真源：`COORD-GRAPH-TRIPLE-UI-DISPATCH-20260831.md` §0.1。
5. **追加 / 重建语义不得被改坏**：append 仍只补新 `org_id`；replace 仍清 ODS+DWD 再造底数。
6. **禁止** 本叶做三方「数据同步」、禁止改 lumen 正式仓、禁止 merge demo→lumen。

## 5. UI 文案（照政策句式，换企业词）

下拉顺序固定：

1. 追加（默认，不清空贴源）
2. **重灌（保留 ODS，只清 DWD 并重算基础指标）**
3. 重建（先清空再灌）← 保持 `divided`

确认框：

> 将保留 ODS 全部贴源，只清空企业 DWD（`enterprise_*` 等映射表），再把现有 ODS 全量映入 DWD 并重算基础指标 / 技商力 / 深度 ADS。不写 Nebula、不建企业图谱。是否继续？

SeedHelpBadge 补一句：重灌不清 ODS、不造数、不建图。

## 6. 验收

1. Demo 企业基础指标页下拉可见三档；正式面禁用。
2. 对已有 ODS 点「重灌」：ODS 行数不变；DWD `enterprise_base` 按现有 ODS 重映；ADS 基础指标可刷新。
3. 点「追加」在无新 `org_id` 时行为与现网一致（不误走 reload）。
4. 点「重建」仍会清 ODS（与重灌可区分）。
5. handoff 附：三档对照表 + 重灌前后 ODS/DWD/ADS 行数 + `grep` 灌数路径无 nebula/graph。

## 7. 并行 / 后续叶

| ID | 域 | 监管人 | 备注 |
|---|---|---|---|
| `ALGO-LIB-SEED-RELOAD-CHAIN-L01` | 产业链 | 李伟 | 已建；仓 `demo-algo-science`，与本叶并行 |
| `ALGO-LIB-SEED-RELOAD-SVC-L01` | 产业服务 | 未建 | 现网「重建」已不清 ODS，需先对齐三档命名再补 reload |

## 8. /goal 监管人

已确认 `supervised_by: human:徐滕强`。`claimed_by: agent:algorithm-agent`，`claim_type: coordinator_dispatch`。
