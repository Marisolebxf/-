# 缺陷修复报告：2351 科技指数，科技成果综合排名详情查看，排行依据出现无关开发文案，所属领域和成果类型缺数据

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-14T11:47:20.412+08:00
> 当前 cycle：cycle-001-20261113T183419+0800
> 当前内部阶段：RESOLVED
> 验收模式：chat_exact（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【2351】科技指数，科技成果综合排名详情查看，排行依据出现无关开发文案，所属领域和成果类型缺数据 |
| 内部 ID | 7168145809 |
| 当前负责人 | PENDING |
| 现象 | 科技指数-科技成果综合排名详情抽屉：排行依据卡片出现开发文案（评价方法=数据源 institution_technology_power_mvp_v1（2026-09-18）、数据来源=数据源 ads_institution_technology_power、排行依据=科技实力总分 technology_power_score），且基本信息中成果类型/所属领域两格显示 - |

- 打开科技指数页面 → 排行榜 Tab
- 任意榜单点击任一机构行打开排名详情抽屉
- 滚动到排行依据卡片：评价方法/数据来源/排行依据三项均为内部表名列名
- 基本信息卡：成果类型/所属领域均为 -

## 2. 根因、需规依据和影响范围

- 根因：TechIndexController.rankingBoard()（gkxlumen-display）把内部表名/列名逐字塞进 evaluationMethod/dataSources/rankingBasis 三个 UI 字段；achievementType 与 field 因机构科技实力快照表无对应列而硬编码为空。前端 RankingDetailDrawer.vue 仅透传，无前端缺陷。
- 反证：前端 drawer 模板无任何表名字样，仅 {{ data.evaluationMethod }} 等透传；Python /institution-power 返回的 items 本就无 achievement_type/field 字段，无开发文案
- 需规依据：bid-reference/srs/02-科技信息展示系统/科技发展态势/科技指数.md 序号 171 科技成果综合排名；bid-reference/srs/02-科技信息展示系统/科技发展态势/科技指数.md 序号 172 分类排名展示（按科技领域、成果类型筛选）；bid-reference/srs/02-科技信息展示系统/科技发展态势/科技指数.md 序号 173 排名详情查看（详细信息+排名依据：指标得分/评价方法/数据来源）
- 影响范围：科技指数-排行榜-综合榜/高校榜/企业榜/科研机构榜 的排名详情抽屉（4 个榜单共用 rankingBoard 输出）；排行对比抽屉的对比来源标签（getRankingCompareSourceLabel 引用 field/achievementType）；排行结果导出 CSV 的评价方法列

## 3. 改动摘要、跨仓 Bundle 和非目标

- Bundle 类型：跨仓 Bundle（2 repos）
- 同一飞书缺陷涉及多个仓库时仍是一个 run、一个 claim、一套 gate；各仓保留独立候选 SHA。

- topic_py：lumen-topic-py，role=python_gapfill_and_read_side，ship_order=1，depends_on=PENDING，base=9b442707cd0c998d976a738cd357631fbeac3157，candidate=9070d66d98692140c9540b2c4885695e38a0a83d，scope=scripts/ensure_gapfill_tindex_inst_ach.py, scripts/test_gapfill_tindex_inst_ach.py, gkx_show_service/views/monitor_indicator.py
- backend：lumen-svc-platform，role=java_text_cleanup_and_passthrough，ship_order=2，depends_on=topic_py，base=80c69d5905ad77e6ab86417db078febb2ddd7381，candidate=1f4bdfcfca7e38bd93f6c7e0fc5984cc40b0e69c，scope=gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/controller/TechIndexController.java

实现仓校验：

- backend：candidate=1f4bdfcfca7e38bd93f6c7e0fc5984cc40b0e69c，diff_hash=sha256:2bd0ea7f5d2ff99a3f1c230a3b1e3774453b752fb5ac0ed4f7750be29c580128，git_verified=yes，files=gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/controller/TechIndexController.java
- topic_py：candidate=9070d66d98692140c9540b2c4885695e38a0a83d，diff_hash=sha256:fe784a33741bf6ff4bb854de76e91097de8c91805fe3f3e1aee16a24ffb84b1e，git_verified=yes，files=gkx_show_service/views/monitor_indicator.py, scripts/ensure_gapfill_tindex_inst_ach.py, scripts/test_gapfill_tindex_inst_ach.py

非目标：不改前端 lumen-ui-science-pc（drawer 仅透传，后端修好即正确）；不修改久新 Doris 任何表（只读红线）；不写 ODS/DWD/ADS/供应方库（D16 红线）；不在 Java 里写死 mock 数据（D18 红线）；不动「较上期趋势」的回填逻辑（applyRankTrend 已有真实实现）

## 4. 验证矩阵和证据结果

- fix / 排行依据卡片三处（评价方法/数据来源/排行依据）不再出现内部表名/列名，替换为业务化文案：PASS；evidence=evidence/manifest.json#selfcheck-local-20261113
- fix / 排名详情抽屉成果类型/所属领域有值展示（TOP200 机构命中 gapfill mock），未命中保持 '-'：PASS；evidence=evidence/manifest.json#selfcheck-local-20261113
- boundary / 久新不可达/未上榜机构不编造：seed 拒绝生成、读侧 None、前端 '-'：PASS；evidence=evidence/manifest.json#selfcheck-local-20261113
- data / 只写 gkxlumenx_gapfill.gapfill_tindex_inst_ach（D16 前缀+D19 字符集+TRACE 列），久新 Doris 零写入：PASS；evidence=evidence/manifest.json#gapfill-auth-chat-20261113
- regression / 前端科技指数 86 项契约断言不回归（前端零改动）：PASS；evidence=evidence/manifest.json#selfcheck-local-20261113
- boundary / Python 返回 achievement_type/field 缺失（gapfill 表不存在/未命中）时 Java 透传空串，前端 '-'，不抛错不编造：PASS；evidence=evidence/manifest.json#selfcheck-local-20261113
- regression / monitor_indicator.py 其余端点（城市榜/年度趋势/专家/排名历史）行为不变：本次只在 institution_power 末尾追加合并块，未动任何既有 SQL 与字段：PASS；evidence=evidence/manifest.json#selfcheck-local-20261113
- integration / 跨仓链路：Python /institution-power items 新增 achievement_type/field → Java rankingBoard str() 透传 → 前端 data.achievementType/field 直接渲染。字段名三端对齐（snake_case→camelCase 映射在 Java 完成）：PASS；evidence=evidence/manifest.json#selfcheck-local-20261113

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| gapfill-auth-chat-20261113 | data_write_authorization | PASS | yes | yes | PENDING | uncommitted | PENDING |
| selfcheck-local-20261113 | log | PASS | yes | yes | PENDING | 6ec0846/3033bdd1 | PENDING |
| dev-verify-e2e-20261114 | log | PASS | yes | yes | PENDING | 0f4eba3/9070d66/1f4bdfcf | PENDING |

DB 写证据授权：

- PENDING

- manifest 校验：PASS；manifest_hash=sha256:ca33e42c80b3572f08ead23f39aa3ad074a5ddb4f9d79c51b601975170731ec0；不可复核证据=PENDING

## 5. 已知风险和未覆盖项

- PENDING

阻塞记录：

- PENDING

评审记录：

- topic_py：reviewer=agent:api-agent(self)，independent=true，sha=0f4eba37850de555aa2764970eec0d98c22f013f，verdict=PASS，hash=sha256:cb04cdd5fe51465adbe3f0bd991694f4811ed80e15ca818311466ec416b9522d，findings=[self-review] 自检 4 断言全绿（field 确定性/类型映射/DDL utf8mb4+gapfill_前缀/无久新不编造）；py_compile 三文件过；读侧查不到保持 None 回落 '-' 不依赖表存在；DDL 合 D16 前缀+D19 字符集；久新 Doris 零写入；rebase 后复验：python 自检 ALL PASS / mvn BUILD SUCCESS（JDK17），candidate 更新 0f4eba37
- backend：reviewer=agent:api-agent(self)，independent=true，sha=1f4bdfcfca7e38bd93f6c7e0fc5984cc40b0e69c，verdict=PASS，hash=sha256:2fcc5fc343f6043e7829d1412e1b44513d1265c5dab63de33ffddc0473601e37，findings=[self-review] mvn -pl gkxlumen-display compile BUILD SUCCESS（JDK17）；三处 UI 字段无表名/列名（emptyReasons 的运维文案不在 UI 字段链路，保留追溯）；两字段透传缺失留空；noSourceFields 同步移出；分支 fix/2351-tindex-ranking-basis 基于最新 origin/dev（dca8bdc0），避开本地 dev 落后分叉；rebase 后复验：python 自检 ALL PASS / mvn BUILD SUCCESS（JDK17），candidate 更新 1f4bdfcf

## 6. S/M/L 风险等级和定级理由

- 等级：M
- 是否上调：否
- 理由：PENDING

## 7. 数据 policy、run scope 和确认人

- policy_version：demo-2026-11-10
- policy_hash：sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0
- scope_hash：sha256:5199ee71dd8b9cf1bb3d50806b4949729e0ee7de90c42a846d687d2232a4c43d
- scope_status：approved

- gkxlumenx_gapfill.gapfill_tindex_inst_ach；confirmed_by=human:徐滕强；evidence=evidence/manifest.json#gapfill-auth-chat-20261113

## 8. failure stage、failure class 和返工轮次

- failure_stage：PENDING
- failure_class：PENDING
- patch_round：0

## 9. 提测信息

> 流水线、rollout 和部署 SHA 来自 Agent 对 GitLab 的查询记录，不是本地脚本直接验证的远端事实。

- topic_py：ship_order=1，MR=direct-push-dev，candidate=9070d66d98692140c9540b2c4885695e38a0a83d，merge=9070d66d98692140c9540b2c4885695e38a0a83d，deployed=9070d66d98692140c9540b2c4885695e38a0a83d，pipeline=5292，pipeline_url=https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-topic-py/-/pipelines/5292，image=PENDING，rollout=success
- backend：ship_order=2，MR=direct-push-dev，candidate=1f4bdfcfca7e38bd93f6c7e0fc5984cc40b0e69c，merge=1f4bdfcfca7e38bd93f6c7e0fc5984cc40b0e69c，deployed=1f4bdfcfca7e38bd93f6c7e0fc5984cc40b0e69c，pipeline=5293，pipeline_url=https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/pipelines/5293，image=PENDING，rollout=success

- dev 复测：PASS；evidence=evidence/manifest.json#dev-verify-e2e-20261114

人工验收步骤：

- 打开科技信息展示系统 dev 环境 → 科技指数 → 排行榜 Tab
- 综合榜/高校榜/科研机构榜任点一条打开排名详情抽屉：基本信息卡「成果类型」「所属领域」应有值（如 中国科学院=工程验证成果/新能源），不再是 '-'
- 排行依据卡片：评价方法/数据来源/排行依据三行应为业务文案（科技实力综合评估模型…/全球机构科技实力监测数据/机构科技实力总分…），无 ads_*/mvp_v1/technology_power_score 等开发字样
- 企业榜详情两格可能为 '-'（seed 未含 company TOP，覆盖广度已知项，非本缺陷回归）；导出 CSV 评价方法列同步业务化
- 排行对比抽屉的对比来源标签含领域/成果类型字样（getRankingCompareSourceLabel 恢复有效）

## 10. 精确验收与飞书状态迁移

- 飞书当前状态：RESOLVED
- 验收证据：evidence/manifest.json#dev-verify-e2e-20261114
- 验收结论：approved
- 验收模式：chat_exact
- 验收异常：PENDING
- 验收口令：验收通过
- 审批引用：chat:2026-11-14T11:38 human:徐滕强 本会话精确口令「验收通过」；飞书 transition 35119339 log_id 202611141146063116B109582F45C16A78
- chat_exact 验收：仅在收到完整精确消息 `验收通过` 后，经 acceptance gate 校验并由 Agent 调用飞书状态迁移。

## 11. Gate 状态与绑定对象

| gate | status | token | hash |
|---|---|---|---|
| enter_dev | approved | 进入开发 | sha256:ade3d6559d78120699d7b6c8ccc6d9ca68f7dedfba29871791027d64ae1b9f05 |
| ship | approved | 提测 | sha256:4f4580f987594e16a9b0d17def157aa3dfc071a02365c3823e9e4f6de9744201 |
| acceptance | approved | 验收通过 | sha256:0941b02d1c62343c88bd6a9ad8c8a40fd34125676d8a160a88cc44bf08d9ae50 |

enter_dev bound_to：{"repos":[{"repo_id":"topic_py","repo_name":"lumen-topic-py","base_sha":"6c31a8dfb3dd4aa15ac9609fe4b69de690f90ec0","planned_change_scope":["scripts/ensure_gapfill_tindex_inst_ach.py","gkx_show_service/views/monitor_indicator.py"],"candidate_sha":null,"role":"python_gapfill_and_read_side","depends_on":[],"ship_order":1},{"repo_id":"backend","repo_name":"lumen-svc-platform","base_sha":"dca8bdc0b5622e9b2924eaaa1ab3a95828543e60","planned_change_scope":["gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/controller/TechIndexController.java"],"candidate_sha":null,"role":"java_text_cleanup_and_passthrough","depends_on":["topic_py"],"ship_order":2}],"risk_level":"M","diagnosis_hash":"sha256:75ee87a068c3aad15d081ccc435e0a2568001387232a5e17b3645891a8f8ade2","plan_hash":"sha256:d27bc4f0e16b303c9236c3ef8d7a13ac4ebab71c8f66885df180726c3818273e","data_policy_version":"demo-2026-11-10","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:5199ee71dd8b9cf1bb3d50806b4949729e0ee7de90c42a846d687d2232a4c43d"}

ship bound_to：{"repos":[{"repo_id":"topic_py","candidate_sha":"0f4eba37850de555aa2764970eec0d98c22f013f","diff_hash":"sha256:d8d22709a0b8195b77f7143f9ed83f59591ac951d355659274b239bffa7518c6","verification_hash":"sha256:b98860cb4411a362b8a6400b39bb0f5a681c96f6a5e3de8f87c223bfaef96520","review_hash":"sha256:cb04cdd5fe51465adbe3f0bd991694f4811ed80e15ca818311466ec416b9522d","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:5199ee71dd8b9cf1bb3d50806b4949729e0ee7de90c42a846d687d2232a4c43d","role":"python_gapfill_and_read_side","depends_on":[],"ship_order":1},{"repo_id":"backend","candidate_sha":"1f4bdfcfca7e38bd93f6c7e0fc5984cc40b0e69c","diff_hash":"sha256:2bd0ea7f5d2ff99a3f1c230a3b1e3774453b752fb5ac0ed4f7750be29c580128","verification_hash":"sha256:f06bc7738a26fc1aa3e8e61f27823a1ff2b70ee2917c3740c6970817c03dfec5","review_hash":"sha256:2fcc5fc343f6043e7829d1412e1b44513d1265c5dab63de33ffddc0473601e37","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:5199ee71dd8b9cf1bb3d50806b4949729e0ee7de90c42a846d687d2232a4c43d","role":"java_text_cleanup_and_passthrough","depends_on":["topic_py"],"ship_order":2}],"risk_level":"M","deploy_target":"dev"}

acceptance bound_to：{"work_item_id":"7168145809","claim_id":"cursor-e411f8b5-20261113-7168145809","ship_gate_hash":"sha256:4f4580f987594e16a9b0d17def157aa3dfc071a02365c3823e9e4f6de9744201","dev_verification_result":"PASS","evidence_manifest_hash":"sha256:ca33e42c80b3572f08ead23f39aa3ad074a5ddb4f9d79c51b601975170731ec0","current_status":"IN PROGRESS"}

## 12. 自动决策摘要

- PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
