# DEC-CHAIN-PORTAL-OVERVIEW-CLUSTER-SELECTOR-20260817

> **模块**：CHAIN-PORTAL-OVERVIEW / 产业链总览（全站选择器同源）  
> **决策日**：2026-08-17  
> **起草**：`human:李伟`（FDE · `CHAIN-INDUSTRY-CLUSTER-SUPP-L01`）  
> **批准人**：`human:高颖`（体验 Owner）  
> **补签日**：2026-08-17  
> **补签记录**：同日 `human:李伟` 指示按已完成、以高颖身份补签。  
> **性质**：修订 `DEC-CHAIN-PORTAL-OVERVIEW-L0-L1-20260806` 的 **D-SELECTOR**；**不改** D-DRILLDOWN  
> **状态**：已批准（2026-08-17）  
> **2026-08-17 晚修订**：分析对象允许只选集群；高级筛选级联到链最后一层。见同目录 `DEC-CHAIN-PORTAL-OVERVIEW-SCOPE-GRAIN-20260817.md`（规则已起草，未改代码）。D-DRILLDOWN 仍不改。  
> **存储真源**：`data/data-design/storage/CHAIN/stores/mysql/dim-industry-cluster.md`  
> **口径**：`客户决策清单跟踪表.md` **Q068** 🟡

---

## 与 2026-08-06 已批 DEC 的关系

| 层 | 内容 |
|---|---|
| 源需求 | 招标「20+8 / 八大未来」原文不改 |
| 2026-08-06 已批 | 顶部**只选 L0**，写入 `industry_id`；对比篮 `industry`；全景默认 L1 可下钻 |
| **本轮决策（已批准）** | 顶部改为 **先选产业集群（15）→ 再选该集群下 L0**；查数仍用 L0；D-DRILLDOWN 不变 |

---

## 决策摘要

| ID | 结论 |
|---|---|
| **D-SELECTOR-R1** | 顶部两级：集群 `cluster_id`（15 个，`CL-SEI-*` / `CL-FUT-*`）→ 该集群映射的 L0 `industry_id`（INB）。五个 Tab 共享这两级。 |
| **D-EMPTY** | 集群枚举始终在；映射 0 条 L0 时停在空态「无相关产业数据」，不造假、不藏集群。 |
| **D-ROUTE** | 分析页主参：`cluster_id` + `industry_id`。旧只带 `industry_id` / `chain_id` / `future_industry_code` 只读兼容，能解析到集群或 L0 则回填。 |
| **D-BASKET** | 对比篮仍写入当前 **L0**（`elementKey=industry`），不写集群、不写 `industry_chain`。 |
| **D-DICT** | 下拉读集群 API（dim），**禁止**用国标 `meta/industries`（`code_nic`）冒充 15 个集群。 |
| **D-DRILLDOWN** | **维持** 2026-08-06：选定 L0 后全景默认 L1，可下钻。不在顶部直接选 L1。 |

---

## D-SELECTOR-R1｜顶部两级选择器

1. 第一级：15 个产业集群，顺序与 storage §3 一致（先 10 战新，再 5 未来）。可检索。  
2. 第二级：仅列出该集群当前映射的 L0；无映射则第二级空，内容区走 D-EMPTY。  
3. 企业 / 产业链 / 展示 / **政策 / 服务链**读同一份目录（P7）。  
4. Tab 内不得再提供第三套产业名单或直接选 L1。  
5. 切集群：清空当前 L0、下钻栈、局部选中；有默认推荐 L0 且仍属于新集群时可用，否则停在空态等用户选。  
6. 切 L0：保留 Tab，清空下钻栈与旧局部状态（同 2026-08-06）。  
7. 全景标题仍是 `{L0产业名称}产业链全景`；集群名可作面包屑前缀，不替代 L0 标题。

---

## 废止的现行句（仅产品口，不改招标）

- 「顶部只选 L0 / 与企业查询所属产业同口径的单级 Select」→ 改为集群 → L0。  
- 「八大未来产业作为现行下拉或统计上限」→ 改为 15 个集群；「覆盖未来产业数」分母先仍按 **5 个未来集群**（实施方案 P3）。  
- 国标行业字典冒充集群下拉。

---

## 落地

| 产物 | 动作 |
|---|---|
| 本目录 USM / IA / TRACE / Wireframe / UX-SPEC / FUNC-DESIGN | 升版记录本决策（已批准） |
| E2 其余叶子 + CHAIN-OPS | 入口选择器同源；CMS 对象键仍是 L0 |
| E-31～E-35 + p2a | 页面上下文改为集群；对比/排名按 15 |
| Demo / lumen | 选择器叶可开；无本单 ID 不改业务仓 |
