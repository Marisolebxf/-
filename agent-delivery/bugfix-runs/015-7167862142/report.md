# 缺陷修复报告：015 政策效果推演-科技政策推演-政策实施路径预测-需规对照有缺失内容：关键节点

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-14T14:32:45.534+08:00
> 当前 cycle：cycle-001-20261114T134447+0800
> 当前内部阶段：READY_SHIP
> 验收模式：policy_only（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【015】政策效果推演-科技政策推演-政策实施路径预测-需规对照有缺失内容：关键节点 |
| 内部 ID | 7167862142 |
| 当前负责人 | PENDING |
| 现象 | 241 政策实施路径预测：需规两处点名「关键节点 / 关键节点说明」，live 真轨 Timeline 渲染了 stage_text 正文但无「关键节点说明」显式区块，QA 逐字对照找不到该名词（G2：live 砍了形态） |

- 打开 政策效果推演 · 科技政策推演 · 政策实施路径预测 子 Tab（USE_MOCK=false）
- 选政策（样例 18363390）→ 点「预测实施路径」
- 页面只有「政策实施流程图」时间轴；无「关键节点说明」标题区块，stage_text 混在时间轴项内

## 2. 根因、需规依据和影响范围

- 根因：demo 原型 toPathItems 只把 note 混在 Timeline 项内；lumen 复刻保留该形态。需规 241-7/241-8 要「关键节点说明」独立可辨识区块；SDD 功能点表有 241-8 行（节点旁 stage_text）但界面必见清单未列显式区块名。同族先例 7167771715（评价页实施路径与风险辅助·缺关键节点）修法 = PolicyTextAnalysis.vue 显式「关键节点」里程碑卡片区
- 反证：数据侧无缺口：gapfill_policy_sim_result 路径环节五行 stage_text 全非空（policy_id 18363390）；mock 轨 policyPathForecastData 与真轨形态缺口无关
- 需规依据：bid-reference/srs/02-科技信息展示系统/科技政策跟踪/政策效果推演.md 序号241（Excel 244）；sdd/科技政策跟踪-系统详细设计说明书.md §241 功能点 241-8；gkx-orchestration/agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/简报/2026-11-14-241-政策实施路径预测-需规分句闭合.md；feishu:6a687a81e231818dec771f9a#7167862142 描述（报告人黄敬洲 2026-11-13 15:22）
- 影响范围：241 子 Tab 真轨区块形态（时间轴下方补关键节点说明卡片行）

## 3. 改动摘要、跨仓 Bundle 和非目标

- Bundle 类型：单仓
- 同一飞书缺陷涉及多个仓库时仍是一个 run、一个 claim、一套 gate；各仓保留独立候选 SHA。

- ui_pc：lumen-ui-science-pc，role=primary，ship_order=1，depends_on=PENDING，base=7ef79f4，candidate=5e96b09d8badd432e0d14264bfebd25d60565a35，scope=src/views/policy/simulation/interpret/InterpretWorkbench.vue, src/views/policy/simulation/FE-POL-03A.test.mjs

实现仓校验：

- ui_pc：candidate=5e96b09d8badd432e0d14264bfebd25d60565a35，diff_hash=sha256:3a363e5536ed9c96d9fb6456fa1f628b757e6e729fd2ed270ed898404aebabea，git_verified=yes，files=src/views/policy/simulation/FE-POL-03A.test.mjs, src/views/policy/simulation/interpret/InterpretWorkbench.vue

非目标：不改 simulation/jobs 契约与 element 读面（数据五行 stage_text 齐备）；不灌历史对照行、不挂历史评估图卡（2026-11-12 卡1=A 维持）；不补 mock 轨形态（缺口只在真轨）；不动说明书（241-8 已有行）

## 4. 验证矩阵和证据结果

- fix / 241 真轨流程图卡出现「关键节点说明」显式区块，逐环节卡含环节名/时间安排/责任主体/说明四字段：PASS；evidence=ev-015-1-selfcheck
- regression / FE-POL-03A 全量 50 项断言无回归；vue-tsc 全量类型门 0 错误：PASS；evidence=ev-015-1-selfcheck, ev-015-2-typecheck

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| ev-015-1-selfcheck | test | PASS | yes | yes | PENDING | 5e96b09 | FE-POL-03A 自检 50 项全绿，含 241-8 关键节点说明显式区块断言 |
| ev-015-2-typecheck | test | PASS | yes | yes | PENDING | 5e96b09 | 主仓全量 vue-tsc 类型门 0 错误（exit 0，773931ms） |

DB 写证据授权：

- PENDING

- manifest 校验：PASS；manifest_hash=sha256:523d3db82e03d4d87582c70e9a1dc5738997542d299fed69d435228bb00097a9；不可复核证据=PENDING

## 5. 已知风险和未覆盖项

- PENDING

阻塞记录：

- PENDING

评审记录：

- ui_pc：reviewer=agent:frontend-agent，independent=false，sha=5e96b09d8badd432e0d14264bfebd25d60565a35，verdict=PASS，hash=sha256:cdf4ff63516e7efd65ff4fd3ab7d7df088401491385914657623b2ac5f86d916，findings=PENDING

## 6. S/M/L 风险等级和定级理由

- 等级：S
- 是否上调：否
- 理由：PENDING

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
| enter_dev | invalidated | 进入开发015 | sha256:dd9854f868b9356139982e94a71404fb3d34e4b2700e238c19f4c76db780e9b9 |
| ship | pending | PENDING | PENDING |
| acceptance | pending | PENDING | PENDING |

enter_dev bound_to：{"diagnosis_hash":"sha256:b87d3e587db5f5ff43e59c4f57a95432a64a33327cd61b1f002e1232b9c71915","plan_hash":"sha256:6b7226e5cf94ef8060ad643777e200e736a5c18b3cd5457d7d7ac63377b1e6e2","risk_level":"S","data_policy_version":"demo-2026-11-10","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2","repos":[{"repo_id":"ui_pc","repo_name":"lumen-ui-science-pc","base_sha":"7ef79f4","planned_change_scope":["src/views/policy/simulation/interpret/InterpretWorkbench.vue"]}]}

ship bound_to：PENDING

acceptance bound_to：PENDING

## 12. 自动决策摘要

- PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
