# 派单说明 · SYSINT-INDDISC-02-L01

```text
/goal doc-agent
身份：你是文档/定义轨 agent。本单只做「展示系统产业领域 ↔ 久新学科领域」两侧口径澄清与挂载方案，不是写业务代码、不是开深度页、不是改指标口径。
强度：ponytail off（定义任务）。不得用 YAGNI 删掉下面已锁定的口径认定和排除项。

任务：SYSINT-INDDISC-02-L01
标题：展示系统产业领域 ↔ 久新学科领域映射：两侧口径澄清与挂载方案
WBS：WBS-02-13
监管人：human:淮政玮
执行：agent:doc-agent。协作 data-agent（口径核验）、product-agent（展示侧口径确认）。同一 task-id，不另开任务。
状态：backlog。开工前 task-claim，claimed_by=agent:doc-agent，supervised_by=human:淮政玮。若认领要求先 ready，先改 ready 再认领。
仓：只写 gkx-orchestration。分支 origin/dev。业务仓一律不动。
开始时间：2026-10-31。完成日期要求：待指定。这两列是我方要求，不是久新承诺。

已锁定（执行时不得改口）：
1. 久新侧「学科领域」= 子学科 subfield_id，沿用 WBS-02-08 的口径。
   明确不用：上一级学科 field_id、技术节点 technology_node_id（那是 WBS-02-12）、正式技术目录 tech_id。
2. 展示侧「产业领域」本叶不预设真源、不先挑一张表当唯一口径，先把「产业领域」这个词在展示系统里对过的出处列全。已知至少四处，逐处写到表 + 字段：
   - 企业侧 dwd.enterprise_industry
   - 链目录 dwd_industry_chain_info
   - 机构标签 dwd_org_industry_tags
   - 久新机构产业覆盖 ads_institution_industry（industry_id / industry_name_zh）——这是产业分类，不是学科，不许当学科侧来对齐
   出处可能存在第五处及以上，查到即补，不得因为列表已有四项就停。
   每处必须标注角色，二分：①「筛选字典」——页面上那个下拉/筛选确实读它；②「仅指标口径」——只承担某个指标的统计口径，不承担页内筛选。
   清单列完后交 human:李伟 指定哪一处为准；在此之前，不得把其中任何一张写成已经对齐，也不得自行把多张合并成一张。

背景：展示系统大量数据已与久新对接，但展示系统侧的「产业领域」维度与久新侧的「学科领域」维度挂不上钩，导致按产业领域筛选/统计的口径与久新供给对不上。李伟 2026-10-31 提出，淮政玮同日认领进三要素集成，在本 WBS 收口。

目标：交出一份可会签的两侧口径对照与映射方案记录。记录要说清三件事：两侧各自的字典真源到什么粒度；哪些能映射、哪些不能；挂不上的部分走哪条已有叶补齐。UI「可用」≠ 已接入，不允许把未确认写成已对齐。

必读：
- 本文件（范围真源）
- agent-delivery/工程过程/04-系统集成/02-对接三要素/WBS.md（WBS-02-13）
- agent-delivery/工程过程/04-系统集成/02-对接三要素/技术方案.md
- agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/调研记录.md
- agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/表清单.csv
- agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/指标支持.csv（含 M_ORG_INDUSTRY_COVER）
- agent-delivery/工程过程/04-系统集成/02-对接三要素/派单说明-SYSINT-TFMAP-02-L01.md（只借【同步】【关联】过程，不改 subfield_topic_map）
- agent-delivery/工程过程/04-系统集成/02-对接三要素/README.md（三要素垂向边界）
任务查询只用 MCP task-get / task-query。禁止读 task-registry.yaml。

范围：
1. 口径真源。① 久新侧「学科领域」= 子学科 subfield_id：写到表 + 字段 + 枚举（沿用 WBS-02-08），并写明被排除的另三套口径（field_id / technology_node_id / tech_id）各自属于谁、为什么不用。② 展示侧「产业领域」不预设：先把上述出处（dwd.enterprise_industry、dwd_industry_chain_info、dwd_org_industry_tags、久新 ads_institution_industry 及其 industry_id / industry_name_zh）逐处写到表 + 字段，标注「筛选字典 / 仅指标口径」、维护方与取值方式；清单交付给 human:李伟 指定真源。
2. 映射结果。给出领域对领域的映射表：可映射的写清依据（同名 ID / 字典对齐 / LLM 判定），不可映射的每一项明写原因。禁止编造映射。
3. 影响面。列出受影响的展示页面与指标（含 M_ORG_INDUSTRY_COVER 一类），标清哪些现在是空态、哪些口径不一致。
4. 补齐路径。挂不上的部分给出一条明确路径：复用 WBS-02-08 的 subfield_topic_map / 新建映射表 / 展示侧改口径，并指明归属哪条已有 WBS 叶。本叶不另开实现叶。
5. handoff：agent-delivery/agent-handoffs/SYSINT-INDDISC-02-L01.md。含 ponytail: off。evidence 指向该 handoff 和本派单。

DoD（与注册表一致）：
1. 两侧口径真源写明到表 + 字段 + 枚举级；展示侧「产业领域」给出上述出处清单（至少 dwd.enterprise_industry、dwd_industry_chain_info、dwd_org_industry_tags、久新 ads_institution_industry），每处标注「筛选字典 / 仅指标口径」，久新 ads_institution_industry（industry_id / industry_name_zh）标注为产业分类而非学科。清单待 human:李伟 指定真源，在此之前不写「已对齐」。
2. 给出领域对领域的映射表；不可映射项明写原因，不编造映射，不把未确认写成已对齐。
3. 补齐路径建议指明归属哪条已有 WBS 叶（WBS-02-08 / 02-12 等），本叶不另开实现叶。
4. 本叶只出口径记录与 handoff，不写业务仓代码、不改指标 seed、不写 ADS、不改 WBS-02-08 已有映射。不要把任务标 done（签收闸门）。

禁止：
- 重开 WBS-02-03，或新建技术链、人才、科研机构深度分析页。
- 修改 demo-ui-system-test、lumen-ui-science-pc、展示 Java、Python 业务仓。
- 改写 subfield_topic_map，或把本叶并进 SYSINT-06-19。
- 改指标口径、改 seed、改 D1–D4、写 ADS。
- 把 0 行表解释成「没有」，把模拟数据当真实覆盖。
- 把展示侧任一张表（dwd.enterprise_industry / dwd_industry_chain_info / dwd_org_industry_tags / ads_institution_industry）写成已经对齐或直接当成唯一真源；真源由 human:李伟 指定后才能动。
- 用 field_id / technology_node_id / tech_id 顶替久新侧学科领域口径。
- task-create 本叶以外的新叶。
```
