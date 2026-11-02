# GDF-SUBFIELD-TOPIC-WORKPACK

两张映射派单里，**先做技术节点产业映射**（`SYSINT-06-20-L01`）。本包（子学科产业关联，`SYSINT-06-19-L01`）排在其后。

子学科和本侧产业节点的两段作业。过程口径跟中台 `SYSINT-TFMAP-02-L01` 相同。不改中台那一页，不在 `demo_gkxlumenx_*` 建表。

本仓没有在 GDF 上建作业，也没有执行建表。执行结果未回，不算可对端。

## 作业

| 作业名 | 命令 | 调度 |
|---|---|---|
| `subfield-topic-sync` | `python scripts/subfield_topic_gdf.py sync` | 每天 T+1 一次，也可以人工触发 |
| `subfield-topic-link` | `python scripts/subfield_topic_gdf.py link` | 只允许人工触发，不要配 cron |
| 核对 | `python scripts/subfield_topic_gdf.py stats` 或 `sql/stats.sql` | 不进作业。只读，不触发同步或模型 |

关键字核对：`python scripts/subfield_topic_gdf.py query --keyword 关键字`。空关键字只列出已有关联的子学科。

自检不连库：`python scripts/subfield_topic_gdf.py --self-check`。

## 表

产线表 `gkxlumenx_dim.subfield_topic_map`。语句在 `sql/subfield_topic_map.sql`。脚本发现表不存在就退出 4，自己不建表。

中台已经在 `demo_gkxlumenx_dim.subfield_topic_map` 落过数。脚本拒绝 `DIM_SCHEMA` 以 `demo_` 开头。

## 环境变量

值不要写进 git。

| 变量 | 作用 |
|---|---|
| `MYSQL_HOST` `MYSQL_PORT` `MYSQL_USER` `MYSQL_PASSWORD` | 本侧 MySQL |
| `DIM_SCHEMA` | 默认 `gkxlumenx_dim` |
| `DWD_SCHEMA` | 默认 `gkxlumenx_dwd` |
| `MAP_TABLE` | 默认 `subfield_topic_map` |
| `SUBFIELD_CATALOG` | 本侧目录，形如 `库.表`，列 `subfield_id`、`name_zh`、`data_version`。不配置则 sync 退出 3 |
| `LLM_API_KEY` | 关联才需要。没有密钥不写假关联 |
| `LLM_BASE_URL` | 默认 `https://open.bigmodel.cn/api/paas/v4`，脚本自己补 `/chat/completions` |
| `LLM_MODEL` | 默认 `glm-5.3-flash` |

依赖：Python 3.9+，作业机自备 `pymysql`。自检不需要它。

## 行为

同步按 `subfield_id` 改名称、版本和同步时间。新 id 插入一行空关联。不整表清空，不删已经有的关联。目录为空则不写表。

关联只处理还没有任何产业节点的子学科。候选是 `CL-*` 集群、挂在这些集群上的产业，以及这些产业下未删除的链节点。模型返回的节点不在候选里就丢掉，该子学科保持未映射。某一批调用失败就停下，后面的子学科不标成已映射。

已映射 = 至少一条非空 `node_id`。未映射 = 已同步但没有这样的行。

## 退出码

| 码 | 含义 |
|---|---|
| 0 | 本趟完成 |
| 1 | 失败，已回滚本趟未提交的写入 |
| 3 | 缺环境，或试图写 demo 库 |
| 4 | 映射表还没建 |
