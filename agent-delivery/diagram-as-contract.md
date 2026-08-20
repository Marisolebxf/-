# 图即契约（Diagram as Contract）

```yaml
---
doc_id: ARCH-DIAGRAM-CONTRACT
role: architecture-convention
status: draft
version: "2026-08-19"
updated: 2026-08-19
signoff_owner: architect
signoff_status: draft
---
```

> **一句话**：人决策画在边上（实线 / 虚线 / 禁止）；AI 负责让图、表、代码同构；coordinator **不收**没有该层图的架构 / 存储 / 功能架构 / 模块实现 / 联调单。  
> **读者**：architect / coordinator / 各 Lead；data / api / frontend / algorithm / integration / ux / product agent。  
> **维护**：architect-agent；变更记本文 §8 + `architecture-baseline.md` §8。  
> **金牌样板**：[`data/data-design/storage/SVC/01-data-flow.md`](data/data-design/storage/SVC/01-data-flow.md)（四图 + 四列表 + 会签只放行拓扑）。  
> **本页不新增 D 决策**。调用链 / ADS / Nebula / D12 仍以 [`architecture-baseline.md`](architecture-baseline.md) 为准。

---

## 0. 粒度（模块 ≠ 叶子 ≠ 存储域）

规程里的「模块」= **能开 DG、有一份产品包的验收父节点**（定义规程 TRACE `module` / `DG-{模块}`），不是招标叶子，也不是 registry 一张 task。图层各自对齐，**禁止按叶子复制 L2**。

| 词 | 粒度 | 例子 | 图怎么挂 |
|---|---|---|---|
| **模块** | 验收父节点；五件套 / `DG-{模块}` / 门 I1 纪要 | `E-31 企业发展`、`DS-25`、`E7 政策` | **L1** IA 首页 `{MODULE}-IA-FUNC` |
| **叶子** | bid 功能点，挂在父 TRACE `leaves` | `E-32 企业整体概况` | 不另起产品包，**不另画 L2** |
| **工程 leaf** | `task-registry` 一张可认领单 | `ENT-JAVA-xxx` | **L4** 可按 `{TASK}-SEQ`；同主路径多叶可共用一张 |
| **存储域** | 数据产品边界（`storage/{域}/`） | `ENT` / `CHAIN` / `SVC` | **L2** 每域一套流图，**多模块共用** |

**L2 域映射（产品模块 → 认哪张已签流图）**

| 产品模块（父节点）落点 | 认的 L2 | 禁止 |
|---|---|---|
| 企业检索 / 企业分析 / 企业发展（E-31 等） | `ENT-STORAGE-FLOW` | 再出「E-31 专用 ODS→ADS」 |
| 专题全景 / 产业链 | `CHAIN-STORAGE-FLOW` | 平行产业链 space / 第二张 G |
| 服务机构 / 产业服务链 | `SVC-STORAGE-FLOW` | 平行 `svc_org_base` / 按 50100 菜单拆流图 |
| 政策 / 人才 / 尚未建域 | 先挂已有域并写 N/A 理由，或另开 **域级** 流图叶 | 按 DS-xx / E-32 **叶子**各画一张工厂图 |

**L3** 跟实现批次，通常对齐模块或要素域；有 ARCH-IMPL 才要。不要给每个叶子各画一张。  
**L0** 全项目一张。**I2-07 的 L0–L4** 是 TRACE **权限档**，与本页图分层同名不同物。

---

## 1. 五层必签图

一张图只答一个问题。已有真源 **只链不复制**。节点名 = `repo-registry` 仓名或运行时服务名（如 `demo-algo-ent-analysis`、`gkxlumen-topic`），禁止写「算法服务」「聚合层」。

| 层 | 人看什么 | 落点 | 图种 | 谁签 | 何时必有 |
|---|---|---|---|---|---|
| **L0 全局微服务** | 仓/服务边界、调用链、D12 | [`architecture-baseline.md`](architecture-baseline.md) §1 · `ARCH-TOPO-LUMEN` | `flowchart` | 架构 | 改拓扑 / 新服务 / 破 D12 嫌疑时改此图，禁止各**模块**另画全局图 |
| **L1 功能架构** | 角色 × 能力 × 入口，不画表 | **模块** IA 首页 · `{MODULE}-IA-FUNC` | `flowchart` | 产品 + UX | 新模块 PACK / 改主路径；`{MODULE}` = 验收父节点。版式参照 [`跨系统-知识图谱/02-概要设计.md`](agent-handoffs/产品整体定义/跨系统-知识图谱/02-概要设计.md) |
| **L2 存储/数据流** | 谁写谁读、工厂主链、F 实线 / P 虚线 | `storage/{域}/01-data-flow.md`（**按存储域**，见 §0） | `flowchart`（可拆批处理 / 在线 / 对象 / Demo） | 架构（流图 Owner） | 无会签流图不得把细表标 approved；**禁止按 bid 叶子复制** |
| **L3 模块实现** | 本**模块**仓内组件、读写面、禁碰清单 | `ARCH-IMPL-{模块}` · `{MODULE}-IMPL-ARCH` | `flowchart` | 架构 + 实现 Lead | 门 3 后有 ARCH-IMPL 才要；对齐父模块/要素域，不对齐 E-32 级叶子 |
| **L4 联调时序** | 一次用户动作：FE → 网关 → Java → Python → 存储 | 联调单 / 工程 leaf · `{TASK}-SEQ` | `sequenceDiagram` | 前后端 Lead + QA | 门 **I2-11**；可按 task，同主路径可共用 |

**边的语义（全层通用）**

| 画法 | 含义 |
|---|---|
| 实线 | 本总控 / 本叶 **授权施工** 的路径 |
| 虚线 | 目标态或他期路径，**本单禁止施工** |
| 图下「禁止事项」 | 与虚线同等效力；口头「先做着」无效 |

---

## 2. 图下四列表（L2 / L3 / L4 必附）

与 [`storage/README.md`](data/data-design/storage/README.md) §6 同构，升为全层：

| 生产者 | 消费者 | 触发 | 失败语义 | 禁止事项 |
|---|---|---|---|---|
| 谁写 / 谁发起 | 谁读 / 谁依赖 | 批 / 在线 / 按钮 / 任务 | 失败时保留什么、禁止半成品冒充成功 | 点名禁写的仓、库、边 |

L0 / L1 可用更短的「职责 | 不做」表（见知识图谱 SAD），但 **禁止只有散文没有图**。

**真源**：git 内 Mermaid。飞书 / 纪要只贴截图，不当源头。会签打开 **渲染后的图**，口头只改边；会后 AI 改 Mermaid + 四列表，人再签 frontmatter。不接受「文档整体 LGTM」。

---

## 3. 派单 / handoff / 拒收

**`/goal`（架构 / 存储流图 / ARCH-IMPL / 联调 / 功能 IA 首页）缺则拒派：**

```text
图：必含 {diagram_id}。先改图再改文；图文冲突以图为准。必读 agent-delivery/diagram-as-contract.md。
```

定义类（ux / architect / product）**禁止**用 ponytail 强度行压掉图。coding 单若改调用链 / 写库方 / 服务边界，必须指向已批准 `diagram_id`，禁止「按常识重画」。

**handoff 必填**

| 字段 | 值 |
|---|---|
| diagram_id | 本叶改动的图 ID（可多个） |
| 图 diff | 三行内：加了哪条边 / 哪条改虚线 / 禁止事项是否变 |
| 会签态 | `draft` / `approved`（只抄 frontmatter，禁止自填绿） |

**coordinator / architect 拒收（`needs-revision`）**

1. 该层规定要图，正文无 ` ```mermaid `
2. 节点名对不上仓名 / 服务名
3. L2/L3/L4 有图无四列表（或 L0/L1 无「职责\|不做」）
4. 长文改了拓扑，图未改
5. 在业务仓 README 另画一套与 L0 / 本域 L2 冲突的全局图（只允许链接 + 本模块 L3/L4）
6. 用 fixture / 前端目录充数代替图上的写库方

**门对照**（规程 v1.0.4 硬闸）：

| 门 | 编号 | 查什么 |
|---|---|---|
| 门 I1 开工 | **I1-11** | 该产品**模块**落到的 **存储域** L2 已签（多模块共用，不新建叶子流图）；本 Sprint 含 ARCH-IMPL 则 **L3** 已落盘。L1 在定义包/IA |
| 门 I2 联调 | **I2-11** | **工程 leaf** 或模块联调单的 L4 `sequenceDiagram` 与 walkthrough / 一条 `traceId` 同构 |

见 [`产品实现规程.md`](产品实现规程.md) §5.2 / §6.2。I1-08 仍只查 ADS/Mock/贴源；I2-01 仍只查调用链铁律。

---

## 4. 图目录（已存在则引用）

| diagram_id | 层 | 文件 | 会签 |
|---|---|---|---|
| `ARCH-TOPO-LUMEN` | L0 | `architecture-baseline.md` §1 | 基线锁定（D1–D12） |
| `ENT-STORAGE-FLOW` | L2 | `data/data-design/storage/ENT/01-data-flow.md` | `human:淮政玮` · 2026-08-12 approved |
| `CHAIN-STORAGE-FLOW` | L2 | `data/data-design/storage/CHAIN/01-data-flow.md` | `human:李伟` · 2026-08-13 approved |
| `SVC-STORAGE-FLOW` | L2 | `data/data-design/storage/SVC/01-data-flow.md` | `human:淮政玮` · 2026-08-19 approved |
| `SVC-STORAGE-LINEAGE` | L2 表级血缘 | 同上 §1.1 | 2026-08-20 选 B 增补；不改 FLOW 拓扑边 |
| `TOPIC-SHARED-FUNC` | L1 | `agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/03-总体设计-共享底座-图.md` | draft · 专题六模块挂底座 |
| `TOPIC-SHARED-IMPL` | L3 | 同上 | draft · 专题运行时 |
| `TOPIC-SHARED-SEQ-B` / `TOPIC-SHARED-SEQ-JOB` | L4 | 同上 | draft · 全景 B 面 / 生成分析 |

新图：**先占 ID 再画**，命名 `{域或模块}-{ROLE}`，ROLE ∈ `FLOW` / `FUNC` / `IMPL` / `SEQ`。禁止文件名带版本号。

历史长文 **不回溯补图**。新开存储 / ARCH-IMPL / 联调 / IA 首页按本页执行。周扫（可选）：规定路径缺 mermaid 报给 architect，禁止一上来全库补图。

---

## 5. 明确不做

- 不上 Draw.io / Figma 架构源、不上自动出 PNG 流水线
- 不为飞书不能渲 Mermaid 换真源
- 不把每张 handoff 做成图册；一叶只碰它声明的 `diagram_id`
- 不为好看把已会签图拆成 20 张（SVC 四图已经够用）
- 不把 USM 验收句、指标 8 件套、DDL 细表改成图来「代替」
- **不按 bid 叶子 / DS 单页复制 L2 流图**（认 §0 域映射）
- 不因本页跳过 D8 / D9 / D10 / 可观测 / handoff

---

## 6. 落地

| 步 | 做什么 | 状态 |
|---|---|---|
| 1 | 本页 + 挂 `architecture-baseline` / `storage/README`；handoff 加图字段；派单手册 §9.0d | 已落 |
| 2 | 下一张 ARCH-IMPL / 存储流图 / 联调单按本页出；人会签只投图 | 待执行 |
| 3 | 门 I1/I2 独立编号硬闸 | **已做**：规程 v1.0.4 · **I1-11 / I2-11** |
| 4 | 粒度钉死（模块/叶子/域） | **已做**：本页 §0；规程 v1.0.5 §0.1 |

---

## 7. 人怎么对 AI 说话（示例）

- 「`SVC-STORAGE-FLOW` 里 50892 保持虚线，本总控不施工。」
- 「L4 缺失败边：Java 5xx → 前端空态，不是扫 DWD。」
- 不要回「你再写清楚一点」却不点边。

---

## 8. 变更

| 日期 | 说明 |
|---|---|
| 2026-08-19 | 初稿：五层图种、四列表、会签只投图、派单/AV 拒收；样板 = SVC 流图 |
| 2026-08-19 | 门对照升硬闸：规程 v1.0.4 **I1-11 / I2-11** |
| 2026-08-19 | **§0 粒度**：模块=验收父节点；L2 按存储域共用；禁止按叶子补流图 |
| 2026-08-19 | 样例：专题共享底座图册 `03-总体设计-共享底座-图.md`（`TOPIC-SHARED-*`） |
