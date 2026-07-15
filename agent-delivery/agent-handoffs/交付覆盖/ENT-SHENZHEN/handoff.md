# ENT-SHENZHEN handoff

## 当前状态

- 已在既有 E-35 v0.3 基础上，按 v0.4 四件套完成领域概况语义修订。
- URL 当前专题产业优先初始化；无有效值时回退到数量最高产业。
- 第三产业选择会被阻止并提示；最后一个已选产业不可取消；选择不改变 KPI、领域、规模和重点企业。
- 历史趋势与顶部深圳市说明模块已归入评审态；业务态仅保留当年数量对比并占满整行。
- 领域标题旁原始需求说明已归入评审态；“当前产业链”“当前产业”两处重复文案已删除。
- “产业链领域映射覆盖”固定 76%/32% 及进度条已删除；业务态改为当前去重领域/环节集合的“已识别领域/环节 X 个”，评审态补充 Q049 口径说明。
- 浏览器验证集成电路为 15 个、海洋经济为 9 个；业务态未检出 Q049、覆盖率标签或进度条。
- 数量对比、历史趋势和规模分析统一预留纵轴单位空间，避免“家”被画布上边界裁切。
- 重点企业区已改为“可见横向 Tabs + 可搜索更多产业”；当前产业从更多入口选择后进入可见 Tab，一次只展示当前产业企业卡。
- 覆盖状态：3 项 `verified`，趋势选择、领域结构、重点企业导航共 3 项 `manual_review`。

## 写入文件

- `repos/demo-ui-topic/src/app/pages/development/ShenzhenEnterprises.tsx`
- `repos/demo-ui-topic/src/app/pages/development/shenzhenEnterpriseTrend.ts`
- `repos/demo-ui-topic/src/app/pages/development/shenzhenEnterprisePresentation.ts`
- `repos/demo-ui-topic/tests/e35-shenzhen-trend-selection.test.mjs`
- `repos/demo-ui-topic/tests/e35-shenzhen-layout-navigation.test.mjs`
- `repos/demo-ui-topic/tests/enterprise-overview-e33-e35.test.mjs`（仅更新 E-35 合同断言）
- `repos/demo-ui-topic/docs/superpowers/plans/2026-07-15-e35-selected-industry-trend.md`
- `repos/demo-ui-topic/docs/superpowers/plans/2026-07-15-e35-layout-navigation-v03.md`
- `repos/demo-ui-topic/docs/superpowers/specs/2026-07-15-e35-domain-summary-semantics-design.md`
- `repos/demo-ui-topic/docs/superpowers/plans/2026-07-15-e35-domain-summary-semantics.md`
- `gkx-orchestration/agent-delivery/agent-handoffs/产品整体定义/E-31-企业发展/E-35-深圳企业介绍/` 四件套（TRACE v0.4）
- 本目录五份交付覆盖文件

## 恢复命令

```bash
cd /Users/ying/Documents/codex/gkx-lumen/repos/demo-ui-topic
node --experimental-strip-types tests/e35-shenzhen-trend-selection.test.mjs
node --experimental-strip-types tests/e35-shenzhen-layout-navigation.test.mjs
node tests/enterprise-overview-e33-e35.test.mjs
npm run design:check
npm run build
```

## 下一步

- 产品方查看 `e35-v04-domain-summary-review.png` 与 `e35-v04-domain-summary-business-marine.png`，确认“已识别领域/环节 X 个”的信息层级；同时保留既有趋势与导航视觉复核。
- Q049 闭合后，用正式 metric_id、ADS 来源与历史序列替换 `ENT-SHENZHEN-TREND-20260715`，保持当前交互状态机不变。

## 门禁

Q049 未闭合，“已识别领域/环节 X 个”只描述当前 DEMO 数据集合，不是产业链映射覆盖率；本次交付不代表 Gate 1、正式指标或数据接入通过。当前修改保留在既有 `dev` 工作区，未提交、未合并、未推送。
