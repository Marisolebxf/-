# 缺陷修复报告：001 科创政策全景-检索历史、收藏、分组名称会显示code应该显示name

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-12T02:49:06.602+08:00
> 当前 cycle：cycle-001-20261111T225448+0800
> 当前内部阶段：AWAITING_ACCEPTANCE
> 验收模式：policy_only（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【001】科创政策全景-检索历史、收藏、分组名称会显示code应该显示name |
| 内部 ID | 7164904200 |
| 当前负责人 | PENDING |
| 现象 | 科创政策全景 live（USE_MOCK=false）下按类别分组标签、二次筛类别 facets、收藏夹条目描述显示英文 code other，应显示中文名（用户裁定：other→其他） |

- USE_MOCK=false 打开科创政策全景，检索任意词
- 结果区切「按类别分组」视图，观察含 category=other 的政策分组标题显示 other
- 二次筛「类别」下拉出现 other 选项；收藏夹条目描述同显 other

## 2. 根因、需规依据和影响范围

- 根因：政策行 category=other 时 categoryLabelMap（index.vue L362，来自 policyCategories+POLICY_TYPE_OPTIONS）无 other 键，groupPoliciesByCategory/buildRefineFacetOptions/收藏描述按 label 或 key 原样回显 code；demo 原型（demo-ui-science displaySearchResultUtils.js L280）同源继承该兜底
- 反证：检索历史标签为用户输入查询词，不含类别 code，不在本缺陷范围；USE_MOCK=true 时种子类别均有中文 label，不复现
- 需规依据：agent-delivery/bid-reference/srs/02-科技信息展示系统/科技政策跟踪/科创政策全景.md#序号200-检索结果筛选与分类；agent-delivery/bid-reference/srs/02-科技信息展示系统/科技政策跟踪/科创政策全景.md#序号201-检索历史与收藏
- 影响范围：lumen-ui-science-pc:src/views/policy/panorama/index.vue（分组标题/二次筛/收藏描述接线）；lumen-ui-science-pc:src/views/policy/panorama/search/displaySearchResultUtils.ts（groupPoliciesByCategory/buildRefineFacetOptions）

## 3. 改动摘要、跨仓 Bundle 和非目标

- Bundle 类型：单仓
- 同一飞书缺陷涉及多个仓库时仍是一个 run、一个 claim、一套 gate；各仓保留独立候选 SHA。

- ui_pc：lumen-ui-science-pc，role=primary，ship_order=1，depends_on=PENDING，base=873fec6fe50416cb4e9e66af41ba58ba2174324a，candidate=aac7a4a2fcba65a392a6bbcaa580b9b00bf830c7，scope=src/views/policy/panorama/search/displaySearchResultUtils.ts, src/views/policy/panorama/search/displayOtherCategory.selfcheck.mjs, src/views/policy/panorama/index.vue

实现仓校验：

- ui_pc：candidate=aac7a4a2fcba65a392a6bbcaa580b9b00bf830c7，diff_hash=sha256:11af6075d432bd13779c2817795385948a44f482e9ea72f1ff684e7849f50c48，git_verified=yes，files=src/views/policy/panorama/index.vue, src/views/policy/panorama/search/displayOtherCategory.selfcheck.mjs, src/views/policy/panorama/search/displaySearchResultUtils.ts

非目标：不改后端 /search/options 接口与数据；不改 mock 种子类别集（USE_MOCK=true 不受影响）；不处理检索历史 label（用户输入词，无 code）；不动其他会话 WIP（policy/analysis/**、package.json 等）

## 4. 验证矩阵和证据结果

- fix / groupPoliciesByCategory 对 category='other' 与空 category 输出 label='其他'；index.vue categoryLabelMap 含 other 键（分组标题/二次筛 facets/收藏描述三消费点统一）：PASS；evidence=v1-fix-other-category-selfcheck
- regression / 既有全景检索自检与 FE-POL-01A 主链路自检不受改动影响：PASS；evidence=v2-regression-existing-selfchecks
- regression / pnpm type-check 全量类型门 0 error：PASS；evidence=v3-typecheck
- boundary / 未知类别 code 行为不回归（map 命中则中文，未命中非 other 仍显原值）；diff 范围与授权 scope 完全一致：PASS；evidence=v1-fix-other-category-selfcheck, v4-repo-scope-verify

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| v1-fix-other-category-selfcheck | test | PASS | yes | yes | PENDING | aac7a4a2fcba65a392a6bbcaa580b9b00bf830c7 | fix 自检：other/空类别落「其他」，未知 code 不回归 |
| v2-regression-existing-selfchecks | test | PASS | yes | yes | PENDING | aac7a4a2fcba65a392a6bbcaa580b9b00bf830c7 | 回归：全景检索自检 + FE-POL-01A 主链路自检全绿 |
| v3-typecheck | test | PASS | yes | yes | PENDING | aac7a4a2fcba65a392a6bbcaa580b9b00bf830c7 | vue-tsc 0 error |
| v4-repo-scope-verify | review | PASS | yes | yes | PENDING | aac7a4a2fcba65a392a6bbcaa580b9b00bf830c7 | verify-repo PASS：changed_files 3 个均在授权 scope 内（diff_hash sha256:11af6075...c48） |
| v5-ship-pipeline-deploy | ci | PASS | yes | yes | PENDING | fc9403a476d351a6ba514867d73ae3a18c43d3bd | push up-to-date：并行会话已推送含修复的 dev；流水线 4957(4bdc7aa5) 全绿含 deploy:k8s success |
| v6-dev-deploy-chunk-check | deployment_check | PASS | yes | yes | PENDING | fc9403a476d351a6ba514867d73ae3a18c43d3bd | dev 全景页 chunk（index-C9qJsz6Z.js）含 ["other","其他"] categoryLabelMap 兜底与 d.category\|\|"other" 分组兜底，确认修复已部署 |

DB 写证据授权：

- PENDING

- manifest 校验：PASS；manifest_hash=sha256:fd942530ca6bb72e0216271398e725619ec6aed1b260167f3d820ae790ac95d6；不可复核证据=PENDING

## 5. 已知风险和未覆盖项

- PENDING

阻塞记录：

- PENDING

评审记录：

- ui_pc：reviewer=agent:coordinator-agent（S 级自审，对照 plan change_scope 逐文件核对 diff），independent=false，sha=aac7a4a2fcba65a392a6bbcaa580b9b00bf830c7，verdict=PASS，hash=sha256:c6df43102d8625f64543378a444cfc5525e55a893c2104cccea2c65409316649，findings=PENDING

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

- ui_pc：ship_order=1，MR=direct-push-dev，candidate=aac7a4a2fcba65a392a6bbcaa580b9b00bf830c7，merge=fc9403a476d351a6ba514867d73ae3a18c43d3bd，deployed=4bdc7aa50d024fcdd62dc1b486347cf1fa8988c5，pipeline=4957，pipeline_url=https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc/-/pipelines/4957，image=dev-4bdc7aa5，rollout=success

- dev 复测：PASS；evidence=v6-dev-deploy-chunk-check, v1-fix-other-category-selfcheck

人工验收步骤：

- 打开 dev 前端（edu.itic-sci.com/tid，branch dev @ 4bdc7aa5）进入「科创政策全景」检索页
- 不选类别空检索或检索出无类别数据，确认分组标题显示「其他」而非 other
- 展开某分组的二次筛选面板，确认类别 facet 同样显示「其他」
- 把一条空类别政策加入收藏，确认收藏描述里类别显示「其他」
- 回归：选「科技部」等类别检索，确认分组标题仍为对应中文且其余功能无异常

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
| enter_dev | invalidated | 进入开发 | sha256:fcd3f280c614830c599c98133638e131a21f16c270c6125faee877d5e73c2f62 |
| ship | approved | 提测 | sha256:f3a5f176f393a9f05a5acb71de2f287f237359877808464ed402acb9f04167a1 |
| acceptance | pending | PENDING | PENDING |

enter_dev bound_to：{"diagnosis_hash":"sha256:fdfcca66e971497356b9ce820363f709427457d2afcb221c3c293907b170670f","plan_hash":"sha256:ace0f105d8b35383120918f5204c003773909d5731164500ef830d4882cd3186","risk_level":"S","data_policy_version":"demo-2026-11-10","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2","repos":[{"repo_id":"ui_pc","repo_name":"lumen-ui-science-pc","base_sha":"220b890583a3ce34408dbcacc7f30da035cefbaf","planned_change_scope":["src/views/policy/panorama/search/displaySearchResultUtils.ts","src/views/policy/panorama/index.vue"],"candidate_sha":null}]}

ship bound_to：{"risk_level":"S","deploy_target":"dev","repos":[{"repo_id":"ui_pc","repo_name":"lumen-ui-science-pc","candidate_sha":"aac7a4a2fcba65a392a6bbcaa580b9b00bf830c7","diff_hash":"sha256:11af6075d432bd13779c2817795385948a44f482e9ea72f1ff684e7849f50c48","verification_hash":"sha256:f221c22c6a7b92250a785550ed1bf9862c36f5a61f34523de781bf95c62f6f2b","review_hash":"sha256:c6df43102d8625f64543378a444cfc5525e55a893c2104cccea2c65409316649","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}]}

acceptance bound_to：PENDING

## 12. 自动决策摘要

- dev 复测以部署产物静态证据替代浏览器交互走查（S 级）；依据=dev 前端 SSO 登录页依赖 edu.itic-sci.com 大 JS（3.58MB）传输，Playwright 会话中反复 ERR_SSL_PROTOCOL_ERROR / Failed to fetch，页面无法挂载、无法输入账号（无固定测试账号，此前 FE-TS-10C 曾依赖用户实时提供邮箱验证码）。改用两层等价证据：(1) dev 部署产物 index-C9qJsz6Z.js 同时含 ["other","其他"] categoryLabelMap 兜底与 d.category\|\|"other" 分组兜底，与候选 commit 逐字符同源（patch-id 79c8ee11 证实 aac7a4a=fc9403a）；(2) 同一函数逻辑已通过本地 V1 自检（v1-fix-other-category-selfcheck）。CI 全绿（流水线 4957 五 job 含 deploy:k8s success）证明构建链无回归。；备选=等网络稳定窗口重试浏览器走查（不可控时延，阻塞提测节奏） / 请用户在已登录浏览器人工点检后回填验收（与 acceptance_steps 设计一致，作为兜底路径）；影响=未做真人浏览器点检，交互层风险极低：修复为纯字符串映射兜底，无逻辑分支新增。验收步骤已写入 ship_package.acceptance_steps，由验收人在已登录会话按 5 步复核；如有异常走 REOPENED 重开。；需人工批准=no；批准人=PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
