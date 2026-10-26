# handoff · DOC-SVC-ORG-COVERAGE-ANALYSIS-CHAIN-L01

- **任务**：服务链·服务机构产业领域分析「完整分析链路设计 + LLM 落点」设计稿（`ponytail: off`；设计任务，未触 repos 业务代码）
- **角色**：agent:architect + agent:algorithm（可带 api）；监管人：human:徐滕强
- **Skill**：`gkx-topic-analysis-chain-design` 四步法（扫 → 落点表 → 链路文 → 归集）
- **日期**：2026-10-26

## 1. 范围与实现（对照 bid / 金样）

| 交付要求（派单 A–G） | 产物 | 位置 |
| --- | --- | --- |
| A 现状对照表（金样 vs 企业 vs as-built） | 会话 A 表（G1–G5 缺口）+ 设计稿 §3 摘要 | 会话记录 + 05.7.1 §3 |
| B 完整链路设计 | §4（触发/冻结/四节点/矩阵/RustFS/前端） | 05.7.1 §4 |
| C LLM 落点专章 | §5（落点表 L1–L4、事实包白名单、三态契约） | 05.7.1 §5 |
| D Prompt 草案 | `svc.coverage.narrate v1` 全文 | 05.7.1 §6 |
| E OpenAPI / RustFS schema / metric 占位 | §7.1–§7.3 | 05.7.1 §7 |
| F 复用边界 | §8（共享 `lumen_common/tasks` 骨架 vs 本叶独有装配） | 05.7.1 §8 |
| G handoff | 本文 | `agent-handoffs/…/DOC-SVC-ORG-COVERAGE-ANALYSIS-CHAIN-L01.md` |

金样对照：`05.3.1` v0.3（§5.6 Prompt / §6 执行框架）、`05.6.1` §3–§5、`05.3.2` 落点三档；as-built 扫描覆盖前端 `svcAnalysisWorkspace/svcCoverageModel`、Java `SvcAnalysisTypes/SvcAnalysisAdapterImpl`、topic-py `gkx_svc_service/views/task.py`、algo `svcan/{views,assembly/{leaves,matrix},engine}`、metric-registry MCP（BREADTH/DEPTH）。

## 2. 偏离说明

1. **workspace 键澄清**：派单写「workspace 键 org_coverage」；代码事实 = workspace 键 `field`，`org_coverage` 是 analysisType/叶子名。按代码事实书写，菜单/路由未改。
2. **L4（采购建议句）列为 P2 落点**：现 as-built 为前端模板句拼接；目标态下沉算法侧规则稿 + LLM 可润色。若评审认为本批只做 L3，L4 可延后（互不影响 schema）。
3. **产物落 RustFS（G4 闭合）纳入目标态**：as-built 为回调内联 payload；设 4.5 兼容窗（无 object_key 允许内联兜底签发），避免灰度期断链。

## 3. 产物清单

- `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.7.1-服务机构产业领域分析.md`（设计稿 v1.0，本文 §1 表中 B–F）
- 本文（G）
- 无代码 / 无 seed / 无矩阵 YAML 改动；未创建/更新 task-registry 条目（挂载待派单方，见 §6）

## 4. 验收证据（设计类）

- 05.7.1 四阶段词表与原型（2026-10-21 用户钉死）逐字一致：`SvcAnalysisTypes.java` = `task.py` = 前端过程页。
- LLM 落点符合润色契约：数字规则锁死（L1/L2）、narration 三态、事实包白名单、无 Key 降级任务仍 success。
- D14 合规：对象键落 `gkx-lumen/gkx-analysis-results/analysis/svcan/…`；Demo 面写 `demo-gkx-analysis-results`。
- D9 诚实：BREADTH D3=partial/D4=mock、DEPTH D1=draft 未翻转宣传；depth 代理口径随 `GAP-SVC-MATRIX-SRC` 下发；禁止 LLM/前端补覆盖数字。
- `cicd: skip`（设计文档，无业务 CI）。

## 5. 架构合规自检

| 铁律 | 自检 |
| --- | --- |
| 1 算法只在 Python | ✅ 矩阵计算/LLM 润色全在 lumen-algo-py |
| 2 调用链 | ✅ 前端→Java→topic-py `/internal/*`→algo `/internal/*`，无越层 |
| 3 NebulaGraph | ✅/n.a. 本叶不涉图谱 |
| 4 可观测 | ✅ envelope 沿用 trace_id；节点回调协议不变 |
| 7 共享聚合核心 | ✅ 复用 `lumen_common/tasks`/worker/LLM client，不新造框架 |
| 8 数据策略 | ✅ 读 ADS 标准表；缺格/空态诚实，不 Mock 填充 |
| 10 D9 | ✅ metric_id 占位 + ⓘ 契约 + 🧪 MockBadge 待 D4 翻转 |
| 12 demo/lumen 隔离 | ✅ 全链路 lumen 仓；未引用 demo 服务 |
| 13/14 RustFS D14 | ✅ 六目录内对象键；凭证不进 git |

## 6. 后续与挂载

- 实现建议拆单：① 前端指纹 4 段 + narration 渲染（fe）；② topic-py org_coverage 投递改造 + 路由正名（api）；③ algo worker 接入 + narrate 包 + RustFS 写（algorithm）。依赖 ③←②←① 联调。
- 开放项见 05.7.1 §9（产业口径 🟡、覆盖度列 🟡、DEPTH 签收 🟡）；产业口径默认值须登记《客户决策清单跟踪表》（PM owner）。
- task-registry 挂载：本设计任务未在 MCP 建单（会话未给 task-id）；如需挂载由 coordinator 补 `task-create` 并回填本 handoff 引用。

## 7. cost

- `actual_tokens`: 待回填（设计会话，估 <200k）
- `model_used`: glm-5.3-Flash
- `actual_cost`: 待回填（估 < $2，无告警）
- `cost_warn`: false

*ponytail: off（定义/文档任务，产物完整性优先）。*
