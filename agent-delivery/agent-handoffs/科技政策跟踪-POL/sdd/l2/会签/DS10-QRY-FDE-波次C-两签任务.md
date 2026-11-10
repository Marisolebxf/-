# DS10-QRY-FDE · 波次 C · 轻档两签

总单：`POL-L2-DS10-QRY-FDE-L01`。定档：**轻**（见 `DS10-QRY-FDE-B-读法方案.md`）。  
多身份对抗会签；异议数为零的会签无效（见 `gkx-fde-design-change/审稿硬清单.md`）。

## C1 · arch-agent（起草收口）

改 `sdd/l2/POL-L2-DS10-QRY-ARCH.md`：**一小段**标明蓝色中枢交互以说明书 2026-11-10「#### 197」为准；旧「点示例即搜 / 热门当关键词搜 / 最近在结果区」标已被取代。**不改**读口、时序、资源表。不 commit。

## C2 · product-agent（审 arch）

审读法方案 + ARCH 补段。按审稿硬清单 product 五问能答的答。至少一条风险或需确认项。写 `会签/DS10-QRY-FDE-C-审稿-product.md`。不改说明书（真源已定）。

## C3 · arch-agent（审 product）

审说明书「#### 197」+ 线框。按 arch 五问。至少一条风险或需确认项。写 `会签/DS10-QRY-FDE-C-审稿-arch.md`。不改正文功能点。

## C4 · 知会（短）

`会签/DS10-QRY-FDE-C-知会-data.md`、`…-algorithm.md` 各写：本波无读口/无新 metric，知悉影响清单即可。

## 闭合条件

审稿异议由起草方逐条「采纳/驳回+理由」写回同目录 `DS10-QRY-FDE-C-异议闭合.md`。无未闭合停机项 → 可派实现（波次 D）。
