# POL-EFFECT-MACRO-FE-TOPIC-L01 · 落地实效宏观代理：lumen-ui-topic 深圳结果板接线

> 总控：[`POL-EFFECT-MACRO-长任务总控.md`](./POL-EFFECT-MACRO-长任务总控.md) §0.4 / §3 · 前序：[`POL-EFFECT-MACRO-JAVA-L01.md`](./POL-EFFECT-MACRO-JAVA-L01.md)（`effect.ext` 透传）· [`POL-EFFECT-MACRO-ALGO-L01.md`](./POL-EFFECT-MACRO-ALGO-L01.md)（ext 键真源）
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
| 说明 | 不新增组件、不加依赖：沿用结果板既有 `PendingBadge` / `MetricSpecCard` / `IndustryReviewOnly`；解析与派生函数加在既有 `policyShenzhenResult.ts`（报告 `policyBlockReportDocument.ts` 复用同一函数，不另写一份）。只新增 1 个行为自检 `policyShenzhenEffect.selfcheck.mjs`（Node 原生剥类型，无框架）。未跳过：D9 ⓘ/待确认角标、评审层零泄漏、诚实性（不写 0）。 |

## 范围与实现（对照 DoD）

| DoD | 实现 |
|---|---|
| `/policy/recommendation` 实效卡展示代理分；⚠️ 待甲方确认；`computable=false` 不编 0 | 结果板「落地实效性」卡读 `cards.effect.{computable,score,reason,ext}`。新增 `policySzEffectShown`：**只认 `computable===true` 且 score 为数值**。`computable=false` / score 为空 / 无 effect → 显示「不可算」+ `reason`，不出分。 |
| 评审 / metric ⓘ 不伪闭合正本三维 | ⓘ 仍挂 `M_POLICY_IMPLEMENTATION_EFFECT`（`MetricSpecCard`，评审层自闸）；宏观代理时标题旁加 `PendingBadge`（`QPOL-02`，hint 明说「不是启动率/兑现率/满意度、权重待甲方确认」）。正本三维一行文案：`not_computable` →「当前不可算，未并入本分」；`partial_gapfill` →「补空诊断分 x，仅作诊断，未并入本分」。**无综合分**。 |
| 范围 | 只改深圳结果板实效卡 + 同源仪表盘/报告/摘要行；**未改**支持力度/适配性公式与展示、配置区、Java/Python。 |

## ext 展示点

| `cards.effect.ext` 键 | 展示 | 评审层门控 |
|---|---|---|
| `caliber=macro_outcome_proxy` | 卡内常显「口径：宏观结果面代理，不等于政策启动率、兑现率或满意度（待甲方确认）」；非该 caliber 不出声明 | 否（业务诚实文案） |
| `indicator_count` | 「参与指标 N 项」 | 否 |
| `city_scores` | 四城截面分列表（仅 `computable=true`；值为 null 的城不显示、不补 0；真 0 保留） | 否 |
| `period_used` | 每城取数期区间「深圳 取数期 2024-09 至 2026-03（n 项）」+「各城取数期以最新一期为准，非同期比较」 | 否 |
| `proxy_notes` | 逐条展示（与「非同期」固定句同义者去重） | 否 |
| `track_a_status` / `track_a_score` | 见上「正本三维」一行 | 否 |
| `caliber` 原值 / `whitelist_version` / `window` / `source_tables` / `indicator_used` | 一行追溯信息 | **是**（`IndustryReviewOnly`，关评审模式 DOM 零泄漏） |

同步改动：
- 仪表盘「落地实效性」、`policyShenzhenFindingLines` 摘要行、导出报告 `policy-sz-effect` 块全部改用 `policySzEffectShown`；报告块追加口径声明 + `proxy_notes`（文本不含 `QPOL-02` / 键名，符合 D9 零泄漏）。
- **修一处隐患（与 Java 叶同源）**：原 `policySzShownScore` 把 `score===0` 当不可算；宏观截面 min-max 下最低城的真分就是 0，会被误显「不可算」。实效卡改用新函数，0 展示；**档位仍沿用旧函数**（档位 0 不展示，口径不变）。

## 五维复刻对齐（`fe-replica-visual-dod`）

| 维 | 结论 |
|---|---|
| 布局 | 沿用已评审深圳页三张固定卡网格，未增卡、未动仪表盘布局；实效卡内新增内容纵向堆叠于原卡内 |
| 交互 | 无新交互；角标沿用 Arco hover/键盘语义（`PendingBadge` 自带 `role=button tabindex=0`） |
| 样式 | 仅用既有 token（`--sci-text-*`、12px/18px 次级文案），无新颜色/组件 |
| 评审 | 技术键进 `IndustryReviewOnly`；⚠️ 角标走 `PendingBadge` 自闸 |
| Mock 开关 | `USE_MOCK=false` 零 fixture：解析全部来自 Java result，无 `@/mock/**` 填数；自检里的样例仅在 `.mjs` 自检内 |

## 偏离说明

1. **D4 语义**：本卡数据是真读真算（Java→Python→`gkx` 只读），**不是 mock**，故**未加 `MockBadge`**（D18 不适用；加了即谎报）。「待确认」语义由 `PendingBadge`（口径待甲方，QPOL-02）承担，不降级为 mock。
2. **指标库种子未登记**：`getMetricMeta('M_POLICY_IMPLEMENTATION_EFFECT')` 在本仓 mock 种子中不存在（同卡支持力度/适配性亦同），ⓘ 弹卡会显示「未入指标库」。属存量状态，非本叶引入；需 data-agent 正式化 8 件套后才有内容，未在前端手写（AGENTS D9 禁止）。
3. **未做截图 / 真实联调**：本机未起前后端，dev 环境 E0 尚未发布；`period_used`/`city_scores` 的真实形状按 ALGO/Java handoff 样例对齐，真数核对留给 E1。
4. `pnpm type-check` 在本机会触发 `pnpm install` 状态检查并改写 `pnpm-workspace.yaml`（`core-js`/`es5-ext` allowBuilds 提示，与本叶无关），故直接跑 `node_modules/.bin/vue-tsc --build`（与 `type-check` 脚本等价），误改的 `pnpm-workspace.yaml` 已 `git checkout` 还原，未入提交。

## 测试结果

| 项 | 结果 |
|---|---|
| `node_modules/.bin/vue-tsc --build`（= `pnpm type-check`） | 绿（exit 0；中途修复 1 处 `noUncheckedIndexedAccess` 报错） |
| `node src/views/policy/policyShenzhen.selfcheck.mjs`（既有 + 新增源码断言） | `policyShenzhen.selfcheck ok` |
| `node src/views/policy/policyShenzhenEffect.selfcheck.mjs`（新，行为自检，真实 import 解析器） | `policyShenzhenEffect.selfcheck ok`：ext 透传 / 城市分 null 不补 0、真 0 保留 / `computable=false` 带 0 不出分 / 空分与缺失不写 0 / 无 ext 与非宏观 caliber 不造声明 / 取数期区间 / 摘要行 |
| `node_modules/.bin/vite build`（= `build-only`） | ✓ built in 1m 4s（仅既有 chunk 体积告警） |

## 架构合规自检（00-team-constitution §2）

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 前端只展示，不算分 |
| 2 调用链 | ✅ 仍只读 Java `GET .../tasks/{id}/result`，无新请求 |
| 3 Nebula | ✅ 不涉及 |
| 4 可观测 | ✅ 沿用既有 `observability.ts`，无新增外部调用 |
| 5 CI/CD | ⏸ 未 push，待人工确认 |
| 6 demo2 只读 merge | ✅ 未 merge |
| 8 数据策略 | ✅ 无写死分、无 fixture |
| 9 D8 | ✅ Arco + 既有 token，无新依赖 |
| 10 D9 | ✅ ⓘ 保留；待确认角标；技术键评审门控、零泄漏；不写「已支持正本三维」 |
| 11 D10 | ✅ 无新交互；角标键盘可达沿用既有组件 |
| 12 D12 | ✅ 不涉及 demo-* |
| 14 D16 / 16 D18 | ✅ 不写 gapfill、不写死 mock |
| 15 D17 | ✅ 未触达锁定闭包 |

## CI/CD · 待推送

- 仓：`lumen-ui-topic`，分支 `dev`，commit **`112afa6`**（`feat(policy): 深圳结果板落地实效卡接 cards.effect.ext 宏观代理口径 [agent:frontend-agent]`）。
- ⏸ **只 commit 未 push**（`fe-manual-confirm-push`，总控 §0.9，派单未写「完工即推」）。**待当前会话用户人工确认后**执行 `git push origin dev`；push 触发 CI → K8s dev 自动 rollout。
- 推送后 E0（`POL-EFFECT-MACRO-E0-DEVOPS-L01`）才能点名 deploy；E0 另须确认 `lumen-algo-py` 可达 `gkx`（ALGO 遗留风险），否则金路径只出现「宏观源不可达」空态。

## 涉及文件（`lumen-ui-topic`）

- `src/utils/policyShenzhenResult.ts`（`PolicySzEffectExt` 类型、`parseEffectExt`、`policySzEffectShown`、`policySzEffectPeriodRows`、`policySzEffectNoteLines`、仪表盘/摘要行改用）
- `src/components/policy/PolicyShenzhenResultBoard.vue`（实效卡）
- `src/components/report/policyBlockReportDocument.ts`（报告实效块）
- `src/views/policy/policyShenzhen.selfcheck.mjs`（+断言）
- `src/views/policy/policyShenzhenEffect.selfcheck.mjs`（新）

## 下游放行建议

- 人工确认并 push 后 → E0 deploy → E1 金路径：`cards.effect.computable=true` 且 `ext` 含 `macro_outcome_proxy`、卡内出现「待甲方确认」与取数期声明；换对比城市分数随截面变化（`ext.city_scores` 列表）；`computable=false` 时无分数、无 0。
- E1 注意：真 0 分（截面最低城）现在会显示「分数 0」，不是空态。

## 问题清单 / 遗留风险

- 指标库种子无 `M_POLICY_IMPLEMENTATION_EFFECT`，ⓘ 弹卡内容为「未入指标库」（见偏离 2）。
- `city_scores` 只在结果板有；冻结快照不带，报告页/历史任务回看时城市分列表为空（不显示、不补 0）。
- 窗口内每城每指标仅 1–6 点、各城期次不齐，跨城可比性有限（卡内已声明非同期）。

## 成本（回填 registry）

| 字段 | 值 |
|---|---|
| actual_tokens | 约 120000 |
| model_used | claude-sonnet-5.5 |
| actual_cost | 0.9 |
| cost_warn | green |
