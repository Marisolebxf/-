# POL-MOCK-BTN-B07 · 研报按钮灌数

> 2026-11-09。只换研报页的写入函数。未改任务状态。未开始 E01。

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
| 说明 | 与派单强度一致。未用 YAGNI 跳过 D16：缺项只进 `gkxlumenx_gapfill`，写前 `assert_demo_mysql_targets`。618 不建文件表、不写文件、不另插一行。614、615、616、617 不写 `metric_id`，不新造指标。政策键和条款只读演示库 `policy_base_info`。不改全景、评价、推演、治理、拆解、对比写入函数的行为。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无 |
| 图 diff | 本单不改图 |
| 会签态 | 无 |
| 说明 | 未改存储流图或接口图 |

## 修改内容

`register_page("report", write_report)` 换掉研报页的 `_zero`。`conn` 为空时返回空字典，回执仍是 0 行。

幂等走已有 `upsert_button_rows`：`DELETE ... WHERE gapfill_batch_id=%s`，参数 `BTN-report`，再 `INSERT ... ON DUPLICATE KEY UPDATE`。不 `TRUNCATE`，不带批次的 `DELETE` 没有。不写 `BTN-panorama`、`BTN-evaluation`、`BTN-simulation`、`BTN-governance`、`BTN-parse`、`BTN-compare`，不碰 `gapfill_policy_sim_forecast` 里 DS12 的 `SYNTH-SIM`。

研报页回执序号是 614、615、616、617、618。

614 写入 `gapfill_policy_report_analysis`。一政策一面一行。侧面只用中文：实施效果、经济社会、产业影响、趋势。

615 写入 `gapfill_policy_report_insight`。一政策一种洞察一行。种类只用中文：观点、建议、风险、机遇。

616 写入 `gapfill_policy_report_body`。一政策一模块一行。模块名是政策概要、深度分析、落实要点。正文在 `body_text`。

617 写入 `gapfill_policy_report_trace`。业务键是 `policy_id` + `direction_name` + `conclusion_key`。方向只用中文：结论到原文、原文到结论。条款号和 `source_excerpt` 来自 `policy_base_info.content` 里切出的「第X条」，不编条款号。不读、不写 `gapfill_policy_lineage_index`。

618 不调用 upsert，不建文件表，不写 PDF / Word，不另插一行。回执本次写入行数是 0，样例是空串。导出只读 616 已经写入的正文。回执「表」列沿用总表里的 `gapfill_policy_report_body`，所以「表内总行数」等于正文表行数，不是 618 又插了行。

无密钥时正文用模板句，生成方式写「模板句」，不报错。样例经 `clip_sample`，不超过 60 字。回执「本次写入行数」是本按钮这次插入或更新的行，不是表内 `COUNT(*)`。

一次最多两条带条款的政策，正文只看前 8000 字。全景、评价、推演、治理、拆解、对比的写入函数未改行为。不写 `gapfill_policy_benchmark_report`、`gapfill_policy_assessment_report`，不写推演解读。

## 自检行数（假游标，未连演示库）

| 序号 | 本次写入行数 | 样例 |
|------|--------------|------|
| 614 | 8 | 《广东省科技型中小企业研发环境支持》第一条的实施效果，要看该条款写明的支持有没有落到对象身上。 |
| 615 | 8 | 自检断言非空且不超过 60 字 |
| 616 | 6 | 自检断言非空且不超过 60 字 |
| 617 | 4 | 自检断言非空且不超过 60 字 |
| 618 | 0 | （空） |

614 的 8 行是 2 条政策 × 四个侧面。615 的 8 行是 2 条政策 × 四种洞察。616 的 6 行是 2 条政策 × 三个模块。617 的 4 行是 2 条政策 × 两个方向。假游标的两条 `policy_id` 是 `18363390`、`18407696`，摘句是游标返回的正文，写函数源码里没有这两个字面量。

## 演示库行数

库属性 `ods` / `dwd` / `ads` 都是 `demo_gkxlumenx_ods` / `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads`。`assert_demo_mysql_targets` 通过后跑了一次 `run("report")`。缺项写入 `gkxlumenx_gapfill`。生成方式为「模板句」。本次合计写入 26 行。

| 序号 | 本次写入行数 | 表内总行数 | 样例 |
|------|--------------|------------|------|
| 614 | 8 | 8 | 《工业和信息化部关于印发《无线电频率使用率要求及核查管理暂行规定》的通知》第一条的实施效果，要看该条款写明的支持有没有落 |
| 615 | 8 | 8 | 《工业和信息化部关于印发《无线电频率使用率要求及核查管理暂行规定》的通知》第一条说明，支持对象和办理要求以该条款原文为准 |
| 616 | 6 | 6 | 《工业和信息化部关于印发《无线电频率使用率要求及核查管理暂行规定》的通知》第一条写明：为促进无线电频谱资源的有效利用，明 |
| 617 | 4 | 4 | 《工业和信息化部关于印发《无线电频率使用率要求及核查管理暂行规定》的通知》关于第一条的结论，可以回到该条款原文核对。 |
| 618 | 0 | 6 | （空） |

618 的表内总行数 6 是正文表 `gapfill_policy_report_body` 的行数，与 616 相同。618 本次写入行数是 0，样例为空。

政策键是 `18318881`、`18318889`，都在 `demo_gkxlumenx_dwd.policy_base_info`。`18318881` 的标题是「工业和信息化部关于印发《无线电频率使用率要求及核查管理暂行规定》的通知」。该政策 617「结论到原文」的 `conclusion_key` 是「第一条结论」，`source_excerpt` 在正文中的位置是 193：

为促进无线电频谱资源的有效利用，明确各类无线电业务的频率使用率要求及核查方法，根据《中华人民共和国无线电管理条例》《无线电频率使用许可管理办法》等相关要求，制定本规定。

`18318889` 的条款键是「第二十五条结论」。方向两种都有：结论到原文、原文到结论。侧面各 2 行：实施效果、经济社会、产业影响、趋势。洞察各 2 行：观点、建议、风险、机遇。模块各 2 行：政策概要、深度分析、落实要点。四张表本批 `metric_id` 有值的行数都是 0。

表内这条实施效果的完整句（回执按 60 字截断，所以停在「有没有落」）：

《工业和信息化部关于印发《无线电频率使用率要求及核查管理暂行规定》的通知》第一条的实施效果，要看该条款写明的支持有没有落到对象身上。

写前写后没变：`gapfill_policy_sim_forecast` 里 `SYNTH-SIM` 仍 1 行，`BTN-simulation` 仍 4 行，`POL-L2-DS12-DEMO-EXTRA` 仍 15 行，`POL-L2-DS12-EST-GAPFILL-L01` 仍 4 行。`gapfill_policy_eval_trend` 的 `BTN-evaluation` 仍 44 行。`gapfill_policy_lineage_index` 的 `BTN-governance` 仍 4 行。`gapfill_policy_semantic` 的 `BTN-parse` 仍 8 行。`gapfill_policy_qry_stat` 的 `BTN-panorama` 仍 0 行。`gapfill_policy_xcmp` / `gapfill_policy_xcmp_viz` / `gapfill_policy_xcmp_summary` 的 `BTN-compare` 仍是 4 / 15 / 2 行。`gapfill_policy_benchmark_report` 与 `gapfill_policy_assessment_report` 的 `BTN-panorama` 仍是 0 行。

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
report_writer 614=8 615=8 616=6 617=4 618=0
report_sample_614 《广东省科技型中小企业研发环境支持》第一条的实施效果，要看该条款写明的支持有没有落到对象身上。
btn self_check ok pages=7 written=0 method_fallback=模板句 upsert=BTN-batch
sample_199 {'序号': '199', '叶名': '检索结果智能排序', '表': 'gapfill_policy_qry_rank', '本次写入行数': 0, '表内总行数': 0, '样例': '', '读取页面与接口': '全景 GET /display/v1/policy/panorama/rank', '生成方式': '模板句'}
```

`written=0` 那一行是不连库的 `run("panorama")`。研报页在 `conn is None` 时同样返回空字典。

假游标断言：返回序号集合为 614、615、616、617、618；618 写入 0 且样例空；四个侧面、四种洞察、两个方向出现在插入参数里；四条 `DELETE` 的参数都是 `BTN-report`，条件都带 `gapfill_batch_id`；无 `TRUNCATE`；插入语句没有 `metric_id`；写入函数没有 `open(`，也没有 PDF / Word 文件写入。

两仓 SHA256：

- `btn.py`：`d13c97d319c23c9a9ba1f34862e0a77547049c9c953c46a76acdc7750d468182`
- `report.py`：`22afba5f108d4764d8abadd4f2a065af586178c674753b0c5d237a70f7fdf56d`

## 遗留风险

- 一次最多两条政策，只取正文前 8000 字里的第一条「第X条」。这次取到 `18318881` 的第一条和 `18318889` 的第二十五条。要更多政策，把 `_POLICY_CAP` 和 `_CONTENT_CHARS` 放大。
- 前 30 条带「第X条」的政策都切不出条款时，614–617 这次写入是 0。618 仍是 0。
- 业务键撞上其它批次时，已有 upsert 会改到那一行。这次四张表的表内总行数等于本次写入行数，库里原先没有这批键。
- 618 的回执表名是正文表，表内总行数会跟着 616 走。没有导出文件。
- 单飞仍只在本进程内。
- 未开始 E01。

## CI/CD（必填）

- 分支：`dev` → `origin/dev`
- demo-algo-ent-analysis：`da8d8eca30b59c7ff5820fd7a381518d7ec7e466`（`9e6a792..da8d8ec`）
- lumen-algo-py：`8e8c0eef4e497b90a858c3ebd040d04f05a86a68`（`0d52625..8e8c0ee`）
- gkx-orchestration：本 handoff 这一次提交。推送后以 `git log -1` 为准
- pipeline：提交后由远端 CI 触发，此处未抄运行结果
- 部署：无新缺项表。镜像随两仓 dev 流水线发布后，按钮代码才在运行中的服务里
- K8s rollout：未在本单核对

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | 符合。只加研报灌数 |
| 调用链不越层 | 符合。未改 Java / 前端 |
| 图谱 | 符合。未写图 |
| D16 缺项只进 `gapfill_` | 符合。upsert 仍拒绝非 `gapfill_` 表。618 不建表、不写文件 |
| 不写 ODS、正式 DWD、ADS、供应方库 | 符合。连接属性以 `demo_` 开头。政策键和条款只读 `policy_base_info` |
| 不新造 `metric_id` | 符合。614–617 都不写该列。本批有值行数为 0 |
| D18 接口不返回写死 mock | 符合。不连库时样例是空字符串；连上后样例来自本批句子和原文条款 |
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

- `repos/demo-algo-ent-analysis/polan/mockgen/report.py`（新建）
- `repos/demo-algo-ent-analysis/polan/mockgen/btn.py`
- `repos/lumen-algo-py/vendor/entan-py/polan/mockgen/` 下同两份文件（字节一致）
- 本 handoff

## 未完成

- 未改任务状态。
- 未开始 E01。
