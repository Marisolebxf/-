# POL-L2-DS11-PLAN-GAPFILL-L01 · 政策分析评价 · 推荐方案报告交互展示 · 灌数

- 任务：`POL-L2-DS11-PLAN-GAPFILL-L01`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 执行：`agent:data-agent`
- 状态：`in_progress`（本单不改状态，等 AV）
- 强度：ponytail full
- 上游：`sdd/l2/POL-L2-DS11-PLAN-DATA.md`（已签收数据落点，本单照它落地）
- 参考做法：`POL-L2-DS10-CMP-GAPFILL-L01`（commit `40d84e2`）

## 范围与实现

按分册在 `gkxlumenx_gapfill`（10.50.11.76:3306）建**一张**表 `gapfill_policy_eval_scheme`，并用独立脚本灌 mock。`row_kind` 只有四种：方案对照、参数模拟、路径与风险、互动意见。不拆四张表，不建 `scheme_id`，不建外键。

- **227 方案对照**：一方案一行，`scheme_name` 互不相同。灌 2 个方案（研发投入加力方案 / 人才引育优先方案），`compare_dims` 同格分行写「维度名：数值」
- **228 参数模拟**：`scheme_name + param_band` 唯一。研发投入方案 3 档（资金基准/资金加力/平台强化）、人才方案 2 档（规模基准/规模扩容），共 5 行
- **229 路径与风险**：一方案多行（每行同带节点与风险）。两方案各 3 个节点，共 6 行；`metric_id` 固定 `M_POLICY_DS_11_POLICY_EVAL_015`
- **230 互动意见**：一方案多行，分类只用 评价/评论/建议。两方案各 3 条，共 6 行；`metric_id` 留空
- **231 导出**：不建行、不占 `row_kind`、不灌任何文件。231 读 227 行 + 230 行拼装，本单不管

`is_mock=1`、`fill_method='manual'`、`gapfill_batch_id='POL-L2-DS11-PLAN-GAPFILL-L01'` 全行一致。不设 `fill_model`（D16 只在 `llm` 时要求）。

## 与分册对照

| 分册要求 | 落地 |
|---|---|
| 只建 `gapfill_policy_eval_scheme` 一张表 | ✅ `information_schema` 里本单只建这一张（库里另有 partition/shell/trend 三张，为并行叶所建，与本单无关） |
| `row_kind` 四种闭集 | ✅ 校验闭集 + 表注释写明 |
| 227 至少两个方案 | ✅ 2 个 |
| 228 每方案至少一行参数模拟、方案+参数档唯一 | ✅ 3+2=5 行，键唯一有断言 |
| 229 每方案若干节点、`metric_id` 固定 `M_POLICY_DS_11_POLICY_EVAL_015` | ✅ 每方案 3 节点；6 行 metric 全部命中，其余种类 metric 全空（SELECT 验证 0 行违例） |
| 230 可灌已定意见行、分类闭集 | ✅ 评价/评论/建议 三分类齐备 |
| 不灌导出文件（PDF/Word/Excel/对象存储） | ✅ 脚本 BANNED 列表显式挡 `.pdf/.docx/.xlsx` |
| 不写 ODS、DWD、ADS | ✅ BANNED 挡库名 + 正则挡反引号全限定名 |
| 不改 D4、不新造 metric_id、不改 `M_POLICY_DS_11_POLICY_EVAL_015` | ✅ 未动 registry、未动 D4、未跑 metric MCP 写操作 |

## 验收证据（连库 SELECT）

实例 `10.50.11.76:3306`，账号 `gkxlumenx`，库 `gkxlumenx_gapfill`，表 `gapfill_policy_eval_scheme`：

```json
{
 "db": "gkxlumenx_gapfill",
 "by_kind": {"互动意见": 6, "参数模拟": 5, "方案对照": 2, "路径与风险": 6},
 "total": 19,
 "is_mock_rows": 19,
 "path_rows_with_metric": 6,
 "other_rows_with_metric_should_be_0": 0,
 "schemes": ["人才引育优先方案", "研发投入加力方案"],
 "param_keys": [
  "人才引育优先方案|人才规模基准档",
  "人才引育优先方案|人才规模扩容档",
  "研发投入加力方案|平台支撑强化档",
  "研发投入加力方案|资金规模加力档",
  "研发投入加力方案|资金规模基准档"
 ]
}
```

幂等：`--apply` 连跑两次，第二次输出 total 仍为 19（先 DELETE 本表再 INSERT，不碰别的表）。

## 灌数命令

在 `repos/lumen-algo-py`（PowerShell，不用 `&&`；口令只放进程环境变量，来自 helm `values.yaml` 既有配置，未写入脚本与本文）：

```powershell
python scripts/seed_gapfill_policy_eval_scheme.py --check
$env:LUMEN_ALGO_MYSQL_PASSWORD = "<secret>"
python scripts/seed_gapfill_policy_eval_scheme.py --apply
```

自检在 `--check` 里，不连库。断言：方案对照行四必填列、参数模拟键唯一、每方案节点数≥2、意见分类闭集、`metric_id` 在 SQL 中出现次数 = 路径行数 + 建表注释 1 次、BANNED 词零出现、INSERT 目标只有本表。

## 产物清单

- `repos/lumen-algo-py/scripts/seed_gapfill_policy_eval_scheme.py`（灌数脚本，含自检）
- `repos/lumen-algo-py/scripts/mysql/gapfill_policy_eval_scheme.sql`（--check 生成的可读 SQL）
- 本 handoff

## CI/CD

- 分支：`dev`
- commit：`423527e`（`feat(policy): 灌评价方案缺项表 [agent:data-agent]`）。推送时遇并行会话同仓提交，经 merge `a527c42` 合入后已在 `origin/dev`（`git branch -r --contains 423527e` 确认）
- pipeline：未查（灌数单，无部署）
- K8s rollout：未触发
- 测试：`--check` 退出码 0；`--apply` 连跑两次幂等；独立 SELECT 见上节

## 架构合规自检

- ✅ 调用链：本单只灌库，不改 Java、不改展示、不在接口里写死 mock
- ✅ 灌数在 Python：`lumen-algo-py/scripts/seed_gapfill_policy_eval_scheme.py`
- ✅ 图谱：未写 nGQL，未读政策子图
- ✅ D16：只写 `gkxlumenx_gapfill` 下 `gapfill_` 前缀表（本单仅一张）；行带 `is_mock`/`metric_id`/`gap_item`/`fill_method`/`gapfill_batch_id`/`generated_at`
- ✅ 未写 ODS、DWD、ADS、供应方库
- ✅ 未改 D4，`GDF-POLICY-MOCK-GATE-L01` 未动
- ✅ 未新造 `metric_id`，未改 `M_POLICY_DS_11_POLICY_EVAL_015`
- ✅ 未灌 PDF、Word、Excel、对象存储
- ✅ 意见请求不插入：本单只灌已定行，无任何写接口改动

## 遗留

- 读取方 `gkxlumen-element`（`jobs`/`shells`）接线属 `POL-L2-DS11-PLAN-API`，不在本单
- 任务状态仍 `in_progress`，等 coordinator AV
