# TOPIC-POL-TS-DEMO-ACCEPT-LOOP · 政策时序分析演示实例反复验收

## 任务

| 字段 | 值 |
|---|---|
| 状态 | `ready` |
| 执行 | `qa-agent` |
| 监管人 | `human:淮政玮` |
| 说明 | 2026-11-07 第一轮。建单后不认领。不签完成。 |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `N/A` |
| 说明 | 本轮只读接口，没有改业务代码。 |

## 运行 2026-11-07

- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/政策时序分析-合规演示用例.md`
- 库：没有连库。结果不是全空，结果里也没有 `rank`。按编排计划，这两种情况之外不核对 `demo_gkxlumenx_dwd.policy_base_info`
- 样本满足：否
- 停止：产业主样本通过。技术领域这一行没有可复用的已签发结果。不建子任务
- 令牌：本机没有 `%USERPROFILE%\.gkx\topic-loop-token`。没有造令牌，也没有重新登录。不带 `Authorization` 的探测仍是 HTTP 200、`code=0`，所以没有走 401、424 熔断
- 探测：`POST http://10.50.69.111:30892/api/topicAsync/topic/v1/analysis/tasks/list`，body `user_id=guest`、`analysisType=policy_timeseries`、`status=success`、`page=1`、`size=5`。返回 5 条成功任务
- 样本：5 条里最新一条对得上集成电路、年、三维全开的是 `POLICY-20261106-003`（`industry_vid=chain:INB1303`，`industry_id=INB1303`，`granularity=year`，`timeseries_dims` 为发布时间、效力层级、支持力度）。同条件更早的 `POLICY-20261106-002` 不读。更新的 `POLICY-20261107-003` 是 `chain:INB1309`，不用
- 读取：`GET .../tasks/POLICY-20261106-003/result?user_id=guest`。HTTP 200、`code=0`，任务状态 `success`，类型 `policy_timeseries`。没有新签发，没有 `force=true`
- 结果板：`mode=timeseries_board`。`honesty.source=dwd`，`fabricated=false`，`empty=false`。`industry_vid=chain:INB1303`。`summary` 含「共」和「条政策」。三块趋势各 22 个年份，从最小年到最大年连续，`period` 都是四位年。空年 `publish_count` 为 0，没有写成 null。`window` 只落在高于均值的年份。`headline` 有政策总数、最近一年发布量、环比、连续性。效力层级是「未标注」。支持强度每年都有 `fund`、`tax`、`land`、`talent`、`total`，是整数计数，没命中为 0。`insights` 有「发布高峰」和「发布连续性」。`key_nodes` 有 `title`、`publish_date`、`window`，`channel` 没有空值。没有「技术锚点不可算」，也没有名为「政策密度指数」的字段
- 不把条数、峰值年、连续性百分比或有效占比写成通过线
- 技术领域：这 5 条里没有「无 `industry_vid`、有关联产业码、粒度年、三维全开」的成功任务。`POLICY-20261105-014` 是技术领域形状（`industry_codes` 为 INB1502、INB2505，名称用顿号连接），但粒度是月，不能拿来通过这一行。`POLICY-20261105-013` 的名称是「全部」，没有关联产业码。验收轮不补发
- 覆盖不到的三行不派单：动态政策库、季月分桶、政策密度指数这个名字

### 可演行

| 行 | 结论 |
|---|---|
| 序号 110 · 指定产业 | 对上。复用任务的类型和创建条件与用例一致。未打开页面，未另发「未选产业」或「三维缺一」的创建 |
| 序号 110 · 指定技术领域 | 未核。没有可复用的已签发结果。不建子任务，验收轮不签发 |
| 序号 110 · 权威渠道 | 对上。有节点和渠道。不核条数，也不把渠道拆成两类计数 |
| 序号 111 · 三维与年粒度 | 对上 |
| 序号 111 · 历年发布量 | 对上。有政策，年份跨度被覆盖 |
| 序号 111 · 效力层级 | 对上。允许未标注。结果里没有 `rank`，不查库 |
| 序号 111 · 支持强度趋势 | 对上。全 0 的年份仍算有这块结果 |
| 序号 111 · 演变与关键节点 | 对上 |

### 缺口

没有归入 DATA、QUERY、ALGO 的缺口。不建子任务。

技术领域这一行不写成缺口键。它不是库缺行，也不是这条集成电路结果算错。下一轮仍只读已签发结果；要核这一行，需在验收轮之外先有一条年粒度、关联产业码、无 `industry_vid`、三维全开的成功任务。

## 运行 2026-11-07 第二轮

- 用例：同一份合规演示用例
- 库：没有连库。结果不是全空，结果里也不靠 `rank` 判失败
- 样本满足：是
- 停止：通过
- 签发：本轮按当次口令补发技术领域任务，不带 `force`。`POST /api/topicAsync/topic/v1/analysis/tasks` 返回 HTTP 200、`code=0`，`reused=false`，任务 `POLICY-20261107-021`，状态 `success`
- 条件：页面技术领域「组织行为与人力资源管理」的关联产业是「人工智能」（`INB1309`）。创建体 `scope_kind=industry`，`industry_codes` 为 `INB1309`，`industry_name` 为「人工智能」，`granularity=year`，三维为发布时间、效力层级、支持力度。无 `industry_vid`，无 `tech_fields`
- 结果：`summary` 含「共」和「条政策」，对象是人工智能，不是 `chain:INB1303`。没有「技术锚点不可算」。三块趋势覆盖 2000 到 2025 且年份连续，空年 `publish_count` 为 0。`window` 只在高于均值的年。支持强度四字段都在。`insights` 有「发布高峰」和「发布连续性」。`key_nodes` 有 `title`、`publish_date`、`window`，`channel` 没有空值。条数不跟集成电路那条对死
- 不建子任务。动态库、季月分桶、政策密度指数名义仍不派单。验收单留在 `ready`，不签完成

## 签收 2026-11-07

计划状态行已回写。可演行已对上，本轮没有子任务。验收单改为 `done`。

### 缺口

没有缺口。
