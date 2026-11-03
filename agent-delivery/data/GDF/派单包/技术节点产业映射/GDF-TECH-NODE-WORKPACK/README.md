# GDF-TECH-NODE-WORKPACK

两张映射派单里，**先做本包**（技术节点产业映射，`SYSINT-06-20-L01`）。子学科产业关联（`SYSINT-06-19-L01`）排在其后。

技术节点和本侧产业节点的两段作业。过程口径跟中台 `SYSINT-TECHMAP-02-L01` 已推送的名称向量最近邻相同。不改中台那一页，不在 `demo_gkxlumenx_*` 建表，不写入 `subfield_topic_map`。产业锚点只认 Milvus 库 `gkxlumen` 的集合 `gkxlumen_industry_anchor`，不读库 `default`，不另建集合。

本仓没有在 GDF 上建作业，也没有执行建表。执行结果未回，不算可对端。

## 作业

| 作业名 | 命令 | 调度 |
|---|---|---|
| `tech-node-industry-sync` | `python scripts/tech_node_industry_gdf.py sync` | 每天 T+1 一次，也可以人工触发 |
| `tech-node-industry-link` | `python scripts/tech_node_industry_gdf.py link` | 只允许人工触发，不要配 cron |
| 核对 | `python scripts/tech_node_industry_gdf.py stats` 或 `sql/stats.sql` | 不进作业。只读，不触发同步或向量 |

关键字核对：`python scripts/tech_node_industry_gdf.py query --keyword 关键字`。空关键字只列出已有关联的技术节点。

自检不连库：`python scripts/tech_node_industry_gdf.py --self-check`。

## 表

产线表 `gkxlumenx_dwd.dwd_tech_node_industry_map`。语句在 `sql/dwd_tech_node_industry_map.sql`。脚本发现表不存在就退出 4，自己不建表。

中台写的是 `demo_gkxlumenx_dwd`。脚本拒绝 `DWD_SCHEMA` 或 `DIM_SCHEMA` 以 `demo_` 开头。

## 同步：从久新拉到本侧表

作业不调用 `lumen-topic-py`。脚本自己用 MySQL 协议只读久新 Doris，和中台字典 `technology_node_page` 读的是同一张表。地址写在 `scripts/tech_node_industry_gdf.py` 顶部，也列在这里。

| 项 | 值 |
|---|---|
| 地址 | `47.93.119.170` |
| 端口 | `29030` |
| 账号 | `test2` |
| 密码 | `m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka`。2026-10-31 用户下令明文写入本文件，供 GDF 独立连库。脚本仍读环境变量 `JX_ADS_PASSWORD`，作业机配成这一串 |
| 库 | `gkx_technology_analysis_dev` |
| 表 | `ads_technology_profile` |
| 约行数 | 1.9 万 |
| 每页 | 500，`ORDER BY technology_node_id LIMIT 偏移, 500` |

读取列：`technology_node_id`、`technology_name_zh`、`technology_name_en`、`data_version`。

写入本侧 `gkxlumenx_dwd.dwd_tech_node_industry_map`：`technology_name_zh` → `name_zh`，`technology_name_en` → `name_en`。中文为空就空着，不抄英文。已有 `technology_node_id` 只更新名称、版本和 `synced_at`。新 id 插入一行，`node_id` 为空。不整表清空，不删已经有的关联。第一页是空的则不改表。某一页失败时，已经提交的页保留。

没有 `JX_ADS_PASSWORD` 时同步退出 3。

## 环境变量

久新只读密码按 2026-10-31 用户例外写在上一节。本侧库口令 `MYSQL_PASSWORD` 仍只放作业机，不写进本文件。

| 变量 | 作用 |
|---|---|
| `JX_ADS_PASSWORD` | 久新 Doris 密码。同步必填。可用 `JX_ADS_HOST` `JX_ADS_PORT` `JX_ADS_USER` `JX_ADS_DATABASE` 覆盖上表默认值 |
| `MYSQL_HOST` `MYSQL_PORT` `MYSQL_USER` `MYSQL_PASSWORD` | 本侧 MySQL，写入映射表 |
| `DWD_SCHEMA` | 默认 `gkxlumenx_dwd`。映射表和产业链节点都在这 |
| `DIM_SCHEMA` | 默认 `gkxlumenx_dim`。集群目录在这 |
| `MAP_TABLE` | 默认 `dwd_tech_node_industry_map` |
| `EMBED_BASE_URL` | 关联才需要。GDF 代理机填 `http://10.50.69.111:30903`。这是 `zhipu-tts` 里 `gkxlumen-embed-tei-nodeport` 的 NodePort，对应容器 8080。脚本自己补 `/v1/embeddings`，不要把路径写进这个变量，也不要填集群内短名 `gkxlumen-embed-tei:8080`。没有地址不写假关联。`EMBED_API_KEY` 留空 |
| `EMBED_MODEL` | 默认 `BAAI/bge-base-zh-v1.5` |
| `EMBED_API_KEY` | 可选。有值才加 Bearer |

依赖：Python 3.9+，作业机自备 `pymysql`。自检不需要它。

## 行为

关联只处理还没有任何产业节点的技术节点。候选是 `CL-*` 集群、挂在这些集群上的产业，以及这些产业下未删除的链节点。每个技术节点用名称向量和候选做余弦，只留最近的一条。同分留候选里更靠前的那条。没有候选节点时不调用向量。向量失败就停下，这一批保持未映射，后面的节点不标成已映射。一个产业挂多个集群时，这一条节点按集群各写一行。

产业锚点只有 Milvus 库 `gkxlumen` 里的集合 `gkxlumen_industry_anchor`（前缀 `gkxlumen_industry_`，768 维，COSINE，模型 `BAAI/bge-base-zh-v1.5`）。这个集合由产业链包 `12` 创建。本包不另建集合，不读数据库 `default`。候选链节点与该集合里的锚点是同一批节点。

已映射 = 至少一条非空 `node_id`。未映射 = 已同步但没有这样的行。清单同时给出 `name_zh`、`name_en` 和 `technology_node_id`。中文为空时展示名用英文。

## 退出码

| 码 | 含义 |
|---|---|
| 0 | 本趟完成 |
| 1 | 失败。同步已提交的页保留；关联未完成的节点不标成已映射 |
| 3 | 缺环境，或试图写 demo 库 |
| 4 | 映射表还没建 |
