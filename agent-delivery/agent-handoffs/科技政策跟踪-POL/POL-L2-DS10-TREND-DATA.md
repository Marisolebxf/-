ponytail: off

# POL-L2-DS10-TREND-DATA · 科创政策全景政策动向数据落点

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 沿用已认领记录。本单不再认领 |
| 说明 | 定义单。只定列。不建表，不灌数，不跑数据库，不标 done |

## Ponytail

ponytail: off

定义任务，定列，不缩文档。未用 YAGNI 跳过 D16 行上必有列、四张缺项表的列清单，以及 203、204、205 趋势、206 时间与地域的只读边界。

## 范围与实现

科创政策全景 · 二级「政策动向跟踪」。SRS 序号 203–206，用户故事 `US-DS-POL-02`。数据落点写在 `sdd/l2/POL-L2-DS10-TREND-DATA.md`。依据已签收的 `POL-L2-DS10-TREND-ARCH` 第 7.3 节、说明书第 11.1 节动向一行、`data-lineage-policy.md` §2.4。本单不改架构稿。

库只允许 `gkxlumenx_gapfill`。四张表不进 ODS、DWD、ADS，不写供应方库。`metric_id` 留空，不新注册。`fill_method` 固定 `manual`。不设、不填 `fill_model`。D4 保持 mock。

本单不灌数。灌数单是 `POL-L2-DS10-TREND-GAPFILL-L01`，仍是 backlog。本单不认领、不执行。

### 不建表的叶子

- 203：第 6 项已有入库列表，本单不新开表。不加字段。派单包和 `ads.md` 没有另点名来源监控入库表，本单不编造 ADS 表名。详情仍走已有 detail。
- 204：不落展示库，不建缺项表，不灌假订阅。展示只委托 `gkxlumen-topic-policy`。不认领 `E-E7-POLICY-M1-L11` / `L12` / `L13`。
- 205 趋势、206 时间轴和趋势：读已有 `gkxlumenx_ads.policy_timeseries`（`M_POLICY_TIMESERIES`）。时序源表架构已写 `dwd_policy_base`。不加表，不加字段，不往 ADS 写 mock，不灌进 `gapfill_policy_qry_stat`。
- 206 地域热力：读 `M_POLICY_NATIONAL_DIST` 所在表 `gkxlumenx_ads.policy_national_dist`。不加表，不加字段，不往 ADS 写 mock。

无行则对应图或列表空，不造 0。

### 四张表的列清单

D16 列四表相同：`metric_id`（留空）、`gap_item`（序号和叶子名）、`fill_method`（固定 `manual`）、`gapfill_batch_id`、`generated_at`。不设 `fill_model`。

| 表 | `gap_item` | 业务列 |
|---|---|---|
| `gapfill_policy_trend_hotspot` | `205 热点识别` | `domain_name` 领域名，`hotspot_name` 热点名称，`brief` 一句说明。不放热度分 |
| `gapfill_policy_trend_impact` | `205 政策影响评估` | `domain_name` 领域名，`impact_object` 影响对象，`impact_direction` 影响方向，`conclusion` 一句结论。不放实施效果分和推演情景 |
| `gapfill_policy_trend_report` | `205 深度分析报告` | `title` 标题，`domain_name` 领域名，`body` 正文。正文在行里。不放文件路径，不写对象存储 |
| `gapfill_policy_theme_dist` | `206 主题分布` | `theme_name` 主题名，`item_count` 件数，`stat_year` 年份可空。不借用政策类型分布 |

类型与空值见数据落点第 5 节。本单不写 DDL。灌数单若要主键，只加与业务无关的自增行号。

热点表：科创发展、人才引进、资金扶持各若干条，由灌数单写入。影响表、报告表：三个领域各一条 / 各一份，由灌数单写入。主题表：若干主题名和件数，年份可空，由灌数单写入。本单一行都不写。

## 偏离

无实现偏离。列与架构第 7.3 节、说明书第 11.1 节动向一行一致。`fill_model` 不设列：方法固定 `manual`，§2.4 只在方法为 `llm` 时必填模型名。

203 不新开表。已有 GDF 派单包和 `ads.md` 未点名单独的来源监控入库表名，故写「第 6 项已有入库列表，本单不新开表」，不编造 ADS 表名。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-TREND-DATA.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS10-TREND-DATA.md`（本 handoff）

未改代码仓，未改 `task-registry.yaml`，未调用 task-registry 写工具，未 commit，未 push。未建表，未灌数，未跑数据库。

## 验收证据

- 四张表名、要灌内容和灌数单号与架构第 7.3 节、说明书第 11.1 节动向一行一致。
- D16 列覆盖 §2.4 在本单适用的五项。`metric_id` 留空。`fill_method` 固定 `manual`。不设 `fill_model`。
- 时序结果表 `gkxlumenx_ads.policy_timeseries`、地域结果表 `gkxlumenx_ads.policy_national_dist` 与派单包 17、`ads.md` 对照过。源表 `dwd_policy_base` 沿架构第 4.3 节，本单不加列。
- 203 未新开表。204 未建缺项表，未灌假订阅。
- 定义任务。未跑业务 CI，未部署。任务状态不在本单改写，不标 done。

## 架构合规自检

- ✅ 调用链：浏览器只打 `/display/v1/policy/**`。203 走 element 读第 6 项已有入库。204 只委托专题门面。热点、影响、深度报告和主题由 element 读缺项表。展示不直连 Python，不直连库。
- ✅ Java 不写算法。热点、影响、深度报告没有模型，不进 Python。mock 行留给灌数单，由 Python 写入缺项表，本单不执行。
- ✅ 不写 nGQL，不读政策子图。
- ✅ D9：不新造 `metric_id`，不改 D4。D4 保持 mock。无行不造 0。
- ✅ D12：不读 demo 库填展示。
- ✅ D14：深度报告正文在 `body`。不写对象存储。
- ✅ D16：缺项表只设计在 `gkxlumenx_gapfill`，表名 `gapfill_` 开头。不进 ODS、DWD、ADS、供应方库。本单不灌数。
- ✅ D18：接口不直接返回写死的 mock。做不到的只走这四张缺项表；203、204、时序和地域不走缺项表。
- ✅ 不新开 GDF，不加已有表字段。不把趋势点写入 ADS。

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | grok-4.7 |
| actual_cost | 0.04 |
| cost_warn | green |

无控制台分项。按定义单习惯估 8000、data-agent 80/20、B 档 `$3/$15` 回填：`8000×0.80×3/1e6 + 8000×0.20×15/1e6 = 0.043`，记 `0.04`。未写入 task-registry。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS10-TREND-ARCH-SEQ` |
| 图 diff | 本数据叶不改图、不加边。读路径沿用架构第 2 节和第 7.3 节 |
| 会签态 | 图源无 frontmatter。本单不另填，不把本单写成已通过 |
| 说明 | 数据落点不替代该图 |

## 问题清单

无。灌数仍等 `POL-L2-DS10-TREND-GAPFILL-L01`，本单不执行。

## 修改内容

- 新增 `sdd/l2/POL-L2-DS10-TREND-DATA.md`
- 新增本 handoff

## 测试结果

定义单。未建表，未灌数，未跑数据库，未跑业务测试。

## 遗留风险

- 四张缺项表还没有行。接口在灌数单完成前读到的是空块。D4 仍是 mock。
- 203 的入库列表没有在已签收文档里点名单独表名。后续实现只读第 6 项已有结果，不能另造 ADS 表。
- `GDF-POLICY-MOCK-GATE-L01` 未解开。时序和地域的正式值仍是 mock。

## CI/CD

- 分支：未提交
- commit：无
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：无
- K8s rollout：未部署
- dev 测试 URL / 命令与结果：定义单，未跑

2026-11-03 human:淮政玮 签收。只定列，灌数仍由 POL-L2-DS10-TREND-GAPFILL-L01 执行。
