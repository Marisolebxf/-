# LUMEN-INTEL-ELEM-DDL-L01 · handoff

- 任务：综合智能分析要素 — 当前 8 张 ADS 表 DDL+预填
- Epic：E8-综合智能分析 ｜ 执行：agent:data-agent ｜ 监管：human:徐滕强
- 仓：`repos/lumen-algo-py`（origin/dev，commit `745cd9d`，**未 push**——coordinator 统一推）
- 日期：2026-11-05
- 强度：ponytail full

## 1. 范围与实现（对照 ELEM 册 v1.0.6 §2 / 总册 v1.0.6 §11）

| 册要求 | 实现 |
|---|---|
| 当前必建 8 张 ADS（index/type_score/level_score/domain_score/indicator/weight/contrib/rank）落 `demo_gkxlumenx_ads` | ✅ `scripts/mysql/synth_elem.sql`：8 张 CREATE TABLE IF NOT EXISTS，逐张按册 §2 表名/粒度/唯一键核对 |
| 唯一键基础键 = region+compare+window + `calc_batch_id`；type/level 另含 `metric_id`+维度码 | ✅ 8 个 `uk_*` 全含四元组；type/level 加 `metric_id`（INDEX/SCORE 两行同表不碰撞） |
| 公共列按总册 §11.2 | ✅ 15 列齐：metric_id/region_code/region_name/compare_scope/window_label/year/period_key/value_num/value_json/calc_batch_id/calc_batch_created_at/calc_status/is_mock/method_version/generated_at |
| 每表 COMMENT 登记血缘 | ✅ 8 张表 COMMENT 均含 主 metric_id + calc-logic 源表清单 + 源系统 |
| `synth_elem_four_dim_score` 不建 | ✅ 脚本内无该表；`--check` 断言禁四维表 |
| 写入方式：整批写（AR-6 跨表同批一致） | ✅ seed 同 `calc_batch_id=mock_20261105_elem_seed` 同 `calc_batch_created_at` 一事务写 8 表，任一步失败整批 rollback |
| 预填默认三元组、is_mock=1、批次 succeeded | ✅ 深圳×全国重点城市（四城盘：深/广/莞/惠）×最近3年（基期 2024）；is_mock=1、calc_status=succeeded |
| 读取语义：只认 succeeded 最新批（按 calc_batch_created_at） | ✅ 条件索引 `idx_cond` + `idx_batch_created`；SQL 头部登记读取口径 |
| AR-4 批次清理任务定义 | ✅ 写入 DDL 头注释（每 24h 按 calc_batch_created_at 保 3 个 succeeded 批、failed/running 超 7 天清、保护引用批；owner data-agent，执行属运维单，不另开表） |

预填数值全部冻结自 calc-logic 复现盘正本（`agent-delivery/metrics/calc-logic/SYNTH/M_SYNTH_ELEM_*.md`）：
- 综合指数 77.6829/45.8001/31.3832/15.4755（等权 1/3×3，VALUE 附录 B.1）
- 类型维 6 维 z 值+17 叶子台账（TYPE_INDEX §2.2/2.4，人才维整维 null 不补 0）
- 层次结构分+成熟度/均衡度（LEVEL_INDEX §2.3/2.4；n=1 结构 balance 恒 60）
- 领域五维（DOMAIN_INDEX §2.4；D4/D5 维 null）
- 贡献 8 格份额（CONTRIB §2.6/2.7；TAL/FUN 成果侧缺行 null+note，B 口径标识；非因果）
- 权重等权 0.33333333×3（WEIGHT 正本；`main_is_official=false`、Q-SYNTH-E-01 🟡，由 is_mock=1 承载）

## 2. 偏离说明

1. **DoD 文案 10 张 → 实作 8 张**：registry DoD 字段串残留 `_ai` 旧口径（`type`/`type_score`、`level`/`level_score` 分列=10 个名字）；按 ELEM 册 v1.0.6 §2「当前 8 张」与任务标题口径收敛——type_score/level_score 各以 `metric_id` 承载 INDEX+SCORE 两行。非设计变更。
2. **业务口径列与公共 value 列并存**：weight/contrib/indicator/rank 的真值在业务列（weight_value/share/raw_value+score/rank_no），公共 `value_num`/`value_json` 置 NULL，DDL 列注释登记「口径见 XX 列防双源」——册 §2「value_num 装指数」按各表口径落地，装包读业务列。
3. **index 表 `weight_profile_code` 不入唯一键**：册 §2 唯一键列清单未含权重方案；等权为唯一方案（EQUAL），后续多方案需改键时另评审。
4. **正式库 DDL 未执行**：结构一致注释给出（`demo_gkxlumenx_ads`→`gkxlumenx_ads` 前缀替换），由 DBA 正式环境执行；本单禁写正式库（铁律）。

## 3. 产物清单

| 文件 | 说明 |
|---|---|
| `scripts/mysql/synth_elem.sql` | 8 张 ADS DDL（幂等 CREATE IF NOT EXISTS；头部登记库落点/公共列/读取口径/AR-4 清理定义；正式库前缀替换说明） |
| `scripts/seed/seed_synth_elem.py` | DDL+seed 一条命令：`--check`（离线自检）/`--apply`（建表+同批整写+验证）；同批先删后插幂等 |
| `agent-delivery/agent-handoffs/LUMEN-INTEL-ELEM-DDL-L01.md` | 本 handoff |

commit：`745cd9d feat(synth-elem): 8张ADS表DDL+预填seed [agent:data]`（2 files，+646；未 push）

## 4. 验收证据（demo 库 10.50.11.76 实跑）

`--check`（离线）：

```
{"mode": "check", "ok": true, "tables": 8, "rows": {"synth_elem_index": 1, "synth_elem_type_score": 52,
 "synth_elem_level_score": 52, "synth_elem_domain_score": 20, "synth_elem_indicator": 108,
 "synth_elem_weight": 3, "synth_elem_contrib": 32, "synth_elem_rank": 4}}
```

`--apply`（实跑 DDL+seed，一事务）：

```
{"mode": "apply", "connected": true, "db": "demo_gkxlumenx_ads", "batch": "mock_20261105_elem_seed",
 "rows": {"synth_elem_index": 1, "synth_elem_type_score": 52, "synth_elem_level_score": 52,
 "synth_elem_domain_score": 20, "synth_elem_indicator": 108, "synth_elem_weight": 3,
 "synth_elem_contrib": 32, "synth_elem_rank": 4}, "problems": [], "ok": true}
```

验收查询（行数>0、唯一键无冲突、is_mock=1、批次字段齐）：

```
synth_elem_index:         total=1   batch=1   bad_flags=0 uk_dup=0
synth_elem_type_score:    total=52  batch=52  bad_flags=0 uk_dup=0
synth_elem_level_score:   total=52  batch=52  bad_flags=0 uk_dup=0
synth_elem_domain_score:  total=20  batch=20  bad_flags=0 uk_dup=0
synth_elem_indicator:     total=108 batch=108 bad_flags=0 uk_dup=0
synth_elem_weight:        total=3   batch=3   bad_flags=0 uk_dup=0
synth_elem_contrib:       total=32  batch=32  bad_flags=0 uk_dup=0
synth_elem_rank:          total=4   batch=4   bad_flags=0 uk_dup=0
index latest succeeded: ('深圳市', 77.6829, 'succeeded', 2026-11-05 20:00)
weights: EQUAL 0.33333333 ×3 (type/level/domain), is_mock=1
```

幂等重跑验证：`--apply` 连跑两次，8 表行数不变（同批先删后插，无重复无残留）。

## 5. 架构合规自检（公约 §2 铁律）

| 铁律 | 自检 |
|---|---|
| 1 算法只在 Python | ✅ 本单纯 DDL/Python seed；无 Java 算法 |
| 2 调用链 | ✅ 未动接口；8 表消费方=entan-py 装包（ELEM-PY 单）+Java 只读 ADS |
| 3 NebulaGraph | N/A（无图谱） |
| 4 可观测性 | N/A（数据脚本；装包侧日志属 ELEM-PY 单） |
| 5 CI/CD | ✅ 仅本地 commit 未 push（coordinator 统一推） |
| 6 demo2 只读 merge | N/A（未动 demo 仓） |
| 7 共享聚合核心 | ✅ ADS 标准表，Java 只读 |
| 8 ADS 先行+Mock | ✅ ADS 落点、is_mock=1 |
| 9 D8 前端规范 | N/A |
| 10 D9 血缘 | ✅ metric_id 齐；表 COMMENT 血缘（源表/源系统）；D4 仍 mock（诚实，不伪闭合） |
| 11 D10 交互规范 | N/A |
| 12 D12 demo/lumen 隔离 | ✅ 只写 `demo_gkxlumenx_ads`；正式 `gkxlumenx_ads` 仅注释说明未执行 |
| 13 D14 对象存储 | N/A |
| 14 D16 gapfill 边界 | ✅ 未建 gapfill 表；结果落 ADS，符合 D18/D16 分工 |
| 15 D17 合规算法 | ✅ 未触碰唐绍祖锁定闭包；表名/指标名未改 |
| 16 D18 签收条件 | ✅ 新建 ADS 表 + Python 灌 mock 行（非接口写死 mock）；四维 blocked 不建表不出数 |

## 6. ponytail 自检

ponytail: full——最小交付两文件（DDL+seed 合一脚本，复用仓内 seed 模式与连接配置）；自检=脚本自带 `--check` 离线断言（表清单/唯一键含批次/无四维表/行数/份额和）+ `--apply` 内建验证查询；无新依赖（pymysql 仓内已用）；无新建框架。

## 7. cost（按 budget-estimate.md 四字段）

| 字段 | 值 |
|---|---|
| actual_tokens | ~110000 |
| model_used | glm-5.3-Flash（Cursor 内） |
| actual_cost | ~$0.15 |
| cost_warn | false（< $10 阈值） |

## 8. 后续依赖（不属本单）

- 装包 elements 分支只读 8 表（`vendor/entan-py`，线 2 归属）；四维固定 `[]+reason=metric_not_registered`
- 正式库 `gkxlumenx_ads` DDL 执行属 DBA；AR-4 清理任务执行属运维单
- 全景（136）无表（真实 DWD 汇聚，装包内实现，AR-8 timeout 降级）
