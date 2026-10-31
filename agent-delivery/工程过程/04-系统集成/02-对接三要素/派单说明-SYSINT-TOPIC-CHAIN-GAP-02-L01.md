# 派单说明 · SYSINT-TOPIC-CHAIN-GAP-02-L01

```text
/goal doc-agent
身份：你是文档/定义轨 agent。本单是专题侧缺口清单收口，不是写业务代码、不是开深度页。
强度：ponytail off（定义任务默认 off）。

任务：SYSINT-TOPIC-CHAIN-GAP-02-L01
标题：专题·产业链分析三要素嵌入供数缺口清单收口
WBS：WBS-02-10
监管人：human:淮政玮
执行：agent:doc-agent。协作 product-agent（口径确认）。同一 task-id，不另开任务。
状态：backlog。开工前 task-claim，claimed_by=agent:doc-agent，supervised_by=human:淮政玮。若认领要求先 ready，先改 ready 再认领。
仓：gkx-orchestration。分支 origin/dev。MCP 写 registry 后须立刻 commit + push。
开始时间：2026-10-31。完成日期要求：待指定。这两列是我方要求，不是久新承诺。

目标：把已落盘的分析稿收成可会签的专题侧缺口清单，挂进技术方案 §5.3 与本维 WBS。不派产业链 Job 嵌入实现，不重开 WBS-02-03 深度叶。

必读：
- agent-delivery/工程过程/04-系统集成/02-对接三要素/专题-产业链分析-三要素对接需求.md（缺口真源，已有草稿）
- agent-delivery/工程过程/04-系统集成/02-对接三要素/WBS.md（WBS-02-10）
- agent-delivery/工程过程/04-系统集成/02-对接三要素/技术方案.md §5.3
- agent-delivery/工程过程/04-系统集成/02-对接三要素/README.md（三要素垂向边界）
- repos/lumen-ui-topic/src/config/industryWorkspace.ts（参数/因子/维度真源）
任务查询只用 MCP task-get / task-query。禁止读 task-registry.yaml。

范围：
1. 核对并补全清单：产业周期、区域产业指数、关键环节、瓶颈堵点、深圳对比、深圳发展、区域竞争力、全景主流技术路线。
2. 只标三要素垂向（技术/技术链、人才、科研机构）。市场/资本/政策/企业商业化标「非本项」。
3. 每条写清页内 metric_id、数据收集、接口是否具备；UI「可用」≠ 已接入。
4. 方案 §5.3、WBS-02-03 行文与 README 入口保持与清单一致。
5. handoff：agent-delivery/agent-handoffs/SYSINT-TOPIC-CHAIN-GAP-02-L01.md。

DoD：与注册表 definition_of_done 一致。不要把任务标 done（签收闸门）。联调确认词不适用本定义叶；会签通过后由监管人推进。

禁止：
- 重开 WBS-02-03 或新建技术链/人才/科研机构深度分析页。
- 在本叶派 frontend/api/algorithm 改 lumen-ui-topic Job 读链。
- 改指标 seed、改 D1–D4、写 ADS。
- 把 SCI-INT 展示叶写成专题已覆盖。
- task-create 本叶以外的新叶（对齐叶已建 SYSINT-TOPIC-CHAIN-ALIGN-02-L01，勿重复建）。
```
