# handoff · DOC-CHAIN-DIAG-FAMILY-L01

- **任务**：产业诊断分析链路设计——关键环节（key_link）+ 瓶颈堵点（bottleneck）合并族完整链路与 LLM 落点（`ponytail: off`；definition 任务，未触 repos 实现）
- **角色**：agent:architect-agent；监管人：human:徐滕强；coordinator 代持（上一会话信息收集后中断，本会话从动笔直接开始，调研结论沿用派单已核实清单）
- **Skill**：`gkx-topic-analysis-chain-design` 四步（扫→落点→链路文→归集）；金样 `05.2.1`（链域体例）/ `05.3.1 §5`（润色契约）/ `05.3.5 §5`（逐格退先例）/ `05.3.2`（三档判定口径）

## 1. 范围与实现（对照派单）

| 要求 | 产物 | 位置 |
| --- | --- | --- |
| 元信息表 + §1–§9 | 05.2.2 全文（元信息表/§1 做什么/§2 完整逻辑/§3 取数与计算/§4 结果组装/§5 LLM 落点/§6 执行框架/§7 报告/§8 相关文档与开放项/§9 修订记录） | `05.2.2-产业诊断分析链路.md` |
| Mermaid ≥2 张 | 差异 flowchart（两叶分叉 + 回传汇合 + LLM 降级虚线边）+ 时序图（FE→GW→JA→AL→DB 完整回调链） | §2 |
| 落点表逐点位 | 9 行（K1–K4 / B1–B5），每行含「判定/可改字段/事实包/无 Key 行为/优先级」 | §5.1 |
| 逐点位三档判定 | LLM 已 as-built 4 处（K1/K2/B1/B2，附差距）；规则锁死 5 处（K3/K4/B3/B4/B5，附锁死理由）；暂缓 0 新增（QC02/QC04 只登记客户决策清单 🟡 第 222/224 行，不回潮） | §5 |
| as-built↔金样差距 | G2 bottleneck 无数字白名单 / G3 三态粒度（skipped/fallback 合并 degraded，key_link 无 llm 字段）/ G4 temperature 未写死 / G5 Java bottleneck 仅通用门禁 / G6 无 Key 空态（非规则稿）/ prompt 内联（§5.4）——全部落开放项 CHAIN-DIAG-01~05 | §5.2/§5.3/§8 |
| FE 消费面 | 四缺口实证：`competition`/`tech_trends`/`causes`/`suggestions` 零消费；`kpi` 块错位（FE 读 summary）；`representative_enterprises.items` 包装错位 | §7 |
| 开放项编号 | CHAIN-DIAG-01~07（与 OPEN-CY-* / ENT-* 无冲突） | §8 |
| 总册指针 | 05.2-产业链.md §8 增 05.2.2 行 | 已改 |
| 不拆文理由 | 两叶共享五环节骨架（`bottleneck.py` 直接 `import key_link as kl`，loader/别名/目录/边全复用）+ 同 FE 工作区 + 同厨房；拆文=骨架契约写两遍 | 元信息表注 + 引言 |

## 2. 偏离说明

1. **narrate as-built 判定**：两叶 LLM 是「流程内能力节点」（annotate 环节内，产结构化 JSON），非 05.3.1「事后收尾」模式；与 05.2.1 cycle 同构，符合 skill 产业链特判「默认产出是差距清单而非新契约」——故 §5 落点表以「已 as-built + 差距收敛」为判定，不改 LLM 结构。
2. **失败语义按实码直写**：现网无 Key 与调用失败同入 `llm_unavailable`，未按金样硬套 `narration` 三态——登记 CHAIN-DIAG-03 待实现侧评估，命名家族维持 05.2.1 §11 冻结拍板，不越权改契约。
3. **测试锚点**：`tests/test_chain_key_link.py`（284 行）/ `tests/test_chain_bottleneck.py`（290 行）已存在并核过文件规模；本文按「文档单」性质未新增实现级自检（无代码产物，DoD=文档评审）。

## 3. 产物清单

- `…/科技专题服务系统-完整详细设计/05.2.2-产业诊断分析链路.md`（v0.1，新增）
- `…/科技专题服务系统-完整详细设计/05.2-产业链.md`（§8 指针 +1 行）
- 本文。无 repos 代码改动；task-registry 状态由本单流程推进（evidence 回填 + ready_to_sign）。

## 4. 验收证据（设计类）

- 落点判定全部代码对读：`key_link.py`（900 行）/ `bottleneck.py`（657 行）/ `job_runtime.py` 图绑定与 degraded 上抛 / Java `ChainKeyLinkResultValidator` + `validateChainResult` 分发（key_link 结构门禁、bottleneck 仅通用）/ FE `IndustryDiagnosisPage.vue` + `parseKeyLinkStages`/`parseBottleneckLinks`/`parseKeyLinkDetail` + `IndustryBottleneckResultBoard.vue`——FE 缺口由全仓 grep 实证（competition/tech_trends/causes/suggestions 零触点）。
- 指标态按 MCP 实查（2026-10-27）：`M_CHAIN_KEY_NODE_COUNT` D1 aligned/D2 provisional/D3 partial（三因子仅企业规模一维可算）/D4 mock；`M_CHAIN_BOTTLENECK_COUNT` 族 D3 partial（读表口径 2026-10-14 已定）。
- 客户决策项 QC02（第 222 行）/QC04（第 224 行）只引用登记，未替甲方拍板。
- `cicd: skip`（设计文档）。

## 5. 架构合规自检

| 铁律 | 自检 |
| --- | --- |
| 1 算法只在 Python | ✅ 两叶 LLM 调用全在 lumen-algo-py（key_link/bottleneck annotate 环节） |
| 2 调用链 | ✅ 前端→Java `/topic/v1/analysis/tasks`→Feign `/internal/v1/chain/jobs/execute`→回调；FE 只调 Java；Java 不调模型不透传 Key |
| 3 NebulaGraph | n.a.（两叶读 DWD/ADS MySQL，无图谱消费） |
| 4 可观测 | ✅ stage 回调 degraded/degrade_reasons 上抛 SSE；本文 §6 登记 |
| 5 CI/CD | `cicd: skip`（纯设计文档） |
| 6 demo2 只读 | n.a.（未涉 demo2 仓） |
| 7 共享聚合核心 | ✅ 前端只调 Java；算法 Common 串 Key；两叶骨架共享复用（kl import） |
| 8 数据策略 | ✅ ADS 只读；缺表诚实空；mock 态 + GAP 引用不造数；QC02/QC04 🟡 只登记 |
| 9 D8 前端规范 | n.a.（本单纯设计，未涉 UI 视觉 token；CHAIN-DIAG-06 实现单 handoff 须带 Design.md §14 清单） |
| 10 D9 数据血缘 | ✅ 指标态按 MCP 2026-10-27 实查书写（D1 aligned/D2 provisional/D3 partial/D4 mock）；kpi mock + pending_ref=QC02/QC04 + gap_ref 对齐；未把 D1–D4 说成 8 件套字段 |
| 11 D10 交互规范 | n.a.（未新定义交互；FE 现状走查沿用已验收诊断工作区） |
| 12 demo/lumen 隔离 | ✅ 全部引用 lumen 仓 as-built（lumen-algo-py/lumen-ui-topic/lumen-svc-platform） |
| 13 D14 RustFS | n.a.（resultData DB 全量，无对象存储写路径，§2 步 8 登记） |
| 润色契约 | ✅ 失败任务仍 success / 数字白名单（key_link 已有，bottleneck 差距已登记）/ 事实包边界 / prompt 版本化目标态（CHAIN-DIAG-01） |

## 6. 成本

| 字段 | 值 |
| --- | --- |
| actual_tokens | 约 260_000（in+out，估） |
| model_used | glm-5.3-Flash |
| actual_cost | 0.26 |
| cost_warn | green |

## 7. registry 回填记录

- `task-update-status` DOC-CHAIN-DIAG-FAMILY-L01 → `ready_to_sign`（coordinator 代持 in_progress 直推，tech_task 型 ready_to_sign 闸门）
- `task-update-fields` evidence 指向本文 §3/§4 + 05.2.2 文档路径 + commit hash
