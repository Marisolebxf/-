# POL-L2-DS11-VIZ-GAPFILL-L01 · 政策分析评价可视化缺项表灌数

ponytail: full

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 任务已在 `in_progress`。本会话不改 task-registry，不把任务标成 done |
| 说明 | 派单授权提交脚本并推送 origin/dev |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用上一轮 CMP 灌数脚本（`40d84e2`）的 `--check`/`--apply` 幂等模式，未另起框架。未用 YAGNI 跳过 D16 追溯列 |

## 范围与实现

真源是 `sdd/l2/POL-L2-DS11-VIZ-DATA.md` 第 3、4 节。范围只有 219、220 两张缺项表。221 不建表（子图是第 7 项已有的），222 不建表、不灌模板选用。未写 ODS、DWD、ADS、供应方库，未改 D4，未新造 `metric_id`。

库目标是 `gkxlumenx_gapfill`。两张表已建并灌入：

| 表 | 序号 | 拣行键 | 库内行数 |
|---|---|---|---|
| `gapfill_policy_eval_trend` | 219 | `switch_dim` + `metric_name` | 44 |
| `gapfill_policy_eval_partition` | 220 | `object_kind`（带投向时再按 `resource_direction`） | 41 |

### 219 趋势（44 行）

三维齐备，同一维同一指标名下的多个 `dim_value` 组成一条序列：

| 维 | 序列数 | 行数 | 内容 |
|---|---|---|---|
| 时间 | 4 | 24 | 2021–2026 连续年份 × 4 个指标名（科技政策连续出台数、研发投入强度、企业受惠覆盖率、政策兑现满意度） |
| 区域 | 2 | 12 | 北京/上海/广东/江苏/湖北/四川 × 2 个指标名（研发投入强度、企业受惠覆盖率） |
| 类别 | 4 | 8 | 资金支持/人才培育/平台建设/税收优惠 × 2 个指标名（科技政策连续出台数、政策兑现满意度） |

每条序列至少一个 `is_key_point=1` 重点点；波动序列带 `is_fluctuation=1`（如出台数 2025 回落 79→2026 升 91）。数值贴合科技政策量级（研发投入强度 2.25–6.56、满意度 76–88、覆盖率 31–68）。灌数同 `switch_dim`+`dim_value`+`metric_name` 只一行（表上建了唯一键）。

### 220 分区（41 行）

三类对象齐备，柱状和热力共用同一批行；`resource_direction` 取财政资金/人才引进/创新平台/税费减免：

| 对象类 | 行数 | 内容 |
|---|---|---|
| 地区 | 24 | 6 省/市 × 4 投向全矩阵 |
| 行业 | 10 | 电子信息(3)、生物医药(2)、高端装备(2)、新材料(1)、新能源(2) |
| 目标群体 | 7 | 科技型中小企业(2)、高新技术企业(2)、青年科技人才(1)、高校科研团队(2) |

同 `object_kind`+`object_name`+`resource_direction` 只一行（唯一键，空投向按空值同档）。

### 追溯列

每行 `is_mock=1`，`metric_id` 留空，`gap_item` 分别为 `219 多维指标趋势图`、`220 分区/群体对比分析图`，`fill_method=manual`，`gapfill_batch_id=POL-L2-DS11-VIZ-GAPFILL-L01`，`generated_at=2026-11-03 21:40:00`。按 DATA 规定不设 `fill_model`、不设 `chart_type`、不设曲线 JSON 列。

## 偏离

| 偏离 | 理由 | as-built |
|------|------|----------|
| 无 | 列、拣行键、gap_item 与 DATA 第 3、4 节逐列一致 | — |

## 产物清单

- `repos/lumen-algo-py/scripts/seed_gapfill_policy_eval_viz.py`
- `repos/lumen-algo-py/scripts/mysql/gapfill_policy_eval_viz.sql`
- 本 handoff

未改 `/display/v1/policy/**`、未改 Java、未改 D4、未新造 `metric_id`、未写 nGQL。

## 验收证据

实例 `10.50.11.76:3306`，账号 `gkxlumenx`，库 `gkxlumenx_gapfill`。连库 SELECT（2026-11-03，口令只放进程环境变量，未打印、未写入脚本和本文）：

| 项 | 结果 |
|---|---|
| `SELECT COUNT(*) FROM gapfill_policy_eval_trend` | 44 |
| `SELECT COUNT(*) FROM gapfill_policy_eval_partition` | 41 |
| trend 按 `switch_dim` 分组 | 时间 24、区域 12、类别 8 |
| partition 按 `object_kind` 分组 | 地区 24、行业 10、目标群体 7 |
| 两表 `is_mock=1 AND metric_id IS NULL` | 44 / 41（全部行） |
| 拣行命中：`switch_dim='时间' AND metric_name='科技政策连续出台数'` | 返回 2021–2026 整条 6 点：48→62→75→83→79(波动)→91(重点) |
| 拣行命中：`object_kind='行业' AND resource_direction='财政资金'` | 5 行（新材料 96.5、新能源 104、生物医药 121、电子信息 132.5、高端装备 118） |
| 拣行落空：`switch_dim='行业'`（非三维） | 0 行 |
| `gapfill_policy_eval_shell` 表存在性 | 已存在（解读二级所建，本单未加列未灌模板行） |

幂等验证：`--apply` 连跑两次，行数保持 44 / 41 不翻倍（先 DELETE 再 INSERT）。

灌数命令（在 `repos/lumen-algo-py`，PowerShell，不用 `&&`）：

```
python scripts/seed_gapfill_policy_eval_viz.py --check
$env:LUMEN_ALGO_MYSQL_PASSWORD = "<secret>"
python scripts/seed_gapfill_policy_eval_viz.py --apply
```

`--check` 退出码 0，输出 `{"mode":"check","ok":true,"rows":{"gapfill_policy_eval_trend":44,"gapfill_policy_eval_partition":41}}`。`--apply` 退出码 0，输出 `{"mode":"apply","connected":true,"host":"10.50.11.76","port":3306,"db":"gkxlumenx_gapfill","rows":{"gapfill_policy_eval_trend":44,"gapfill_policy_eval_partition":41}}`。

自检在 `--check` 里（不连库），锁住：三维/三类对象齐备；拣行键唯一；每条序列完整有序且至少一个重点；时间维年份连续 2021–2026；拣行对不上返回空；每行 `is_mock=1`、`metric_id` 空、`fill_method=manual`；SQL 只写 `gkxlumenx_gapfill` 两张表，不出现 `fill_model`、`chart_type`、ODS/DWD/ADS、demo 库名、`M_POLICY_`、`policy_effect`。

## 架构合规自检

- ✅ D16：只写 `gkxlumenx_gapfill` 下两张 `gapfill_` 表，行上带规定追溯列；未写 ODS、DWD、ADS、供应方库
- ✅ 221 不建表、222 不建表不灌模板选用；壳表未加列
- ✅ 未改 D4，未动 `GDF-POLICY-MOCK-GATE-L01`
- ✅ 未新造 `metric_id`；趋势点与对照数不是指标
- ✅ 调用链：本单只灌库，不改 Java/展示/算法接口
- ✅ 图谱：未写 nGQL

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 15000 |
| model_used | glm-5.3 |
| actual_cost | 0.08 |
| cost_warn | green |

本会话不改 task-registry，上表不回写注册表。数字是估算。

## CI/CD

- 分支：`lumen-algo-py` `dev` 已推送（commit `0942212`，merge 后远端顶端 `a527c42`）
- 库：`10.50.11.76:3306` 的 `gkxlumenx_gapfill` 两张表已灌入
- pipeline：本单不跟发布
- 部署：无

## 未做的事

- 未把任务标成 done，状态仍是 `in_progress`
- 未改读取接口。读表是 `gkxlumen-element` 的事
- 未改架构稿、DATA、说明书、注册表
- 未碰同仓另一会话的 shell/scheme 灌数产物（只让位 pull 后随远端合入）
