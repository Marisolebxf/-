# 缺陷修复报告：2341 深圳创新监测报告，报告内出现无关开发文案

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-12T23:06:00.248+08:00
> 当前 cycle：cycle-001-20261112T214628+0800
> 当前内部阶段：AWAITING_ACCEPTANCE
> 验收模式：policy_only（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【2341】深圳创新监测报告，报告内出现无关开发文案 |
| 内部 ID | 7166957735 |
| 当前负责人 | PENDING |
| 现象 | 深圳创新监测报告（生成报告导出的 Word/PDF）在正式章节之外出现成段开发向文案：Doris 表名清单（ads_institution_profile 等）、「专利授权口径实测不可靠，不出数」「创新价值/排名/四维分/贡献度等字段在数仓无对应列，报告中一律不出现」「城市对比只呈现真实原始计数，不形成能力分、名次或年份预测」等内部实现说明，以「数据口径」区块和分节段落形式进入用户报告。 |

- 打开科技发展态势 → 深圳创新监测页
- 点击「生成报告」，下载/打开导出的报告文件
- 报告开头出现「数据口径」区块，第 1-4 条均为数仓表名、口径不可靠说明等开发向文案；第一节「创新载体综合展示」段落里也出现「创新价值、综合排名、四维分与贡献度在数据源数仓无对应列，报告中不呈现、不推算」

## 2. 根因、需规依据和影响范围

- 根因：src/views/situation/shenzhen-innovation/index.vue 的 buildSzInnovationReport() 把开发阶段的诚实性备注原样写进 dataNotes（渲染成报告「数据口径」区块）与分节 paragraphs。这些内容面向开发/验收（Doris 表名、数仓列缺口、口径不可靠判断），不属于 SRS seq 135 要求的用户报告内容（对比结果、竞争力分析、发展建议）。同族缺陷 7165535282（全球创新城市政策建议开发性文案）已按同样思路修复（fb63422）。
- 反证：SRS seq 135（报告生成与导出）只要求对比结果、排名情况、竞争力分析和发展建议，PDF/Word 导出；不含数据源表名或开发口径说明；同仓 7165535282 修复已确立口径：开发性文案不进用户报告 DOM/导出内容；诚实性约束保留：数据缺口不在报告里伪造数值，只是不再用开发语言表述
- 需规依据：agent-delivery/bid-reference/srs/02-科技信息展示系统/科技发展态势/深圳创新监测.md#报告生成与导出·序号135
- 影响范围：lumen-ui-science-pc/src/views/situation/shenzhen-innovation/index.vue（buildSzInnovationReport 的 dataNotes 与分节 paragraphs）；新增深圳报告文案自检测试

## 3. 改动摘要、跨仓 Bundle 和非目标

- Bundle 类型：单仓
- 同一飞书缺陷涉及多个仓库时仍是一个 run、一个 claim、一套 gate；各仓保留独立候选 SHA。

- ui_pc：lumen-ui-science-pc，role=primary，ship_order=1，depends_on=PENDING，base=fb63422662883062e7b9b37931abb62edcb19414，candidate=38b47fadce7a020157e59719f4bc96fb03834539，scope=src/views/situation/shenzhen-innovation/index.vue, src/views/situation/shenzhen-innovation/szReportCopy.test.mjs

实现仓校验：

- ui_pc：candidate=38b47fadce7a020157e59719f4bc96fb03834539，diff_hash=sha256:664a643b3fe7b5711adaafa10deb6024b0445c848acc67d3963dd4eeaab293f4，git_verified=yes，files=src/views/situation/shenzhen-innovation/index.vue, src/views/situation/shenzhen-innovation/szReportCopy.test.mjs

非目标：不改深圳页面 DOM 展示（页面上的角标/说明条不在本缺陷范围）；不改后端接口与数据口径；不为报告伪造排名/评分等缺失数据

## 4. 验证矩阵和证据结果

- fix / buildSzInnovationReport 的 dataNotes 与分节段落不再包含 Doris 表名、「口径实测不可靠不出数」「数仓无对应列不推算」等开发向文案；数据说明改为业务语言：PASS；evidence=ev-sz-report-copy-test
- regression / 深圳模块既有自检（szDomainTabFixes / szCarrierScatter）全绿，报告四章节保留，type-check 与 build 通过：PASS；evidence=ev-sz-regression-selfchecks, ev-typecheck-build
- boundary / 报告组装对数据缺口保持诚实：dataset 未加载时抛业务错误提示（不产出空报告）；coverage 为空时输出「本次暂未取到产业集群覆盖率数据」而非假设 100%：PASS；evidence=ev-sz-report-copy-test

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| ev-sz-report-copy-test | test | PASS | yes | yes | PENDING | 38b47fadce7a020157e59719f4bc96fb03834539 | szReportCopy.test.mjs 断言报告组装源码不含开发性短语、保留 SRS seq 135 四章节 |
| ev-typecheck-build | build | PASS | yes | yes | PENDING | 38b47fadce7a020157e59719f4bc96fb03834539 | pnpm type-check 与 pnpm build 均 exit 0 |
| ev-sz-regression-selfchecks | test | PASS | yes | yes | PENDING | 38b47fadce7a020157e59719f4bc96fb03834539 | 深圳模块既有自检（szDomainTabFixes 6+1 项 / szCarrierScatter）全 PASS，相邻行为未回归 |
| ev-dev-verify-deployed-chunk | deploy | PASS | yes | yes | PENDING | 5409e72ced85ccf502ad6aa7aead44b00a6ccefd | pipeline 5119 绿 + 镜像 5409e72c rollout 完成；容器内深圳 chunk（index-C5LotCzP.js）旧开发文案 0 次、新业务文案 1 次 |

DB 写证据授权：

- PENDING

- manifest 校验：PASS；manifest_hash=sha256:3821b9ead0b2c2236081a98e25ec50a4aaa0006f86b52f26b62160897872dcd3；不可复核证据=PENDING

## 5. 已知风险和未覆盖项

- PENDING

阻塞记录：

- PENDING

评审记录：

- ui_pc：reviewer=agent:frontend-agent，independent=true，sha=38b47fadce7a020157e59719f4bc96fb03834539，verdict=PASS，hash=sha256:767426002fb491e3bdede7d7a7247b06a35e7e9ae1ddd89ff18af319c1e72d38，findings=PENDING

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

- ui_pc：ship_order=1，MR=direct-dev，candidate=38b47fadce7a020157e59719f4bc96fb03834539，merge=5409e72ced85ccf502ad6aa7aead44b00a6ccefd，deployed=5409e72ced85ccf502ad6aa7aead44b00a6ccefd，pipeline=5119，pipeline_url=https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc/-/pipelines/5119，image=harbor.test.com/zp-tts/gkx-lumen-pc:5409e72c，rollout=success

- dev 复测：PASS；evidence=ev-dev-verify-deployed-chunk

人工验收步骤：

- 打开科技信息展示系统 dev 环境 → 科技发展态势 → 深圳创新监测。
- 等页面数据加载完成后点「生成报告」，下载并打开报告文件（或「打印 / 另存 PDF」预览）。
- 确认报告「数据口径」区块只出现业务语言说明（科技信息展示系统数仓按年度统计、覆盖率按实际归类、城市对比维度说明），不再出现 Doris 表名清单、「专利授权口径实测不可靠不出数」「数仓无对应列不呈现不推算」等开发向文案。
- 确认四个章节（创新载体综合展示 / 科技发展指标 / 科技领域分布 / 城市科技发展对比）与表格数据完整保留，无伪造排名/评分。

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
| enter_dev | approved | 进入开发 | sha256:0f03a34ceefd31b1732e9023c7213564114d73c350003880171ab3211341347a |
| ship | approved | 提测 | sha256:487787837bc693138949d7f294cab09cf4fd021f6f4ef190899b30ba6335f69e |
| acceptance | pending | PENDING | PENDING |

enter_dev bound_to：{"repos":[{"repo_id":"ui_pc","repo_name":"lumen-ui-science-pc","remote":"https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc.git","base_branch":"dev","base_sha":"fb63422662883062e7b9b37931abb62edcb19414","candidate_sha":null,"planned_change_scope":["src/views/situation/shenzhen-innovation/index.vue","src/views/situation/shenzhen-innovation/szReportCopy.test.mjs"],"role":"primary","depends_on":[],"ship_order":1}],"diagnosis_hash":"sha256:ef5fac7d5b167b5ac8b55248080bcefd125fff134b40abfcf2f3c2b8ef6299cc","plan_hash":"sha256:dd900eb29770f28e8a3f16967d027b77b277c44d0cbfa2f9246dd5b9391c9b51","risk_level":"M","data_policy_version":"demo-2026-11-10","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}

ship bound_to：{"repos":[{"repo_id":"ui_pc","candidate_sha":"38b47fadce7a020157e59719f4bc96fb03834539","diff_hash":"sha256:664a643b3fe7b5711adaafa10deb6024b0445c848acc67d3963dd4eeaab293f4","verification_hash":"sha256:efa61253f97bbf68984b13f41012071e15dd06115f8f0a047c0829f26f3d23f3","review_hash":"sha256:767426002fb491e3bdede7d7a7247b06a35e7e9ae1ddd89ff18af319c1e72d38","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2","role":"primary","ship_order":1,"depends_on":[]}],"risk_level":"M","deploy_target":"dev"}

acceptance bound_to：PENDING

## 12. 自动决策摘要

- PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
