# E7-政策分析 · V1 Demo 实现切片 1（对象流骨架）Handoff

- 日期：2026-08-05 ｜ 执行：agent:frontend ｜ 监管：human:高颖
- 阶段：`v1_hifi_round1`（前置：四件套冻结 + UX-SPEC `ready_for_v1`，validate_ux_spec.py = UX_SPEC_OK）
- 仓库：`repos/demo-ui-topic`（main 直推）

## 本切片范围与实现

| Frame | 内容 | 状态 |
|---|---|---|
| F-POL-00 | `/policy/search` 政策查询（ElementSearchWorkbench 共享壳；智能/查政策/高级筛选三模式；最近检索；结果卡仅「加入对比篮/已加入」，无深度分析） | verified |
| F-POL-CMP | 系统对比篮政策 Tab 激活（独立容量 50、去重、篮内搜索/全选、「发起分析」Modal 三任务分发） | verified |
| F-POL-01/02/03 门禁 | 分发上下文门禁 + 空态按篮 count 分支 + 「来自对比篮 · 调整对象」上下文条 + URL `policy_ids[]` 恢复 | verified |
| 路由/菜单 | IA 契约路由恢复（三分析页、门户六页直连、`/policy/maintenance`）；侧边栏「政策分析」六项；旧 policy-center 受控重定向 | verified |
| 三分析页内容 | 沿用旧原型内容（GAP-E7-S2-ANALYSIS-REBUILD：四态壳 + SystemTaskLayer + 报告合同下切片重构） | implemented |
| 门户/OPS | 路由恢复；入篮按钮与 ENT-OPS 复用为下切片 GAP | implemented |

## 产物清单

- 新增：`src/app/pages/policy/{policyAnalysisRegistry.ts, PolicyCompareBasketPanel.tsx, PolicyAnalysisGate.tsx, PolicyTopicSearchPage.tsx}`
- 修改：`src/app/pages/enterprise/EnterpriseCompareBasketPage.tsx`（政策 Tab）、`src/app/routes.tsx`、`src/app/components/Layout.tsx`
- 测试：`tests/policy-dispatch-contract.test.mjs`（10/10）、`tests/policy-dispatch-pointer.test.mjs`（Playwright 真实指针，1920/1680/1440）
- 证据：`交付覆盖/E7-政策分析/evidence/*.png`（12 张：查询入篮 / 篮分发 Modal / 分发后分析页 / 空态）

## 验收证据

- `npm run build` ✅ ｜ `npm run design:check` ✅ ｜ 复合 label 审计 ✅（6 文件 0 违规）
- 契约测试 `node --experimental-strip-types tests/policy-dispatch-contract.test.mjs` → 10 pass
- 指针测试 `node tests/policy-dispatch-pointer.test.mjs`（dev server :4177）→ 三视口通过，无 pageerror、无横向溢出
- 已知环境问题：存量 `tests/compare-basket-store-migration.test.mjs` 在无 `--experimental-strip-types` 下本就失败（非本次引入）

## 架构合规自检（公约 §2）

1 算法只在 Python ✅（纯前端 Mock）｜2 调用链 ✅（未新增后端调用）｜3 图谱 ✅ 不涉｜4 可观测 ✅ 沿用 observability｜5 CI/CD ✅ push 后自动｜6 demo2 只读 merge ✅ 不涉｜7 共享聚合核心 ✅ 不涉｜8 Mock 先行 ✅（确定性 seed）｜9 D8 Arco/token ✅（design:check 绿）｜10 D9 ✅（新页未新增统计指标；追溯挂载齐）｜11 D10 ✅（Arco 语义、键盘/焦点沿用共享组件）

## 后续切片（已登记 GAP）

1. 三分析页四态壳重构 + SystemTaskLayer + 报告合同（GAP-E7-S2-ANALYSIS-REBUILD）
2. 门户六页入篮（GAP-E7-S2-PORTAL-BASKET）；维护管理 ENT-OPS 复用（GAP-E7-S2-OPS-REUSE）
3. 新挂载双模式 DOM 证据补齐（GAP-E7-S2-DUAL-MODE-EVIDENCE）

恢复命令：`cd repos/demo-ui-topic && npx vite --port 4177 --strictPort` 后跑两个 policy 测试。
