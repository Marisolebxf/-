# ENT 存储可选收尾 · 最粗派单汇总（供审）

> **日期**：2026-08-12  
> **派单人**：`human:淮政玮`  
> **监管 / 落地 Owner**：`human:徐滕强`（三单均同）  
> **拆法**：最粗 **3 包**（另已派出灌数 UI = 第 4 单，不在本批新建）  
> **状态**：registry **ready** · **待淮政玮检查后知会腾强 / 再 push 编排仓**

---

## 任务一览

| # | Task ID | 标题 | Agent | 类型 | 优先级 |
|---|---|---|---|---|---|
| 已派 | `DEMO-ENT-UI-SEED-ODS-L01` | system-test「灌数据」接 llm_ods 主路径 | algorithm | feature | P0 |
| ① | `DATA-ENT-STORAGE-OPS-OPEN-L01` | OPEN-01~04 合包（调度/MinIO/前缀/SLA） | data | tech_task | P1 |
| ② | `DATA-ENT-STORAGE-STORES-APPROVE-L01` | stores 细表结构评审 → approved | data | definition | P1 |
| ③ | `DEMO-ENT-LLM-ODS-EXPAND-L01` | llm_ods 扩场景 + MinIO 样例 + Nebula 定名 | algorithm | feature | P1 |

分册说明：

- [`DEMO-ENT-UI-SEED-ODS-L01-派单说明.md`](./DEMO-ENT-UI-SEED-ODS-L01-派单说明.md)（已推）
- [`DATA-ENT-STORAGE-OPS-OPEN-L01-派单说明.md`](./DATA-ENT-STORAGE-OPS-OPEN-L01-派单说明.md)
- [`DATA-ENT-STORAGE-STORES-APPROVE-L01-派单说明.md`](./DATA-ENT-STORAGE-STORES-APPROVE-L01-派单说明.md)
- [`DEMO-ENT-LLM-ODS-EXPAND-L01-派单说明.md`](./DEMO-ENT-LLM-ODS-EXPAND-L01-派单说明.md)

---

## 建议执行顺序（不硬挡）

```text
① OPS OPEN（可并行找 GDF/平台填数）
② stores approved（文档评审，可与 ① 并行）
已派 UI 灌数（P0，优先）
③ Demo 扩表（软依赖 UI 主路径；硬依赖 LLM-ODS 已 done）
```

---

## 检查清单（给你）

- [ ] 三包边界是否过粗 / 是否要把 OPEN-01 拆给 GDF 单独
- [ ] ③ 是否应硬依赖 `DEMO-ENT-UI-SEED-ODS-L01`
- [ ] 监管是否一律 `human:徐滕强`（① 是否改 GDF 主责 + 徐会签）
- [ ] 标题 / DoD / 优先级是否改口
- [ ] 通过后：编排仓 commit + push `origin/dev` + 飞书知会

---

**本协调会话不执行 ①②③ 业务改造**（仅派单草稿）。
