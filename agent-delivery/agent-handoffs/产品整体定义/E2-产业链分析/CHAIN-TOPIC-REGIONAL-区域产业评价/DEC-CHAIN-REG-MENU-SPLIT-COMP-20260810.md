# DEC · 区域产业竞争力评价拆为独立 L2

| 字段 | 值 |
|---|---|
| ID | `DEC-CHAIN-REG-MENU-SPLIT-COMP-20260810` |
| 日期 | 2026-08-10 |
| 状态 | **已拍板（产品）** |
| 范围 | `demo-ui-topic` 侧栏 L2 + 区域评价工作台 Tab；不改 lumen 正式仓 |

---

## 1. 决策

| 侧栏 L2 | `workspace` | 页内 Tab | 菜单位置 |
|---|---|---|---|
| **区域产业指数评价** | `index` | 区域产业指数评价 · 分析记录 | 产业周期分析之后（原位） |
| **区域产业竞争力评价** | `competitiveness` | 区域产业竞争力评价 · 分析记录 | **深圳产业决策之后** |

路由仍共用 `/industry-center/regional`；权限码复用 `MENU_CHAIN_REGIONAL`。

---

## 2. 兼容

- 旧链 `?tab=index|competitiveness|records`（无 workspace）：按 tab 推断；`records` 默认 `index`。
- 对比篮分组与侧栏对齐；`buildIndustryAnalysisUrl` 写入对应 `workspace`。
