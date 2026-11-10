# 603-STRUCT-FDE · 波次 C · 轻档两签

总单：`POL-L2-PC1-STRUCT-FDE-L01`。定档：**轻**（见 `603-STRUCT-FDE-B-读法方案.md`）。  
多身份对抗会签；异议数为零的会签无效（见 `gkx-fde-design-change/审稿硬清单.md`）。

## C1 · arch-agent（起草收口）

改 `sdd/l2/POL-L2-PC1-STRUCT-ARCH.md`：**一小段**标明治理页可触发单条抽取，以说明书 2026-11-10「#### 603」为准；旧「只读呈现、不重跑 / 排除本叶触发 parse/clauses」标已被取代。**不改**主读时序（仍 `governance/results`）、不重开 GDF、不迁中台。同步 `POL-L2-PC1-STRUCT-API.md` 声明复用 `POST /display/v1/policy/parse/clauses`。不 commit。

## C2 · product-agent（审 arch）

审读法方案 + ARCH/API 补段。按审稿硬清单 product 五问。至少一条风险或需确认项。写 `会签/603-STRUCT-FDE-C-审稿-product.md`。不改说明书（真源已定）。

## C3 · arch-agent（审 product）

审说明书「#### 603」+ 线框。按 arch 五问。至少一条风险或需确认项。写 `会签/603-STRUCT-FDE-C-审稿-arch.md`。不改正文功能点。

## C4 · 知会（短）

`会签/603-STRUCT-FDE-C-知会-data.md`、`…-api.md`、`…-algorithm.md` 各写：本波无新表/无新 metric；两表 Wave0 seed；抽取复用 parse/clauses；知悉影响清单即可。

## 闭合条件

审稿异议由起草方逐条「采纳/驳回+理由」写回 `603-STRUCT-FDE-C-异议闭合.md`。无未闭合停机项 → 可派实现（波次 D）。  
「已结构化是否允许再抽」若监管人已拍，写入闭合单默认；未拍则实现前再卡一次。
