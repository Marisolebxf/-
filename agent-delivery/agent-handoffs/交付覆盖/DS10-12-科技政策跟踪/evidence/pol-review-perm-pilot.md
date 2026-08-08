# Evidence · 政策模块评审/权限试点（图2）

日期：2026-08-08  
仓：`repos/demo-ui-science`

## 范围铁律

- 顶栏图2 **仅** `isPolicyTopic(activeTopic)` 时显示  
- 评审开关 / `ReviewOnly` **仅** `policy-tracking` 角标  
- 权限锁态 **仅** 侧栏「科技政策跟踪」组 + 政策页 `PolicyRouteGuard`  
- 其它六大模块仍用图1 `userRoles`，行为不变  

## 预览

```bash
cd repos/demo-ui-science && npm run dev
# 进入「科创政策全景」→ 右上角应变为图2
# 关「内部评审模式」→ KPI 旁 ⓘ/🧪/⚠️ 消失
# Level=L0 → 「政策效果推演」锁态；Screen=大屏 → 推演/核增锁态
# 回到「科技全域态势」→ 右上角恢复图1
```
