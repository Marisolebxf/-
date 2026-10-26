# SYSINT-06-03-DDL-L01 · 政策产线库初始化 ODS / DWD / ADS 空表

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 2026-10-26 认领。锁定 4 小时。tech_task，不代替 `SYSINT-06-03-L01` 的执行结果回传。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 派单备注指定 full。只按已冻结 DDL 建空表或补缺索引，不新写加工、不猜 ads.md 其余表的列。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无。本叶不改 POLICY 存储流图 |
| 图 diff | 无 |
| 会签态 | 未改图 |
| 说明 | 不写 ES、不写 Nebula，流图边不变。 |

## 范围与实现

实例 MySQL 8.0.39，`10.50.11.76:3306`。只动 `gkxlumenx_ods` / `gkxlumenx_dwd` / `gkxlumenx_ads`。未建 `gkxlumenx_dws`（`information_schema.SCHEMATA` 无此库）。未写 `demo_gkxlumenx_*`，未写供应库 `gkx`。全部目标表行数为 0，未灌数。

| 库.表 | 动作 | 行数 | 依据 |
|------|------|------|------|
| `gkxlumenx_ods.dwd_policy_base` | 新建空表，35 列，主键 `id` | 0 | `storage/POLICY/sources/ods-ddl.md` |
| `gkxlumenx_ods.dwd_global_policy_base` | 新建空表，35 列，主键 `id` | 0 | 同上 |
| `gkxlumenx_dwd.policy_base_info` | 按 `10/` 新建空表，44 列，唯一键 `(source_plane, policy_id)` | 0 | `10-DWD-MySQL-DDL/policy_base_info-MySQL.md` |
| `gkxlumenx_dwd.policy_industry_rel` | 列已与冻结 DDL 一致；补索引 `idx_policy_industry_rel_code (industry_link_code, is_deleted, policy_id)` | 0 | `policy_industry_rel-MySQL.md` |
| `gkxlumenx_ads.policy_industry_rel` | 同上，只补同一索引，未改列 | 0 | 同一份 DDL |

`ads.md` 其余 15 张已在 `gkxlumenx_ads`，本叶未改结构：`policy_level_dist`、`policy_type_dist`、`policy_timeseries`、`policy_national_dist`、`policy_sz_dist`、`policy_focus`、`policy_intensity`、`policy_effect`、`policy_metric_timeseries`、`policy_graph_node`、`policy_graph_edge`、`policy_entity`、`policy_text_parse`、`policy_match`、`policy_simulate`。

## 偏离

原 `gkxlumenx_dwd.policy_base_info` 是 0 行的 37 列壳（`status`/`publish_year`/`level`/`is_deleted` 为 bigint，`policy_id` 为 longtext，无 `source_plane`）。与派单包 `10/` 对不上，也不能在不改列类型的前提下加到冻结形状。无外键、无触发器。已改名为 `gkxlumenx_dwd.policy_base_info_retired_20261026`（仍 0 行），主名按冻结 DDL 重建。该退休表不是贴源目标，确认无人使用后可删。

`gkxlumenx_ods.policy`（7 列）和 `gkxlumenx_ads.realdata_policy_metrics` 不是本叶清单，未改。

## 产物清单

- 产线库上述空表与两个索引
- 本 handoff
- 无业务仓代码，无 CDC，无 ES，无 Nebula

## 验收证据

2026-10-26 `information_schema` 核对：

- 列数：ODS 两表各 35；DWD `policy_base_info` 44；两张 `policy_industry_rel` 各 7；退休表 37
- 索引：DWD 主表 `PRIMARY(id)`、`uk_policy_plane_id(source_plane,policy_id)`；两张关联表均有 `idx_policy_industry_rel_pid(policy_id,is_deleted)` 与 `idx_policy_industry_rel_code(industry_link_code,is_deleted,policy_id)`
- 抽列：`source_plane varchar(16) NOT NULL`，`policy_id varchar(100) NOT NULL`，`status varchar(20)`，`is_deleted smallint NOT NULL`，`created_time datetime NOT NULL`；ODS `t_id bigint NOT NULL`，国内 `id varchar(100)` 主键，国际 `year text NOT NULL`，`is_history int`
- 六张相关表 `COUNT(*)` 均为 0
- `gkxlumenx_dws` 不存在
- `gkxlumenx_ads` 上列 16 张政策表均在

本仓无业务 pipeline。CI 不适用。

## 测试结果

- 建表语句执行退出码 0
- 建表后立即用 `information_schema` 与 `COUNT(*)` 复核，结果如上

## 遗留风险

- 退休表仍在 `gkxlumenx_dwd`。算法 demo 里仍有按旧列（`ext1`、`level`）读 `policy_base_info` 的语句；那些语句对着产线主表会因列不存在而失败。Java CMS 读的是 `demo_gkxlumenx_dwd`，本叶未动 demo。
- 本叶不是 Wave A/B 跑通，不代替 `SYSINT-06-03-L01`。

## 问题清单

- 无阻塞。退休表是否删除等监管人确认，不挡本叶签收。

## 修改内容

- 产线库 DDL，见上表
- 编排仓只新增本 handoff 与任务登记

## CI/CD（必填）

- 分支：`gkx-orchestration` `dev`
- commit：随本 handoff 提交
- pipeline URL / ID：编排仓无业务 pipeline
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：直连 `10.50.11.76:3306` 做 `information_schema` 核对，未走 K8s

## 可观测性（建议）

- 无新服务进程，无 trace

## 架构合规自检

- ✅ 算法只在 Python：本叶无算法代码
- ✅ 调用链：未改前端 / Java / Python
- ✅ 图谱：未写 Nebula，未写 nGQL
- ✅ 可观测：无新服务，不新增埋点
- ✅ CI/CD：编排仓文档与登记，无业务发布
- ✅ D12：未写 `demo_gkxlumenx_*`，未调用 demo 服务
- ✅ D14：未碰对象存储
- ✅ 数据策略：只建空表，不灌数，不写供应库 `gkx`

## Cost 回填

本会话没有 token 计量接口。下列是会话量级估算，不是账单。

| 字段 | 值 |
|------|-----|
| actual_tokens | 120000 |
| model_used | cursor-grok-4.7 |
| actual_cost | 1.00 |
| cost_warn | green |

## 涉及文件

- `agent-delivery/agent-handoffs/政策模块-E7/SYSINT-06-03-DDL-L01.md`
- 产线库 `gkxlumenx_ods` / `gkxlumenx_dwd` / `gkxlumenx_ads`（不在 git）
