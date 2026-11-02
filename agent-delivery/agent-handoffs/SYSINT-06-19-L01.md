# SYSINT-06-19-L01 · GDF：子学科与产业关联落地（同步+关联两过程）

> 范围真源：`agent-delivery/工程过程/04-系统集成/06-GDF数据治理集成/派单说明-SYSINT-06-19-L01.md`。图 `SYSINT-06-19-SEQ` 在该文件「调用时序」。未改图。任务保持 `in_progress`，未标 done，不写可对端。

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | pull |
| 说明 | 2026-10-31 用户下令领取并执行。前序 `SYSINT-TFMAP-02-L01` 已是 done。登记表原注「监管人待指定」，本次按下令验收前序的同一监管人填写。 |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `full` |
| 说明 | 一个脚本加建表语句。未新加依赖。未跳过调用链和 handoff。 |

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `SYSINT-06-19-SEQ` |
| 图 diff | 未改图。同步读本侧目录写映射表。关联在脚本内调模型，只写校验通过的行。查询不进作业。 |
| 会签态 | 派单未标 approved。按用户开工令交付脚本，不把会签态改绿。 |

## 范围与实现

GDF 两段作业，表和脚本在 `agent-delivery/data/GDF/派单包/子学科产业关联/GDF-SUBFIELD-TOPIC-WORKPACK/`。

- 作业 `subfield-topic-sync`：按 `subfield_id` 更新目录，不删已有关联。可 T+1 每天一次。
- 作业 `subfield-topic-link`：只允许人工触发。未映射子学科对上 `CL-*` 集群下已有产业的链节点。校验失败保持未映射。
- 核对用 `stats` / `query` 或 `sql/stats.sql`。只读，不触发同步或模型。

本仓没有在 GDF 平台上建这两段作业，没有执行 `sql/subfield_topic_map.sql`。

## 表名

产线：`gkxlumenx_dim.subfield_topic_map`。列与中台 TFMAP 的 `demo_gkxlumenx_dim.subfield_topic_map` 相同。2026-10-31 只读 information_schema：产线 dim 还没有这张表；demo dim 已有。脚本拒绝写入 `demo_` 开头的库。

## 与 TFMAP 的差异

| 项 | TFMAP | 本叶 |
|---|---|---|
| 触发 | 中台页面按钮 | GDF 作业。本仓未建作业 |
| 调用 | 页面 → 网关 → gkx-innov → 字典或 lumen-algo-py | 作业直接跑本包 Python。模型在脚本内，不配内部 HTTP |
| 表 | `demo_gkxlumenx_dim.subfield_topic_map` | `gkxlumenx_dim.subfield_topic_map`（语句已给，未执行） |
| 子学科来源 | 中台字典读久新 Doris | 只读本侧 `SUBFIELD_CATALOG`。不连久新 |

已映射 / 未映射的定义与中台相同。一个产业挂多个集群时，每个集群各留一行，不把集群列清空。

## 目录缺口

2026-10-31 只读 information_schema（未打印口令）：

- `ads_discipline_subfield` 不在 `gkxlumenx_ads`、`gkxlumenx_dim`、`demo_gkxlumenx_ads`、`demo_gkxlumenx_dim`。中台字典读的是久新 Doris `gkx_technology_analysis_dev.ads_discipline_subfield`。本脚本不连那台库。`SUBFIELD_CATALOG` 未配置时 sync 退出 3，不改映射表。
- 产线已有 `gkxlumenx_dim.industry_cluster`、`industry_cluster_map`，以及 `gkxlumenx_dwd.industry_chain`、`industry_chain_node`。本会话没有重数行数。没有可关联节点时，link 不调模型。
- 不编造节点，不用久新 `ads_industry.industry_id` 充当链节点。

## 偏离

中台页仍独立。未改企业、产业链、政策派单包，未改 Java 和前端。执行结果未回，不写可对端。

## 产物清单

- `agent-delivery/data/GDF/派单包/子学科产业关联/GDF-SUBFIELD-TOPIC-WORKPACK/README.md`
- `sql/subfield_topic_map.sql`
- `sql/stats.sql`
- `scripts/subfield_topic_gdf.py`
- 本 handoff

## 验收证据

`python scripts/subfield_topic_gdf.py --self-check` 输出 `self-check ok`。自检不连库。没有 GDF 作业执行回执。

## 架构合规自检

- ✅ 调用链：GDF 作业跑 Python；Java 不在本叶里转发模型
- ✅ 算法只在 Python
- ✅ 不写图库
- ✅ 脚本打印同步条数，以及关联的成功、失败、未触及条数
- ✅ 密钥不进 git
- ✅ 不把 demo 服务接到 lumen 前端，脚本拒绝写 demo 库
- ✅ 核对数字不加指标 ⓘ

## Cost 回填

本会话没有 Console 精确数。按主力档（输入 $3/M、输出 $15/M，算法 75/25）估算。

- actual_tokens: 40000
- model_used: grok-4.7
- actual_cost: 0.24
- cost_warn: green

## CI/CD

- 认领提交已推 `origin/dev`：`df8c374d`
- 派单包和本 handoff 停在本地，未推送
- 无 pipeline，无 GDF 作业，无 K8s rollout

ponytail: full
headroom: skip
