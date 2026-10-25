# LUMEN-POLICY-SZ3D-D-FE-L01 · 深圳政策现状三张固定卡

> 设计：`05.6.2-深圳政策现状分析.md`。只改深圳配置、结果和报告。未改时序过程页、区域对比结果板、门户 Tab。未领 E0/E1。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | C 叶已在 integration。同仓时序前端锁未改其文件。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 删掉勾选模型和综合分/雷达，沿用现页壳与 Java `cards`/`strategies`。不加依赖。时序/区域指纹仍带历史 34/33/33，避免当天复用被拆开。 |

## 修改内容

- `/policy/recommendation` 配置区改为三张只读卡。无二级 Checkbox、无一级权重步进器、无一键均分、无「目录为空则可开始」绿条。
- 支持力度只读政策条数与政策层级，档位写不可算。ⓘ 为 `M_POLICY_SUPPORT_STRENGTH`，QPOL-02 用 PendingBadge。评审模式关闭时角标自闸。
- 开始分析只看锚点。深圳创建参数不带 `weights` / `selected_indicators`。
- 结果只渲染 Java `cards`：城市截面分、名次、条数、层级均值；文案标明非资金强度，以及市级备案多会拉低层级分。适配性无分数/命中/原因时写「本锚点无适配结果」。实效卡只写不可算。综合分恒为 null，档位 null 不写成 0。
- 优化建议只渲染 `strategies`。无卡时写「本结果没有可写的优化建议」。报告第 5 章优先用快照 `report_chapters`，否则用同一份 `strategies`。模板号 `POL-SZ-3D-PDF-v1`。
- 过程五步（条件校验 → 分卡读数 → 结果组装 → 优化建议 → 解读润色）只作说明，`totalNodes` 仍由 Java 给出。
- `USE_MOCK=false` 路径不引用 Demo `POLICY_SZ_CORE_INDICATORS`。

## 测试结果

- `node src/views/policy/policyShenzhen.selfcheck.mjs`
- `node src/views/policy/policyConfig.selfcheck.mjs`
- `node src/views/policy/policyTimeseries.selfcheck.mjs`
- `node src/views/policy/policyRegional.selfcheck.mjs`
- `node src/views/policy/policyWaitView.selfcheck.mjs`
- 以上均通过。
- `vue-tsc --build`：本叶指纹类型错误已消。仓库里仍有既有缺模块：`CmsRichText.vue` 的编辑器、`evalReportPdf.ts` 的 html2canvas/jspdf。与本叶无关。
- 浏览器 `http://127.0.0.1:3001/policy/recommendation`：三张卡 `support/fit/effect` 都在，勾选卡和权重步进器为 0。未选锚点时开始分析禁用；选中「集成电路」后页脚为「锚点已选，可开始分析」，按钮可点。评审模式打开后可见三枚指标入口和 QPOL-02。时序页仍有「时序三维」且没有深圳固定卡；区域对比页仍有「对比区域 / 评价维度」。未点击开始分析，没有向网关创建任务。

## CI/CD

- 分支：`lumen-ui-topic` `origin/dev`
- commit：`5a41dee5bc0e044e6906a2a7f8c4b295c988c0bc`
- 部署：本叶不点部署

## 遗留

- 结果板和报告没有用一条已签发的深圳任务在浏览器里点开。后端本轮未部署。
- 本地指标镜像把三枚政策指标显示为「未登记」，ⓘ 仍指向对应 metric_id。不在前端改绿。
- 任务不写「联调通过」。E0/E1 仍为 backlog。

## 涉及文件

- `repos/lumen-ui-topic/src/views/policy/PolicyAnalysisConfigPage.vue`
- `repos/lumen-ui-topic/src/components/policy/PolicyShenzhenResultBoard.vue`
- `repos/lumen-ui-topic/src/components/policy/PolicyShenzhenReportHost.vue`
- `repos/lumen-ui-topic/src/utils/policyShenzhenResult.ts`
- `repos/lumen-ui-topic/src/config/policyAnalysisRegistry.ts`
- `repos/lumen-ui-topic/src/views/industry-center/industryDiagnosis.css`
- `repos/lumen-ui-topic/src/views/policy/policyConfig.selfcheck.mjs`
- `repos/lumen-ui-topic/src/views/policy/policyShenzhen.selfcheck.mjs`

## 架构合规

| 铁律 | 结果 |
|------|------|
| 前端只调 Java | ✅ 不直连 Python，不算分 |
| 不把 null 写成 0、不补综合分 | ✅ |
| D9 ⓘ / PendingBadge 走评审层 | ✅ |
| 时序页与区域对比页不回退 | ✅ 自检 + 浏览器 |
| D12 不引用 demo 服务或 fixture | ✅ |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 80000 |
| model_used | grok-4.7 |
| actual_cost | 0.16 |
| cost_warn | green |
| 说明 | source: session_estimate。沿用 C 叶 60000 token ≈ $0.12 的比例，本叶按登记估算 80000。无 Console 的 in/out 分离值。 |
