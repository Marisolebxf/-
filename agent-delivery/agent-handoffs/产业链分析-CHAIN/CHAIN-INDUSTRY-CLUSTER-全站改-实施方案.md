# 产业集群全站改 · 实施方案（改前范围，供淮政玮过目）

> **状态**：波次 A 收口；波次 B Java 已落；DDL 已 apply 到 `demo_gkxlumenx_dim`（`111.198.38.90:34306`，15/12/8 pending）。选择器 DEC 高颖已补签。 · 2026-08-17  
> **任务**：`CHAIN-INDUSTRY-CLUSTER-SUPP-L01`（in_progress · `human:李伟`）  
> **目的**：开干前把**整个项目**要改的地方摊开，避免专题先换、企业/展示漏改，避免文档和代码各说各的。  
> **存储真源**：[`storage/CHAIN/stores/mysql/dim-industry-cluster.md`](../../data/data-design/storage/CHAIN/stores/mysql/dim-industry-cluster.md)  
> **任务说明书**：[`CHAIN-INDUSTRY-CLUSTER-全站改-任务说明书.md`](./CHAIN-INDUSTRY-CLUSTER-全站改-任务说明书.md)  
> **口径**：Q068 🟡；对外目录锁定深圳 3.0 **10+5**。招标原文不改写。  
> **本轮不做**：改 DWD `industry_chain`、进 `gkxlumenx_cfg`、投 Nebula Cluster 点、无 registry 叶改代码。

淮政玮 2026-08-17 17:01：**registry 只建一条**「产业集群功能设计和实现的补充任务」。§5 是单内波次，不是 10 个 task-id。未建该单、未点头前不起子智能体、不改 demo/lumen。

---

## 0. 一句话

不是「专题下拉换一下」。是：**产品定义先改口，demo 按新口刷新，中间链提供同一份 15 个集群，lumen 复刻 demo，产业 / 企业 / 展示 / 政策 / 服务链同一天换源。**

文档和代码必须同一份目录。谁还写「八大未来」当现行下拉，谁就是漏改。

---

## 1. 产品上要先想清楚（高颖 / 淮哥拍）

这些不定，前端会各改各的。

| # | 问题 | 团队默认（可改） | 不定会漏在哪 |
|---|---|---|---|
| P1 | 选择器几层 | **2026-08-17 晚修订**（`DEC-…-SCOPE-GRAIN-20260817`）：分析对象 = 集群 + **可选** L0（只选集群查该集群下全部）；高级筛选 = 集群一直选到该分支最后一层。无映射仍空态。白天「必须再选 L0 / 自动带第一项」作废 | 有人只换名单、或把 `CL-*` 当产业编码去查 |
| P2 | 路由主参 | 分析页：`cluster_id` + `industry_id`（L0）。CMS / 对比篮 / 全景对象仍是 L0 | URL、书签、Tab 继承对不齐 |
| P3 | 「各未来产业」统计分组 | **对比/排名用 15 个集群**（没数的集群仍占位或标无数据）。「覆盖未来产业数」分母先仍按 **5 个未来集群** 计，不把 10 个战新算进去；metric 文案跟着改 | E-32/E-35 还按 8 根柱子 |
| P4 | 招标 20+8 / 旧八大 | 源需求保留；本轮决策 = 10+5；五件套写「源需求 / 本轮决策 / Q068」三层，不把招标改成 10+5 | 合规被说超范围 |
| P5 | 旧 `future_industry_code` | 兼容只读一版，能解析到集群或 L0；新写入用 `cluster_id` / `industry_id` | 明星企业、深圳介绍书签全断 |
| P6 | 维护管理 | 加「产业集群映射」一项：改映射，不增删 15 个名字（换政策版除外） | 只有前台、没有改映射的地方 |
| P7 | 政策 / 服务链是否跟 15 | **跟。** 2026-08-17 `human:李伟`：E7 政策分析、E7 服务链（门户+分析）产业下拉与企业/产业链/展示同一份 15。政策「技术领域」不换。旧 `ind-*` 只读兼容，对不上不猜 | 政策配置页、服务链门户/分析仍写八大或 `ind-ic` |

**选择器 DEC**：`DEC-CHAIN-PORTAL-OVERVIEW-CLUSTER-SELECTOR-20260817.md` **高颖已补签**（2026-08-17；李伟指示按已完成、以高颖身份签）。选择器叶可开。

---

## 2. 修改范围总表（防漏）

### 2.1 产品定义五件套（先改口，再改界面）

五件套 = USM / TRACE / IA / Wireframe（有交互规范的加 UX-SPEC）。只改「目录 / 选择器 / 统计分组 / 空态」，不重写模块故事。

**产业链 E2（全部叶子都有顶部或对象产业）**

| 包 | 必改点 |
|---|---|
| `CHAIN-PORTAL-OVERVIEW` 五件套 + FUNC-DESIGN + DEC | 顶部从「只选 L0」改为「集群 → L0」；字典接口改为集群 API |
| `CHAIN-TOPIC-PANORAMA` | 主对象仍是确认后的链；入口产业口径跟总览 |
| `CHAIN-TOPIC-DIAGNOSIS` / `ANALYSIS` / `REGIONAL` / `SHENZHEN` | 分析对象选择器同源 |
| `CHAIN-OPS-维护管理` 五件套 + 能力全清单 | 新增映射维护项；产业选择先集群 |

**企业 E-31（现行口是「八大未来」）**

| 包 | 必改点 |
|---|---|
| `USM/IA/TRACE/Wireframe-E31` | 页面上下文从「八大未来」改为「10+5 集群」 |
| `E-32` 纪要/字段 | 排名/对比按 15 集群；覆盖数口径见 P3 |
| `E-33` KEYPANO | 「当前未来产业 + 当前产业链」→「当前集群 + 当前 L0」 |
| `E-34` STAR | 选择器与 `future_industry_code` 规则按 P5 |
| `E-35` SHENZHEN | 目录不得把 8 写成上限；对比按 15 |

**必须同步的会话/规格（否则文档和 demo 会打架）**

- `p2a-session/DECISIONS.md`、`PLAN.md`、`企业模块深化UE规格.md`（多处已确认「八大」）
- Q049（`future_industry_code` 与 E-32/E-34 同源）旁注指向 Q068
- `产业维护管理-能力全清单.md` 加映射项

**政策 E7 + 服务链 E7（2026-08-17 李伟：跟 15）**

| 包 | 必改点 |
|---|---|
| `E7-政策分析` 五件套 | 产业锚点 / 对比篮产业 Tab / 配置页下拉改读集群 API；废 `POLICY_SCOPE_INDUSTRIES` 的 8 个 `ind-*`。**技术领域** `POLICY_TECH_FIELDS` 不换 |
| `SVCCHAIN-PORTAL` | 「八大产业领域字典」→ 15 集群；与政策扶持「同款级联」= 同一集群 API |
| `SVCCHAIN-ORG-ANALYSIS` / `ECOSYSTEM` / `RECOMMEND` | 分析侧产业上下文同源；无映射空态 |

展示侧 `DS10-12` 政策跟踪五件套无产业目录下拉，本轮不改。

**展示系统**

- 展示侧多数没有和专题同结构的五件套。本轮：**有功能设计/IA 的改口；没有的以 demo 常量为准，并在本方案登记，避免 lumen 复刻时抄回八大。**
- 已扫到写死八大的：`demo-ui-science` 的 `futureIndustryOptions.js`、`futureIndustryChain.ts`、`FilterBar.tsx`、科技创新评估页。人才态势等 `industryOptions` 要核是不是同一份目录（国标行业的不要误换）。

**不改**

- `bid-reference/*.md` 原文
- 已会签 `01-data-flow.md`
- 图谱 SAD / Nebula schema（本轮）

### 2.2 UI Demo 原型（按新五件套刷新）

| 仓 | 必改 | 典型漏点 |
|---|---|---|
| `demo-ui-topic` | 共享 `filterOptions.ts` 的 `industryOptions` / `futureIndustryDomainOptions`；企业四 Tab；产业链各页；**政策** `POLICY_SCOPE_INDUSTRIES` / `PolicyAnalysisConfigPanel`；**服务链** `service-portal` 与分析侧产业选择；维护管理加映射页 | 现在同时存在「八大未来」、另一套 12 名、政策 `ind-*`，都要废，改读同一 mock/API |
| `demo-ui-science` | 评估范围、态势 FilterBar、未来产业链环节勾选 | 文案「八大未来产业（上中下游全环节）」 |
| `demo-ui-system-test` | 维护管理：集群 15 + 映射到 L0 | 空 CMS 表不是这个需求 |

Demo 未接 Java 前：mock **必须**与 storage §3/§4 同编码（`CL-SEI-*` / `CL-FUT-*` / INB L0），禁止再发明一套 slug。

### 2.3 中间实现链

| 层 | 改什么 | 不改什么 |
|---|---|---|
| DIM | 建 `industry_cluster` + `industry_cluster_map`，灌 15 + 种子映射 | DWD 十四表 |
| Java | **新**只读：集群列表、按集群展开 L0、覆盖状态。维护写接口只改 map | 国标 `meta/industries`（`code_nic`）不要冒充集群 |
| 现有专题/企业 API | 入参仍吃 `industry_id[]`（L0）。前端先展开再调 | ADS 主键不改成 `cluster_id` |
| Python | 若 `/internal/.../meta` 还在吐旧产业列表，改为读 dim 或停用该列表 | 不在算法里写 15 个名字 |
| CMS | 继续按 L0 `industry_id` 挂文案 | 不要按集群建一套 CMS |
| 图谱 | 不投影 | — |

### 2.4 Lumen 复刻

| 仓 | 对齐谁 |
|---|---|
| `lumen-ui-topic` | 复刻已刷新的 `demo-ui-topic`（选择器 + 维护页），禁止另写名单 |
| `lumen-ui-science-pc` | 复刻已刷新的 `demo-ui-science` 产业勾选 |
| `lumen-svc-platform` | 实现 §2.3 Java 契约；lumen 只打 `gkxlumen-*`（D12） |

现扫：`lumen-ui-topic` / `lumen-ui-science-pc` 几乎还没有「八大」常量——**漏改风险是复刻时把 demo 旧八大抄进去**。所以 demo 必须先换源，lumen 才能跟。

---

## 3. 文档 ↔ 代码 对齐规矩

1. 名字和编码只出自 `dim-industry-cluster.md` §3/§4。  
2. 五件套改完再刷 demo；demo 刷完再 lumen。允许同一波并行，但 **禁止 lumen 先于 demo 发明交互**。  
3. 每个前端 PR 自检：仓内不得再出现「八大未来产业」作为**现行**下拉或统计上限（历史说明、招标引用可以留）。  
4. 关闭评审模式后 DOM 不得泄漏 `CL-SEI` / `Q068` 等治理字样（D9 门控照旧）。

---

## 4. 防漏清单（开干后逐条打勾）

- [x] DEC 选择器补签（`human:高颖` · 2026-08-17）  
- [x] E2 六个产品包 + OPS 能力清单（总览五件套已改口；其余叶子 USM 已挂 Q068；OPS 增 C7）  
- [x] E-31 父包 + E-32～E-35（目录/选择器/分组/空态已改口，故事未重写）  
- [x] p2a 三份「八大」已确认句（历史保留 + 文首本轮决策）  
- [x] Q049 旁注 Q068  
- [x] P7：政策 / 服务链跟 15（李伟 2026-08-17）  
- [x] E7 政策五件套正文（已挂 Q068；查询粒度 + 旧 `ind-*` 只读兼容已写入）  
- [x] SVCCHAIN 四包正文（门户现行「八大领域」选择器已改 15 集群；分析侧 `field-*` 字典不换）  
- [x] `demo-ui-topic` `filterOptions.ts` 两套名单  
- [x] `demo-ui-topic` 企业四 Tab + 产业链各页 + **政策配置 + 服务链门户/分析** + 维护  
- [x] `demo-ui-science` 评估/态势/环节  
- [x] `demo-ui-system-test` 映射页  
- [x] 2026-08-18：联调台（系统和算法）产业链选择器 + 算法 mock/门禁（`demo-algo-science` INB L0；`demo-algo-ent-analysis` DOMAINS）  
- [x] dim 表 + 种子（`demo_gkxlumenx_dim` @ `111.198.38.90:34306`：cluster=15 / map=12 / pending=8）  
- [x] Java 集群 API（`demo-svc-platform` `gkx-innov` 已落；含 `POST .../resolve-scope`）  
- [ ] `lumen-ui-topic` / `lumen-ui-science-pc` 复刻  
- [x] 三个端空态（有集群、无 L0；三层门禁：UX / `canQueryAds` / Java `grain=empty`）  
- [x] 回归：旧 `future_industry_code` / 政策 `ind-*` URL（只读回填；对不上不猜；`industry-analysis-scope.check.mjs` 覆盖）  
- [x] 2026-08-18 夜终核：science 不偷 L0 / 图谱与评估不装有数；E-32 契约对齐 15 集群；`getChainNodes` 无映射空；死页 Introduction 不再按旧八大中文 key 崩  
- [x] 2026-08-18：分析页出数前 `fetchResolveScope`（本地核禁生成；点生成再问 Java）；science 评估 NewPage 同接；网关补企业前缀  

---

## 5. 单内波次（registry 只有 1 条）

**唯一任务**：`CHAIN-INDUSTRY-CLUSTER-SUPP-L01` · 产业集群功能设计和实现的补充任务。

```text
波次 A  产品口（可并行）
        E2 五件套 + DEC + OPS 清单
        E-31～E-35 + p2a 八大句
        E7 政策 + SVCCHAIN 四包（跟 15）
        （展示无独立五件套则写进本单变更说明）

波次 B  数据 + 契约（建表后出接口）
        dim 建表灌种 → Java 集群 API → Demo 种子

波次 C  Demo 刷新（三端同时，一起收）
        demo-ui-topic / demo-ui-science / demo-ui-system-test

波次 D  Lumen 复刻
        lumen-ui-topic / lumen-ui-science-pc（只复刻 C）

波次 E  对账
        三个端同一份 15；空态；旧 URL；文档无现行「八大下拉」
```

子智能体按波次并行，**handoff 仍写在这一条 task-id 下**，并回链 storage / 本方案 / 任务说明书，保证以后能溯源整段设计。

专题 / 企业 / 展示 / 政策 / 服务链不允许做成互不等待的「单独干完」。

---

## 6. 请淮哥拍的三件事

1. 范围：§2 已含产业 / 企业 / 展示 / **政策 / 服务链**（李伟 2026-08-17 点名补进）。人才态势、国标 NIC、政策技术领域不换。若还有漏模块请再点名。  
2. 产品默认：§1 的 P1～P7，尤其 P3（15 根柱 vs 覆盖数仍算 5 个未来）。  
3. 节奏：registry 只建本补充任务；单内按 A→E 推进。

点头前：只改编排仓文档。点头后：先 A+B，再 C 三端并行，再 D 复刻。
