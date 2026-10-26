# DOC-CHAIN-CYCLE-ANALYSIS-CHAIN-L01 · Handoff

| 项 | 内容 |
| --- | --- |
| 任务 | 产业周期分析 — 完整分析链路设计 + LLM 落点（05.2.1） |
| 角色 | architect-agent（+algorithm 视角；监管人 human:徐滕强） |
| 强度 | ponytail: off（definition 设计任务） |
| 状态 | 产物完成，进会签（integration） |

## 范围与实现

按 skill `gkx-topic-analysis-chain-design` 四步，为产业链「产业周期分析」叶（`chain:diagnosis:cycle` / `cycle.graph.v1`）产出完整链路设计 + LLM 落点，本单只设计不写业务仓实现：

- **A 现状对照**：政策金样 05.6.1 / 企业评价 05.3.1(v0.3) / cycle as-built 三方对照；差距 G1~G7 + G-FE-1（文档 §12）。
- **B 完整链路**：触发指纹单飞 → 参数冻结（QC06 ADS 预填）→ 五真实节点 1:1 过程页（freeze/retrieve/diagnose_stage/forecast/validate_assemble）→ job_runtime 厨房 → arts 管线 → `chain.cycle.result_payload.v1` → Java 唯一签发 `res-{taskId}`（resultData DB 全量，无 RustFS 写路径）→ `parseCycleBoard` 字段映射（§2~§6、§10）。
- **C LLM 落点专章**：流程内双落点（L1 相位确认 `cycle.diagnose.v2` temp0.1/512tok/8s；L2 趋势归纳 `cycle.forecast.v2` temp0.3/1024tok/15s）；护栏=不得改判（confirmed==primary）+ 数字白名单 + 临时口径语气；失败 `degraded` 不改任务终态（§7）。
- **D Prompt v2 草案**：`lumen_common/prompts/chain/` 版本化文件目标态 + 两份 system 全文 + 白名单伪代码（§8）；现状内联为 chain 域共性债，本单只落 cycle 两文件（OPEN-CY-1）。
- **E as-built 契约五段**：create / execute(202) / stages / complete / poll-result；无新接口，LLM 对上层屏蔽（§9）。
- **F 企业域差异**：单收尾 vs 双落点=域间合理差异；`honesty.llm` ↔ `narration` 语义等价映射，命名冻结（§11）。
- **G 开放项**：OPEN-CY-1~5 + QC03/QC06/QC10 🟡 只引用不拍板（§13）。

## 偏离说明

1. 交付清单原文要求「RustFS 结果 JSON schema 的 key 约定」——as-built 实查该叶结果走 `task.resultData` DB 全量（`resultBucket/resultUrl=null`），无对象存储写路径；按实设计为「无新增 key」并在 §9 登记，报告导出归 `chain:report:export` 另域。已获监管人 2026-10-26 确认。
2. 文档落位用 `05.2.1-产业周期分析链路.md`（进 05.2 总册序列，体例对齐 05.3.1），未用清单建议的 `agent-handoffs/.../DOC-CHAIN-CYCLE-ANALYSIS-CHAIN-L01.md` 命名；任务号照登 registry。

## 产物清单

| 产物 | 位置 |
| --- | --- |
| 设计文档 v0.1 | `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.2.1-产业周期分析链路.md` |
| 总册指针 | 同目录 `05.2-产业链.md` §8 |
| registry | `DOC-CHAIN-CYCLE-ANALYSIS-CHAIN-L01`（definition，P1，epic DOC-CHAIN-CYCLE） |

## 验收证据

- commits：`1263bbeb`（文档+指针）、`47f9e9b2`（registry 登记），均已 push `origin/dev`。
- 评审过程：监管人逐步走查（A 表点头 → 五追问澄清 → 五决策冻结 → 批准落笔）。
- 指标实查：metric-registry MCP `M_CHAIN_CYCLE_STAGE` / `M_CHAIN_PHASE_DETERMINATION` / `M_CHAIN_MARKET_SIZE`（QC03/QC06 🟡，D4 mock，与 payload honesty 一致）。

## 架构合规自检

| 铁律 | 自检 |
| --- | --- |
| 调用链 前端→Java→Python /internal | ✅ §2/§9，Java 唯一发号签发、禁 Python 自签 |
| 算法只在 Python / LLM Key 边界 | ✅ LLM 仅算法侧 Common 管道，Key 只在集群 Secret `gkx-zhipu-llm` |
| 不替甲方拍板 | ✅ QC03/QC06/QC10 只引用 🟡；两套相位口径并存登记不调和（§12 G7） |
| D9 指标 8 件套 / Design.md | ✅ KPI 带 metric_id+QC03/QC06 角标；mock 不改绿；ⓘ 呈现以 Job 快照口径为准 |
| demo/lumen 隔离（D12） | ✅ 本单只涉 lumen 仓 as-built 引用，零 demo 依赖 |
| RustFS（D14） | ✅ 无新写路径、无自造桶/目录 |

## 后续建议单

- `CHAIN-CYCLE-NARRATE-L01`（algorithm）：Prompt v2 两文件落盘 + loader + 数字白名单 + `_narrate_client` 式单测（OPEN-CY-1/2）。
- api 侧：Java cycle 结果 schema 校验（OPEN-CY-3）；frontend 侧：CI 阴影带接线（OPEN-CY-4）。
