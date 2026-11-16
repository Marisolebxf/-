# 缺陷修复报告：2621 科技发展规划-综合发展规划，推送设置里关注领域没有内容

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-16T13:35:13.216+08:00
> 当前 cycle：cycle-001-20261116T122951+0800
> 当前内部阶段：AWAITING_ACCEPTANCE
> 验收模式：policy_only（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【2621】科技发展规划-综合发展规划，推送设置里关注领域没有内容 |
| 内部 ID | 7168907585 |
| 当前负责人 | PENDING |
| 现象 | 推送设置弹窗『关注领域』a-select 仅 tags 模式且未绑定 :options，下拉无任何候选项；真实轨道 subscriptions 为空时回退 fields:[]，弹窗呈现空白 |

- 打开 /trend/tech-development-plan 综合发展规划页签 → 科创资源整合与推送卡 → 推送设置 → 点击关注领域下拉，无候选项

## 2. 根因、需规依据和影响范围

- 根因：OverviewTab.vue L1134-1140 关注领域 a-select 未绑定 :options（对照同弹窗 L1144 推送频率 select 有 :options 正常渲染）；页面无任何领域字典供给该下拉
- 反证：推送频率 select 有 :options 渲染正常，排除弹窗级样式/组件故障；mock 轨道 subscriptions 有默认 fields 但下拉依旧无候选，排除『仅数据为空』假设
- 需规依据：agent-delivery/bid-reference/srs/02-科技信息展示系统/科技发展态势/科技发展规划.md#seq183/五级:综合发展规划/科创资源整合与推送（设置关注领域和推送条件，n/a_ops 壳）
- 影响范围：lumen-ui-science-pc/src/views/situation/tech-development-plan/tabs/OverviewTab.vue（推送设置弹窗模板与脚本）

## 3. 改动摘要、跨仓 Bundle 和非目标

- Bundle 类型：单仓
- 同一飞书缺陷涉及多个仓库时仍是一个 run、一个 claim、一套 gate；各仓保留独立候选 SHA。

- ui_pc：lumen-ui-science-pc，role=PENDING，ship_order=PENDING，depends_on=PENDING，base=02c620bbd8d52151c095e3b4e4b1317b87414bc2，candidate=2a2ea83ac14f39b5959432ff21e882d66f54049d，scope=src/views/situation/tech-development-plan/tabs/OverviewTab.vue

实现仓校验：

- ui_pc：candidate=2a2ea83ac14f39b5959432ff21e882d66f54049d，diff_hash=sha256:9ce99a5a217264ff5b91cc10e87801965a70c0aeda1ef3ef2178b77cbc880261，git_verified=yes，files=src/views/situation/tech-development-plan/tabs/OverviewTab.vue

非目标：不改 POST/GET resource-push/subscriptions 接口契约；不动推送频率/渠道逻辑；不引入新的后端字段或表结构

## 4. 验证矩阵和证据结果

- fix / 推送设置弹窗关注领域下拉点开后呈现非空领域候选列表（具身智能/量子计算/合成生物学/人工智能大模型等真实字典项），DOM listbox + 截图双证据：PASS；evidence=E-IMG-001
- regression / 已保存订阅回显不受影响：默认 fields『人工智能』以选中 tag 形态回显在下拉框：PASS；evidence=E-IMG-001
- regression / npm run type-check（vue-tsc）0 错误；npm run build-only vite 构建 4619 模块通过：PASS；evidence=E-LOG-001

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| E-IMG-001 | screenshot | PASS | yes | yes | PENDING | 771967a42114f2b115f249fdf195b0eed341105a | PENDING |
| E-LOG-001 | log | PASS | yes | yes | PENDING | 771967a42114f2b115f249fdf195b0eed341105a | PENDING |
| E-DEPLOY-001 | log | PASS | yes | yes | PENDING | 2a2ea83ac14f39b5959432ff21e882d66f54049d | PENDING |

DB 写证据授权：

- PENDING

- manifest 校验：PASS；manifest_hash=sha256:f9bd7b72b0ed70fccd916f02b5ec6556bf657a3b841d1ed9cc316169a23f7a4b；不可复核证据=PENDING

## 5. 已知风险和未覆盖项

- PENDING

阻塞记录：

- PENDING

评审记录：

- ui_pc：reviewer=agent:zcode（自审，S-lite 豁免独立评审），independent=false，sha=2a2ea83ac14f39b5959432ff21e882d66f54049d，verdict=PASS，hash=sha256:2f3c3be569cbf046faf2b321d9f16ba012d03b421e9e7c25880b09e88cdf710f，findings=PENDING

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

- ui_pc：ship_order=PENDING，MR=none-direct-push-dev，candidate=2a2ea83ac14f39b5959432ff21e882d66f54049d，merge=2a2ea83ac14f39b5959432ff21e882d66f54049d，deployed=2a2ea83ac14f39b5959432ff21e882d66f54049d，pipeline=5568，pipeline_url=https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc/-/pipelines/5568，image=2a2ea83a，rollout=success

- dev 复测：PASS；evidence=E-DEPLOY-001

人工验收步骤：

- 登录 https://edu.itic-sci.com/tid/（领导驾驶舱用户）→ 科技发展态势 → 科技发展规划
- 综合发展规划页签 → 科创资源整合与推送卡 → 点『推送设置』
- 关注领域下拉点开：应呈现非空领域候选列表（具身智能/量子计算/合成生物学/人工智能大模型等）
- 已保存的关注领域（如人工智能）应回显为选中标签；新选领域后保存提示成功
- 强刷 Ctrl+F5 确认新前端包（镜像 2a2ea83a）

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
| enter_dev | approved | 进入开发 | sha256:58d75bd0fd2a19dc93c8eb273cf7f33dddee17a98879700d8e3e3d0f9c388c47 |
| ship | approved | 提测 | sha256:c1b67259a9221000a8e1147ca402b902967822b72d519f86a5e2fce8d847bb12 |
| acceptance | pending | PENDING | PENDING |

enter_dev bound_to：{"repos":[{"repo_id":"ui_pc","repo_name":"lumen-ui-science-pc","base_sha":"02c620bbd8d52151c095e3b4e4b1317b87414bc2","planned_change_scope":["src/views/situation/tech-development-plan/tabs/OverviewTab.vue"]}],"risk_level":"S","diagnosis_hash":"sha256:7230db1e59cc91645e50ad287c9dd4d81b01cf2e36f15aa8162c989b3c35bf45","plan_hash":"sha256:edc505bab9338a78125890a5bf3946905125d00a03c1153bca1e89905b84a690","data_policy_version":"demo-2026-11-10","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}

ship bound_to：{"repos":[{"repo_id":"ui_pc","candidate_sha":"2a2ea83ac14f39b5959432ff21e882d66f54049d","diff_hash":"sha256:9ce99a5a217264ff5b91cc10e87801965a70c0aeda1ef3ef2178b77cbc880261","verification_hash":"sha256:39aa5578ddcff3349eebbcd4abc3b6ba4d6582317a30922b918c102c271fab8f","review_hash":"sha256:2f3c3be569cbf046faf2b321d9f16ba012d03b421e9e7c25880b09e88cdf710f","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:dab94ad9d1ee0032538752e9d0c571b97dd2aec3998e58b90f7af3b2c80d25c2"}],"risk_level":"S","deploy_target":"dev"}

acceptance bound_to：PENDING

## 12. 自动决策摘要

- PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
