# 派单包：ENT-MOD-RECRUIT-V1-HIFI

- **派单方**：coordinator（用户指示「逐个执行」）
- **时间**：2026-07-22
- **执行 Agent**：`ui-agent`
- **监管**：`human:高颖`（Agent 会话）
- **HIFI 共决**：`human:高颖` + `human:孔东`（2026-07-22 起）
- **Sprint**：2026-W30
- **上游**：`ENT-MOD-RECRUIT-PACK-L01` ✅ done（**PM 淮政玮 2026-07-22 评审通过**）
- **并行**：`ENT-MOD-RECRUIT-METRIC-OPEN-L01`（唐绍祖监管；不阻塞本 V1 首轮）
- **并行注意**：同仓错峰 `ENT-MOD-RISK-V1-HIFI` / `ENT-MOD-EVAL-V1-HIFI-R1`；本任务只动引育推荐相关页面

## 1. 目标

依据冻结的引育推荐核心产品包，在 `demo-ui-topic` 完成 **招引 / 培育** 两独立视图的 V1 高保真 Demo + 首轮会签：

- `agent-handoffs/产品整体定义/E-26_E-27-引育推荐/UI-HIFI-ENT-RECRUIT-R1-会签单.md`
- 版本号建议：`HIFI-ENT-RECRUIT-medium-r1`

## 2. 范围

- 一个二级页「引育推荐」下两个独立视图（全国招引 / 深圳培育）
- 筛选 → 显式执行分析 → 名单/排名 → 联动详情 → 报告与导出
- 状态：初始、分析中、成功、空结果、部分缺失、失败、无权限、报告/导出
- **禁止**：候选池、异步任务中心、历史资产、公式/权重编辑
- GAP-RECRUIT-* / Q015 显示 ⚠️，不伪造成正式数值

## 3. 输入

- `E-26_E-27-引育推荐/` 四件套
- `Design.md` + D10 交互规范
- bid-reference 招引/培育章节（业务真源）

## 4. Definition of Done

见 registry `ENT-MOD-RECRUIT-V1-HIFI.definition_of_done`（8 条）。关键交付：会签单 H-01～H-08 + 预览路由 + 截图 + commit SHA。

## 5. 认领话术

```text
/goal ENT-MOD-RECRUIT-V1-HIFI
监管：human:高颖
HIFI 共决：human:高颖 + human:孔东
仓：demo-ui-topic（main）
必读：ENT-MOD-RECRUIT-V1-HIFI-派单包.md + E-26_E-27-引育推荐 四件套 + Design.md
交付：UI-HIFI-ENT-RECRUIT-R1-会签单.md + Demo commit SHA
注意：两视图对象范围/筛选/模型/结论不得混用
```
