# ENT-COMPARE Demo v1.5 交接

## 当前结果

- 覆盖项：6；`verified=6`，`blocked=0`，`manual_review=0`。
- 对比篮已移除来源筛选；卡片已移除统一社会信用代码与来源标签。
- 企业名称和企业类型旁的筛选恢复动作已统一为“重置”，不再显示“清空筛选”。
- 已选工具栏已改为“已选 X 家 / 取消选择 / 发起分析 / 加入招引候选 / 加入培育候选”。
- “发起分析”打开“选择分析任务”浮层；选择 3+2 种任务时不跳转，点击“下一步：前往配置”后才分发。
- 对比篮有对象时使用稳定高度工作区：筛选区固定顶部、企业列表独立滚动、批量操作栏固定底部；短列表与长列表均已验证。
- “对比篮说明”已挂到共享评审模式，业务模式关闭后不渲染。
- 分发目标页已显示来源、企业数和返回入口；返回后恢复筛选、勾选与滚动位置。
- 分发目标页自动接管企业对象且不强制重选；3 种企业评估和 2 种风险洞察始终保留“从对比篮带入”，支持直接进入后的导入或主动调整；综合竞争力等待用户主动开始分析。
- “查看引育名单”可定向进入招引或培育候选 Tab 并查看已加入对象。
- 对比篮容量按定义对齐 50 家。

## 关键实现文件

- `repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseCompareBasketPage.tsx`
- `repos/demo-ui-topic/src/app/pages/enterprise/CompareBasketHandoffBar.tsx`
- `repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseCenterPage.tsx`
- `repos/demo-ui-topic/src/app/pages/enterprise/compareBasketReturnContext.ts`
- `repos/demo-ui-topic/src/app/pages/enterprise/compareBasketTargetContext.ts`
- `repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseCapabilityEvaluation.tsx`
- `repos/demo-ui-topic/src/app/pages/enterprise/CompetitivenessAnalysis.tsx`
- `repos/demo-ui-topic/src/app/pages/enterprise/SupplyChainAnalysis.tsx`
- `repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseRecommendation.tsx`
- `repos/demo-ui-topic/src/app/components/common/CompareBasket.tsx`

## 验证与续接

- 验证详情：`validation-report.md`
- 机器覆盖源：`implementation-coverage.yaml`
- 恢复命令：`cd /Users/ying/Documents/codex/gkx-lumen/repos/demo-ui-topic && npm run dev -- --host 0.0.0.0 --port 4177`
- 当前变更未提交；未修改任务状态。
