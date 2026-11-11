# 缺陷修复报告：2021 科技全域态势，关键词检索提示检索服务不可用，且展示两个✗号

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-11T13:05:47.933+08:00
> 当前 cycle：cycle-001-20261111T111344+0800
> 当前内部阶段：RESOLVED
> 验收模式：policy_only（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【2021】科技全域态势，关键词检索提示检索服务不可用，且展示两个✗号 |
| 内部 ID | 7161805594 |
| 当前负责人 | human:7695591354147146731 |
| 现象 | 科技全域态势关键词检索：输入后提示「检索服务不可用」；搜索框右侧同时出现两个清除用的 ✗。 |

- 打开科技全域态势（真实轨 USE_MOCK=false）
- 在顶部「关键词检索」输入任意关键字
- 观察输入框右侧清除控件数量与下拉候选面板提示文案

## 2. 根因、需规依据和影响范围

- 根因：双✗：SituationFilterBar 使用 type=search 的原生清除钮 + 自定义 IconClose 清除按钮叠层。检索不可用：前端在 result.degraded===true 或请求抛错时展示该文案；Java SituationFactorSearchController 在 Feign 调 search-py /internal/gkx-search/factors 失败时返回 degraded=true；Python 在 ES ping/初始化失败时抛 RealDataUnavailable→503。本机无法直连 10.50.69.111 复测线上是否仍为下游失败。
- 反证：需规序号4要求输入关键字后触发检索并生成候选，不是显示服务不可用；诚实降级契约要求下游不可用时才显示「检索服务不可用」，不得回落伪结果；双✗与 degraded 文案是两个独立表面；前者可单仓前端修复
- 需规依据：agent-delivery/bid-reference/srs/02-科技信息展示系统/科技发展态势/科技全域态势.md#搜索要素定位-序号4
- 影响范围：lumen-ui-science-pc：SituationFilterBar.vue 搜索框 type/清除钮；若线上仍 degraded：lumen-svc-platform Feign + lumen-topic-py factor_search + ES 可用性（可能升 L/跨仓）

## 3. 改动摘要和非目标

- ui_pc：lumen-ui-science-pc，base=4fc8d77a3cff0d095aa07861c5d57c9a0deeafc1，candidate=49df406da73d6cdc5e2c607c16bbf8d5489e8985，scope=src/views/situation/overview/components/SituationFilterBar.vue, src/views/situation/overview/situationFilterBar.test.mjs

实现仓校验：

- ui_pc：candidate=49df406da73d6cdc5e2c607c16bbf8d5489e8985，diff_hash=sha256:9f69ae3460ac5f3aa03c69305ca2d5689a2d2efddf7998a4802b4932cacd442a，git_verified=yes，files=src/views/situation/overview/components/SituationFilterBar.vue, src/views/situation/overview/situationFilterBar.test.mjs

非目标：不回落本地伪候选冒充真实检索；不新建 ES 索引补齐论文/专利/项目类目；未经确认不把环境故障当代码补丁轮次

## 4. 验证矩阵和证据结果

- fix / 关键词输入仅一个清除✗（type=text + 自定义清除）：PASS；evidence=E-FIX-2021-001
- regression / 改动不越界且保留自定义清除/清空语义：PASS；evidence=E-REG-2021-002
- boundary / 空关键词时不显示清除钮；clearSearch 仍可清空：PASS；evidence=E-BND-2021-001
- integration / factors/search 线上 degraded 复测：SKIPPED；evidence=E-INT-2021-001

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| E-FIX-2021-001 | test | PASS | yes | yes | PENDING | a89f8ab347ca60729a8f950c54108399c2c02c2d | 关键词块无 type=search，保留单一自定义清除 |
| E-REG-2021-001 | test | FAIL | yes | yes | PENDING | a89f8ab347ca60729a8f950c54108399c2c02c2d | overviewTab.test 因本机缺少 vite/node_modules 失败；回归改由 E-REG-2021-002 承载 |
| E-BND-2021-001 | code | PASS | yes | yes | PENDING | a89f8ab347ca60729a8f950c54108399c2c02c2d | 空输入时清除钮由 v-if=searchInput 隐藏，clearSearch 仍在 |
| E-INT-2021-001 | api | SKIPPED | yes | yes | PENDING | a89f8ab347ca60729a8f950c54108399c2c02c2d | 本机网络不可达，线上检索 degraded 本轮 SKIPPED |
| E-REG-2021-002 | code | PASS | yes | yes | PENDING | a89f8ab347ca60729a8f950c54108399c2c02c2d | 改动仅限计划内两文件；自定义清除钮与 clearSearch 仍保留。overviewTab.test 因本机无 vite/node_modules 未跑。 |
| E-PIPE-2021-001 | pipeline | FAIL | yes | yes | PENDING | 49df406da73d6cdc5e2c607c16bbf8d5489e8985 | Harbor unauthorized；build 绿；二次重试仍红 |
| E-PIPE-2021-002 | pipeline | PASS | yes | yes | PENDING | 0529bd13ee391205ed1fa9d15c8a5349e14db8e2 | pipeline 4790 全绿，deploy:k8s 成功；49df406 为其祖先 |
| E-DEP-2021-001 | bundle | PASS | yes | yes | PENDING | 0529bd13ee391205ed1fa9d15c8a5349e14db8e2 | 已部署前端包内关键词输入为 type=text，仅一个自定义清除钮 |
| E-DEP-2021-002 | api | PASS | yes | yes | PENDING | 0529bd13ee391205ed1fa9d15c8a5349e14db8e2 | dev 检索返回 degraded=false、12 条候选 |
| E-ACC-2021-001 | external | PASS | yes | yes | PENDING | 0529bd13ee391205ed1fa9d15c8a5349e14db8e2 | 飞书状态由人工迁移为 RESOLVED（update_time 2026-11-11T13:05:21+08:00） |

DB 写证据授权：

- PENDING

- manifest 校验：PASS；manifest_hash=sha256:cd62aa33fc1cd1b57a95b5179bc736004b9ada3699ada9e936553169735c2ddf；不可复核证据=PENDING

## 5. 已知风险和未覆盖项

- 双✗为单仓前端叠层清除钮
- 检索不可用可能涉及 Java Feign/Python ES，需可达环境确认后决定是否升级 L

评审记录：

- ui_pc：reviewer=agent:review-agent:5a9fcfed，independent=true，sha=49df406da73d6cdc5e2c607c16bbf8d5489e8985，verdict=PASS，hash=sha256:3e6bc97b83cd9a3d79480372a046aec85ddbb055cecda2ade7e551300d1c8543，findings=non-blocking: type=text loses native searchbox semantics

## 6. S/M/L 风险等级和定级理由

- 等级：M
- 是否上调：否
- 理由：双✗为单仓前端叠层清除钮；检索不可用可能涉及 Java Feign/Python ES，需可达环境确认后决定是否升级 L

## 7. 数据 policy、run scope 和确认人

- policy_version：demo-2026-11-10
- policy_hash：sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0
- scope_hash：sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2
- scope_status：pending

- PENDING

## 8. failure stage、failure class 和返工轮次

- failure_stage：pipeline
- failure_class：environment_or_release
- patch_round：0

## 9. 提测信息

> 流水线、rollout 和部署 SHA 来自 Agent 对 GitLab 的查询记录，不是本地脚本直接验证的远端事实。

- ui_pc：MR=direct-dev，candidate=49df406da73d6cdc5e2c607c16bbf8d5489e8985，merge=0529bd13ee391205ed1fa9d15c8a5349e14db8e2，deployed=0529bd13ee391205ed1fa9d15c8a5349e14db8e2，pipeline=4790，pipeline_url=https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc/-/pipelines/4790，image=harbor.test.com/zp-tts/gkx-lumen-pc:0529bd13，rollout=completed

- dev 复测：PASS；evidence=E-PIPE-2021-002, E-DEP-2021-001, E-DEP-2021-002

人工验收步骤：

- 打开 http://10.50.69.111:30891/ 进入 科技全域态势
- 在顶部「关键词检索」输入关键字（如 深圳）
- 确认输入框右侧只有 1 个 ✗，且候选面板出候选而非「检索服务不可用」
- 点该 ✗ 能清空关键词并收起候选

## 10. 人工验收步骤

- 飞书当前状态：RESOLVED
- 验收证据：evidence/manifest.json#E-ACC-2021-001
- 验收结论：approved
- Agent 不主动调用 `transition_state` 将缺陷置为 RESOLVED；只在飞书已出现业务状态迁移后读取并记录。

## 11. Gate 状态与绑定对象

| gate | status | token | hash |
|---|---|---|---|
| enter_dev | invalidated | 进入开发 | sha256:98672063396ed20948c528936331d8b1ca73eb764301c85956edbd89d4bcfedb |
| ship | approved | 提测 | sha256:201df38462ec77e0a1bb1c34f9b949082ab8b418dc43f2853d65c7b0fd3e6244 |

enter_dev bound_to：{"repos":[{"repo_id":"ui_pc","repo_name":"lumen-ui-science-pc","base_sha":"e6de9ea497ea891389c0952b3aa4ed630ecc03c1","planned_change_scope":["src/views/situation/overview/components/SituationFilterBar.vue","src/views/situation/overview/situationFilterBar.test.mjs"]}],"diagnosis_hash":"sha256:4d32ff2de9380e1374da0c9f432657adde1e57aaf65f903343cdf99b4465c738","plan_hash":"sha256:61e4101900ac4fbe8c1d77dd54b50281c79bd88ca3e8b454b7d7abd52017b69f","risk_level":"M","data_policy_version":"demo-2026-11-10","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}

ship bound_to：{"repos":[{"repo_id":"ui_pc","candidate_sha":"49df406da73d6cdc5e2c607c16bbf8d5489e8985","diff_hash":"sha256:9f69ae3460ac5f3aa03c69305ca2d5689a2d2efddf7998a4802b4932cacd442a","verification_hash":"sha256:c6ca5cbd152345739f4d1feab4f7da390aaae1b2a9bd77a0a82aef6401307931","review_hash":"sha256:3e6bc97b83cd9a3d79480372a046aec85ddbb055cecda2ade7e551300d1c8543","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}],"risk_level":"M","deploy_target":"dev"}

## 12. 自动决策摘要

- PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
