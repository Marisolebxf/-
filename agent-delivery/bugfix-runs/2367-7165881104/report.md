# 缺陷修复报告：2367 科创政策全景-政策来源选地方政策时查询的是全部来源

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-14T16:44:51.307+08:00
> 当前 cycle：cycle-001-20261114T160809+0800
> 当前内部阶段：RESOLVED
> 验收模式：chat_exact（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【2367】科创政策全景-政策来源选地方政策时查询的是全部来源 |
| 内部 ID | 7165881104 |
| 当前负责人 | human:淮政玮 |
| 现象 | 科创政策全景把政策来源选成地方政策时，结果几乎等于全部来源。 |

- 打开科创政策全景政策检索
- 政策来源选地方政策
- 命中数接近未筛选的全量

## 2. 根因、需规依据和影响范围

- 根因：scope=local 的条件是层级白名单或省/市/区任一非空。国内政策几乎都有行政区，所以地方政策约 20235 条，全量约 20270 条。
- 反证：scope=national 只等于 rank=国家级；现有测试 test_scope_local_whitelist_and_admin_columns 锁住了行政区非空这段 OR
- 需规依据：agent-delivery/工程过程/04-系统集成/05-展示系统集成/测试用例/POL-L2-DS10-QRY-FE-DISP-L01-验收用例.md#检索条件条下拉变化后触发 search
- 影响范围：lumen-algo-py polan.search.scope_clause 的 local 分支；科创政策全景政策来源=地方政策

## 3. 改动摘要、跨仓 Bundle 和非目标

- Bundle 类型：单仓
- 同一飞书缺陷涉及多个仓库时仍是一个 run、一个 claim、一套 gate；各仓保留独立候选 SHA。

- innov_py：lumen-algo-py，role=PENDING，ship_order=PENDING，depends_on=PENDING，base=294f19b9e67640f8b8beefffb8562254d42e6f83，candidate=c16748a5ad3a579f69ae86ed963ec8b6d7c5be4b，scope=vendor/entan-py/polan/search.py, tests/test_policy_search_filter.py

实现仓校验：

- innov_py：candidate=c16748a5ad3a579f69ae86ed963ec8b6d7c5be4b，diff_hash=sha256:ff2fb81a32428b5176b38fde4cf18802b3702e9b52f1b603bc97b3c4b75b3b7b，git_verified=yes，files=tests/test_policy_search_filter.py, vendor/entan-py/polan/search.py

非目标：不改国家政策和海外政策的条件；不改适用地区的行政区匹配；不改前端文案

## 4. 验证矩阵和证据结果

- fix / 地方政策的 SQL 只按省级、市级、区县级、区级过滤，不再使用省市区非空：PASS；evidence=ev-pytest-scope
- regression / 国家政策、海外政策和全部来源的检索条件测试仍然通过：PASS；evidence=ev-pytest-scope

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| ev-pytest-scope | command | PASS | yes | yes | PENDING | c16748a5ad3a579f69ae86ed963ec8b6d7c5be4b | 地方政策不再包含省市区非空，国家/海外/全部的相邻测试仍通过，共 23 项 |
| ev-pipeline-5398 | command | PASS | yes | yes | PENDING | c16748a5ad3a579f69ae86ed963ec8b6d7c5be4b | 流水线 5398 自动作业全部成功，deploy:entan-api 已部署；整条状态为 manual 只因 deploy:entan-worker 未点 |

DB 写证据授权：

- PENDING

- manifest 校验：PASS；manifest_hash=sha256:3fe1d06a16d0f6c329bd8d4351a7b9f197ee15e8a42e6fbd5931dafad925e3f2；不可复核证据=PENDING

## 5. 已知风险和未覆盖项

- PENDING

阻塞记录：

- PENDING

评审记录：

- innov_py：reviewer=agent:algorithm-agent，independent=false，sha=c16748a5ad3a579f69ae86ed963ec8b6d7c5be4b，verdict=PASS，hash=sha256:18988b0c9d47cd74ab6cbe2f254ca6eb09d1af4eb37e82f50d242d822190626a，findings=PENDING

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

- innov_py：ship_order=PENDING，MR=direct-push，candidate=c16748a5ad3a579f69ae86ed963ec8b6d7c5be4b，merge=c16748a5ad3a579f69ae86ed963ec8b6d7c5be4b，deployed=c16748a5ad3a579f69ae86ed963ec8b6d7c5be4b，pipeline=5398，pipeline_url=https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-algo-py/-/pipelines/5398，image=PENDING，rollout=success

- dev 复测：PASS；evidence=ev-pytest-scope, ev-pipeline-5398

人工验收步骤：

- 打开科创政策全景，政策来源选地方政策，命中数应明显少于全部来源

## 10. 精确验收与飞书状态迁移

- 飞书当前状态：RESOLVED
- 验收证据：evidence/manifest.json#ev-pytest-scope
- 验收结论：approved
- 验收模式：chat_exact
- 验收异常：PENDING
- 验收口令：验收通过
- 审批引用：20261114164446D18049B7C802ABF68CC7
- chat_exact 验收：仅在收到完整精确消息 `验收通过` 后，经 acceptance gate 校验并由 Agent 调用飞书状态迁移。

## 11. Gate 状态与绑定对象

| gate | status | token | hash |
|---|---|---|---|
| enter_dev | approved | 进入开发 | sha256:4525f28766ef1e3545bec04ec4cfa66974484060d3ec14985fe840b0defa5568 |
| ship | approved | 提测 | sha256:02067eaac39d5b48ae642aaee91ca1ae8a53291edc4fa4432eb0769eda69b6d6 |
| acceptance | approved | 验收通过 | sha256:1fb9ccf8aa63548af056a6290771e4c2192aba761fa0b2067152de582eab7aba |

enter_dev bound_to：{"repos":[{"repo_id":"innov_py","repo_name":"lumen-algo-py","base_sha":"294f19b9e67640f8b8beefffb8562254d42e6f83","candidate_sha":null,"planned_change_scope":["vendor/entan-py/polan/search.py","tests/test_policy_search_filter.py"]}],"diagnosis_hash":"sha256:abbe3fff3e54916e2d70096432f0ca2f442e38cb6fedefb3deba68ab89c4fdb5","plan_hash":"sha256:f3494b88cd51c4b33074776e432a2b1be90336c36746aed6686107b42a375326","risk_level":"S","data_policy_version":"demo-2026-11-10","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}

ship bound_to：{"repos":[{"repo_id":"innov_py","candidate_sha":"c16748a5ad3a579f69ae86ed963ec8b6d7c5be4b","diff_hash":"sha256:ff2fb81a32428b5176b38fde4cf18802b3702e9b52f1b603bc97b3c4b75b3b7b","verification_hash":"sha256:600aa4b3369f2de687dec4a9ba86bd92305c488de0d26428068485ccad4f95ab","review_hash":"sha256:18988b0c9d47cd74ab6cbe2f254ca6eb09d1af4eb37e82f50d242d822190626a","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}],"risk_level":"S","deploy_target":"dev"}

acceptance bound_to：{"work_item_id":"7165881104","claim_id":"c92e5cce-2367","ship_gate_hash":"sha256:02067eaac39d5b48ae642aaee91ca1ae8a53291edc4fa4432eb0769eda69b6d6","dev_verification_result":"PASS","evidence_manifest_hash":"sha256:3fe1d06a16d0f6c329bd8d4351a7b9f197ee15e8a42e6fbd5931dafad925e3f2","current_status":"IN PROGRESS"}

## 12. 自动决策摘要

- PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
