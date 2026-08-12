# DATA-CHAIN-STORAGE-S2-L01 · 派单说明

> **日期**：2026-08-12（**2026-08-13：本单为建表主单**）  
> **Task ID**：`DATA-CHAIN-STORAGE-S2-L01`（backlog · 依赖 S1）  
> **派单人**：`human:淮政玮`  
> **监管 / 建表 Owner**：`human:李伟`（须本人确认或亲自建）  
> **执行**：`data-agent` / `human:李伟`  
> **强度**：ponytail **lite**（文档）+ 建表实施按 **full**

---

## 1. 目标

在 S1 会签后：

1. 落地 sources / etl / seeds 文档  
2. **按三方在线文档在 Demo ODS 建表**（表名 + 字段与 md-extract 一致）

```text
在线文档(md-extract 产业链要素库)
  → CREATE TABLE @ demo_gkxlumenx_ods
  →（后续）模拟 GDF → demo_dwd / ads …
```

---

## 2. 建表真源（唯一）

| 优先级 | 路径 |
|---|---|
| 权威 | `third-party-source/doc/*.xlsx`（市场研究…汇总表等） |
| **日常建表读取** | `doc/md-extract/_csv/市场研究（金融、宏观行业、行业分析、产业链）数据汇总表__产业链要素库.csv` |
| 对照 | 同目录 `.md` / sheet「产业链要素库」 |
| 禁止 | `gkx-mysql-raw`；Wave A 未对齐草稿 |

可参考企业侧实现：`demo-algo-ent-analysis/entan/llm_ods/schema.py`（从 CSV 解析 → DDL）；产业链可新脚本或复用同一模式，**Owner = 李伟**。

落库：`demo_gkxlumenx_ods`（已存在且已授权 `gkxlumenx`）。  
Demo 技术主键可用 `_demo_id`（与 ENT 一致），**业务列名不得改写约定英文字段**。

---

## 3. DoD

### A. 文档

- [ ] `sources/inventory.md`：产业链 ODS 表级清单（表名来自 md-extract）+ 真源入口  
- [ ] `etl/pipeline-demo-mock.md`（或等价）：命名与入口  
- [ ] `seeds/README.md`：覆盖矩阵骨架  

### B. 建表（必做 · 李伟负责）

- [ ] 按产业链要素库 CSV **创建（或更新）约定表**于 `demo_gkxlumenx_ods`  
- [ ] 字段类型/可空/主键语义与在线文档一致（冲突以 xlsx 裁决）  
- [ ] 交：建表脚本路径 + `SHOW CREATE TABLE` / 表清单探测摘要（handoff）  
- [ ] **零**写入 `gkxlumenx_ods` 正式库  

### C. 收尾

- [ ] handoff · 李伟确认 · 放行 S3  

---

## 4. 禁止

- 只写 inventory 不建表  
- 从正式 ODS 抄 as-built 当约定结构  
- 密钥入库  

---

## 5. 认领（S1 done 后）

```text
认领 DATA-CHAIN-STORAGE-S2-L01
claimed_by=human:李伟（或 agent:data-agent）
supervised_by=human:李伟
强度：ponytail lite（文档）/ 建表按 full
目标：md-extract 产业链要素库 → demo_gkxlumenx_ods 建表
```

**汇总**：[`CHAIN-STORAGE-S1-S4-DISPATCH-2026-08-12.md`](./CHAIN-STORAGE-S1-S4-DISPATCH-2026-08-12.md)
