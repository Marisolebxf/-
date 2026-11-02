# SYSINT-06-20-L01 · GDF：技术节点与产业映射落地（同步+关联两过程）

> 状态仍是 in_progress。本交接不把任务标 done，不写可对端。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | 派单写明监管人徐滕强。前序 `SYSINT-TECHMAP-02-L01` 当时是 `ready_to_sign`，不是 `done`。2026-10-31 用户下令领取并执行。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 脚本只覆盖同步、关联、只读核对和一次不连库自检。未新加依赖。未改中台页、Java、lumen 前端、企业/产业链/政策/子学科包。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SYSINT-06-20-SEQ` |
| 图 diff | 未改图 |
| 会签态 | 派单说明未标 `approved` |
| 说明 | 图上写「模型只在本脚本内调用」。已推送的中台方案把关联收成名称向量余弦，本脚本按那个口径调用向量服务，不另开对话模型，不经 Java |

## 范围与实现

产线表 `gkxlumenx_dwd.dwd_tech_node_industry_map`。建表语句在派单包，本会话没有执行。脚本发现表不存在就退出 4，自己不建表。`DWD_SCHEMA` 或 `DIM_SCHEMA` 以 `demo_` 开头则拒绝。不写入 `subfield_topic_map`。

同步作业名 `tech-node-industry-sync`。脚本用 MySQL 协议只读久新 Doris `47.93.119.170:29030`，库 `gkx_technology_analysis_dev`，表 `ads_technology_profile`，账号 `test2`。2026-10-31 用户下令把久新只读密码明文写入派单包 README，供 GDF 独立连库。脚本仍只读环境变量 `JX_ADS_PASSWORD`。每页 500，按 `technology_node_id` 排序。`technology_name_zh` 原样进 `name_zh`，空中文不抄英文。不整表清空，不删已有关联。目录为空不改表。某一页失败时已提交的页保留。不调用 `lumen-topic-py`。

关联作业名 `tech-node-industry-link`。只许人工触发。只处理还没有非空 `node_id` 的技术节点，每批 20，一次触发连续跑到没有未映射或某一批失败。候选来自 `gkxlumenx_dim` 的 `CL-*` 和 `gkxlumenx_dwd` 的 `industry_chain` / `industry_chain_node`。每个技术节点只留余弦最近的一个产业节点，同分留更靠前的候选。没有候选节点时不调用向量。向量失败只给这一批空行写 `fail_reason`，后面的节点保持未映射。一个产业挂多个集群时按集群各写一行。

已映射 = 至少一条非空 `node_id`。未映射 = 已同步但没有这样的行。`stats` 和 `sql/stats.sql` 只读，不进作业。空关键字只看已关联。展示名有中文用中文，否则用英文，中文列仍原样。

## 偏离

图和派单初稿写的是对话模型。过程真源 `方案-SYSINT-TECHMAP-02-L01.md` 在 `6c919236` 改成名称向量最近邻。本叶按方案，不按初稿的对话模型。

前序任务没有签收成 `done`。用户在它处于 `ready_to_sign` 时下令领取本叶。

2026-10-31 用户要求 GDF 能独立还原第一次同步。脚本改为直接按页读久新 `ads_technology_profile`。密码明文只出现在派单包 README，这是用户当场指定的例外。

## 产物清单

| 路径 | 内容 |
|---|---|
| `agent-delivery/data/GDF/派单包/技术节点产业映射/GDF-TECH-NODE-WORKPACK/sql/dwd_tech_node_industry_map.sql` | 产线建表语句，未执行 |
| `agent-delivery/data/GDF/派单包/技术节点产业映射/GDF-TECH-NODE-WORKPACK/sql/stats.sql` | 只读两侧清单 |
| `agent-delivery/data/GDF/派单包/技术节点产业映射/GDF-TECH-NODE-WORKPACK/scripts/tech_node_industry_gdf.py` | sync / link / stats / query / --self-check |
| `agent-delivery/data/GDF/派单包/技术节点产业映射/GDF-TECH-NODE-WORKPACK/README.md` | 作业名、环境变量、退出码 |

登记认领已写入。派单包和本交接还在本地，未推送。

## 验收证据

`python scripts/tech_node_industry_gdf.py --self-check` 输出 `self-check ok`，退出码 0。这一步不连库、不调向量。

没有在 GDF 上建作业。没有执行建表。没有跑 sync 或 link。执行结果未回，不写可对端。

## 架构合规自检

- ✅ 调用链：GDF 作业只跑这份 Python。Java 和页面只读已落库表，不在本叶改代码
- ✅ 算法只在 Python。向量调用在本脚本内，不经 Java
- ✅ 图谱：本叶不写图库
- ✅ 可观测：脚本打印同步页数和关联处理、失败条数。不为每个技术节点加指标 ⓘ
- ✅ D12：不调用 demo 服务，不写 `demo_gkxlumenx_*`
- ✅ 不把企业当成科研机构。不把英文抄进 `name_zh`。不用模拟商业价值填映射
- ✅ 同步只读久新 Doris 画像表并写入本侧映射表。Java 和页面不直连久新。久新只读密码按用户 2026-10-31 例外写在派单包 README，不写进脚本

## 遗留

- 同步要在作业机配置 `JX_ADS_PASSWORD`。地址、账号、库、表已写在脚本和 README。本会话没有连久新试拉。
- 产线表本会话没有创建。表不存在时脚本退出 4。
- GDF 工位上的两个作业还没有建。
- 前序 `SYSINT-TECHMAP-02-L01` 仍待 `human:淮政玮` 签收。

## Cost 回填

没有 Console 精确数。按本叶会话量级估算，价表没有 Grok 档，沿用主力档（输入 $3/M、输出 $15/M，75/25）。

- actual_tokens: 45000
- model_used: grok-4.7
- actual_cost: 0.27
- cost_warn: green

ponytail: full
diagram_id: SYSINT-06-20-SEQ
headroom: skip
