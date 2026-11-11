# 缺陷修复报告：2254 技术发展跟踪，地理分布图展示，筛选不同技术类型分布图无反应

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-11T14:59:52.003+08:00
> 当前 cycle：cycle-001-20261111T120927+0800
> 当前内部阶段：BLOCKED
> 验收模式：policy_only（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【2254】技术发展跟踪，地理分布图展示，筛选不同技术类型分布图无反应 |
| 内部 ID | 7164837522 |
| 当前负责人 | 徐滕强 |
| 现象 | 技术发展跟踪结果页切换到地理分布图后，点击图例中的技术类型复选框只改变图例状态，地图点位没有可见变化。 |

- 进入技术发展跟踪结果页
- 切换到地理分布图展示
- 逐个取消/勾选当前勾选技术类型
- 地图点位和点位技术类型颜色未随选择变化

## 2. 根因、需规依据和影响范围

- 根因：Vue 版 ResultDashboard 的 mapPoints 迁自 demo 时丢失了图例启用态到点位颜色的映射，也没有按 selectedMapTechnologyTypeKeys 对 mapRegions 做前端即时过滤。后端虽按“区域技术类型与选中集合有交集”过滤，但同一区域通常包含多个技术类型，减少一个选中项时区域集合可能完全不变；同时点位 HTML 固定使用默认蓝色，因此用户看到筛选无反应。
- 反证：后端 TrackingController 已按 selectedMapTechnologyTypeKeys 过滤区域，不是完全未接线；mock/tracking 已有交集过滤测试，说明数据集层基础筛选逻辑存在；TiandituMap 会按 points 渲染 key 重绘，但当前点位内容未体现所选技术类型
- 需规依据：agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md#1.1.1.1.4.1.3.1.2 地理分布图展示：支持图例筛选不同技术类型
- 影响范围：lumen-ui-science-pc 技术发展跟踪结果页地理分布图；图例技术类型选择与地图点位可视化映射

## 3. 改动摘要、跨仓 Bundle 和非目标

- Bundle 类型：单仓
- 同一飞书缺陷涉及多个仓库时仍是一个 run、一个 claim、一套 gate；各仓保留独立候选 SHA。

- ui_pc：lumen-ui-science-pc，role=PENDING，ship_order=PENDING，depends_on=PENDING，base=49df406da73d6cdc5e2c607c16bbf8d5489e8985，candidate=cfca2edb62b56c6f919fb82d2c7219c2a5de4449，scope=src/views/situation/tracking/models/trackingMapFilter.ts, src/views/situation/tracking/components/ResultDashboard.vue, src/views/situation/tracking/tracking.test.mjs

实现仓校验：

- ui_pc：candidate=cfca2edb62b56c6f919fb82d2c7219c2a5de4449，diff_hash=sha256:3af1fed372003979a958c778d9f0c86a160d3966a84a8f0000ad8274941a9f38，git_verified=yes，files=src/views/situation/tracking/components/ResultDashboard.vue, src/views/situation/tracking/models/trackingMapFilter.ts, src/views/situation/tracking/tracking.test.mjs

非目标：不修改后端区域聚合口径；不修改数据库或制造 Mock 数据；不扩展到其他地图页面；不改变需规和验收标准

## 4. 验证矩阵和证据结果

- fix / 取消或切换技术类型后，地图区域按选中类型收敛，点位主类型颜色随首个命中类型切换：PASS；evidence=evidence/manifest.json#E-2254-TRACKING-TEST, evidence/manifest.json#E-2254-BUG-SCREENSHOT
- regression / 技术发展评估结果标题中文名等既有自检保持通过：PASS；evidence=evidence/manifest.json#E-2254-TRACKING-TEST
- integration / Vue/TypeScript 全仓类型检查通过：PASS；evidence=evidence/manifest.json#E-2254-TYPECHECK
- integration / 生产构建通过，新增模块可被 Vite 正常打包：PASS；evidence=evidence/manifest.json#E-2254-BUILD

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| E-2254-BUG-SCREENSHOT | ui | PASS | yes | yes | PENDING | 49df406da73d6cdc5e2c607c16bbf8d5489e8985 | 缺陷截图：技术发展跟踪地理分布图的技术类型图例筛选未产生可见地图变化 |
| E-2254-TRACKING-TEST | command | PASS | yes | yes | PENDING | cfca2edb62b56c6f919fb82d2c7219c2a5de4449 | 技术发展跟踪自检通过：原有标题回归 + 技术类型筛选与主类型颜色切换 |
| E-2254-TYPECHECK | command | PASS | yes | yes | PENDING | cfca2edb62b56c6f919fb82d2c7219c2a5de4449 | vue-tsc 类型检查通过 |
| E-2254-BUILD | command | PASS | yes | yes | PENDING | cfca2edb62b56c6f919fb82d2c7219c2a5de4449 | Vite 生产构建通过；仅保留仓库既有的 chunk/unocss 警告 |
| E-2254-FRONTEND-IMAGE-FAIL | pipeline | FAIL | yes | yes | PENDING | 71ac9e0b3558131879851e67a6165a5e701baa02 | frontend:image 连续两次因 Harbor 登录 unauthorized 失败；frontend:build 和 sonar:scan 已成功，非代码或测试失败 |
| E-2254-DEV-DEPLOY-MISMATCH | ui | FAIL | yes | yes | PENDING | a647090cfd040adabc205dfdc193e3f13b1d2425 | dev 仍返回旧入口 index-CSWdLnzv.js；本修复构建入口 index-C2fHQ1mu.js 为 404。部署的 tracking chunk 不含 map-marker-type-color，说明修复未实际部署 |

DB 写证据授权：

- PENDING

- manifest 校验：PASS；manifest_hash=sha256:110a076d6a2242d4ff2027652e752145f8160f47c367e47b713bdca2d250eb62；不可复核证据=PENDING

## 5. 已知风险和未覆盖项

- 单仓前端交互修复，无数据库写入、无后端口径变化、无权限或生产风险

评审记录：

- ui_pc：reviewer=codex:self-review，independent=false，sha=cfca2edb62b56c6f919fb82d2c7219c2a5de4449，verdict=PASS，hash=sha256:2f9714d800bf00bef098091ed9fd0a5b55c6a3bf8dbfb254e9272ed0dd0260a7，findings=后端已有交集过滤，前端补足即时可见反馈，不改变后端口径；点位 id 纳入主类型 key，确保 TiandituMap 在颜色变化时重绘；地图 HTML 对区域名称、key 和颜色值做转义，避免注入

## 6. S/M/L 风险等级和定级理由

- 等级：S
- 是否上调：否
- 理由：单仓前端交互修复，无数据库写入、无后端口径变化、无权限或生产风险

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

- PENDING

- dev 复测：PENDING；evidence=PENDING

人工验收步骤：

- PENDING

## 10. 人工验收步骤

- 飞书当前状态：IN PROGRESS
- 验收证据：PENDING
- 验收结论：pending
- Agent 不主动调用 `transition_state` 将缺陷置为 RESOLVED；只在飞书已出现业务状态迁移后读取并记录。

## 11. Gate 状态与绑定对象

| gate | status | token | hash |
|---|---|---|---|
| enter_dev | approved | 进入开发 | sha256:72edddd4f66e830d51d70facdeb27ae933ec5c9d813a771128d23526adffadaa |
| ship | invalidated | 提测 | sha256:6776192e190dd9edbd837beb293dc86ef8bd04961e78926f306e34ea9a9e5bec |

enter_dev bound_to：{"repos":[{"repo_id":"ui_pc","repo_name":"lumen-ui-science-pc","base_sha":"49df406da73d6cdc5e2c607c16bbf8d5489e8985","candidate_sha":null,"planned_change_scope":["src/views/situation/tracking/models/trackingMapFilter.ts","src/views/situation/tracking/components/ResultDashboard.vue","src/views/situation/tracking/tracking.test.mjs"]}],"diagnosis_hash":"sha256:5cec4fa5fb894aa51a5c67563dec04e93d54306d89531cd1d63de7b68517e567","plan_hash":"sha256:cb4b00da20f0e348d21743337eae6804a3b79f69fa27fbeb544737aa5b39aa87","risk_level":"S","data_policy_version":"demo-2026-11-10","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}

ship bound_to：{"repos":[{"repo_id":"ui_pc","candidate_sha":"cfca2edb62b56c6f919fb82d2c7219c2a5de4449","diff_hash":"sha256:3af1fed372003979a958c778d9f0c86a160d3966a84a8f0000ad8274941a9f38","verification_hash":"sha256:d918af98ea62159300873b5dec2cabca124dae385aa966fe4bd5b6433cf43147","review_hash":"sha256:2f9714d800bf00bef098091ed9fd0a5b55c6a3bf8dbfb254e9272ed0dd0260a7","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}],"risk_level":"S","deploy_target":"dev"}

## 12. 自动决策摘要

- PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
