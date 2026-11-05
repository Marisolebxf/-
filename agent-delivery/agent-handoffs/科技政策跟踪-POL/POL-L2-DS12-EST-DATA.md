ponytail: off

# POL-L2-DS12-EST-DATA · 政策效果推演效果预估数据落点

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 登记表已有认领。本单不改认领字段 |
| lock_until | `2026-11-06T14:52:38.762Z` |
| 说明 | 定义单。只写数据落点。列级定义只定粒度和必要列。不建库，不灌数，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过 D9、D16 行级列、调用链和空表返回空。

## 范围

政策效果推演 · 二级「效果预估」。SRS 序号 232–234，用户故事 `US-DS-POL-06`。上游是 `POL-L2-DS12-EST-ARCH` 第 9 节。数据落点写在 `sdd/l2/POL-L2-DS12-EST-DATA.md`。235、236 只留一句交叉，不在本表定列。

| 序号 | 叶子 | 落点 |
|---|---|---|
| 232 | 未出台政策仿真模拟 | 库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_forecast` 的未出台仿真行。按本次提交的参数档拣 |
| 233 | 新出台政策效果预测 | 同一张表的新出台预测行。按 `policy_id` 拣 |
| 234 | 区域经济发展空间模拟 | 同一张表的区域空间行。区域必选，按区域名称拣 |

235 的列归 `POL-L2-DS12-SIM-DATA` 的库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_result`，236 的列归同一单的库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_stakeholder`；读路径见 `POL-L2-DS12-EST-ARCH` §5.4/§5.5，灌数见 `POL-L2-DS12-SIM-GAPFILL-L01`。

## 表与粒度

只一张表：库 `gkxlumenx_gapfill`，表 `gapfill_policy_sim_forecast`。本单只定列，不建库，不灌数。三种 `row_kind`：未出台仿真、新出台预测、区域空间。

未出台仿真一行一组参数档：政策类型、覆盖范围、支持力度、实施时间、经济效益、社会影响、创新促进的预测值与变化率、逐年趋势、一句解释。`gap_item` 为 `232 未出台政策仿真模拟`。`metric_id` 固定 `M_POLICY_SIMULATE`。四类都没提交、或对不上，则该次模拟空。多行由前端并排。服务端不存用户模拟历史。

新出台预测一行挂一条已有政策：短长期效果、经济增长、产业发展、科技创新、时间趋势、空间特征、相似政策依据说明。`gap_item` 为 `233 新出台政策效果预测`。`metric_id` 固定 `M_POLICY_SIMULATE`。`policy_id` 与全景目录同一业务键。无标识则该区空。不灌文本解析行。「新出台」在甲方确认前不按颁布日期截断。

区域空间一行是一个区域名称 × 一个政策类型：GDP 增长、产业结构变化、就业率变化、空间分布。`gap_item` 为 `234 区域经济发展空间模拟`。`metric_id` 固定 `M_POLICY_SIMULATE`。未选区域则空。不造全国兜底行，不灌地图文件。

每行带 `metric_id`、`gap_item`、`fill_method=manual`、`gapfill_batch_id`、`generated_at`，以及 `is_mock=1`。不设 `fill_model`。查询不插入。列清单不是可执行 SQL。空态是空，不写成 501。

本二级不读已有 ADS 来填这三类预测。`ads.policy_simulate` 不复制进本表。`ads.policy_text_parse` 不复制进本表。不写 ODS、DWD、ADS、供应方库。D4 保持 mock。

## 灌数单

只点名，本单不认领，不执行。

| 灌数单 | 点名内容 |
|---|---|
| `POL-L2-DS12-EST-GAPFILL-L01` | 按本单第 2 节，在库 `gkxlumenx_gapfill` 建表 `gapfill_policy_sim_forecast`，灌三种行。不灌文本解析行，不灌 235、236。依赖本单。当前 `backlog` |

该单 DoD 已指向这一张表。本单不改那张任务的注册字段。查询请求不调用这张灌数单。235、236 的灌数见上一节那一句，本单不执行 `POL-L2-DS12-SIM-GAPFILL-L01`。

## 不重开 GDF

不重开 GDF。不写 nGQL。不加 ODS、DWD、ADS 表。不新造 `metric_id`。不把 D4 从 mock 改绿。

## 偏离

无。字段名由架构第 9 节交给本单。库、表、三种种类、`metric_id`、`fill_method`、D4，以及 235、236 不进本表，都与架构第 9 节一致。2026-11-05 架构稿对第 5.4、5.5 节的库.表改写，本单只在交叉句里沿用，不改那份稿。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS12-EST-DATA.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS12-EST-DATA.md`（本 handoff）

未改代码仓，未改 `task-registry.yaml` 手稿，未 commit，未 push。未改架构稿、调研分册、`指标与501.md`、说明书、WBS。未认领 `POL-L2-DS12-EST-GAPFILL-L01`。未建库，未灌数。

## 验收证据

- 232–234 的库表与架构第 9 节一致：只一张，库 `gkxlumenx_gapfill`，表 `gapfill_policy_sim_forecast`，三种种类。
- 三叶 `metric_id` 都是已有 `M_POLICY_SIMULATE`。`fill_method=manual`。D16 列写明。D4 保持 mock。
- 空表或条件对不上时该区为空。不把空态写成 501。不读 `ads.policy_simulate` 填数。不灌文本解析行。
- 235、236 未在本分册写列。交叉句指向架构 §5.4/§5.5 与 `POL-L2-DS12-SIM-GAPFILL-L01`。
- 定义任务，未跑业务 CI，未部署。待会签。不标 done，不标 ready_to_sign。

## 架构合规自检

- ✅ 调用链：`gkxlumen-element` 只读这张表。展示不直连库，不直连 Python。
- ✅ Java 不写算法，不按弹性公式现算，不插入行。
- ✅ 不写 nGQL。
- ✅ D9：不新造 `metric_id`，不改 D4。无行不造数。
- ✅ D14：不写地图文件，不新建桶，不写对象键。
- ✅ D16：只在库 `gkxlumenx_gapfill`。行上带 `metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`。不写 ODS、DWD、ADS、供应方库。
- ✅ D18：mock 先落这张表，再被查询。查询不直接返回 mock。空态是空。
- ✅ 不重开 GDF。

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | grok-4.7 |
| actual_cost | 0.04 |
| cost_warn | green |

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS12-EST-ARCH-SEQ` |
| 图 diff | 本数据叶不改图、不加边。读路径沿用架构第 9 节 |
| 会签态 | `draft`。源文件无 frontmatter，沿架构稿记 draft。不自填绿 |
| 说明 | 数据落点不替代该图。本单待会签 |

## 问题清单

- `POL-L2-DS12-EST-GAPFILL-L01` 仍是 backlog。表尚未建。查询在表出现之前返回空。本单不认领它。
- 架构稿文件头仍写待四角色会签，不标 done。本单按第 9 节定列，不改那份稿。
- 「新出台」口径需规未定义。临时默认写在数据分册第 4 节：按已有 `policy_id` 挂行，查询不按颁布日期截断。本单未改客户决策清单。

## 修改内容

- 新增 `sdd/l2/POL-L2-DS12-EST-DATA.md`
- 新增本 handoff

## 测试结果

- 只读核对架构第 9 节、第 5.1–5.3 节，以及 SIM 架构第 7、9 节的表归属。未跑业务测试，未建库，未灌数。

## 遗留风险

- 灌数单未执行。空表时三叶都返回空。这是当前正确行为。
- 架构稿若在签收时改第 9 节的种类或表名，本分册要跟着改。本单不预先改架构。
- 甲方若另行定义「新出台」或区域名称口径，灌数单改挂哪些行。本分册的列不用先拆开。

## CI/CD

- 分支：未提交
- commit：无
- pipeline URL / ID：无。定义任务，`cicd: skip`
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：未部署。未建库，未灌数

## 可观测性

- OTEL_SERVICE_NAME：本叶不新设计观测点。trace 沿既有展示链
- traceId（dev 抽样）：无。未发请求
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS12-EST-DATA.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS12-EST-DATA.md`
