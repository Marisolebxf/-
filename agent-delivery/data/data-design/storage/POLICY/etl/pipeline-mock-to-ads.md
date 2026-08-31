# 管道 · Mock 直写 ADS（政策）

```yaml
---
doc_id: POLICY-ETL-MOCK-ADS
element: POLICY
role: etl
status: not-built
version: "2026-08-31"
updated: 2026-08-31
engine: mysql
task_id: DATA-POLICY-STORAGE-ETL-FILL-L01
---
```

## 结论：本域无此旁路

CHAIN / ENT 有「Mock 直写 ADS」可选旁路，用于 ODS→DWD 工厂未通时先验证 Java 只读面。**政策域不设该旁路**，因为政策的 Mock 走的是另一条路。

## 政策的 Mock 是「贴源 Mock」

政策 Mock 写的是 **ODS 与 DWD**，不是 ADS：

```text
mockgen/generate.py  →  ODS dwd_policy_base  →  DWD policy_base_info
                                                      │
                                        A/B/C/D 各模块照常算  ↓
                                                    ADS policy_*
```

ADS 永远由 [`pipeline-dwd-to-ads.md`](./pipeline-dwd-to-ads.md) 从当前 DWD 算出来，**没有任何模块把 Mock 直接灌进 ADS**。这样做的好处是 Mock 数据同样经过完整算法链，指标口径与 live 完全一致，不会出现"两套 ADS 结构"。

详见 [`pipeline-demo-mock.md`](./pipeline-demo-mock.md)（E0→E1→T2→L3→L4 分解）与 [`pipeline-ods-to-dwd.md`](./pipeline-ods-to-dwd.md)。

## 容易混淆的两个「mock」

| 概念 | 位置 | 行为 | 是否落库 |
|---|---|---|---|
| **贴源 Mock** | `polan/mockgen/` | 造政策明细，写 ODS/DWD | ✅ 落 ODS/DWD |
| **查询期降级** | `polan/metrics/metrics.py` | ADS 表空或不可用时返回 mock 值 + 口径标注 | ❌ **不回写 ADS** |

第二个不是 ETL，是读侧兜底。前端据此显示 🧪 MockBadge（D4 `mock`）。

## 禁止

新建 Mock → ADS 直写脚本；把查询期降级结果回写 ADS；用 `policyData.js`（展示原型 fixture）当 ADS 数据源。
