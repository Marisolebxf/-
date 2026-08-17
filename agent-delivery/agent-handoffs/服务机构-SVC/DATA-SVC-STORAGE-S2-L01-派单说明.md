# DATA-SVC-STORAGE-S2-L01 · 派单说明

> **日期**：2026-08-14  
> **Task ID**：`DATA-SVC-STORAGE-S2-L01`（registry · **claimed** · 依赖 S1 已满足）  
> **派单人**：`human:淮政玮` / 放行开 S2：`human:侯佳伟`（2026-08-14）  
> **监管 / 建表 Owner**：`human:侯佳伟`  
> **认领**：`claimed_by=agent:data-agent` · `supervised_by=human:侯佳伟` · `claim_type=coordinator_dispatch`  
> **S1 实稿约束**：`storage/SVC/00-context.md` §2 · `01-data-flow.md` §6/§7（核对/补齐，禁止第二套主表）  
> **执行**：`data-agent`（本会话）  
> **前置**：`ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01` · `01-data-flow` **approved**（侯佳伟 · 2026-08-14 · 本地未 push）  
> **强度**：ponytail **lite**（文档）+ 建表实施按 **full**  
> **汇总**：[`SVC-STORAGE-S1-S4-DISPATCH-2026-08-14.md`](./SVC-STORAGE-S1-S4-DISPATCH-2026-08-14.md)

---

## 1. 目标

在 S1 会签后：

1. 落地 sources / etl / seeds 文档（`etl/pipeline-demo-mock.md` S1 已锁定口径，本单补脚本入口与对列证据）  
2. **按三方在线文档在 Demo ODS 核对/补齐**（表名 + 字段与 md-extract 一致）

```text
在线文档(md-extract 国内机构要素库)
  → 复用 ENT 已建表 @ demo_gkxlumenx_ods（禁止再 CREATE 一套 dwd_org_base_info）
  → 缺文档列（含 industry*）则按 md-extract 补列（Q-SVC-009：live 无列 ≠ 文档无列）
  →（后续）模拟 GDF → ENT 机构 DWD → SVC 圈定（待核验）→ demo_dwd / ads …
```

机构主体权威在 ENT；本域只做依赖清单 + 圈定/关系管道准备。**禁止**平行 `svc_org_base`。

---

## 2. 建表真源（唯一）

| 优先级 | 路径 |
|---|---|
| 权威 | `third-party-source/doc/*.xlsx`（版权人才、企业机构、政策数据汇总表） |
| **日常建表读取** | `doc/md-extract/_csv/版权人才、企业机构、政策数据汇总表__国内机构要素库.csv` |
| 对照 | 同目录 `.md` / sheet「国内机构要素库」 |
| 禁止 | `gkx-mysql-raw`；L01 现网实查 DDL；Wave A 未对齐草稿 |

可参考：`demo-algo-ent-analysis/entan/llm_ods/schema.py`（从 CSV 解析 → DDL）。  
落库：`demo_gkxlumenx_ods`。Demo 技术主键可用 `_demo_id`（与 ENT 一致），**业务列名不得改写约定英文字段**。

---

## 3. DoD

### A. 文档

- [ ] `sources/inventory.md`：本域依赖的 ODS 表级清单（表名来自 md-extract）+ 真源入口 + 与 ENT 共用/本域独有标注  
- [ ] `etl/pipeline-demo-mock.md`：回填 S2 入口脚本路径（S1 已锁定口径，勿另写第二套主路径）  
- [ ] `seeds/README.md`：覆盖矩阵骨架（含「待核验」圈定样例，不伪闭合 Q-SVC-010）  

### B. 建表（必做）

- [ ] 按国内机构要素库 CSV **核对 ENT 已建约定表**于 `demo_gkxlumenx_ods`；缺列（含 `industry*`）按文档 **补列**，禁止再建一套主表  
- [ ] 字段类型/可空/主键语义与在线文档一致（冲突以 xlsx 裁决；live 缺列不得反向删文档列）  
- [ ] 交：建表脚本路径 + `SHOW CREATE TABLE` / 表清单探测摘要（handoff）  
- [ ] **零**写入 `gkxlumenx_ods` 正式库  

### C. 收尾

- [ ] handoff · Owner 确认 · 放行 S3  

---

## 4. 禁止

- 只写 inventory 不交核对/补列证据  
- 再建一套 `dwd_org_base_info` / `svc_org_base`  
- 从正式 ODS / L01 抄 as-built 当约定结构  
- 密钥入库  
- 把 business_scope 词典写成已批准准入主路径  

---

## 5. 认领（已办 · 2026-08-14）

```text
认领 DATA-SVC-STORAGE-S2-L01
claimed_by=agent:data-agent
supervised_by=human:侯佳伟
claim_type=coordinator_dispatch
强度：ponytail lite（文档）/ 建表按 full
目标：md-extract 国内机构要素库 → demo_gkxlumenx_ods 核对/补齐（复用 ENT，禁止第二套主表）
```

**已认领**（`claimed` · 锁约 4h）。侯佳伟新开 **data-agent** 会话，贴下方「会话提示词」。

---

## 6. 会话提示词（可贴）

```text
/goal data-agent
身份：数据工程。落地 sources/etl/seeds + Demo ODS 核对/补齐；不写业务 Java/前端；不伪闭合 Q-SVC-010。
任务：DATA-SVC-STORAGE-S2-L01
执行人：agent:data-agent · 监管：human:侯佳伟（已认领 · claimed）
派单：human:侯佳伟 · coordinator_dispatch（S1 会签放行后开 S2）
强度：ponytail lite（文档）/ 建表 full
仓：gkx-orchestration（文档）+ demo-algo-ent-analysis（建表脚本，可复用 entan/llm_ods）

前置已满足：
- ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01 · 01-data-flow signoff_status=approved · human:侯佳伟 · 2026-08-14
- Demo ODS 实例 = demo_gkxlumenx_ods（与 ENT 同实例）

交付：
1. sources/inventory.md：本域 ODS 表级清单（md-extract 国内机构要素库）+ 真源入口 + 与 ENT 共用/本域独有
2. etl/pipeline-demo-mock.md：回填 S2 脚本入口（勿另写第二套主路径）
3. seeds/README.md：覆盖矩阵骨架（含待核验圈定样例；不伪闭合 Q-SVC-010）
4. 按 md-extract CSV 核对 ENT 已建表 @ demo_gkxlumenx_ods；缺列（含 industry*）按文档补列；禁止再建一套 dwd_org_base_info / svc_org_base
5. handoff：建表脚本路径 + SHOW CREATE / 表清单摘要；零写入正式 gkxlumenx_ods；确认后放行 S3

必读：
- agent-handoffs/服务机构-SVC/DATA-SVC-STORAGE-S2-L01-派单说明.md
- storage/SVC/00-context.md · 01-data-flow.md §6/§7
- storage/ENT/sources/inventory.md · etl/pipeline-demo-mock.md
- doc/md-extract/_csv/版权人才、企业机构、政策数据汇总表__国内机构要素库.csv
- 可复用：repos/demo-algo-ent-analysis/entan/llm_ods/

禁止：只写 inventory 无核对证据；第二套主表；以 gkx-mysql-raw / L01 当建表真源；密钥入库；把临时准入口径写成已批准。
```
