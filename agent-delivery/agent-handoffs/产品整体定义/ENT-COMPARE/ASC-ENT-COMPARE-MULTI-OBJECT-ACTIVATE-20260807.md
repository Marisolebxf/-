# ASC-ENT-COMPARE-MULTI-OBJECT-ACTIVATE-20260807

> **状态**：`pending_approval`（不可当作已批准范围）
> **提出**：agent:product-agent · 2026-08-07
> **待签**：体验 Owner 高颖 · 合规 PM 郭万迎
> **架构会签建议**：徐滕强 / 李伟
> **关联四件套**：ENT-COMPARE v2.9

## 1. 决策摘要

在既有 `ASC-ENT-COMPARE-MULTI-OBJECT-SHELL-20260731` 五 Tab 壳层上，激活以下对象域的真实存储、来源加入与同域分发：

| Tab 标签 | tab_key | object_type | 容量 | 状态 |
|---|---|---|---|---|
| 企业 | enterprise | enterprise | 50 | 已启用（既有） |
| 产业 | industry | industry, industry_chain | 各 50 | **本次激活** |
| 政策 | policy | policy | 50 | **本次激活** |
| 服务机构 | service_org | service_org | 50 | **本次激活** |
| 区域 | region | region | 50（目标） | 仍开发中占位 |

## 2. 关键规则

1. 「共 X 项」统计全部已启用类型合计。
2. 产业 Tab 同屏管理产业与产业链；禁止混选后发起分析；角标为二者合计 / 单池 max。
3. 跨 Tab 混选与跨域联合分析仍禁止；篮内不生成任何分析结果。
4. Demo as-built 仅作对齐证据，不能单独构成批准。
5. 不新增、删除或合并 Bid 叶子；不重新宣告门 1 通过。

## 3. Demo 证据路径

- `repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseCompareBasketPage.tsx`
- `repos/demo-ui-topic/src/app/pages/industry-center/IndustryCompareBasketPanel.tsx`
- `repos/demo-ui-topic/src/app/pages/policy/PolicyCompareBasketPanel.tsx`
- `repos/demo-ui-topic/src/app/pages/service-center/ServiceOrgCompareBasketPanel.tsx`

## 4. 签字区

| 角色 | 姓名 | 结论 | 日期 |
|---|---|---|---|
| 体验 Owner | 高颖 | ☐ 同意 / ☐ 驳回 | |
| 合规 PM | 郭万迎 | ☐ 同意 / ☐ 驳回 | |
| 架构（可选） | 徐滕强 / 李伟 | ☐ 会签 | |

签字后将 TRACE 中本 ASC 的 `approval_status` 改为 `approved`，并回填 `confirmed_by` / `confirmed_at`。
