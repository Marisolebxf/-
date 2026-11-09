# POL-PC1-CASE-FILL-FE · handoff

- **任务**：POL-PC1-CASE-FILL-FE（602 治理页清洗 Tab · 政策选择器 + 质量明细接真）
- **执行**：agent:frontend ｜ **监管人**：human:淮政玮 ｜ **日期**：2026-11-09
- **claim_type**：coordinator_dispatch
- **ponytail**: full（复用既有 watch 链路与映射模式，不新增组件/依赖/写按钮）
- **仓**：`repos/lumen-ui-science-pc`（分支 dev；**改动停本地工作区，未 commit 未 push**，待人工确认）

## 改动文件（仅 2 个，工作区其他会话未提交改动未触碰）

| 文件 | 改动 |
|---|---|
| `src/api/policy.ts`（fetchGovernanceLive） | ① policyOptions 优先读 `results.policyOptions`，为空回退 lineage+indicator 合并；② `governanceBatches` 由恒空数组改为映射 `results.qualityAgg` |
| `src/views/policy/governance/index.vue` | ① showPolicyPicker 加 `'clean'`；② 清洗 Tab 批次表改绑 `cleanBatches` computed（live 优先、baseReady 开关回落种子）；③ 批次状态槽支持 failed；④ 口径文案 |

## 字段映射（以 Java 返回为准，兼容驼峰/蛇形）

### policyOptions（api 层）

- 优先：`results.policyOptions[]`（api-agent 叶新加，元素含 `id/title`，限 200）→ `{ id, title, level: '—', region: '—', dept: '—' }`；id 兼容 `policy_id`、title 兼容 `policy_title`。
- 回退：空数组时维持原 lineage-index + indicator-library 合并去重逻辑（行为不变，老后端不受影响）。

### 清洗批次（governanceBatches ← results.qualityAgg，字段 `job,status,row_count`）

| 页面列 | live 映射 | 种子字段 |
|---|---|---|
| 批次 | `job`（回退 `batch_id`、`批次N`） | `batch` |
| 规则命中 | `row_count`（缺省 0，不造假分数） | `ruleHits` |
| 失败样例（脱敏） | `note`（回退 `fail_samples`、`—`） | `failSamples` |
| 更新时间 | `updated_at`（回退 `—`） | `updatedAt` |
| 状态 | `status`：success→成功(绿) / failed→失败(红) / 其他(skipped 等)→部分(金) | `status` |

`results.qualityDetails`（`job,policy_id,status,batch_id,tried_at,try_count,note`）已由 api 层读入 `detailRows`；当前页面批次表消费的是 `qualityAgg` 汇总行，明细列如后续要展开再消费 `qualityDetails`，本叶未加新 UI（ponytail：不加没被要求的表）。

### 页面 cleanBatches 显隐口径（诚实态）

- live 有行 → 直接展示后端行；**无行时空表**，不伪造批次。
- mock（USE_MOCK=true）→ dataset 自带种子 3 行；底座就绪演示开关关闭时也置空（与 KPI 降档演示口径一致）。

## 与算法中台口径对照（只借口径不借代码）

- 口径真源：`demo-ui-system-test/src/views/policy/pages/PolicyMockPage.vue` 的 `MOCK_JOBS`/`DERIVED`——「按现有政策流水线顺序**重算 10 步汇总**：基础指标…、焦点、力度、效果、短板、机遇、布局、DS-07 组合、匹配、推演」；行状态「**待追加 → 已入库**」。
- 本页落地：批次卡 extra 文案改为「作业状态只读 · **待追加 → 入仓 → 重算 10 步汇总**」（用户拍板的过程口径）；页面保持**只读**，未加任何写按钮 / 触发动作；业务标题与 DS-PC-01 评审文案零改动。
- job 名（去重合并/格式标准化/噪声过滤/完整性校验/一致性校验/准确性校验/采集接入）与 DATA 叶灌入 `script_state.job` 的中文规则名同源，即页面「清洗规则与校验」6 规则 + 批次明细标题，前端无需再映射一层。

## 联调链路确认

- 选政策 → `watch(selectedPolicyId)` → `loadGovernance(id)`（既有链路，未改）；清洗 Tab 现在也受同一选择器驱动，`results` 带 `policyId` 请求，`qualityAgg`/`qualityDetails` 即该政策过滤后的行（后端已支持）。
- 与 DATA 叶（POL-PC1-CASE-FILL-DATA）灌数对齐：demo 库 `script_state` 19 行（3 政策 × 7 job），policy_id = 18318861 / 18319069 / 18319394，选这三个政策应见批次行；policyOptions 后端口就绪前由 gapfill lineage/indicator 回退提供同样 3 个候选。

## 自检证据

- `vue-tsc --build`（等价 `pnpm type-check`）**EXIT=0，0 error**。
  （注：本仓 `pnpm-workspace.yaml` 被并行改动暂缺 `packages` 字段，`pnpm run` 被工作区解析阻塞，故直调仓内 `node_modules/.bin/vue-tsc.cmd --build`；脚本本体未动。）
- `git status --porcelain` 限 `src/api/policy.ts` + `src/views/policy/governance/index.vue` 两个 M，无其他文件被扫入。

## 架构合规自检

- 调用链 ✅ 只打 `/display/v1/policy/governance/**`（Java REST），不越层。
- D9/D12 ✅ 不自填就绪度；live 无行诚实空，无伪 8 件套；未动 mock 种子语义。
- 只读 ✅ 无写按钮、无 POST/PUT/DELETE；演示态语义（baseReady 开关）保持。
- 边界 ✅ 未触碰其他会话未提交改动（IndustrySelect / .env.development）。
