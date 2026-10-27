# DOC-ENT-PAIN-ANALYSIS-CHAIN-L01 · 企业痛难点 — 完整分析链路设计 + LLM 落点（05.3.5）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:architect-agent`（algorithm 协作：pain_points as-built 事实源核对） |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | E-ENT-SCRUM-PDR / definition / P1 / effort 5；仅企业轨，不串 SVC/CHAIN |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | 定义/文档任务；不写 repos 实现（`narrate_pain` 实现另开单 ENT-PAIN-01）。产品定义与会签产物完整性优先。 |

## 问题清单

- A 表确认阶段的两个「确认点」（诚实句保留口径、四格校验粒度）经监管人指出属设计者职权，已撤回问询并**直接定死**：诚实句=整句原样保留（子串匹配校验）；校验粒度=逐格退（一格违规退该格，`reason=title:field:verdict`）。不再作为开放项。
- 条款号核对：E-29=`1.1.1.2.4.2.3.9`「企业发展痛难点分析」（bid-reference L4583，子叶 .9.1/.9.2）；页面菜单同名。
- 诚实句实位确认：三条诚实句内嵌于 `pain_points.py` 对应 issue 的 evidence/cause 规则句（L99/L145/L173），非独立字段——事实包设计据此带 `unavailable_fields` + `honesty_note`。
- P7 判定与四条硬约束直接引自 05.3.2 v0.8 拍板记录，本文不重判、只落到可执行校验（verdict 枚举 `long{N}|cause|num:{x}|policy|honesty_missing`）。

## 修改内容

- 新增 `05.3.5-企业发展痛难点分析.md`（v1.0）：
  - A 身份：E-29 / `risk_insight`·`pain_points` / SCIENCE 五节点（与评估族六节点差异=无 confidence）；
  - B 链路：§2.1 两张 Mermaid（差异 flowchart + 全链时序图，含 narrate_pain 目标态交互）；
  - C 规则 as-built：四维七类问题表（title=Q018 固定名、evidence 函数、三条诚实句实位）+ 四格模板 + 维度计数卡；
  - D 落点契约：`narrate_pain` 目标态——只改 `issues[]` 四格 text；事实包（signal_summary 计数 + unavailable_fields + drafts，禁原始明细）；逐格校验（计数白名单/禁因果外推/诚实句整句必留/禁政策工具 verdict）；三态；新 prompt 文件 `pain/pain.narrate.v1.txt`（PROMPT_PACK=pain.narrate.v1，与评估族分文件同治理）；
  - E 允许/禁止示例；F 与评估族差异表（五节点/四格论证链/计数白名单/分 prompt）；G 开放项 ENT-PAIN-01/02/03。
- `05.3-企业.md` §5 总册加 05.3.5 指针。

## 测试结果

- 文档任务无代码测试；一致性自检：
  - 条款号与 bid-reference 实文核对一致（E-29=`1.1.1.2.4.2.3.9` L4583）；
  - 四格标签与 FE `PainPointsPanel.vue` 渲染字段核对一致；
  - 硬约束四条与 05.3.2 v0.8 拍板原文逐条对齐，未新增未删减；
  - Mermaid 图件 2 张（对齐金样图件密度）；
  - 共享章节（执行框架/报告双路径）引用 05.3.1 不重写。
- **v1.1 审查勘误后新增机械自检**：`scripts/check-pain-asbuilt.py`（assert 式，无框架）——grep `pain_points.py` 七个 title + 三句诚实句与 05.3.5 §3.1 表比对，防文档再漂移；随勘误 commit 入库并实跑通过。

## 遗留风险

- `narrate_pain` 为目标态设计，实现单 ENT-PAIN-01 未开；实现时若发现事实包字段缺失（如 signal_summary 需 pain_points.compute 增产），按实现单处理不回改本文口径。
- 政策工具词表（solution 判拒依据）需实现单冻结，词表缺失期间该 verdict 不会触发（安全方向：宁可漏放，不误杀）。
- 诚实句「整句保留」对模型是强约束，若实测 ok 率过低，降级方案=仅要求保留「不可用，未作为判断依据」语义短语（需监管人拍板后升 prompt 版本）。

## CI/CD（必填）

- 分支：`dev`（gkx-orchestration，无业务 CI）
- commit：`[agent:architect-agent] DOC-ENT-PAIN-ANALYSIS-CHAIN-L01 05.3.5 + 总册指针 + handoff`
- pipeline / 部署 / K8s：不适用

## 可观测性（建议）

- 无新增埋点；`narrate_pain` 实现后沿用 narration 快照 + 日志检索指引（同评估族）。

## 涉及文件

- `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.3.5-企业发展痛难点分析.md`（新增）
- `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.3-企业.md`（§5 加指针）
- `agent-delivery/agent-handoffs/DOC-ENT-PAIN-ANALYSIS-CHAIN-L01.md`（本文件）
