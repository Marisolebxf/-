# 方案 · SYSINT-TOPICMAP-02-L01

Topic 是久新库五类主体（人才/机构/论文/专利/项目）都挂的学科维度，平台统一 `topic_id`（`top_<hex32>`）。本方案仿照「技术节点与产业映射」（[方案-SYSINT-TECHMAP-02-L01.md](./方案-SYSINT-TECHMAP-02-L01.md)），把 `ads_discipline_topic`（4,516 个 Topic）同步进本侧表，再做 Topic→产业节点的关联。可行性判定见 [Topic桥可行性判定.md](./调研/Topic桥可行性判定.md)。

## 菜单

算法中台 `demo-ui-system-test`，维护管理，与「技术节点与产业映射」并列。

| 项 | 值 |
|---|---|
| 菜单名 | Topic与产业映射 |
| 路由 | `/ops/topic-map` |
| 按钮 | 【同步】【关联】。打开页面、查询都不触发这两步 |

## 可同步与排除

| 久新表 | 行数量级 | 决定 | 原因 |
|---|---:|---|---|
| `ads_discipline_topic` | 4,516 | **同步** | Topic 字典主数据。主键 `topic_id`，含中文名（已审核）、英文名、所属 subfield/field/domain |
| `ads_discipline_subfield` / `field` / `domain` | 252 / 26 / 4 | **同步** | Topic 的上级字典，页面级联与血缘展示需要 |
| `ads_talent_topic_profile`（684.7 万） | 不同步 | 主体挂接表，消费侧按 topic_id 过滤时读久新镜像（阶段二圈表），不是本叶的映射对象 |
| `ads_institution_topic_entry`（335.8 万） | 不同步 | 同上 |
| `ads_patent_analysis_topic`（36.5 万，带 run_id） | 不同步 | 分析族产物，版本化口径待久新确认（主文档 §3.1 在问） |
| `ads_emerging_topic_*` | 不同步 | Topic 上的评估结果，不是映射主体 |

## 同步

来源是已有字典通道，不在页面直连久新。

`lumen-topic-py` `POST /internal/gkx-svc/dict/query`，新增 `op=discipline_topic_page`。只读 Doris `ads_discipline_topic`（可附带 subfield/field/domain 三个上级字典，同样分页）。每页最多 500。

Java `gkx-innov` 按页写入本侧表。按 `topic_id` 更新名称和版本，不整表清空，不删已有关联。某一页失败时，已写入的页保留。字典为空则不改表。

## 本侧表

库：现网是 `demo_gkxlumenx_dwd`。

| 表 | 内容 |
|---|---|
| `dwd_discipline_topic` | Topic 字典镜像：`topic_id`、`name_zh`、`name_en`、`subfield_id`、`field_id`、`domain_id`、data_version |
| `dwd_topic_industry_map` | Topic→产业节点映射：一行一个 topic 的一条产业关联 |

`dwd_topic_industry_map` 一行是一个 Topic 的一条产业关联。还没关联时保留一行，`node_id` 为空。

逻辑键：`topic_id` + 本侧产业节点 `node_id`（再加集群，一个产业节点可挂多个集群）。

不写入 `subfield_topic_map`，不写入 `dwd_tech_node_industry_map`。三张映射表各管各的维度（子学科/技术节点/Topic），互不覆盖。

## 关联

与 tech-node-map 同构：人点击【关联】才做向量匹配。一次请求只处理 20 个尚未关联的 topic。页面点一次按批自动请求，直到未映射为 0；某一批失败或剩余数不再下降就停下。每个 Topic 用 `name_zh`（空则 `name_en`）名称向量，与本批候选产业节点的向量做余弦，只留最近的一条。

调用：`demo-ui-system-test` → 网关 `/ops/v1/topic-maps/**` → `gkx-innov` → `lumen-algo-py` `POST /internal/topic-industry/link`。

候选只用本侧已有目录：集群 `CL-*`、产业节点来自 `industry_chain` / `industry_chain_node`。向量只在这批候选里比。

量级提示：4,516 个 topic ÷ 每批 20 = 约 226 批；候选产业节点为 `industry_chain_node` 全量（1,220）时单批向量计算可控，但整表跑完需要一段时间，页面按批循环与 tech-node-map 相同。

## 页面

与 tech-node-map 同构：已映射 / 未映射全表数量；Topic 合成一张表，按「是否已映射」区分，已映射行显示产业节点名称；已映射、未映射各最多 200 行；关键字查询最多 200 个 topic，留空只看已关联。另给已映射产业及其 topic 数量；选定产业后只列该产业上已映射的 topic 及数量；选定产业节点后列出已关联的 topic，不触发同步或模型。

## 消费闭环（为什么做这张表）

Topic 桥（[Topic桥可行性判定.md](./调研/Topic桥可行性判定.md)）：链节点 →(subfield_topic_map)→ subfield →(本表关联)→ topic →(久新 *_topic 表)→ 人才/机构/论文/专利/项目。本叶落地后，「subfield → topic」从字典从属关系（一跳 18 个 topic 的粗粒度）升级为**显式产业节点关联**，人才/机构/成果即可按链节点精确过滤。消费方（展示态势、专题产业链）后续读本侧表，不直连久新。
