# TS-L2-DS02-SCORE-L01 · 科学技术全景三个数字灌数

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | task-get 未返回该字段。开工时状态已是 `in_progress` |
| 说明 | 不改 task-registry，不把任务标 done |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只建一张 D18 mock 表，编号复用读图返回的 id。未跳过调用链、D18、指标身份 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `TS-L2-DS02-SDD-DATA` |
| 图 diff | 图保持原样。已写入的技术点图供给三个功能；`ads_technology_panorama_score` 只供给关联实体和关键路径的三个数字。灌数不在 `graph` 请求里 |
| 会签态 | 源文件无 frontmatter。抄 `TS-L2-DS02-SDD`：功能架构四角色同意。签收未做 |
| 说明 | 说明书第 4 节。没有改 Mermaid 语义 |

## 修改内容

- 库表 `demo_gkxlumenx_ads.ads_technology_panorama_score`。D18 mock 结果表。不在 ODS、DWD、供应方库，表名没有 `gapfill_` 前缀。
- 列只有 `subject_id`、`score_kind`、`score_value`。`score_kind` 闭集是 `influence`、`centrality`、`path_priority`。对齐 `JdbcPanoramaScores` 的只读 SELECT。
- `subject_id` 用读图同一套 id：技术点是 `technology_node_id`（中心度，`M_TECH_PATH_CENTRALITY`），论文 / 专利 / 机构是 `paper_id` / `patent_id` / `institution_id`（影响力，`M_TECH_ENTITY_INFLUENCE`）。路径优先级对应 `M_TECH_PATH_PRIORITY`，id 会走 `path_id`。
- 数值是可重复的 mock，不是这三条注册公式的输出。没有新造 `metric_id`，没有改口径，没有把 D4 改成 live。
- `POST /internal/tech-graph/read` 和写入接口没有改。建表和灌数在独立脚本里。
- 口令不在本次新增文件里。脚本从环境变量或仓内已有配置读取。

## 测试结果

- `python scripts/seed/seed_technology_panorama_score.py --check`：`ok=true`。列名与 `score_kind` 闭集通过，不连库。
- `python -m pytest tests/test_technology_panorama_score.py -q`：1 passed。
- `python scripts/seed/seed_technology_panorama_score.py --apply`：连上 `10.50.11.76` 的 `demo_gkxlumenx_ads`，表已在库里。灌入 271793 行。`centrality` 19430，`influence` 252363。`other_kinds=0`。
- 灌完后再查 information_schema：列顺序就是 `subject_id`、`score_kind`、`score_value`。空编号和超 128 字的编号为 0。图上技术点 `tcn_000f21ac06aceb9cdd0575e82d0d85fc` 有中心度行，论文 `W1014257459` 有影响力行。
- 图上技术点 19430、论文 108337、专利 126484、机构 17542，分页行数与 `count` 一致。人顶点为 0。边类型里没有 `tech_path_step`、`tech_rel`、`tech_has_*`，路径优先级 0 行。

## 遗留风险

- 路径优先级没有可对齐的路径编号，所以没有灌 `path_priority`。图上出现 `tech_path_step` 后，重跑 `--apply` 会补上，仍用读图的 `path_id`。
- 读图选中点时，属性 `WHERE` 会报 `IndexNotFound`。本单没有改读接口。三个数字要等那次读图能把实体和路径带回，Java 才会按编号填上。
- 人的影响力没有行：`tech_person` 为 0，也没有 `tech_has_person`。
- 默认打开读图最多回 200 个技术点。中心度按全部技术点编号灌了，这 200 个是其中的子集。
- 集群里 display 是否已有 ADS 口令，本单没有改 Helm。

## CI/CD（必填）

- 分支：`lumen-algo-py` `dev`
- commit：`828315a4bb8dad6225d51296913a9ec38dc3fdf1`
- push：`origin/dev`（`13906c3..828315a`）。未 force，未推 main
- pipeline URL / ID：未查
- 部署 namespace / 镜像 tag：未查
- K8s rollout：未查。本单是建表灌数，不靠这次镜像才有行
- dev 测试 URL / 命令与结果：见测试结果。编排仓本单不提交

## 架构合规自检

1. 算法只在 Python。这次没有跑注册公式，只写 mock 行。✅
2. 调用链未改。分数仍由 display 按编号只读这张表。✅
3. 没有写 `gkx_chain`，没有改图空间。✅
4. 可观测沿用现有服务，本叶不另建 tracer。✅
5. 已 push `origin/dev`。CI 结果未查。✅（未宣称绿）
6. D12：没有调用 `demo-*` 服务。✅
7. D18：表在 `demo_gkxlumenx_ads`，Python 灌 mock，Java 只读。D4 仍是 mock。✅

## 涉及文件

- `scripts/mysql/ads_technology_panorama_score.sql`
- `scripts/seed/seed_technology_panorama_score.py`
- `tests/test_technology_panorama_score.py`

## 没做的事

- 没有把任务标 done，没有改 `task-registry.yaml`，没有提交 `gkx-orchestration`。
- 没有改指标注册口径，没有把 D4 改成 live。
- 没有改 `POST /internal/tech-graph/read`，没有改写入接口。

## 范围与实现

在 `demo_gkxlumenx_ads.ads_technology_panorama_score` 建 D18 mock 表并灌行。列是 `subject_id`、`score_kind`、`score_value`。`score_kind` 只允许 `influence`、`centrality`、`path_priority`。编号对齐读图返回的技术点、论文、专利、机构 id。

## 偏离

路径优先级 0 行：图上没有 `tech_path_step`，没有可对齐的路径编号，没有另造 id。人的影响力 0 行：人顶点为 0。

## 产物清单

- `lumen-algo-py` `828315a4bb8dad6225d51296913a9ec38dc3fdf1`
- `scripts/mysql/ads_technology_panorama_score.sql`
- `scripts/seed/seed_technology_panorama_score.py`
- `tests/test_technology_panorama_score.py`

## 验收证据

`--check` 通过。`pytest tests/test_technology_panorama_score.py`：1 passed。`--apply` 已在库中灌入 271793 行（centrality 19430，influence 252363，path_priority 0）。

## Cost 回填

- actual_tokens: 12000
- model_used: claude-sonnet-4.5（会话模型 Grok 4.7，枚举无 Grok，按登记枚举回填）
- actual_cost: 0.06
- cost_warn: green
