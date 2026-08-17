# ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01 · 派单说明

> **日期**：2026-08-14  
> **Task ID**：`ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01`（registry · **integration** · 待侯佳伟签 `approved`）  
> **派单人**：`human:淮政玮`  
> **监管 / 会签 Owner**：`human:侯佳伟`  
> **执行**：`architect-agent`（起草）或 `human:侯佳伟`（签字权）  
> **强度**：ponytail **off**（definition / 会签，不写业务代码）  
> **汇总**：[`SVC-STORAGE-S1-S4-DISPATCH-2026-08-14.md`](./SVC-STORAGE-S1-S4-DISPATCH-2026-08-14.md)

---

## 1. 目标

新建 `storage/SVC/`，完成 `01-data-flow.md` 会签，**明确 ODS 建表真源 = 三方在线文档**，放行 S2（按文档在 `demo_*` **核对/补齐**，复用 ENT 机构主表，禁止再建一套）。

本单只做 **S1：骨架 + 数据流图会签**，不写 DDL、不灌细表、不改 E7 产品包。

---

## 2. 必读（按序）

| 序 | 路径 | 用途 |
|---:|---|---|
| 1 | `data/data-design/storage/README.md` | 体系规范（写作顺序、决策 #5/#6） |
| 2 | `storage/ENT/`（模板）+ `storage/CHAIN/00-context.md` + `01-data-flow.md` | 同构样例 |
| 3 | `architecture-baseline.md` | D3 ADS / D6 Nebula / D7 工厂 |
| 4 | `storage/platform/minio.md` | 平台 MinIO（只引用） |
| 5 | `agent-handoffs/产品整体定义/E7-产业服务链分析/README.md` | 产品边界（输入，不重跑） |
| 6 | `third-party-source/doc/md-extract/` · 国内机构要素库 | ODS 约定入口 |
| 7 | `客户决策清单跟踪表.md` §2.ae | Q-SVC-010 等开放项 |

**不要**当会签真源：`SVC-DATA-ANALYSIS-L01-数据分析报告.md`（仅开放项备忘）、`gkx-mysql-raw` as-built、`服务机构域数据库设计(v1).md`（S4 再 stub）。

---

## 3. 交付

### 3.1 目录骨架

```text
data/data-design/storage/SVC/
├── README.md
├── CHANGELOG.md
├── 00-context.md
├── 01-data-flow.md          ← 会签主件
├── sources/                 占位
├── etl/                     占位（可先链 ENT/CHAIN 的 pipeline-demo-mock 口径）
├── seeds/                   占位
└── stores/                  占位
```

并更新 `storage/README.md`：范围扩到 **SVC 同构域**。

### 3.2 `00-context.md` 必须写清

- 域内 / 域外：功能设计、指标口径正文不进本树  
- **不复制** `dwd_org_base_info`；机构主体权威 = ENT  
- Demo 主路径：md-extract → `demo_*` ODS → ETL 模拟 GDF  
- 关系库仅 MySQL；图谱仅 NebulaGraph  

### 3.3 `01-data-flow.md` 会签动作

1. 三张图：批处理主链 / 在线读路径 / 对象产物  
2. 每图表：生产者 \| 消费者 \| 触发 \| 失败语义 \| 禁止事项（禁止空白「待填」无说明）  
3. 写死：Demo ODS 表名字段 = `doc/md-extract`；落 `demo_gkxlumenx_ods`；禁止正式 ODS  
4. 圈定层：`OPEN-SVC-FLOW-*` 纳入 Q-SVC-010（阻断级，不伪闭合）  
5. frontmatter：`signoff_status` / `signoff_by` / `signoff_at`（人签后才 `approved`）  
6. 勾选会签清单；写明放行 S2（S2 必须按在线文档建表）  

### 3.4 Handoff

路径：`agent-handoffs/服务机构-SVC/ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01.md`

含：决议、基线对照、开放项、下游 S2 放行或暂缓、`ponytail: off`、签字。

---

## 4. 禁止

- 以 live as-built / L01 实查当 ODS 真源  
- 本单执行 DDL（DDL 在 S2），但不得写「等现网表结构」替代在线文档  
- 替甲方拍板准入口径；把六类主表标成已批准  
- 写 Java / Python / 前端；改 E7 五件套  

---

## 5. DoD

- [ ] `storage/SVC` 骨架 + `01-data-flow` 三图与失败语义  
- [ ] 流图写死 ODS 真源 = 在线文档；Demo = `demo_gkxlumenx_ods`  
- [ ] `00-context` 写清与 ENT 共用机构主数据  
- [ ] `OPEN-SVC-FLOW-*` 至少含 Q-SVC-010  
- [ ] `storage/README.md` 已登记 SVC  
- [ ] handoff 放行 S2：**必须按在线文档建表**  
- [ ] 人签 `signoff_by` 后才标 approved  

---

## 6. 认领（registry 建单后）

```text
认领 ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01
claimed_by=human:侯佳伟
supervised_by=human:侯佳伟
强度：ponytail off
```
**已认领**（2026-08-14 · coordinator_dispatch）。

---

## 7. 会话提示词（可贴）

```text
/goal architect-agent
身份：架构师。维护存储流图与基线，不写业务代码、不写 DDL。
任务：ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01
强度：ponytail off
仓：gkx-orchestration（仅文档；cicd skip_design_only）

目标：同构 storage/ENT 与 storage/CHAIN，新建 storage/SVC/，完成 S1。
交付：
1. storage/SVC 骨架（README / 00-context / 01-data-flow / sources·etl·seeds·stores 占位）
2. 01-data-flow.md 三图（批处理主链 / 在线读路径 / 对象产物），每图含 生产者|消费者|触发|失败语义|禁止事项
3. ODS 真源写死：权威 = third-party-source/doc/ xlsx；优先读 md-extract/版权人才、企业机构、政策数据汇总表（国内机构要素库）；Demo 落 demo_gkxlumenx_ods；禁止正式 ODS、禁止 gkx-mysql-raw as-built 当建表真源
4. 00-context 写清：SVC 不复制 dwd_org_base_info；机构主体权威在 ENT；本域只保留服务机构圈定规则、关系、本域 ADS/ES/图谱切片
5. OPEN-SVC-FLOW-*：至少纳入 Q-SVC-010（准入无主路径，阻断级，不伪闭合）、Q-SVC-009（industry 承诺 vs 文档）
6. 更新 storage/README.md 登记 SVC 同构域
7. handoff：agent-handoffs/服务机构-SVC/ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01.md

必读（按序）：
- data/data-design/storage/README.md
- storage/ENT/（模板）+ storage/CHAIN/00-context.md + 01-data-flow.md
- architecture-baseline.md
- E7：agent-handoffs/产品整体定义/E7-产业服务链分析/README.md
- L01 仅作开放项备忘：data-design/服务机构/SVC-DATA-ANALYSIS-L01-数据分析报告.md
- 客户决策清单跟踪表.md §2.ae

禁止：DDL；stores 细表标 approved；续写 L01；以现网探库替代 md-extract；替甲方拍板准入口径。
会签：frontmatter 待 human 签字后再标 approved；未签字不得放行 S2。
```
