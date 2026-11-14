# 缺陷修复报告：014 政策效果推演-新出台政策效果预测，历史政策效果，短期和长期效果，没有数据

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-14T15:56:59.494+08:00
> 当前 cycle：cycle-001-20261114T132900+0800
> 当前内部阶段：READY_SHIP
> 验收模式：policy_only（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【014】政策效果推演-新出台政策效果预测，历史政策效果，短期和长期效果，没有数据 |
| 内部 ID | 7168131856 |
| 当前负责人 | human:淮政玮 |
| 现象 | 政策效果推演：新出台政策效果预测、历史政策效果板块的短期/长期效果无数据（P1，工单仅截图无步骤） |

- 打开 政策效果推演 页（src/views/policy/simulation）
- 新出台政策效果预测 / 历史政策效果：执行推演后查看短中长期效果区块
- 现象：短期与长期效果无数据（截图 2026-11-13 工单附件）

## 2. 根因、需规依据和影响范围

- 根因：前端解析分支缺失：灌数端 lumen-algo-py mockgen/simulation.py 直写竖线格式「短期\|2.5\|2.6\|5；中期\|…；长期\|…」「名称\|85\|良好；…」，而 simulationLive.mjs 的 termKpiItems/similarPolicyItems 在 01e86b2（去重重构）时误删竖线解析分支，导致该格式落空返回 []，短/长期效果卡无数据；非数据侧缺数
- 反证：灌数端 gapfill_policy_sim_result 的 term_kpi_text / similar_policies_text 竖线格式文本非空（mockgen 直写），数据在库；自检闭集断言：竖线格式经恢复后的解析器输出 3 期 KPI / 2 条政策，修复前同输入落空
- 需规依据：POL-L2-DS12-WIRING-L01
- 影响范围：src/views/policy/simulation/simulationLive.mjs

## 3. 改动摘要、跨仓 Bundle 和非目标

- Bundle 类型：单仓
- 同一飞书缺陷涉及多个仓库时仍是一个 run、一个 claim、一套 gate；各仓保留独立候选 SHA。

- ui_pc：lumen-ui-science-pc，role=primary，ship_order=PENDING，depends_on=PENDING，base=cf9d154383897dda04d54b2d7af432c792d1f7e9，candidate=8fff84bb76e9c825e2e8224ca8c01047e396a8fd，scope=src/views/policy/simulation/simulationLive.mjs

实现仓校验：

- ui_pc：candidate=8fff84bb76e9c825e2e8224ca8c01047e396a8fd，diff_hash=sha256:882c381b1d2cf003bbbc7424e30feb966ea7485cbf55f49ce59a38be086edf44，git_verified=yes，files=src/views/policy/simulation/simulationLive.mjs

非目标：不改灌数端格式（后端为真源）；不动 Java/Python 链路；不加新依赖

## 4. 验证矩阵和证据结果

- fix / 短/长期效果卡按灌数端竖线格式出 3 枚 KPI（termKpiItems/similarPolicyItems 恢复竖线解析，自检断言新旧两格式闭集）：PASS；evidence=ev-selfcheck
- regression / 相邻解析行为不受影响：JSON/括号兜底/空串/无结构/残期落空等闭集断言全绿；全仓 vue-tsc 类型门绿：PASS；evidence=ev-selfcheck, ev-typecheck
- boundary / 边界输入不冒充数据：单条竖线、2 期残缺、非 KPI 数字串、空串均落空返回 []，不伪造 KPI（D9 诚实空态）：PASS；evidence=ev-selfcheck

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| ev-selfcheck | selfcheck | PASS | yes | yes | PENDING | 8fff84bb76e9c825e2e8224ca8c01047e396a8fd | PENDING |
| ev-typecheck | typecheck | PASS | yes | yes | PENDING | 5e6fb49cafe84dfc32048822bc4dfd949b23dfc0 | PENDING |

DB 写证据授权：

- PENDING

- manifest 校验：PASS；manifest_hash=sha256:fc7e55babe175e02b487c492b378f18bc06602f0882d404f0b28278f72db7f21；不可复核证据=PENDING

## 5. 已知风险和未覆盖项

- PENDING

阻塞记录：

- PENDING

评审记录：

- ui_pc：reviewer=agent:coordinator-agent，independent=true，sha=8fff84bb76e9c825e2e8224ca8c01047e396a8fd，verdict=PASS，hash=sha256:e62556844a30d953a4b9ae52adbe100c59997f7a858a2884918d3d993964d44f，findings=PENDING

## 6. S/M/L 风险等级和定级理由

- 等级：M
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
| enter_dev | invalidated | 进入开发014 | sha256:fab42e4684f652a3f75720db4c0b33a9918ae5a43c41648007f81b297ed77b83 |
| ship | pending | PENDING | PENDING |
| acceptance | pending | PENDING | PENDING |

enter_dev bound_to：{"risk_level":"M","diagnosis_hash":"sha256:35d3e90ba215ee1e7cccd1ef6c85e8eb4fc6972952263492f244c7635b093936","plan_hash":"sha256:d19e7bb455d79112f2d48a536c850baef0092e6bf21695535b090cdead3eb36c","data_policy_version":"demo-2026-11-10","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2","repos":[{"repo_id":"ui_pc","repo_name":"lumen-ui-science-pc","base_sha":"cf9d154383897dda04d54b2d7af432c792d1f7e9","planned_change_scope":["src/views/policy/simulation/simulationLive.mjs"]}]}

ship bound_to：PENDING

acceptance bound_to：PENDING

## 12. 自动决策摘要

- PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
