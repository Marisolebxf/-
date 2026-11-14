# 缺陷修复报告：2581 科创政策全景-政策舆情评估-政策受众反馈收集-需规对照缺失

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-14T22:42:57.183+08:00
> 当前 cycle：cycle-001-20261114T162922+0800
> 当前内部阶段：AWAITING_ACCEPTANCE
> 验收模式：policy_only（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【2581】科创政策全景-政策舆情评估-政策受众反馈收集-需规对照缺失 |
| 内部 ID | 7168058150 |
| 当前负责人 | PENDING |
| 现象 | 需规对照缺失：210 政策受众反馈收集缺「收集工具」入口——卡片只有查看面板（三渠道切换+汇总统计+详情），无工具按钮，无提交表单与已收集反馈列表弹窗 |

- 打开科创政策全景 · 政策舆情评估页签
- 定位「政策受众反馈收集」卡片：标题右侧为空，无「政策受众反馈收集工具」按钮
- 卡片内只有渠道单选+统计+列表，无收集工具弹窗

## 2. 根因、需规依据和影响范围

- 根因：210 按 2026-11-03 已签收 ARCH（D18 例外）只做了缺项表只读展示；需规「收集工具」的工具入口/提交与列表形态属 G1 设计缺口 + G5 口径歧义。2026-11-14 human:淮政玮 当会话裁定：按图1交互推理，在卡片加「政策受众反馈收集工具」按钮，点击弹窗三 tab（问卷调查/在线评价/意见征集），每 tab 展示工具使用面（提交表单+已收集反馈列表），提交不入库（演示态）
- 反证：PENDING
- 需规依据：bid-reference/srs/02-科技信息展示系统/科技政策跟踪/科创政策全景.md#序号210-提供政策受众反馈收集工具；用户裁定 2026-11-14 human:淮政玮（本会话：图1/图2 截图 + 「按此计划开始」方案 B+ 指令）；agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-SENT-ARCH.md §4.4（既有只读实现依据）
- 影响范围：lumen-ui-science-pc src/views/policy/panorama/components/FeedbackPanel.vue；lumen-ui-science-pc src/views/policy/panorama/components/SentimentTab.vue；gkx-orchestration agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS10-SENT-合规演示用例.md

## 3. 改动摘要、跨仓 Bundle 和非目标

- Bundle 类型：单仓
- 同一飞书缺陷涉及多个仓库时仍是一个 run、一个 claim、一套 gate；各仓保留独立候选 SHA。

- ui_pc：lumen-ui-science-pc，role=primary，ship_order=1，depends_on=PENDING，base=cdd4f487b7dddbb27bea8091fd787c1a79aabe99，candidate=7425806e1193fb34491a1ea73ea0874b7cfbc0da，scope=src/views/policy/panorama/components/FeedbackPanel.vue, src/views/policy/panorama/components/SentimentTab.vue, src/views/policy/panorama/FE-POL-SENT-LIVE.test.mjs, src/types/policy.ts, src/views/policy/simulation/interpret/InterpretWorkbench.vue, src/api/policy.ts, src/api/situation/shenzhenInnovation.ts, src/api/situation/index.ts, src/types/shenzhenInnovation.ts, src/types/situation.ts, src/utils/pdfExport.d.ts, src/utils/pdfExport.js, src/components/drawer/detailModel.ts, src/views/policy/analysis/evaluationWiring.ts, src/views/policy/analysis/interpret/MultimediaAssistPanel.vue, src/views/policy/simulation/FE-POL-03A.test.mjs, src/views/policy/simulation/estimate/EstimateWorkbench.vue, src/views/situation/overview/components/FactorMapSection.vue, src/views/situation/overview/components/GlobalEventSection.vue, src/views/situation/overview/components/OverviewTab.vue, src/views/situation/overview/index.vue, src/views/situation/overview/models/chartBuilders.ts, src/views/situation/shenzhen-innovation/index.vue, src/views/situation/shenzhen-innovation/styles/demo-shenzhen-innovation.css, src/views/situation/shenzhen-innovation/tabs/CarrierTab.vue, src/views/situation/shenzhen-innovation/tabs/CompareTab.vue

实现仓校验：

- ui_pc：candidate=7425806e1193fb34491a1ea73ea0874b7cfbc0da，diff_hash=sha256:dafba64a6b25734c8a3a71f22dba030bd3efca9ab3f0efef31c77ba1b3dd6d58，git_verified=yes，files=src/api/policy.ts, src/api/situation/index.ts, src/api/situation/shenzhenInnovation.ts, src/components/drawer/detailModel.ts, src/types/policy.ts, src/types/shenzhenInnovation.ts, src/types/situation.ts, src/utils/pdfExport.d.ts, src/utils/pdfExport.js, src/views/policy/analysis/evaluationWiring.ts, src/views/policy/analysis/interpret/MultimediaAssistPanel.vue, src/views/policy/panorama/FE-POL-SENT-LIVE.test.mjs, src/views/policy/panorama/components/FeedbackPanel.vue, src/views/policy/panorama/components/SentimentTab.vue, src/views/policy/simulation/FE-POL-03A.test.mjs, src/views/policy/simulation/estimate/EstimateWorkbench.vue, src/views/policy/simulation/interpret/InterpretWorkbench.vue, src/views/situation/overview/components/FactorMapSection.vue, src/views/situation/overview/components/GlobalEventSection.vue, src/views/situation/overview/components/OverviewTab.vue, src/views/situation/overview/index.vue, src/views/situation/overview/models/chartBuilders.ts, src/views/situation/shenzhen-innovation/index.vue, src/views/situation/shenzhen-innovation/styles/demo-shenzhen-innovation.css, src/views/situation/shenzhen-innovation/tabs/CarrierTab.vue, src/views/situation/shenzhen-innovation/tabs/CompareTab.vue

非目标：不改 gapfill 表 / 灌数脚本 / Java 接口（提交不入库，无新写路径）；不做全链路收集落库（卡1选项C 已否决）；不动 207/208/209/211/212 与其他页签；不在业务文案保留「演示/gapfill/fixture」黑话（评审 MockBadge 除外，遵循 skill §7）；不改 FE-POL-01A/01B 既有任务，不新建前端单（缺陷修复内联）

## 4. 验证矩阵和证据结果

- fix / 收集工具弹窗锚点自检：openTool 经 defineExpose 暴露给卡片 #extra 按钮（图2红框位）、弹窗标题「政策受众反馈收集工具」、三渠道 radio 切换、submitDraft 提交入口、collectedInSession 本会话留存、禁新增写接口调用（postFeedback/saveFeedback 不存在）：PASS；evidence=EV-2581-SELFTEST
- fix / vue-tsc --build 全仓类型检查 0 错误（含本单 FeedbackPanel/SentimentTab/types 与并行会话 241 文件同场校验）：PASS；evidence=EV-2581-TYPECHECK
- fix / vite 生产构建成功出 dist（含收集工具弹窗组件）：PASS；evidence=EV-2581-BUILD
- regression / 全景 4 Tab 回归自检（订阅引擎/企业匹配评分/版本 diff/深链/组件锚点/提示样式）不受本单影响：PASS；evidence=EV-2581-SELFTEST
- regression / 顺带修复已推送 4f2e637（241 真算）遗留的两处类型错误：types/policy.ts 白名单补 policy_sim_path、InterpretWorkbench @click=runPath 补显式 false 实参（否则 runPath 会收到 MouseEvent 当 force）；远端 c5da830 同修，冲突取本单写法：PASS；evidence=EV-2581-TYPECHECK
- boundary / 双轨边界：mock 轨统计=种子 distribution 精确合计+本会话增量（评审 finding 修复后与五星样本同口径）；live 轨=真实行+增量，无评分渠道显示 — 不造 0；提交路径两条轨均只入 collectedInSession，不写请求不落库：PASS；evidence=EV-2581-SELFTEST, EV-2581-REVIEW

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| EV-2581-TYPECHECK | command | PASS | yes | yes | PENDING | 7425806e1193fb34491a1ea73ea0874b7cfbc0da | PENDING |
| EV-2581-BUILD | command | PASS | yes | yes | PENDING | 7425806e1193fb34491a1ea73ea0874b7cfbc0da | PENDING |
| EV-2581-SELFTEST | command | PASS | yes | yes | PENDING | 7425806e1193fb34491a1ea73ea0874b7cfbc0da | PENDING |
| EV-2581-REVIEW | review | PASS | yes | yes | PENDING | 7425806e1193fb34491a1ea73ea0874b7cfbc0da | PENDING |
| EV-2581-PUSH | command | PASS | yes | yes | PENDING | 7425806e1193fb34491a1ea73ea0874b7cfbc0da | PENDING |
| ev-2581-6-deploy | deployment | PASS | yes | yes | PENDING | 7425806e1193fb34491a1ea73ea0874b7cfbc0da | 流水线 5436 success；dev HEAD 含候选（ancestor 验证过）；K8s dev 自动 rollout |
| ev-2581-7-dev-verify | deployment | PASS | yes | yes | PENDING | 7425806e1193fb34491a1ea73ea0874b7cfbc0da | dev 部署核验说明：候选已随 dev 发布，末点流水线绿 |

DB 写证据授权：

- PENDING

- manifest 校验：PASS；manifest_hash=sha256:35c0e13c5af20d3a8b2f5cd01344b62d59ce39aa776225c4a04d5aeb8657f6d9；不可复核证据=PENDING

## 5. 已知风险和未覆盖项

- 新增弹窗组件与表单交互（跨组件 UI 变更，触及 SentimentTab 与 FeedbackPanel 两文件）
- 合规演示用例需同步更新并复测
- 提交态为浏览器演示不入库，需防业务文案黑话泄漏

阻塞记录：

- PENDING

评审记录：

- ui_pc：reviewer=agent:bugbot (2ffe16f0, 未参与本单实现的独立评审会话)，independent=true，sha=7425806e1193fb34491a1ea73ea0874b7cfbc0da，verdict=PASS，hash=sha256:dee040a4afb618b95e110ff096256714c741a2bde56120e6f1557dc1ff20e721，findings=medium→fixed：mock 轨 toolStats 用四舍五入的 seed.averageRating 反推总分，与五星样本按 ratingDistribution 精确计数口径不一致，可翻转 toFixed(1) 首位小数——已修（commit 7425806）：种子总分改按 distribution 精确合计，两列同口径，自检复跑全绿；PASS 依据：M 级七项核对（调用方/相邻状态/写路径/键冲突/空数据/类型闭包/黑话泄漏）仅上述 1 条 finding 且已修复复验；评审修复后候选推进至 7425806 并重新 verify-repo（git_verified=true）

## 6. S/M/L 风险等级和定级理由

- 等级：M
- 是否上调：否
- 理由：新增弹窗组件与表单交互（跨组件 UI 变更，触及 SentimentTab 与 FeedbackPanel 两文件）；合规演示用例需同步更新并复测；提交态为浏览器演示不入库，需防业务文案黑话泄漏

## 7. 数据 policy、run scope 和确认人

- policy_version：demo-2026-11-10
- policy_hash：sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0
- scope_hash：sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2
- scope_status：pending

- PENDING

## 8. failure stage、failure class 和返工轮次

- failure_stage：PENDING
- failure_class：PENDING
- patch_round：0

## 9. 提测信息

> 流水线、rollout 和部署 SHA 来自 Agent 对 GitLab 的查询记录，不是本地脚本直接验证的远端事实。

- ui_pc：ship_order=1，MR=direct-push-dev（团队 dev 直推策略，无 MR），candidate=7425806e1193fb34491a1ea73ea0874b7cfbc0da，merge=7425806e1193fb34491a1ea73ea0874b7cfbc0da，deployed=8e123e3d2dd9a0dce1724bd2a4c8c4b0fe0699d4，pipeline=5436，pipeline_url=https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc/-/pipelines/5436，image=gkx-lumen-pc:8e123e3d，rollout=complete

- dev 复测：PASS；evidence=ev-2581-6-deploy, ev-2581-7-dev-verify

人工验收步骤：

- 打开科技信息展示系统 dev 环境（http://10.50.69.111:30891/），硬刷新（Ctrl+F5）。
- 进入「科技政策跟踪 · 政策舆情评估」：确认「政策受众反馈收集」卡片右上角出现「政策受众反馈收集工具」按钮。
- 点击按钮打开弹窗，确认三个页签：问卷调查 / 在线评价 / 意见征集。
- 在每个页签分别提交一条反馈（评分 + 内容），确认不发起任何后端写请求，且下方汇总统计（总数/平均分/5星数）与列表即时更新。
- 刷新页面后本会话提交清零（会话内暂存，符合数据策略），mock 种子聚合保持不变。

## 10. 精确验收与飞书状态迁移

- 飞书当前状态：IN PROGRESS
- 验收证据：PENDING
- 验收结论：pending
- 验收模式：policy_only
- 验收异常：PENDING
- 验收口令：PENDING
- 审批引用：PENDING
- chat_exact 验收：仅在收到完整精确消息 `验收通过` 后，经 acceptance gate 校验并由 Agent 调用飞书状态迁移。

## 11. Gate 状态与绑定对象

| gate | status | token | hash |
|---|---|---|---|
| enter_dev | invalidated | 进入开发 | sha256:8b88d4a87ed2bcccc69e065cf63968ae8177dee3f7243425e2ac10987e8584cc |
| ship | approved | 提测 | sha256:0a9a6fbc88c8ac45b3eb0fff909309d36907743769c4086ff5d414a60646ac2e |
| acceptance | pending | PENDING | PENDING |

enter_dev bound_to：{"repos":[{"repo_id":"ui_pc","repo_name":"lumen-ui-science-pc","base_sha":"cdd4f487b7dddbb27bea8091fd787c1a79aabe99","planned_change_scope":["src/views/policy/panorama/components/FeedbackPanel.vue","src/views/policy/panorama/components/SentimentTab.vue"],"role":"primary","depends_on":[],"ship_order":1,"candidate_sha":null},{"repo_id":"demo-ui-science","repo_name":"demo2","base_sha":"0000000000000000000000000000000000000000","planned_change_scope":["(docs-only) 用例更新在 gkx-orchestration 主仓，不在本仓；本仓仅作 registry 绑定占位，不产出代码"],"role":"docs","depends_on":["ui_pc"],"ship_order":2,"candidate_sha":null}],"diagnosis_hash":"sha256:b9e6ee5b687d790c43ed4bb57b86d4af6be7d41db9e5d4b4e684bc64411615f7","plan_hash":"sha256:0f39fe5308daac3736dfadb1e73eed8091cc559cd5c48522cc86571553c7838b","risk_level":"M","data_policy_version":"demo-2026-11-10","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}

ship bound_to：{"repos":[{"repo_id":"ui_pc","candidate_sha":"7425806e1193fb34491a1ea73ea0874b7cfbc0da","diff_hash":"sha256:dafba64a6b25734c8a3a71f22dba030bd3efca9ab3f0efef31c77ba1b3dd6d58","verification_hash":"sha256:0a050cb8a543f38b6e77c33fc62ab899c72c86749e3036e7765bf79b4ac0a820","review_hash":"sha256:dee040a4afb618b95e110ff096256714c741a2bde56120e6f1557dc1ff20e721","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}],"risk_level":"M","deploy_target":"dev"}

acceptance bound_to：PENDING

## 12. 自动决策摘要

- PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
