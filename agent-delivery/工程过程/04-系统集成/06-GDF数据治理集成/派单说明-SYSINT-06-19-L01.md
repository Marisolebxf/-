# 派单说明 · SYSINT-06-19-L01

```text
/goal algorithm-agent
身份：你是数据治理 / 算法落地 agent。本单把「子学科 ↔ 产业」的【同步】【关联】两过程落到 GDF 平台，不是改中台 demo 页，不是开专题深度页。
强度：ponytail full。算法与模型只在 Python；Java 不算、不调模型。密码与模型密钥不进 git。

任务：SYSINT-06-19-L01
标题：GDF：子学科与产业关联落地（同步+关联两过程）
WBS：WBS-06-19
监管人：待指定。未指定前不认领、不改产线。指定后 task-claim，claimed_by=agent:algorithm-agent，supervised_by 用指定的人。
执行：agent:algorithm-agent。协作 data-agent、api-agent。GDF 侧实施可按协作指南对接辜少彬团队，沟通结论记本维流水。
状态：backlog。依赖 SYSINT-TFMAP-02-L01（过程真源）。
仓：编排仓派单包 / GDF 工位与脚本；不把作业写进 lumen 业务仓。分支 origin/dev。MCP 写 registry 后立刻 commit + push。
开始时间：2026-10-31。完成日期要求：暂无截至时间。

目标：在 GDF 上具备与图1（中台「子学科与专题映射」）同语义的两按钮过程——【同步】【关联】——以及已映射/未映射清单与数量。过程对照第 02 项 WBS-02-08，本叶是 GDF 侧生产落地。

过程对照（图1 / TFMAP）：
1. 【同步】：把子学科目录写入映射存储；按 subfield_id 更新名称与版本；不整表清空；不删除已有关联。
2. 【关联】：人工触发；只处理未映射子学科；候选为已有产业集群 / 产业 / 产业节点；非法 id 丢弃，该行保持未映射；失败可见。
3. 统计：已映射 / 未映射两侧列表（中文名 + subfield_id）与数量。
4. 查询：只读映射结果；不自动同步、不自动关联。

必读：
- agent-delivery/工程过程/04-系统集成/02-对接三要素/派单说明-SYSINT-TFMAP-02-L01.md（过程与调用边界真源）
- agent-delivery/工程过程/04-系统集成/06-GDF数据治理集成/WBS.md（WBS-06-19）
- agent-delivery/data/GDF/GDF协作指南.md
- agent-delivery/architecture-baseline.md（算法只在 Python；页面/Java 不直连久新）
任务查询只用 MCP。禁止读 task-registry.yaml。

范围：
1. 在 GDF 约定落点实现两过程（作业、脚本或工位，以监管人与 GDF 约定为准）。表结构、作业名写入 handoff。
2. 与 TFMAP 对照：同语义、可有平台差异；差异必须在 handoff 写明。
3. 产出编排仓说明或派单包片段（路径自定，写进 handoff）。不改企业/产业链/政策现行贴源包的 Wave A/B 范围。
4. 消费方：下游只读已落库映射；不在请求线程打久新字典或现算 LLM。

DoD：与注册表 definition_of_done 一致。执行结果未回不写可对端。不要标 done。

禁止：
- 用本叶代替 WBS-06-02 产业链贴源跑通。
- 用本叶关掉或重写 demo-ui-system-test 的 TFMAP 页（第 02 项仍独立）。
- 重开 WBS-02-03 深度页；改 iticsci 仓。
- Java 写提示词或调模型；前端/Java 直连久新。
- 密码、模型密钥进 git；fixture 填映射。
- 把未回传的执行结果写成可对端或已接入。
```
