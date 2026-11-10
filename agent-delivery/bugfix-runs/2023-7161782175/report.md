# 缺陷修复报告：2023 科技全域态势，实时数据监控，选择饼图实际展示为折线图

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-11T00:45:55.844+08:00
> 当前 cycle：cycle-002-20261110T232435+0800
> 当前内部阶段：READY_SHIP
> 验收模式：policy_only（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【2023】科技全域态势，实时数据监控，选择饼图实际展示为折线图 |
| 内部 ID | 7161782175 |
| 当前负责人 | human:7695591354147146731 |
| 现象 | 选择“饼图”后，企业领域分布面板已显示饼图，但下方 KPI 要素卡仍显示折线，未随图表类型统一切换 |

- 打开科技全域态势-实时数据监控
- 统计指标选择数量统计
- 点击图表类型饼图
- 观察企业领域分布面板为饼图，但下方专家学者、会议等 KPI 卡仍是折线

## 2. 根因、需规依据和影响范围

- 根因：OverviewTab.sparkOptionOf 将 KPI 卡图表固定为 line/bar，饼图态被强制回落折线；饼图只接入了 distribution panel，没有接入 factorCards
- 反证：图表类型按钮与标题均显示饼图，说明状态已切换；后端返回 factorCards 的年度序列正常，问题在渲染层未选择 pie option
- 需规依据：科技信息展示系统 SRS 1.1.1.1.4.1.1.3.2 统计指标展示功能；用户验收口径：选择饼图时右侧分布面板及下方所有 KPI 卡都应显示饼图
- 影响范围：lumen-ui-science-pc OverviewTab KPI 卡图表渲染；chartBuilders 要素卡图表 option 构造

## 3. 改动摘要和非目标

- ui_pc：lumen-ui-science-pc，base=2e91005ec368bb1b3acd32b7cc0de7cc6e357073，candidate=30eb4682c75c86a1edad591c3e842c50000415d5，scope=src/views/situation/overview/components/OverviewTab.vue, src/views/situation/overview/models/chartBuilders.ts, src/views/situation/overview/overviewTab.test.mjs

实现仓校验：

- ui_pc：candidate=30eb4682c75c86a1edad591c3e842c50000415d5，diff_hash=sha256:a0daa9372536c2318cedc9fd6278f87242e48ece03e89307ece7d6d6a3c1e9be，git_verified=yes，files=src/views/situation/overview/components/OverviewTab.vue, src/views/situation/overview/models/chartBuilders.ts, src/views/situation/overview/overviewTab.test.mjs

非目标：不改后端 /situation/overview 取数逻辑；不改筛选条件与 KPI 数值；不调整图表类型按钮的文案和布局

## 4. 验证矩阵和证据结果

- fix / 选择饼图后，企业领域分布面板和下方全部 9 张 KPI 要素卡均切换为饼图；KPI 饼图保留口径说明 tooltip。：PASS；evidence=evidence/manifest.json#E-UI-003, evidence/manifest.json#E-CMD-009
- regression / 折线、柱状图路径保持不变，Situation 测试、类型检查和生产构建均通过。：PASS；evidence=evidence/manifest.json#E-CMD-009, evidence/manifest.json#E-CMD-010, evidence/manifest.json#E-CMD-011, evidence/manifest.json#E-CMD-012
- boundary / 空序列和全零序列返回 null 并降级为暂无趋势数据，不伪造饼图；零值扇区被过滤。：PASS；evidence=evidence/manifest.json#E-CMD-009

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| E-CMD-001 | test | PASS | yes | yes | PENDING | d2d66afeb4750d42c67ae714dc479338088d9300 | Situation 测试全部通过，覆盖默认折线及饼图联动自检。 |
| E-CMD-002 | test | PASS | yes | yes | PENDING | d2d66afeb4750d42c67ae714dc479338088d9300 | vue-tsc 类型检查通过。 |
| E-CMD-003 | test | PASS | yes | yes | PENDING | d2d66afeb4750d42c67ae714dc479338088d9300 | Vite 生产构建通过。 |
| E-CMD-004 | test | PASS | yes | yes | PENDING | d2d66afeb4750d42c67ae714dc479338088d9300 | 本次改动文件 ESLint 通过；全仓 lint 存在 618 个与本改动无关的存量错误。 |
| E-UI-001 | browser | PASS | yes | yes | PENDING | d2d66afeb4750d42c67ae714dc479338088d9300 | 默认分布图为 line，9 张 KPI 均为 line；点击饼图后分布图为 pie（6 扇区），9 张 KPI 全部为 pie（每张 7 扇区）。 |
| E-CMD-005 | test | PASS | yes | yes | PENDING | 87dfa211b4fd2ab9b4b6750b45619ebd789ac523 | 最终候选 Situation 测试全部通过；overviewTab.test.mjs 已改为真实 builder 行为测试。 |
| E-CMD-006 | test | PASS | yes | yes | PENDING | 87dfa211b4fd2ab9b4b6750b45619ebd789ac523 | 最终候选 vue-tsc 类型检查通过。 |
| E-CMD-007 | test | PASS | yes | yes | PENDING | 87dfa211b4fd2ab9b4b6750b45619ebd789ac523 | 最终候选 Vite 生产构建通过。 |
| E-CMD-008 | test | PASS | yes | yes | PENDING | 87dfa211b4fd2ab9b4b6750b45619ebd789ac523 | 最终候选改动文件 ESLint 通过。 |
| E-UI-002 | browser | PASS | yes | yes | PENDING | 87dfa211b4fd2ab9b4b6750b45619ebd789ac523 | 最终候选默认分布图和 9 张 KPI 均为 line；点击饼图后分布图 pie，9 张 KPI 全部 pie，所有 KPI tooltip 存在。 |
| E-CMD-009 | test | PASS | yes | yes | PENDING | 30eb4682c75c86a1edad591c3e842c50000415d5 | 最终提交 Situation 测试全部通过。 |
| E-CMD-010 | test | PASS | yes | yes | PENDING | 30eb4682c75c86a1edad591c3e842c50000415d5 | 最终提交类型检查通过。 |
| E-CMD-011 | test | PASS | yes | yes | PENDING | 30eb4682c75c86a1edad591c3e842c50000415d5 | 最终提交生产构建通过。 |
| E-CMD-012 | test | PASS | yes | yes | PENDING | 30eb4682c75c86a1edad591c3e842c50000415d5 | 最终提交改动文件 ESLint 通过。 |
| E-UI-003 | browser | PASS | yes | yes | PENDING | 30eb4682c75c86a1edad591c3e842c50000415d5 | 默认分布图和 9 张 KPI 均为 line；点击饼图后分布图为 pie，9 张 KPI 全部 pie，所有 KPI tooltip 存在。 |

DB 写证据授权：

- PENDING

- manifest 校验：PASS；manifest_hash=sha256:718811809d36c7d69d31cf59f45b5fe97cc52dc0fa665a9b38db9880d2ae9977；不可复核证据=PENDING

## 5. 已知风险和未覆盖项

- 修复涉及实时数据监控中分布面板与全部 KPI 要素卡的图表类型联动，影响范围覆盖整个右侧图表区
- 已通过本地真实交互断言覆盖首屏和视区外全部 9 张 KPI 卡；提测后仍需在 dev 真实接口环境复验一次

评审记录：

- ui_pc：reviewer=agent:review-agent:01a1c650，independent=true，sha=30eb4682c75c86a1edad591c3e842c50000415d5，verdict=PASS，hash=sha256:acad4aac92715f6d17536cd3a4a7d7d34f7a5a472db4f9c0cb1615569ad0d597，findings=PENDING

## 6. S/M/L 风险等级和定级理由

- 等级：M
- 是否上调：否
- 理由：修复涉及实时数据监控中分布面板与全部 KPI 要素卡的图表类型联动，影响范围覆盖整个右侧图表区；已通过本地真实交互断言覆盖首屏和视区外全部 9 张 KPI 卡；提测后仍需在 dev 真实接口环境复验一次

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

- PENDING

- dev 复测：PENDING；evidence=PENDING

人工验收步骤：

- PENDING

## 10. 人工验收步骤

- 飞书当前状态：IN PROGRESS
- 验收证据：PENDING
- 验收结论：pending
- Agent 不主动调用 `transition_state` 将缺陷置为 RESOLVED；只在飞书已出现业务状态迁移后读取并记录。

## 11. Gate 状态与绑定对象

| gate | status | token | hash |
|---|---|---|---|
| enter_dev | approved | 进入开发 | sha256:3a5e0ba87c0dca8578332d3fdff7c41e7cc5922dfec767636fd82ef0363b2bd4 |
| ship | pending | PENDING | PENDING |

enter_dev bound_to：{"repos":[{"repo_id":"ui_pc","repo_name":"lumen-ui-science-pc","base_sha":"2e91005ec368bb1b3acd32b7cc0de7cc6e357073","planned_change_scope":["src/views/situation/overview/components/OverviewTab.vue","src/views/situation/overview/models/chartBuilders.ts","src/views/situation/overview/overviewTab.test.mjs"]}],"diagnosis_hash":"sha256:38822450b4dcac2506e15d65cac4ec6808b0685d0857f7e79f4b0802c4230ba0","plan_hash":"sha256:d93a4a90d14b7c116ffca8f56074a418687974cf9df8ea56fc7d4655588e06dc","risk_level":"M","data_policy_version":"demo-2026-11-10","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}

ship bound_to：PENDING

## 12. 自动决策摘要

- 保持 KPI factor card 的饼图回落折线语义，仅修复企业领域分布面板的年份回退；依据=原 demo 和现有组件均明确 factorCardChartType 将 pie 映射为 line；图表类型控件作用于 distribution panel；备选=把每张 KPI 卡也改成饼图，但不同要素单位不可比且偏离原型 / 继续隐藏分布面板并禁用图表切换，但无法满足需规的饼图展示；影响=用户选择饼图后由恢复的企业领域分布面板展示饼图，KPI 卡继续展示年度 sparkline；需人工批准=no；批准人=PENDING
- 修复在独立分支完成并创建 Draft MR !6，当前停在 READY_SHIP 等待精确口令；依据=M 级改动已通过独立 review、23 个 Situation 测试和 git scope 校验；备选=直接修改 dev（禁止，未获提测授权） / 继续扩大改动范围（无必要，当前证据已覆盖缺陷）；影响=收到提测口令后将合并 dev、触发后端部署并做 dev 复测；需人工批准=no；批准人=PENDING
- 提测流水线以 required jobs 全部成功作为发布门槛，可选 sonar:scan 不阻塞本次 dev 复测；依据=pipeline 4729 的 backend:build、backend:image:display、deploy:display 均为 success，display 镜像 77bf1374 已完成 Kubernetes rollout；sonar:scan 配置为 allow_failure 且仍在运行；备选=继续等待可选 sonar:scan 结束，但会无谓阻塞已完成的 dev 发布与业务验证；影响=dev 已发布本次候选合并后的 SHA 77bf137495d3f5c57deb676caa506324a3687b3a；后续 sonar 结果不影响本次业务复测，但会在报告中保留该事实；需人工批准=no；批准人=PENDING
- 废止上一 cycle 的“KPI 卡继续保持折线”判断，以用户最新验收口径为准：选择饼图时分布面板和全部 KPI 卡都显示饼图；依据=用户在 REOPEN 时明确指出所有 KPI 卡也必须切换为饼图；本地页面已验证 9 张 KPI 全部由 line 切换为 pie；备选=只修复分布面板（已被用户验收否决） / 不同要素单位不可比为理由拒绝 KPI 饼图（不符合用户明确验收口径）；影响=最终候选 30eb468 统一使用 buildOverviewFactorCardOption 选择图表类型，并保留原有 line/bar 和空数据降级行为；需人工批准=no；批准人=PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
