# POL-MOCK-BTN-B05 · 治理与拆解按钮灌数

> 2026-11-09。只换治理页和拆解页的写入函数。对比页、研报页仍是空实现。未改任务状态。未开始 B06。

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
| 说明 | 与派单强度一致。未用 YAGNI 跳过 D16：缺项只进 `gkxlumenx_gapfill`，写前 `assert_demo_mysql_targets`。602、603、607、608、609 不建表、不灌。605 与 606 不写 `metric_id`，不新造指标。不改全景、评价、推演写入函数的行为。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无 |
| 图 diff | 本单不改图 |
| 会签态 | 无 |
| 说明 | 未改存储流图或接口图 |

## 修改内容

`register_page("governance", write_governance)`、`register_page("parse", write_parse)` 换掉这两页的 `_zero`。`conn` 为空时返回空字典，回执仍是 0 行。

幂等走已有 `upsert_button_rows`：`DELETE ... WHERE gapfill_batch_id=%s`，治理参数 `BTN-governance`，拆解参数 `BTN-parse`，再 `INSERT ... ON DUPLICATE KEY UPDATE`。不 `TRUNCATE`，不带批次的 `DELETE` 没有。不写 `BTN-panorama`、`BTN-evaluation`、`BTN-simulation`，不碰 `gapfill_policy_sim_forecast` 里 DS12 的 `SYNTH-SIM`。

604 写入 `gapfill_policy_lineage_index`。每条政策一行原文条款、一行条款结论，条款号都是「第一条」，结论键是「第一条结论」。`policy_id` 和标题只来自本次查询的 `demo_gkxlumenx_dwd.policy_base_info`，最多 2 条。

605 写入 `gapfill_policy_indicator_lib`。维度只用中文：扶持力度、适用范围、实施时效、申请条件。插入语句不带 `metric_id`。

606 写入 `gapfill_policy_semantic`。侧面只用中文：主旨、适用场景、约束、条款分类。每行带上述真实 `policy_id`。插入语句不带 `metric_id`。

602、603 不在治理页序号集合里，607、608、609 不在拆解页序号集合里。这两页的回执只有 604、605 和 606。那五个序号没有插入，也没有样例。

无密钥时正文用模板句，生成方式写「模板句」，不报错。样例经 `clip_sample`，不超过 60 字。回执「本次写入行数」是本按钮这次插入或更新的行，不是表内 `COUNT(*)`。

`seed_gapfill_policy_lineage_index.py`、`seed_gapfill_policy_indicator_lib.py` 的 `--apply` 改为调用同一个 `apply_from_seed()`（治理按钮），不再执行整表删除。`--check` 仍校验行形状。生成的 SQL 里没有 `DELETE FROM`、`TRUNCATE`。

全景、评价、推演的写入函数未改行为。

## 自检行数（假游标，未连演示库）

| 序号 | 本次写入行数 | 样例 |
|------|--------------|------|
| 604 | 4 | 《广东省科技型中小企业研发环境支持》第一条的结论是符合条件的主体可以按该条款申请支持。 |
| 605 | 8 | 《广东省科技型中小企业研发环境支持》的扶持力度按文件载明的资助档位描述，不另造评分指标。 |
| 606 | 8 | 《广东省科技型中小企业研发环境支持》的主旨是明确支持对象，并说明如何申请。 |

604 的 4 行是 2 条政策 ×（原文条款 + 条款结论）。605 的 8 行是 2 条政策 × 四个维度。606 的 8 行是 2 条政策 × 四个侧面。两条 `policy_id` 来自假游标返回的 `18363390`、`18407696`，写函数源码里没有这两个字面量。

## 演示库行数

库名：`demo_gkxlumenx_ods` / `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads`，外加缺项库 `gkxlumenx_gapfill`。`assert_demo_mysql_targets` 通过后各跑了一次 `run("governance")`、`run("parse")`。生成方式为「模板句」。

| 序号 | 本次写入行数 | 表内总行数 | 样例 |
|------|--------------|------------|------|
| 604 | 4 | 14 | 《工业和信息化部办公厅关于印发重点跟踪培育纺织服装品牌企业名单（2020版）的通知》第一条的结论是符合条件的主体可以按该 |
| 605 | 8 | 20 | 《工业和信息化部办公厅关于印发重点跟踪培育纺织服装品牌企业名单（2020版）的通知》的扶持力度按文件载明的资助档位描述， |
| 606 | 8 | 8 | 《工业和信息化部办公厅关于印发重点跟踪培育纺织服装品牌企业名单（2020版）的通知》的主旨是明确支持对象，并说明如何申请 |

政策键是 `18318860`、`18318861`，标题与 `demo_gkxlumenx_dwd.policy_base_info` 一致。605 本批 8 行的 `metric_id` 都是空。维度各 2 行，侧面各 2 行。

写前写后没变的批次：`SYNTH-SIM` 仍 1 行，`BTN-simulation` 仍 4 行，溯源旧批 `POL-L2-PC1-LINEAGE-GAPFILL-L01` 仍 10 行，指标库旧批 `POL-L2-PC1-INDLIB-GAPFILL-L01` 仍 12 行。

## 测试结果

两仓都执行 `python -m polan.mockgen.btn`，退出码 0。不连库。

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
btn self_check ok pages=7 written=0 method_fallback=模板句 upsert=BTN-batch
sample_199 {'序号': '199', '叶名': '检索结果智能排序', '表': 'gapfill_policy_qry_rank', '本次写入行数': 0, '表内总行数': 0, '样例': '', '读取页面与接口': '全景 GET /display/v1/policy/panorama/rank', '生成方式': '模板句'}
```

`written=0` 那一行是不连库的 `run("panorama")`。治理页和拆解页在 `conn is None` 时同样返回空字典。

假游标断言：治理返回序号集合为 604、605；拆解返回序号集合为 606；样例非空、不超过 60 字、不含 TODO/TBD/xxx/待补充/测试数据/N/A/null；治理两条 `DELETE` 的参数都是 `BTN-governance`，拆解一条 `DELETE` 的参数是 `BTN-parse`，条件都带 `gapfill_batch_id`；无 `TRUNCATE`；605 的插入语句没有 `metric_id`；604 和 606 的插入同样不带 `metric_id`。

两个种子 `--check` 退出码 0。生成的 SQL 无 `DELETE FROM`、`TRUNCATE`。

两仓 SHA256：

- `btn.py`：`77da5db11fd98d3ed0a650cf7787c0e07f848c520690048c352b342a07c44f2e`
- `governance.py`：`04dc1895d9f5d83185bcabccdcf2a557a995abf1e2a4319be4dfedfeab0a6935`
- `parse.py`：`71de6426b51d03abe67b28d930a6c0123dc18eea86f22e6f8042717c2cc66f01`

## 遗留风险

- 溯源索引和指标库现网没有业务唯一键。本批追加在旧种子旁边，只删 `BTN-governance`。重跑不会清掉 `POL-L2-PC1-*` 旧行。
- 政策按 `policy_id` 排序取前 2 条干净标题。这次取到的是纺织服装品牌名单和蚕桑丝绸计划。
- 602、603、607、608、609 仍不在回执序号里。展示若要单独显示「未灌」行，要先改 `_LINES`，本单不改。
- 单飞仍只在本进程内。
- 未开始 B06。

## CI/CD（必填）

- 分支：`dev` → `origin/dev`
- demo-algo-ent-analysis：`89ef53b7b3b41a74060ef9ffe1b008d70a6346a2`
- lumen-algo-py：`76e3c7fe50778a6a7f21f313ebfd798e3569279f`（本单提交 `4a67dfa7611e3c14e4d505edf4ae466a75ac7b7e`，推送前与远端 merge）
- gkx-orchestration：本 handoff 这一次提交。推送后以 `git log -1` 为准
- pipeline：提交后由远端 CI 触发，此处未抄运行结果
- 部署：无新缺项表。镜像随两仓 dev 流水线发布后，按钮代码才在运行中的服务里
- K8s rollout：未在本单核对

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | 符合。只加治理和拆解灌数 |
| 调用链不越层 | 符合。未改 Java / 前端 |
| 图谱 | 符合。未写图 |
| D16 缺项只进 `gapfill_` | 符合。upsert 仍拒绝非 `gapfill_` 表 |
| 不写 ODS、正式 DWD、ADS、供应方库 | 符合。本次连接的是 `demo_gkxlumenx_*`。政策键只读 `policy_base_info` |
| 不新造 `metric_id` | 符合。604、605、606 都不写该列 |
| D18 接口不返回写死 mock | 符合。不连库时样例是空字符串；连上后样例来自本批句子 |
| D12 | 符合。lumen 侧 mockgen 是字节副本 |
| 可观测 | 沿用按钮框架的失败日志。未加新 span |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 200000（估算，含本会话上下文，非控制台精确值） |
| model_used | `grok-4.7` |
| actual_cost | 1.00（按算法工程化量级估算，美元） |
| cost_warn | `green` |

## 涉及文件

- `repos/demo-algo-ent-analysis/polan/mockgen/governance.py`（新建）
- `repos/demo-algo-ent-analysis/polan/mockgen/parse.py`（新建）
- `repos/demo-algo-ent-analysis/polan/mockgen/btn.py`
- `repos/lumen-algo-py/vendor/entan-py/polan/mockgen/` 下同三份文件（字节一致）
- `repos/lumen-algo-py/scripts/seed_gapfill_policy_lineage_index.py`
- `repos/lumen-algo-py/scripts/seed_gapfill_policy_indicator_lib.py`
- 上述两份脚本对应的 `scripts/mysql/gapfill_policy_lineage_index.sql`、`gapfill_policy_indicator_lib.sql`（去掉整表删除）
- 本 handoff

## 未完成

- 未改任务状态。
- B06 及以后的页未开始。
