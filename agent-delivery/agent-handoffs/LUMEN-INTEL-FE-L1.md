# LUMEN-INTEL-FE-L1 · handoff

## 认领信息

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| repo / branch | `repos/lumen-ui-topic` · `dev`（改动停本地，走查通过后再推） |
| ponytail | `full` |

## 范围与实现（DoD 对照）

总纲 `API-SYNTH-INTEL-REPLICA-PLAN.md` §1（共享上下文）/ §2.3（跑批快照 mock 面）/ D9 种子。

| DoD | 交付 |
|---|---|
| `composables/useSynthCtx.ts`：URL>localStorage>默认；windowToUrl 映射；storage key 对齐 demo | ✅ 语义移植 demo `synthCtx.ts`（`topic-synth-workbench` / 默认三元组 深圳×全国重点城市×最近3年 / 1y/3y/5y 双向映射 / compare 兼容旧 key）+ Vue 版 `useSynthCtx()`：route.query 真源、`setCtx` replace 回写 URL 并保留无关参数、watch 持久化；`synthCtxFingerprint` = `region\|compare\|window`（#102 analysis_fp 同构） |
| `mock/intel/` 三叶确定性数据 + synthReadinessSeed 只读镜像 + metricSeed 扩 SYNTH 段 | ✅ 6 个新文件：`vitalityMock.ts`（四维/12 指标/排名/趋势/task 按 region.length 推导）、`elementMock.ts`（七要素/三透镜/四维评分/贡献路径=演示关联权重）、`collabMock.ts`（图谱 7 节点 6 边/集群/孤立主体/Pearson 关联，**COLLAB_CORR_SERIES 12 点随迁**：sz5/bj5/sh2）、`intelMetricSeed.ts`（21 条 8 件套，def_status 逐字对齐 demo）、`synthReadinessSeed.ts`（21 条四维；missing→D2~D4=n/a，头注释注明矩阵真源待 data-agent 登记）、`intelBatchApi.ts`。接线：`getMetricMeta`/`getMetricReadiness` 尾挂 SYNTH 段 |
| `mock/register.ts` 统一注册；USE_MOCK=false 不注册；跑批快照仅默认三元组返回、其余 404 | ✅ `registerApiMock('synthVitalityBatch'/'synthElementBatch'/'synthCollabBatch')` 三键；`IntelBatchSnapshotNotFound`(status=404)；registerAllMocks 仅在 USE_MOCK 时被调用（http.ts 既有机制），mock 数据零 fixture 填数 |

诚实态（任务 note 要求）：Q-SYNTH-01/02/03/V-01/E-01/E-02/C-01/C-02/C-03 治理引用逐字保留（selfcheck 断言锁定）；TEMP_WEIGHTS ⚠️待甲方确认；gradeNote 带「演示态」；协同禁「密度×强度」权威化、关联散点非因果、样本<3 不出系数（sh 序列 2 点 → insufficient 演示路径保留）；集群 score=null 不伪造权威分。**无任何就绪度改绿**（missing 条目 D2~D4 全 n/a）。

## 产物清单（lumen-ui-topic，本地未提交）

新增：
- `src/composables/useSynthCtx.ts`（~190 行）
- `src/mock/intel/vitalityMock.ts` / `elementMock.ts` / `collabMock.ts`
- `src/mock/intel/intelMetricSeed.ts` / `synthReadinessSeed.ts` / `intelBatchApi.ts`
- `src/mock/intel/intel.selfcheck.mjs`

修改：
- `src/mock/enterprise/metricSeed.ts`（+2 行：import + fallback 链）
- `src/mock/enterprise/readinessSeed.ts`（+2 行：同上）
- `src/mock/register.ts`（+6 行：import + 三键注册）

## 验收证据

- `node src/mock/intel/intel.selfcheck.mjs` → `intel.selfcheck L1 ok`（上下文契约/五阶段互斥/治理引用/D1 一致性 seed↔readiness/404 契约/确定性禁随机数，共 40+ 断言）
- `node src/router/menu.selfcheck.mjs` → 三段全绿（无回归）
- `pnpm type-check` → exit 0；`pnpm build` → ✓ 18.99s
- `pnpm lint` → 新文件 0 错误（仓内存量 64 错误与本次无关，如 `servicePortalIndustryScope.ts` `_chainQuery` 未使用）

## 架构合规自检（公约 §2）

| # | 铁律 | 结论 |
|---|------|------|
| D9 | 指标血缘 | ✅ 8 件套 + 四维就绪度只读镜像；missing 不出伪 8 件套；矩阵真源头注释注明（SYNTH 矩阵待 data-agent 登记，登记后同步） |
| D12 | demo 隔离 | ✅ 纯数据移植，无 demo import；确定性推导无随机数 |
| Mock 纪律 | USE_MOCK=false | ✅ registerAllMocks 机制保证不注册、无填数 |
| §4.2 | push 纪律 | ✅ 停本地待走查 |

## 开放项

- `metric-readiness-matrix-SYNTH.yaml` 未登记（data-agent 职责）；镜像头注释已注明，矩阵到位后按 D1–D4 同步
- L1B（任务中心扩展：AnalysisType +6 键、SSE 五阶段文案、任务桥）依赖本单走查通过后开工

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | ~85k |
| model_used | glm-5.3 |
| actual_cost | ~$2.2 |
| cost_warn | false |
