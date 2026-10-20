# FE-TOPIC-SVC-REC-ALIGN-L02｜招引/培育推荐分析页对齐 demo 定点（内置固定权重）

> 仓库：`lumen-ui-topic`（`dev`）· 执行：`agent:frontend` · 日期：2026-10-20
> 触发：用户指着 `svc-rec-analysis-config` / `svc-rec-cultivate-config` 两个面板指出「功能、布局、样式完全对齐原型 demo 站」。

## 1. 差异根因

demo 原型 2026-08-10 评审定点（`demo-ui-topic` commit `afd6583`，《符合度评估-产业服务链-三页定点.md》偏离-1，TOPIC-SVCCHAIN-ALIGN-L01）**去掉了招引/培育模型的自定义权重 UI，改为内置固定权重 Tag**。lumen 10 月复刻时跟的是更早的 USM v1.0-r3 可调权重版，配置区仍是「InputNumber 网格 + 权重合计条 + 按比例归一/恢复默认」，与已评审 demo 不一致。

## 2. 改动清单（demo 定点 → lumen）

| 点 | demo 定点后 | lumen 本次对齐 |
|----|------------|---------------|
| 招引模型区 | `.svc-fixed-weights` 固定权重 Tag（35/30/20/15）+ 指标说明入 Tag tooltip + footer 说明 + 主 CTA | `svc-rec-fixed-weights`（Tag tooltip=指标描述）+ `svc-rec-eval-footer`（演示口径 + 开始/重新分析）；删 InputNumber 网格、权重合计条、归一/恢复默认 |
| 培育模型区 | 同上（25/30/25/20）；筛选（机构类型/服务环节）保留 | 同左；筛选行、全空禁用、blocker 提示保留 |
| 结果区 stale 提示 | 固定权重后无「配置已变更」 | 删 `configDirty` 黄条（权重不可变，筛选不进指纹不裁名单） |
| 签发分声明 | — | 「当前为后端签发分，内置固定权重仅为演示口径说明」 |
| URL/localStorage | demo store v2 移除权重字段 | 删 `aw`/`cw` 查询键与 4 个 localStorage key 及同步 watch |

### 文件

- `4ffb5f4` 走查追加：删配置区两处冗余口径文案（`svc-rec-model-note`、`svc-rec-demo-caliber`/`svc-rec-cultivate-caliber`；demo 定点无此说明，口径声明由结果区 `svc-rec-issued-warn` 承担），footer CTA 改右对齐

- `ServiceRecommendAttractWorkspace.vue` / `ServiceRecommendCultivateWorkspace.vue`：配置区重构 + 权重状态/持久化删除；修复在途 `reportSurface` 模板的孤立 `</template>`（lint 解析错误）；清死 import
- `svcRecommendAttractModel.ts` / `svcRecommendCultivateModel.ts`：删权重编辑/归一/序列化/存储 API（约 -170 行）；`DEFAULT_*_WEIGHTS` 保留仅供 Tag 展示
- `svcRecWeightGate.ts`：**删除**（唯一消费者已清空）
- `serviceRecommendAttract.css`：删 `.svc-rec-indicator-*`/`.svc-rec-weight-bar`/`.svc-rec-placeholder`/`.svc-rec-config-dirty`；新增 `.svc-rec-fixed-weights`/`.svc-rec-eval-footer`/`.svc-rec-model-note`（对齐 demo `.svc-fixed-weights`/`.svc-eval-footer`）
- 3 个 selfcheck 断言反转（不再断言 InputNumber/归一存在，改为断言固定权重 Tag 且上述 UI 绝迹）

## 3. 保留的 lumen 契约（未降级）

- 名单只认 Java `POST /svc/topic/v1/service/rec-list` 实包；禁止本地 Σ、禁止 fixture 填数（`USE_MOCK` mock 走 `@/mock` 注册层）
- 指纹 `svc|attract|*` / `svc|cultivate|*` 不含权重/筛选；I2-12：切条件不自动 create、单飞、当天复用、「重新分析」强制重跑
- D9：ⓘ（M_SVC_REC_ATTRACT_SCORE / GAP-SVC-REC-CULTIVATE-SCORE + Q063 待核验不改绿）、MockBadge、评审层门控与关评零泄漏
- 培育入篮、招引不入篮；画像抽屉；CSV 导出（含演示口径声明行）

## 4. 验证证据

- commit：`4f5807f`（`fix(svc): 招引/培育配置区对齐 demo 定点 ALIGN-L01（内置固定权重）`，9 files，+321/−987）+ 修复 `5f29b6b`（剥离 `4f5807f` 误带的另一单 reportSurface WIP——当时两个 Workspace 工作区副本已被那单写入，提交时按路径筛选未能排除；以 `9ade25e` 为基重写为纯对齐版），均已推 `origin/dev`（rebase 于 `9ade25e` ORG-BASKET-ENTRY-L01 之上）
- `node src/views/service/serviceRecAttractWeight.selfcheck.mjs` / `serviceRecommendAttract.selfcheck.mjs` / `serviceRecCultivate.selfcheck.mjs` → 全绿
- `npx eslint`（4 个改动文件）→ 0 error；`pnpm type-check` → 修复后全仓 0 错（`5f29b6b` 复验）
- 浏览器实测（dev :5199，mock auth）：招引页 DOM 断言 `fixedWeights=1, tags=[35/30/20/15], inputNumber=0, weightBar=0`；培育页 `tags=[25/30/25/20], filterRow=1`；点「开始分析」→ processing 视图（`task_id=SVC-20261020-004`），无报错

## 5. 架构合规自检

- 调用链：前端只调 Java REST ✅（未动 API 层）
- D12：未引入任何 demo-* 依赖 ✅
- D8/D9/D10：token/ⓘ/角标/交互语义保留 ✅
- I2-12：指纹不含权重（更不可能了）；CTA/单飞/当天复用/重新分析全保留 ✅
- ponytail：强度 full；净删约 -240 行（含删除整文件 1 个）

## 6. 开放项

- 正式模型口径仍待 Q063 / Q-SVCCHAIN-05；闭合后由算法签发权重与分数
- 仓内另有在途未提交改动（对象集/机构分析/门户等，72 tracked + 15 untracked），与远端 `9ade25e` 在 3 个 `ServiceOrg*` 文件有冲突；已完整保存在 `stash@{0}`（`wip-before-rebase-e342c38`），工作区已还原干净，由对应任务会话自行 `stash pop` 解冲突
- `reportSurface` 模板配对修复已并入本次提交

## cost

- actual_tokens: ~90k · model_used: glm-5.3 · actual_cost: ~$0.6 · cost_warn: false
