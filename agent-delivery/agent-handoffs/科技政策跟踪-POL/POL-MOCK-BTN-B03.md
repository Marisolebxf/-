# POL-MOCK-BTN-B03 · 评价按钮灌数

> 2026-11-09。只换评价页的写入函数。推演及以后的页仍是空实现。未改任务状态。未开始 B04。

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
| 说明 | 与派单强度一致。未用 YAGNI 跳过 D16：缺项只进 `gkxlumenx_gapfill`，写前 `assert_demo_mysql_targets`。223 短板、223 焦点、226 摘要不建缺项表，演示 MySQL 上先校验再调已有 `run()`。221 不建表，231 不灌导出文件。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无 |
| 图 diff | 本单不改图 |
| 会签态 | 无 |
| 说明 | 未改存储流图或接口图 |

## 修改内容

`register_page("evaluation", write_evaluation)` 换掉评价页的 `_zero`。`write_evaluation(ctx)` 返回 `{序号: {written, sample, method}}`。`conn` 为空时返回空字典，回执仍是 0 行。

幂等走已有 `upsert_button_rows`：`DELETE ... WHERE gapfill_batch_id=%s`，参数 `BTN-evaluation`，再 `INSERT ... ON DUPLICATE KEY UPDATE`。不 `TRUNCATE`，不整表 `DELETE`。不写 `BTN-panorama`，不写 `gapfill_policy_sim_forecast`，不碰 DS12 的 `SYNTH-` 行，不清 `gapfill_policy_audience_feedback` 与 `gapfill_policy_assessment_report`。

219 写 `gapfill_policy_eval_trend`，220 写 `gapfill_policy_eval_partition`，222 写 `gapfill_policy_eval_template`，224 与 225 合写一次 `gapfill_policy_eval_shell`，227–230 合写一次 `gapfill_policy_eval_scheme`。同一张表只 upsert 一次，避免后一次删除把前一次的 `BTN-evaluation` 行清掉。

221 回执 `written=0`、样例空。231 同样。不建 `gapfill_policy_eval_focus`，不建 `gapfill_policy_eval_summary`。

223 短板调 `polan.eval.gap.run`，只重算 `demo_gkxlumenx_ads.policy_effect` 里 `scope_type=region_gap` 的行。焦点调 `polan.eval.focus.run`，写 `policy_focus`。226 调 `polan.text.parse.run`，写 `policy_text_parse`。这三处只在 `backend=mysql` 时执行，且先 `assert_demo_mysql_targets`。自检注入空跑替身，不连库。没有调用 `effect.run`，全景用的 `region_effect` 行不动。

229 路径行的 `metric_id` 只有已有的 `M_POLICY_DS_11_POLICY_EVAL_015`。其它评价缺项行不写 `metric_id`。

无密钥时正文用模板句，生成方式写「模板句」，不报错。样例经 `clip_sample`，不超过 60 字。

`seed_gapfill_policy_eval_viz.py`、`template.py`、`shell.py`、`scheme.py` 的 `--apply` 改为调用 `apply_from_seed()`，不再执行整表 `DELETE` 或 `DROP TABLE`。`--check` 仍校验行形状，生成的 SQL 里没有 `DELETE FROM`、`DROP TABLE`、`TRUNCATE`。

## 自检行数（假游标，未连演示库）

| 序号 | 本次写入行数 | 样例 |
|------|--------------|------|
| 219 | 44 | 按时间看，科技政策连续出台数在2026年记为91，高于2021年的48。 |
| 220 | 41 | 广东省在财政资金上的对照值高于同组其它地区。 |
| 221 | 0 | （空） |
| 222 | 10 | 科技政策月度动态报告按月度、时间和趋势图选用。 |
| 223 | 7 | 广东省的区域短板与政策焦点已按既有口径重算。 |
| 224 | 4 | 政策实施强度连续三年上行，适用行业范围持续扩大。 |
| 225 | 3 | 以一页图解说明加计扣除比例、适用行业与申报流程要点。 |
| 226 | 3 | 研发费用加计扣除的适用行业在近三年持续扩大。 |
| 227 | 2 | 以企业研发费用加计扣除扩围和省市联动补助为核心，三年内带动规上工业企业研发投入强度提升。 |
| 228 | 5 | 前两年投入快速爬坡，第三年随退坡政策接续，增速小幅回落。 |
| 229 | 6 | 部分县域企业信息渠道有限，需依托科技特派员和行业协会下沉宣讲。 |
| 230 | 6 | 方案对研发投入的拉动测算偏乐观，建议对照近三年同类政策实际兑现率再校一版弹性系数。 |
| 231 | 0 | （空） |

223 的 7 是假游标对短板 `COUNT` 返回 2、焦点 `COUNT` 返回 5 的和。226 的 3 是假游标对 `policy_text_parse` 的 `COUNT` 返回值。用来证明回执能带上行数，不是演示库落库行数。

229 的 `metric_id` 只有 `M_POLICY_DS_11_POLICY_EVAL_015`，插入参数里出现 6 次，与 6 条路径行一一对应。其它插入语句不带 `metric_id` 列。

## 演示库行数

库名：`demo_gkxlumenx_ods` / `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads`，外加缺项库 `gkxlumenx_gapfill`。`assert_demo_mysql_targets` 通过后跑了一次 `run("evaluation")`。生成方式为「模板句」。回执本次写入合计 40490 行。

| 序号 | 本次写入行数 | 表内总行数 | 样例 |
|------|--------------|------------|------|
| 219 | 44 | 44 | 按时间看，科技政策连续出台数在2026年记为91，高于2021年的48。 |
| 220 | 41 | 41 | 广东省在财政资金上的对照值高于同组其它地区。 |
| 221 | 0 | 0 | （空） |
| 222 | 10 | 10 | 科技政策月度动态报告按月度、时间和趋势图选用。 |
| 223 | 20200 | 20355 | 北京市的区域短板与政策焦点已按既有口径重算。 |
| 224 | 4 | 14 | 政策实施强度连续三年上行，适用行业范围持续扩大。 |
| 225 | 3 | 14 | 以一页图解说明加计扣除比例、适用行业与申报流程要点。 |
| 226 | 20169 | 20169 | 工信厅消费函〔2020〕279号各省、自治区、直辖市及计划单列市、新疆生产建设兵团工业和信息化主管部门:为贯彻落实《关于 |
| 227 | 2 | 38 | 以企业研发费用加计扣除扩围和省市联动补助为核心，三年内带动规上工业企业研发投入强度提升。 |
| 228 | 5 | 38 | 前两年投入快速爬坡，第三年随退坡政策接续，增速小幅回落。 |
| 229 | 6 | 38 | 部分县域企业信息渠道有限，需依托科技特派员和行业协会下沉宣讲。 |
| 230 | 6 | 38 | 方案对研发投入的拉动测算偏乐观，建议对照近三年同类政策实际兑现率再校一版弹性系数。 |
| 231 | 0 | 0 | （空） |

223 的 20200 = 区域短板 31 + 焦点（`policy_id` 非空）20169。表内总行数 20355 = `policy_effect` 全表 155 + `policy_focus` 全表 20200。`policy_effect` 里 `region_effect`、`region_layout`、`ds_guide`、`ds_guard` 仍各 31 行，本单没有重算它们。`policy_focus` 另有 31 行 `policy_id` 为空，`focus.run` 的既有删除条件不包括这些行。

226 的样例是解析 `run()` 写进 `policy_text_parse.summary` 的第一句，回执截到 60 字。

演示库上 `BTN-evaluation` 的方案行：路径与风险 6 行的 `metric_id` 都是 `M_POLICY_DS_11_POLICY_EVAL_015`，方案对照、参数模拟、互动意见的 `metric_id` 为空。旧批次 `POL-L2-DS11-PLAN-GAPFILL-L01` 的路径行也是这一个指标，本单没有新造指标。

趋势、分区、模板三张表有唯一键，旧种子行被本批键吸成 `BTN-evaluation`，所以表内总行数等于本次写入。解读壳和方案表没有业务唯一键，旧批次各留 7 行和 19 行，与本批并存。受众反馈仍是 591 行，评估报告仍是 2 行。

## 测试结果

两仓都执行 `python -m polan.mockgen.btn`，退出码 0。不连库。

```
panorama_writer 197=18 198=18 199=9 200=3 205=12 206=5 209=4 210=6 211=2 212=4 213=3 214=3 215=6 216=4 217=6 218=4
panorama_sample_199 《北京市产业园区扶持意见》在相关性排序中位于第1名。
evaluation_writer 219=44 220=41 221=0 222=10 223=7 224=4 225=3 226=3 227=2 228=5 229=6 230=6 231=0
evaluation_sample_229 部分县域企业信息渠道有限，需依托科技特派员和行业协会下沉宣讲。
evaluation_metric_229 M_POLICY_DS_11_POLICY_EVAL_015
btn self_check ok pages=7 written=0 method_fallback=模板句 upsert=BTN-batch
sample_199 {'序号': '199', '叶名': '检索结果智能排序', '表': 'gapfill_policy_qry_rank', '本次写入行数': 0, '表内总行数': 0, '样例': '', '读取页面与接口': '全景 GET /display/v1/policy/panorama/rank', '生成方式': '模板句'}
```

`written=0` 那一行是不连库的 `run("panorama")`。评价页在 `conn is None` 时同样返回空字典，回执样例保持空字符串。

假游标断言：返回序号集合为 219–231；221 与 231 的写入为 0、样例为空；其余样例非空、不超过 60 字、不含 TODO/TBD/xxx/待补充/测试数据/N/A/null，也不含 `region_gap` 和路径指标号；每条 `DELETE` 的条件带 `gapfill_batch_id` 且参数为 `BTN-evaluation`；无 `TRUNCATE`；不出现全景批次、仿真表、受众表、评估表、`gapfill_policy_eval_focus`、`gapfill_policy_eval_summary`；调用顺序是 `assert` → `gap` → `focus` → `parse`；短板计数条件是 `region_gap`。

四个种子 `--check` 退出码 0。生成的 SQL 无 `DELETE FROM`、`DROP TABLE`、`TRUNCATE`。

两仓 SHA256：

- `btn.py`：`CE8D9A71980A870D9D1AE9D2854337CB88685695661F67CEEDD673003C482CE2`
- `evaluation.py`：`DC8F0664D7717B480E40F9BE9FEDD407C6BAE5F243E5DF291032E467EEE90D48`

## 遗留风险

- 解读壳和方案表没有业务唯一键。本批追加在旧种子批次旁边，读口按时间倒序时会先看到本批。
- 趋势、分区、模板的唯一键冲突时，`ON DUPLICATE KEY UPDATE` 会把同一键的旧行改成 `BTN-evaluation`。
- `focus.run` 按既有实现删除 `policy_id` 非空的焦点行再写入。`policy_id` 为空的 31 行还在。
- `parse.run` 按既有实现清空演示库 `policy_text_parse` 再写入。这次写入了 20169 行。没有动正式库。
- `gap.run` 只删 `scope_type=region_gap`。其它 `policy_effect` 范围未改。
- 单飞仍只在本进程内。
- 未开始 B04。

## CI/CD（必填）

- 分支：`dev` → `origin/dev`
- demo-algo-ent-analysis：`fbc67e6f9a28c2e18b1e6e59722bbb0d576777f6`
- lumen-algo-py：`b4fff0289ffd45417d1ee117be91a728f1a09ceb`（含本单 `91745bd`，推送前与远端 merge）
- gkx-orchestration：本 handoff 这一次提交。推送后以 `git log -1` 为准
- pipeline：提交后由远端 CI 触发，此处未抄运行结果
- 部署：无新缺项表。镜像随两仓 dev 流水线发布后，按钮代码才在运行中的服务里
- K8s rollout：未在本单核对

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | 符合。只加评价灌数 |
| 调用链不越层 | 符合。未改 Java / 前端 |
| 图谱 | 符合。未写图 |
| D16 缺项只进 `gapfill_` | 符合。upsert 仍拒绝非 `gapfill_` 表。223/226 只调已有 ADS `run()` |
| 不写 ODS、正式 DWD、供应方库 | 符合。本次连接的是 `demo_gkxlumenx_*`。ADS 写入发生在这三张已有演示表 |
| 不新造 `metric_id` | 符合。路径行只用 `M_POLICY_DS_11_POLICY_EVAL_015` |
| D18 接口不返回写死 mock | 符合。不连库时样例是空字符串；连上后样例来自本批句子或已有解析摘要 |
| D12 | 符合。lumen 侧是 vendor 字节副本 |
| 可观测 | 沿用按钮框架的失败日志。未加新 span |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 260000（估算，含本会话上下文，非控制台精确值） |
| model_used | `grok-4.7` |
| actual_cost | 1.30（按算法工程化量级估算，美元） |
| cost_warn | `green` |

## 涉及文件

- `repos/demo-algo-ent-analysis/polan/mockgen/evaluation.py`（新建）
- `repos/demo-algo-ent-analysis/polan/mockgen/btn.py`
- `repos/lumen-algo-py/vendor/entan-py/polan/mockgen/evaluation.py`（字节一致副本）
- `repos/lumen-algo-py/vendor/entan-py/polan/mockgen/btn.py`（字节一致副本）
- `repos/lumen-algo-py/scripts/seed_gapfill_policy_eval_viz.py`
- `repos/lumen-algo-py/scripts/seed_gapfill_policy_eval_template.py`
- `repos/lumen-algo-py/scripts/seed_gapfill_policy_eval_shell.py`
- `repos/lumen-algo-py/scripts/seed_gapfill_policy_eval_scheme.py`
- 上述四份脚本对应的 `scripts/mysql/gapfill_policy_eval_*.sql`（去掉整表 `DELETE` / `DROP`）
- 本 handoff

## 未完成

- 未改任务状态。
- B04 及以后的页未开始。
