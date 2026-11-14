# 缺陷修复报告：2593 科技指数-指数可视化-筛选产业出现异常提示

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-14T12:48:25.677+08:00
> 当前 cycle：cycle-001-20261113T175652+0800
> 当前内部阶段：RESOLVED
> 验收模式：chat_exact（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【2593】科技指数-指数可视化-筛选产业出现异常提示 |
| 内部 ID | 7168140581 |
| 当前负责人 | PENDING |
| 现象 | 科技指数页（指数可视化展示/科技成果综合排名 Tab）筛选产业后出现堆叠 toast「请求失败：获取产业列表失败：获取产业链数据失败：undefined」，被用户视为系统异常提示。 |

- 线上 10.50.69.111:30891 科技指数页选择产业集群（如 CL-SEI-01）→ POST /display/v1/situation/tech-index/dataset 返回 200
- 返回体 noTopicPathSections=[comprehensive,university,enterprise,research]，ranking 四榜置空
- 前端 Message.info 弹「…无 topic 映射路径，产业筛选下暂为空」+ industryFilterNote info，两条堆叠 toast
- 截图里的堆栈式文案在当前 dev 代码与线上 bundle（215 个 chunk 全量扫描）均不存在，为旧版本构建产物

## 2. 根因、需规依据和影响范围

- 根因：非接口故障：HTTP 200 下游诚实置空 + 前端 info toast 堆叠（industryFilterNote 与 noTopicPathSections 各弹一条）被误读为异常；旧版构建中的「获取产业链数据失败：undefined」堆栈式报错已随迭代消失。待修点 = 前端把产业筛选导致的诚实空态从全局 toast 改为页内空态说明。
- 反证：全仓 rg「获取产业链数据失败/获取产业列表失败/请求失败：」0 命中（前端 lumen-ui-science-pc + 后端 lumen-svc-platform + 算法仓）；线上 30891 前端 215 个 JS chunk 全量下载扫描，均无该文案；ti chunk（index-DnUhhIeF.js）确认只有「无 topic 映射路径」info；直连 dataset 接口 CL-SEI-01 / INB1303 / slug / 15 集群载荷全部 HTTP 200 code=0，无 5xx；Loki lumen 平面 display 日志无「获取产业/请求失败」错误行；display 的「downstream returned failure」全部来自政策全景 policy/search 链路（industry_code 校验拒绝），与 tech-index 无关；Tempo trace 8b40bd26aa786b1fc4d1fc47f066b62 在两个平面均查不到（empty ring），span 层无断点证据
- 需规依据：飞书缺陷 2593 / 7168140581（科技指数-指数可视化-筛选产业出现异常提示）；数据血缘铁律 D9：诚实空态允许，但应以页内空态而非全局 toast 表达
- 影响范围：repos/lumen-ui-science-pc src/views/situation/tech-index/index.vue（loadDataset 的 info toast 逻辑）；用户体验：筛选产业后的提示形态（toast → 页内空态说明），不改后端接口与数据口径

## 3. 改动摘要、跨仓 Bundle 和非目标

- Bundle 类型：单仓
- 同一飞书缺陷涉及多个仓库时仍是一个 run、一个 claim、一套 gate；各仓保留独立候选 SHA。

- ui_pc：lumen-ui-science-pc，role=frontend，ship_order=PENDING，depends_on=PENDING，base=d5db467e093820f6c018874326c6b7a133c22b28，candidate=2efd81b12cbaa48b8d2d4316f743404caa36f521，scope=src/views/situation/tech-index/index.vue, src/views/situation/tech-index/styles/demo-tech-index.css, src/views/situation/tech-index/techIndex.test.mjs

实现仓校验：

- ui_pc：candidate=2efd81b12cbaa48b8d2d4316f743404caa36f521，diff_hash=sha256:d4ec65eab3080a473b952fea76507219c74ca845d3ea20092fcd33f2d9115273，git_verified=yes，files=src/views/situation/tech-index/index.vue

非目标：不改后端 tech-index dataset 接口与 topic 映射口径（诚实空态语义保持）；不处理旧版本构建产物「获取产业链数据失败：undefined」文案（已消失）；不改其他页面的 toast 行为

## 4. 验证矩阵和证据结果

- fix / pnpm type-check（vue-tsc --build）exit 0：PASS；evidence=EV-selftest
- fix / pnpm build 生产构建成功：PASS；evidence=EV-selftest
- fix / techIndex.test.mjs 90 项断言全过（含防 toast 回流 4 项）：PASS；evidence=EV-selftest, EV-export-selftest
- regression / 两轮 diff 合计仅 tech-index 3 文件+1 文件，无其他页面受影响；git_verified=true：PASS；evidence=EV-diff, EV-diff-r2
- regression / 独立 agent 评审（384d1beb）PASS：正确性/hint 移除安全/高度链不破/断言无误报/D9D10 合规逐项确认：PASS；evidence=EV-diff
- boundary / 边界：请求失败时 notice 与整页数据同寿命（既有失败静默契约）；空 notice 零 DOM：PASS；evidence=EV-diff
- fix / 用户复验反馈英文 key 暴露 → 第二轮修复：板块枚举转中文榜名、去「topic 映射路径」术语；线上 30891 新 bundle 实扫命中「暂无产业关联数据」（chunk index-BQfmnmjC）：PASS；evidence=EV-diff-r2

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| EV-diff | code_diff | PASS | yes | yes | PENDING | pending | PENDING |
| EV-selftest | test_run | PASS | yes | yes | PENDING | pending | PENDING |
| EV-export-selftest | test_run | PASS | yes | yes | PENDING | pending | PENDING |
| EV-diff-round2 | code_diff | PASS | yes | yes | PENDING | 2efd81b | PENDING |
| EV-diff-r2 | code_diff | PASS | yes | yes | PENDING | 2efd81b | PENDING |

DB 写证据授权：

- PENDING

- manifest 校验：PASS；manifest_hash=sha256:9f3cf1a46eaab1c16eadbcbf0a4d1114ca69d2508311a61b75785dfca428dffa；不可复核证据=PENDING

## 5. 已知风险和未覆盖项

- PENDING

阻塞记录：

- PENDING

评审记录：

- ui_pc：reviewer=agent:review-agent，independent=true，sha=be38a6a6f602dd2239bb2d0980af8819f39afefd，verdict=PASS，hash=sha256:bee635a1a69c3534758014b3dcf5d9997445e1ef8b660ba54f7194c0b00f3e42，findings=PENDING

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

- ui_pc：ship_order=PENDING，MR=direct-push-dev，candidate=2efd81b12cbaa48b8d2d4316f743404caa36f521，merge=2efd81b12cbaa48b8d2d4316f743404caa36f521，deployed=2efd81b12cbaa48b8d2d4316f743404caa36f521，pipeline=auto-on-dev，pipeline_url=https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc/-/pipelines，image=gkx-lumen-pc:dev-2efd81b，rollout=complete

- dev 复测：PASS；evidence=EV-selftest, EV-diff-r2

人工验收步骤：

- 打开 http://10.50.69.111:30891/display/ 科技指数页「指数可视化展示」Tab（强刷 Ctrl+Shift+R）
- 产业领域筛选选择任一产业集群（如 新一代信息技术）
- 确认页面顶部一条页内说明，文案为中文榜名（综合榜/高校榜/企业榜/科研机构榜）+「暂无产业关联数据」，无英文编码、无 toast 弹窗
- 清空产业筛选，说明消失、数据恢复全量
- 「科技成果综合排名」Tab 重复确认

## 10. 精确验收与飞书状态迁移

- 飞书当前状态：RESOLVED
- 验收证据：evidence/manifest.json#EV-diff-r2
- 验收结论：approved
- 验收模式：chat_exact
- 验收异常：PENDING
- 验收口令：验收通过
- 审批引用：chat:cursor-1886ed47:2026-11-14T12:31 用户消息「验收通过」
- chat_exact 验收：仅在收到完整精确消息 `验收通过` 后，经 acceptance gate 校验并由 Agent 调用飞书状态迁移。

## 11. Gate 状态与绑定对象

| gate | status | token | hash |
|---|---|---|---|
| enter_dev | approved | 进入开发 | sha256:c10bcb8bef93245fc2b039ea21b96693ea0c220a6e71e8ef8c4461e8ca382997 |
| ship | approved | 提测 | sha256:f1b362e335dd0f9aefc6702cf77691efe9b03119d9c8ee57bac3cf7758c6508d |
| acceptance | approved | 验收通过 | sha256:8bfd867e9b5a676f93ee6458896a1513ef57363df3960ea636ab2c0d6f4d6345 |

enter_dev bound_to：{"repos":[{"repo_id":"ui_pc","repo_name":"lumen-ui-science-pc","remote":"https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc.git","base_branch":"dev","base_sha":"d5db467e093820f6c018874326c6b7a133c22b28","planned_change_scope":["src/views/situation/tech-index/index.vue","src/views/situation/tech-index/styles/demo-tech-index.css","src/views/situation/tech-index/techIndex.test.mjs"]}],"risk_level":"M","diagnosis_hash":"sha256:e19d71f2c39e76284f946776630242b4ff59cb2b126ae4ada61f6f028a5a1bbf","plan_hash":"sha256:1727b107beac59048f8f501e9282dd9ad6c264ea0ad06aea6a69777d2cad52bb","data_policy_version":"demo-2026-11-10","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}

ship bound_to：{"repos":[{"repo_id":"ui_pc","candidate_sha":"be38a6a6f602dd2239bb2d0980af8819f39afefd","diff_hash":"sha256:f5dcfc399b8a2a47bbe3cf38c9761383109b174bec409becbe2e0a6f5bd56ce5","verification_hash":"sha256:b055b8688e5d64363662f7d58f0aa1adecb239eddd3bba664ba53923f8e6ba41","review_hash":"sha256:bee635a1a69c3534758014b3dcf5d9997445e1ef8b660ba54f7194c0b00f3e42","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}],"risk_level":"M","deploy_target":"dev"}

acceptance bound_to：{"work_item_id":"7168140581","claim_id":"2593","ship_gate_hash":"sha256:f1b362e335dd0f9aefc6702cf77691efe9b03119d9c8ee57bac3cf7758c6508d","dev_verification_result":"PASS","evidence_manifest_hash":"sha256:9f3cf1a46eaab1c16eadbcbf0a4d1114ca69d2508311a61b75785dfca428dffa","current_status":"IN PROGRESS"}

## 12. 自动决策摘要

- PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
