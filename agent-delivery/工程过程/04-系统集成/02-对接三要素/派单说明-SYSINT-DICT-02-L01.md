# 派单说明 · SYSINT-DICT-02-L01

```text
/goal algorithm-agent
身份：你是经验丰富、遵循最佳实践的资深算法/数据工程师。本单是字典只读接口，不是模型、不是指标计算。算法与字典查询只在 Python。Java 只转发。
强度：ponytail full（默认）。禁止用 YAGNI 跳过 D8/D9/D10、可观测与架构铁律。
图：必含 SYSINT-DICT-02-SEQ。先写调用时序再写代码。沿用技术方案 SYSINT-SCHEME-02-SEQ 的读链，本叶只加 Python 只读久新字典表。不另画全局拓扑。图文冲突以图为准。必读 agent-delivery/diagram-as-contract.md。

任务：SYSINT-DICT-02-L01
标题：专题字典下拉：只读久新 ADS 字典并做成内部 API
监管人：human:淮政玮
执行：agent:algorithm-agent。协作 api-agent（Java 只转发）、frontend-agent（政策三页接线）。同一 task-id，不另开任务。
状态：backlog，未认领。开工前 task-claim，claimed_by=agent:algorithm-agent，supervised_by=human:淮政玮。若认领要求先 ready，先把状态改到 ready 再认领。未获监管人确认不改业务仓。
仓：lumen-topic-py 为主；Java 在 lumen-svc-platform 的专题服务，只转发；页面在 lumen-ui-topic（Vue 3 + Arco Design Vue）。分支 dev。业务仓完工停在本地，不自行 commit / push，除非监管人明确说提交。
开始时间：2026-10-27。完成日期要求：待指定。这两列是我方要求，不是久新承诺。

目标：专题字典下拉改为只读久新 Doris 库 gkx_technology_analysis_dev 的字典表，接口放在 lumen-topic-py 的 /internal/*。不放 gkx_show_service。行为对照 iticsci 的 topic-common/dict，不改那两个 iticsci 仓。

图放在 agent-delivery/工程过程/04-系统集成/02-对接三要素/字典下拉接口.md，diagram_id 为 SYSINT-DICT-02-SEQ，用 sequenceDiagram。节点名用仓名：lumen-ui-topic、网关、lumen-svc-platform、lumen-topic-py、久新 Doris。handoff 引用同一张图。

调用方向（必须落在图上）：
专题前端 → 网关 → 专题 Java（只转发） → lumen-topic-py /internal/* → 只读久新 Doris。
前端不直连久新，不直连 Python。Java 不使用只读账号 test2。密码、完整连接串不进 git。连接坐标只读 对接文档/对端/README.md，密钥走环境变量或 Secret。

必读：
- agent-delivery/工程过程/04-系统集成/02-对接三要素/字典下拉接口.md（范围真源）
- agent-delivery/工程过程/04-系统集成/02-对接三要素/WBS.md（WBS-02-07）
- agent-delivery/工程过程/04-系统集成/02-对接三要素/对接文档/对端/README.md
- agent-delivery/architecture-baseline.md（调用链、D12、D15）
- agent-delivery/diagram-as-contract.md
- iticsci-tech-topic-backend 的 topiccommon/controller/dict 与 iticsci-tech-topic-frontend 的 blade-kj-topic-common-dict.ts（只读对照，不改）
- lumen-ui-topic 的 PolicyAnalysisConfigPage.vue（三个政策路由共用）
任务查询只用 MCP task-get / task-query。禁止读 task-registry.yaml。

范围：
1. lumen-topic-py 提供内部字典接口，只读这些表：ads_discipline_domain、ads_discipline_field、ads_discipline_subfield、ads_discipline_topic、ads_talent_taxonomy 的当前 PUBLISHED release 及其 ads_talent_taxonomy_node、ads_institution_type、ads_location、ads_industry。复用仓内已有 /internal 路由和配置；没有现成只读客户端时按仓内写法加一处。不写 ADS。
2. 列表保留按名称关键字过滤。分页保留页码和页大小。返回带该表 data_version。树带父子 id。技术领域选项值用 subfield_id，名称只用中文名；没有中文名则留空，不把英文抄成中文。机构类型保留类型代码，company 是企业，不是科研机构。地理位置支持中国、仅深圳两档。
3. 专题 Java 只转发上述接口。不在 Java 写查询 SQL，不直连久新。
4. 政策时序 /policy/overview、区域政策对比 /policy/analysis、深圳政策现状 /policy/recommendation 的「技术领域」多选改读子学科字典。表没有行就返回空列表，页面保持空选项，不用 fixture 填数。布局和样式不动，继续用 Arco 多选。产业下拉仍走现有产业集群目录，不换成 ads_industry。
5. Field、Topic、人才类型、机构类型、地理位置、产业分类先有接口。本叶不新开页面，不新开菜单。

DoD（与注册表一致）：
1. lumen-topic-py 提供上述字典内部接口。只读。密码不进 git。不写 ADS。
2. 专题 Java 只转发。前端不直连久新、不直连 Python。Java 不使用 test2。
3. 政策三页的「技术领域」多选改读子学科字典。表空则选项为空。产业下拉不变。
4. 不建技术链、人才、科研机构深度分析页。不改 iticsci 专题仓。company 不算科研机构。handoff 指向字典下拉接口清单。
5. handoff：agent-delivery/agent-handoffs/SYSINT-DICT-02-L01.md。含 ponytail: full。evidence 指向该 handoff、字典下拉接口.md（含 SYSINT-DICT-02-SEQ）和三个业务仓的本地改动路径。不要把任务标 done。联调确认词只在监管人确认后写入。

可观测：新的 Python /internal 路由沿用仓内已有 OTel。不新做角标类型。字典选项不是统计指标，不为每条选项加 ⓘ。已有指标角标保持不动。

禁止：
- 重开 WBS-02-03，或新建技术链、人才、科研机构深度分析页。
- 修改 iticsci-tech-topic-backend、iticsci-tech-topic-frontend。
- 把接口放到 gkx_show_service，或让前端、Java 直连久新。
- 继续用政策 indicators 的 kind=tech_field 当技术领域目录。
- 用 fixture、Mock 或随机数填空表。
- 把政策页产业下拉换成久新 ads_industry。
- 把 QPOL-tech 写成已确认。有选项不等于分类体系已经甲方确认。
- 在本叶做指标计算、写 ADS、建表、灌数。
- 把密码或完整连接串写入 git。
- task-create 新叶，或修改本任务以外的 depends_on、状态、DoD。
- 业务仓自行 commit / push。
```
