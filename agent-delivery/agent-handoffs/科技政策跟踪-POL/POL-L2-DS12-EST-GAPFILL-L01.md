# POL-L2-DS12-EST-GAPFILL-L01 · 效果预估预测缺项表灌数

ponytail: full

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | 注册表已由淮政玮认领并处于 `in_progress`。本会话不改 task-registry，不把任务标成 done |
| 说明 | 执行角色 `agent:data-agent`。只提交 `lumen-algo-py` 本地 commit，不 push |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 `seed_gapfill_policy_eval_template.py` 的 `--check` / `--apply` 与单表 SQL 覆写。未另起框架。未用 YAGNI 跳过 D16 列 |

## 范围与实现

真源是 `sdd/l2/POL-L2-DS12-EST-DATA.md` 第 2–5 节。只建并准备灌库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_forecast`。不写 ODS、DWD、ADS、供应方库。不灌 235、236。不建解析表，不写文件。不改 D4，不新造 `metric_id`。

| 行种类 | 行数 | `gap_item` | `metric_id` |
|---|---|---|---|
| 未出台仿真 | 2 | `232 未出台政策仿真模拟` | `M_POLICY_SIMULATE` |
| 新出台预测 | 2 | `233 新出台政策效果预测` | `M_POLICY_SIMULATE` |
| 区域空间 | 2 | `234 区域经济发展空间模拟` | `M_POLICY_SIMULATE` |

合计 6 行。每行 `is_mock=1`，`fill_method=manual`，`gapfill_batch_id=POL-L2-DS12-EST-GAPFILL-L01`，`generated_at=2026-11-06 01:00:00`。用不到的列是 NULL，不是空串。

未出台仿真两行的四参数不同：研发补助 × 广东省高新技术企业 × 按研发投入的20%补助 × 2026年至2028年；人才引进 × 深圳市重点实验室 × 每人每年30万元 × 2027年至2029年。每行有经济效益、社会影响、创新促进、逐年趋势、一句解释。

新出台预测的 `policy_id` 复用 `scripts/seed_gapfill_policy_cmp.py` 里已出现的 `18363390`、`18407696`。同一 `policy_id` 一行。不设颁布日期截断。`policy_title` 是展示短名（广东省科技型中小企业研发环境支持；深圳市外国人来华工作许可），不是从政策正文复制的正式标题。

区域空间两行：广东省 × 研发补助；深圳市 × 人才引进。没有名为「全国」的行。不存地图文件。`spatial_items` 是更细区域名和数值的展示原文。

## 偏离

| 偏离 | 理由 | as-built |
|------|------|----------|
| `--apply` 未连上库 | 本会话环境没有 `LUMEN_ALGO_MYSQL_PASSWORD`。不改连接信息，不把口令写入 git | SQL 已落盘。有口令后同一条 `--apply` 可建表灌数 |
| `policy_title` 不是目录正式标题 | 本仓种子只有业务键，没有这两条政策的正式标题。DATA 要求名称只供展示、不复制正文 | 展示短名来自 cmp 种子里这两条键的申报说明缩写 |

## 产物清单

- `repos/lumen-algo-py/scripts/seed_gapfill_policy_sim_forecast.py`
- `repos/lumen-algo-py/scripts/mysql/gapfill_policy_sim_forecast.sql`
- 本 handoff（只在编排仓工作区，未提交）

本地 commit：`04ce9b4bf9a34b35231d76905b9388a22d96947f`。未 push。

## 验收证据

在 `repos/lumen-algo-py` 执行（PowerShell，不用 `&&`）：

```
python scripts/seed_gapfill_policy_sim_forecast.py --check
```

退出码 0：

```
{"mode": "check", "ok": true, "db": "gkxlumenx_gapfill", "rows": {"gapfill_policy_sim_forecast": 6}, "sql": "E:\\zhipu\\gkx-lumen\\repos\\lumen-algo-py\\scripts\\mysql\\gapfill_policy_sim_forecast.sql"}
```

```
python scripts/seed_gapfill_policy_sim_forecast.py --apply
```

退出码 2：

```
{"mode": "apply", "connected": false, "reason": "no password"}
```

`--check` 锁住：三种 `row_kind` 闭集且各 2 行；每种必填列有值、其余业务列为 NULL；未出台四参数唯一；新出台 `policy_id` 唯一且等于上述两个业务键；区域 `region_name`×`policy_type` 唯一；`metric_id` 只有 `M_POLICY_SIMULATE`；SQL 不出现文本解析、文件路径、`gkxlumenx_ads`、`gkxlumenx_ods`、`gkxlumenx_dwd`。

## 架构合规自检

- D16：脚本只准备写 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`，行上带规定追溯列
- 未写 ODS、DWD、ADS、供应方库，未改 `policy_text_parse`
- 未调用 `polan.text.parse.run`、`polan.text.simulate.run`
- 未改 D4，未新造 `metric_id`
- 未把布局推荐、评价方案、受众反馈、中台 `ads.policy_simulate` 拷进本表

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 40000 |
| model_used | grok-4.7 |
| actual_cost | 0.20 |
| cost_warn | green |

估算。本会话不回写注册表。

## CI/CD

- 分支：`lumen-algo-py` `dev`，本地超前 `origin/dev` 2、落后 14。未 pull，未 push
- commit：`04ce9b4bf9a34b35231d76905b9388a22d96947f`
- pipeline：未推送，无
- 部署：无

## 未做的事

- 未把任务标成 done
- 未改同仓他人未提交文件：`k8s/README.md`、`scripts/mysql/gapfill_policy_eval_template.sql`

## 总控推送

2026-11-06 三仓都落地后推 `lumen-algo-py` `origin/dev`。提交 `04ce9b4bf9a34b35231d76905b9388a22d96947f` 已在远端。`--apply` 仍未执行，表未灌进库。
