# POL-MOCK-BTN-B01 · 按页重灌按钮框架与回执

> 2026-11-09。只搭七页按钮的启动、单飞、回执和幂等写入约束。各页灌数是 B02–B07，本单写 0 行。未改任务状态。

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
| 说明 | 与派单强度一致。未用 YAGNI 跳过 D16：公共写入只接受 `gapfill_` 表，写前 `assert_demo_mysql_targets`，正式库拒绝。回执在写 0 行时样例为空字符串，不造句。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无 |
| 图 diff | 本单不改图 |
| 会签态 | 无 |
| 说明 | 未改存储流图或接口图 |

## 修改内容

按页入口在 `polan/mockgen/btn.py`。与 `synth` 共用进程内单飞（同一把锁和 `_STATE`）。进度与回执走已有 GET，不另开轮询口。页写入函数本单都是空实现，`register_page` 留给后续单换上。

未改 `synth.py`，未改 `_upsert_sim_forecast`，未重建或清空任何缺项表。

### 接口路径

| 方法 | 路径 | 作用 |
|------|------|------|
| POST | `/v1/policy/mock/page` | 启动一页。JSON 体 `{"page":"<页键>"}` |
| GET | `/v1/policy/mock/synth` | 与合成、补外围共用的状态轮询。进行中 `data.job` 为 `btn:<页键>`；结束后回执在 `data.last` |

页键：`panorama` / `evaluation` / `simulation` / `governance` / `parse` / `compare` / `report`。

- 页键非法：`code=1`，`msg` 为 `page 须为 panorama/evaluation/simulation/governance/parse/compare/report`。
- 已有合成、补外围或另一页在跑：`code=1`，`msg` 为 `已有 Mock 任务在进行`，`data` 为当前状态。
- 接受后立即返回 `synth.status()`，写入在后台线程。
- 正式库：后台捕获 `RuntimeError`，`data.last.status=failed`，`data.last.note` 以 `失败：refusing non-demo MySQL target` 开头。其它异常的 note 只留类型名。

`data.last` 字段：`job`、`page`、`page_name`、`status`、`method`、`written`、`receipt`、`duration_sec`、`note`、`finished_at`。

### 回执字段

`receipt` 按需规序号逐行，键名如下：

| 字段 | 含义 |
|------|------|
| 序号 | 需规序号。一序号一行 |
| 叶名 | 说明书 §2 的叶名 |
| 表 | 缺项表或已有 ADS 表。多表用顿号连接。不建表的序号写「不建表」或「不另建表」 |
| 本次写入行数 | 本单固定 0 |
| 表内总行数 | 连上演示库时按表 `COUNT(*)`，多表相加。自检不连库，为 0 |
| 样例 | 不超过 60 字。本次写入为 0 时固定空字符串 |
| 读取页面与接口 | 展示页与 `/display/v1/policy/...` |
| 生成方式 | `大模型` 或 `模板句` |

批次号 `BTN-<页键>`。后续写入走 `upsert_button_rows`：先 `DELETE ... WHERE gapfill_batch_id=%s`，再 `INSERT ... ON DUPLICATE KEY UPDATE`。不 `TRUNCATE`，不删其它批次。检索三表和动向四表（`gapfill_policy_qry_*` 三张、`gapfill_policy_trend_*` 三张、`gapfill_policy_theme_dist`）不写 `is_mock`。

`gapfill_policy_sim_forecast` 若被后续单经此函数写入，删除条件只等于 `BTN-simulation`，碰不到 DS12 的 `SYNTH-` 行。本单推演页写入函数返回空，不会调用这次删除。

无密钥时 `render_sentence` 返回模板句且不调用传入的模型函数。有密钥但模型函数抛错，同样退回模板句。框架自己不调模型。

### 回执覆盖的序号

| 页键 | 序号 |
|------|------|
| panorama | 197、198、199、200、205、206、209–218 |
| evaluation | 219–231 |
| simulation | 232–242 |
| governance | 604、605 |
| parse | 606 |
| compare | 610、611、613 |
| report | 614–618 |

197、198、200、206 在总控序号格里没有单列，表名单含 `qry_*` 与 `theme_dist`，所以挂在全景页。201、202、204、602、603、607–609、612 不进回执。221、231、240 的表为「不建表」。237 为「不另建表」。209、212、216、218、223、226 只登记已有 ADS 表，`upsert_button_rows` 拒绝非 `gapfill_` 表。

205 一行三张动向表，表内总行数是三张表相加。223 一行两张 ADS 表，同样相加。

## 测试结果

两仓都执行 `python -m polan.mockgen.btn`，退出码 0。不连库。

```
btn self_check ok pages=7 written=0 method_fallback=模板句 upsert=BTN-batch
sample_199 {'序号': '199', '叶名': '检索结果智能排序', '表': 'gapfill_policy_qry_rank', '本次写入行数': 0, '表内总行数': 0, '样例': '', '读取页面与接口': '全景 GET /display/v1/policy/panorama/rank', '生成方式': '模板句'}
```

自检覆盖：七页回执字段齐全且写入 0、样例空；无密钥不调模型函数；模型函数抛错退回模板句；正式库 `run` / `upsert` 抛 `refusing non-demo` 且不执行 SQL；仿真表删除语句只带 `BTN-simulation`；检索名次表 SQL 无 `is_mock`；全景 `run` 只 `COUNT` 不 `DELETE`；单飞占用时 `start` 返回 False。

两仓 `python -m py_compile api/policy_routes.py` 退出码 0（lumen 在 `vendor/entan-py` 下）。

`btn.py` 两仓 SHA256：`E3AC32F45E5F201C9DC97630EF39061655A7B2B28A0E109F302E14D494E5156B`。

## 遗留风险

- 页写入仍是空函数。线上点按钮会连演示库、计总行数、写 0 行，不改变已有缺项行。
- 业务键与其它批次冲突时，`ON DUPLICATE KEY UPDATE` 会改到同一键的那一行。不冲突的其它批次不删。
- 单飞只在本进程内。
- 237 仍无缺项行种类。本单不臆造。
- 未对真实演示库点按钮。

## CI/CD（必填）

- 分支：`dev` → `origin/dev`
- demo-algo-ent-analysis：`31af291c9fcf7969208b4d0719c649c928582ee9`（其上 `ece688449549b8406fa18e6cc9bc988186bdce73` 为框架首提）
- lumen-algo-py：`cdd073af7c1fba10ffd09e8c7217b8cc165adc2c`（其上 `7cc06cc282589a8fa57cdd3fe545bc47c6e46664` 为框架首提）
- gkx-orchestration：本 handoff 这一次提交。推送后以 `git log -1` 为准
- pipeline：提交后由远端 CI 触发，此处未抄运行结果
- 部署：无新缺项表，不依赖本次镜像才存在框架代码。镜像随两仓 dev 流水线发布
- K8s rollout：未在本单核对

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | 符合。只加按钮框架 |
| 调用链不越层 | 符合。未改 Java / 前端 |
| 图谱 | 符合。未写图 |
| D16 缺项只进 `gapfill_` | 符合。upsert 拒绝其它表名 |
| 不写 ODS、正式 DWD、ADS、供应方库 | 符合。写前拒绝非 `demo_` 的 ODS/DWD/ADS。ADS 序号只计数 |
| 不新造 `metric_id` | 符合。写入函数不补指标号 |
| D18 接口不返回写死 mock | 符合。写 0 行时样例是空字符串 |
| D12 | 符合。lumen 侧是 vendor 字节副本，不是把 demo 并进 lumen |
| 可观测 | 失败写进程日志。未加新 span |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 180000（估算，含本会话上下文，非控制台精确值） |
| model_used | `grok-4.7` |
| actual_cost | 0.90（按算法工程化量级估算，美元） |
| cost_warn | `green` |

## 涉及文件

- `repos/demo-algo-ent-analysis/polan/mockgen/btn.py`（新建）
- `repos/demo-algo-ent-analysis/api/policy_routes.py`（POST `/v1/policy/mock/page`）
- `repos/lumen-algo-py/vendor/entan-py/polan/mockgen/btn.py`（字节一致副本）
- `repos/lumen-algo-py/vendor/entan-py/api/policy_routes.py`（同一路由）
- 本 handoff

## 未完成

- B02–B07 的按页灌数未开始。
- 未改任务状态。
- 未配大模型密钥，也未调用模型。
