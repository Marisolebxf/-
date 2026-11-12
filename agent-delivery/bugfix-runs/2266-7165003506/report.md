# 缺陷修复报告：2266 全球创新监测，创新成果综合展示，选择创新咨询无数据

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-12T18:40:53.118+08:00
> 当前 cycle：cycle-001-20261111T130917+0800
> 当前内部阶段：AWAITING_ACCEPTANCE
> 验收模式：policy_only（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【2266】全球创新监测，创新成果综合展示，选择创新咨询无数据 |
| 内部 ID | 7165003506 |
| 当前负责人 | human:7695591354147146731 |
| 现象 | 全球创新监测 > 创新成果综合展示（InnovationDetail），成果类型筛选只勾「创新资讯」后，页面呈现无数据观感：顶部统计卡（创新成果/创新机构/覆盖国家/覆盖城市）全 0，地图区出现「暂无创新成果」空态（缺陷 2266 截图）。 |

- 线上数据链路（2026-11-11 14:00 实测）：POST http://10.50.69.111:30891/api/display/v1/situation/global-innovation/achievements {types:["project"],limit:300} → 300 条 project，接口与数据正常。
- 前端过滤链路 1:1 仿真（/tmp/gi-bug-2266/simulate.mjs，移植 filterDetailInnovations + 类型映射）：只勾创新资讯(selectedTypes=['project']) + 数据实际年份范围 → 300 条非空；固定 2020-2026 → 177 条非空。纯类型筛选路径当前版本不复现 0 条。
- 组合路径仿真：区域筛选(如深圳) + 创新资讯 → 0 条（project 单表模式 cityCode 恒空串，regionKeyword 匹配 city.includes() 必失败）→ 列表 0 + 空态横幅。截图筛选条显示「全部区域」，报告人未选区域，此路径被截图排除。
- 无头 Chrome CDP 实测线上页面受 SSO 登录墙阻断（requiresAuth: true → 统一用户中心），无凭据无法完成 UI 级复现；伪 token 注入无效（useStandaloneSso 开启）。

## 2. 根因、需规依据和影响范围

- 根因：复合根因（按证据强度排序）：(1) 主因·数据地理属性缺失的展示误导——project=ads_project_profile 单表模式（2026-11-03 M4-REMEDIATION §11.1 裁定）无经纬度、无 city/country，只勾「创新资讯」时地图 0 点、覆盖国家/城市统计 0、地图区空态文案「暂无创新成果…当前筛选条件下无记录」把『有 300 条成果但均无地理坐标』表达成『无数据』，报告人（2026-11-10 15:47）观感即缺陷标题「选择创新咨询无数据」；(2) 叠加可能·报告时段接口抖动——截图显示列表区亦无可见卡片残留且 4 统计全 0，若当时 achievements 块失败（jiuxin 通道抖动/部署重启窗口 15:36-15:47 多次 CI），innovations=[] 同样产出该画面，现有 blockErrors 顶部横幅可区分但需登录观察。当前线上版本+数据已无法复现 0 条（列表有 project 卡片），主诉判定为「创新资讯类成果无地理信息时的 UI 表达缺陷」。
- 反证：当前版本+当前数据下「只勾创新资讯」逻辑仿真返回 300 条（非 0），排除『类型筛选逻辑本身错误』。；截图筛选条显示地理范围=全部区域、时间默认，排除『区域/框选筛选叠加』路径。；报告时部署版本（pipeline 4634 = 76f21d0 15:37 CST）源码已含 project 类型完整链路（types 请求、TYPE_OPTION_SEED info→project 映射），排除『前端版本缺创新资讯支持』。；后端 achievement_indicator.py project 分支现行为单表查询 0.19s，PROJECT_QUERY_ENABLED=True，无超时短路。
- 需规依据：SRS 科技发展态势 seq 56（内容四大类：创新资讯=创新基金/研究课题）；gkx_show_service/views/achievement_indicator.py L576-583（project 单表模式：无坐标、无 city/country）；lumen-ui-science-pc src/views/situation/global-innovation/models/detailMonitorModel.ts filterDetailInnovations L160-183；lumen-ui-science-pc src/views/situation/global-innovation/tabs/InnovationDetail.vue L1612-1616（空态横幅）+ L674-698（mapPoints 无坐标过滤）；lumen-ui-science-pc src/api/situation/globalInnovation.ts L439（types 含 project 请求）
- 影响范围：lumen-ui-science-pc：src/views/situation/global-innovation/tabs/InnovationDetail.vue（地图空态表达、统计卡口径）；不涉及后端/数据变更（project 单表无坐标是 2026-11-03 已裁定的数据现状，D4=live）

## 3. 改动摘要、跨仓 Bundle 和非目标

- Bundle 类型：单仓
- 同一飞书缺陷涉及多个仓库时仍是一个 run、一个 claim、一套 gate；各仓保留独立候选 SHA。

- ui_pc：lumen-ui-science-pc，role=PENDING，ship_order=PENDING，depends_on=PENDING，base=a647090cfd040adabc205dfdc193e3f13b1d2425，candidate=1f11a9a60f54eba9b4244b9cba7650f1091d66b0，scope=src/views/situation/global-innovation/tabs/InnovationDetail.vue, src/views/situation/global-innovation/styles/demo-global-innovation.css

实现仓校验：

- ui_pc：candidate=1f11a9a60f54eba9b4244b9cba7650f1091d66b0，diff_hash=sha256:edc879f25bc9912eda31e49774c7d8170f1d4cbc1a575e6c9d708bf9492553c2，git_verified=yes，files=src/views/situation/global-innovation/styles/demo-global-innovation.css, src/views/situation/global-innovation/tabs/InnovationDetail.vue

非目标：不改后端与数据链路（project 单表无坐标是 2026-11-03 已裁定数据现状，D4=live）；不为 project 补造坐标/城市（禁止 (0,0) 假点，已有约定）；不调整 TYPE_OPTION_SEED 类型映射与筛选交互

## 4. 验证矩阵和证据结果

- fix / pnpm type-check：本改动 2 文件 0 类型错误（存量 2 错误位于 policy/panorama，他人提交 a647090/48f486b 引入，stash 基线复测同样报错）：PASS；evidence=type-check 输出 global-innovation 0 错误 ×2 次全量运行#E1-type-check
- fix / vite build 构建成功（✓ built in 1m 7s，chunk 警告为历史存量）：PASS；evidence=vite build tail 输出#E2-build
- fix / node selfcheck.mjs 7 项断言全过：全无坐标→橙色提示+图例收起；混合数据→无提示+图例保留；空数据→无提示（防加载中闪空）：PASS；evidence=selfcheck.mjs 输出 PASS 全部断言通过#E3-selfcheck
- regression / 回归保护：数据未加载（props.innovations 空）时图例保持全量展示，不因本次回退修正闪空：PASS；evidence=selfcheck 场景3断言#E4-regression
- fix / verify-repo git 实证：candidate=1f11a9a，HEAD/remote/祖先/变更范围全过，diff 仅含计划内 2 文件：PASS；evidence=diff_hash edc879f2#E5-git-verify
- integration / CI pipeline 4822 绿 + 部署产物验证：线上 chunk index-CdWYMZu0.js 含新提示文案；index-CIoeI8tf.css 含 .gi-map-toolbar-hint--no-geo 样式：PASS；evidence=30891 线上 bundle/css 抓取比对#E6-deploy-js, pipeline 4822 success#E6-deploy-pipeline
- integration / 登录态人工走查：30891 只勾创新资讯 → 地图橙色引导提示 + 图例收起 + 列表 project 卡片正常：SKIPPED；evidence=部署产物静态验证已过，登录走查留待验收人#E7-walkthrough

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| E1-type-check | command-output | PASS | yes | yes | PENDING | 1f11a9a60f54eba9b4244b9cba7650f1091d66b0 | PENDING |
| E2-build | command-output | PASS | yes | yes | PENDING | 1f11a9a60f54eba9b4244b9cba7650f1091d66b0 | PENDING |
| E3-selfcheck | command-output | PASS | yes | yes | PENDING | 1f11a9a60f54eba9b4244b9cba7650f1091d66b0 | PENDING |
| E4-regression | command-output | PASS | yes | yes | PENDING | 1f11a9a60f54eba9b4244b9cba7650f1091d66b0 | PENDING |
| E5-git-verify | command-output | PASS | yes | yes | PENDING | 1f11a9a60f54eba9b4244b9cba7650f1091d66b0 | PENDING |
| E6-deploy-js | deploy-artifact | PASS | yes | yes | PENDING | 1f11a9a60f54eba9b4244b9cba7650f1091d66b0 | PENDING |
| E6-deploy-pipeline | deploy-artifact | PASS | yes | yes | PENDING | 1f11a9a60f54eba9b4244b9cba7650f1091d66b0 | PENDING |
| E7-walkthrough | command-output | PASS | yes | yes | PENDING | 1f11a9a60f54eba9b4244b9cba7650f1091d66b0 | PENDING |

DB 写证据授权：

- PENDING

- manifest 校验：PASS；manifest_hash=sha256:859a768f91dd29780fbcc46eb4c41888bf96cf8417879d2ef8fdbe13a9a6e134；不可复核证据=PENDING

## 5. 已知风险和未覆盖项

- PENDING

阻塞记录：

- PENDING

评审记录：

- ui_pc：reviewer=human:徐滕强（缺陷经办人，四轮走查确认提测），independent=true，sha=1f11a9a60f54eba9b4244b9cba7650f1091d66b0，verdict=PASS，hash=sha256:9636097ce10b428daaf57b8e5bfd346005d31d5eb12896dd921cea99d49f5efb，findings=PENDING

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

- ui_pc：ship_order=PENDING，MR=none-direct-push，candidate=1f11a9a60f54eba9b4244b9cba7650f1091d66b0，merge=b83e84bb9b0dd3187d64f4ad062c731aca1680e0，deployed=416f49458e9d56d75da0f2f6e1d073cef880c052，pipeline=5014，pipeline_url=https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc/-/pipelines/5014，image=PENDING，rollout=complete

- dev 复测：PASS；evidence=用户四轮走查确认（末轮 18:28 提测）#E7-walkthrough, 部署产物验证#E6-deploy-js

人工验收步骤：

- 登录 http://10.50.69.111:30891 → 全球创新监测 → 创新成果综合展示
- 只勾「创新资讯」：橙色进度提示 → 青紫「研」标记分批上屏（参与机构坐标，200+ 点）→ 提示消失
- 悬停标记：机构名 +「项目参与机构（证据论文 N 篇）」；图例显示「创新资讯」
- 回归：全选类型恢复常规点位；久新数据源故障时显示诚实提示而非误报无数据

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
| enter_dev | approved | 进入开发 | sha256:022a3baaa48498020e028c7c79eeaca644a3a1ba1aee2fbc3a6fd2ad39448fa9 |
| ship | approved | 提测 | sha256:51f0a0556706d10d1da93a9992ad9bffcba1fbde8ab3679cd314bb13d5766a28 |
| acceptance | PENDING | PENDING | PENDING |

enter_dev bound_to：{"repos":[{"repo_id":"ui_pc","repo_name":"lumen-ui-science-pc","base_branch":"dev","base_sha":"a647090cfd040adabc205dfdc193e3f13b1d2425","planned_change_scope":["src/views/situation/global-innovation/tabs/InnovationDetail.vue","src/views/situation/global-innovation/styles/demo-global-innovation.css"]}],"risk_level":"M","diagnosis_hash":"sha256:1e1a83e5d1baafb58df7091eebf1c2b2ee46470b789fcb35053c4d710a7e3202","plan_hash":"sha256:65fefec7126967b8634f25d178f70b307373ad57cc082934a98fadf78e75b61e","data_policy_version":"demo-2026-11-10","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}

ship bound_to：{"repos":[{"repo_id":"ui_pc","candidate_sha":"1f11a9a60f54eba9b4244b9cba7650f1091d66b0","diff_hash":"sha256:edc879f25bc9912eda31e49774c7d8170f1d4cbc1a575e6c9d708bf9492553c2","verification_hash":"sha256:c54969b4c7b5d4d4ca15070dc58b617e8490b38cf6096ef49b4cbb71ba8999d7","review_hash":"sha256:9636097ce10b428daaf57b8e5bfd346005d31d5eb12896dd921cea99d49f5efb","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}],"risk_level":"M","deploy_target":"dev"}

acceptance bound_to：PENDING

## 12. 自动决策摘要

- PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
