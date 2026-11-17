# 缺陷修复报告：2371 科创政策全景，政策来源、适用地区两个控件给同一个后端接口传值

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-14T15:51:45.632+08:00
> 当前 cycle：cycle-001-20261114T152610+0800
> 当前内部阶段：RESOLVED
> 验收模式：chat_exact（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【2371】科创政策全景，政策来源、适用地区两个控件给同一个后端接口传值 |
| 内部 ID | 7166023304 |
| 当前负责人 | human:淮政玮 |
| 现象 | 科创政策全景同时选择政策来源与适用地区时，两个条件看起来都没过滤。 |

- 打开科创政策全景政策检索
- 政策来源选海外政策，适用地区选北京市
- 缺陷截图里结果仍是未筛选的 61 条

## 2. 根因、需规依据和影响范围

- 根因：2026-11-11 18:17 建单时 buildPanoramaSearchQuery 把政策来源 scope 译进 level/region，和适用地区抢同一个 region 参数。同日 23:48 commit 230b519 已改为 scope 原样直传，后端 scope 子句与 region 条件 AND。
- 反证：现码 displayPanoramaQuery.ts 对 scope 写 query.scope，对适用地区写 query.region；search_policies 实算：无筛选 20270，海外 1，北京 2274，海外且北京 0
- 需规依据：agent-delivery/工程过程/04-系统集成/05-展示系统集成/测试用例/POL-L2-DS10-QRY-FE-DISP-L01-验收用例.md#检索条件条下拉变化后触发 search
- 影响范围：lumen-ui-science-pc 科创政策全景检索条；lumen-algo-py /internal/policy/search 的 scope 与 region

## 3. 改动摘要、跨仓 Bundle 和非目标

- Bundle 类型：单仓
- 同一飞书缺陷涉及多个仓库时仍是一个 run、一个 claim、一套 gate；各仓保留独立候选 SHA。

- ui_pc：lumen-ui-science-pc，role=PENDING，ship_order=PENDING，depends_on=PENDING，base=fc9403a476d351a6ba514867d73ae3a18c43d3bd，candidate=230b51909563d4d3c9b3c6a26b36453144cde99f，scope=src/views/policy/panorama/search/displayPanoramaQuery.ts, src/views/policy/panorama/search/displayPanoramaQuery.compliance.test.mjs

实现仓校验：

- ui_pc：candidate=230b51909563d4d3c9b3c6a26b36453144cde99f，diff_hash=sha256:2ed0ef6386ce78130b120c61f1d6baddfb20c31a7b7deed5acfd06e9fac55657，git_verified=yes，files=src/views/policy/panorama/search/displayPanoramaQuery.compliance.test.mjs, src/views/policy/panorama/search/displayPanoramaQuery.ts

非目标：不改 2367 的地方政策 SQL（省级或行政区非空仍会命中绝大多数国内政策）；不改适用地区的 province/city/district 匹配

## 4. 验证矩阵和证据结果

- fix / 政策来源海外政策与适用地区北京市同时选择时，查询分别携带 scope=overseas 与 region=北京：PASS；evidence=ev-scope-region
- regression / 政策检索查询映射、空响应和分享路径的既有合规自检仍然通过：PASS；evidence=ev-compliance

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| ev-scope-region | command | PASS | yes | yes | PENDING | 230b51909563d4d3c9b3c6a26b36453144cde99f | 海外政策加北京市同时传 scope=overseas 与 region=北京 |
| ev-compliance | command | PASS | yes | yes | PENDING | 230b51909563d4d3c9b3c6a26b36453144cde99f | 政策检索查询合规自检全绿，scope 不再派生 region |
| ev-pipeline-5382 | command | PASS | yes | yes | PENDING | 37a87de1c421928c0ea99d3aa990a61cb998c54d | dev 尖端流水线 5382 成功，deploy:k8s 成功，且包含修复提交 230b519 |

DB 写证据授权：

- PENDING

- manifest 校验：PASS；manifest_hash=sha256:95f0a1cfa9bc89c6738d07875db04acfe7dba3f8dc739f5a018226db4f4c12bf；不可复核证据=PENDING

## 5. 已知风险和未覆盖项

- PENDING

阻塞记录：

- PENDING

评审记录：

- ui_pc：reviewer=agent:frontend-agent，independent=false，sha=230b51909563d4d3c9b3c6a26b36453144cde99f，verdict=PASS，hash=sha256:a6f3f5f4157fb580801d62dbe20b00a317b0371a06d7d9dd92517e1a210e136d，findings=PENDING

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

- ui_pc：ship_order=PENDING，MR=direct-push，candidate=230b51909563d4d3c9b3c6a26b36453144cde99f，merge=37a87de1c421928c0ea99d3aa990a61cb998c54d，deployed=37a87de1c421928c0ea99d3aa990a61cb998c54d，pipeline=5382，pipeline_url=https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc/-/pipelines/5382，image=PENDING，rollout=success

- dev 复测：PASS；evidence=ev-scope-region, ev-pipeline-5382

人工验收步骤：

- 打开科创政策全景检索，政策来源选海外政策，适用地区选北京市，结果应少于只选其中一项

## 10. 精确验收与飞书状态迁移

- 飞书当前状态：RESOLVED
- 验收证据：evidence/manifest.json#ev-scope-region
- 验收结论：approved
- 验收模式：chat_exact
- 验收异常：PENDING
- 验收口令：验收通过
- 审批引用：2026111415514050EB655E9F11D9DB21B9
- chat_exact 验收：仅在收到完整精确消息 `验收通过` 后，经 acceptance gate 校验并由 Agent 调用飞书状态迁移。

## 11. Gate 状态与绑定对象

| gate | status | token | hash |
|---|---|---|---|
| enter_dev | approved | 进入开发 | sha256:b5c242cc121bde91ad167efe9670bb6ce054847b3479799aaea9123379a61e40 |
| ship | approved | 提测 | sha256:f964d9dcd8e5cabb1a67608093850841cc7d5bbdc20a13f951824280644da6dd |
| acceptance | approved | 验收通过 | sha256:215fa7ad89c7e58375e838de64d9b4b78426f9cf1cbae78d04dfd6a28868911e |

enter_dev bound_to：{"repos":[{"repo_id":"ui_pc","repo_name":"lumen-ui-science-pc","base_sha":"fc9403a476d351a6ba514867d73ae3a18c43d3bd","candidate_sha":null,"planned_change_scope":["src/views/policy/panorama/search/displayPanoramaQuery.ts","src/views/policy/panorama/search/displayPanoramaQuery.compliance.test.mjs"]}],"diagnosis_hash":"sha256:5b7f494c3fbb829ba90fbd592d36b4e13acfc95cdc4d9b2587625cdcb47ce615","plan_hash":"sha256:1a81ee6629dc71e927f12f0565648985a5661a954fdfe3bbe95332f8b6f81bbe","risk_level":"S","data_policy_version":"demo-2026-11-10","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}

ship bound_to：{"repos":[{"repo_id":"ui_pc","candidate_sha":"230b51909563d4d3c9b3c6a26b36453144cde99f","diff_hash":"sha256:2ed0ef6386ce78130b120c61f1d6baddfb20c31a7b7deed5acfd06e9fac55657","verification_hash":"sha256:6fd9020bcf08b0e265c3932dc1ad064c90aba2a1509981fb012c8b5b474cdc09","review_hash":"sha256:a6f3f5f4157fb580801d62dbe20b00a317b0371a06d7d9dd92517e1a210e136d","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}],"risk_level":"S","deploy_target":"dev"}

acceptance bound_to：{"work_item_id":"7166023304","claim_id":"c92e5cce-2371","ship_gate_hash":"sha256:f964d9dcd8e5cabb1a67608093850841cc7d5bbdc20a13f951824280644da6dd","dev_verification_result":"PASS","evidence_manifest_hash":"sha256:95f0a1cfa9bc89c6738d07875db04acfe7dba3f8dc739f5a018226db4f4c12bf","current_status":"IN PROGRESS"}

## 12. 自动决策摘要

- PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
