# handoff · DOC-CHAIN-REGIONAL-FAMILY-L01

| 项 | 内容 |
| --- | --- |
| 任务 | 区域产业评价（指数+竞争力合并族）完整链路设计 + LLM 落点（05.2.3） |
| 角色 | [agent:architect-agent]（只设计不写业务仓） |
| 监管人 | human:徐滕强（coordinator_dispatch 总授权队列 2） |
| 仓 | gkx-orchestration（origin/dev） |
| 强度 | ponytail off（架构/产品文档任务，产物完整性优先） |
| 状态 | 完工，待监管人评审（definition 会签材料齐备） |

## 1. 范围与实现（对照 /goal）

| 要求 | 交付 | ✅/❌ |
| --- | --- | --- |
| `05.2.3-区域产业评价链路.md` 落盘（合并族；若拆两文须给理由） | **两叶合并一文**，理由写进卷首：共享对象栏（`parse_regional_combo`）/读取链（`load_regional_scorecard`+`apply_input_bases`）/LLM 客户端（`call_gap_llm`+`GAP_SYSTEM`）/同构五环节 STAGE_CODES，差异仅输入契约（四力模板 vs 三维权重）与 sections 形状；拆文会把共享契约写两遍 | ✅ |
| 元信息表 + §1–§9 全齐 | 卷首 10 行元信息表 + §1 做什么 / §2 完整逻辑 / §3 取数与计算（as-built 逐行对照）/ §4 结果组装 / §5 LLM 落点专章 / §6 执行框架 / §7 报告与前端消费 / §8 相关文档与开放项 / §9 修订记录 | ✅ |
| Mermaid ≥2 张（差异 flowchart + 时序图） | §2 两图：双 subgraph 差异 flowchart（index/comp 两图并行 + 降级虚线）+ 全链时序图（FE→GW→Java→厨房→ADS→GLM→回调签发） | ✅ |
| §3 两叶 as-built 逐行对照实码 | 身份/输入契约/对象栏/维度模型/读面/计算核心/排名/规则稿/honesty 冻结/versions 快照 十行×两叶对照表，全部对齐 `regional_index.py` / `regional_competitiveness.py` / `regional_common.py` 实码（gap/维度合成的 hit 语义：命中 Q056/QC07 整行维度置 None、缺底分主体 incomparable 不硬拒、权重容差 ±0.05、模板配置 DEFAULT_TEMPLATE 兜底） | ✅ |
| §5 LLM 落点表逐点位三档判定 | R1/R2=LLM（已 as-built，差距收敛）、R3/R4=规则锁死；**无暂缓位**（无 QC 未闭合导致的改造禁区）；「gap.prompts.v1 半迁移态」§5.3 如实记录（4 步事实链 + 迁移方案进 REGIONAL-01 实现单建议，本单不落码）；QC 类 🟡 只引用客户决策清单第 225/231 行，不回潮 | ✅ |
| §8 开放项 REGIONAL-01 起编号 | REGIONAL-01~06（prompt 外置/数字白名单/三态粒度/参数写死/FE 接线包/Java schema 校验），与 OPEN-CY-*、CHAIN-DIAG-* 不冲突 | ✅ |
| 总册指针检查 | 05.2 总册 §8 已加 05.2.3 指针行（编号 05.2.3 与 05.2.1/05.2.2 顺延无冲突，总册现有展开文仅此两篇） | ✅ |

## 2. 偏离说明

| 偏离 | 理由 |
| --- | --- |
| 章节体例为 §1–§9 而非 05.2.1 的 §1–§15 | 按 /goal 指定「体例对标 05.3.1（元信息表/§1-§9）」；05.2.1 的 §10–§15 内容（契约五段/状态机映射/域间差异/差距 A 表）在本单分别收敛进 §2 步骤表、§7、卷首 QC11 命名纪律块与 §5.2 差距列，金样密度对齐不缺项 |
| 指标就绪度实查只落 3 枚代表指标（壳/叶/竞争力） | metric-registry 实查口径与 05.2.2 §3 同款（D1 aligned / D2 partial·provisional / D3 分档 / D4 mock）；REGIONAL 族 16 枚叶指标全查属数据侧动作，本文引用注册表入口即可 |

## 3. 产物清单

| 文件 | 说明 |
| --- | --- |
| `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.2.3-区域产业评价链路.md` | 本单主交付（v0.1） |
| `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.2-产业链.md` | 总册 §8 加 05.2.3 指针行（唯一改动） |
| `agent-delivery/agent-handoffs/DOC-CHAIN-REGIONAL-FAMILY-L01.md` | 本 handoff |
| task-registry | DOC-CHAIN-REGIONAL-FAMILY-L01 回填 evidence/cost + 推 ready_to_sign（MCP 操作，非手改 YAML） |

## 4. 验收证据

- 实码锚点：`lumen-algo-py` `lumen_common/algorithms/chain/{regional_index,regional_competitiveness,regional_common,job_runtime}.py`；测试 `tests/test_chain_regional.py` 17 例（图谱注册/成功形状互斥/maxObjects 冻结拒/底分诚实失败/系统模板兜底/legacy 权重别名/Q056 禁入/LLM 越权键不变数/四力混入拒/GIS 跳过/禁自签源码扫描）。
- Java 锚点：`gkxlumen-topic-async-service` `ChainAnalysisTypes`（`chain:regional:*` 白名单 + 四映射；无 regional 专用校验器，已如实登记 REGIONAL-06）。
- FE 锚点：`lumen-ui-topic` `IndustryRegionalPage.vue` / `IndustryRegionalResultBoard.vue` / `parseRegionalBoard`（industryChainTask.ts L524–613）/ `REGIONAL_TASK_STAGES`（industryWorkspace.ts L276–290）；五缺口实况（热力图 x 轴 demo 别名硬编码 / version_boundary 块错位 / heatmap_gis·leaf_contributions·config_honesty 零消费）逐条核对源码后登记，非推断。
- 指标就绪度：metric-registry 实查 2026-10-27（`M_CHAIN_REGION_INDEX` / `M_CHAIN_REG_COMMERCIALIZATION` / `M_CHAIN_COMPETITIVENESS_INDEX`，D1–D4 详见文档 §3）。
- 客户决策项：QC05（第 225 行）/ QC11（第 231 行）🟡 只引用。

## 5. 架构合规自检（公约 §2 铁律逐条）

| 铁律 | 自检 |
| --- | --- |
| 1 算法只在 Python | ✅ 纯设计文档；文中加权合成/排名全部在 `lumen-algo-py`，Java 仅门禁签发 |
| 2 调用链 前端→Java REST→Python `/internal/*` | ✅ §1 调用链与 §2 时序图严格分层，无越层 |
| 3 NebulaGraph | ✅ 本族不涉图谱写；`_no_snapshot` 测试断言禁 graph_snapshot，文档如实记录 |
| 4 可观测性 | ✅ stage_degraded→SSE、honesty/degrade_reasons 契约面写死；埋点不在本单范围（纯文档任务） |
| 5 CI/CD | cicd: skip（设计类，definition 文档交付） |
| 6 demo2 只读 merge | ✅ 未触 demo2；demo 仅读参考（DESIGN-LANDING/GRAPH 真源引用） |
| 7 共享聚合核心 | ✅ 前端只调 Java、Java 不写算法、只读 ADS（`connect_chain_readonly`）全文遵守 |
| 8 ADS 先行 Mock 填充 | ✅ SEED-09 mock 底分真源引用；`honesty.data_mode=mock` 与 D4 一致，禁止前端改绿写进文档 |
| 9 D8 前端规范 | ✅ 不涉新页面；FE 缺口全走 REGIONAL-05 实现单并要求过产品定义 |
| 10 D9 数据血缘 | ✅ 每个统计数字对应 metric_id（M_CHAIN_REGION_INDEX + 计入项/三维全列）、QC05/QC11 ⚠️、GAP-CHAIN-REG-METRICS 缺口真源指向注册表，禁止前端硬编码 |
| 11 D10 交互规范 | ✅ 不涉新交互；过程页/角标语义与既有 Figma 定制一致 |
| 12 demo/lumen 隔离 | ✅ 未触 demo 仓写路径；lumen 调用链无 demo 服务引用 |
| 13 对象存储桶（D14） | ✅ 结果走 `task.resultData` DB 全量，无对象存储写路径、无新桶新 key |
| 人机分工 §3 | ✅ 决策未外包：QC05/QC11/拆文与否（用户已在 /goal 授权合并）/开放项处置全部登记待人拍板，本文不替甲方拍板 |

## 6. cost 回填（budget-estimate.md §8.2 口径）

| 字段 | 值 | 说明 |
| --- | --- | --- |
| actual_tokens | 350000 | in+out 估算（全会话：两叶实码+5 篇金样+registry/指标/F·E·Java 交叉核对的阅读量 + 文档产出 ≈15k tokens） |
| model_used | glm-5.3-Flash | 本会话实际模型 |
| actual_cost | 0.05 | USD，按 Flash 档公开价估（in 80%/out 20% 比例）；green |
| cost_warn | green | < $5 阈值 |

> 注：agent 无法从 Console 取精确 in/out 分离值，按 default_ratios 估算；如需精确值由人工在 Cursor Analytics 补核。

## 7. 遗留与建议

- 同组实现单 `CHAIN-REGIONAL-NARRATE-L01`（任务注记：待本单 ready_to_sign 后开）建议范围=REGIONAL-01~04（prompt 外置+数字白名单+三态粒度+参数写死），本设计 §5.3 迁移方案可直接引用。
- REGIONAL-05（FE 接线包）涉 QC05/QC11 展示面，其中叶贡献/配置诚实块需先过产品定义。
- 半迁移态事实链（§5.3）为核对清单，后续迁移单勿凭记忆改写 pack 名与文件路径。
