# 派单包：ENT-MOD-RISK-V1-HIFI

- **派单方**：coordinator（用户指示「逐个执行」）
- **时间**：2026-07-22
- **执行 Agent**：`ui-agent`
- **监管**：`human:高颖`（Agent 会话）
- **HIFI 共决**：`human:高颖` + `human:孔东`（2026-07-22 起；勿再派许丹丹/望淋莉）
- **Sprint**：2026-W30
- **上游**：`ENT-MOD-RISK-PACK-L01` ✅ done · `ENT-MOD-RISK-METRIC-OPEN-L01` ✅ done
- **并行注意**：同仓 `demo-ui-topic` 上 `ENT-MOD-EVAL-V1-HIFI-R1` 仍在跑；本任务只动 `EnterpriseRiskInsight*` / `riskInsight*`，勿改评估页

## 1. 目标

对已有风险洞察 Demo 完成 **V1 首轮会签**（非最终冻结），产出：

- `agent-handoffs/产品整体定义/E-28_E-29-风险洞察/UI-HIFI-ENT-RISK-R1-会签单.md`（H-01～H-08）
- 版本号建议：`HIFI-ENT-RISK-medium-r1`

## 2. 范围页面

| 路由族 | 组件 / 模块 |
|--------|-------------|
| `/enterprise-center/...` 风险洞察 | `EnterpriseRiskInsightPage.tsx`、`RiskInsightSupplyResult.tsx`、`RiskInsightPainResult.tsx`、`riskInsight*.ts` |

须覆盖两模式：**供应链关系分析**、**企业发展痛难点识别**；配置、处理中、结果、历史、报告；默认/加载/空/错/无权限/数据缺失/低可信。

## 3. 输入

- `E-28_E-29-风险洞察/` 四件套
- `METRIC-OPEN-ENT-RISK-核对记录.md` + `ENT-RISK-data-gap-catalog.yaml`
- `Design.md` §4–§7、§14；D10 交互规范 §19
- Q017/Q018 保持 🟡，挂 PendingBadge，不伪闭合

## 4. Definition of Done

1. UI-HIFI-ENT-RISK-R1-会签单齐备，H-01～H-08 无阻断 ❌  
2. 与对比篮分析类型分发契约一致（只承接供应链/痛难点）  
3. `npm run design:check` 与 `npm run build`（本模块相关失败须说明）  
4. handoff + 高颖首轮会签；**不**宣告最终冻结  

## 5. 认领话术

```text
/goal ENT-MOD-RISK-V1-HIFI
监管：human:高颖
HIFI 共决：human:高颖 + human:孔东
仓：demo-ui-topic（main）
必读：ENT-MOD-RISK-V1-HIFI-派单包.md + E-28_E-29-风险洞察 四件套 + Design.md
交付：UI-HIFI-ENT-RISK-R1-会签单.md + Demo commit SHA
Convoy：勿改 EnterpriseEvaluation*（EVAL-V1 并行）
```
