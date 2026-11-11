# 缺陷修复报告：2253 技术发展跟踪，地理分布图展示，区域名称被标点遮挡展示不全

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-11T10:12:24.389+08:00
> 当前 cycle：cycle-001-20261111T014802+0800
> 当前内部阶段：AWAITING_ACCEPTANCE
> 验收模式：policy_only（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【2253】技术发展跟踪，地理分布图展示，区域名称被标点遮挡展示不全 |
| 内部 ID | 7164883066 |
| 当前负责人 | human:7695591354147146731 |
| 现象 | 技术发展跟踪的“地理分布图展示”中，区域标记的蓝色圆点压住区域名称首字，导致北京市显示成“京市”、天津市显示成“津市”、石家庄市显示成“家庄市”等，名称展示不全。 |

- 进入技术发展跟踪页面并完成/打开一次技术评估结果
- 切换到“地理分布图展示”
- 查看地图区域标记，区域名称首字被蓝点遮挡

## 2. 根因、需规依据和影响范围

- 根因：ResultDashboard 的简单区域标记使用 soft-workbench__map-marker-dot + soft-workbench__map-marker-label；点采用 absolute+z-index 定位，而通用 marker 的 label 没有定义水平偏移、display 或独立背景，标签从 marker 原点开始，首字落入圆点覆盖范围。
- 反证：区域名称数据已存在于 marker DOM 中，不是接口或字段缺失；问题只在简单 marker 样式出现；object marker 有 flex/gap 规则时可正常分列；飞书截图 2253 中多个城市名都以相同方式丢失首字
- 需规依据：agent-delivery/bid-reference/srs/02-科技信息展示系统/科技发展态势/技术发展跟踪.md#地理分布图展示-序号49；Feishu 2253 缺陷截图：区域名称被标点遮挡展示不全
- 影响范围：lumen-ui-science-pc 技术发展跟踪 ResultDashboard 地图简单 marker 布局；不涉及地图数据、评估结果、接口和交互语义

## 3. 改动摘要和非目标

- ui_pc：lumen-ui-science-pc，base=2e5ed3fe31cdb3039b49ecdac9aac06625e24ec9，candidate=1be171d38c94df1381d383933abf8bea02258a6c，scope=src/views/situation/tracking/styles/demo-tech-tracking.css

实现仓校验：

- ui_pc：candidate=1be171d38c94df1381d383933abf8bea02258a6c，diff_hash=sha256:865a15c37d6034488f7c782b53b320f080e719fcfed57a0ef03dcad0143e880c，git_verified=yes，files=src/views/situation/tracking/styles/demo-tech-tracking.css

非目标：不改图例、点位位置、缩放、点击下钻和技术评估数据；不改天地图底图或公共地图组件行为；不改区域名称文案

## 4. 验证矩阵和证据结果

- fix / 区域 marker 名称与圆点分离，北京市、石家庄市、沈阳市等名称完整显示，不再被圆点覆盖。：PASS；evidence=evidence/manifest.json#E-UI-2253-001
- regression / Situation 相关回归测试、类型检查与生产构建通过；object marker 规则未被覆盖。：PASS；evidence=evidence/manifest.json#E-CMD-2253-001, evidence/manifest.json#E-CMD-2253-002, evidence/manifest.json#E-CMD-2253-003

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| E-UI-2253-001 | browser | PASS | yes | yes | PENDING | 1be171d38c94df1381d383933abf8bea02258a6c | 北京市、石家庄市、沈阳市 marker 名称与圆点间距分别为 4px/8px/10px，名称完整且未裁切。 |
| E-CMD-2253-001 | test | PASS | yes | yes | PENDING | 1be171d38c94df1381d383933abf8bea02258a6c | 4 个 Situation 回归测试文件通过，排除已知无关的 innovationEvaluation 存量失败。 |
| E-CMD-2253-002 | test | PASS | yes | yes | PENDING | 1be171d38c94df1381d383933abf8bea02258a6c | vue-tsc 类型检查通过。 |
| E-CMD-2253-003 | test | PASS | yes | yes | PENDING | 1be171d38c94df1381d383933abf8bea02258a6c | Vite 生产构建通过。 |
| E-CMD-2253-004 | test | FAIL | yes | yes | PENDING | 1be171d38c94df1381d383933abf8bea02258a6c | 全量 Situation 运行仅 innovationEvaluation.test.mjs 存量断言失败；该文件与本次 CSS 修改无关，已从回归矩阵单独排除并保留原始日志。 |
| E-PIPE-2253-001 | pipeline | PASS | yes | yes | PENDING | 68de33006e2d76230e5fdbcf45c2b61e66cd058b | Pipeline 4780 全绿，镜像 68de3300 已推送，deploy:k8s 成功，gkx-lumen-pc rollout completed。 |

DB 写证据授权：

- PENDING

- manifest 校验：PASS；manifest_hash=sha256:a376c61a1547f7eb8058797fa1f8eb8248c29084f7cdb482b59466f9c65a2aa1；不可复核证据=PENDING

## 5. 已知风险和未覆盖项

- PENDING

评审记录：

- ui_pc：reviewer=agent:self-review，independent=false，sha=1be171d38c94df1381d383933abf8bea02258a6c，verdict=PASS，hash=sha256:3be0d8a068058ec93e57a7dde79dc83f29a14373f7a6927b12fec71040bab0bf，findings=residual: 全量 Situation 中 innovationEvaluation.test.mjs 存在与本次无关的存量失败

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

- ui_pc：MR=direct-dev，candidate=1be171d38c94df1381d383933abf8bea02258a6c，merge=68de33006e2d76230e5fdbcf45c2b61e66cd058b，deployed=68de33006e2d76230e5fdbcf45c2b61e66cd058b，pipeline=4780，pipeline_url=https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc/-/pipelines/4780，image=harbor.test.com/zp-tts/gkx-lumen-pc:68de3300，rollout=completed

- dev 复测：PASS；evidence=evidence/manifest.json#E-UI-2253-001, evidence/manifest.json#E-PIPE-2253-001

人工验收步骤：

- 打开技术发展跟踪页面并进入一次技术评估结果
- 切换到“地理分布图展示”
- 检查北京、天津、石家庄、沈阳等区域标记
- 确认区域名称完整显示，首字不再被蓝色圆点遮挡
- 点击区域标记，确认详情和地图交互保持正常

## 10. 人工验收步骤

- 飞书当前状态：IN PROGRESS
- 验收证据：PENDING
- 验收结论：pending
- Agent 不主动调用 `transition_state` 将缺陷置为 RESOLVED；只在飞书已出现业务状态迁移后读取并记录。

## 11. Gate 状态与绑定对象

| gate | status | token | hash |
|---|---|---|---|
| enter_dev | approved | 进入开发 | sha256:a37f9bd196221bd98ac84a6c6ba5dac2ff1e69b488b0dd0834eb48e987eac374 |
| ship | approved | 提测 | sha256:10429ca3b63e666dde06223f72280f11b9717f5611db048365bf75089b55a37e |

enter_dev bound_to：{"repos":[{"repo_id":"ui_pc","repo_name":"lumen-ui-science-pc","base_sha":"2e5ed3fe31cdb3039b49ecdac9aac06625e24ec9","planned_change_scope":["src/views/situation/tracking/styles/demo-tech-tracking.css"]}],"diagnosis_hash":"sha256:54644b991a94c6337a458439bf837626042be2a038a997e5cbebc4ca62a27b01","plan_hash":"sha256:39cce1f374e12f36e703699fac5d3577f3ece26713e1ee093a1983849844e088","risk_level":"S","data_policy_version":"demo-2026-11-10","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}

ship bound_to：{"repos":[{"repo_id":"ui_pc","candidate_sha":"1be171d38c94df1381d383933abf8bea02258a6c","diff_hash":"sha256:865a15c37d6034488f7c782b53b320f080e719fcfed57a0ef03dcad0143e880c","verification_hash":"sha256:33713e6f27299dd5925ae53a56076dc3694778ab581d84df0f6cad51f5cc1cb9","review_hash":"sha256:3be0d8a068058ec93e57a7dde79dc83f29a14373f7a6927b12fec71040bab0bf","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}],"risk_level":"S","deploy_target":"dev"}

## 12. 自动决策摘要

- PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
