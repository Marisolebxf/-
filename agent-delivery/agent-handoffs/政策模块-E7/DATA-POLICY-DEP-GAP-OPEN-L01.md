# DATA-POLICY-DEP-GAP-OPEN-L01 · 三个缺失依赖登记为开放项

## 任务认领

| 字段 | 值 |
|---|---|
| task_id | `DATA-POLICY-DEP-GAP-OPEN-L01` |
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| repo / branch | `gkx-orchestration` / `origin/dev` |
| depends_on | `DATA-POLICY-STORAGE-S3-GAP-L01`（≥ ready_to_sign） |

## Ponytail

- ponytail: `full`
- 三项登记进 `01-data-flow.md` §5 **既有开放项表**，未另建 gap 清单文件（本域已有 OPEN-POLICY-* 命名体系，再开一份就是第二真源）。
- §5.1 只写「受影响指标 / seed 声明 / as-built 做法 / 风险」四列，不展开解决方案设计。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | **无**。只在 §5 开放项登记缺口，拓扑与施工范围未变，不翻签。 |
| 会签态 | `approved`（`human:淮政玮` · 2026-08-21）维持 |

## 缺口来源

2026-08-31 对政策 17 个指标做「定义完整性 + 存储支撑」核查时发现：三个对象被 seed 的 `source_tables` 声明为依赖，但 POLICY 存储树里没有对应设计，`polan` 也没有实现。属于**声明与实现两头都缺**，此前无任何登记。

## 修改内容

`storage/POLICY/01-data-flow.md` §5 新增三行开放项 + 新增 §5.1 说明表：

| ID | 缺失对象 | 受影响指标 | Owner |
|---|---|---|---|
| `OPEN-POLICY-DIM-01` | `dim.region`（省级 / 深圳区县映射） | `M_POLICY_NATIONAL_DIST` · `M_POLICY_SZ_DIST` | data-agent |
| `OPEN-POLICY-DIM-02` | 专家策略库维表 | `M_POLICY_LAYOUT_REC_COUNT` | `human:淮政玮`（随 QPOL-02） |
| `OPEN-POLICY-XDOM-01` | `dwd.industry_chain`（跨域） | `M_POLICY_INDUSTRY_COVERAGE` | data-agent |

§5.1 逐项写明 as-built 现状与风险，并钉死「补齐对象」与「改 seed 源表为 as-built 做法」二选一、不得并存。

**未改**代码、**未**建表、**未**改 seed（seed 属 `DATA-POLICY-METRIC-REGISTRY-FIX-L01` 范围，且当前被阻塞）。

## 验收证据

| 结论 | 来源 |
|---|---|
| seed 声明 `dim: dim.region` | `M_POLICY_NATIONAL_DIST` / `M_POLICY_SZ_DIST` 的 `kit.source_tables`（经 `scripts/lib/metric-registry-lib.mjs` `getMetric` 读出，未直读 YAML） |
| as-built 无维表、直接按 region 字符串聚合 | `polan/basic/indicators.py` A4/A5 实现 |
| seed 声明 `dwd.industry_chain（跨域产业链维表）` | `M_POLICY_INDUSTRY_COVERAGE` 的 `kit.source_tables` |
| 产业侧实际取 `related_entities.industry` / `ext5` | `polan/graph/entity.py` L113 |
| seed 声明「专家策略库（待补维表）」 | `M_POLICY_LAYOUT_REC_COUNT` 的 `kit.source_tables` |
| `layout` 仅融合机遇 + 短板 | `polan/eval/layout.py` L31/L35 读 `policy_focus` + `policy_effect` |

无 CI（定义叶）。

## 顺带核实（不属本叶改动）

「政策总数是否含国际政策」经查**已登记**为 `QPOL-05`「国内/国际政策是否合并入统计及归一化」，临时默认「仅统计国内；国际单列不进综合池」，状态 🟡 待甲方。seed 的 13 条源表只引国内表，与该临时默认一致，**不是遗漏**。本叶不重复登记，避免决策表出现平行条目。

## 遗留风险

- 三项均需 `human:淮政玮` 定向后才能进入施工或改口径，本叶只登记不推动。
- `OPEN-POLICY-DIM-01` 若选「改 seed 为 as-built」，须同时在口径里写明按字符串聚合的降级与漂移风险，否则等于把缺陷洗白。
- `OPEN-POLICY-XDOM-01` 涉跨域，需与 CHAIN 域约定读法，单域无法闭合。

## CI/CD

- 分支：`gkx-orchestration` `origin/dev`
- commit：待提交（`[agent:data-agent]`）
- pipeline / K8s：N/A（编排仓文档叶）

## 涉及文件

- `agent-delivery/data/data-design/storage/POLICY/01-data-flow.md`

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 零代码改动 |
| 调用链 / D12 | ✅ 未涉及 |
| 图谱 Nebula 一张 G | ✅ 未动图 |
| 无闸门不写正式库 | ✅ 本叶不建表不灌数 |
| D9 血缘 | ✅ 三项缺口显式登记，未伪闭合 |
| 指标真源纪律 | ✅ 未直读 / 未改 `registry/` YAML；查询走 lib 只读函数 |

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 39000 |
| model_used | claude-opus-4.6 |
| actual_cost | 0.51 |
| cost_warn | green |
