# 缺陷修复报告：2020 科技全域态势，服务机构和专利无数据

> 本文件由 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 从 `state.json` 和 `evidence/manifest.json` 渲染，不手工补写事实。
> 生成时间：2026-11-11T11:10:18.864+08:00
> 当前 cycle：cycle-001-20261111T105229+0800
> 当前内部阶段：BLOCKED
> 验收模式：policy_only（operator_verified=false）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【2020】科技全域态势，服务机构和专利无数据 |
| 内部 ID | 7161864249 |
| 当前负责人 | human:7695591354147146731 |
| 现象 | 科技全域态势当前筛选为粤港澳大湾区、2016-2026、专利与服务机构时：服务机构被前端判定为不可用并提示暂无数据；专利卡显示 71,043 件但趋势区显示暂无趋势数据。 |

- 进入科技全域态势并选择粤港澳大湾区、2016-2026
- 科创要素同时选择专利和服务机构
- 实时数据监控右侧出现服务机构暂无数据提示，专利卡显示总量但无趋势

## 2. 根因、需规依据和影响范围

- 根因：两个症状分别有代码依据：1) 后端 SituationController.buildRegions 的 layerOrder 只包含企业、GEO_FACTOR_ORDER 与 MOCK_FACTOR_ORDER，服务机构已从 MOCK_FACTOR_ORDER 移除，但未加入任何 layerOrder 集合，因此 /map 的 region.layerKeys 永远不会包含 service，前端 getFactorAvailability 将其判为不可用；2) 后端 buildFactorCards 对专利显式传入 series=null，Python yearly-trend 当前不返回 patent_count，因此专利只有单年总量，没有年度序列。修复需同时改 lumen-svc-platform 与 lumen-topic-py。
- 反证：截图显示专利卡已有 71,043 件，说明专利 KPI 本身有数，缺失的是年度趋势序列；SRS 序号 10 要求统计指标支持增长趋势，序号 12 要求按时间查看监测数据趋势；服务机构问题不是前端字段展示错误；前端仅按 /map layerKeys 做诚实不可用提示
- 需规依据：agent-delivery/bid-reference/srs/02-科技信息展示系统/科技发展态势/科技全域态势.md#实时数据监控-序号6；agent-delivery/bid-reference/srs/02-科技信息展示系统/科技发展态势/科技全域态势.md#统计指标展示功能-序号10；agent-delivery/bid-reference/srs/02-科技信息展示系统/科技发展态势/科技全域态势.md#监测数据趋势变化查看功能-序号12
- 影响范围：lumen-svc-platform：SituationController.buildRegions 的服务机构 layerKeys，以及 buildFactorCards/趋势装配；lumen-topic-py：gkx_show_service 的 yearly-trend 需增加专利年度计数，供 BFF 组装专利趋势；lumen-ui-science-pc：现有前端可消费 series，预计无需改动；需用真实响应验证字段契约

## 3. 改动摘要和非目标

- PENDING

实现仓校验：

- PENDING

非目标：不修改前端字段结构，除非契约验证发现必要适配；不改变指标口径或补零；不将无源数据标记为真实

## 4. 验证矩阵和证据结果

- PENDING

| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |
|---|---|---|---|---|---|---|---|
| E-SCREEN-2020-001 | screenshot | PASS | yes | yes | PENDING | 2e5ed3fe31cdb3039b49ecdac9aac06625e24ec9 | 截图显示服务机构暂无数据提示、专利卡 71,043 件但趋势为空。另有截图已保存到 run evidence/raw。 |

DB 写证据授权：

- PENDING

- manifest 校验：PENDING；manifest_hash=PENDING；不可复核证据=PENDING

## 5. 已知风险和未覆盖项

- 修复同时涉及 Java BFF 与 Python 数据门面，属于跨仓变更
- 服务机构 layerKeys 与专利年度趋势均涉及真实数据契约，超出 P0 单仓轻量流
- 需要契约同步和两个仓库独立验证

评审记录：

- PENDING

## 6. S/M/L 风险等级和定级理由

- 等级：L
- 是否上调：是
- 理由：修复同时涉及 Java BFF 与 Python 数据门面，属于跨仓变更；服务机构 layerKeys 与专利年度趋势均涉及真实数据契约，超出 P0 单仓轻量流；需要契约同步和两个仓库独立验证

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
| enter_dev | pending | PENDING | PENDING |
| ship | pending | PENDING | PENDING |

enter_dev bound_to：PENDING

ship bound_to：PENDING

## 12. 自动决策摘要

- PENDING

## 13. 回滚版本、回滚方式和回滚验证

- PENDING
