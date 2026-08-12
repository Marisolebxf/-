# ENT 存储 · 徐滕强任务看板（2026-08-13 更新）

> **派单人**：`human:淮政玮`  
> **监管**：`human:徐滕强`  
> **口径真源**：`storage/ENT/etl/pipeline-demo-mock.md`  
> **Demo 库（维持短期，不再扩其它 gkxlumenx_*）**：  
> `demo_gkxlumenx_ods` / `_dwd` / `_ads` / `_dim`（已建齐 + 授权 `gkxlumenx`）  
> CFG 等平台库 **共享正式**，不建 demo。

---

## 任务一览（更新后）

| # | Task ID | 状态 | 优先级 | 说明 |
|---|---|---|---|---|
| A | `DEMO-ENT-DEMO-DB-TRIPLE-L01` | **库侧已完成 → 待腾强签收** | P0 | 建库/授权/默认切换已由淮政玮落地；含 DIM |
| B | `DEMO-ENT-UI-SEED-ODS-L01` | **ready · 优先认领** | P0 | 灌数主路径必须只写 **demo_***；ODS=md-extract |
| ① | `DATA-ENT-STORAGE-OPS-OPEN-L01` | ready | P1 | OPEN-01~04；可与 B 并行 |
| ② | `DATA-ENT-STORAGE-STORES-APPROVE-L01` | ready | P1 | stores 细表 approved |
| ③ | `DEMO-ENT-LLM-ODS-EXPAND-L01` | ready | P1 | 扩招投标/产业链/风险等；**只灌 demo_ods** |

---

## 建议顺序

```text
A 签收确认（库已齐）
→ B 灌数 UI + run_all 默认 demo_*（P0）
→ ①② 文档/开放项（可并行）
→ ③ 扩覆盖（建议 B 合入后）
```

---

## 铁律（给执行方）

1. 开发默认读写 **仅** `demo_gkxlumenx_{ods,dwd,ads,dim}`  
2. ODS 表名/字段以 **`doc/md-extract`** 为准（权威 xlsx）  
3. 禁止默写 `gkxlumenx_ods/dwd/ads/dim`；对账须显式开关  
4. 不新建其它 `demo_gkxlumenx_*`（app/cfg/bi…）

分册：各 `*-派单说明.md` · 库执行记录 `DEMO-ENT-DEMO-DB-TRIPLE-L01.md`
