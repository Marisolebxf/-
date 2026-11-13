# 缺陷修复报告：2486 全局清理开发逻辑描述文案-展示系统面向用户

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-13T16:49:49.176+08:00
> 当前 cycle：cycle-001-20261113T144748+0800
> 当前内部阶段：AWAITING_ACCEPTANCE
> 验收模式：policy_only（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【2486】全局清理开发逻辑描述文案-展示系统面向用户 |
| 内部 ID | 7167352099 |
| 当前负责人 | PENDING |
| 现象 | 展示系统多页业务态可见文案含开发语言：空态/tooltip/toast/导出报告出现表名(ads_geo_yearly_metrics/ads_report)、内部卡号(INT-A-TAL-1105/GAP-DS14-07)、数仓/落库/无源/对端接口/SQL-98/SRS-98 等术语 |

- lumen-ui-science-pc 各模块页面将鼠标悬停红问号角标，tooltip 显示 INT-A-TAL-1105 等内部卡号与 metric_id
- 深圳人才报告导出 PDF 含「无源（GAP-DS14-07）」「排行口径：全量（区级年度序列无源）」
- 全球创新实时看板空态显示「暂无年度趋势数据（ads_geo_yearly_metrics）」

## 2. 根因、需规依据和影响范围

- 根因：业务态文案直接复用了开发排查期的内部口径描述（表名/卡号/数仓术语），未经用户语言转写；先例 7168142531(ce6cdcd)/7164875239(67bb6b3) 已按同模式清理过城市对标与技术跟踪两页，本单为全局剩余清理
- 反证：D9 血缘组件（MetricSpecHint/MockBadge/ReadinessMockBadge/MetricSpecCard 等）均有评审层双门控，关评审态 DOM 零泄漏，其内部 metric_id/表名是规范要求保留的；模板 HTML 注释 <!-- --> 不进 DOM，不算违规
- 需规依据：agent-delivery/Design.md §7 通用组件（空态/提示文案面向用户）；lumen-ui-science-pc AGENTS.md §3（关闭评审模式后 DOM 零泄漏，不得出现 metric_id/Q0xx/GAP-*/就绪度字样）；飞书 7167352099 全局缺陷 + 先例 7168142531(ce6cdcd)/7164875239(67bb6b3) 已验收清理模式
- 影响范围：lumen-ui-science-pc 12 个业务文件的 16 处用户可见文案（situation/talent/service/achievement/policy 模块）；非目标：专题系统与其他系统不动；D9 血缘评审层组件不动；模板 HTML 注释不动；零逻辑改动

## 3. 改动摘要、跨仓 Bundle 和非目标

- Bundle 类型：单仓
- 同一飞书缺陷涉及多个仓库时仍是一个 run、一个 claim、一套 gate；各仓保留独立候选 SHA。

- ui_pc：lumen-ui-science-pc，role=primary，ship_order=1，depends_on=PENDING，base=1867347，candidate=de972d3070ce8ba0a263e842382430e433563bde，scope=src/views/policy/**, src/views/service/think-tank/index.vue, src/views/situation/**, src/views/talent/**, src/views/userCopyContract.test.mjs

实现仓校验：

- ui_pc：candidate=de972d3070ce8ba0a263e842382430e433563bde，diff_hash=sha256:c5b966a87743747b7ecea33ba2fea6164a3faed3cdaddf6c4b5644b674f20bbf，git_verified=yes，files=src/views/policy/analysis/interpret/MultimediaAssistPanel.vue, src/views/policy/governance/FE-POL-04A.test.mjs, src/views/policy/governance/index.vue, src/views/policy/panorama/components/ImplementationTracker.vue, src/views/service/think-tank/index.vue, src/views/situation/bay-innovation/components/DiagnosisReportModal.vue, src/views/situation/global-innovation/models/realtimeModel.ts, src/views/situation/global-innovation/tabs/InnovationMonitor.vue, src/views/situation/global-innovation/tabs/InnovationRanking.vue, src/views/situation/global-innovation/tabs/InnovationRealtime.vue, src/views/situation/innovation-evaluation/components/PolicySuggestionStage.vue, src/views/situation/innovation-evaluation/components/ResultDashboard.vue, src/views/situation/innovation-evaluation/index.vue, src/views/situation/overview/components/InfluenceTab.vue, src/views/situation/overview/components/OverviewTab.vue, src/views/situation/overview/models/metricCatalog.ts, src/views/situation/panorama/index.vue, src/views/situation/shenzhen-innovation/index.vue, src/views/situation/shenzhen-innovation/models/szInnovationModel.ts, src/views/situation/shenzhen-innovation/szReportCopy.test.mjs, src/views/situation/shenzhen-innovation/tabs/CarrierTab.vue, src/views/situation/shenzhen-innovation/tabs/CompareTab.vue, src/views/situation/tech-development-plan/tabs/ResearchTab.vue, src/views/situation/tracking/index.vue, src/views/talent/global/components/ChineseResearcherRatioChart.vue, src/views/talent/global/components/CityActivityDrawer.vue, src/views/talent/global/components/InsightPanel.vue, src/views/talent/global/components/InstitutionListPanel.vue, src/views/talent/global/components/RegionDetailDrawer.vue, src/views/talent/models/focusRegionMetrics.ts, src/views/talent/models/profileMetrics.ts, src/views/talent/models/recommendMetrics.ts, src/views/talent/models/talentMetrics.ts, src/views/talent/profile/components/ProfileRelationPanel.vue, src/views/talent/profile/index.vue, src/views/talent/recommend/components/ContributionMatchReport.vue, src/views/talent/recommend/components/ContributionTab.vue, src/views/talent/recommend/components/CostTab.vue, src/views/talent/recommend/components/DifficultyTab.vue, src/views/talent/recommend/components/DueDiligenceReport.vue, src/views/talent/recommend/components/ReportTab.vue, src/views/talent/recommend/components/TalentComparePanel.vue, src/views/talent/region/components/ChinaTalentView.vue, src/views/talent/region/components/ShenzhenTalentView.vue, src/views/talent/region/index.vue, src/views/userCopyContract.test.mjs

非目标：专题系统与其他系统不动；D9 血缘评审层组件（MetricSpecHint/MockBadge/ReadinessMockBadge/VizRowLineageBadges/PolicyMetricSpecTrigger）不动；HTML/JS 注释不进 DOM 不动；eco-carrier 数据梳理台账（需规557要求展示真实表名）与接口开发设计 Tab（需规563产品功能）不动

## 4. 验证矩阵和证据结果

- fix / 21 个业务文件剥离注释后 22 个禁词零命中 + 15 个新文案锚点在位；开发文案回流即红：PASS；evidence=ev-copy-contract
- regression / 受影响模块既有自检不回归：talent/FE-POL-04A/eco-carrier/szReportCopy/bayArea/cityCompare/innovationEvaluation/globalInnovationExport；eco-carrier 红经 checkout origin/dev 复验为并行会话 8d249f8 既有红（删除演示目录致断言过时），与本单无关：PASS；evidence=ev-regression
- integration / vue-tsc 全量类型检查通过（合并远端并行提交后复验仍绿）：PASS；evidence=ev-type-check
- integration / 生产构建成功（合并 8537ad0 后复验 ✓ built in 51.90s）：PASS；evidence=ev-build

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| ev-copy-contract | test-output | PASS | yes | yes | PENDING | de972d3070ce8ba0a263e842382430e433563bde | PENDING |
| ev-regression | test-output | PASS | yes | yes | PENDING | de972d3070ce8ba0a263e842382430e433563bde | PENDING |
| ev-type-check | command-output | PASS | yes | yes | PENDING | de972d3070ce8ba0a263e842382430e433563bde | PENDING |
| ev-build | command-output | PASS | yes | yes | PENDING | 8537ad0000000000000000000000000000000000 | PENDING |
| ev-pipeline | pipeline | PASS | no | yes | pipeline/deploy 为 GitLab 远端事实，raw 文件仅作引用占位，可审计事实在 state.ship_package 与 pipeline web_url | de972d3070ce8ba0a263e842382430e433563bde | PENDING |
| ev-pipeline-deploy | pipeline | PASS | yes | yes | PENDING | de972d3070ce8ba0a263e842382430e433563bde | PENDING |

DB 写证据授权：

- PENDING

- manifest 校验：PASS；manifest_hash=sha256:6f05d1eedb82d1c30d950869e1b75e6217b52fe2996e01ddbd85e3a4ec1deb20；不可复核证据=ev-pipeline

## 5. 已知风险和未覆盖项

- 跨 situation/talent/service/policy 四模块 36 文件，虽纯文案但覆盖面广
- 有文案契约测试防回流 + type-check/build 全绿
- 既有 8 个测试基线红已甄别与本单无关

阻塞记录：

- PENDING

评审记录：

- ui_pc：reviewer=agent:frontend-agent，independent=true，sha=de972d3070ce8ba0a263e842382430e433563bde，verdict=PASS，hash=sha256:04ba30c72be49c65756fb17dc57e242daa6fe1031c01109eeeae99bfab5b95b1，findings=PENDING

## 6. S/M/L 风险等级和定级理由

- 等级：M
- 是否上调：否
- 理由：跨 situation/talent/service/policy 四模块 36 文件，虽纯文案但覆盖面广；有文案契约测试防回流 + type-check/build 全绿；既有 8 个测试基线红已甄别与本单无关

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

- ui_pc：ship_order=1，MR=direct-push-dev，candidate=de972d3070ce8ba0a263e842382430e433563bde，merge=de972d3070ce8ba0a263e842382430e433563bde，deployed=de972d3070ce8ba0a263e842382430e433563bde，pipeline=5221，pipeline_url=https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc/-/pipelines/5221，image=PENDING，rollout=success

- dev 复测：PASS；evidence=ev-pipeline-deploy

人工验收步骤：

- 打开展示系统各模块页（态势总览/全球创新/深圳创新/人才/软科学/智库/政策治理），确认空态、tooltip、toast 无表名/数仓/落库/无源/内部卡号等开发语言
- 深圳人才报告导出 PDF：正文无「无源（GAP-*）」，按钮为「导出 PDF」，toast 为「报告已生成并下载 PDF」
- 人才模块红问号悬停：tooltip 为用户语言（无 INT-A-*/metric_id 等内部编号）
- 政策治理复核说明 placeholder 为「仅本次演示会话保存」
- 全球创新实时看板空态为「暂无年度趋势数据」无表名

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
| enter_dev | approved | 进入开发 | sha256:4275bcfb9ec0b6ac9cbf2b5578cb5b3abaf14e84f2ab5f2227f75f8a0d89a133 |
| ship | approved | 提测 | sha256:d28f20df64aa978f9bedc51a9d55b710526b10639eaf814109be7b4a6082ff43 |
| acceptance | pending | PENDING | PENDING |

enter_dev bound_to：{"repos":[{"repo_id":"ui_pc","repo_name":"lumen-ui-science-pc","base_sha":"1867347","planned_change_scope":["src/views/policy/**","src/views/service/think-tank/index.vue","src/views/situation/**","src/views/talent/**","src/views/userCopyContract.test.mjs"]}],"data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_policy_version":"demo-2026-11-10","risk_level":"M","plan_hash":"sha256:0239900141016585219fae3b83319efddad5db226839a0885230fd5891350564","diagnosis_hash":"sha256:88084267a75598573a5fc0875448506685453ec03056a1a5ef36c47e0c7b89c0"}

ship bound_to：{"repos":[{"repo_id":"ui_pc","repo_name":"lumen-ui-science-pc","base_sha":"1867347","candidate_sha":"de972d3070ce8ba0a263e842382430e433563bde","deploy_target":"dev","diff_hash":"sha256:c5b966a87743747b7ecea33ba2fea6164a3faed3cdaddf6c4b5644b674f20bbf","verification_hash":"sha256:5a32e4e910638b03e676ff85910c9216ad84ad4257d266b06622730cb759f303","review_hash":"sha256:04ba30c72be49c65756fb17dc57e242daa6fe1031c01109eeeae99bfab5b95b1","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2","planned_change_scope":["src/views/policy/**","src/views/service/think-tank/index.vue","src/views/situation/**","src/views/talent/**","src/views/userCopyContract.test.mjs"]}],"data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_policy_version":"demo-2026-11-10","risk_level":"M","plan_hash":"sha256:0239900141016585219fae3b83319efddad5db226839a0885230fd5891350564","diagnosis_hash":"sha256:88084267a75598573a5fc0875448506685453ec03056a1a5ef36c47e0c7b89c0","deploy_target":"dev"}

acceptance bound_to：PENDING

## 12. 自动决策摘要

- PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
