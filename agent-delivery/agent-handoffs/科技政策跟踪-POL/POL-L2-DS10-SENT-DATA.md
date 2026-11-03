ponytail: off

# POL-L2-DS10-SENT-DATA · 科创政策全景政策舆情评估数据落点

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 定义单。只写数据落点。列级定义只定粒度和必要列。不建库，不灌数，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过 D9、D16 行级列、调用链和空表返回空。

## 范围

科创政策全景 · 二级「政策舆情评估」。SRS 序号 207–212，用户故事 `US-DS-POL-03`。上游是已签收的 `POL-L2-DS10-SENT-ARCH` 第 8 节。数据落点写在 `sdd/l2/POL-L2-DS10-SENT-DATA.md`。

| 序号 | 叶子 | 落点 |
|---|---|---|
| 207 | 政策查询与对比 | 与检索叶同一条 `stats` / `search` / `detail`。不另建缺项表 |
| 208 | 区域政策差异性分析 | 不建表。只消费第 7 项已有子图 |
| 209 | 政策实施效果跟踪 | 已有 `policy_effect`、`policy_metric_timeseries` |
| 210 | 政策受众反馈收集 | `gkxlumenx_gapfill.gapfill_policy_audience_feedback` |
| 211 | 政策效果评估报告 | `gkxlumenx_gapfill.gapfill_policy_assessment_report` |
| 212 | 政策匹配与推送 | 已有 `policy_match` |

## 表与粒度

207 不第二套灌数。正式统计与目录有行时，读检索叶已定的 `gkxlumenx_ads` 统计结果和 `gkxlumenx_dwd.policy_base_info`。正式表没有行时，同一条 `stats` / `search` / `detail` 读到 `gkxlumenx_gapfill.gapfill_policy_qry_stat`、`gapfill_policy_qry_doc`。不读 `gapfill_policy_qry_rank`。

208 无表。子图没有结果则该块空。

209 一行区域：`demo_gkxlumenx_ads.policy_effect`，`scope_type=region_effect`。社会维、环境维在该行已有 `ext` 里，带 `is_mock` 与 `QPOL-02`。落地实效另读 `demo_gkxlumenx_ads.policy_metric_timeseries`，且 `metric_id=M_POLICY_IMPLEMENTATION_EFFECT`。不加列。

210 一行一条意见。列：反馈主体、渠道（问卷、在线评价、意见征集）、意见正文、可选评分、关联政策、时间，以及 `is_mock=1` 和 D16 列。`metric_id` 留空。`gap_item` 为 `210 政策受众反馈收集`。`fill_method=manual`。另有 `gapfill_batch_id`、`generated_at`。不灌假问卷。

211 一行一份报告。列：范围、达成度、社会影响、问题、建议、报告正文，以及 `is_mock=1` 和同一组 D16 列。`gap_item` 为 `211 政策效果评估报告`。`metric_id` 留空。不灌对标报告和研报文件，不新建对象存储桶。

212 一行是一个受控主体对一条政策的一条匹配，同一主体内名次至多 8。表 `demo_gkxlumenx_ads.policy_match`，行上 `metric_id` 为已有 `M_POLICY_MATCH`。`M_POLICY_INDUSTRY_FIT` 读同表。不灌假通知、假邮件。

210、211 只写 `gkxlumenx_gapfill`。不写 ODS、DWD、ADS、供应方库。查询请求不灌数。空表返回空。接口不直接返回 mock。D4 保持 mock。

列清单在数据落点正文第 5、6 节。那是列定义，不是可执行 SQL。

## 灌数单

只点名，本单不执行。

| 灌数单 | 点名内容 |
|---|---|
| `POL-L2-DS10-SENT-MOCK-ADS` | 只跑已有 `polan.eval.effect.run`、`polan.text.match.run`。不另建表，不改公式 |
| `POL-L2-DS10-SENT-MOCK-210` | 按本单列定义建表并灌 210。依赖本单 |
| `POL-L2-DS10-SENT-MOCK-211` | 按本单列定义建表并灌 211。依赖本单 |

`POL-L2-DS10-QRY-GAPFILL-L01` 属于检索叶。207 只消费它的两张表，本叶不执行，不第二套灌数。

## 不重开 GDF

不重开 GDF。不写 nGQL。不加已有 ADS 列。不新造 `metric_id`。不把 D4 从 mock 改绿。

## 偏离

无实现偏离。209、212 的库名沿用 `ads.md` 已登记的 `demo_gkxlumenx_ads`，与已有 `run()` 同一张表。本单不把这三张表复制进 `gkxlumenx_ads`。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-SENT-DATA.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS10-SENT-DATA.md`（本 handoff）

未改代码仓，未改 `task-registry.yaml`，未 commit，未 push。未改 WBS、说明书、SENT-ARCH、兄弟分册、GDF 派单包。

## 验收证据

- 207–212 的库表与已签收架构第 8 节、说明书第 11.1 节舆情两行一致。
- 210、211 的 D16 列按本单写明：`metric_id` 留空，`fill_method=manual`，`gap_item` 带序号和叶子名。
- 三张舆情灌数单只出现在点名表，本单没有建库、没有插入、没有调用 `run()`。
- 定义任务，未跑业务 CI，未部署。会签未完成。不标 done。

## 架构合规自检

- ✅ 调用链：207 仍走展示委托专题门面；210、211 由 `gkxlumen-element` 只读缺项表；209、212 读已有 ADS。展示不直连库。
- ✅ Java 不写算法。209、212 不改已有 `run()`。
- ✅ 不写 nGQL。208 只消费已有子图。
- ✅ D9：不新造 `metric_id`，不改 D4。无行不造 0。
- ✅ D14：211 不新建桶，不写对象键。
- ✅ D16：210、211 只在 `gkxlumenx_gapfill`，行上带规定列。不写 ODS、DWD、ADS、供应方库。
- ✅ D18：209、212 不另建表。查询不直接返回 mock。
- ✅ 不重开 GDF。

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 未计 |
| model_used | 未计 |
| actual_cost | 未计 |
| cost_warn | 未计 |

未回写注册表的成本字段。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS10-SENT-ARCH-SEQ` |
| 图 diff | 本数据叶不改图、不加边。读路径沿用架构第 8 节 |
| 会签态 | `draft`。不自填绿 |
| 说明 | 数据落点不替代该图。未会签通过 |

## 修改内容

- 新增 `sdd/l2/POL-L2-DS10-SENT-DATA.md`
- 新增本 handoff
