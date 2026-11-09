# POL-IMPL-EFFECT-MOCK-VIA-UI-L01 · 落地实效缺项：挂进算法库页两入口

详设依据：[05.6.2 §3.1](../产品整体定义/科技专题服务系统-完整详细设计/05.6.2-深圳政策现状分析.md)（已按 as-built 修订）；存储索引 `data/data-design/storage/POLICY/stores/README.md`。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人 2026-11-09 授权 mock/造数。状态停在待签收，不改为 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 `upsert_effects` 与 `_attach`，只加一个回补函数和一个注入口；无新依赖、无旁路按钮。自检用注入函数，不碰库。未删 D16 边界。 |

## 范围与实现

问题（查实库 + 读码）：

1. `run_real` 只给「LLM 成功的组」写 effect；LLM 解析失败的组（线上 4 组 `JSONDecodeError`）会没有 effect。
2. 真实政策都已补过外围时 `run_real` 直接返回，存量「已补」缺 effect 的无修复路径。
3. 建表只 `CREATE TABLE IF NOT EXISTS`，未抽成统一入口。

修改（`demo-algo-ent-analysis` 与 `lumen-algo-py/vendor/entan-py` 同文）：

- `polan/mockgen/effect_gapfill.py`：新增 `ensure_table`（只建表，不 `CREATE DATABASE`，与 `test_no_create_database` 口径一致）、`backfill_missing`（DWD 缺 effect 的政策 UPSERT 一行，只写 `gapfill_`）；自检带 FakeConn 断言。
- `polan/mockgen/synth.py`：`_attach(effect_recs=…)`；`run_real` 传全部挑中政策；两入口末尾 `_effect_fix`（调 `_backfill_effects`）；全部已补时也回补；写入后触发汇总重算；注入口 `effect_fn` / `effect_fix_fn`，自检覆盖两入口。
- 响应 JSON `effect_rows` = 本次写入 + 回补。
- 不改按钮文案条数、不改 FE、不复开 `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-DATA`。

## 偏离说明（as-built vs 派单）

- 派单写「无结构则 CREATE 库表」：库 `gkxlumenx_gapfill` 在线上已存在且应用路径禁止建库，故只建表。已写入 05.6.2 §3.1。
- 05.6.2 §3.1 / stores README 原稿只写「对当次政策 UPSERT」；as-built 增加「挑中全部」「回补缺口」「全部已补时也回补」，已修订。

## 验收证据（实库 `10.50.11.76`，`gkxlumenx_gapfill.gapfill_policy_sz_effect`）

表已存在，故本次未触发建表；建表路径由自检覆盖。口令未打印。

### 前（BEFORE，改码前）

| 指标 | 值 |
|---|---|
| effect 行数 | 20141 |
| DWD `policy_base_info` 行数 | 20141 |
| DWD 缺 effect | 0 |
| 真实已补外围（214，非 SYN） | 79 |
| 其中缺 effect | 0 |
| 合成行 / 缺 effect | 133 / 0 |
| 坏行（分数越界、空对象、空日期、空元数据） | 0 |

为验证存量修复路径，人工删除 3 条「已补」真实政策的 effect 行（仅 gapfill 表）：`18359198`、`18359201`、`18359235`。

```sql
DELETE FROM gkxlumenx_gapfill.gapfill_policy_sz_effect WHERE policy_id IN ('18359198','18359201','18359235');  -- 删 3 行
-- 此后：effect=20138，DWD 缺 effect=3，已补缺 effect=3
```

### 入口②「真实政策补外围」`POST /api/policy/v1/policy/mock/periphery {"count":50}`

线上返回（节选）：`job=real status=partial picked=50 history_versions=15 detail_rows=30 feedback_rows=110 effect_rows=68 errors=[periphery:JSONDecodeError ×4]`。

`68 = 50（挑中，含 LLM 失败组）+ 15（历史版）+ 3（存量缺口回补）`。外围 LLM 有 4 组 JSON 解析失败（`detail_rows` 只有 30），effect 仍全部写入，证明不依赖 LLM。

```sql
SELECT COUNT(*) FROM gkxlumenx_gapfill.gapfill_policy_sz_effect;                 -- 20138 → 20156
SELECT COUNT(*) FROM demo_gkxlumenx_dwd.policy_base_info p WHERE NOT EXISTS (
  SELECT 1 FROM gkxlumenx_gapfill.gapfill_policy_sz_effect e
  WHERE e.policy_id=p.policy_id COLLATE utf8mb4_unicode_ci);                     -- 3 → 0
-- 已补外围缺 effect：3 → 0；real_done 79 → 109；DWD 20141 → 20156（+15 历史版）
```

### 入口①「Mock 10 条数据」`POST /api/policy/v1/policy/mock/synth {"count":10}`

线上返回：`job=synth status=partial requested=10 ingested=9 history_versions=4 detail_rows=9 feedback_rows=33 effect_rows=13`（1 条 LLM 未成稿，不造行）。`13 = 9 新政策 + 4 历史版`。

```sql
SELECT COUNT(*) FROM gkxlumenx_gapfill.gapfill_policy_sz_effect;                 -- 20156 → 20169
-- DWD 20156 → 20169（+9 +4）；DWD 缺 effect = 0；合成行 148 → 161，缺 effect = 0
-- 本次 13 行：implementation_date > publish_date = 13，= publish_date = 0
```

### 终态

| 指标 | 值 |
|---|---|
| effect 行数 = DWD 行数 | 20169 = 20169 |
| DWD 缺 effect | 0 |
| 已补外围缺 effect | 0 |
| 坏行 | 0 |
| 批次 | `…EFFECT-GAPFILL` 20058；`…EFFECT-SYNTH` 111 |
| 样例（`SYN202611094b92333dac`） | 2026-08-30 / 企业 / 4 / `M_POLICY_IMPLEMENTATION_EFFECT` / `落地执行启动,受益覆盖,实施反馈` / `rule` / `…EFFECT-SYNTH` / 2026-11-09 11:07:57 |

### 自检

- 两仓 `python -c "from polan.mockgen import effect_gapfill, synth; effect_gapfill.self_check(); synth.self_check()"` 均 `policy synth self_check OK`。
- 新增断言：入口① 15 个 effect id = 新政策 + 旧版；入口② LLM 全失败仍写 10 条；全部已补时 `effect_rows=3` 且触发重算。

## 产物清单

- demo-algo-ent-analysis `dev`：`6576c58`、`a46dace`
- lumen-algo-py `dev`（vendor/entan-py）：`d90bb52`、`ce80898`
- 编排仓：本 handoff、`05.6.2-深圳政策现状分析.md` §3 / §3.1、`stores/README.md` 写入口句

## CI/CD

- 分支均 `origin/dev`。demo 仓 CI 热更新 `demo-platform-*`；线上 `10.50.69.111:30889` 在推送后约 10 分钟内已运行新逻辑（上述 `effect_rows=68` 含存量回补 3，旧逻辑不会产出该值）。
- 未打开流水线页面；K8s rollout 以行为核对。`lumen-algo-py` 副本同文，线上 lumen 侧未单独触发。

## 架构合规自检

| 条目 | 结果 |
|---|---|
| 算法只在 Python | ✅ 改动全在 Python |
| 调用链 前端→Java→Python | ✅ 本单只动 Python 算法库，入口为既有 UI 按钮 |
| Nebula 协议 | ✅ 不涉及图 |
| D12 demo/lumen 隔离 | ✅ 两仓同文，未让 lumen 调 demo |
| D16 缺项只进 `gapfill_` | ✅ 只写 `gkxlumenx_gapfill.gapfill_policy_sz_effect`；不写 ODS / 正式 DWD / ADS / 供应方库 |
| 不写 0 / 零日期 / 抄发布日 | ✅ 实施日 > 发布日（13/13）；评分 1–5；坏行 0 |
| D4 | 仍 mock，本单不改矩阵 |

## 遗留风险

- 合成与补外围的 DWD 写入沿用 2026-11-07 淮政玮批准的 D16 例外（写 `demo_gkxlumenx_*`），未变。
- 外围 LLM 偶发 JSON 解析失败（本次 4 组），`status=partial`；effect 不受影响，其余外围表要再点一次补。
- Mock 与补外围为线上真跑：新增 `SYN` 9 条 + 历史版 4 条，真实政策外围补 30 条 214、110 条 210。「删除所有 Mock」按标记可清。
- `backfill_missing` 为逐行 UPSERT；缺口达数万行时请用 `lumen-algo-py/scripts/seed_gapfill_policy_sz_effect.py` 批量。
- 3 条人工删除的 effect 行已由入口②回补（批次 `…EFFECT-SYNTH`）。

## 成本（会话估算）

| 字段 | 值 |
|---|---|
| actual_tokens | 160000 |
| model_used | claude-sonnet-5.5 |
| actual_cost | 2.5 |
| cost_warn | green |
