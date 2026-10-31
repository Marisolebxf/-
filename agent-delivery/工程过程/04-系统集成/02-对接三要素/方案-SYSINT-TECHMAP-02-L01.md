# 方案 · SYSINT-TECHMAP-02-L01

技术路线就是候选技术节点，主键 `technology_node_id`。本方案只定一个菜单。证据表、边、路径、簇群、正式目录都不另开菜单，因为它们不是这条关联的主键。

## 菜单

算法中台 `demo-ui-system-test`，维护管理，与「子学科与专题映射」并列。

| 项 | 值 |
|---|---|
| 菜单名 | 技术节点与产业映射 |
| 路由 | `/ops/tech-node-map` |
| 按钮 | 【同步】【关联】。打开页面、查询都不触发这两步 |

## 可同步与排除

| 久新表 | 行数量级 | 决定 | 原因 |
|---|---:|---|---|
| `ads_technology_profile` | 19,430 | **同步** | 节点主数据。主键 `technology_node_id` |
| `ads_technology_paper` / `patent` / `institution` / `application_case` | 见调研 | 不同步 | 节点证据。关联不靠它们 |
| `ads_technology_graph_edge` / `evolution_edge` | 各 587,252 | 不同步 | 节点和节点的边，不是产业关联主体 |
| `ads_technology_evolution_path_step` | 47,909 | 不同步 | 代表路径，不是节点身份 |
| `ads_technology_community` / `community_member` | 1,731 / 19,430 | 不同步 | 算法簇群。1,708 个是单节点簇 |
| `ads_technology_graph_node` | 19,430 | 不同步 | 与画像同一节点，簇字段不参与产业关联 |
| 热点、潜力、阶段、年度、区域 | 见调研 | 不同步 | 节点上的评估结果，不是第二条技术路线 |
| `ads_technology_commercial_value_simulation` | 8 | 不能当主数据 | 主键是 `tech_id`，且是模拟值 |
| `ads_technology_policy_evidence` | 0 | 还没有 | 0 行不是「没有政策」 |
| 正式 `tech_id` | 空 | 还没有 | `mapping_status=UNMAPPED`，映射表不存在 |
| `M_TECH_INVEST_AMOUNT` | — | 还没有 | 市场、收入、融资未接入 |

中文名当时为空。同步把 `technology_name_zh` 原样写入 `name_zh`，英文放 `name_en`。空中文不抄英文。

## 同步

来源是已有字典通道，不在页面直连久新。

`lumen-topic-py` `POST /internal/gkx-svc/dict/query`，`op=technology_node_page`。只读 Doris `ads_technology_profile`。每页最多 500。

Java `gkx-innov` 按页写入本侧表。按 `technology_node_id` 更新名称和版本，不整表清空，不删已有关联。某一页失败时，已写入的页保留。字典为空则不改表。

## 本侧表

库：现网是 `demo_gkxlumenx_dwd`。demo 写入前会把不带 `demo_` 的 `gkxlumenx_dwd` 改成这个库。专题全景只读这一库，不读 `subfield_topic_map`。

表：`dwd_tech_node_industry_map`。表还不存在或还没有关联行时，全景显示「暂无已发布主流技术路线」，不把子学科名称填进来。

一行是一个技术节点的一条产业关联。还没关联时保留一行，`node_id` 为空。

逻辑键：`technology_node_id` + 本侧产业节点 `node_id`（再加集群，因为一个产业节点可以挂多个集群）。

不写入 `subfield_topic_map`。

## 关联

人点击【关联】才调用模型。一次只处理 20 个尚未关联的节点，避免浏览器和网关超时。剩下的再点一次。

调用：`demo-ui-system-test` → 网关 `/ops/v1/tech-node-maps/**` → `gkx-innov` → `lumen-algo-py` `POST /internal/tech-node-industry/link`。

候选只用来自本侧已有目录：集群 `CL-*`，产业节点来自 `industry_chain` / `industry_chain_node`。模型返回的 `node_id` 不在候选里就丢弃，该技术节点保持未关联。没有候选节点时不调用模型。

Java 不写提示词。前端不直连久新、Python、模型。

## 页面

已映射 / 未映射给出全表数量。列表各最多 200 行。关键字查询最多 200 个技术节点；留空只看已关联。无中文名时展示英文名，列上仍能看出中文为空。
