# 派单说明 · SYSINT-TOPIC-CHAIN-ALIGN-02-L01

```text
/goal data-agent
身份：你是数据/指标对照 agent。本单只出「页内 metric ↔ 久新 ADS」对照记录，不是灌数、不是改 seed、不是开深度页。
强度：ponytail lite。禁止用 YAGNI 跳过 D9 诚实性（未对齐不标已接入）。

任务：SYSINT-TOPIC-CHAIN-ALIGN-02-L01
标题：专题产业链三要素指标与久新 ADS 对照对齐（只出记录）
WBS：WBS-02-11
监管人：human:唐绍祖（已指派；claimed_by / supervised_by 同此人）
执行：可由 human:唐绍祖 本人推进，或再派 agent:data-agent（须其确认）。协作 doc-agent。
状态：claimed。依赖 SYSINT-TOPIC-CHAIN-GAP-02-L01。依赖未到 ready_to_sign/会签确认前不要开工实现对照终稿；可先读调研草稿。
仓：gkx-orchestration。分支 origin/dev。
开始时间：2026-10-31。完成日期要求：待指定。

目标：按缺口清单总表，对技术成熟度、专利、科研机构、技术壁垒、人才结构、瓶颈·技术/人才等写出对照表。三分清单未到前不判「归久新 / 归智树自算」。

必读：
- agent-delivery/工程过程/04-系统集成/02-对接三要素/专题-产业链分析-三要素对接需求.md
- agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/指标支持.csv
- agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/调研记录.md
- agent-delivery/metric-mcp-usage-guide.md（只用 metric-get / metric-query，禁止直接读 seed YAML）
- agent-delivery/工程过程/04-系统集成/02-对接三要素/WBS.md（WBS-02-11）

范围：
1. 对照列至少含：页面、指标名、页内 metric_id、候选久新 metric_id、候选表、库内支持、字段缺口、口径是否同、待三分清单。
2. 产物落在本维夹或 agent-handoffs/SYSINT-TOPIC-CHAIN-ALIGN-02-L01/，路径写入 handoff。
3. 与 TOPIC-CHAIN-METRIC-MIGRATE-L01（demo M_CHAIN_* 口径迁移）分流，本叶不做前端改口径。

DoD：与注册表 definition_of_done 一致。

禁止：
- 改 cfg_metric seed / readiness 矩阵 / D1–D4。
- 写 ADS、灌数、建离线作业。
- 重开 WBS-02-03；建 Job 嵌入实现叶。
- 把「有行」写成「已对齐」或「已接入」。
```
