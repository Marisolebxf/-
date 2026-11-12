# 缺陷修复报告：2322 粤港澳大湾区创新能力，各城市创新能力指标构成，创新机制和同比为空；表内其他城市无数据

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-12T11:48:12.351+08:00
> 当前 cycle：cycle-001-20261112T104834+0800
> 当前内部阶段：READY_SHIP
> 验收模式：policy_only（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【2322】粤港澳大湾区创新能力，各城市创新能力指标构成，创新机制和同比为空；表内其他城市无数据 |
| 内部 ID | 7165631850 |
| 当前负责人 | human:7695591354147146731 |
| 现象 | 粤港澳大湾区创新能力页“各城市创新能力指标构成”中：创新机制列始终为—，同比列始终为—；接口只返回 8 个城市，东莞/佛山/广州/惠州/江门/深圳/珠海/肇庆中仅 4 城有综合得分和四维值，其余 4 城显示 NaN（当前前端已改为—，但仍无数据）；中山、香港、澳门未出现在表中。 |

- 打开 dev：科技发展态势 → 湾区创新监测 → 粤港澳大湾区创新能力。
- 观察“各城市创新能力指标构成”：创新机制列全部为空，同比列全部为空。
- 对照接口 /display/v1/situation/bay-innovation/capability：返回 8 城，只有广州/深圳/惠州/东莞有 score 与四维子指标，佛山/江门/珠海/肇庆为 null。
- 只读核对 gkxlumenx_ads.ads_gba_capacity_index：共 11 行，仅 4 行有 capacity_index/res_index/org_index/mech_index/env_index；其余 7 行为 null。
- 只读核对 demo_gkxlumenx_ads.city_index：已有广州/深圳/东莞等部分城市历史，但不足以覆盖湾区 11 城，也没有当前接口使用的统一演示版本。

## 2. 根因、需规依据和影响范围

- 根因：链路存在三处叠加缺口：1）Python capability-score 已从 ads_gba_capacity_index 取到 4 城 mech_index，但前端 mapper 硬编码 mechanismIndex=undefined，主动丢弃机制值；2）接口没有返回同比或能力历史，前端 trend 也硬编码 undefined；3）display 聚合层只遍历 geoMetrics 返回的 8 城，未按湾区固定 11 城补行，而现有 Demo 能力表又只有 4 城有分值。结果是页面既无法展示机制/同比，也无法覆盖完整 11 城。
- 反证：SRS 序号96明确要求展示创新资源、创新机构、创新机制、创新环境子指标及贡献度；序号95要求展示当前数值和历史变化；序号107要求详情包含同比环比变化和历史趋势。；Python 接口实际已下发 indicators.mechanism，说明不是上游完全无值；问题包含前端主动隐藏。；Demo 阶段 policy demo-2026-11-10 允许在逐表 scope 批准后向 demo_gkxlumenx_ads 写 Mock；用户已明确要求合规演示阶段覆盖需规、不得改表结构、不得 Mock 久新库和正式 ADS。；demo_gkxlumenx_ads.city_index 已存在城市-期间-总分-子分-指标 JSON 结构，可在不改表结构的前提下承载 11 城演示数据和同比所需历史。
- 需规依据：agent-delivery/bid-reference/srs/02-科技信息展示系统/科技发展态势/湾区创新监测.md#序号 95 指标数值展示；agent-delivery/bid-reference/srs/02-科技信息展示系统/科技发展态势/湾区创新监测.md#序号 96 指标构成分析；agent-delivery/bid-reference/srs/02-科技信息展示系统/科技发展态势/湾区创新监测.md#序号 107 指标数据详情查看
- 影响范围：lumen-topic-py/gkx_show_service/views/gba_indicator.py：能力分改读当前 Demo 配置库的 city_index 演示版本，输出 11 城、机制、同比和历史。；lumen-topic-py/gkx_show_service/scripts/seed_gba_capacity_demo.py：幂等补齐 demo_gkxlumenx_ads.city_index 的 11 城年度演示数据。；lumen-svc-platform/gkxlumen-display/.../BayInnovationController.java：按湾区固定 11 城组装列表并透传 mechanism/trend/history。；lumen-ui-science-pc/src/api/situation/bayAreaInnovation.ts 与 CapacityTab.vue：消费并展示机制、同比、历史，不再主动隐藏。；数据写入仅限 demo_gkxlumenx_ads.city_index；不写正式 ADS、不写久新库、不改表结构。

## 3. 改动摘要、跨仓 Bundle 和非目标

- Bundle 类型：跨仓 Bundle（3 repos）
- 同一飞书缺陷涉及多个仓库时仍是一个 run、一个 claim、一套 gate；各仓保留独立候选 SHA。

- topic_py：lumen-topic-py，role=backend_python，ship_order=1，depends_on=PENDING，base=7bc646a4b1f5685128fcfdd09188b07637f14f4a，candidate=0687fb873ce53bfe41cf46c6af4c333fa4322a04，scope=gkx_show_service/views/gba_indicator.py, gkx_show_service/scripts/seed_gba_capacity_demo.py, tests/test_gba_capacity_score.py
- backend：lumen-svc-platform，role=backend_java，ship_order=2，depends_on=topic_py，base=da2260aeee781138d7b8006ce45873f471c49da1，candidate=4eb0a85919bfe97bd5f48bdeaabfcd708b078d23，scope=gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/controller/BayInnovationController.java, gkxlumen-display/src/test/java/com/topcomm/gkxlumen/display/controller/BayInnovationControllerTest.java
- ui_pc：lumen-ui-science-pc，role=frontend，ship_order=3，depends_on=backend，base=b83e84bb9b0dd3187d64f4ad062c731aca1680e0，candidate=68805b383e99cb32ba2d340646f8696e1f8067a2，scope=src/api/situation/bayAreaInnovation.ts, src/views/situation/bay-innovation/tabs/CapacityTab.vue

实现仓校验：

- topic_py：candidate=0687fb873ce53bfe41cf46c6af4c333fa4322a04，diff_hash=sha256:3afc5b114b83e1c9feaba2d85e0b6f0fcb24abc84a7722f48e9a8430986b391a，git_verified=yes，files=gkx_show_service/scripts/seed_gba_capacity_demo.py, gkx_show_service/views/gba_indicator.py, tests/test_gba_capacity_score.py
- backend：candidate=4eb0a85919bfe97bd5f48bdeaabfcd708b078d23，diff_hash=sha256:cee565d9649d81a6f450747d48576b04d809829c7499e6114c715ff9ac3581d6，git_verified=yes，files=gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/controller/BayInnovationController.java, gkxlumen-display/src/test/java/com/topcomm/gkxlumen/display/controller/BayInnovationControllerTest.java
- ui_pc：candidate=68805b383e99cb32ba2d340646f8696e1f8067a2，diff_hash=sha256:e8ea5529bac42931e48a39a5324fda2b8edb0cd04172fddbd70ad33a53a07aca，git_verified=yes，files=src/api/situation/bayAreaInnovation.ts, src/views/situation/bay-innovation/tabs/CapacityTab.vue

非目标：不修改 demo_gkxlumenx_ads.city_index 表结构。；不写 gkxlumenx_ads、久新 ODS/DWD、任何正式 ADS 或生产环境。；不伪造 geoMetrics 原始计数；原始计数仍按真实接口返回，缺城可为空。；不扩大到湾区创新监测其他 Tab 的数据口径改造。

## 4. 验证矩阵和证据结果

- fix / Python capability-score 固定返回 11 城，并以 demo_gkxlumenx_ads.city_index 的 gba-capacity-demo-v1 生成 score、四维指标、同比、历史与排名。：PASS；evidence=ev-2322-python-tests-r2, ev-2322-db-write-r2
- fix / Java capability 聚合固定输出湾区 11 城，透传 indicators、trend、history，并保留能力分空结果的降级原因。：PASS；evidence=ev-2322-java-tests-r2
- fix / 前端映射机制、同比和历史字段，并在 11 城表格、排名、雷达图和趋势图中展示。：PASS；evidence=ev-2322-ui-build-r2, ev-2322-cross-repo-contract-r2
- regression / 无演示行时仍返回 11 城空行；合法 0 子指标不被 truthy 回落吞掉；历史不足时不伪造同比。：PASS；evidence=ev-2322-python-tests-r2
- regression / 能力分服务返回空列表时仍保留 11 城，不补 0、不丢失原始计数与降级原因。：PASS；evidence=ev-2322-java-tests-r2
- regression / 前端不篡改原始 geoMetrics 计数；能力分趋势按“分”展示，不再误用论文数单位；旧机制说明依赖已移除。：PASS；evidence=ev-2322-ui-build-r2, ev-2322-cross-repo-contract-r2
- boundary / 覆盖空数据、非法/缺失能力分和合法 0 值，确保不显示 NaN、不以 0 冒充真实值。：PASS；evidence=ev-2322-python-tests-r2, ev-2322-java-tests-r2
- integration / Python 输出、Java 聚合透传和前端字段消费形成完整 11 城能力分链路，机制/同比/历史均可到达页面模型。：PASS；evidence=ev-2322-cross-repo-contract-r2, ev-2322-db-write-r2
- data / 仅向 demo_gkxlumenx_ads.city_index 幂等 upsert gba-capacity-demo-v1，不修改表结构、不触碰正式 ADS 和久新库。：PASS；evidence=ev-2322-seed-dry-run-r2, ev-2322-db-write-r2
- regression / 三仓候选改动无空白错误且被限制在授权 change scope 内。：PASS；evidence=ev-2322-diff-check-r2

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| ev-2322-city-index-readonly | db_read | PASS | yes | yes | PENDING | show_py@7bc646a4b1f5685128fcfdd09188b07637f14f4a | 确认 city_index 结构可承载 11 城总分/子分/历史；Demo 现有数据未覆盖统一版本；正式能力表 11 行中仅 4 行有分值。 |
| ev-2322-python-tests-r2 | test | PASS | yes | yes | PENDING | topic_py@0687fb873ce53bfe41cf46c6af4c333fa4322a04 | 3 个目标测试通过：固定 11 城、机制/同比/历史映射、零值子指标保留。 |
| ev-2322-java-tests-r2 | test | PASS | yes | yes | PENDING | backend@4eb0a85919bfe97bd5f48bdeaabfcd708b078d23 | BayInnovationControllerTest 2 个测试通过：固定 11 城聚合、趋势/历史透传和能力分空结果降级。 |
| ev-2322-ui-build-r2 | build | PASS | yes | yes | PENDING | ui_pc@68805b383e99cb32ba2d340646f8696e1f8067a2 | TypeScript/Vue 类型检查与生产构建通过；仅保留仓库既有构建告警。 |
| ev-2322-cross-repo-contract-r2 | integration | PASS | yes | yes | PENDING | topic_py@0687fb873ce53bfe41cf46c6af4c333fa4322a04;backend@4eb0a85919bfe97bd5f48bdeaabfcd708b078d23;ui_pc@68805b383e99cb32ba2d340646f8696e1f8067a2 | 16 项跨仓契约检查全部通过：demo 数据源隔离、11 城、机制/同比/历史贯通及前端渲染。 |
| ev-2322-diff-check-r2 | review | PASS | yes | yes | PENDING | topic_py@0687fb873ce53bfe41cf46c6af4c333fa4322a04;backend@4eb0a85919bfe97bd5f48bdeaabfcd708b078d23;ui_pc@68805b383e99cb32ba2d340646f8696e1f8067a2 | 三个仓库候选 diff 均无空白错误。 |
| ev-2322-seed-dry-run-r2 | data_plan | PASS | yes | yes | PENDING | topic_py@0687fb873ce53bfe41cf46c6af4c333fa4322a04 | dry-run 确认写入 44 行、11 城、4 个年度观测点且无主键冲突。 |
| ev-2322-db-write-r2 | db | PASS | yes | yes | PENDING | topic_py@0687fb873ce53bfe41cf46c6af4c333fa4322a04 | demo_gkxlumenx_ads.city_index 幂等 upsert 44 行；回读 11 城、4 个年度观测点，2025-05 的机制、同比和历史均有值。 |

DB 写证据授权：

- ev-2322-db-write-r2：demo_gkxlumenx_ads.demo_gkxlumenx_ads.city_index；operation=upsert；gate=sha256:c877c022df81ed0483ab8370f2c7271ed14f17c03b022a61be551f4b13a91379；policy=sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0；scope=sha256:51fd208d6363fe55c37ddd390be5ea497336ce793651f393005c45451b386494；authorization=sha256:cc32ecedaa61e3ec6563d7130f1a439c4da37b3489af12b10ae8b6fd60986be0

- manifest 校验：PASS；manifest_hash=sha256:e04dc012e5e4b0d5c01c55e73fd234e916efbd18afa4cd45a029a165d3b2d52e；不可复核证据=PENDING

## 5. 已知风险和未覆盖项

- PENDING

阻塞记录：

- PENDING

评审记录：

- topic_py：reviewer=subagent:independent-review-2322，independent=true，sha=0687fb873ce53bfe41cf46c6af4c333fa4322a04，verdict=PASS，hash=sha256:7738fd5cd98956def769582bc8b9f66c7578e06799f7033d5f3dd1e26c6b2f54，findings=P1 已关闭：capability-score 显式绑定 demo_gkxlumenx_ads，source 由同一常量生成，避免环境漂移误读正式 ADS。；P2 已关闭：子指标改用键存在且非 None 的取值，合法 0 不再被 truthy 回落吞掉；3 个目标测试通过。；残余 P2：seed 数据未接入部署初始化任务，环境重建后仍需人工执行脚本。
- backend：reviewer=subagent:independent-review-2322，independent=true，sha=4eb0a85919bfe97bd5f48bdeaabfcd708b078d23，verdict=PASS，hash=sha256:ba2bb9e801cc9133c2f281078ff84538721a93a09b65290da9efd85534b65291，findings=P2 已关闭：能力分返回空列表或调用异常时保留 11 城，并通过 capabilityEmptyReason 与 emptyReason 透出明确降级原因。；P3：新增测试覆盖空列表，未直接模拟 Feign 抛异常；异常分支逻辑简单，不阻断提测。
- ui_pc：reviewer=subagent:independent-review-2322，independent=true，sha=68805b383e99cb32ba2d340646f8696e1f8067a2，verdict=PASS，hash=sha256:b5d68ea062bf6922b1e330326cebd9b569cab0ef36c842f7e55fc2bb89fa4d61，findings=P1 已关闭：趋势图标题改为“头部城市创新能力综合得分趋势”，tooltip 单位改为“分”，不再把能力分误标为论文数。；机制缺数文案改为中性描述，并移除 GBA_ANALYSIS_SUBITEMS 旧依赖。；残余 P2：review/readiness.ts 的旧 w_v1.0-demo/3 城说明未纳入本次改动 scope，提测时需同步或确认不影响展示。

## 6. S/M/L 风险等级和定级理由

- 等级：M
- 是否上调：否
- 理由：PENDING

## 7. 数据 policy、run scope 和确认人

- policy_version：demo-2026-11-10
- policy_hash：sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0
- scope_hash：sha256:51fd208d6363fe55c37ddd390be5ea497336ce793651f393005c45451b386494
- scope_status：approved

- demo_gkxlumenx_ads.city_index；confirmed_by=human:7695591354147146731；evidence=evidence/manifest.json#ev-2322-city-index-readonly

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
| enter_dev | approved | 进入开发 | sha256:c877c022df81ed0483ab8370f2c7271ed14f17c03b022a61be551f4b13a91379 |
| ship | pending | PENDING | PENDING |
| acceptance | pending | PENDING | PENDING |

enter_dev bound_to：{"repos":[{"repo_id":"topic_py","repo_name":"lumen-topic-py","remote":"https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-topic-py.git","base_branch":"dev","base_sha":"7bc646a4b1f5685128fcfdd09188b07637f14f4a","planned_change_scope":["gkx_show_service/views/gba_indicator.py","gkx_show_service/scripts/seed_gba_capacity_demo.py","tests/test_gba_capacity_score.py"],"role":"backend_python","depends_on":[],"ship_order":1},{"repo_id":"backend","repo_name":"lumen-svc-platform","remote":"https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform.git","base_branch":"dev","base_sha":"da2260aeee781138d7b8006ce45873f471c49da1","planned_change_scope":["gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/controller/BayInnovationController.java","gkxlumen-display/src/test/java/com/topcomm/gkxlumen/display/controller/BayInnovationControllerTest.java"],"role":"backend_java","depends_on":["topic_py"],"ship_order":2},{"repo_id":"ui_pc","repo_name":"lumen-ui-science-pc","remote":"https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc.git","base_branch":"dev","base_sha":"b83e84bb9b0dd3187d64f4ad062c731aca1680e0","planned_change_scope":["src/api/situation/bayAreaInnovation.ts","src/views/situation/bay-innovation/tabs/CapacityTab.vue"],"role":"frontend","depends_on":["backend"],"ship_order":3}],"diagnosis_hash":"sha256:5b5742aaea5b4ec4bde4dcadc0195de71b4d2b79a4bd284ec0cc1e3392f9d673","plan_hash":"sha256:1529b8eef04262c14e65fde495aa62590eda0231730e90457d6b28e749b0de49","risk_level":"M","data_policy_version":"demo-2026-11-10","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:51fd208d6363fe55c37ddd390be5ea497336ce793651f393005c45451b386494"}

ship bound_to：PENDING

acceptance bound_to：PENDING

## 12. 自动决策摘要

- PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
