# POLICY-METRIC-OPEN-L01 · 政策维度指标语义 + 开放项核对

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:王惠` |
| dual_sign | `human:王惠` + `human:唐绍祖`（方案 B） |
| claim_type | `pull` |
| collaborators | `data-agent`（贴源核对） |

## 范围与实现

对照 E7 + DS10-12 产品包中的 `M_POLICY_*` 引用，完成五件套第 4–5 项定义真源：

| DoD | 产物 | 状态 |
|-----|------|------|
| METRIC-OPEN 核对记录 | `产品整体定义/METRIC-OPEN-E7-DS10-12-核对记录.md` | ✅ |
| 算法定义卡 | `metrics/registry/metric-spec-POLICY.yaml` | ✅ |
| cfg_metric 核对更新 | `metrics/registry/cfg_metric-POLICY-seed.yaml` → seed_version **0.2.0** | ✅ |
| data-gap-catalog | `产品整体定义/POLICY-data-gap-catalog.yaml` | ✅ |
| QPOL-01~07 状态更新 | `客户决策清单跟踪表.md` §2.aa 落地列 | ✅（保持 🟡） |

## 偏离说明

- 未将任何 QPOL 升 🟢（甲方未书面确认）。
- 12 条 🔧 POC formula 已存在于 polan，但 mapping_status **不升 ✅**（口径未闭合）。
- `M_POLICY_CONTINUITY_INDEX` 未在 seed 独立注册；暂并 TIMESERIES（GAP 已记）。

## 验收证据

- 19/19 metric 进入 gap catalog，与 seed 状态分布一致（✅4/🔧12/⚠️3）
- 定义卡含 7 个模型 + 基础指标 + QPOL-02 三处权重冲突登记
- 双签区留白，待王惠/唐绍祖签署

## 架构合规自检

| # | 铁律 | 结论 |
|---|------|------|
| 1 | 算法只在 Python | ✅ 定义卡指向 polan，无前端公式 |
| 2 | 调用链 | ✅ ADS / Java 只读声明 |
| 3 | 图谱 Nebula | ✅ 关联度经 Python 图谱，非 Neo4j |
| 4 | 可观测性 | ✅ 定义包 N/A |
| 5 | CI/CD | ✅ 无业务仓 rollout 要求 |
| 6 | demo2 不 merge lumen | ✅ 未改业务仓 |
| 7 | 共享聚合 | ✅ Java 只读 ADS |
| 8 | ADS/Mock | ✅ mapping 不升绿 |
| 9 | Design.md | ✅ N/A（无 UI） |
| 10 | D9 血缘 | ✅ 8 件套 + Pending 文案 |
| 11 | D10 | ✅ N/A（无交互稿） |
| 12 | D12 | ✅ 未改 lumen 前端 |
| — | 不替甲方拍板 | ✅ 全部 🟡 保留 |

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 72000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 2.0 |
| cost_warn | green |

## 建议下一状态

definition → **integration**（会签）；签署后可支撑政策维度门 1「有条件闭合」。
