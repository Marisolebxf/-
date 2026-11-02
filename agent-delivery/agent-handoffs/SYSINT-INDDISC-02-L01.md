# SYSINT-INDDISC-02-L01 · 展示系统产业领域 ↔ 久新学科领域映射：两侧口径澄清与挂载方案

> 定义任务。只写编排仓。领域对领域没有可确认映射。不标已对齐。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:doc-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 2026-10-31 淮政玮下令认领并执行。任务原为 backlog。未手改 ready，由 MCP `task-claim` 从 backlog 进入 claimed，再进入 in_progress |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | 定义任务。派单锁定的口径和排除项保留 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本单读派单、调研清单和已有代码里的表字段，不用压缩代替 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无。本叶不改架构图 |
| 图 diff | 无 |
| 会签态 | 不涉及 |
| 说明 | 只增口径记录 |

## 问题清单

- 展示系统「产业领域」字典是哪张表、哪个字段。
- 久新「学科领域」是否就是子学科 `subfield_id`。
- 两侧能不能做领域对领域映射；不能的原因是什么。
- 挂不上的部分归哪条已有 WBS 叶。

## 修改内容

- 口径记录：`agent-delivery/工程过程/04-系统集成/02-对接三要素/方案-SYSINT-INDDISC-02-L01.md`
- 结论：久新侧锁定为 `ads_discipline_subfield.subfield_id`（调研时 252 行）。展示侧筛选字典是深圳 10+5：种子 yaml，以及 `{INNOV_DIM_SCHEMA}.industry_cluster.cluster_id`（`CL-*`）和 `industry_cluster_map.industry_id`（`INB*`）。页面文案是「产业分类」。
- 领域对领域：没有同名 ID，没有已对齐字典。6 行对照全部是不可映射或排除，原因写在方案 §3。不编造名称对照。
- `M_ORG_INDUSTRY_COVER` 的候选表是 `ads_institution_industry`（久新产业分类，无 `subfield_id`）。D1 `draft`，D4 `mock`，口径还没有。
- 补齐：子学科落到展示集群，归 WBS-02-08 已有的 `subfield_topic_map`，本叶不改表，也不把已有 LLM 行标成已对齐。机构产业覆盖对不上展示 `INB*` 或 `subfield_id`，WBS-02-08 与 WBS-02-12 都接不住，本叶不另开实现叶。
- **2026-11-01 追加（李伟口径）**：久新侧学科领域进一步排除上一级 `field_id` / `domain_id` 与下一级 `topic_id`，只留子学科 `subfield_id`。新增方案 §2.4「展示侧产业领域出处清单」，列出五处——① `industry_cluster` + `industry_cluster_map`（`CL-*` / `INB*`，**筛选字典**）；② `dwd_industry_chain_info`（目录类，角色待定）；③ `dwd_org_industry_tags`（主体↔链标签，`INB*` 多码未拆行，角色待定）；④ `dwd.enterprise_industry`（企业侧画像，**仅指标口径**）；⑤ 久新 `ads_institution_industry`（**产业分类非学科**，只是 `M_ORG_INDUSTRY_COVER` 候选）。五处互不合并，真源交 `human:李伟` 指定，在此之前不写已对齐。§3 相应加两行（第 2–4 项未结论、`field_id` 排除）。

## 测试结果

- 对照来源：派单、WBS-02-13、调研表清单 / 字段清单 / 指标支持、字典下拉接口、TFMAP 派单与 `subfield_topic_map` 建表、展示 `IndustrySelect` 与集群种子、专题 `IndustryClusterService` 与子学科关联所用集群 SQL。
- 未改业务仓，未跑页面，未查线上行数。行数用调研记录当时快照。

## 遗留风险

- `SYSINT-SURVEY-02-L01` 仍是 `in_progress`，不是 `done`。本叶使用的是已落盘的调研记录。扫描不会因该依赖未签收而把本任务升到 ready。
- WBS-02-08 已有 130 个已映射子学科。本叶未逐条复核，不能当成领域字典。
- 展示页有的列名写成「产业领域」，本叶只确认了「产业分类」级联的字典。那些列名的行键未逐页核对。
- §2.4 清单里第 2/3 项（`dwd_industry_chain_info`、`dwd_org_industry_tags`）与第 1 项 `INB*` 的同源关系**未核**；`dwd_org_industry_tags` 的多码拆行、空值、与主档 JOIN 键仍未书面确认（ENT-P0-2 待回复）。第 4 项 `dwd.enterprise_industry` 是否实装、行数多少本叶未查。这三条都影响「哪一处能当筛选字典」的判断，故角色一律写「待定」，等 `human:李伟` 指定。

## CI/CD（必填）

- 分支：`gkx-orchestration` `origin/dev`
- commit：随本 handoff 提交
- pipeline URL / ID：编排仓无业务 CI
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：无运行时变更

## 可观测性（建议）

- 无新接口，无 trace

## 涉及文件

- `agent-delivery/工程过程/04-系统集成/02-对接三要素/方案-SYSINT-INDDISC-02-L01.md`
- `agent-delivery/工程过程/04-系统集成/02-对接三要素/WBS.md`
- `agent-delivery/工程过程/04-系统集成/02-对接三要素/沟通流水.md`
- `agent-delivery/agent-handoffs/SYSINT-INDDISC-02-L01.md`

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 / 算法只在 Python | 未改代码 |
| D12 不调 demo 服务 | 未改 lumen 前端 |
| D9 指标 | 未改 seed，未把 draft/mock 写成已对齐 |
| D14 / D16 | 未写 ADS，未写桶 |
| D17 | 未改合规算法 |

## 成本

| 字段 | 值 |
|---|---|
| actual_tokens | 80000 |
| model_used | grok-4.7 |
| actual_cost | 0.34 |
| cost_warn | green |
| 说明 | 无控制台分项。按任务估量 80000、输入 90% / 输出 10%，用预算表 Sonnet 档 $3 / $15 每百万 token 计算：0.216 + 0.120。价表没有 grok-4.7 |

ponytail: off
