# POL-MOCK-BTN-B02 · 全景按钮灌数

> 2026-11-09。只换全景页的写入函数。评价及以后的页仍是空实现。未改任务状态。

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
| 说明 | 与派单强度一致。未用 YAGNI 跳过 D16：缺项只进 `gkxlumenx_gapfill`，写前 `assert_demo_mysql_targets`。209/212/216/218 不建缺项表，演示 MySQL 上先校验再调已有 `run()`。201/202/204 不灌。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无 |
| 图 diff | 本单不改图 |
| 会签态 | 无 |
| 说明 | 未改存储流图或接口图 |

## 修改内容

`register_page("panorama", write_panorama)` 换掉全景的 `_zero`。`write_panorama(ctx)` 返回 `{序号: {written, sample, method}}`。`conn` 为空时返回空字典，回执仍是 0 行。

幂等走已有 `upsert_button_rows`：`DELETE ... WHERE gapfill_batch_id=%s`，参数 `BTN-panorama`，再 `INSERT ... ON DUPLICATE KEY UPDATE`。不 `TRUNCATE`，不整表 `DELETE`。检索三表和动向四表不写 `is_mock`，不 `ALTER`。不写 `gapfill_policy_sim_forecast`，碰不到 DS12 的 `SYNTH-` 行。

政策键只来自本次查询 `demo_*.policy_base_info` 的结果。无密钥时用这些字段填模板句，生成方式为「模板句」，不报错。一次最多抽 6 条政策。

`gapfill_policy_qry_stat` 只用已有 7 个 `metric_id`：`M_POLICY_TOTAL_COUNT`、`M_POLICY_LEVEL_DIST`、`M_POLICY_NATIONAL_DIST`、`M_POLICY_SZ_DIST`、`M_POLICY_TIMESERIES`、`M_POLICY_TYPE_DIST`、`M_POLICY_VALIDITY_RATE`。197 与 198 记这批统计行数，200 记目录行数。不新造指标。

名次列 `rank_dim` 仍写 `relevance` / `timeliness` / `importance`，因为全景排序读口按这三个因子取值。回执样例写「相关性 / 时效性 / 重要性」，不把英文码写进句子。时序列 `period_type` 仍是现表约定的 `Y`。

209 调 `polan.eval.effect.run`，212 调 `polan.text.match.run`，216 与 218 共用一次 `polan.eval.intensity.run`（同一张力度表，不连跑两次）。这三处只在 `backend=mysql` 时执行，且先 `assert_demo_mysql_targets`。自检注入空跑替身，不连库。

210 的已有 591 行、211 的已有 2 行不在 `BTN-panorama`，按钮不会清掉。

`seed_gapfill_policy_qry.py`、`trend.py`、`audience.py`、`assessment.py`、`cmp.py` 的 `--apply` 改为调用 `apply_from_seed()`，不再执行整表 `DELETE`。`--check` 仍校验旧的 SQL 形状，生成的 SQL 里没有 `DELETE FROM`。`sz_effect.py` 与 `demo_extra.py` 本来就不是整表清空，未改。

## 自检行数（假游标，未连演示库）

| 序号 | 本次写入行数 | 样例 |
|------|--------------|------|
| 197 | 18 | 本次汇总的政策总数为3。 |
| 198 | 18 | 本次汇总的政策总数为3。 |
| 199 | 9 | 《北京市产业园区扶持意见》在相关性排序中位于第1名。 |
| 200 | 3 | 《深圳市科技创新条例》由深圳市科技创新局于2024-03-01发布，适用于广东省深圳市。 |
| 205 | 12 | 《深圳市科技创新条例》所在的科创发展把研发机构布局写进同一组措施。 |
| 206 | 5 | 研发费用加计扣除在抽取政策里出现0条。 |
| 209 | 4 | 广东省效果评分已按既有口径重算。 |
| 210 | 6 | 来自问卷的意见认为，《深圳市科技创新条例》的办理材料希望能一次提交。 |
| 211 | 2 | 本报告评估广东省《深圳市科技创新条例》：达成度是支持范围更清楚；问题是材料重复提交；建议合并入口并公开时限。 |
| 212 | 4 | 已为演示主体匹配《深圳市科技创新条例》。 |
| 213 | 3 | 对照2023-01-15的文本，《深圳市科技创新条例》在2024-03-01这一稿上有新增。 |
| 214 | 3 | 申报单位注册地在广东省，事项与《深圳市科技创新条例》的适用对象一致。 |
| 215 | 6 | 部门对照按地区和实施部门汇总。 |
| 216 | 4 | 广东省力度指数已按既有口径重算，供标杆比对。 |
| 217 | 6 | 广东省《深圳市科技创新条例》在政策类型上与对照地区不同，可借鉴对方把同类措施写清楚的做法。 |
| 218 | 4 | 广东省力度指数已按既有口径重算，供对标展示。 |

197/198 的 18 行覆盖上面 7 个 `metric_id`，其中级别、类型各 5 行。209/212/216/218 的 4 是假游标对 `COUNT(*)` 的返回值，用来证明回执能带上行数，不是演示库落库行数。

201、202、204 不在返回的序号里。

## 没写 ADS 的原因

本次没有改 `demo_gkxlumenx_ads` 的 `policy_effect`、`policy_match`、`policy_intensity`。自检规定不连库。写入函数只在连接后端是 MySQL 且没有注入替身时，才调用 `effect.run` / `match.run` / `intensity.run`；调用前执行 `assert_demo_mysql_targets`。自检把后端标成演示 MySQL，但注入了三个空函数，所以只证明了调用顺序：`assert` → `effect` → `match` → `intensity`。

## 测试结果

两仓都执行 `python -m polan.mockgen.btn`，退出码 0。不连库。

```
panorama_writer 197=18 198=18 199=9 200=3 205=12 206=5 209=4 210=6 211=2 212=4 213=3 214=3 215=6 216=4 217=6 218=4
panorama_sample_199 《北京市产业园区扶持意见》在相关性排序中位于第1名。
btn self_check ok pages=7 written=0 method_fallback=模板句 upsert=BTN-batch
sample_199 {'序号': '199', '叶名': '检索结果智能排序', '表': 'gapfill_policy_qry_rank', '本次写入行数': 0, '表内总行数': 0, '样例': '', '读取页面与接口': '全景 GET /display/v1/policy/panorama/rank', '生成方式': '模板句'}
```

`written=0` 那一行是不连库的 `run("panorama")`：`conn is None` 时写入函数返回空字典，回执样例保持空字符串。

假游标断言：返回序号集合为 197、198、199、200、205、206、209–218；每条样例非空、不超过 60 字、不含 TODO/TBD/xxx/待补充/测试数据/N/A/null 和英文名次码；每条 `DELETE` 的条件是 `` `gapfill_batch_id`=%s `` 且参数为 `BTN-panorama`；无 `TRUNCATE`；不出现 `gapfill_policy_sim_forecast`；检索三表和动向四表的 SQL 无 `is_mock`；统计表插入的 `metric_id` 集合等于上述 7 个。

五份种子 `--check` 退出码 0。生成的 SQL 无 `DELETE FROM`。

两仓 SHA256：

- `btn.py`：`6C280A012B5CD02E5070DDA785548D99E94096611C143E252B514F9BCD70B4B5`
- `panorama.py`：`8FEAF3389FE4247627682724AF3B3483EFDBDC8FDE3C20E3B9B8529FA62C2C3B`

## 遗留风险

- 本单没有对演示库点按钮。线上点全景才会按 `BTN-panorama` 写入，并在演示 MySQL 上重跑效果、匹配和力度。力度 `run()` 与匹配 `run()` 会按它们既有实现清空对应 ADS 表后再写入。
- 其它批次的旧行保留。名次表若已有同一 `rank_dim` + `rank_no`，`ON DUPLICATE KEY UPDATE` 会改到那一行。不冲突的旧行不删，其中可能仍有早先种子的假政策号。
- 210、211 只有主键。本批新行追加在已有 591 行和 2 行之外，不覆盖它们。
- 单飞仍只在本进程内。
- 未开始 B03。

## CI/CD（必填）

- 分支：`dev` → `origin/dev`
- demo-algo-ent-analysis：`c5028a252ddf84e7619f036739ef5fe3d5c6fba3`
- lumen-algo-py：`2b5a055f50db9357de05b626a0fc48bf3a8c8d35`
- gkx-orchestration：本 handoff 这一次提交。推送后以 `git log -1` 为准
- pipeline：提交后由远端 CI 触发，此处未抄运行结果
- 部署：无新缺项表。镜像随两仓 dev 流水线发布后，按钮代码才在运行中的服务里
- K8s rollout：未在本单核对

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | 符合。只加全景灌数 |
| 调用链不越层 | 符合。未改 Java / 前端 |
| 图谱 | 符合。未写图 |
| D16 缺项只进 `gapfill_` | 符合。upsert 仍拒绝非 `gapfill_` 表 |
| 不写 ODS、正式 DWD、供应方库 | 符合。政策键只读演示 DWD。ADS 只准备调用已有 `run()`，本次未执行 |
| 不新造 `metric_id` | 符合。统计表只用已有 7 个 |
| D18 接口不返回写死 mock | 符合。不连库时样例是空字符串；连上后样例来自本批句子 |
| D12 | 符合。lumen 侧是 vendor 字节副本 |
| 可观测 | 沿用按钮框架的失败日志。未加新 span |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 220000（估算，含本会话上下文，非控制台精确值） |
| model_used | `grok-4.7` |
| actual_cost | 1.10（按算法工程化量级估算，美元） |
| cost_warn | `green` |

## 涉及文件

- `repos/demo-algo-ent-analysis/polan/mockgen/panorama.py`（新建）
- `repos/demo-algo-ent-analysis/polan/mockgen/btn.py`
- `repos/lumen-algo-py/vendor/entan-py/polan/mockgen/panorama.py`（字节一致副本）
- `repos/lumen-algo-py/vendor/entan-py/polan/mockgen/btn.py`（字节一致副本）
- `repos/lumen-algo-py/scripts/seed_gapfill_policy_qry.py`
- `repos/lumen-algo-py/scripts/seed_gapfill_policy_trend.py`
- `repos/lumen-algo-py/scripts/seed_gapfill_policy_audience.py`
- `repos/lumen-algo-py/scripts/seed_gapfill_policy_assessment.py`
- `repos/lumen-algo-py/scripts/seed_gapfill_policy_cmp.py`
- 上述五份脚本对应的 `scripts/mysql/gapfill_policy_*.sql`（去掉整表 `DELETE`）
- 本 handoff

## 未完成

- 未对演示库执行全景按钮，ADS 三张表本次没有重算。
- B03 及以后的页未开始。
- 未改任务状态。
