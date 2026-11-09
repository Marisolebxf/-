# POL-EFFECT-MACRO-MID-L01 · 落地实效宏观代理：算法中台展示与试算

> 总控：[`POL-EFFECT-MACRO-长任务总控.md`](./POL-EFFECT-MACRO-长任务总控.md) §0 · 前序：[`POL-EFFECT-MACRO-ALGO-L01.md`](./POL-EFFECT-MACRO-ALGO-L01.md)（`macro_effect_card` / `ext` 契约）· 读路径：`data/data-design/storage/POLICY/etl/pipeline-macro-effect-proxy.md`
> 日期：2026-11-09 · 类型：feature · Epic：`E-POLICY-PDR` · 故事：`US-E7-POL-04`

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用现有 `EffectEval` 页、`MetricHint`、`useGraceful`、`ErrorBanner`；新增 1 个组件 + 1 个纯函数 `.mjs`（含 node 自检），不加依赖。D9 ⓘ（MetricHint，`M_POLICY_IMPLEMENTATION_EFFECT`，warn+待确认）、D10 错误态/加载态均已交付，未用 YAGNI 跳过。 |

## 问题清单

- 总控 §3 金路径 #3：算法中台政策算法页须可见新口径说明 + 试算/结果，且非写死。
- demo 算法仓此前**没有任何路由**暴露 `macro_effect_card()`（ALGO 叶只写了模块，接线只在 lumen 结果板）。前端无来源可读，故须补一个薄路由。

## 修改内容

| 项 | 实现 |
|---|---|
| 页面 | 政策算法 → **效果评估**（`/policy/effect`，`EffectEval.vue`；「保障力」页同嵌）顶部新增「落地实效 · 宏观结果面代理（macro_outcome_proxy）」区块。 |
| 口径说明 | 白名单 `macro-eff-v1`、TB·DNLJ、四城截面 min-max 等权；**明确不等于启动率/兑现率/满意度**；正本三维缺数据仍「当前不可算」、不以 0 代替；各城取数期不对齐、非同期比较；⚠️「待甲方确认（QPOL-02）」tag + 分数旁 ⓘ。 |
| 试算/结果 | 进入页自动调 `GET /policy/v1/policy/effect/macro`，另有「重新试算」按钮。展示深圳试算分、四城分/参与指标数表、指标×城市「取数期」表、`proxy_notes`。**分数全部来自后端 card**（`macroView()` 只做形状转换，不造分）。 |
| 不可算 | `computable=false` / 缺 score / 请求失败 → 只显示 `reason` 警示条或 ErrorBanner，**不显示分数、不写 0**。 |
| D17 | ALGO 叶确认无冲突（未触达唐绍祖锁定闭包）：单名「落地实效性」+ 待确认说明，**不做 -合规/-合理 成对**，无副本包。`policyHelp.ts` effect 页「落地实效性」口径同步改写。 |
| 后端接线（跨仓，薄） | `demo-algo-ent-analysis/api/policy_routes.py` 新增 `GET /v1/policy/effect/macro` → `macro_effect_card()`，9 行；不改算法、不改锁定路由。经现有网关 `/policy/**` 前缀可达，无需新增网关路由。 |

## 测试结果

| 项 | 结果 |
|---|---|
| `node src/views/policy/components/effectMacro.selfcheck.mjs` | `effectMacro.selfcheck ok`（有分展示 / 三种不可算形态均 score=null） |
| `vite build`（demo-ui-system-test） | ✓ built in 45.29s |
| `python -m polan.eval.effect_macro`（demo-algo-ent-analysis） | `OK effect_macro self_check`；`api/policy_routes.py` ast 解析通过 |
| `pnpm build` | ⚠️ 本机 pnpm 触发依赖状态检查 `pnpm install` 失败（`allowBuilds` 审批提示，与本叶无关），改用 `node_modules/.bin/vite build` 直跑；pnpm 误生成的 `pnpm-workspace.yaml` 已删除。仓内无 `type-check` 脚本（无 vue-tsc）。 |
| 真实试算联调 | **未做**：新路由尚未 push/部署，本机未起 Python 服务；`gkx` 读库在本机不可达（self_check 中 `load failed` 为预期的不可达分支）。 |
| 截图 | **无**。路由未部署前页面只能看到「服务暂不可用」态，截图无意义；待路由随 CI 部署后由 E1 / 人工补（建议路径 `agent-delivery/agent-handoffs/政策模块-E7/screenshots/POL-EFFECT-MACRO-MID-L01-effect.png`）。 |

## 遗留风险

- **新路由依赖部署**：`demo-algo-ent-analysis` 需推送并 rollout 后，页面才有真数；且 demo 算法 Pod 须配 `GKX_ODS_MYSQL_*` 可达 `gkx`，否则页面显示 `宏观源不可达`（不写 0）。
- 路由挂在 demo 算法仓（该仓目前无结果板）；若后续要求中台直读 lumen 链路，须另开叶（D12：lumen 不得反向调 demo）。
- `INDICATOR_NAMES`（index_code→中文名）为前端静态展示映射，白名单换版（`macro-eff-v1`→`v2`）时需同步。
- 指标分跨城可比性有限、期次不对齐（ALGO 叶已列），页面已文字提示。
- 旧「落地实效」列（`ads.policy_effect.impl_effect` 受控代理）仍在下方表格保留，未改，二者口径并存，上方区块为现行可算路径。

## CI/CD

- 分支：`origin/dev`（**均未 push**）
- commit：`demo-ui-system-test` `41d757a`（前端，`fe-manual-confirm-push` 适用，**待人工确认后再推**）；`demo-algo-ent-analysis` `707edd0`（后端薄路由，本地 commit，未推——推送会触发该仓 CI→K8s dev，需监管人定夺并建议与前端同批推送）
- pipeline / K8s：未触发
- dev 测试：见上

## 涉及文件

- `demo-ui-system-test/src/views/policy/components/EffectMacroProxy.vue`（新）
- `demo-ui-system-test/src/views/policy/components/effectMacro.mjs`（新）
- `demo-ui-system-test/src/views/policy/components/effectMacro.selfcheck.mjs`（新）
- `demo-ui-system-test/src/views/policy/components/EffectEval.vue`
- `demo-ui-system-test/src/views/policy/components/policyHelp.ts`
- `demo-ui-system-test/src/api/policy/index.ts`（`fetchEffectMacro`）
- `demo-algo-ent-analysis/api/policy_routes.py`（`GET /v1/policy/effect/macro`）

## 架构合规自检（00-team-constitution §2）

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 前端不算分；路由只调既有 Python 函数 |
| 2 调用链 | ✅ demo 中台沿用既有 `/policy/v1/**` 网关→Python 范式（与同页其余接口一致） |
| 3 Nebula | ✅ 不涉及 |
| 4 可观测 | ✅ 后端沿用 `policy.effect_macro.*` span；前端沿用 `request.ts` traceId + ErrorBanner |
| 5 CI/CD | ⏸ 待推送 |
| 6 demo 只读 merge | ✅ 未 merge 进 lumen |
| 8 数据策略 | ✅ 真读真算，无写死分 |
| 9 D8 | ✅ Element Plus（本仓栈）+ 沿用本仓 token 与组件 |
| 10 D9 | ✅ 分数旁 ⓘ + warn + 待确认；metric_id 不变 |
| 11 D10 | ✅ 加载/错误/不可算态覆盖，按钮可键盘操作（原生 el-button） |
| 12 D12 | ✅ demo 仓内闭环，不触 lumen |
| 14 D16 / 16 D18 | ✅ 不写 gapfill、不新增 mock 表 |
| 15 D17 | ✅ 无冲突，单名 + 待确认说明 |

## 成本

| 字段 | 值 |
|---|---|
| actual_tokens | 约 110000 |
| model_used | claude-sonnet-5.5 |
| actual_cost | 0.8 |
| cost_warn | green |
