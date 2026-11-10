# POL-MOCK-BTN-B04 · 推演按钮灌数

> 2026-11-09。只换推演页的写入函数。治理及以后的页仍是空实现。未改任务状态。未开始 B05。

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
| 说明 | 与派单强度一致。未用 YAGNI 跳过 D16：缺项只进 `gkxlumenx_gapfill`，写前 `assert_demo_mysql_targets`。232 不另写一套文案，与合成入口共用 `upsert_sim_forecast`。237 不另建表，240 不灌。不写布局推荐，不新造 `metric_id`。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无 |
| 图 diff | 本单不改图 |
| 会签态 | 无 |
| 说明 | 未改存储流图或接口图 |

## 修改内容

`register_page("simulation", write_simulation)` 换掉推演页的 `_zero`。`write_simulation(ctx)` 返回 `{序号: {written, sample, method}}`。`conn` 为空时返回空字典，回执仍是 0 行。

幂等走已有 `upsert_button_rows`：`DELETE ... WHERE gapfill_batch_id=%s`，参数 `BTN-simulation`，再 `INSERT ... ON DUPLICATE KEY UPDATE`。不 `TRUNCATE`，不整表 `DELETE`。不写 `BTN-panorama`、`BTN-evaluation`。

232 不走这批删除。`synth._upsert_sim_forecast` 改为调用 `polan.mockgen.simulation.upsert_sim_forecast`。合规文案只在 `compliance_row()`。键是政策类型「知识产权」、覆盖「广东省高新技术企业」、力度「每人每年30万元」、实施时间「2026年至2028年」。`target_industry` 是「新一代信息技术 / 集成电路 / 半导体材料」。经济效益句与逐年趋势按 DS12 原句写回。`metric_id` 是已有 `M_POLICY_SIMULATE`，`gapfill_batch_id` 是 `SYNTH-SIM`，`fill_method` 是 `llm-synth`。按钮在本批写入之后再调用它，避免同键更新把批次改成 `BTN-simulation`。

233、234 写入 `gapfill_policy_sim_forecast`，`metric_id` 同样只用 `M_POLICY_SIMULATE`。233 的 `policy_id` 和标题来自本次查询的 `demo_gkxlumenx_dwd.policy_base_info`，最多 2 条。234 按地区「广东省 / 深圳市」各一行。

235、238、239、241、242 合写一次 `gapfill_policy_sim_result`。236 写一次 `gapfill_policy_sim_stakeholder`。这两张表不写 `metric_id`。238 及以后挂在本批第一条新出台政策上。237 回执 `written=0`、样例空。240 同样。不调用布局推荐，不写 `M_POLICY_LAYOUT_REC_COUNT`。

无密钥时正文用模板句，生成方式写「模板句」，不报错。样例经 `clip_sample`，不超过 60 字。回执「本次写入行数」是本按钮这次插入或更新的行，不是表内 `COUNT(*)`。

`seed_gapfill_policy_sim_forecast.py`、`seed_gapfill_policy_sim_result.py` 的 `--apply` 改为调用 `apply_from_seed()`，不再执行整表 `DELETE`。`--check` 仍校验行形状。生成的 SQL 里没有 `DELETE FROM`、`TRUNCATE`。

评价页和全景页的写入函数未改行为。

## 自检行数（假游标，未连演示库）

| 序号 | 本次写入行数 | 样例 |
|------|--------------|------|
| 232 | 1 | 经济效益预测值约74亿元，相对基线变化率约4.2%。AI推演结果，仅供参考。 |
| 233 | 2 | 短期内《广东省科技型中小企业研发环境支持》的办理与兑现更顺畅，受惠主体数 |
| 234 | 2 | GDP增长约1.2个百分点。AI推演结果，仅供参考。 |
| 235 | 4 | 经济效益高于其余三维。AI推演结果，仅供参考。 |
| 236 | 3 | 建议把研发补助的覆盖范围写清楚，便于部门执行。 |
| 237 | 0 | （空） |
| 238 | 4 | 把研发投入强度作为这组重点的展示项。AI推演结果，仅供参考。 |
| 239 | 3 | 受惠主体以科技型中小企业为主。AI推演结果，仅供参考。 |
| 240 | 0 | （空） |
| 241 | 5 | 发布申报通知。AI推演结果，仅供参考。 |
| 242 | 4 | 为改善科技型中小企业研发环境而作的推演正文。AI推演结果，仅供参考。 |

233 的两条 `policy_id` 来自假游标返回的 `18363390`、`18407696`，写函数源码里没有这两个字面量。232 的 1 是共享函数本轮 upsert 的一行，批次参数是 `SYNTH-SIM`，不是 `BTN-simulation`。

## 演示库行数

库名：`demo_gkxlumenx_ods` / `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads`，外加缺项库 `gkxlumenx_gapfill`。`assert_demo_mysql_targets` 通过后跑了一次 `run("simulation")`。生成方式为「模板句」。回执本次写入合计 28 行。

| 序号 | 本次写入行数 | 表内总行数 | 样例 |
|------|--------------|------------|------|
| 232 | 1 | 24 | 经济效益预测值约74亿元，相对基线变化率约4.2%。AI推演结果，仅供参考。 |
| 233 | 2 | 24 | 短期内《工业和信息化部办公厅关于印发重点跟踪培育纺织服装品牌企业名单（2020版）的通知》的办理与兑现更顺畅，受惠主体数 |
| 234 | 2 | 24 | GDP增长约1.2个百分点。AI推演结果，仅供参考。 |
| 235 | 4 | 41 | 经济效益高于其余三维。AI推演结果，仅供参考。 |
| 236 | 3 | 11 | 建议把研发补助的覆盖范围写清楚，便于部门执行。 |
| 237 | 0 | 0 | （空） |
| 238 | 4 | 41 | 把研发投入强度作为这组重点的展示项。AI推演结果，仅供参考。 |
| 239 | 3 | 41 | 受惠主体以科技型中小企业为主。AI推演结果，仅供参考。 |
| 240 | 0 | 0 | （空） |
| 241 | 5 | 41 | 发布申报通知。AI推演结果，仅供参考。 |
| 242 | 4 | 41 | 为改善科技型中小企业研发环境而作的推演正文。AI推演结果，仅供参考。 |

233 写入的政策键是 `18318860`、`18318861`，标题与 `demo_gkxlumenx_dwd.policy_base_info` 一致。预测表本批 4 行的 `metric_id` 都是 `M_POLICY_SIMULATE`。结果表本批没有 `M_POLICY_LAYOUT_REC_COUNT`。

合规行仍在，逐字核对通过：四段键、目标产业、经济效益句、逐年「2026年62、2027年71、2028年80」、社会影响句、创新促进句、解释句都与 DS12 原句一致。`gapfill_batch_id=SYNTH-SIM`，`metric_id=M_POLICY_SIMULATE`。预测表批次仍有 `POL-L2-DS12-EST-GAPFILL-L01` 4 行、`POL-L2-DS12-DEMO-EXTRA` 15 行、`BTN-simulation` 4 行、`SYNTH-SIM` 1 行。

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
btn self_check ok pages=7 written=0 method_fallback=模板句 upsert=BTN-batch
sample_199 {'序号': '199', '叶名': '检索结果智能排序', '表': 'gapfill_policy_qry_rank', '本次写入行数': 0, '表内总行数': 0, '样例': '', '读取页面与接口': '全景 GET /display/v1/policy/panorama/rank', '生成方式': '模板句'}
```

`written=0` 那一行是不连库的 `run("panorama")`。推演页在 `conn is None` 时同样返回空字典。

`python -c "from polan.mockgen.synth import self_check; self_check()"` 退出码 0，输出 `policy synth self_check OK`。

假游标断言：返回序号集合为 232–242；237 与 240 的写入为 0、样例为空；其余样例非空、不超过 60 字、不含 TODO/TBD/xxx/待补充/测试数据/N/A/null，也不含布局推荐指标；每条 `DELETE` 的条件带 `gapfill_batch_id` 且参数为 `BTN-simulation`；无 `TRUNCATE`；插入只落到预测、结果、参与意见三张缺项表；预测行的 `metric_id` 只有 `M_POLICY_SIMULATE`；结果表和意见表的插入不带 `metric_id`；合规键四段字符串出现在 `upsert_sim_forecast` 源码里；经济效益句只在 `compliance_row`，合成入口的 `_upsert_sim_forecast` 不再保留第二套文案。

两个种子 `--check` 退出码 0。生成的 SQL 无 `DELETE FROM`、`TRUNCATE`。

两仓 SHA256：

- `btn.py`：`dc7c6cb127150e6382b692989bb78364ff69165341ed2c68ef3021a7feb032a1`
- `synth.py`：`2446239039c038bb29128514d4bff7fc3a7f846cc41834edfd8d036a97a6be9e`
- `simulation.py`：`be5a377b4aec9ee5dbed3ded9d69e9521dfc91ff8fa1c8fae3cebdc997955dbd`

## 遗留风险

- 结果表的重点、影响范围，以及参与意见表，现网没有业务唯一键。本批追加在旧种子旁边。维度、路径、解读和区域空间有唯一键，同键旧行会被改成 `BTN-simulation`。
- 新出台预测按 `policy_id` 排序取前 2 条干净政策。这次取到的是纺织服装品牌和蚕桑丝绸计划，不是种子 SQL 里的 `18363390`、`18407696`。那两行旧批次还在。
- 共享函数每次会刷新合规行的 `generated_at`。四段键、目标产业、经济效益句、逐年趋势和 `SYNTH-SIM` 批次不变。
- 单飞仍只在本进程内。
- 未开始 B05。

## CI/CD（必填）

- 分支：`dev` → `origin/dev`
- demo-algo-ent-analysis：`1571eb0af984e0bb085c5566a6dc32bbe70c1523`
- lumen-algo-py：`268c574ae5db2dcae81046a9ca785d8b0448eb6a`
- gkx-orchestration：本 handoff 这一次提交。推送后以 `git log -1` 为准
- pipeline：提交后由远端 CI 触发，此处未抄运行结果
- 部署：无新缺项表。镜像随两仓 dev 流水线发布后，按钮代码才在运行中的服务里
- K8s rollout：未在本单核对

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | 符合。只加推演灌数 |
| 调用链不越层 | 符合。未改 Java / 前端 |
| 图谱 | 符合。未写图 |
| D16 缺项只进 `gapfill_` | 符合。upsert 仍拒绝非 `gapfill_` 表 |
| 不写 ODS、正式 DWD、ADS、供应方库 | 符合。本次连接的是 `demo_gkxlumenx_*`。政策键只读 `policy_base_info` |
| 不新造 `metric_id` | 符合。232–234 只用 `M_POLICY_SIMULATE`。结果表和意见表该列留空 |
| D18 接口不返回写死 mock | 符合。不连库时样例是空字符串；连上后样例来自本批句子 |
| D12 | 符合。lumen 侧 mockgen 是字节副本 |
| 可观测 | 沿用按钮框架的失败日志。未加新 span |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 180000（估算，含本会话上下文，非控制台精确值） |
| model_used | `grok-4.7` |
| actual_cost | 0.90（按算法工程化量级估算，美元） |
| cost_warn | `green` |

## 涉及文件

- `repos/demo-algo-ent-analysis/polan/mockgen/simulation.py`（新建）
- `repos/demo-algo-ent-analysis/polan/mockgen/btn.py`
- `repos/demo-algo-ent-analysis/polan/mockgen/synth.py`
- `repos/lumen-algo-py/vendor/entan-py/polan/mockgen/` 下同三份文件（字节一致）
- `repos/lumen-algo-py/scripts/seed_gapfill_policy_sim_forecast.py`
- `repos/lumen-algo-py/scripts/seed_gapfill_policy_sim_result.py`
- 上述两份脚本对应的 `scripts/mysql/gapfill_policy_sim_*.sql`（去掉整表 `DELETE`）
- 本 handoff

## 未完成

- 未改任务状态。
- B05 及以后的页未开始。
