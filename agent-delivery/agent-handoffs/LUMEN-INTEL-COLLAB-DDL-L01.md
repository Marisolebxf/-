# LUMEN-INTEL-COLLAB-DDL-L01 · handoff

- 任务：综合智能分析协同 — ADS 表 DDL+预填
- Epic：E8-综合智能分析 ｜ 执行：agent:data-agent ｜ 监管：human:徐滕强
- 仓：`repos/lumen-algo-py`（origin/dev，commit `b778c07`，**未 push**——coordinator 统一推；`fe-manual-confirm-push` 不适用本仓，任务文亦明示不 push）
- 日期：2026-11-05
- 强度：ponytail full

## 1. 范围与实现（对照 COLLAB 册 v1.0.8 §2 / 总册 v1.0.6 §11.2–11.3 / 签收单 AR-4/AR-9/AR-10）

| 册要求 | 实现 |
|---|---|
| 指标 4 张 ADS（index/network_stat/relation_input/output_corr）落 `demo_gkxlumenx_ads` | ✅ `scripts/mysql/synth_collab.sql` 1–4/8 张；唯一键=基础键（region+compare+window+`calc_batch_id`），network_stat `+stat_type`、relation_input `+relation_type`、output_corr `+(x_metric_id,output_metric_id,period_start,period_end)` |
| output_corr 列对齐 calc-logic（v0.5） | ✅ `x_metric_id/output_metric_id/r_value/sample_n/status(sufficient\|insufficient)/reason` 五列齐；`n<3` 存合法 `insufficient` 行（非 failed 批）；表 COMMENT 登记「Pearson 区域×年配对、禁跨区域截面、零方差 insufficient」 |
| 本期 0 行口径（v1.0.7：源无年） | ✅ index/network_stat/output_corr 三表留空（读取侧 null+`reason=no_year_on_source`）；cluster 空表（C-02 前不派生，`clusters=[]`+`cluster_rule_unclosed`）；node/edge 空表且禁灌演示行——空态=读表结果非接口写死，D18 合规 |
| relation_input 预填演示行（is_mock=1） | ✅ 默认三元组 3 行（co_patent/co_project/talent_flow），数值冻结自 `metrics/repro/out/M_SYNTH_COLLAB_RELATION_INPUT_out.json` 正本（全国事件级 2026-10-22 快照）；`M_SYNTH_COLLAB_RELATION_INPUT` 五码含入（canonical 唯一源） |
| 空表 batch_meta + 图事实 node/edge（ADS，不进 gapfill） | ✅ 5–8/8 张；batch_meta `uk(snapshot_id)`+`idx(cache_key,is_latest)`；node/edge `uk(...含 metric_id+graph_batch_id)`；未建任何 `gapfill_synth_collab_*` |
| batch_meta 列集（COLLAB 册 §2） | ✅ snapshot_id/calc_batch_id/graph_batch_id/cache_key/region/compare/window/published_at/is_latest 九列；AR-9「is_latest 翻转同事务」写入列注释与表 COMMENT |
| AR-10 豁免与映射 | ✅ DDL 头注释+表体注释双登记：豁免 metric_id/calc_batch_created_at/calc_status/is_mock/method_version/generated_at；region/compare/window≈region_code/compare_scope/window_label；published_at≈generated_at |
| 公共列（总册 §11.2） | ✅ 7 张表 15 公共列齐；`synth_collab_edge` 按 v1.0.6「边去掉 year」豁免 year/period_key（列注释注明） |
| 每表 COMMENT 血缘 | ✅ 8 张表 COMMENT 均含 metric_id/calc-logic 式或源表/源系统；relation_input 注明「canonical 唯一源，图谱只读本表 metric_id 行」 |
| 读取口径：succeeded 最新批按 calc_batch_created_at | ✅ 条件索引 `idx_cond`+`idx_batch_created`；SQL 头注释登记（禁 calc_batch_id 字符串比大小） |
| AR-4 批次清理任务定义 | ✅ DDL 头注释（每 24h 按 calc_batch_created_at 保 3 个 succeeded 批；failed/running 超 7 天清；**删除前检查 batch_meta 引用：被引用 calc_batch_id/graph_batch_id 及关联行跳过保护**；owner data-agent，执行属运维单，不另开表） |
| 写入方式：整批写（AR-6 同批一致） | ✅ seed 同 `calc_batch_id=mock_20261105_collab_seed` 同 `calc_batch_created_at` 一事务写；失败整批 rollback |

## 2. 偏离说明

1. **任务文「7 张 DDL / 空表 3 张」→ 实作 8 张 DDL / 空表 7 张**：按铁律「表清单以册 §2 为准逐张核对」——册 §2 表清单=指标 4 + cluster + batch_meta + node + edge=**8 张**（node/edge 算 2 张，空表实际 7 张）；任务文数字为笔误（其自身括注「node/edge 算 2 张，合计空表实际 4 张」已自相矛盾，以册为准）。非设计变更。
2. **registry DoD `gapfill_synth_collab_{node,edge}` 不建**：DoD 文案残留 v1.0.4 旧口径（gapfill 图）；v1.0.5 会签退回已改「指标与图改落 ADS、废止 gapfill 图」，总册 §11.3 同步「废止 gapfill_synth_collab_node/edge」。`--check` 断言禁止 gapfill 表（符合 D16/D18 边界）。
3. **registry 标题「_ai 5 张 + gapfill 2 张」为旧库口径**：v1.0.5 已废止 `gkxlumenx_ai` 与 gapfill 图落点，任务 note 与 SIGNOFF AR-1 同款文档同步问题；实作按册 §2 ADS 落点。
4. **relation_input 的 `window_label` 取默认窗「最近3年」仅作条件键归位**：该指标实为全历史累计口径（源无年），册 §2 写入策略明令「不把全历史计数抄进 1y/3y/5y」——冲突消解：行保留（canonical 源供图谱与输入盘点读），`value_json.caliber='全历史累计'`+`source_has_year=false` 披露口径，装包/图谱按 canonical 读行不按窗复制截面；1y/3y/5y 窗语义由 node/edge（0 行）与 batch_meta 承载。若装包实现单判定该行不应落默认窗，删行即可（空表方案兼容）。
5. **output_corr 本期 0 行**：册 §2 写入策略「n<3 存为合法 insufficient 行」指**实算时**的行为契约（DDL 列与 COMMENT 已支持）；本期年度序列未落盘（C-05），无任何可算行，按册「图空则不灌数/留空表+注释」执行，不编 insufficient 演示行。
6. **正式库 `gkxlumenx_ads` DDL 未执行**：结构一致（demo 前缀替换），由 DBA 正式环境执行；本单禁写正式库。

## 3. 产物清单

| 文件 | 说明 |
|---|---|
| `scripts/mysql/synth_collab.sql` | 8 张 ADS DDL（幂等 CREATE IF NOT EXISTS；头部登记库落点/公共列/AR-10 豁免/读取口径/AR-4 清理定义；正式库前缀替换说明） |
| `scripts/seed/seed_synth_collab.py` | DDL+seed 一条命令：`--check`（离线断言）/`--apply`（建表+灌 relation_input 3 行+验证）；同批先删后插幂等；复用 seed_synth_elem.py 连接/事务模式 |
| `agent-delivery/agent-handoffs/LUMEN-INTEL-COLLAB-DDL-L01.md` | 本 handoff |

commit：`b778c07 feat(synth-collab): 协同ADS表DDL+预填seed [agent:data]`（2 files，+484；未 push）

## 4. 验收证据（demo 库 10.50.11.76 实跑）

`--check`（离线）：

```
{"mode": "check", "ok": true, "tables": 8, "seeded": {"synth_collab_relation_input": 3},
 "empty": ["synth_collab_index", "synth_collab_network_stat", "synth_collab_output_corr",
           "synth_collab_cluster", "synth_collab_batch_meta", "synth_collab_node", "synth_collab_edge"]}
```

`--apply`（实跑 DDL+seed，一事务）：

```
{"mode": "apply", "connected": true, "db": "demo_gkxlumenx_ads", "batch": "mock_20261105_collab_seed",
 "rows": {"synth_collab_index": 0, "synth_collab_network_stat": 0, "synth_collab_relation_input": 3,
          "synth_collab_output_corr": 0, "synth_collab_cluster": 0, "synth_collab_batch_meta": 0,
          "synth_collab_node": 0, "synth_collab_edge": 0}, "problems": [], "ok": true}
```

验收查询（明细 / 唯一键零冲突 / is_mock / 批次字段）：

```
('co_patent',   6477.0000, '"全历史累计"', is_mock=1, succeeded, mock_20261105_collab_seed)
('co_project',     0.0000, '"全历史累计"', is_mock=1, succeeded, mock_20261105_collab_seed)
('talent_flow', 18553.0000, '"全历史累计"', is_mock=1, succeeded, mock_20261105_collab_seed)
uk_dup=0（uk_collab_rel_input 五元组 GROUP BY HAVING COUNT(*)>1 → 0）
```

- 空表确认：index/network_stat/output_corr/cluster/batch_meta/node/edge 全部 `COUNT(*)=0`（apply 内建断言，problems=[]）。
- 幂等重跑：`--apply` 连跑两次行数不变（同批先删后插，无重复无残留）。
- 断言覆盖：表清单=册 §2 顺序 8 张、指标 7 表唯一键含 calc_batch_id、node/edge 唯一键含 graph_batch_id、batch_meta `uk(snapshot_id)`、无 gapfill 表、edge 表体无 year/period_key、三类关系行齐、co_project=0 合法实测值。

## 5. 架构合规自检（公约 §2 铁律）

| 铁律 | 自检 |
|---|---|
| 1 算法只在 Python | ✅ 本单纯 DDL/Python seed；无 Java 算法 |
| 2 调用链 | ✅ 未动接口；8 表消费方=entan-py 装包/图谱（COLLAB-PY 单）+Java 只读 ADS |
| 3 NebulaGraph | N/A（本期图谱读 ADS 事实表，不做 Nebula 导出，COLLAB 册 §1） |
| 4 可观测性 | N/A（数据脚本；装包侧日志/batch_meta 回显属 COLLAB-PY 单） |
| 5 CI/CD | ✅ 仅本地 commit 未 push（coordinator 统一推） |
| 6 demo2 只读 merge | N/A（未动 demo 仓） |
| 7 共享聚合核心 | ✅ ADS 标准表，Java 只读 |
| 8 ADS 先行+Mock | ✅ ADS 落点；relation_input is_mock=1；其余 7 张诚实空表 |
| 9 D8 前端规范 | N/A |
| 10 D9 血缘 | ✅ metric_id 齐；表 COMMENT 血缘（源表/源系统）；D4 仍 mock（诚实，不伪闭合） |
| 11 D10 交互规范 | N/A |
| 12 D12 demo/lumen 隔离 | ✅ 只写 `demo_gkxlumenx_ads`；正式 `gkxlumenx_ads` 仅注释说明未执行 |
| 13 D14 对象存储 | N/A |
| 14 D16 gapfill 边界 | ✅ 未建任何 gapfill 表（v1.0.5 已废止 gapfill 图）；结果落 ADS，符合 D16/D18 分工 |
| 15 D17 合规算法 | ✅ 未触碰唐绍祖锁定闭包；表名/指标名未改 |
| 16 D18 签收条件 | ✅ 新建 ADS 表 + Python 灌 mock 行（仅 relation_input 3 行）+ 其余读表空态（非接口写死 mock）；D4 仍 mock |

## 6. ponytail 自检

ponytail: full——最小交付两文件（DDL+seed，复用仓内 seed_synth_elem.py 连接/幂等/事务模式，不另起框架）；自检=脚本自带 `--check` 离线断言 + `--apply` 内建验证查询；无新依赖（pymysql 仓内已用）；无建多余表（registry DoD 的 gapfill 2 张按 v1.0.5 口径**不建**即最小交付）。

## 7. cost（按 budget-estimate.md 四字段）

| 字段 | 值 |
|---|---|
| actual_tokens | ~105000 |
| model_used | glm-5.3-Flash（Cursor 内） |
| actual_cost | ~$0.14 |
| cost_warn | false（< $10 阈值） |

## 8. 后续依赖（不属本单）

- 装包 collaboration 分支（`vendor/entan-py`，COLLAB-PY 单）：读 4 张指标表（本期 index/network_stat 三窗 null+`no_year_on_source`、output_corr 空态）；图谱只读 relation_input canonical 行；发布成功写 `synth_collab_batch_meta`（AR-9：is_latest 翻转同事务）；不派生 cluster
- 图谱接口（Java 门面+Python）：按 §3.2 契约，本期返回空图 `reason=no_year_on_source`
- 正式库 `gkxlumenx_ads` DDL 执行属 DBA；AR-4 清理任务执行属运维单
- C-05 换源解锁后：实算写入 node/edge/指标行，非空验收移 `COLLAB-C05-SRC`
