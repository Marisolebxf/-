# POLICY-DDL-GDF-SYNC-L09 · 政策派单包从 dwd.md/ads.md 复制建表语句

会签通过。签收自检退出码 `0`。

未 ALTER 数据库。未改 `ads.md` / `dwd.md`。未改 `GDF-POLICY-WORKPACK-V2-L01` 的状态（保持 done）。未 git commit / push。未改 task-registry。口令未写入本文件。

## 任务认领

| 字段 | 值 |
|------|-----|
| 任务 | `POLICY-DDL-GDF-SYNC-L09` |
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| status | 开工时已是 `in_progress`。本叶不改 task-registry |
| 说明 | 从现行派单包 `GDF-POLICY-WORKPACK-v2` 原样复制 CREATE。不另写一套，不改库名 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义/文档复制，不写业务代码 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无 |
| 图 diff | 本叶未改存储流图 |
| 会签态 | 不涉及 |

## 复制了哪些表

SQL 块与 `agent-delivery/data/data-design/storage/POLICY/stores/mysql/` 下对应 md 的 ```sql 围栏逐字相同，含注释、库名 `demo_gkxlumenx_*`、缩进。未改成产线库名。

### DWD（`dwd.md` 三块）

| 表 | 派单包文件 |
|----|------------|
| `policy_base_info` | `10-DWD-MySQL-DDL/policy_base_info-MySQL.md`：替换原 CREATE。块外说明仍在。该文件只剩这一块 CREATE |
| `policy_industry_rel` | `10-DWD-MySQL-DDL/policy_industry_rel-MySQL.md`：写入 `dwd.md` 那一块。原先没有 CREATE |
| `policy_text_parse` | 新建 `10-DWD-MySQL-DDL/policy_text_parse-MySQL.md`。一句「从 dwd.md 原样复制。空表，不从 ADS 拷行。」加上 `dwd.md` 那一块 |

`ads.md` 没有 `policy_industry_rel` 的 CREATE。派单包没有另写一份。

### ADS（`ads.md` 15 块，顺序与 md 相同）

新建 `14-ADS-MySQL-DDL/ads-creates.md`。文件头：「从 ads.md 原样复制，库名不改。」

`policy_level_dist`、`policy_type_dist`、`policy_timeseries`、`policy_national_dist`、`policy_sz_dist`、`policy_focus`、`policy_intensity`、`policy_effect`、`policy_metric_timeseries`、`policy_graph_node`、`policy_graph_edge`、`policy_entity`、`policy_text_parse`、`policy_match`、`policy_simulate`。

## 同名表 `policy_text_parse` 哪一块生效

`check_gdf_ddl.py` 的 `collect()` 按排序后的路径收集 ```sql CREATE，同名表只留最后一块。

- 结构真源：`ads.md` 排在 `dwd.md` 前。生效块是 `dwd.md` 的 `demo_gkxlumenx_dwd.policy_text_parse`。库核对打在 `demo_gkxlumenx_dwd` 与 `gkxlumenx_dwd`，输出为「库一致」。
- 派单包：`10-DWD-MySQL-DDL/policy_text_parse-MySQL.md` 先被收集，`14-ADS-MySQL-DDL/ads-creates.md` 后被收集并覆盖。派单包侧留下的是 ADS 那一块（库名 `demo_gkxlumenx_ads`）。
- 两块列、索引、表注释、字符集、排序规则相同，差别只有库名。脚本的 `same()` 不比库名，所以「文件一致 policy_text_parse」。两块都在派单包里。

## 自检

```powershell
python .cursor/skills/gkx-gdf-ddl-signoff/scripts/check_gdf_ddl.py --task GDF-POLICY-WORKPACK-V2-L01
```

- 派单包：`agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2`
- 结构真源：`agent-delivery/data/data-design/storage/POLICY/stores/mysql`
- 退出码：`0`
- 结果：`通过`
- 文件一致 18 张：`policy_base_info`、`policy_effect`、`policy_entity`、`policy_focus`、`policy_graph_edge`、`policy_graph_node`、`policy_industry_rel`、`policy_intensity`、`policy_level_dist`、`policy_match`、`policy_metric_timeseries`、`policy_national_dist`、`policy_simulate`、`policy_sz_dist`、`policy_text_parse`、`policy_timeseries`、`policy_type_dist`
- 库一致：上表各自按 md 最后一块的库名核对 demo 与 lumen。`policy_industry_rel` 与 `policy_text_parse` 的库核对是 DWD 两库。跑完已清除环境变量 `GKX_LUMEN_MYSQL_PASSWORD`

## 架构合规

- D1–D4：未改算法、未改 Java、未改调用链、未改 Nebula、未改可观测埋点。✅
- D5：无代码提交，无 pipeline。✅
- D6 / D12：只读核对 demo 与产线库，没有把 demo 仓 merge 进 lumen，也没有让 lumen 调用 demo 服务。✅
- D8 / D10：未改前端。✅
- D9：未改口径，只把已有 CREATE 原样复制进派单包。✅
- D14：未涉及对象存储。✅
- 未写 ODS / 供应库 `gkx`。未 ALTER、未 DROP。未改 `ads.md` / `dwd.md`。✅
- `GDF-POLICY-WORKPACK-V2-L01` 保持 done。✅
- 口令未写入本文件。✅

## cost

- actual_tokens: 未单列
- model_used: grok-4.7
- actual_cost: 0
- cost_warn: green

## CI/CD

- 分支：`dev`（未提交）
- commit：无
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：`check_gdf_ddl.py --task GDF-POLICY-WORKPACK-V2-L01` 退出码 0

## 可观测性

- 无服务变更，无新 trace。

## 涉及文件

- 改 `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/10-DWD-MySQL-DDL/policy_base_info-MySQL.md`
- 改 `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/10-DWD-MySQL-DDL/policy_industry_rel-MySQL.md`
- 新增 `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/10-DWD-MySQL-DDL/policy_text_parse-MySQL.md`
- 新增 `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/14-ADS-MySQL-DDL/ads-creates.md`
- 新增 `agent-delivery/agent-handoffs/政策模块-E7/POLICY-DDL-GDF-SYNC-L09.md`
- 只读 `ads.md`、`dwd.md`
