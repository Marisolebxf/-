# 缺陷修复报告：2026111501 门户，有新增机构数没有全球机构数

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-16T15:53:08.800+08:00
> 当前 cycle：cycle-001-20261115T124403+0800
> 当前内部阶段：IMPLEMENTING
> 验收模式：policy_only（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【2026111501】门户，有新增机构数没有全球机构数 |
| 内部 ID | 7168664833 |
| 当前负责人 | PENDING |
| 现象 | 专题服务门户「全球服务机构概况」选定产业「未来制造（智能机器人）/ 具身智能」（INB1354）时，全球机构约数为 0 家，本年新增机构为 6 家，历年曲线仍有点。同一批机构不可能新增有数而总数为 0。 |

- POST https://edu.itic-sci.com/tts/lumen/api/svc/topic/v1/service-portal/overview body {"industry":"INB1354"}：kpi.org_in_pool=0，new_org_series 末点 2025=6，序列合计 921，industry_layout 为空，filtered=true，chain_codes=[INB1354]
- 同接口无产业参数：kpi.org_in_pool=43296，全量总数有值，不是事实表缺行

## 2. 根因、需规依据和影响范围

- 根因：产业切片时总数按 svc_org_card ∩ enterprise_industry_chain 计数，新增序列 _sliced_new_series 只按 dwd_org_base_info ∩ 挂链计数，没有再交 svc_org_card。具身智能挂链上有成立年的企业 921 家（末年 6 家），但服务机构卡交集为 0。口径真源要求挂链 ∩ 卡表 ∩ ODS 成立年。深圳趋势 _sliced_sz_trend 是同一处漏交。
- 反证：无产业参数时 org_in_pool=43296，否定「全量 M_SVC_ORG_CNT 缺行」；INB1303 序列合计 124 等于卡表总数 124，INB2503 序列合计 5267 等于卡表总数 5267：卡表已覆盖的链上两边一致
- 需规依据：agent-delivery/bid-reference/srs/01-智慧服务门户系统/集群服务/科技专题服务.md#88（全球服务机构概况：服务机构数量分析/总体数量与历年趋势）
- 影响范围：专题服务门户全球概况页产业切片态的本年新增与历年新增曲线；同切片口径的深圳历年趋势（_sliced_sz_trend）

## 3. 改动摘要、跨仓 Bundle 和非目标

- Bundle 类型：单仓
- 同一飞书缺陷涉及多个仓库时仍是一个 run、一个 claim、一套 gate；各仓保留独立候选 SHA。

- topic_py：lumen-topic-py，role=python-api，ship_order=1，depends_on=PENDING，base=c96b08b24cac489f24bcb934b4081f1f10ae2037，candidate=fb10f48e4e41b1964281e55abb06595a3e491d55，scope=gkx_svc_service/repo.py, tests/test_svc_portal_chain_slice.py

实现仓校验：

- topic_py：candidate=fb10f48e4e41b1964281e55abb06595a3e491d55，diff_hash=sha256:ea04d8a213b875c8713e5f99f4a76b37ded7d076de5874edfe014490aed9c2ce，git_verified=yes，files=gkx_svc_service/repo.py, tests/test_svc_portal_chain_slice.py

非目标：不改前端 lumen-ui-topic（0 与暂无的展示是诚实行为）；不改 Java lumen-svc-platform（纯透传）；不把产业链上未进卡表的企业回填成全球机构总数；不补写 svc_metric_fact，全量总数已有值；不改全量态 portal_overview（无 chain_codes 时仍读 ADS 事实表/序列表）

## 4. 验证矩阵和证据结果

- PENDING

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| ev-scope-confirm-001 | data-scope-confirm | PASS | yes | yes | PENDING | c96b08b24cac489f24bcb934b4081f1f10ae2037 | PENDING |

DB 写证据授权：

- PENDING

- manifest 校验：PENDING；manifest_hash=PENDING；不可复核证据=PENDING

## 5. 已知风险和未覆盖项

- PENDING

阻塞记录：

- PENDING

评审记录：

- PENDING

## 6. S/M/L 风险等级和定级理由

- 等级：M
- 是否上调：否
- 理由：PENDING

## 7. 数据 policy、run scope 和确认人

- policy_version：demo-2026-11-10
- policy_hash：sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0
- scope_hash：sha256:09d32040be006c9322fa75dab26fd9eb6d98350926482f320b54d914d62fd659
- scope_status：approved

- demo_gkxlumenx_ads.svc_metric_fact；confirmed_by=human:孔东；evidence=evidence/manifest.json#ev-scope-confirm-001

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
| enter_dev | approved | 进入开发 | sha256:a0cf61fa2626bcbd1f33bf81989cd894a1e18e90e673882a32b9794d0c8408c5 |
| ship | pending | PENDING | PENDING |
| acceptance | pending | PENDING | PENDING |

enter_dev bound_to：{"repos":[{"repo_id":"topic_py","repo_name":"lumen-topic-py","base_sha":"c96b08b24cac489f24bcb934b4081f1f10ae2037","candidate_sha":null,"planned_change_scope":["gkx_svc_service/repo.py","tests/test_svc_portal_chain_slice.py"]}],"diagnosis_hash":"sha256:8d6f5f88c123e610f70b13e6608ea38fa05df9a4d3dca05bf94136f985120456","plan_hash":"sha256:b8ac129daf9d40d4ca1c023e57f973def3d6085e0db7ada8081e131bbc4128c9","risk_level":"M","data_policy_version":"demo-2026-11-10","data_policy_hash":"sha256:04214d607e0dd16aca72d0c51b92cb56920ce5256095996e56d9a18fb2b400e0","data_scope_hash":"sha256:09d32040be006c9322fa75dab26fd9eb6d98350926482f320b54d914d62fd659"}

ship bound_to：PENDING

acceptance bound_to：PENDING

## 12. 自动决策摘要

- PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
