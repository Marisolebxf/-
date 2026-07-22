# 派单包：ENT-MOD-EVAL-V1-HIFI-R1

- **派单方**：coordinator
- **时间**：2026-07-21
- **执行 Agent**：`ui-agent`（监管 `human:高颖` · HIFI 共决 `human:高颖` + `human:孔东`）
- **Sprint**：2026-W30 stretch
- **上游**：`ENT-MOD-EVAL-PACK-L01` ✅ done
- **并行**：`ENT-MOD-EVAL-METRIC-OPEN-L01`（不互相阻塞）

## 1. 目标

对 **已有** demo 页 `EnterpriseEvaluation*` 完成 **V1 首轮会签**（非最终冻结），产出：

- `UI-HIFI-ENT-EVAL-会签单.md`（H-01~H-08）
- 版本号 **`HIFI-ENT-EVAL-medium-r1`**

## 2. 范围页面

| 路由 | 组件 |
|------|------|
| `/enterprise-center/evaluation` | `EnterpriseEvaluationPage.tsx`、`EnterpriseCapabilityEvaluation.tsx`、`EnterpriseEvaluationResultWorkspace.tsx` |

须覆盖三模式：**技术力 / 商业力 / 综合竞争力**；配置、处理中、结果、历史、空/错/无权限/数据缺失态。

## 3. 输入

- `E-23_E-24_E-30-企业评估/` 四件套
- `Design.md` §4–§7、§14 检查清单
- `PendingBadge.tsx` / `MetricSpecCard`（METRIC-OPEN catalog 就绪后挂 ⚠️，本会签可先 🟡 登记）

## 4. Definition of Done

1. **UI-HIFI-ENT-EVAL-会签单.md** 齐备，H-01~H-08 无阻断 ❌
2. wireframe 第 6 列 metric_id 与页面 ⓘ 一致
3. handoff + 高颖签字
4. **不**宣告 V1 最终冻结（冻结走 `ENT-MOD-EVAL-V1-FINAL`）

## 5. 认领话术

```text
/goal ENT-MOD-EVAL-V1-HIFI-R1
监管：human:高颖
HIFI 共决：human:高颖 + human:孔东
demo-ui-topic 企业评估页首轮会签；交付 UI-HIFI-ENT-EVAL-会签单.md
```
