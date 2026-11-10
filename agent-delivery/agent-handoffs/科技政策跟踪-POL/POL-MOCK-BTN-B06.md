# POL-MOCK-BTN-B06 · 对比按钮灌数

> 2026-11-09。只换对比页的写入函数。研报页仍是空实现。未改任务状态。未开始 B07。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 开工时已是 in_progress。本单不调 task-registry，不改状态。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单强度一致。未用 YAGNI 跳过 D16：缺项只进 `gkxlumenx_gapfill`，写前 `assert_demo_mysql_targets`。612 不建表、不灌。610、611、613 不写 `metric_id`，不新造指标。对照数只读全景已有主题件数，不在本按钮重算分布。不改全景、评价、推演、治理、拆解写入函数的行为。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无 |
| 图 diff | 本单不改图 |
| 会签态 | 无 |
| 说明 | 未改存储流图或接口图 |

## 修改内容

`register_page("compare", write_compare)` 换掉对比页的 `_zero`。`conn` 为空时返回空字典，回执仍是 0 行。

幂等走已有 `upsert_button_rows`：`DELETE ... WHERE gapfill_batch_id=%s`，参数 `BTN-compare`，再 `INSERT ... ON DUPLICATE KEY UPDATE`。不 `TRUNCATE`，不带批次的 `DELETE` 没有。不写 `BTN-panorama`、`BTN-evaluation`、`BTN-simulation`、`BTN-governance`、`BTN-parse`，不碰 `gapfill_policy_sim_forecast` 里 DS12 的 `SYNTH-SIM`。

对比页回执序号是 610、611、612、613。612 的表名是「不建表」，写入函数固定返回 0 行、样例空串，不建表、不插配置行。

610 写入 `gapfill_policy_xcmp`。一对政策四种关系各一行。关系只用中文：共性、差异、互补、冲突。`policy_id_a` 取字典序较小的键。键和标题只来自本次查询的 `policy_base_info`。

611 写入 `gapfill_policy_xcmp_viz`。图种只用中文：对比表、柱、雷达。对照项和 `compare_value` 来自已有 `gapfill_policy_theme_dist` 的 `theme_name`、`item_count`，查询没有 `GROUP BY`、没有 `COUNT`。同一对照数在三种图里各放一行。

613 写入 `gapfill_policy_xcmp_summary`。种类只用中文：对比摘要、核心结论。正文在行里。不产 PDF、Word，不写文件。

无密钥时正文用模板句，生成方式写「模板句」，不报错。样例经 `clip_sample`，不超过 60 字。回执「本次写入行数」是本按钮这次插入或更新的行，不是表内 `COUNT(*)`。

一次只对照字典序最小的两条政策。全景、评价、推演、治理、拆解的写入函数未改行为。

## 自检行数（假游标，未连演示库）

| 序号 | 本次写入行数 | 样例 |
|------|--------------|------|
| 610 | 4 | 《广东省科技型中小企业研发环境支持》与《深圳市外国人来华工作许可》都写明了支持对象和办理要求，可以放在一起看。 |
| 611 | 6 | 假游标给了 2 个主题，三种图各写一遍。样例在自检里断言非空且不超过 60 字 |
| 612 | 0 | （空） |
| 613 | 2 | 自检断言非空且不超过 60 字 |

610 的 4 行是 1 对政策 × 四种关系。611 的 6 行是 3 种图 × 2 个假主题（件数 2 和 1，不是按政策现算）。613 的 2 行是对比摘要和核心结论。两条 `policy_id` 来自假游标返回的 `18363390`、`18407696`，写函数源码里没有这两个字面量。

## 演示库行数

库属性 `ods` / `dwd` / `ads` 都以 `demo_` 开头。`assert_demo_mysql_targets` 通过后跑了一次 `run("compare")`。缺项写入 `gkxlumenx_gapfill`。生成方式为「模板句」。本次合计写入 21 行。

| 序号 | 本次写入行数 | 表内总行数 | 样例 |
|------|--------------|------------|------|
| 610 | 4 | 4 | 《工业和信息化部办公厅关于印发重点跟踪培育纺织服装品牌企业名单（2020版）的通知》与《六部门关于印发《蚕桑丝绸产业高质 |
| 611 | 15 | 15 | 研发费用加计扣除在全景统计里记为12，供这两份政策对照。 |
| 612 | 0 | 0 | （空） |
| 613 | 2 | 2 | 《工业和信息化部办公厅关于印发重点跟踪培育纺织服装品牌企业名单（2020版）的通知》与《六部门关于印发《蚕桑丝绸产业高质 |

政策键是 `18318860`、`18318861`。`policy_id_a` 是 `18318860`。标题与 `policy_base_info` 一致。表内这条互补关系的正文是：

《工业和信息化部办公厅关于印发重点跟踪培育纺织服装品牌企业名单（2020版）的通知》与《六部门关于印发《蚕桑丝绸产业高质量发展行动计划(2021-2025年)》的通知》可以配合，一份补上另一份没有写明的办理环节。

回执样例按 60 字截断，所以 610 和 613 的回执停在「高质」。表内正文是完整句。

关系各 1 行：共性、差异、互补、冲突。图种各 5 行：对比表、柱、雷达。摘要各 1 行：对比摘要、核心结论。对照数与全景主题件数一致：研发费用加计扣除 12、高层次人才安居 8、创业投资引导 6、中试平台建设 4、概念验证支持 3。三张表本批 `metric_id` 有值的行数都是 0。

写前写后没变：`gapfill_policy_sim_forecast` 里 `SYNTH-SIM` 仍 1 行，`BTN-simulation` 仍 4 行，`POL-L2-DS12-DEMO-EXTRA` 仍 15 行，`POL-L2-DS12-EST-GAPFILL-L01` 仍 4 行。`gapfill_policy_eval_trend` 的 `BTN-evaluation` 仍 44 行。`gapfill_policy_lineage_index` 的 `BTN-governance` 仍 4 行。`gapfill_policy_semantic` 的 `BTN-parse` 仍 8 行。`gapfill_policy_qry_stat` 的 `BTN-panorama` 仍 0 行。

## 测试结果

两仓都执行 `python -m polan.mockgen.btn`，退出码 0。不连库。输出相同，下面是 lumen 这份：

```
panorama_writer 197=18 198=18 199=9 200=3 205=12 206=5 209=4 210=6 211=2 212=4 213=3 214=3 215=6 216=4 217=6 218=4
panorama_sample_199 《北京市产业园区扶持意见》在相关性排序中位于第1名。
evaluation_writer 219=44 220=41 221=0 222=10 223=7 224=4 225=3 226=3 227=2 228=5 229=6 230=6 231=0
evaluation_sample_229 部分县域企业信息渠道有限，需依托科技特派员和行业协会下沉宣讲。
evaluation_metric_229 M_POLICY_DS_11_POLICY_EVAL_015
simulation_writer 232=1 233=2 234=2 235=4 236=3 237=0 238=4 239=3 240=0 241=5 242=4
simulation_sample_232 经济效益预测值约74亿元，相对基线变化率约4.2%。AI推演结果，仅供参考。
simulation_metric_232 M_POLICY_SIMULATE
governance_writer 604=4 605=8
governance_sample_604 《广东省科技型中小企业研发环境支持》第一条的结论是符合条件的主体可以按该条款申请支持。
parse_writer 606=8
parse_sample_606 《广东省科技型中小企业研发环境支持》的主旨是明确支持对象，并说明如何申请。
compare_writer 610=4 611=6 612=0 613=2
compare_sample_610 《广东省科技型中小企业研发环境支持》与《深圳市外国人来华工作许可》都写明了支持对象和办理要求，可以放在一起看。
btn self_check ok pages=7 written=0 method_fallback=模板句 upsert=BTN-batch
sample_199 {'序号': '199', '叶名': '检索结果智能排序', '表': 'gapfill_policy_qry_rank', '本次写入行数': 0, '表内总行数': 0, '样例': '', '读取页面与接口': '全景 GET /display/v1/policy/panorama/rank', '生成方式': '模板句'}
```

`written=0` 那一行是不连库的 `run("panorama")`。对比页在 `conn is None` 时同样返回空字典。

假游标断言：返回序号集合为 610、611、612、613；612 写入 0 且样例空；关系四词和图种三词出现在插入参数里；三条 `DELETE` 的参数都是 `BTN-compare`，条件都带 `gapfill_batch_id`；无 `TRUNCATE`；插入语句没有 `metric_id`；主题查询没有 `GROUP BY` 和 `COUNT(`。

两仓 SHA256：

- `btn.py`：`a478049ff07e629d2d0e2070b109ede2c97bf88a7e5828a2d5fd470303af2208`
- `compare.py`：`c765778b4c0be8789d4389cb12aa1149188bf2c087f4688d2694ac41ff83633b`

## 遗留风险

- 只对照字典序最小的两条干净标题。这次取到的是纺织服装品牌名单和蚕桑丝绸计划。要多对政策，把 `_pair` 的上限放开。
- 全景主题表没有行时，611 这次写入是 0。对照项最多 5 个。
- 业务键撞上其它批次时，已有 upsert 会改到那一行。这次三张表的表内总行数等于本次写入行数，库里原先没有这批键。
- 612 在回执里，表名是「不建表」。没有配置保存。
- 单飞仍只在本进程内。
- 未开始 B07。

## CI/CD（必填）

- 分支：`dev` → `origin/dev`
- demo-algo-ent-analysis：`9e6a792c0a7da960dbb756513035e9aa63f46586`（`89ef53b..9e6a792`）
- lumen-algo-py：`0d526257541e02dfba47557dd09e41f0e98240eb`（`76e3c7f..0d52625`）
- gkx-orchestration：本 handoff 这一次提交。推送后以 `git log -1` 为准
- pipeline：提交后由远端 CI 触发，此处未抄运行结果
- 部署：无新缺项表。镜像随两仓 dev 流水线发布后，按钮代码才在运行中的服务里
- K8s rollout：未在本单核对

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | 符合。只加对比灌数 |
| 调用链不越层 | 符合。未改 Java / 前端 |
| 图谱 | 符合。未写图 |
| D16 缺项只进 `gapfill_` | 符合。upsert 仍拒绝非 `gapfill_` 表。612 不建表 |
| 不写 ODS、正式 DWD、ADS、供应方库 | 符合。连接属性以 `demo_` 开头。政策键只读 `policy_base_info`。主题件数只读 `gkxlumenx_gapfill.gapfill_policy_theme_dist` |
| 不新造 `metric_id` | 符合。610、611、613 都不写该列。本批有值行数为 0 |
| D18 接口不返回写死 mock | 符合。不连库时样例是空字符串；连上后样例来自本批句子和已有主题件数 |
| D12 | 符合。lumen 侧 mockgen 是字节副本 |
| 可观测 | 沿用按钮框架的失败日志。未加新 span |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 180000（估算，含本会话上下文，非控制台精确值） |
| model_used | `grok-4.7` |
| actual_cost | 1.00（按算法工程化量级估算，美元） |
| cost_warn | `green` |

## 涉及文件

- `repos/demo-algo-ent-analysis/polan/mockgen/compare.py`（新建）
- `repos/demo-algo-ent-analysis/polan/mockgen/btn.py`
- `repos/lumen-algo-py/vendor/entan-py/polan/mockgen/` 下同两份文件（字节一致）
- 本 handoff

## 未完成

- 未改任务状态。
- B07 及以后的页未开始。
