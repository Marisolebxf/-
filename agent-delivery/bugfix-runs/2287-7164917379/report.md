# 缺陷修复报告：2287 全球创新监测，创新监测与分析，有空数据

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-11T23:30:54.697+08:00
> 当前 cycle：cycle-001-20261111T230903+0800
> 当前内部阶段：AWAITING_ACCEPTANCE
> 验收模式：policy_only（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【2287】全球创新监测，创新监测与分析，有空数据 |
| 内部 ID | 7164917379 |
| 当前负责人 | 徐滕强 |
| 现象 | 全球创新监测-创新监测与分析-创新价值评估表格中，“影响潜力”和“成熟度”两列大面积显示缺测。 |

- 进入全球创新监测/创新监测与分析
- 打开创新点详情中的创新价值评估
- 查看模型候选项表格
- 影响潜力、成熟度列基本为空

## 2. 根因、需规依据和影响范围

- 根因：算法库真实结果同时包含 top 与 comparable_top。前端当前直接对所有 candidates 按 value_score 截前10，单维新颖性候选因 value_score=100 大量占据主表，把具有成熟度或影响潜力的二维候选挤出；因此不是全无数据，而是候选选择未考虑维度覆盖。影响潜力在专利侧仍受血缘限制，但论文关键词存在真实影响潜力值，二维候选可如实展示，不应补 0。
- 反证：M_INNOV_POINT_VALUE precompute 中 ipc4 有 13 个 n_with_maturity 候选，keyword_patent 有 353 个，keyword_paper 有 2 个 n_with_influence 候选；当前接口 candidates 中可筛出 10 个以上至少两维可算的真实候选；影响潜力专利侧缺测是算法自评“部分支持”的真实限制，不能通过前端伪造
- 需规依据：agent-delivery/bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md#序号79 创新价值评估；agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md#1.1.1.1.4.1.4.5.3 创新价值评估
- 影响范围：lumen-ui-science-pc 全球创新监测-创新监测与分析-创新价值评估候选表；模型候选排序展示与支撑度说明

## 3. 改动摘要、跨仓 Bundle 和非目标

- Bundle 类型：单仓
- 同一飞书缺陷涉及多个仓库时仍是一个 run、一个 claim、一套 gate；各仓保留独立候选 SHA。

- ui_pc：lumen-ui-science-pc，role=PENDING，ship_order=PENDING，depends_on=PENDING，base=220b890583a3ce34408dbcacc7f30da035cefbaf，candidate=7c0e38da36fdfdf4b28e92ef17e7e382fb422ba3，scope=src/views/situation/global-innovation/models/innovationValueSelection.ts, src/views/situation/global-innovation/tabs/InnovationMonitor.vue, src/views/situation/global-innovation/innovationMonitor.test.mjs

实现仓校验：

- ui_pc：candidate=7c0e38da36fdfdf4b28e92ef17e7e382fb422ba3，diff_hash=sha256:0dadf56099c60781fcdf22c5490f84b36639541963086198560df401a3f4874e，git_verified=yes，files=src/views/situation/global-innovation/innovationMonitor.test.mjs, src/views/situation/global-innovation/models/innovationValueSelection.ts, src/views/situation/global-innovation/tabs/InnovationMonitor.vue

非目标：不修改算法库 value_score 或数据口径；不伪造影响潜力/成熟度数值；不修改后端接口；不扩展到其他创新监测模块

## 4. 验证矩阵和证据结果

- fix / 主表优先展示至少两维可算的真实候选，单维100分候选不再挤占主表：PASS；evidence=evidence/manifest.json#E-2287-INNOV-MONITOR-TEST, evidence/manifest.json#E-2287-BUG-SCREENSHOT
- boundary / 完全没有二维候选时仍展示真实单维候选兜底，不伪造维度：PASS；evidence=evidence/manifest.json#E-2287-INNOV-MONITOR-TEST
- regression / Vue/TypeScript 全仓类型检查保持通过：PASS；evidence=evidence/manifest.json#E-2287-TYPECHECK
- integration / 生产构建可正常打包创新价值候选选择模块：PASS；evidence=evidence/manifest.json#E-2287-BUILD
- integration / dev部署资源包含二维候选优先展示修复：PASS；evidence=evidence/manifest.json#E-2287-DEV-VERIFIED

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| E-2287-BUG-SCREENSHOT | ui | PASS | yes | yes | PENDING | 220b890583a3ce34408dbcacc7f30da035cefbaf | 缺陷截图：创新价值评估主表的影响潜力、成熟度列大面积缺测 |
| E-2287-INNOV-MONITOR-TEST | command | PASS | yes | yes | PENDING | 7c0e38da36fdfdf4b28e92ef17e7e382fb422ba3 | 创新价值候选选择自检通过：单维100分候选不会挤占二维候选，无二维候选时保留单维兜底 |
| E-2287-TYPECHECK | command | PASS | yes | yes | PENDING | 7c0e38da36fdfdf4b28e92ef17e7e382fb422ba3 | vue-tsc 类型检查通过 |
| E-2287-BUILD | command | PASS | yes | yes | PENDING | 7c0e38da36fdfdf4b28e92ef17e7e382fb422ba3 | Vite 生产构建通过；仅保留仓库既有的 chunk/unocss 警告 |
| E-2287-DEV-VERIFIED | ui | PASS | yes | yes | PENDING | 7c0e38da36fdfdf4b28e92ef17e7e382fb422ba3 | 流水线4912和deployment 9120成功；dev全球创新监测分块已包含二维候选优先展示和单维候选不进主表说明 |

DB 写证据授权：

- PENDING

- manifest 校验：PASS；manifest_hash=sha256:640e35f83951e51fb4a9ae498b891ea4a8b3c6bd3ee3428c9ac2d4346cacbc0b；不可复核证据=PENDING

## 5. 已知风险和未覆盖项

- 单仓前端展示修复，不改算法分数和数据口径，无数据库写入或权限风险

阻塞记录：

- PENDING

评审记录：

- ui_pc：reviewer=codex:self-review，independent=false，sha=7c0e38da36fdfdf4b28e92ef17e7e382fb422ba3，verdict=PASS，hash=sha256:9254cd6a994f2b2a726c5ddf19bb5ea630f18d5ca3ba22204d5175e5d0d48361，findings=只改变候选展示顺序，不修改 value_score 或任何缺测值；单维候选仅在完全没有二维候选时兜底；详情匹配候选也优先选择维度更完整的真实词条

## 6. S/M/L 风险等级和定级理由

- 等级：S
- 是否上调：否
- 理由：单仓前端展示修复，不改算法分数和数据口径，无数据库写入或权限风险

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

- ui_pc：ship_order=PENDING，MR=direct-dev-push，candidate=7c0e38da36fdfdf4b28e92ef17e7e382fb422ba3，merge=7c0e38da36fdfdf4b28e92ef17e7e382fb422ba3，deployed=7c0e38da36fdfdf4b28e92ef17e7e382fb422ba3，pipeline=4912，pipeline_url=https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc/-/pipelines/4912，image=PENDING，rollout=success

- dev 复测：PASS；evidence=evidence/manifest.json#E-2287-DEV-VERIFIED

人工验收步骤：

- 打开全球创新监测-创新监测与分析
- 打开创新点详情中的创新价值评估
- 确认主表优先展示二维可算候选，影响潜力和成熟度不再整体为空
- 查看模型支撑度说明，确认缺测维度未补0

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
| enter_dev | approved | 进入开发 | sha256:461cdfbc1edd98f934617c28ca361894fd9a5a40f6d58b4f8ed589dd00a8ec0b |
| ship | invalidated | 提测 | sha256:f5b470bf1afad49c8db2664e84a80f2bd5f43c7b872b04df77eee2d61d428084 |
| acceptance | pending | PENDING | PENDING |

enter_dev bound_to：{"repos":[{"repo_id":"ui_pc","repo_name":"lumen-ui-science-pc","base_sha":"220b890583a3ce34408dbcacc7f30da035cefbaf","candidate_sha":null,"planned_change_scope":["src/views/situation/global-innovation/models/innovationValueSelection.ts","src/views/situation/global-innovation/tabs/InnovationMonitor.vue","src/views/situation/global-innovation/innovationMonitor.test.mjs"]}],"diagnosis_hash":"sha256:b79b289c1f049464ca7abc012259bf427adb22bc018cfe89d2e77ab5605bf474","plan_hash":"sha256:1ee26ed52434a525afc5e8715d3986b3a1b00a99ae99b7a6dd9ec0c6e57640df","risk_level":"S","data_policy_version":"demo-2026-11-10","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}

ship bound_to：{"repos":[{"repo_id":"ui_pc","candidate_sha":"7c0e38da36fdfdf4b28e92ef17e7e382fb422ba3","diff_hash":"sha256:0dadf56099c60781fcdf22c5490f84b36639541963086198560df401a3f4874e","verification_hash":"sha256:61fa2c33eb8d3607615e8778d619059350e245c7db579f3ec2938d204069ca97","review_hash":"sha256:9254cd6a994f2b2a726c5ddf19bb5ea630f18d5ca3ba22204d5175e5d0d48361","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}],"risk_level":"S","deploy_target":"dev"}

acceptance bound_to：PENDING

## 12. 自动决策摘要

- PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
