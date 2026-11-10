# 缺陷修复报告：2023 科技全域态势，实时数据监控，选择饼图实际展示为折线图

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-10T21:44:33.641+08:00
> 当前 cycle：cycle-001-20261110T212039+0800
> 当前内部阶段：IMPLEMENTING
> 验收模式：policy_only（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【2023】科技全域态势，实时数据监控，选择饼图实际展示为折线图 |
| 内部 ID | 7161782175 |
| 当前负责人 | human:7695591354147146731 |
| 现象 | 科技全域态势-实时数据监控中，统计指标选择数量统计并点击饼图后，页面可见的论文 KPI 卡仍显示折线趋势，未出现饼图。 |

- 打开科技全域态势-实时数据监控
- 保持当前领域=不限领域，时间范围 2016-2026，在地图选择粤港澳大湾区
- 统计指标选择数量统计，点击图表类型饼图
- 观察到上方企业领域分布图未出现，页面只剩 KPI 卡；论文卡仍为年度折线

## 2. 根因、需规依据和影响范围

- 根因：图表类型控件作用于 distribution panel（visibleSlices），不作用于 KPI factor card sparkline；当前 /display/v1/situation/overview 用 scope.endYear()=2026 调用 element /domain-dist，但 ads.enterprise_domain_dist 的最新可用年份为 2025，导致 visibleSlices 为空、分布面板被隐藏；factorCardChartType 又把 pie 明确回落为 line，所以用户只看到折线。
- 反证：前端图表切换代码在 visibleSlices 非空时会根据 pie/bar/line 正常生成分布图；截图中的论文卡是 factor card，不是 distribution panel；KPI 卡趋势图按原设计 pie 回落 line；区域、要素卡和论文年度序列已有真实数据，问题不在整页鉴权或整页接口失败
- 需规依据：科技信息展示系统 SRS 1.1.1.1.4.1.1.3.2 统计指标展示功能；需规要求数量统计/分布比例/增长趋势支持柱状图、饼图、折线图展示
- 影响范围：lumen-svc-platform gkxlumen-display /display/v1/situation/overview 领域分布取数；lumen-ui-science-pc 科技全域态势 OverviewTab 分布面板与 KPI 卡展示

## 3. 改动摘要和非目标

- backend：lumen-svc-platform，base=46520a828cbcea6acd15b5537dbd2455cc03fa62，candidate=PENDING，scope=gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/controller/SituationController.java, gkxlumen-display/src/test/java/com/topcomm/gkxlumen/display/controller

实现仓校验：

- PENDING

非目标：不修改 KPI factor card 的 sparkline 语义；不新增 mock 数据；不改前端筛选范围或图表控件交互；不改其他 situation 端点

## 4. 验证矩阵和证据结果

- PENDING

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| E-UI-001 | ui | PASS | yes | yes | PENDING | 46520a828cbcea6acd15b5537dbd2455cc03fa62 | 缺陷截图：饼图按钮选中，企业领域分布面板缺失，论文 KPI 卡展示年度折线 |

DB 写证据授权：

- PENDING

- manifest 校验：PASS；manifest_hash=sha256:a76fa6eca876dc5c32280c40832e5bdd9a1e0a14f1b15c599d40d3a36ed6856d；不可复核证据=PENDING

## 5. 已知风险和未覆盖项

- 涉及后端领域分布取数年份语义和前端统计图展示联动，但不改表结构或权限
- 需要提测后验证 2016-2026 筛选下饼图真正出现

评审记录：

- PENDING

## 6. S/M/L 风险等级和定级理由

- 等级：M
- 是否上调：否
- 理由：涉及后端领域分布取数年份语义和前端统计图展示联动，但不改表结构或权限；需要提测后验证 2016-2026 筛选下饼图真正出现

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
| enter_dev | approved | 进入开发 | sha256:0071489e13c7e4f43c0be7a9e03c2ee5de53bc603ef8f4947c92a8a4ff35bb40 |
| ship | pending | PENDING | PENDING |

enter_dev bound_to：{"repos":[{"repo_id":"backend","repo_name":"lumen-svc-platform","base_sha":"46520a828cbcea6acd15b5537dbd2455cc03fa62","candidate_sha":null,"planned_change_scope":["gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/controller/SituationController.java","gkxlumen-display/src/test/java/com/topcomm/gkxlumen/display/controller"]}],"diagnosis_hash":"sha256:a5d89561c232a95ea0c5bac997d35b204589fec79cd78b1b4626d45aa80bb4ce","plan_hash":"sha256:2040cfa177cdce2538d21bd4871f9e3542f6ba3a51f8052efb33aa5f5a758f20","risk_level":"M","data_policy_version":"demo-2026-11-10","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}

ship bound_to：PENDING

## 12. 自动决策摘要

- 保持 KPI factor card 的饼图回落折线语义，仅修复企业领域分布面板的年份回退；依据=原 demo 和现有组件均明确 factorCardChartType 将 pie 映射为 line；图表类型控件作用于 distribution panel；备选=把每张 KPI 卡也改成饼图，但不同要素单位不可比且偏离原型 / 继续隐藏分布面板并禁用图表切换，但无法满足需规的饼图展示；影响=用户选择饼图后由恢复的企业领域分布面板展示饼图，KPI 卡继续展示年度 sparkline；需人工批准=no；批准人=PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
